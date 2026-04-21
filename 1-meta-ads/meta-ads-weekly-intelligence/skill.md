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
| `meta_ads_campaigns.json` | Structured ad set × creative breakdown with 7d + 28d metrics, creative audience matrix, account summary. Includes `stage` (TOF/MOF/BOF), `stage_spend_7d`, `data_caveats` | Operational numbers |
| `ghl_dms.json` | IG DM funnel (inbound/outbound threads, 7d) — BOF downstream signal | Diagnosing ad vs landing vs DM bottleneck |
| `SCHEMA.md` | Field-by-field schema documentation (breaking change 2026-04-17) | Reference only |

**Important:** Do NOT call Meta API directly. The weekly cron handles data collection. This skill only reads the committed JSON files.

**Field naming (2026-04-17 breaking change):** Antonio's pipeline renamed `calls_booked*` → `form_submits*` after the double-count incident. A form submit is NOT a booked call — historical ratio is roughly 4.5 form submits per booked call. Ground truth for bookings is Mahmoud's manual sheet until STS rollout. Never label `form_submits` as "calls booked" in the output.

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

Read these files:
- `<path>/public/data/intelligence.json`
- `<path>/public/data/meta_ads_campaigns.json`
- `<path>/public/data/ghl_dms.json` (for BOF DM funnel diagnosis)
- `<path>/public/data/SCHEMA.md` (only when a field is ambiguous — it's the source of truth)

Before interpreting numbers, surface anything in `meta_ads_campaigns.summary.data_caveats` — those are Antonio's active caveats (e.g. "form submits are not booked calls", GHL gaps, paused ad sets). They must show up at the top of the report.

### Step 3 — Generate the weekly report

Present the output in this exact order:

---

**a) Data Caveats (always first)**

Render every entry from `meta_ads_campaigns.summary.data_caveats` as a bullet list before any analysis. No report should open with numbers when there is an active caveat — the reader needs to know what's directional vs exact first.

**b) Executive Summary**

One paragraph. Pull from `intelligence.meta_ads.channel_tldr` + `meta_ads_campaigns.summary`. Include:
- Total weekly spend + trend vs previous week (from 28d data)
- Total form submits (`total_form_submits_7d`) and cost per form submit (`overall_cost_per_form_submit_7d`) — label both clearly as form submits, not calls
- Estimated booked calls using the 4.5:1 rule of thumb, with "pending Mahmoud's sheet" caveat
- Best performing ad set + worst performing ad set (by stage)
- One sentence on the single biggest opportunity this week

**c) Funnel Health Check**

Table from `meta_ads_campaigns.ad_sets` joined with `intelligence.meta_ads.ad_set_verdicts`. Group rows by `stage` (BOF → MOF → TOF) so the funnel reads top-down.

| Stage | Ad Set | Status | Learning | Spend 7d | Key metric | Form submits | Cost/form submit | Verdict |
|---|---|---|---|---|---|---|---|---|

"Key metric" depends on stage:
- **BOF** → CTR link, cost per form submit
- **MOF** → cost per opt-in, DM conversations (`ghl_dms.totals.threads_7d` when relevant)
- **TOF** → ThruPlay rate, CPM, frequency (NEVER surface cost per form submit for TOF — that's a category error per SCHEMA)

Below the table: 2-3 sentence interpretation using `stage_spend_7d`. Where is the funnel leaking? Which stage needs attention?

**d) BOF Call Booking Growth**

This is Ben's primary concern. Answer: "How do we get more booked calls?" (not form submits)

Pull from:
- `intelligence.meta_ads.bof_recommendations` (Opus's specific recommendations)
- `meta_ads_campaigns.creative_audience_matrix` (which creatives drive form submits in which audiences — filter to `stage = BOF`)
- Ad set verdicts (which BOF audiences convert best)
- `ghl_dms.json` (is the DM funnel catching the submits? Look at `threads_7d`, inbound/outbound ratio)

Structure:
1. Current state: X form submits/week at £Y/submit → ~Z estimated bookings (4.5:1 ratio, directional)
2. Biggest lever: [specific action with numbers — name the ad set / creative]
3. Second lever: [specific action]
4. Third lever: [specific action — e.g. DM response gap if outbound/inbound ratio is off]

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

**e → f) Spend Scaling Guidance** (renumbered after Data Caveats became section a)

Answer: "What do we do with increasing spend on creatives?"

Pull from:
- `meta_ads_campaigns.summary.stage_spend_7d` (actual BOF/MOF/TOF split in £)
- `meta_ads_campaigns.ad_sets` (per-ad-set budget, grouped by `stage`)
- `intelligence.meta_ads.ad_set_verdicts` (scale/watch/kill by ad set)
- `intelligence.meta_ads.anomalies` (delivery gaps, frequency fatigue, stage_mismatch)

Structure:
1. Current split (from `stage_spend_7d`) vs target **50 BOF / 30 MOF / 20 TOF**
2. Recommended reallocation — specific £ amounts per ad set, respecting stage
3. Scale readiness per ad set:
   - Learning phase status (`learning_stage` field)
   - Frequency risk (TOF fatigue threshold > 3.5)
   - Creative diversity (enough ads in the stage to scale without fatigue?)
4. "If we add £X/day, put it here because [reason grounded in stage + verdict]"

**f) Anomalies & Quality Flags**

Pull from `intelligence.meta_ads.anomalies` + `intelligence.meta_ads.quality_flags`.

Numbered list, ordered by severity (high → medium → low). Each entry:
- What's happening (with numbers)
- Why it matters
- What to do about it

**g) Paid ROAS Snapshot**

