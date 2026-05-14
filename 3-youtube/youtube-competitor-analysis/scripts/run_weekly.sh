#!/bin/bash
# Weekly YouTube Competitor Analysis pipeline.
# Runs every Monday after the IG competitor cron lands.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$(cd "$SKILL_DIR/../.." && pwd)"
LOG_DIR="$SKILL_DIR/cron-logs"
mkdir -p "$LOG_DIR"
TODAY="$(date +%Y-%m-%d)"
LOG_FILE="$LOG_DIR/run-$TODAY.log"

{
  echo "=== YouTube Competitor Analysis run @ $(date '+%Y-%m-%d %H:%M:%S %Z') ==="
  cd "$PROJECT_ROOT"

  # Load .env so GEMINI_API_KEY is available to the python scripts
  if [ -f "$PROJECT_ROOT/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    source "$PROJECT_ROOT/.env"
    set +a
  fi

  # Make sure yt-dlp is available
  if ! command -v yt-dlp >/dev/null 2>&1; then
    echo "[fatal] yt-dlp not installed. Run: brew install yt-dlp"
    exit 1
  fi

  echo "[1/6] scrape_channels.py"
  python3 "$SCRIPT_DIR/scrape_channels.py" --days 30 --max-videos 30

  echo "[2/6] analyse_top5.py (Antonio intelligence brief)"
  python3 "$SCRIPT_DIR/analyse_top5.py" --top 5

  echo "[3/6] aggregate.py"
  python3 "$SCRIPT_DIR/aggregate.py"

  echo "[4/6] generate_idea_bank.py (Ben video idea bank, 5 channels x latest video)"
  python3 "$SCRIPT_DIR/generate_idea_bank.py"

  echo "[5/6] render_md.py (markdown mirror)"
  python3 "$SCRIPT_DIR/render_md.py"

  echo "[6/6] render_gdoc.py + render_idea_bank_gdoc.py (Drive Docs)"
  python3 "$SCRIPT_DIR/render_gdoc.py"
  python3 "$SCRIPT_DIR/render_idea_bank_gdoc.py"

  echo "=== Run finished @ $(date '+%Y-%m-%d %H:%M:%S %Z') ==="
} >> "$LOG_FILE" 2>&1
