---
name: meta-ads-daily-action-plan
description: Daily action-first Meta Ads brief for Ben Mahmoud. Reads the meta-ads-daily-review JSON and the dashboard intelligence + Calendly bookings, reasons about what changed vs yesterday / 7d / 28d, and writes ONE Google Doc per day with three prioritised actions, pipeline state, per-ad-set verdicts (KILL/SCALE/WATCH), anomalies, and the exact Ads Manager changes Mahmoud should execute today. Tone is eight-figure consultant, not descriptive report.
---

# Meta Ads Daily Action Plan

Action-first daily brief for Ben Mahmoud. Inherits from `meta-ads-daily-review` and `meta-ads-weekly-intelligence` — reads their data, layers reasoning on top, ships one Google Doc per day.

## Purpose

The other two skills give analysis. This one gives **decisions**.

Ben Hawksworth's literal brief (2026-04-27):

> "MUST be focused on actions to improve & scale."

Ben Mahmoud's literal brief:

> "this is literally what just do straight away."

Output is what Mahmoud opens in the morning, copy-pastes into Ads Manager, and works through. Nothing else.

## What This Skill Does

When invoked:

1. **Pulls upstream skill data** — runs `meta-ads-daily-review` if today's JSON isn't already in its `outputs/` folder, otherwise reads the existing file.
2. **Pulls dashboard intelligence** — reads `intelligence.json` + `meta_ads_campaigns.json` + `calendly_bookings.json` from the cloned tcc-dashboard repo (`/tmp/tcc-dashboard/public/data/`).
3. **Reads yesterday's action plan** — to check what flags carried over and whether previous decisions were acted on.
4. **Reasons about deltas** — today vs yesterday vs 7d vs 28d. Looks for: CTR shifts, cost-per-real-call moves, audience saturation, learning-phase exits, fatigue, quality drops, spend redistribution.
5. **Spawns sub-agents only when needed** — if a single ad set's CTR drops by more than 25% day-over-day, dig into creative-level. If audience saturation suspected, pull historical comparison. If everything stable, don't pad.
6. **Drafts the brief** — exact structure below.
7. **Writes a timestamped Google Doc** to the Daily Action Plans folder.

## Inputs (read in this order)

| File | Purpose |
|---|---|
| `1-meta-ads/meta-ads-daily-review/outputs/DAILY-REVIEW-*-{today}.json` | Live Meta API + Calendly per BOF campaign run today |
| `/tmp/tcc-dashboard/public/data/intelligence.json` | Opus strategic verdicts, anomalies, weekly priorities |
| `/tmp/tcc-dashboard/public/data/meta_ads_campaigns.json` | 7d + 28d ad-set breakdown for ALL campaigns, stage classification, `summary.stage_spend_7d` |
| `/tmp/tcc-dashboard/public/data/calendly_bookings.json` | Real paid bookings (ground truth) |
| `/tmp/tcc-dashboard/public/data/sheet_revenue.json` | Signups + revenue (literal `name` field is binding, see §Names) |
| `1-meta-ads/meta-ads-daily-action-plan/outputs/{yesterday}.md` | Yesterday's brief, for "did we act on it?" tracking |

### Coverage rule (multi-campaign)

The brief must cover spend across all stages, not just BOF. Single-campaign briefs hide whichever stage is currently consuming the most spend.

- **BOF campaigns:** run `meta-ads-daily-review` per active BOF campaign-id and read every `DAILY-REVIEW-*-{today}.json` written today. Live Meta + Calendly numbers come from these.
- **TOF + MOF + UNKNOWN campaigns:** read directly from `meta_ads_campaigns.json.ad_sets[]`, filtered by `stage` field. No live Meta call needed for these stages, the cron-fresh JSON is sufficient.
- **Sanity check first:** read `meta_ads_campaigns.json.summary.stage_spend_7d` at the start. If the largest stage by spend has no presence in the brief, stop and surface the gap.

### Clone source

