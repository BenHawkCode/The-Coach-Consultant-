---
name: meta-ads-weekly-intelligence
description: Weekly strategic Meta Ads intelligence report for Ben (founder). Reads intelligence.json + meta_ads_campaigns.json from Antonio's tcc-dashboard GitHub repo. Produces funnel health overview, ROAS scaling guidance, BOF booking growth plan, creative needs analysis, spend scaling recommendations, and cross-platform insights. Runs every Monday after the weekly cron pipeline refreshes the data.
---

# Meta Ads Weekly Intelligence

Strategic weekly intelligence report for Ben Hawksworth (founder). This is the birds-eye funnel view that tells Ben where the business stands on Meta Ads and what to do next.

## Purpose

Ben's brief (April 2026):

> Connected to our intelligence dashboard & GitHub repo. Gives weekly feedback and recommendations. Tells us where we need to improve our funnel. Tells us how we can get more BOF call bookings. Tells us what new creatives we need. Tells us what to do with increasing spend on creatives.

This skill delivers all six points in a single weekly report.

## Data Source

All data comes from Antonio's `tcc-dashboard` GitHub repo (forked at `SudhakaPr/tcc-dashboard`). The weekly Python pipeline runs every Monday 06:00 UTC and commits fresh data to `public/data/`.

**Files this skill reads:**

| File | What it contains | Used for |
|---|---|---|
| `intelligence.json → meta_ads` | Opus's strategic analysis: weekly priorities, ad set verdicts, creative verdicts, anomalies, quality flags, TOF/MOF/BOF recommendations | Core intelligence layer |
| `intelligence.json → cross_platform` | Cross-channel strategy, market trends, hooks to repurpose | Context + creative inspiration |
| `meta_ads_campaigns.json` | Structured ad set × creative breakdown with 7d + 28d metrics, creative audience matrix, account summary | Operational numbers |
| `SCHEMA.md` | Field-by-field schema documentation | Reference only |

**Important:** Do NOT call Meta API directly. The weekly cron handles data collection. This skill only reads the committed JSON files.

## Instructions for Claude

When this skill is invoked:

### Step 1 — Refresh data

Credentials are in the project root `.env` file:
- `TCC_GITHUB_TOKEN` — GitHub PAT for cloning/pulling the repo
- `TCC_GITHUB_REPO` — repo URL (SudhakaPr/tcc-dashboard)

If the repo is not yet cloned locally:
```bash
source .env
git clone https://${TCC_GITHUB_TOKEN}@github.com/SudhakaPr/tcc-dashboard.git /tmp/tcc-dashboard
```

If already cloned, pull latest:
```bash
cd /tmp/tcc-dashboard && git pull
```

Ensure the latest Monday data is pulled.

### Step 2 — Read the data files

Read these two files:
- `<path>/public/data/intelligence.json`
- `<path>/public/data/meta_ads_campaigns.json`

### Step 3 — Generate the weekly report

Present the output in this exact order:

---

**a) Executive Summary**

One paragraph. Pull from `intelligence.meta_ads.channel_tldr` + `meta_ads_campaigns.summary`. Include:
- Total weekly spend + trend vs previous week (if available from 28d data)
- Total calls booked + cost per call
- Best performing ad set + worst performing ad set
- One sentence on the single biggest opportunity this week

**b) Funnel Health Check**

Table from `meta_ads_campaigns.ad_sets` joined with `intelligence.meta_ads.ad_set_verdicts`:

| Ad Set | Status | Learning | Spend 7d | CTR link | CPC link | Calls | Cost/Call | Verdict |
|---|---|---|---|---|---|---|---|---|

Below the table: 2-3 sentence interpretation. Where is the funnel leaking? Which stage (TOF/MOF/BOF) needs attention?

**c) BOF Call Booking Growth**

This is Ben's primary concern. Answer: "How do we get more BOF call bookings?"

