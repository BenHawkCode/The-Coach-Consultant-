---
name: meta-ads-daily-action-plan-new
description: One-page Meta Ads daily action plan in Ben's preferred format. Five sections — Yesterday's Number, Kill Today, Scale Today, Anomaly Alert, Today's Priority — under 30 short lines. Pulls from the same data sources as the v1 skill (daily-review JSONs + dashboard JSONs + Calendly + sheet revenue + yesterday's plan), inherits all framework rules from `1-meta-ads/CLAUDE.md`, but the output is action-only with no narrative blocks. Layered on top of vertical-scaling thinking — every recommendation links back to a pain angle from `docs/new-ip/06-pain-isolation.md` so the AI thinks like a strategist, not a number reporter.
---

# Meta Ads Daily Action Plan — New Format

Same brain, different output. The v1 skill writes a comprehensive consultant-style brief. This one writes the one-pager Ben wrote himself for Mahmoud (5 May 2026 example below). Mahmoud opens it, scans it in 60 seconds, applies the actions in Ads Manager, closes it.

## Why this exists (separate from v1)

Ben H sent Mahmoud a one-pager example, told Antonio "this is what we want from now on". v1 brief is too long. The numbers and analysis are right, but Mahmoud doesn't read past Action 2. This skill ships the same analysis in the format that gets read.

Critically, this version layers vertical-scaling thinking on top: every recommendation should link back to which pain angle from `docs/new-ip/06-pain-isolation.md` and `docs/new-ip/10-pain-point-articulation.md` is being addressed. The output is short, but the recommendations are sharper because the AI is asked to think in terms of pain coverage, not just metric thresholds.

## Reference example (Ben's hand-written one, 5 May 2026)

```
05 May 2026

Yesterday's Number
Spend: £35.98
Calendly calls: 2 (master sheet, Week 3)
Cost per call: N/A (master sheet cost per call null)
ROAS: Pending (cash maturing, 7-14 day lag)
Cash sales: Pending (cash maturing, 7-14 day lag)
Status: Watch (BOF is the only active spend yesterday at £35.98 with 0 pixel calls; master sheet shows 2 booked calls for the week but cost per call and ROAS are unconfirmed, and cost per follower on profile visit ads is £3.20, sitting in the amber zone between healthy and problem.)

Kill Today
1. Graphic - If you're consultant WHITE (Warm V2 - Retargeting 30%)
Reason: £0.03 spend over 7 days, 0 clicks, 0 calls, CTR 0% - no spend being allocated but creative is dead weight pulling ad set data; pause to consolidate budget to converting creatives.
Daily saving: ~£0/day direct but frees ad set budget allocation

2. Graphic - If you're SP WHITE (Warm V2 - Retargeting 30%)
Reason: 0% CTR across 18 impressions, 0 calls pixel, £0.39 spent at £21.67 CPM with no returns; tiny spend but underperforming against all creative peers in the same ad set.
Daily saving: ~£0.06/day

Scale Today
1. Graphic 6 - old vs ai (Warm - Retargeting 30%)
Budget change: Prioritise budget allocation within ad set
Why: 2.0% CTR and 2 pixel calls from only £1.20 spend over 7 days - strongest conversion signal in the entire account by cost per pixel call (£0.60). Meta is under-serving it; flag to Meta for more delivery or duplicate into its own ad set.

2. Warm - Retargeting 30% (BOF Campaign 4)
Budget change: +£10/day
Why: 4.26% CTR over 7 days, £24.74 pixel cost per call (well under £75 threshold), 2 pixel calls on £49.48 spend. Best performing ad set with room to scale before hitting efficiency ceiling.

Anomaly Alert
MOF Webinar ad sets (Cold - Interest Based and Warm - Retargeting) show 14 pixel calls combined over 7 days at £0 spend - these calls are almost certainly from a prior active period and the pixel is attributing them retrospectively. Do not use these for decision-making. MOF campaigns appear fully paused with zero impressions and zero spend.

Today's Priority
Check why 'Graphic 6 - old vs ai' is receiving only £1.20 of budget over 7 days despite the strongest pixel conversion rate in the account - manually boost its budget weighting or isolate it into a dedicated ad set today before the weekly review window closes.
```

That's the gold-standard. Mimic the structure exactly.

