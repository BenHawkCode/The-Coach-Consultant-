"""Streamlit UI for the Thumbnail Generator."""
from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from thumbnail_engine import GenerationRequest, generate, load_recent_generations
from prompts.style_presets import PRESET_LABELS

ROOT_DIR = Path(__file__).parent
FACE_LIBRARY_DIR = ROOT_DIR / "assets" / "ben-faces"

load_dotenv(ROOT_DIR / ".env")

st.set_page_config(
    page_title="TCC Thumbnail Generator",
    page_icon="🎬",
    layout="wide",
)


def _api_key_present() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY"))


def _load_face_library() -> list[Path]:
    if not FACE_LIBRARY_DIR.exists():
        return []
    return sorted(
        p for p in FACE_LIBRARY_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )


def _save_uploaded_face(uploaded_file) -> Path:
    FACE_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    target = FACE_LIBRARY_DIR / uploaded_file.name
    target.write_bytes(uploaded_file.getbuffer())
    return target


def render_sidebar() -> Path | None:
    st.sidebar.header("Face Library")

    faces = _load_face_library()
    if not faces:
        st.sidebar.warning("No faces in library. Upload one below.")

    selected_name = st.sidebar.radio(
        "Select a face",
        options=[p.name for p in faces],
        index=0 if faces else None,
        key="selected_face",
    ) if faces else None

    for face in faces:
        st.sidebar.image(str(face), caption=face.name, width=120)

    uploaded = st.sidebar.file_uploader(
        "Upload new face",
        type=["jpg", "jpeg", "png", "webp"],
        key="face_uploader",
    )
    if uploaded is not None:
        saved = _save_uploaded_face(uploaded)
        st.sidebar.success(f"Saved {saved.name}")
        st.rerun()

    st.sidebar.divider()
    render_history_sidebar()

    if selected_name is None:
        return None
    return FACE_LIBRARY_DIR / selected_name


def render_history_sidebar() -> None:
    st.sidebar.header("Recent generations")
    entries = load_recent_generations(limit=10)
    if not entries:
        st.sidebar.caption("No generations yet.")
        return
    for entry in entries:
        with st.sidebar.expander(f"{entry['timestamp'][:19]} — {entry['title'][:40]}"):
            st.caption(f"Mode: {entry['mode']}")
            for out_path in entry["output_paths"]:
                if out_path.exists():
                    st.image(str(out_path), width=200)


def _run_generation(req: GenerationRequest) -> None:
    """Run generation with UI feedback and render results."""
    try:
        with st.spinner("Generating with Gemini..."):
            results = generate(req)
    except RuntimeError as e:
        st.error(str(e))
        return
    except ValueError as e:
        st.error(f"Invalid input: {e}")
        return
    except Exception as e:  # pragma: no cover - surface unknown API errors to the user
        st.error(f"Generation failed: {e}")
        return

    st.success(f"Generated {len(results)} thumbnail(s).")
    cols = st.columns(len(results))
    for col, result in zip(cols, results):
        with col:
            st.image(result.image_bytes, use_container_width=True)
            st.download_button(
                label="Download PNG",
                data=result.image_bytes,
                file_name=result.output_path.name,
                mime="image/png",
                key=f"dl-{result.output_path.name}",
            )


def render_clone_tab(face_path: Path) -> None:
    st.subheader("Clone a reference thumbnail")
    st.caption(
        "Upload a thumbnail you like. Gemini will copy its style using the "
        "selected face and your title."
    )

    ref_file = st.file_uploader(
        "Reference thumbnail",
        type=["jpg", "jpeg", "png", "webp"],
        key="clone_ref_uploader",
    )
    title = st.text_input("Title text", key="clone_title")
    variant_count = st.slider(
        "Variants", min_value=1, max_value=4, value=3, key="clone_variants"
    )

    can_generate = ref_file is not None and title.strip() != ""
    if not st.button(
        "Generate",
        key="clone_generate",
        type="primary",
        disabled=not can_generate,
    ):
        return

    ref_path = ROOT_DIR / "outputs" / "_uploads" / ref_file.name
    ref_path.parent.mkdir(parents=True, exist_ok=True)
    ref_path.write_bytes(ref_file.getbuffer())

    req = GenerationRequest(
        mode="clone",
        face_image_path=face_path,
        title_text=title.strip(),
        reference_image_path=ref_path,
        variant_count=variant_count,
    )
    _run_generation(req)


