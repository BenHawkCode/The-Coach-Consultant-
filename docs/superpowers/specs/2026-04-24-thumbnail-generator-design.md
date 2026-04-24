# YouTube Thumbnail Generator — Design Spec

**Date:** 2026-04-24
**Owner:** Jay (Gencay)
**For:** Ben Hawksworth — The Coach Consultant
**Status:** Design approved, ready for implementation plan

---

## Problem

Ben runs a YouTube channel and wants to scale from ~1K to 10K+ subscribers. Thumbnails from the external agency are poor. He wants to generate his own thumbnails, pass them to his team for distribution, and have full creative control.

Context from Ben (17–22 April 2026):
- "I've had a company doing it but the thumbnails are terrible"
- "I'd ideally like to be able to just generate my own thumbnails to then give to a team for distribution"
- "literally just want to go with whatever will work"
- YouTube channels he watches: Liam Ottley, Alex Hormozi, Dan Martell

## Goal

A local Streamlit app that takes (1) Ben's face, (2) an optional reference thumbnail, (3) a title and style inputs — and produces ready-to-use YouTube thumbnails via Gemini 3.1 Flash Image Preview.

v1 is local-first. Skill wrapper comes later.

## Non-Goals (v1)

- No YouTube Studio API integration (not this iteration)
- No A/B CTR testing, no analytics
- No multi-user deploy / auth
- No video-to-thumbnail extraction
- No team sharing features

## Architecture

Single-page Streamlit app, stateless except for a face library on disk and generation history.

```
The Coach Consultant/3-youtube/thumbnail-generator/
├── app.py                    # Streamlit UI (tabs, forms, preview grid)
├── thumbnail_engine.py       # Gemini API wrapper + prompt builder
├── prompts/
│   └── style_presets.py      # Preset prompt strings (Hormozi, MrBeast, Podcast, etc.)
├── assets/
│   └── ben-faces/            # Ben's face library (seeded with 2 images)
│       ├── ben-headshot.jpg
│       └── ben-face-crop.png
├── outputs/                  # YYYY-MM-DD/ subfolders with generated thumbnails + metadata.json
├── examples/                 # Reference thumbnail library (Ben's liked refs, optional)
├── requirements.txt
├── .env.example              # GEMINI_API_KEY=
└── README.md
```

### Data Flow

1. User opens app → Streamlit loads, reads `assets/ben-faces/` into sidebar library
2. User picks mode tab (A/B/C), fills form, clicks Generate
3. `thumbnail_engine.generate(mode, inputs)` builds the prompt and calls Gemini
4. Gemini returns N images (default 3 variants)
5. App shows preview grid; user downloads or regenerates
6. Every generation is saved to `outputs/YYYY-MM-DD/` with a sibling `metadata.json` (mode, prompt, inputs, timestamp)
7. Sidebar "Recent generations" shows last 10 from disk

## Components

### `app.py` — Streamlit UI

Responsible for:
- Rendering 3 tabs: Clone Reference / Preset Style / Hybrid
- Loading face library from `assets/ben-faces/` at startup
- Face selector (click thumbnails in sidebar) + "Upload new face" → saves to library
- Form inputs per tab (see Modes below)
- Calling `thumbnail_engine.generate()` and rendering preview grid
- Download buttons (PNG, 1280×720)
- Recent generations sidebar section

Not responsible for: prompt construction, API calls, file I/O beyond the UI layer.

### `thumbnail_engine.py` — Generation Engine

Public interface:
```python
def generate(
    mode: Literal["clone", "preset", "hybrid"],
    face_image_path: str,
    title_text: str,
    reference_image_path: str | None = None,
    preset_key: str | None = None,
    overrides: dict | None = None,
    variant_count: int = 3,
) -> list[GeneratedImage]
```

Returns list of `GeneratedImage` dataclass: `{image_bytes, output_path, metadata_path}`.

Responsible for:
- Building the prompt based on mode (delegates preset lookup to `prompts/style_presets.py`)
- Calling Gemini 3.1 Flash Image Preview with correct multimodal payload (face img + optional ref img + prompt)
- Saving output PNGs + metadata JSON to `outputs/YYYY-MM-DD/`
- Error handling (rate limits, safety blocks, network)

### `prompts/style_presets.py` — Preset Library

Dict of `{preset_key: prompt_template}`. v1 seeds:
- `hormozi_bold` — big centered text, high contrast, person on one side
- `mrbeast_reaction` — shocked expression, bright saturated background, arrow/circle annotations
- `podcast_split` — split-screen, person on left, large title on right
- `minimal_text` — clean, minimal text, person prominent, plain background
- `alex_hormozi_black` — all-black background, white bold text, person cutout

Each template takes `{title}` and optional `{extra_instructions}` placeholders.

### `assets/ben-faces/` — Face Library