## Inputs (read in this order, same as v1)

| File | Purpose |
|---|---|
| `1-meta-ads/meta-ads-daily-review/outputs/DAILY-REVIEW-*-{today}.json` | Live Meta API + Calendly per BOF campaign run today |
| `/tmp/tcc-dashboard/public/data/intelligence.json` | Opus strategic verdicts, anomalies, weekly priorities, staleness warnings |
| `/tmp/tcc-dashboard/public/data/meta_ads_campaigns.json` | 7d + 28d ad-set + creative breakdown for ALL stages |
| `/tmp/tcc-dashboard/public/data/calendly_bookings.json` | Real paid bookings (ground truth) |
| `/tmp/tcc-dashboard/public/data/sheet_revenue.json` | Signups + revenue (literal `name` field is binding) |
| `1-meta-ads/meta-ads-daily-action-plan-new/outputs/{yesterday}.md` | Yesterday's plan, for carry-forward and "did we act on it?" tracking |
| `docs/new-ip/06-pain-isolation.md` | Six pain layers — used to tag creatives and surface pain-coverage gaps |
| `docs/new-ip/10-pain-point-articulation.md` | Verbatim pain quotes + ready-made hooks for new creative briefs |

If today's daily-review JSON for a BOF campaign is missing, run `bash 1-meta-ads/meta-ads-daily-review/setup.sh --campaign-id <ID> --week <N> --days 7` per active BOF campaign first.

## Reasoning framework (inherits from `1-meta-ads/CLAUDE.md`)

All analysis rules are the same as v1. Read v1 skill (`meta-ads-daily-action-plan/skill.md`) §Reasoning Framework if needed. Summary of what stays:

- Stage classification first (TOF / MOF / BOF). Use the `stage` field in `meta_ads_campaigns.json`.
- Per-stage metrics. BOF on cost per real Calendly call (account headline) + `cost_per_booking_pixel_7d` (per ad set).
- BOF kill/scale/watch thresholds anchored on `cost_per_booking_pixel_7d`: ≤ £150 with ≥ 2 bookings = scale, ≤ £200 = healthy, £200-£300 = watch, > £300 sustained = kill candidate.
- CTR link < 0.8% kill candidate, ≥ 1.5% healthy, ≥ 2.5% scale signal.
- Min 1,000 impressions per ad set for a verdict.
- Never kill in `LEARNING` / `LEARNING_LIMITED`.
- Pixel match-rate edge case: 0 pixel bookings + non-zero applications + non-zero Calendly = ad blocker / cookie loss, NOT a kill.
- ROAS: numerator = sheet revenue email-matched to Calendly paid_ads_28d, denominator = BOF spend only. "Pending" if denominator > 0 and numerator = 0.
- Read `intelligence._metadata.meta_ads_staleness_warning`. If `CRITICAL`, abort.

## Vertical-scaling layer (new in this skill)

Every Kill / Scale / Anomaly / Priority recommendation must answer: **which pain angle is this addressing, and which pain angle is missing from the active creative pool?**

### Step 1 — Tag every active creative against a pain layer

Read creative names + ad-copy hints from `meta_ads_campaigns.json.ad_sets[].ads[].creative` (where available, otherwise use creative name as the proxy). Map each one to one of the six layers from `docs/new-ip/06-pain-isolation.md`:

1. **Guesswork Tax** — every decision is a guess (hooks: "every campaign you run is a coin flip", "you have no AI intelligence behind a single decision")
2. **Bottleneck Identity** — everything runs through the founder ("you are the bottleneck of your business", "9pm doing admin")
3. **Trust Trauma** — burnt by mentors, frameworks just the same, debt
4. **Plate Anxiety** — "I cannot add any more stress to my plate"
5. **Partner Pressure** — relationship strain from the rollercoaster
6. **AI Era Anxiety** — watching AI-forward competitors pull away

Some creative names are pain-explicit ("9pm doing admin" → Bottleneck Identity, "old vs ai" → AI Era Anxiety). Others are identity callouts only ("If you're coach WHITE", "If you're BIZ owner WHITE") and need either the actual creative content OR a manual mapping from Mahmoud to confirm pain. When the mapping is uncertain, label as "identity callout (pain unspecified)" and surface the gap.

