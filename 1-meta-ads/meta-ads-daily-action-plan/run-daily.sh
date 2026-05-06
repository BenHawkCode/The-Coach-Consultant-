#!/bin/bash
# Meta Ads Daily Action Plan — local launchd runner
# Triggered by ~/Library/LaunchAgents/com.thecoachconsultant.meta-ads-daily-action-plan.plist
# Schedule: every day at 09:00 Europe/Istanbul

set -euo pipefail

PROJECT_ROOT="/Users/learnai/Desktop/The Coach Consultant"
LOG_DIR="${PROJECT_ROOT}/1-meta-ads/meta-ads-daily-action-plan/cron-logs"
TODAY="$(date +%Y-%m-%d)"
LOG_FILE="${LOG_DIR}/run-${TODAY}.log"
CLAUDE_BIN="/Users/learnai/.local/bin/claude"

mkdir -p "$LOG_DIR"

{
  echo "=== Meta Ads Daily Action Plan run @ $(date '+%Y-%m-%d %H:%M:%S %Z') ==="
  cd "$PROJECT_ROOT"

  # Load .env so META_ACCESS_TOKEN, TCC_GITHUB_TOKEN, etc. are available
  if [ -f "${PROJECT_ROOT}/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    source "${PROJECT_ROOT}/.env"
    set +a
  fi

  "$CLAUDE_BIN" -p "Use the meta-ads-daily-action-plan skill to generate today's brief for ${TODAY}. Follow the skill's full workflow: pull upstream daily-review JSON (run setup.sh per active BOF campaign if missing), pull dashboard intelligence from /tmp/tcc-dashboard, read yesterday's brief, write the markdown to outputs/${TODAY}.md, and upload as a Google Doc to the Daily Action Plans folder. Apply every framework rule and pre-ship check from 1-meta-ads/CLAUDE.md before shipping." \
    --dangerously-skip-permissions

  echo "=== Run finished @ $(date '+%Y-%m-%d %H:%M:%S %Z') ==="
} >> "$LOG_FILE" 2>&1
