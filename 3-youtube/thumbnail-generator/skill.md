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

When the user triggers this skill (e.g. "open the thumbnail generator", "make a thumbnail", "/thumbnail"), follow this sequence — do NOT skip steps.

### Step 1 — Pre-flight checks (run all in parallel)

Run these Bash commands to check readiness:

```bash
# Check virtualenv exists
test -d "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator/.venv" && echo "VENV_OK" || echo "VENV_MISSING"

# Check .env file exists and has a non-placeholder key
if [ -f "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator/.env" ]; then
  grep -q "GEMINI_API_KEY=AIza" "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator/.env" && echo "ENV_OK" || echo "ENV_NO_KEY"
else
  echo "ENV_MISSING"
fi

# Check requirements installed (streamlit binary present in venv)
test -f "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator/.venv/bin/streamlit" && echo "DEPS_OK" || echo "DEPS_MISSING"

# Check if app is already running on common ports
lsof -i :8501 -i :8520 2>/dev/null | grep LISTEN | head -3
```

### Step 2 — Fix anything that's missing

**If `VENV_MISSING`:**
```bash
cd "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator"
python3 -m venv .venv
```

**If `DEPS_MISSING` (or after creating venv):**
```bash
cd "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator"
source .venv/bin/activate
pip install -r requirements.txt
```

**If `ENV_MISSING`:** Ask the user for their Gemini API key (point them to https://aistudio.google.com/apikey if they don't have one). Then write `.env`:
```bash
cat > "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator/.env" <<EOF
GEMINI_API_KEY=<paste_key_here>
EOF
```

**If `ENV_NO_KEY`:** Open the file for the user with `open "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator/.env"` and tell them to replace the placeholder.

**If app already running on 8501/8520:** Skip to Step 4 — tell the user the URL it's already on. Don't start a duplicate.

### Step 3 — Launch the app

Run in background (do NOT block the terminal):

```bash
cd "/Users/learnai/Desktop/The Coach Consultant/3-youtube/thumbnail-generator"
source .venv/bin/activate
streamlit run app.py --server.port 8520 > /tmp/streamlit-thumb.log 2>&1
```

Use `run_in_background: true` on the Bash tool. Wait ~4 seconds, then verify with:
```bash
curl -s -o /dev/null -w "HTTP %{http_code}" http://localhost:8520
```

If response is `HTTP 200`, app is up. If not, read `/tmp/streamlit-thumb.log` and report the error.

### Step 4 — Hand off to the user

Tell the user:
- **URL:** http://localhost:8520 (open it in a browser)
- **Sidebar:** select one of the seeded faces (ben-headshot.jpg or ben-face-crop.png), or upload a new one
- **Three tabs to choose from:**
  - **Clone Reference** → upload a thumbnail you like + title + optional extra instructions, app copies the style
  - **Preset Style** → pick a preset (Hormozi Bold / MrBeast Reaction / Podcast Split / Minimal Text / Alex Hormozi Black) + title
  - **Hybrid** → full control: ref optional, background colour, text position, face expression, free-text instructions
- **Output:** click "Download PNG" under any generated thumbnail to save it. Everything is also auto-saved to `outputs/YYYY-MM-DD/`.

Do NOT try to generate thumbnails directly from Claude Code — the app is the interface. Claude Code's job is to launch it and explain how to use it.