### Step 2 — Identify pain-coverage gaps

Across the active BOF creative pool, count which of the six layers are represented and which are absent. Example:

```
Active BOF creatives (Warm V2 - Retargeting 30%, 5 active):
- "Graphic 6 - old vs ai"               → AI Era Anxiety
- "Graphic - If you're BIZ owner WHITE" → Identity callout (pain unspecified)
- "Graphic - If you're coach WHITE"     → Identity callout (pain unspecified)
- "Graphic 5 - the numbers"             → Cost-of-inaction
- "Reel 4 - Client best kept secret"    → Visibility (legacy old-IP angle)

Pain coverage:
✓ AI Era Anxiety
✗ Guesswork Tax (HERO PAIN — missing)
✗ Bottleneck Identity (close-second — missing)
✗ Trust Trauma
✗ Plate Anxiety
✗ Partner Pressure
```

### Step 3 — Use the gap when sourcing the Top Priority

If a hero pain (Guesswork Tax) or close-second pain (Bottleneck Identity) is missing from the active creative pool, that becomes a candidate for "Today's Priority" — either propose a new creative brief or ask Mahmoud to confirm whether one of the unlabeled identity creatives actually addresses the pain. Verbatim hooks for new briefs come from `docs/new-ip/10-pain-point-articulation.md` — never invent language, lift it.

### Step 4 — Don't add a new section for this

Vertical scaling is reasoning that informs the existing five sections, not a sixth section. The output stays the Ben one-pager. The sharpening shows up in the Reason / Why / Today's Priority lines, where the recommendation references the pain angle ("scale because this is the only Bottleneck Identity creative converting", "kill because this Identity callout has no pain anchor and is competing for budget against pain-anchored creatives").

## Output structure (binding)

Mimic Ben's example exactly. ONE Google Doc per day. Filename: `Meta Ads Daily Action Plan — {YYYY-MM-DD}`. Local mirror at `outputs/{YYYY-MM-DD}.md`.

The skill writes markdown, then `jay-skills/md-to-gdocs/convert.py` converts to `.docx`, then `gws drive files copy` with `mimeType=application/vnd.google-apps.document` lands the styled Google Doc in the Daily Action Plans folder. Markdown structure must match Ben's reference doc structure 1:1 (which uses HEADING_1 for date, HEADING_2 for sections, bullet lists for metrics + reasons).

### Markdown template

```markdown
# {DD Month YYYY}

## Yesterday's Number

- Spend: £{X} ({optional context like "Warm V2 day three burn, 7d total now £Y"})
- Calendly calls: {N} in 7d, {M} in 28d (master sheet, Week {W})
- Cost per call: £{Y} (or "N/A (...)" with rationale)
- ROAS: {value or "Pending (cash maturing, 7-14 day lag)"}
- Cash sales: {value or "Pending (cash maturing, 7-14 day lag)"}

Status: {Watch / Healthy / Concern} ({one-sentence rationale tying to BOF stage spend, pixel match rate, TOF cost per follower if applicable})

## Kill Today

1. {Creative name} ({Ad set name}) — {qualifier like "soften hook, do not kill angle" or omit if straight kill}

- Reason: {1-2 sentences. Cite the metric breach + pain-angle context, e.g. "this is an Identity callout creative with no pain anchor, underperforming all pain-anchored peers in the ad set."}
- Daily saving: £{Z}/day (or "frees ad set budget allocation", or "£0/day, this is a copy fix not a budget cut")

2. {Creative name} ({Ad set name}) — {qualifier}

- Reason: {as above}
- Daily saving: £{Z}/day

## Scale Today

1. {Creative or ad set name} ({Ad set / campaign name})

- Budget change: {+£X/day, or "Prioritise budget allocation within ad set", or "Hold {X} daily budget, do not pause", or "Duplicate into dedicated ad set"}
- Why: {1-2 sentences. Cite the metric strength + pain-angle context, e.g. "2.0% CTR and 2 pixel calls from £1.20 spend over 7 days, strongest conversion signal in the account, AI Era Anxiety is currently the only converting pain anchor, scale before pool exhausts."}

2. {as above}

## Anomaly Alert

{1-3 sentences naming THE most material anomaly. Don't list eight. If material anomalies stack, write the one Mahmoud must act on today. Pixel match-rate gaps, MOF dead-cohort spend, learning-phase stuck, single-creative dominance > 40%, etc.}

## Today's Priority

{ONE paragraph (1-3 sentences). The single thing that compounds if not closed today. Often a carry-forward. Sometimes a pain-coverage gap ("the BOF pool has zero Bottleneck Identity creatives, brief one today using the verbatim hooks in docs/new-ip/10"). Sometimes a pixel-fix open loop. Always one thing.}
```

