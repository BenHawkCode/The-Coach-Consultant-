---
name: youtube-thumbnail-generator
description: Generate YouTube thumbnails for Ben Hawksworth using Gemini 3.1 Flash Image Preview. Launches a local Streamlit app with three modes — Clone Reference (upload any thumbnail and copy its style), Preset Style (Hormozi Bold / MrBeast Reaction / Podcast Split / Minimal Text / Alex Hormozi Black), and Hybrid (full control with overrides). Seeded face library (ben-headshot.jpg, ben-face-crop.png), generation history, metadata sidecars. Triggers on "thumbnail", "youtube thumbnail", "generate thumbnail", "/thumbnail".
---

# YouTube Thumbnail Generator

Local Streamlit app that generates YouTube thumbnails for Ben Hawksworth using Gemini 3.1 Flash Image Preview.

## When To Use

Trigger this skill when Ben (or anyone on the team) says:
- "Generate a thumbnail for [video title]"
- "Make me a thumbnail"
- "Open the thumbnail generator"
- "/thumbnail"
- Anything involving YouTube thumbnails for his channel

## What It Does

Launches a Streamlit app in the browser with three generation modes:

1. **Clone Reference** — Upload a thumbnail you like (from Hormozi, Ottley, Martell, anyone). Gemini analyses the layout, typography, and colour, then recreates that style with Ben's face and the new title.

2. **Preset Style** — Pick from curated presets with no reference needed:
   - `hormozi_bold` — Bold centered text, person on one side, saturated background
   - `mrbeast_reaction` — Shocked expression, bright background, red annotations
   - `podcast_split` — Split layout, person left, bold title right
   - `minimal_text` — Clean, prominent person, minimal text
   - `alex_hormozi_black` — All-black background, white bold text, person cutout

3. **Hybrid** — Full control. Optional reference, plus overrides:
   - Background colour (hex picker)
   - Text position (left/right/top/bottom/centre)
   - Face expression (serious/shocked/smiling/confident)
   - Free-text extra instructions

All modes enforce negative instructions — no timestamps, no YouTube UI elements, no duration overlays, no watermarks (Gemini copies those from reference images if not blocked).

## How To Run It

From Claude Code / the terminal, run:

```bash
cd "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator"
source .venv/bin/activate
streamlit run app.py
```

The app opens at http://localhost:8501 (or another port if 8501 is in use).

### First-time setup (one-off)

If the venv doesn't exist yet:

```bash
cd "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and add GEMINI_API_KEY (get one at https://aistudio.google.com/apikey)
```

## Configuration

The app reads `GEMINI_API_KEY` from `.env` in the skill directory. The key must be set before generation works — if missing, the app shows a red banner and blocks input.

**Model:** `gemini-3.1-flash-image-preview` (Gemini's image generation model)
**Docs:** https://ai.google.dev/gemini-api/docs/image-generation

## Face Library

Seeded with two images of Ben at `assets/ben-faces/`:
- `ben-headshot.jpg` — full portrait, studio, colourful background
- `ben-face-crop.png` — tighter crop, black t-shirt, glasses

Upload additional faces via the sidebar — they're saved into the library for future use.

## Output

Every generation is saved to `outputs/YYYY-MM-DD/`:
- `HHMMSS-<hash>-v1.png`, `-v2.png`, ... (one PNG per variant)
- `HHMMSS-<hash>.json` (metadata sidecar: mode, prompt, face used, title, overrides)

The sidebar "Recent generations" section shows the last 10.

## Files

```
3-youtube/thumbnail-generator/
├── skill.md                  # this file
├── app.py                    # Streamlit UI
├── thumbnail_engine.py       # Gemini wrapper + prompt builder
├── prompts/
│   └── style_presets.py      # 5 curated preset templates
├── assets/ben-faces/         # Ben's face library (seeded)
├── outputs/                  # Generated thumbnails + metadata
├── requirements.txt
├── .env.example
└── README.md
```

## Invocation Workflow

When a user triggers this skill:

1. Check if `.venv` exists at `3-youtube/thumbnail-generator/.venv`. If not, guide them through first-time setup (above).
2. Check if `.env` has `GEMINI_API_KEY`. If not, ask them to add it before launching.
3. Launch the app with the commands in "How To Run It" above.
4. Tell the user which URL the app is running on (usually http://localhost:8501).
5. Briefly describe the three tabs so they know where to click.

Do NOT try to generate thumbnails directly from Claude Code — the app is the interface. Claude Code's job is to launch it and explain how to use it.