`/tmp/tcc-dashboard` is cloned from `antonio-gasso/tcc-dashboard` directly using `TCC_GITHUB_TOKEN`. Same PAT works for both upstream and forks. Avoid `SudhakaPr/tcc-dashboard` (the fork) because it goes stale unless manually synced post-cron.

```bash
# First-time clone
git clone https://${TCC_GITHUB_TOKEN}@github.com/antonio-gasso/tcc-dashboard.git /tmp/tcc-dashboard

# Each run
git -C /tmp/tcc-dashboard pull
```

If today's daily-review JSON for a BOF campaign is missing, run `bash 1-meta-ads/meta-ads-daily-review/setup.sh --campaign-id <ID> --week <N> --days 7` per active BOF campaign first.

## Reasoning Framework

The skill is the brain. Decide what to investigate based on what the data shows. Frameworks below are non-negotiable — see `1-meta-ads/CLAUDE.md` §5 for the full spec.

### Step 1 — Classify every campaign first

Read `stage` field already computed in `meta_ads_campaigns.json` per ad set. Do not re-derive. If missing, map from objective:
- `OUTCOME_AWARENESS`, `OUTCOME_VIDEO_VIEWS` → TOF
- `OUTCOME_TRAFFIC` → MOF (TOF if optimised for profile visits)
- `OUTCOME_ENGAGEMENT` → MOF (TOF if Profile Visits / ThruPlay)
- `OUTCOME_LEADS`, `OUTCOME_SALES` → BOF

### Step 2 — Judge each stage by its own metric

| Stage | Primary | Never judge by |
|---|---|---|
| TOF | Cost per IG follower | CTR, form submits, cost per call |
| MOF | Cost per opt-in / DM conversation | Cost per booked call |
| BOF | Cost per real Calendly call (spend / `paid_ads_7d`) | Pixel `lead` events as calls |

### Step 3 — Apply BOF kill/scale/watch thresholds (BOF ONLY)

- CTR link < 0.8% → kill candidate
- CTR link ≥ 1.5% → healthy, ≥ 2.5% across ad sets → scale candidate
- Cost per form submit ≤ £50 healthy, > £75 problem
- Landing page form submit rate ≥ 8% target (NEVER recommend "simplify the form")
- Min 1,000 impressions per ad set for a verdict, else "insufficient signal"
- Never kill during `LEARNING` / `LEARNING_LIMITED`. Min 50 conversion events.
- Budget split target: 50% BOF / 30% MOF / 20% TOF (use `summary.stage_spend_7d`)

### Step 4 — Ground truth for ROAS

- **Numerator:** `sheet_revenue.json` signups in the last N days whose email matches a `calendly_bookings.paid_ads_28d` entry (email join, 28d window for sales-cycle lag).
- **Denominator:** BOF ad-set spend only from `meta_ads_campaigns.json`.
- Never compute ROAS from pixel events.
- If denominator > 0 and numerator = 0 → display "Pending", not "0.0x".

### Trigger sub-agent when

- Single ad set CTR drops > 25% vs yesterday on > 1000 impressions.
- Cost per real Calendly call jumps > 50% week-over-week.
- Ad set in `LEARNING_LIMITED` for > 7 days.
- Frequency > 3.5 (TOF) or > 4.5 (BOF) suggests fatigue.
- One creative consumes > 40% of an ad set's spend.

**Don't pad. If a section has nothing material, write one line: "No anomalies today."**

### Today's 3 Actions — sourcing rules

The Top-3 must rotate as the data rotates. Don't paraphrase yesterday's actions back in.

Source priority (highest first):