### Hard formatting rules

- **Date** is `# H1` (e.g. `# 07 May 2026`). No day-of-week prefix, no year-first.
- **Section headings** are `## H2` exactly: `Yesterday's Number`, `Kill Today`, `Scale Today`, `Anomaly Alert`, `Today's Priority`. No alternative wording.
- **Yesterday's Number metrics** (Spend, Calendly calls, Cost per call, ROAS, Cash sales) → bullet list (`- `).
- **Status: ...** sits below the bullet list as a normal paragraph (NOT a bullet).
- **Kill Today / Scale Today items** are numbered (`1. `, `2. `) at top level, followed by Reason / Why / Budget change / Daily saving as bullets (`- `) underneath.
- **Em-dashes (—) are allowed in this skill output** (Ben uses them in his reference doc). This is a deliberate exception to the global TCC voice rule. Use them where Ben would: between a creative name and a qualifier (`Reel NEW - 100k staff wages — soften hook`), or as a clause break inside Anomaly Alert / Today's Priority paragraphs.
- **Total length target: 35-50 lines of markdown** (roughly 1 page in Google Doc once converted). The reference doc is 33 lines.

### Reference output

`outputs/2026-05-07.md` is the canonical reference written 7 May 2026 in the new format. Match that file's structure exactly when writing future briefs. The matching live Google Doc lives at `https://docs.google.com/document/d/1VU5ZQDy-0Vsv6ezBsmPqqe8InIXe-_7sBcfXGTKWoT0/edit` for visual sanity-check.

### What NOT to put in this version

- The v1 "Today's 3 Actions" multi-paragraph block. Killed.
- The v1 "Pipeline State" multi-line metric dump. Replaced by the 6-line "Yesterday's Number".
- The v1 "Ad Set Verdicts" table. The verdict shows up implicitly in Kill / Scale.
- The v1 "Today's Ads Manager Changes" bulleted list. The Kill / Scale items ARE the Ads Manager changes.
- The v1 "Yesterday's Flags — Acted On?" block. Carry-forward goes in Today's Priority.

The v1 skill keeps producing its long brief in parallel for now. Mahmoud chooses which to use day to day; Ben H gets sent the new format. Once the new format is validated, v1 can be archived.

## Tone & output rules (binding, see `1-meta-ads/CLAUDE.md` §6)

All v1 hard nevers + hard alwayses still apply. Specifically:

**Hard nevers:**
- Kill verdicts on `status=PAUSED` ad sets.
- "Simplify the form" / "reduce LP friction".
- Treat Meta pixel `lead` events as booked calls.
- Team-member names (Mahmoud, Ben, Rob, Jay, Antonio) in free-text.
- Internal snake_case in prose.
- En-dashes (–) anywhere. (Em-dash exception — see below.)
- Pad numbers to look precise on directional data.
- Paraphrase signup names from email handles (use literal `name` field).
- Word "baseline" for the 8% form-submit threshold.
- Invent pain-angle mappings when the creative content isn't visible. If unsure, label "identity callout (pain unspecified)" and ask for confirmation in Today's Priority.

**Em-dash exception (this skill only):** Ben's 5 May 2026 reference doc uses em-dashes (—) as clause breaks. This skill's output mirrors Ben's structure exactly, so em-dashes are permitted here even though the global TCC voice rule forbids them. Use them only where Ben would — between a creative name and its qualifier in numbered Kill / Scale items, or as a clause break inside Anomaly Alert and Today's Priority paragraphs. Do not use em-dashes inside the bullet-list lines (Reason, Daily saving, Budget change, Why) — those should read as plain sentences.

**Hard alwayses:**
- British English. £ for money. "Optimise", "behaviour", "organisation".
- Stage-aware verdicts.
- Per-stage reasoning when relevant.
- Pixel staleness gate (read `intelligence._metadata.meta_ads_staleness_warning`).
- Pain angle context when recommending Kill / Scale.

