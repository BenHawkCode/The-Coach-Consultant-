# YouTube Thumbnail Generator

Local Streamlit app for generating YouTube thumbnails using Gemini 3.1 Flash Image Preview.

## Setup

1. Create a virtualenv and install deps:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Gemini API key:
   ```bash
   cp .env.example .env
   # edit .env
   ```

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