1. **Carry-forward gaps from yesterday's brief.** If yesterday's Action 1 was "reactivate the BOF campaign" and the campaign is still paused today, that becomes today's Action 1 again with a "still not actioned" framing. Open loops always come first.
2. **Today's anomalies that breach a framework threshold.** Cost per real call jumps over £75, CTR drops below 0.8%, frequency past fatigue, single-creative dominance, learning-phase stuck. Daily-fresh.
3. **`intelligence.meta_ads.weekly_priorities`** (Opus strategic anchor, refreshes Monday). Use only after carry-forward and daily anomalies are exhausted, and only when the priority is still current (the underlying state hasn't changed since the cron).

If three days run with the same Top-3 because state hasn't moved, write that explicitly in the brief (e.g. "Action 1 carried forward 3 days, BOF still paused — escalating") instead of repeating the action with new wording.

## Output Structure

ONE Google Doc per day. Filename format: `Meta Ads Daily Action Plan — {YYYY-MM-DD}`.

```
# Meta Ads Daily Action Plan
{Day, DD Month YYYY} · Generated {HH:MM UK time}

Data refreshed: {intelligence.json._metadata.generated_at} · Calendly: {fetched_at} · Live Meta API run today

> Pipeline form-submit numbers de-dupe `lead` / `fb_pixel_lead` / `lead_grouped`. They are application submissions, not booked calls. Booked-call counts come from Calendly only.

## Today's 3 Actions

1. [Action] · [Concrete Ads Manager change]
2. [Action] · [Concrete Ads Manager change]
3. [Action] · [Concrete Ads Manager change]

## Pipeline State

Real bookings (paid ads, Calendly): {X} this week, {Y} in 28d pipeline
Awaiting close: {Z}
Signed this week (sheet revenue, email-matched): {N}
Spend (BOF only, 7d): £{S}
ROAS: {value or "Pending"}
Cost per real call: £{X}

## Ad Set Verdicts

| Stage | Ad Set | Status | Spend 7d | Stage-relevant metric | Verdict | Reasoning |
|---|---|---|---|---|---|---|
| BOF | Warm Retargeting | ACTIVE | £203 | £18.45 / real call | SCALE | Healthy by BOF rule (£50 ceiling), scaling at 8% increments |

(Filter out PAUSED ad sets. Group by stage: BOF first, MOF, TOF. Stage-relevant metric column changes by stage: cost per real call for BOF, cost per opt-in for MOF, cost per IG follower for TOF.)

## Anomalies

[Numbered list, one line each. If nothing material, write "No anomalies today."]

## Today's Ads Manager Changes

[Concrete bullets Mahmoud executes. Filter out paused ad sets:]
- Kill Reel 5 in Cold Lookalike (BOF, CTR 0.6%, 0 calls in 7d)
- Increase Warm Retargeting daily budget from £50 to £55 (8% bump, scale rule respected)
- Duplicate "OG Hook" creative into Cold Interest with new 9-second variant
- Pause Profile Visits creative #3 (TOF, cost per follower £4.20, target £1.50)

## Yesterday's Flags — Acted On?

[One bullet per yesterday's action with status: actioned / not actioned / superseded. If yesterday's plan didn't exist, omit this section.]
```

## Tone & Output Rules (binding, see `1-meta-ads/CLAUDE.md` §6)

**Hard nevers:**
- Kill verdicts on ad sets with `status=PAUSED`. Filter by active status before issuing kill.
- "Simplify the form", "reduce landing page friction", "remove qualification". The application form IS the qualification filter by design.
- Treat Meta pixel `lead` events as booked calls. Always cross-reference Calendly.
- Team-member names (Mahmoud, Ben, Rob, Jay, Antonio) in free-text recommendations.
- Internal snake_case field names (`paid_calls_booked`, `taken_no_outcome`) in prose.
- Assert "the call happened" as fact. Write "scheduled calls" or "bookings".
- Speculate about sales-call quality, pitch clarity, onboarding friction.
- Directive "kill immediately". Reframe as "watch closely" or "concern" with reasoning.
- Em-dashes (—), en-dashes (–) anywhere.
- Pad numbers to look precise when the data is directional.
- **Paraphrase or interpret signup names from email handles.** A user with email `danny@thedadcompass.com` is not "Danny Compass". Read the literal `name` field from `sheet_revenue.signups_7d[]` and use it verbatim. If `name` is missing, write "name not in sheet" rather than guess.
- **Word "baseline" for the 8% form submit rate** or any other framework threshold. The 8% is a target, not a baseline. TCC isn't historically at 8%. Always write "8% target" or "8% threshold". Same applies to other framework thresholds (£50 cost per submit ceiling, 1.5% CTR target, etc.).

**Hard alwayses:**
- Data freshness stamp at the top (read `intelligence.json._metadata.generated_at` + collector `fetched_at`).
- Data caveat block where any Meta pixel number appears (form submits ≠ calls).
- Stage-aware verdicts. Never issue a verdict without declaring the stage.
- Per-stage reasoning. Explain which stage rule applies.
- Pipeline state when revenue-related. If pending paid bookings exist, say so explicitly.
- British English. £ for money. "Optimise", "behaviour", "organisation".

**Voice:** Eight-figure consultant. State what to do and why. Don't hedge.

## Google Doc Writing

Markdown rendered as a styled Google Doc via the `md-to-gdocs` skill. Direct `documents.batchUpdate` writes raw text, no headings, no tables. Don't go that route.

Workflow:

```bash
# 1. Convert today's MD into a .docx with proper styles
python3 jay-skills/md-to-gdocs/convert.py \
    1-meta-ads/meta-ads-daily-action-plan/outputs/{YYYY-MM-DD}.md \
    "Meta Ads Daily Action Plan — {YYYY-MM-DD}"

# 2. Upload + convert to Google Doc in one step (mimeType triggers conversion)
gws drive files create \
    --upload "Meta Ads Daily Action Plan — {YYYY-MM-DD}.docx" \
    --params '{...}' \
    --format json

# 3. The upload arrives as .docx in Drive. Issue a copy with target mimeType
#    `application/vnd.google-apps.document` to convert. The original .docx
#    can then be deleted.
gws drive files copy \
    --params '{"fileId":"<DOCX_ID>"}' \
    --json '{"name":"Meta Ads Daily Action Plan — {YYYY-MM-DD}","mimeType":"application/vnd.google-apps.document","parents":["<FOLDER_ID>"]}' \
    --format json
```

Folder ID is stored in `outputs/folder_id.txt` after first run. If Ben hasn't shared the TCC Drive folder yet, the Doc lands in the runner's My Drive root and gets relocated manually.

Clean up the intermediate `.docx` (local file + uploaded copy in Drive) once the converted Google Doc is confirmed.

## Local Output (always)

Mirror the brief to `outputs/{YYYY-MM-DD}.md` so:
- Yesterday's plan is readable for tomorrow's "did we act on it?" check.
- Git diffs show how the brief evolves week to week.
- If Drive write fails, the brief still exists locally.

## When to Invoke

- Manually: every morning by Mahmoud.
- Eventually: scheduled via Claude Routines (every weekday morning, 07:00 UK).
- First few automated runs need Antonio's sanity check, then 2-3 days validation by Mahmoud before acting on recommendations for ad spend changes.

## Pre-ship checklist (binding, see `1-meta-ads/CLAUDE.md` §8)

Before writing any Doc to Drive, every run must verify:

- Bookings come from Calendly, revenue from `sheet_revenue.json` email-matched, Meta pixel only for ad-set health.
- Every verdict declares its stage. No verdict without stage.
- Per-stage metrics applied. No BOF thresholds on TOF / MOF.
- Kill verdicts exclude `PAUSED` ad sets.
- No team names, no snake_case in prose, no "simplify the form", no "kill immediately", no em-dashes.
- Freshness stamp present. Data caveat present where pixel numbers appear.
- ROAS shows "Pending" (not "0.0x") when bookings exist but revenue not yet matched.
- If Meta and Calendly disagree, the gap is explained in-text, not silently picked.

If any check fails, stop and fix before shipping.

## Version

**v1.0 (2026-04-28)** — initial action-first brief, inherits from daily-review + weekly-intelligence, writes one Google Doc per day to the TCC Automations → Meta Ads Daily Briefs folder. Anchored to `1-meta-ads/CLAUDE.md` framework rules (stage classification, per-stage metrics, hard nevers, build checklist).