## Google Doc writing

The flow is `markdown → .docx → upload → copy as Google Doc → cleanup`. Tested and working as of 7 May 2026.

```bash
# Inputs
DATE=$(date +%Y-%m-%d)
TITLE="Meta Ads Daily Action Plan (NEW format) — $DATE"
FOLDER_ID=$(cat 1-meta-ads/meta-ads-daily-action-plan-new/outputs/folder_id.txt)

# 1. Markdown → .docx (md-to-gdocs handles H1/H2/bullet/numbered list styling)
python3 jay-skills/md-to-gdocs/convert.py \
    "1-meta-ads/meta-ads-daily-action-plan-new/outputs/${DATE}.md" \
    "$TITLE"

# convert.py creates a file WITHOUT .docx extension. Rename it.
mv "$TITLE" "${TITLE}.docx"

# 2. Upload .docx to Drive (note: parents in params, not as a separate flag)
DOCX_ID=$(gws drive files create \
    --upload "${TITLE}.docx" \
    --params "{\"name\":\"$TITLE\",\"parents\":[\"$FOLDER_ID\"]}" \
    --format json \
    | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

# 3. Copy with mimeType=google-apps.document to convert .docx → native Google Doc
GDOC_ID=$(gws drive files copy \
    --params "{\"fileId\":\"$DOCX_ID\"}" \
    --json "{\"name\":\"$TITLE\",\"mimeType\":\"application/vnd.google-apps.document\",\"parents\":[\"$FOLDER_ID\"]}" \
    --format json \
    | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

echo "Google Doc ready: https://docs.google.com/document/d/${GDOC_ID}/edit"

# 4. Cleanup: delete the intermediate .docx in Drive + the local .docx
gws drive files delete --params "{\"fileId\":\"$DOCX_ID\"}"
rm -f "${TITLE}.docx" download.html
```

**Folder ID:** stored in `outputs/folder_id.txt`. For TCC the value is `1pduNpfkMt3HQRs2t0z5e3L3_R5prdwUs` (Drive folder "Daily Action Plans" — same folder the v1 skill writes to).

**Why three steps and not one upload-with-conversion:** `gws drive files create` does NOT honour `mimeType=google-apps.document` on upload (the file lands as `text/markdown` or `application/vnd.openxmlformats-officedocument.wordprocessingml.document`). Conversion only happens via `files.copy` with a target mimeType. Tested both routes 7 May 2026.

## Local output (always)

Mirror to `outputs/{YYYY-MM-DD}.md` for:
- Yesterday's plan readability for tomorrow's carry-forward.
- Git diffs to show how the brief evolves.
- Drive write fallback.

## When to invoke

- Manually today: `Use the meta-ads-daily-action-plan-new skill to generate today's brief for {YYYY-MM-DD}.`
- Run alongside v1 for at least 3 days. Ship both Docs to Mahmoud + Ben H. Get format feedback before flipping the cron.
- Once validated, replace `meta-ads-daily-action-plan` cron target with this skill, archive the v1 folder.

## Pre-ship checklist

Before writing any Doc to Drive, verify:

- Bookings come from Calendly, revenue from `sheet_revenue.json` email-matched, Meta pixel only for ad-set health.
- Every Kill / Scale verdict declares its stage (BOF/MOF/TOF) implicitly via the ad set name + the threshold being applied.
- Per-stage metrics applied. No BOF thresholds on TOF or MOF.
- Kill verdicts exclude `PAUSED` ad sets.
- No team names, no snake_case, no "simplify form", no "kill immediately" directives, no em-dashes.
- Output length under 40 lines.
- Pain-angle context cited in at least one Kill or Scale Reason/Why line.
- Today's Priority is ONE sentence. One thing.

If any check fails, fix before shipping.

## Version

**v1.0 (2026-05-07)** — initial new-format skill. One-page output mimicking Ben's hand-written 5 May example. Inherits all v1 framework rules from `meta-ads-daily-action-plan/skill.md` and `1-meta-ads/CLAUDE.md`. Adds vertical-scaling pain-angle layer to sharpen recommendations. Runs in parallel with v1 until format is validated by Ben H + Mahmoud.