Pull from `intelligence.meta_ads.roas_snapshot` (added 2026-04-20 by Antonio). This is the deterministic paid ROAS view — real Calendly bookings tagged with the `-pa` slug joined against Meta spend and `sheet_revenue.json` from Rob's Master Client Tracker.

Render as:
- **7-day paid calls booked** (`roas_snapshot.paid_calls_7d`)
- **28-day paid pipeline** (`roas_snapshot.paid_pipeline_28d`)
- **7-day paid spend** (`roas_snapshot.spend_7d`)
- **Closed revenue** (`roas_snapshot.revenue_closed`) with a "£0 closed yet" note if zero
- **ROAS** = revenue / spend when revenue > 0, else "pending closes"

This section replaces the form-submit-based booking estimate from `meta-ads-daily-review`. When available, always prefer the `roas_snapshot` numbers over the 4.5:1 directional fallback — they come from real Calendly bookings, not pixel leads.

**h) This Week's Priority Actions**

Pull from `intelligence.meta_ads.weekly_priorities`. Present as numbered list (max 5).

Each priority:
- **Action** — specific, actionable (name the ad set / creative / budget change)
- **Why** — grounded in numbers
- **Impact** — what happens if we do/don't do this

**i) Cross-Platform Context (Optional)**

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

## Paid ROAS Snapshot

| Metric | Value |
|---|---|
| Paid calls booked (7d) | [roas_snapshot.paid_calls_7d] |
| Paid pipeline (28d) | [roas_snapshot.paid_pipeline_28d] |
| Paid spend (7d) | £[roas_snapshot.spend_7d] |
| Revenue closed | £[roas_snapshot.revenue_closed] |
| ROAS | [see rendering rule below] |

**ROAS display rule (per Antonio 2026-04-20):** When `paid_calls_booked_7d > 0` and `paid_revenue_7d == 0`, display **"Pending"**, not "0.00x". Rationale: the pipeline-pending state (paid calls booked, sales not closed yet) is a normal sales-cycle lag, not a failure signal. Only show the numeric ROAS when `paid_revenue_7d > 0`.

*Source: `intelligence.meta_ads.roas_snapshot` — Calendly bookings tagged `-pa` joined against Meta spend + Master Client Tracker revenue.*

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

## Step 5 — Auto-generate HTML dashboard

Every run produces both the markdown report AND the HTML dashboard — no prompt, no opt-in. Per Antonio 2026-04-20: Ben should get the visual rendering by default so there's no extra click between "skill finished" and "I can read it."

After saving the markdown report:

1. Convert the markdown report into a single-file HTML dashboard
2. Use Tailwind CSS via CDN for styling
3. Include:
   - Colour-coded verdict badges (green = scale, amber = watch, red = kill)
   - Tables with alternating row colours
   - Anomaly cards with severity colour coding (red = high, amber = medium)
   - Spend allocation bar chart (current vs target, CSS-only)
   - Creative matrix heatmap (CTR values colour-coded: green ≥ 1.5%, amber 0.8-1.5%, red < 0.8%)
   - ROAS tile: render "**Pending**" in neutral grey when paid calls > 0 and paid revenue = 0 (Antonio UX rule). Render the numeric ROAS in green (≥ 2x) / amber (1–2x) / red (< 1x) only when revenue > 0.
   - Collapsible sections for each report area
   - Print-friendly layout
4. Save to `outputs/WEEKLY-DASHBOARD-[YYYY-MM-DD].html`
5. Open in default browser: `open outputs/WEEKLY-DASHBOARD-[YYYY-MM-DD].html`

Markdown remains the persisted, git-friendly output for week-over-week diffs. HTML is the rendered view for Ben.

---

## Thresholds (per stage — aligned with SCHEMA 2026-04-17)

Never apply a BOF threshold to a TOF/MOF campaign. Each stage is judged on its own metric.

**TOF** — awareness / video views / reach
- ThruPlay rate (higher is better)
- CPM > £25 = concern
- Frequency > 3.5 = fatigue
- **Never kill a TOF ad set for zero form submits** — category error

**MOF** — engagement / opt-ins / DM
- Cost per opt-in (not cost per call)
- DM conversations started (from `ghl_dms.totals.threads_7d`)
- Inbound-to-outbound ratio (DM funnel health)

**BOF** — application / call booking
- CTR link < 0.8% = kill candidate
- CTR link ≥ 1.5% = target
- Cost per form submit ≤ £50 = healthy, > £75 = problem
- Landing page form rate ≥ 8%

**Budget split target:** 50% BOF / 30% MOF / 20% TOF (`summary.stage_spend_7d` reports actual).

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

**v1.2 (2026-04-21)** — ROAS snapshot + auto HTML dashboard
- Added section (g) for `intelligence.meta_ads.roas_snapshot` — real paid calls booked (Calendly `-pa` slug), 28-day paid pipeline, spend, revenue, ROAS
- HTML dashboard now generated every run (no opt-in prompt) alongside markdown
- Section letters shifted: Priorities → h, Cross-Platform → i

**v1.1 (2026-04-19)** — aligned with SCHEMA breaking change

- `calls_booked*` → `form_submits*` across all reads
- Added `ghl_dms.json` for BOF DM funnel diagnosis
- Per-stage thresholds (TOF/MOF/BOF judged separately)
- `data_caveats` block is now section (a) of every report
- Booked-call estimate uses 4.5:1 form-to-book ratio (directional) until Mahmoud's sheet/STS lands

**v1.0 (2026-04-15)** — initial
- Reads from `tcc-dashboard` GitHub repo (SudhakaPr fork)
- intelligence.json (Opus analysis) + meta_ads_campaigns.json (operational data)
