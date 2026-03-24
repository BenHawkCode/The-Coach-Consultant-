#!/bin/bash
# Meta Ad Copy Skill - Auto Setup Script
# Checks dependencies and installs if needed

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SKILL_DIR/venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Setting up meta-ad-copy skill (first time only)..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install -q requests python-dotenv
    echo "✅ Setup complete!"
else
    source "$VENV_DIR/bin/activate"
fi

# Run the fetch script with all passed arguments
python3 "$SKILL_DIR/fetch_meta_ads.py" "$@"
