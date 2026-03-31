#!/bin/bash
# Auto-pull from BenHawkCode/The-Coach-Consultant- GitHub repo
# Runs periodically to keep local files in sync

REPO_DIR="/Users/benhawksworth/Documents/Claude Code Projects/the-coach-consultant"
LOG_FILE="$REPO_DIR/.git/auto-pull.log"
REMOTE="benhawk"
BRANCH="main"

cd "$REPO_DIR" || exit 1

# Log timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - Checking for updates..." >> "$LOG_FILE"

# Fetch from BenHawkCode remote
git fetch "$REMOTE" 2>> "$LOG_FILE"

# Check if there are new commits
LOCAL=$(git rev-parse HEAD)
REMOTE_HEAD=$(git rev-parse "$REMOTE/$BRANCH")

if [ "$LOCAL" != "$REMOTE_HEAD" ]; then
    # Check if remote has new commits (is ahead)
    if git merge-base --is-ancestor "$REMOTE_HEAD" HEAD; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Local is ahead or equal. No pull needed." >> "$LOG_FILE"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - New commits found. Pulling..." >> "$LOG_FILE"
        git merge "$REMOTE/$BRANCH" --no-edit 2>> "$LOG_FILE"
        if [ $? -eq 0 ]; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') - Pull successful." >> "$LOG_FILE"
        else
            echo "$(date '+%Y-%m-%d %H:%M:%S') - MERGE CONFLICT - manual resolution needed." >> "$LOG_FILE"
            git merge --abort 2>> "$LOG_FILE"
        fi
    fi
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Already up to date." >> "$LOG_FILE"
fi

# Keep log file manageable (last 200 lines)
tail -200 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
