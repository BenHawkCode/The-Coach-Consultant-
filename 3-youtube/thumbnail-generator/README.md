# YouTube Thumbnail Generator

Local Streamlit app for generating YouTube thumbnails using Gemini 3.1 Flash Image Preview.

## Setup

1. Create a virtualenv and install deps:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Add your Gemini API key to the project-root `.env` (one level up from `3-youtube/`). Get a key at https://aistudio.google.com/apikey, then:
   ```bash
   echo "GEMINI_API_KEY=your_key_here" >> "../../.env"
   ```
   The Gemini key lives alongside the other shared tokens (Meta, GitHub, Apify, Calendly) — not in this skill folder.

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Modes

- **Clone Reference** — upload a thumbnail you like, app copies its style
- **Preset Style** — pick a preset (Hormozi Bold, MrBeast Reaction, etc.)
- **Hybrid** — full control with ref, overrides, and custom instructions

## Output

Generated thumbnails land in `outputs/YYYY-MM-DD/` with a sibling `metadata.json`.