def render_preset_tab(face_path: Path) -> None:
    st.subheader("Use a style preset")
    st.caption("Pick a preset — no reference image needed.")

    preset_key = st.selectbox(
        "Preset",
        options=list(PRESET_LABELS.keys()),
        format_func=lambda k: PRESET_LABELS[k],
        key="preset_key",
    )
    title = st.text_input("Title text", key="preset_title")
    extra = st.text_area(
        "Extra instructions (optional)",
        key="preset_extra",
        placeholder="e.g. red background, point at camera",
    )
    variant_count = st.slider(
        "Variants", min_value=1, max_value=4, value=3, key="preset_variants"
    )

    if not st.button(
        "Generate",
        key="preset_generate",
        type="primary",
        disabled=title.strip() == "",
    ):
        return

    req = GenerationRequest(
        mode="preset",
        face_image_path=face_path,
        title_text=title.strip(),
        preset_key=preset_key,
        overrides={"extra_instructions": extra.strip()} if extra.strip() else {},
        variant_count=variant_count,
    )
    _run_generation(req)


def render_hybrid_tab(face_path: Path) -> None:
    st.subheader("Hybrid / Custom")
    st.caption(
        "Full control. Reference image is optional; use the overrides to steer "
        "composition."
    )

    ref_file = st.file_uploader(
        "Reference image (optional)",
        type=["jpg", "jpeg", "png", "webp"],
        key="hybrid_ref_uploader",
    )
    title = st.text_input("Title text", key="hybrid_title")

    col1, col2 = st.columns(2)
    with col1:
        bg_color = st.color_picker("Background colour", value="#000000", key="hybrid_bg")
        text_position = st.selectbox(
            "Text position",
            options=["left", "right", "top", "bottom", "centre"],
            key="hybrid_text_pos",
        )
    with col2:
        face_expression = st.selectbox(
            "Face expression",
            options=["serious", "shocked", "smiling", "confident"],
            key="hybrid_expression",
        )
        variant_count = st.slider(
            "Variants", min_value=1, max_value=4, value=3, key="hybrid_variants"
        )

    extra = st.text_area(
        "Extra instructions",
        key="hybrid_extra",
        placeholder="Free-form directives appended to the prompt.",
    )

    if not st.button(
        "Generate",
        key="hybrid_generate",
        type="primary",
        disabled=title.strip() == "",
    ):
        return

    ref_path: Path | None = None
    if ref_file is not None:
        ref_path = ROOT_DIR / "outputs" / "_uploads" / ref_file.name
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        ref_path.write_bytes(ref_file.getbuffer())

    overrides = {
        "background_color": bg_color,
        "text_position": text_position,
        "face_expression": face_expression,
    }
    if extra.strip():
        overrides["extra_instructions"] = extra.strip()

    req = GenerationRequest(
        mode="hybrid",
        face_image_path=face_path,
        title_text=title.strip(),
        reference_image_path=ref_path,
        overrides=overrides,
        variant_count=variant_count,
    )
    _run_generation(req)


def main() -> None:
    st.title("YouTube Thumbnail Generator")
    st.caption("Gemini 3.1 Flash Image Preview — for Ben Hawksworth")

    if not _api_key_present():
        st.error(
            "`GEMINI_API_KEY` is not set. Copy `.env.example` to `.env` and "
            "add your key, then restart the app."
        )
        st.stop()

    selected_face = render_sidebar()

    if selected_face is None:
        st.info("Add a face to the library (sidebar) to get started.")
        return

    st.write(f"**Selected face:** `{selected_face.name}`")
    tab_clone, tab_preset, tab_hybrid = st.tabs(
        ["Clone Reference", "Preset Style", "Hybrid"]
    )

    with tab_clone:
        render_clone_tab(selected_face)

    with tab_preset:
        render_preset_tab(selected_face)

    with tab_hybrid:
        render_hybrid_tab(selected_face)


if __name__ == "__main__":
    main()
