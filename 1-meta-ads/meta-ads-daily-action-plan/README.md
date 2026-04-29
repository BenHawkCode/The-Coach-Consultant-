# Meta Ads Daily Action Plan

Action-first daily brief for Mahmoud. One Google Doc per day, structured around the three actions to execute in Ads Manager today, the live pipeline state, and per-ad-set verdicts.

The skill inherits from `meta-ads-daily-review` (live Meta API) and `meta-ads-weekly-intelligence` (cron-fresh dashboard JSONs). It does not re-implement that analysis. It reads their output, layers reasoning on top, and renders a Doc.

## What you need before running

1. **Both upstream skills already work on your machine.**
   - `1-meta-ads/meta-ads-daily-review/` runs and produces `outputs/DAILY-REVIEW-*.json`.
   - The dashboard repo is cloned at `/tmp/tcc-dashboard` (or `TCC_DASHBOARD_PATH` env var points elsewhere).

2. **`.env` at the project root has these tokens.**
   - `META_ACCESS_TOKEN`, `META_ACCOUNT_ID` — the daily-review uses them.
   - `CALENDLY_API_KEY` — for the live booking fetch (read-only PAT, scope: `scheduled_events:read`, `event_types:read`).
   - `TCC_GITHUB_TOKEN` — for cloning / pulling `tcc-dashboard`.
   - `IG_BUSINESS_ACCOUNT_ID` (optional, defaults to Ben's IG account) — for TOF profile-visit CPF.

3. **`gws-cli` installed and authenticated** (see "Installing gws-cli" below). The Doc write step will not work without it.

4. **`md-to-gdocs` skill at `jay-skills/md-to-gdocs/convert.py`.** Used to render the markdown brief as a styled docx with native tables and headings. Without it, the Doc lands as raw text with `|` characters everywhere.

## Installing gws-cli

```bash
# Install the CLI
brew install --cask google-workspace-cli  # macOS

# Or via npm if Homebrew isn't your thing
npm install -g @googleworkspace/cli

# Authenticate against your Google account (one-off)
gws auth login

# Confirm
gws drive files list --params '{"pageSize":1}' --format json
```

Token cache lives at `~/.config/gws/`. The first auth pops a browser window, after that it's silent.

For the production runner (not your laptop), use a service account with Drive scope. Documented in the gws CLI README.

## How to run today's brief

```bash
# 1. Make sure the dashboard clone is fresh
git -C /tmp/tcc-dashboard pull

# 2. Run the upstream daily-review (live Meta API + Calendly)
cd 1-meta-ads/meta-ads-daily-review
bash setup.sh --campaign-id 120239672138210377 --week 3 --days 7

# 3. Invoke this skill (manual today, Routine-scheduled later)
#    Claude reads skill.md, builds the brief, writes outputs/{YYYY-MM-DD}.md,
#    converts to docx, uploads to Drive as a Google Doc.
```

End state per run:
- `outputs/{YYYY-MM-DD}.md` — local mirror, git-friendly, used by tomorrow's brief for the "did we act on it?" check.
- A Google Doc named `Meta Ads Daily Action Plan — {YYYY-MM-DD}` in the Drive folder (folder ID stored in `outputs/folder_id.txt` after first run, root of My Drive otherwise).

## What the skill does in order

1. Confirms today's `meta-ads-daily-review` JSON exists. If not, runs it.
2. Pulls `intelligence.json`, `meta_ads_campaigns.json`, `calendly_bookings.json`, `sheet_revenue.json` from the dashboard clone.
3. Reads yesterday's `outputs/{date}.md` if present, to check action follow-through.
4. Reasons about deltas (today vs yesterday, 7d, 28d). Spawns a sub-agent only when triggers fire (CTR drop > 25%, cost per real call > 50% week-over-week, learning-phase stuck > 7 days, frequency over fatigue threshold, single creative > 40% of ad set spend).
5. Drafts the brief in markdown using the structure in `skill.md` § Output Structure.
6. Saves to `outputs/{YYYY-MM-DD}.md`.
7. Runs `jay-skills/md-to-gdocs/convert.py` against the MD to produce a styled docx.
8. Uploads the docx via `gws drive files create --upload`.
9. Copies it into a Google Doc mimeType (the upload arrives as docx, the copy converts).
10. Deletes the intermediate docx (local file + uploaded copy in Drive).

## The framework it follows

Hard rules anchored in `1-meta-ads/CLAUDE.md` (Antonio's build guide, sections 5, 6, 8):

- Stage classification first. No verdict without stage.
- Per-stage metrics. TOF on cost per IG follower, MOF on cost per opt-in, BOF on cost per real Calendly call. No BOF thresholds applied to TOF or MOF.
- Kill verdicts exclude `PAUSED` / `CAMPAIGN_PAUSED` ad sets.
- Booked calls come from Calendly only. Pixel `lead` events are form submissions, not calls. Historical ratio roughly 4.5 form submits per booked call.
- ROAS = sheet revenue (email-matched against paid Calendly bookings, 28d window) divided by BOF spend. When the denominator is positive but the numerator is zero, display "Pending" not "0.0x".
- No team names in prose. No snake_case in visible text. No em-dashes. No "simplify the form" or "kill immediately" directives.
- Data freshness stamp at the top, data caveat block where pixel numbers appear.

The skill checks every brief against the § 8 build checklist before the Drive write fires. If any check fails, it stops and surfaces the gap rather than shipping a flawed Doc.

## Files in this folder

```
meta-ads-daily-action-plan/
├── skill.md            # the actual skill spec Claude reads
├── README.md           # this file
└── outputs/
    ├── {YYYY-MM-DD}.md # one markdown brief per day
    └── folder_id.txt   # Drive folder ID, populated after first run
```

## Testing the skill on your end

1. Pull the latest from `BenHawkCode/The-Coach-Consultant-` main.
2. Confirm the four prerequisites above.
3. Run today's brief from your terminal (the skill is invoked via Claude Code, not directly).
4. Open the resulting Google Doc and the local `outputs/{date}.md`. They should match.
5. Sanity check the numbers against the dashboard at tcc-dashboard.netlify.app and against the Calendly app directly.

If something is off, the difference is almost always in:
- Which campaign got fed to `daily-review` (campaign-id flag).
- Whether the dashboard clone is actually fresh (`git -C /tmp/tcc-dashboard pull`).
- Whether the live Calendly fetch returned the expected slug suffix (`-pa`).

Open an issue or DM Jay with the gap and the run's `outputs/{date}.md` content for the diff.

## Routine scheduling (next step)

Once the manual run is verified, the same flow gets wrapped in a Claude Routine that fires every weekday morning. The runner machine has to stay on for the routine to execute, so the host machine is a separate decision.

First few automated runs need Antonio's sanity check, then 2-3 days of validation by Mahmoud before the recommendations drive ad-spend changes.