Pull from:
- `intelligence.meta_ads.bof_recommendations` (Opus's specific recommendations)
- `meta_ads_campaigns.creative_audience_matrix` (which creatives drive calls in which audiences)
- Ad set verdicts (which audiences convert best)

Structure:
1. Current state: X calls/week at £Y/call from Z ad sets
2. Biggest lever: [specific action with numbers]
3. Second lever: [specific action]
4. Third lever: [specific action]

Each lever must reference specific creatives and ad sets by name with actual numbers.

**d) Creative Needs Analysis**

Answer: "What new creatives do we need?"

Pull from:
- `intelligence.meta_ads.creative_verdicts` (what's working, what's dying)
- `intelligence.meta_ads.tof_recommendations` + `bof_recommendations`
- `intelligence.meta_ads.quality_flags` (what Meta is penalising)
- `intelligence.cross_platform.top_hooks_to_repurpose` (hooks from other channels)

Structure:
1. **Kill list** — creatives to turn off (verdict = kill, with reason + numbers)
2. **Scale list** — creatives to increase spend on (verdict = scale, with reason + numbers)
3. **New creative briefs** — 3-5 specific creative concepts to produce, each with:
   - Format (reel / graphic / carousel)
   - Hook angle
   - Target audience (warm / cold lookalike / cold interest)
   - Why (grounded in data or cross-channel insight)
   - Inspired by (competitor or own top performer reference)

**e) Spend Scaling Guidance**

Answer: "What do we do with increasing spend on creatives?"

Pull from:
- `meta_ads_campaigns.ad_sets` (current budget splits)
- `intelligence.meta_ads.ad_set_verdicts` (scale/watch/kill by ad set)
- `intelligence.meta_ads.anomalies` (delivery gaps, frequency fatigue)

Structure:
1. Current budget split vs target (50 BOF / 30 MOF / 20 TOF)
2. Recommended reallocation (specific £ amounts per ad set)
3. Scale readiness per ad set:
   - Learning phase status
   - Frequency risk
   - Creative diversity (enough ads to scale without fatigue?)
4. "If we add £X/day, put it here because [reason]"

**f) Anomalies & Quality Flags**

Pull from `intelligence.meta_ads.anomalies` + `intelligence.meta_ads.quality_flags`.

Numbered list, ordered by severity (high → medium → low). Each entry:
- What's happening (with numbers)
- Why it matters
- What to do about it

**g) This Week's Priority Actions**

Pull from `intelligence.meta_ads.weekly_priorities`. Present as numbered list (max 5).

Each priority:
- **Action** — specific, actionable (name the ad set / creative / budget change)
- **Why** — grounded in numbers
- **Impact** — what happens if we do/don't do this

**h) Cross-Platform Context (Optional)**

If `intelligence.cross_platform` has relevant insights for Meta Ads (hooks to repurpose, market trends affecting ad performance), include a brief section:
- 2-3 bullet points from cross-channel insights relevant to ad creative or positioning
- Any hooks from email/YouTube/Instagram worth testing as ad hooks

### Step 4 — Save the report

Save to `outputs/WEEKLY-INTELLIGENCE-[YYYY-MM-DD].md`

---

## Output Format

