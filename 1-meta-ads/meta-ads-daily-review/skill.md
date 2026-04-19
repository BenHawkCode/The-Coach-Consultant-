---
name: meta-ads-daily-review
description: Daily Meta Ads campaign review for Ben Mahmoud. Pulls live API data for BOF campaigns, runs ad set health check, creative × audience matrix, kill/scale/watch verdicts, Meta quality flags, anomaly detection, and top priorities. Replaces manual screenshot-to-Claude workflow. Uses threshold-based logic (0.8% kill, 1.5% target, £50 cost/call, 8% booking rate, 50/30/20 split). Supports weekly phase logic (weeks 1-6+).
---

# Meta Ads Daily Review

Automated daily campaign review skill for Ben Mahmoud. Replaces the manual process of screenshotting Meta Ads Manager results and pasting them into Claude. Pulls live API data and produces the same analysis format in one run.

## Purpose

Ben Mahmoud currently reviews BOF Meta Ads campaigns daily by:
1. Opening Meta Ads Manager
2. Screenshotting ad set + creative performance
3. Pasting screenshots into Claude
4. Asking for kill/scale verdicts, quality flags, anomalies, priorities

This skill automates steps 1-3 via Meta API and produces the same output format without any manual data entry.

## What This Skill Does

When invoked:

1. **Fetches live data from Meta Ads API** (campaign, ad set, ad, creative, insights endpoints)
2. **Runs ad set level health check** (impressions, CTR, CPC, calls booked, learning status)
3. **Builds creative × audience matrix** across all ad sets
4. **Assigns kill/scale/watch verdicts** per creative using threshold logic
5. **Flags Meta quality rankings** (below average detection)
6. **Detects anomalies** (CTR vs quality mismatch, delivery issues, conversion gaps)
7. **Generates top priorities list** for the week
8. **Outputs a formatted markdown report** matching the Claude reference output

## Analysis Framework

All verdicts use these thresholds (configurable via `config.yaml`):

| Metric | Threshold | Action |
|---|---|---|
| CTR kill threshold | < 0.8% | Flag for kill after sufficient impressions |
| CTR target | ≥ 1.5% | Healthy baseline |
| CTR scale signal | ≥ 2.5% consistent across ad sets | Priority scale candidate |
| Cost per form submit target | £50 | Flag if higher |
| Landing page form submit rate | 8% | Flag if lower |
| Budget split (Warm/Lookalike/Interest) | 50/30/20 | Flag if off |
| Min impressions for verdict | 1000 per ad set | Below = "insufficient data" |

**Naming note:** The skill reports `form_submits`, not `calls_booked`. A Meta pixel `lead` event is a form submission, not a booked call — historical ratio is ~4.5 form submits per booked call. The JSON output also includes an `estimated_bookings` field (form_submits / 4.5) flagged as directional until Mahmoud's sheet/STS lands. This aligns with Antonio's dashboard schema (2026-04-17 rename).

### Learning Phase Awareness

- Every ad set checked for `effective_status` (LEARNING, ACTIVE, LEARNING_LIMITED)
- If in learning phase: verdicts marked **directional**, not final
- No kill recommendations until 50 conversion events per ad set
- Budget changes discouraged during learning

### Week Phase Logic

- **Week 1:** Pure data collection, only "watch" verdicts allowed
- **Week 2:** First kill/scale decisions on creatives with enough impressions
- **Weeks 3-5:** Copy testing phase (statement vs metric vs question hook variants)
- **Week 6+:** Scale winners, rotate losers

The skill reads the current week number from `config.yaml` or accepts it as a CLI flag.

## Instructions for Claude

When this skill is invoked:

1. **Confirm the campaign to review**

   Use the AskUserQuestion tool to ask:

   **Question 1: Campaign**
   - Header: "Which campaign?"
   - Options: Pulled dynamically from Meta API (list of active BOF campaigns)

   **Question 2: Week Number**
   - Header: "What week is this campaign in?"
   - Options: Week 1, Week 2, Week 3, Week 4, Week 5, Week 6+

   **Question 3: Date Range (Optional)**
   - Header: "Date range"
   - Options: Last 7 days (default), Last 14 days, Last 30 days, Campaign lifetime

2. **Fetch live Meta Ads data:**
   ```bash
   cd 1-meta-ads/meta-ads-daily-review && bash setup.sh --campaign "<name>" --week <N> --days <N>
   ```

   Script pulls:
   - Ad set level: impressions, clicks, CTR, CPC, spend, calls booked, effective_status
   - Ad level: same metrics + creative ID + quality_ranking + engagement_rate_ranking + conversion_rate_ranking
   - Delivery issues: issues_info, delivery_info

3. **Run the analysis framework:**

   **Step A — Ad Set Health Check**
   - Build table: Ad set | Impressions | CTR | CPC | Calls booked | Learning status
   - Mark overall health (healthy / concerning / learning)

   **Step B — Creative × Audience Matrix**
   - Build table: Creative | Warm retargeting CTR | Cold lookalike CTR | Cold interest CTR | Signal
   - Signal column categories:
     - ⭐ Strongest overall (≥2.5% across all 3)
     - ⭐ Consistent across all 3 (≥ target in all)
     - ⭐ [Audience] standout (only strong in one audience)
     - Solid, watch (close to target)
     - Mixed (varies significantly)
     - Below target across board (< 1.5% in 2+ audiences)
     - Too little data (< 1000 impressions)

   **Step C — Kill / Scale / Watch Verdicts**

   Build three buckets:

   **Watch closely for scaling:**
   - Creatives with CTR ≥ 2.5% in 2+ ad sets
   - Flag as "priority scaling at week [N+1]"
   - Note the strongest audience for each

   **Watch — need more data:**
   - Creatives with impressions 1000-3000 per ad set
   - Creatives with mixed signals (strong in 1, weak in 2)

   **Concern — underperforming:**
   - CTR < 1.5% in 2+ ad sets WITH sufficient impressions
   - Quality ranking "Below Average" flagged
   - Note: do NOT kill during learning phase

   **Step D — Meta Quality Flags**
   - List every ad with `quality_ranking = BELOW_AVERAGE`
   - List every ad with `engagement_rate_ranking = BELOW_AVERAGE`
   - Explain why it matters (Meta deprioritises delivery)

   **Step E — Anomaly Detection**

   Detect and flag:
   - **CTR + quality mismatch** (high CTR but below average quality → clickbait risk)
   - **Delivery starvation** (creative getting <500 impressions while others get 5000+ → auction losing)
   - **Click-but-no-booking** (ads working, landing page broken)
   - **Spend concentration** (one creative eating >40% of ad set budget)

   **Step F — Top Priorities This Week**

   Generate ordered list of actions:
   1. Landing page issues (always first if present)
   2. Learning phase blockers (don't change budget until learning complete)
   3. Priority scale candidates (name specific creatives)
   4. Quality ranking fixes (name specific creatives)
   5. Kill candidates for next week review

4. **Output formatted report:**
   - Save to `outputs/DAILY-REVIEW-[campaign-name]-[YYYY-MM-DD].md`
   - Use the structure from the Claude reference output (ad set level, creative analysis, verdicts, anomalies, priorities)

## Data Caveat — Always Prepend

Every generated report must open with a "DATA CAVEAT" block before the ad set table. Rationale: Meta's action-type mapping to "booked calls" has not been validated against ground truth (Calendly / GHL pipeline stage / manual). Skill now de-duplicates the `lead` / `offsite_conversion.fb_pixel_lead` family (2x inflation bug fixed), but the underlying question — "is a Meta `lead` event a form submit or a booked call?" — is still open.

Keep the caveat in every report until Ben confirms:
1. Ground truth source for bookings
2. Which Meta action type represents a real booked call in his pixel
3. Attribution window

Also flag that Antonio's dashboard pipeline (`collect_own_meta.py:91`) still has the 2x bug and may show inflated numbers until patched.

## Output Format

```markdown
# Daily Review — [Campaign Name]

**Date:** 2026-04-15
**Week:** Week 2
**Date Range:** Last 7 days
**Analyst:** Ben Mahmoud (via meta-ads-daily-review skill)

---

## ⚠️ DATA CAVEAT — READ FIRST

[2-4 sentences: what's fixed, what's pending ground-truth validation, directional vs exact]

---

## AD SET LEVEL — HEALTH CHECK

[Context paragraph: learning phase status, overall health]

| Ad set | Impressions | CTR (all) | CPC (all) | Calls booked | Status |
|---|---|---|---|---|---|
| Warm — Retargeting | 13,640 | 2.26% | £0.70 | 0 | Learning |
| Cold — Lookalike | 11,126 | 2.26% | £0.87 | 1 | Learning |
| Cold — Interest | 13,586 | 2.27% | £0.86 | 3 | Learning |

[Summary paragraph]

---

## CREATIVE ANALYSIS — ACROSS ALL 3 AD SETS

| Creative | Warm retargeting | Cold lookalike | Cold interest | Signal |
|---|---|---|---|---|
| Graphic 2 — Claude specialist | 2.46% | 1.66% | 2.79% | ⭐ Strongest overall |
| ... | ... | ... | ... | ... |

---

## KILL / SCALE / WATCH VERDICTS

**Note:** [Impression volume caveat if relevant]

### Watch closely for scaling
- **[Creative]** — [reason] → [action next week]

### Watch — need more data
- [Creative list]

### Concern — underperforming
- **[Creative]** — [reason] → [recommended action]

### Meta quality flags to act on
- **[Creative]** in [ad set] — [quality issue explanation]

---

## ANOMALIES WORTH FLAGGING

- **[Creative/issue]** — [explanation + why it matters]

---

## TOP PRIORITIES FOR THIS WEEK

1. [Highest priority action]
2. [Second priority]
3. [Third priority]
4. [Fourth priority]

---

**Next review:** [suggested date]
```

## Required Environment

**`.env` file** (in skill folder):
```
META_ACCESS_TOKEN=<token>
META_ACCOUNT_ID=<account_id>
```

Reuses the same token as `meta-ad-copy` skill. Antonio will provide the new token once configured.

## Files

- `skill.md` — this file
- `fetch_daily_review.py` — Meta API data fetcher + analysis runner
- `config.yaml` — threshold logic + week phase rules (configurable)
- `setup.sh` — venv + dependency installer, entrypoint
- `outputs/` — generated daily reports

## Ben's Voice Rules (for the output narrative)

The skill uses plain analytical prose, not Ben's marketing voice. But for any commentary/recommendations:

- British English (£, optimise, behaviour, organisation)
- No dashes, no AI filler phrases
- Short, direct sentences
- "Business owners and service providers" (never "coaches")
- No corporate jargon

## Integration

**Daily workflow for Ben Mahmoud:**
1. Morning: run `/meta-ads-daily-review`
2. Answer 3 quick questions (campaign, week, date range)
3. Skill pulls data + generates report in ~30 seconds
4. Review report, action top priorities
5. No screenshots, no copy-paste

**Weekly complement:** Output feeds into `meta-ads-weekly-intelligence` skill (reads from Antonio's GitHub repo) for the birds-eye funnel view Ben (founder) sees.

## Version

**v1.0 (initial)** — built 2026-04-15 based on Ben Mahmoud's Claude conversation reference output (2026-04-14) and Ben's Meta-Ads brief.

**Pending:**
- Antonio to configure new Meta Ads token
- Raw data push to `antonio-gasso/tcc-dashboard` repo
- README from Antonio pointing to clean/raw data files
