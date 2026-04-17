#!/bin/bash
# Meta Ads Daily Review — setup + runner
# First run creates venv + installs deps. Subsequent runs use existing venv.

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SKILL_DIR"

VENV_DIR="$SKILL_DIR/venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "[setup] Creating virtualenv..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install --quiet --upgrade pip
    pip install --quiet requests python-dotenv pyyaml
else
    source "$VENV_DIR/bin/activate"
fi

PROJECT_ROOT="$(cd "$SKILL_DIR/../.." && pwd)"
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "[error] No .env found at $PROJECT_ROOT/.env. Add META_ACCESS_TOKEN and META_ACCOUNT_ID."
    exit 1
fi

python fetch_daily_review.py "$@"
