"""Thumbnail generation engine.

Public entry point: `generate()`. Builds prompts based on mode, calls Gemini,
writes outputs + metadata to disk.

Modes:
- clone: copy a reference thumbnail's style, apply face + title
- preset: use a named preset template
- hybrid: ref optional, overrides allowed, custom instructions
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from PIL import Image

from prompts.style_presets import PRESET_LABELS, render_preset

Mode = Literal["clone", "preset", "hybrid"]

ROOT_DIR = Path(__file__).parent
OUTPUTS_DIR = ROOT_DIR / "outputs"

NEGATIVE_INSTRUCTIONS = (
    "Do NOT include any of the following under any circumstances: "
    "timestamps, video duration overlays (e.g. '36:20'), time counters, "
    "progress bars, play buttons, YouTube UI elements, subscribe buttons, "
    "channel logos, watermarks, or any text other than the title specified above. "
    "The output must be a clean standalone thumbnail image."
)

from io import BytesIO

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(ROOT_DIR / ".env")

_GEMINI_MODEL = "gemini-3.1-flash-image-preview"


def _gemini_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not set. Copy .env.example to .env and add your key."
        )
    return genai.Client(api_key=api_key)


@dataclass
class GeneratedImage:
    image_bytes: bytes
    output_path: Path
    metadata_path: Path


@dataclass
class GenerationRequest:
    mode: Mode
    face_image_path: Path
    title_text: str
    reference_image_path: Path | None = None
    preset_key: str | None = None
    overrides: dict = field(default_factory=dict)
    variant_count: int = 3


def build_prompt(req: GenerationRequest) -> str:
    """Build the text prompt sent to Gemini for a given request."""
    if req.mode == "preset":
        if req.preset_key not in PRESET_LABELS:
            raise ValueError(f"Unknown preset: {req.preset_key}")
        extra = req.overrides.get("extra_instructions", "") if req.overrides else ""
        base = render_preset(req.preset_key, req.title_text, extra)
        return f"{base} {NEGATIVE_INSTRUCTIONS}"

    if req.mode == "clone":
        return (
            "Create a 1280x720 YouTube thumbnail. "
            "Analyse the layout, typography, colour palette, and composition of "
            "the reference image provided. Recreate that visual style with the "
            "person from the face image provided and the title text: "
            f"\"{req.title_text}\". Match the reference's visual style closely "
            "without copying it verbatim. The person's face must remain recognisable. "
            f"{NEGATIVE_INSTRUCTIONS}"
        )

    if req.mode == "hybrid":
        parts = [
            "Create a 1280x720 YouTube thumbnail.",
            f"Title text to include: \"{req.title_text}\".",
            "Use the person from the face image provided. Keep the face recognisable.",
        ]
        if req.reference_image_path is not None:
            parts.append(
                "Use the reference image provided as a loose style starting point "
                "for layout, typography, and colour — do not copy it directly."
            )
        if req.overrides:
            bg = req.overrides.get("background_color")
            if bg:
                parts.append(f"Background colour: {bg}.")
            pos = req.overrides.get("text_position")
            if pos:
                parts.append(f"Position the title text on the {pos} of the frame.")
            expr = req.overrides.get("face_expression")
            if expr:
                parts.append(f"The person's expression should be {expr}.")
            extra = req.overrides.get("extra_instructions")
            if extra:
                parts.append(extra)
        parts.append(NEGATIVE_INSTRUCTIONS)
        return " ".join(parts)

    raise ValueError(f"Unknown mode: {req.mode}")


def _short_hash(seed: str) -> str:
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]


def _output_paths(req: GenerationRequest, variant_index: int) -> tuple[Path, Path]:
    """Return (image_path, metadata_path) for a given variant index."""
    now = datetime.now(timezone.utc)
    date_dir = OUTPUTS_DIR / now.strftime("%Y-%m-%d")
    date_dir.mkdir(parents=True, exist_ok=True)
    ts = now.strftime("%H%M%S")
    short = _short_hash(f"{req.title_text}|{now.isoformat()}")
    image_path = date_dir / f"{ts}-{short}-v{variant_index}.png"
    metadata_path = date_dir / f"{ts}-{short}.json"
    return image_path, metadata_path


def _write_metadata(
    metadata_path: Path,
    req: GenerationRequest,
    prompt: str,
    output_image_paths: list[Path],
) -> None:
    metadata = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": req.mode,
        "face": str(req.face_image_path.name),
        "reference": str(req.reference_image_path) if req.reference_image_path else None,
        "title": req.title_text,
        "preset": req.preset_key,
        "overrides": req.overrides or None,
        "prompt": prompt,
        "variant_count": req.variant_count,
        "outputs": [str(p.name) for p in output_image_paths],
    }
    metadata_path.write_text(json.dumps(metadata, indent=2))


def _validate_image(path: Path) -> None:
    """Raise ValueError if path is not a readable image."""
    try:
        with Image.open(path) as img:
            img.verify()
    except Exception as e:
        raise ValueError(f"Invalid image at {path}: {e}") from e


def generate(req: GenerationRequest) -> list[GeneratedImage]:
    """Generate thumbnails for the given request."""
    _validate_image(req.face_image_path)
    if req.reference_image_path is not None:
        _validate_image(req.reference_image_path)

    prompt = build_prompt(req)
    client = _gemini_client()

    contents: list = [prompt]
    with Image.open(req.face_image_path) as face_img:
        face_img.load()
        contents.append(face_img.copy())
    if req.reference_image_path is not None:
        with Image.open(req.reference_image_path) as ref_img:
            ref_img.load()
            contents.append(ref_img.copy())

    results: list[GeneratedImage] = []
    output_image_paths: list[Path] = []
    metadata_path_for_batch: Path | None = None

    for variant_index in range(1, req.variant_count + 1):
        image_path, metadata_path = _output_paths(req, variant_index)
        if metadata_path_for_batch is None:
            metadata_path_for_batch = metadata_path

        response = client.models.generate_content(
            model=_GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        image_bytes = _extract_image_bytes(response)
        image_path.write_bytes(image_bytes)
        output_image_paths.append(image_path)
        results.append(
            GeneratedImage(
                image_bytes=image_bytes,
                output_path=image_path,
                metadata_path=metadata_path_for_batch,
            )
        )

    if metadata_path_for_batch is not None:
        _write_metadata(metadata_path_for_batch, req, prompt, output_image_paths)

    return results


def _extract_image_bytes(response) -> bytes:
    """Pull the first inline image out of a Gemini response."""
    for candidate in response.candidates or []:
        for part in candidate.content.parts or []:
            inline = getattr(part, "inline_data", None)
            if inline is not None and inline.data:
                return inline.data
    raise RuntimeError(
        "Gemini response contained no image data. "
        "This usually means the prompt was blocked by safety filters."
    )


def load_recent_generations(limit: int = 10) -> list[dict]:
    """Return metadata for the N most recent generations.

    Each entry is the parsed metadata JSON plus a resolved `output_paths`
    list of absolute `Path` objects.
    """
    if not OUTPUTS_DIR.exists():
        return []

    json_files: list[Path] = []
    for date_dir in sorted(OUTPUTS_DIR.iterdir(), reverse=True):
        if not date_dir.is_dir():
            continue
        json_files.extend(sorted(date_dir.glob("*.json"), reverse=True))
        if len(json_files) >= limit:
            break

    entries: list[dict] = []
    for path in json_files[:limit]:
        try:
            data = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        data["output_paths"] = [path.parent / name for name in data.get("outputs", [])]
        data["metadata_path"] = path
        entries.append(data)
    return entries