Seeded with the two images Ben provided:
- `ben-headshot.jpg` — full portrait, studio, colourful background (from `/Users/learnai/Desktop/ben-2.jpeg`)
- `ben-face-crop.png` — tighter crop, black t-shirt, arms crossed, glasses (from `/Users/learnai/Desktop/Screenshot 2026-04-24 at 07.26.27.png`)

App reads everything in this folder at startup. User uploads are saved here too (deduplicated by filename hash).

## Modes (UI Tabs)

### Tab A — Clone Reference
Copies the look of a reference thumbnail Ben likes (Hormozi, Ottley, Martell screenshots).

**Inputs:** reference image upload, face selector, title text.
**Prompt strategy:** "Analyse the layout, typography, colour palette, and composition of the reference. Recreate with the provided person's face and the given title. Match the visual style exactly. Output 1280×720."

### Tab B — Preset Style
Uses a curated prompt template — no reference needed.

**Inputs:** face selector, title text, preset dropdown (5 options above).
**Prompt strategy:** Substitute title into preset template, pass face image as conditioning input.

### Tab C — Hybrid / Custom
Full control. Ref optional, overrides available.

**Inputs:** optional reference image, face selector, title text, overrides panel:
- background colour (hex or colour picker)
- text position (left / right / top / bottom / centre)
- face expression (serious / shocked / smiling / confident)
- extra instructions (free textarea)

**Prompt strategy:** Compose base prompt from whatever inputs are provided, append overrides as explicit directives.

## Output & History

- Output path: `outputs/YYYY-MM-DD/<timestamp>-<short-hash>-v<N>.png`
- Metadata sibling: `outputs/YYYY-MM-DD/<timestamp>-<short-hash>.json`
  ```json
  {
    "timestamp": "2026-04-24T14:32:18Z",
    "mode": "clone",
    "face": "ben-headshot.jpg",
    "reference": "uploads/hormozi-ref-1.png",
    "title": "Why Most Coaches Fail In Year Two",
    "preset": null,
    "overrides": null,
    "prompt": "...full prompt text...",
    "variant_count": 3,
    "outputs": ["...-v1.png", "...-v2.png", "...-v3.png"]
  }
  ```
- Sidebar "Recent generations" lists last 10 from disk (scan `outputs/` folders, sort by timestamp)

## Tech Stack

- `streamlit` — UI
- `google-genai` — Gemini SDK (model: `gemini-3.1-flash-image-preview`)
- `pillow` — image handling / resize to 1280×720
- `python-dotenv` — API key loading

API key: Ben's key goes into `.env` (not committed). `.env.example` documents the required variable.

## Error Handling

| Failure | Behaviour |
|---|---|
| `GEMINI_API_KEY` missing | Red banner on app open with setup instructions; inputs disabled |
| Gemini rate limit | Toast error + "Retry in 30s" button |
| Gemini safety block | Explain which input likely triggered it + "Try different wording" hint |
| Network error | Generic retry button |
| Corrupt face/ref image | Validate on upload (PIL open); reject before calling API |
| No face in library | Prompt user to upload one before enabling Generate |

## Testing

Manual v1 — no automated tests needed for the UI layer. What we verify before handing to Ben:
1. App launches with both seed faces visible
2. Each tab generates at least 1 usable thumbnail with Ben's face
3. Downloads produce 1280×720 PNGs
4. Metadata JSON is well-formed and matches generated files
5. Recent generations sidebar reflects the last 10 outputs
6. API key missing → clear error state (not a stack trace)

If Gemini output quality is inconsistent, we iterate on prompt templates in `prompts/style_presets.py` — that's expected v1 work.

## Future Work (Not v1)

- Wrap the app in a `/thumbnail` slash command skill
- Deploy publicly (Streamlit Cloud) so Ben's team can use it
- YouTube Studio API — pull recent video titles + CTR data
- A/B variant scoring (predicted CTR model)
- Competitor thumbnail library auto-scraped from Hormozi/Ottley/Martell channels
- Batch mode: upload a video title list → generate thumbnails for all

## Risks

- **Gemini image quality for faces.** Model may distort identity. Mitigation: use the strongest face image Ben has; iterate prompts; offer Hybrid mode for manual steering.
- **Style cloning → IP concerns.** Clone Reference mode reproduces competitor style. Mitigation: document that v1 is for internal experimentation; produce original compositions, not direct copies.
- **API cost.** Gemini image generation isn't free. Mitigation: default to 3 variants, not 10; show cost estimate in sidebar eventually.

## Handoff

Once v1 works and Ben is happy with the output quality, next iterations:
1. Bind the app into a Claude Code skill at `3-youtube/thumbnail-generator/skill.md`
2. Pipe in YouTube Studio data so titles can be pulled, not retyped
3. Expand preset library based on what actually performs for Ben's channel