```markdown
# Weekly Meta Ads Intelligence — [Date]

**Week:** 2026-W16
**Data refreshed:** [intelligence._metadata.generated_at]
**Prepared for:** Ben Hawksworth (Founder)

---

## Executive Summary

[One paragraph with key numbers and single biggest opportunity]

---

## Funnel Health Check

| Ad Set | Status | Learning | Spend 7d | CTR link | CPC link | Calls | Cost/Call | Verdict |
|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

[2-3 sentence interpretation]

---

## BOF Call Booking Growth

**Current state:** [X] calls/week at £[Y]/call

1. **[Lever 1]** — [specific action + expected impact]
2. **[Lever 2]** — [specific action + expected impact]
3. **[Lever 3]** — [specific action + expected impact]

---

## Creative Needs

### Kill
- **[Creative name]** — [reason with numbers]

### Scale
- **[Creative name]** — [reason with numbers]

### New Creative Briefs
1. **[Concept]** — [format] for [audience]. Hook: "[hook]". Why: [data reason]. Inspired by: [reference].

---

## Spend Scaling Guidance

**Current split:** [actual] vs **Target:** 50/30/20

[Recommended reallocation table]

**Scale readiness:**
- [Ad set]: [ready/not ready] — [reason]

**If adding £X/day:** [specific recommendation]

---

## Anomalies & Quality Flags

1. **[HIGH]** [Description] → [Action]
2. **[MEDIUM]** [Description] → [Action]

---

## This Week's Priorities

1. **[Action]** — Why: [reason]. Impact: [what happens].
2. ...

---

## Cross-Platform Context

- [Insight relevant to Meta Ads]
- [Hook worth testing]

---

*Generated by meta-ads-weekly-intelligence skill | Data: tcc-dashboard weekly pipeline*
```

## Step 5 — Dashboard prompt

After saving the markdown report, ask the user:

> "Report saved. Want me to generate an HTML dashboard from this?"

If yes:
1. Convert the markdown report into a single-file HTML dashboard
2. Use Tailwind CSS via CDN for styling
3. Include:
   - Colour-coded verdict badges (green = scale, amber = watch, red = kill)
   - Tables with alternating row colours
   - Anomaly cards with severity colour coding (red = high, amber = medium)
   - Spend allocation bar chart (current vs target, CSS-only)
   - Creative matrix heatmap (CTR values colour-coded: green ≥ 1.5%, amber 0.8-1.5%, red < 0.8%)
   - Collapsible sections for each report area
   - Print-friendly layout
4. Save to `outputs/WEEKLY-DASHBOARD-[YYYY-MM-DD].html`
5. Open in default browser: `open outputs/WEEKLY-DASHBOARD-[YYYY-MM-DD].html`

If no: skill ends after the markdown report.

---

## Thresholds

Same as `meta-ads-daily-review` (shared framework):

| Metric | Threshold |
|---|---|
| CTR link kill | < 0.8% |
| CTR link target | ≥ 1.5% |
| Cost per call healthy | ≤ £50 |
| Cost per call problem | > £75 |
| Landing page booking rate | ≥ 8% |
| Budget split target | 50% BOF / 30% MOF / 20% TOF |

## Ben's Voice Rules

Output uses analytical prose but follows Ben's brand voice for any commentary:

- British English (£, optimise, behaviour, organisation)
- No em-dashes, no AI filler phrases
- Short, direct sentences
- "Business owners and service providers" (never "coaches")
- See `CLAUDE.md` for full forbidden-phrases list

## Repo Access

Clone URL (with PAT):
```
git clone https://<PAT>@github.com/SudhakaPr/tcc-dashboard.git
```

Or pull from antonio-gasso/tcc-dashboard if you have access to the upstream.

## Files

- `skill.md` — this file
- `outputs/` — generated weekly reports

## Integration

**Weekly workflow for Ben (founder):**
1. Monday morning (after 06:00 UTC cron completes): run `/meta-ads-weekly-intelligence`
2. Skill pulls latest data from GitHub
3. Report generated in ~30 seconds
4. Ben reviews funnel health, priorities, creative needs, spend guidance
5. Delegates actions to Ben Mahmoud (daily review) and team

**Daily complement:** `meta-ads-daily-review` skill handles Ben Mahmoud's operational daily campaign reviews using the same data source.

## Version

**v1.0 (initial)** — built 2026-04-15

- Reads from `tcc-dashboard` GitHub repo (SudhakaPr fork)
- intelligence.json (Opus analysis) + meta_ads_campaigns.json (operational data)
- Full schema documented in `public/data/SCHEMA.md`
