---
name: meta-ads-daily-action-plan-new
description: Daily Meta Ads action plan in Ben's one-page magazine format. Five sections — Yesterday's Number, Kill Today, Scale Today, Anomaly Alert, Today's Priority — written so the media buyer can defend or challenge every Kill/Scale call inside 60 seconds. Pulls live daily-review JSON + dashboard intelligence + Calendly bookings + sheet revenue + yesterday's plan. Inherits all framework rules from `1-meta-ads/CLAUDE.md`. Layered with vertical-scaling thinking — every recommendation links to a pain angle from `docs/new-ip/06-pain-isolation.md` so the AI thinks like a strategist, not a number reporter. Schema-resilient: tolerates the 7 May 2026 dashboard refactor (ghl_source_filter prefix, validation_deltas field, recalibrated paid_calls_booked_28d, Webinar as a distinct stage).
---

# Meta Ads Daily Action Plan — New Format

Same brain as v1 (`meta-ads-daily-action-plan/`), different output. The v1 skill ships a comprehensive consultant-style brief. This one ships the one-pager Ben hand-wrote for Mahmoud (5 May 2026), upgraded with the visual treatment Antonio sketched in the GWS CLI internal guide and the reasoning depth Mahmoud asked for in his 5 May call.

## Why this exists (separate from v1)

Three bits of feedback shaped this skill:

1. **Ben H, 5 May 2026 hand-written one-pager** — the v1 brief is too long. The numbers and analysis are right, but Mahmoud doesn't read past Action 2.
2. **Mahmoud, 5 May call (via Antonio)** — "the format is good, but I still need a bit of context on why the AI is recommending each action, because sometimes it may suggest a kill/scale and I'll look at it and disagree." Each Kill / Scale line must carry enough reasoning for the media buyer to defend or challenge the call quickly.
3. **Antonio, 7 May Internal Setup Guide visual** — magazine-style cover (kicker + serif H1 + subtitle), an "Audience / Time / Outcome" three-cell summary box, generous spacing, calm body. The action plan should look like a respected internal document, not a cron dump.

This skill answers all three. Length is no longer capped at 33 lines — Mahmoud is fine with 1-2 pages so long as every Kill / Scale line lets him defend or challenge the call. The cap that matters is **clarity per line, not total length.**

## Reference example (Ben's hand-written one, 5 May 2026)

Plain text from the original — the *content* shape we mirror, not the visual styling.

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

[…etc, see canonical 5 May Doc]

Today's Priority
Check why 'Graphic 6 - old vs ai' is receiving only £1.20 of budget over 7 days despite the strongest pixel conversion rate in the account - manually boost its budget weighting or isolate it into a dedicated ad set today before the weekly review window closes.
```

Mimic the *content shape* exactly. The visual treatment comes from §Visual Treatment below.

## Inputs (read in this order)

| File | Purpose |
|---|---|
| `1-meta-ads/meta-ads-daily-review/outputs/DAILY-REVIEW-*-{today}.json` | Live Meta API + Calendly per BOF campaign run today |
| `/tmp/tcc-dashboard/public/data/intelligence.json` | Opus strategic verdicts, anomalies, weekly priorities, staleness warnings, validation_deltas (post 7 May refactor) |
| `/tmp/tcc-dashboard/public/data/meta_ads_campaigns.json` | 7d + 28d ad-set + creative breakdown for ALL stages |
| `/tmp/tcc-dashboard/public/data/calendly_bookings.json` | Real paid bookings (ground truth) |
| `/tmp/tcc-dashboard/public/data/sheet_revenue.json` | Signups + revenue (literal `name` field is binding) |
| `1-meta-ads/meta-ads-daily-action-plan-new/outputs/{yesterday}.md` | Yesterday's plan, for carry-forward and "did we act on it?" tracking |
| `docs/new-ip/06-pain-isolation.md` | Six pain layers — used to tag creatives and surface pain-coverage gaps |
| `docs/new-ip/10-pain-point-articulation.md` | Verbatim pain quotes + ready-made hooks for new creative briefs |

If today's daily-review JSON for a BOF campaign is missing, run `bash 1-meta-ads/meta-ads-daily-review/setup.sh --campaign-id <ID> --week <N> --days 7` per active BOF campaign first.

## Schema resilience (7 May 2026 dashboard refactor)

Antonio flagged the next cron run will change four things in `intelligence.json`. The skill must handle both pre-refactor and post-refactor shapes without crashing or silently misreading.

### 1. `paid_pipeline_breakdown_source`

- **Pre-refactor value:** `"ghl"` (exact string)
- **Post-refactor value:** `"ghl_source_filter"` (and possibly `"ghl_source_filter_v2"` etc later)

Use `.startswith("ghl")` everywhere this field is read. Never `==`. The `ghl` prefix means GHL pipeline status is the source; everything else (Calendly snapshot, Meta pixel) has different downstream handling.

### 2. New `meta_ads.validation_deltas`

Post-refactor `intelligence.json.meta_ads` will contain a `validation_deltas` object comparing API-derived numbers against Mahmoud's master sheet. Read it if present; tolerate its absence on older snapshots.

When present, surface a one-line note inside Anomaly Alert if any delta exceeds a sane threshold — e.g. "API reads 13 paid bookings 28d, master sheet shows 11. Reconcile in tomorrow's call." Don't pad if all deltas are within tolerance.

### 3. `paid_calls_booked_28d` recalibration

The pre-refactor number was email-match inflated (showed 14 on 5 May, dropped to 12 on 7 May, will land around 6 post-refactor). When the next cron lands and the number drops sharply versus yesterday's brief, the skill must NOT flag this as a campaign collapse. The drop is a counting fix, not a performance problem.

If today's number is materially lower than yesterday's stored number AND `intelligence.json._metadata` shows a fresh cron timestamp post 2026-05-08, tag the day's brief Status with a one-line note: "28d paid bookings recalibrated by the dashboard cron on {date}. Today's number is the new ground truth, not a campaign drop."

### 4. Webinar as a distinct stage

Post-refactor, the `stage` field in `meta_ads_campaigns.json.ad_sets[]` will return `WEBINAR` for webinar-funnel ad sets, separate from `MOF`. Treat WEBINAR with its own metric (cost per webinar registration / cost per webinar attendee) — not the MOF cost-per-opt-in metric. Until the post-refactor data lands, the skill maps any ad set with "Webinar" in its name into a `WEBINAR` virtual stage so the report stops describing webinar dead-cohort spend as "MOF dead-cohort spend".

The Stage Spend Snapshot in any debug output (not the public Doc) should track BOF / MOF / WEBINAR / TOF / UNKNOWN as five buckets, with the 50/30/20 budget split target re-attributed only across BOF / MOF / TOF (Webinar is a campaign-period spend bucket, not a steady-state share of always-on budget).

## Reasoning framework (inherits from `1-meta-ads/CLAUDE.md` and v1 skill)

All v1 analysis rules apply unchanged. Summary of what stays:

- Stage classification first (TOF / MOF / WEBINAR / BOF). Use the `stage` field directly. If absent, map from objective.
- Per-stage metrics. BOF on cost per real Calendly call (account headline) + `cost_per_booking_pixel_7d` (per ad set).
- BOF kill/scale/watch thresholds anchored on `cost_per_booking_pixel_7d`: ≤ £150 with ≥ 2 bookings = scale, ≤ £200 = healthy, £200-£300 = watch, > £300 sustained = kill candidate.
- CTR link < 0.8% kill candidate, ≥ 1.5% healthy, ≥ 2.5% scale signal.
- Min 1,000 impressions per ad set for a verdict.
- Never kill in `LEARNING` / `LEARNING_LIMITED`.
- Pixel match-rate edge case: 0 pixel bookings + non-zero applications + non-zero Calendly = ad blocker / cookie loss, NOT a kill.
- ROAS: numerator = sheet revenue email-matched to Calendly paid_ads_28d, denominator = BOF spend only. "Pending" if denominator > 0 and numerator = 0.
- Read `intelligence._metadata.meta_ads_staleness_warning`. If `CRITICAL`, abort.

## Strategist layer (this skill's main upgrade)

The v1 skill answered "what does the data say?" This skill must answer "what would a sharp media buyer do, and why?" That requires three new reasoning passes layered on top of the framework.

### Pass A — Vertical-scaling pain coverage

Tag every active creative against one of the six new IP pain layers (Guesswork Tax, Bottleneck Identity, AI Era Anxiety, Trust Trauma, Plate Anxiety, Partner Pressure). When an active creative is an "identity callout" (e.g. "If you're coach WHITE") with no specific pain anchor, label it explicitly and flag that the pool is under-anchored.

Across the active BOF creative pool, count which layers are represented and which are missing. If a hero pain (Guesswork Tax) or close-second pain (Bottleneck Identity) is missing, that surfaces inside Today's Priority as a brief proposal — propose a new creative angle using a verbatim hook from `docs/new-ip/10-pain-point-articulation.md`. Never invent pain language; lift it.

### Pass B — Scale-the-winner discipline

When a creative or ad set sits in the scale band (BOF: `cost_per_booking_pixel_7d ≤ £150` with ≥ 2 bookings; or CTR ≥ 2.5% sustained across ≥ 1,000 impressions; or strongest cost per follower in TOF), the skill should:

1. Recommend the budget bump explicitly (+10% / +20% / +£10/day, etc) — not vague language like "scale up".
2. Surface the headroom — how much more spend can this ad set / creative absorb before it hits efficiency ceiling. Use historic data from `meta_ads_campaigns.json` 28d window to estimate.
3. Pair the scale call with a hedge — what's the second-best creative or ad set if the winner saturates this week? The hedge becomes the natural Tuesday or Thursday follow-up.

A "scale today, hedge ready, ceiling known" recommendation is what Mahmoud can defend on a sales call. "Scale up because CTR is good" is not.

### Pass C — Close-rate ladder awareness

The skill must remember that media buying is upstream of the close. A booked call that doesn't close is wasted spend. Every recommendation should pass a final filter: does this action move the cost-per-closed-client number, not just the cost-per-booked-call number?

Two practical implications:

1. When the 28d pipeline shows N taken-no-outcome leads, surface the outcome-logging gap as a recommendation in Today's Priority — closing that loop unlocks the real ROAS read and tells Meta which creatives produced closes vs no-shows. This is often higher-leverage than any media-buying tweak.
2. When Calendly bookings are healthy but no-show rate climbs above 15% (28d), don't recommend more spend on that ad set. Recommend a thank-you-page / pre-call sequence audit instead, and surface the no-show rate inside Anomaly Alert. Spend feeds the top of the funnel; the bottleneck is downstream.

These two passes plus Pass A are what make the AI a strategist instead of a threshold reader. Every Kill / Scale / Anomaly / Priority line should pass at least one of them.

### Reasoning depth requirement (Mahmoud's 5 May feedback)

Each Kill / Scale Reason or Why line must answer three sub-questions in order:

1. **What metric / signal triggers this call?** (£220 cost per submit, 4.8% CTR with BELOW_AVERAGE quality, 28d £105 cost per pixel booking, etc.)
2. **What pain or strategic context makes the call directionally right?** (Cost-of-Inaction is one of the strongest pain anchors — soften the hook rather than kill the angle. Or: this is the only scale-band ad set in the account, hedge with second-best before the winner saturates.)
3. **What's the implicit hypothesis if the media buyer disagrees?** (If you don't think 4.8% CTR justifies a copy fix, the implicit alternative is "kill the angle entirely" — that loses Cost-of-Inaction as a working pain in the pool. Surface that trade-off so disagreement is informed.)

When all three are present in two sentences, Mahmoud can defend or challenge the call inside 30 seconds. If only the metric is cited, rewrite.

## Output structure (binding)

Mimic Ben's content shape exactly. ONE Google Doc per day. Filename: `Meta Ads Daily Action Plan — {YYYY-MM-DD}`. Local mirror at `outputs/{YYYY-MM-DD}.md`.

The skill writes markdown, then `jay-skills/md-to-gdocs/convert.py` converts to `.docx`, then `gws drive files copy` with `mimeType=application/vnd.google-apps.document` lands the styled Google Doc in the Daily Action Plans folder.

### Markdown template

```markdown
The Coach Consultant · Daily Action Plan

# {DD Month YYYY}

{One-sentence subtitle that summarises today's account state in plain language. Examples: "Pixel still blind, day six. Six fresh creatives finally close the Guesswork Tax gap." or "Warm V2 carrying the funnel alone, Cold reactivation ready to fire once the pixel reads." Always one sentence, always informative, always scannable.}

| Today's Spend | Calls | ROAS |
|---|---|---|
| £{X} (live, 7d total £{Y}) | {N} 7d / {M} 28d | {value or "Pending"} |

## Yesterday's Number

- Spend: £{X} ({optional context like "Warm V2 day three burn, 7d total now £Y"})
- Calendly calls: {N} in 7d, {M} in 28d (master sheet, Week {W})
- Cost per call: £{Y} (or "N/A (rationale)" — never bare "N/A")
- ROAS: {value or "Pending (cash maturing, 7-14 day lag)"}
- Cash sales: {value or "Pending (cash maturing, 7-14 day lag)"}

Status: {Watch / Healthy / Concern} ({one-sentence rationale tying to BOF stage spend, pixel match rate, TOF cost per follower if applicable, and any 7 May 2026 schema-refactor recalibration note}).

## Kill Today

1. {Creative name} ({Ad set name}) — {short qualifier like "soften hook, do not kill angle" or omit if straight kill}

- Reason: {Sentence 1: metric or signal that triggers the call. Sentence 2: pain-angle context + the implicit hypothesis if Mahmoud disagrees. Two sentences max.}
- Daily saving: £{Z}/day (or "frees ad set budget allocation", or "£0/day, this is a copy fix not a budget cut")

2. {Creative name} ({Ad set name}) — {qualifier}

- Reason: {as above}
- Daily saving: £{Z}/day

(If there's no second meaningful kill, write "2. No second kill recommended today" and explain in one sentence why the obvious candidates aren't being pulled.)

## Scale Today

1. {Creative or ad set name} ({Ad set / campaign name})

- Budget change: {+£X/day, +10%, "Hold daily budget, do not pause", "Duplicate into dedicated ad set"} — never vague.
- Why: {Sentence 1: metric strength. Sentence 2: scale headroom + hedge or second-best creative if the winner saturates this week.}

2. {as above}

## Anomaly Alert

{One paragraph of 1-3 sentences naming THE most material anomaly — pixel match-rate, MOF dead-cohort spend, learning-phase stuck, single-creative dominance > 40%, validation_deltas mismatch, no-show rate climbing. If material anomalies stack, name the one Mahmoud must act on today; the others sit in the v1 brief.}

## Today's Priority

{One paragraph (1-3 sentences). The single thing that compounds if not closed today. Often a carry-forward. Sometimes a pain-coverage gap ("the BOF pool has zero Bottleneck Identity creatives, brief one today using the verbatim hooks in `docs/new-ip/10`"). Sometimes an outcome-logging gap that unlocks the real ROAS read. Sometimes a pixel-fix open loop. Always one thing, named in the Reason column of the live dashboard if Antonio's pipeline supports it.}
```

### Hard formatting rules

- **Kicker** (top, plain text): `The Coach Consultant · Daily Action Plan`
- **Date** is `# H1` (e.g. `# 07 May 2026`). No day-of-week prefix.
- **Subtitle** (one sentence under the date, normal paragraph) — describes today's account state in plain language.
- **Snapshot table** (3 cells: Today's Spend, Calls, ROAS) — quick read for anyone who only opens the Doc for 10 seconds.
- **Section headings** are `## H2` exactly: `Yesterday's Number`, `Kill Today`, `Scale Today`, `Anomaly Alert`, `Today's Priority`. No alternative wording.
- **Yesterday's Number metrics** → bullet list (`- `).
- **Status: ...** sits below the bullet list as a normal paragraph (NOT a bullet).
- **Kill Today / Scale Today items** are numbered (`1. `, `2. `) at top level, followed by Reason / Why / Budget change / Daily saving as bullets (`- `) underneath.
- **Em-dashes (—) are allowed in this skill output** (Ben uses them in his reference doc). Use them where Ben would: between a creative name and a qualifier (`Reel NEW - 100k staff wages — soften hook`), or as a clause break inside subtitle / Anomaly Alert / Today's Priority paragraphs. Do not use em-dashes inside the bullet-list lines.
- **Total length target: 1-2 pages of styled Google Doc** (roughly 50-90 lines of markdown). Mahmoud is fine with two pages so long as every Kill / Scale Reason / Why passes the three-sub-question depth test.

## Visual treatment (Antonio's GWS CLI guide style)

The Google Doc should *feel* like Antonio's 7 May Internal Setup Guide: confident, calm, slightly editorial. Concrete instructions for the `md-to-gdocs` converter:

- **Kicker line** sits above the H1 in a smaller weight; the converter renders it as a normal paragraph in slightly smaller / muted styling. If the converter doesn't support that natively, ship it as a normal paragraph in the doc and let the caller restyle once. Document the post-render styling in `outputs/STYLE.md` so future runs match.
- **H1 (date)** uses the converter's default Heading 1 style. Don't override.
- **Subtitle** sits on its own paragraph between the H1 and the snapshot table. No styling overrides — the converter's normal paragraph rendering is fine; the *length* (one sentence) is what gives it the editorial feel.
- **Snapshot table** is a 3-column markdown table. The converter supports tables natively; the styling will look clean enough as a basic 1-row data table.
- **Section headings** (Yesterday's Number, Kill Today, Scale Today, Anomaly Alert, Today's Priority) use H2. The converter's H2 style is the magazine-style black serif Antonio used.
- **Generous spacing.** Always leave a blank line between the kicker / H1 / subtitle / table block. Always leave a blank line between bullet groups. Never let two bullets from different items abut.

The aim isn't pixel-perfect Antonio replication on day one — the converter has limits — but to make the Doc *feel* like a respected internal document. Mahmoud should want to open it.

## Tone & output rules (binding, see `1-meta-ads/CLAUDE.md` §6)

**Hard nevers:**
- Kill verdicts on `status=PAUSED` ad sets.
- "Simplify the form" / "reduce LP friction".
- Treat Meta pixel `lead` events as booked calls.
- Team-member names (Mahmoud, Ben, Rob, Jay, Antonio) in free-text.
- Internal snake_case in prose.
- En-dashes (–) anywhere. (Em-dash exception below.)
- Pad numbers to look precise on directional data.
- Paraphrase signup names from email handles (use literal `name` field).
- Word "baseline" for the 8% form-submit threshold.
- Invent pain-angle mappings when the creative content isn't visible. If unsure, label "identity callout (pain unspecified)" and ask for confirmation in Today's Priority.
- Equate `paid_pipeline_breakdown_source == "ghl"` (use `startswith` instead).
- Flag a `paid_calls_booked_28d` drop as a campaign collapse on the day the post-7-May cron lands. The drop is a counting recalibration, not a performance problem.

**Em-dash exception (this skill only):** Ben's 5 May reference doc uses em-dashes (—) as clause breaks. This skill mirrors Ben's structure exactly, so em-dashes are permitted in subtitle, qualifier-after-creative-name, Anomaly Alert and Today's Priority. Not inside bullet lines.

**Hard alwayses:**
- British English. £ for money. "Optimise", "behaviour", "organisation".
- Stage-aware verdicts (TOF / MOF / WEBINAR / BOF).
- Per-stage reasoning when relevant.
- Pixel staleness gate (read `intelligence._metadata.meta_ads_staleness_warning`).
- Pain-angle context cited in at least one Kill or Scale Reason / Why line.
- Three-sub-question depth test on every Kill / Scale Reason or Why (metric, strategic context, implicit hypothesis if Mahmoud disagrees).
- Schema resilience: `.startswith("ghl")` for `paid_pipeline_breakdown_source`; tolerate missing / present `validation_deltas`; surface but never panic on `paid_calls_booked_28d` recalibration.

## Google Doc writing

The flow is `markdown → .docx → upload → copy as Google Doc → cleanup`. Tested 7 May 2026.

```bash
DATE=$(date +%Y-%m-%d)
TITLE="Meta Ads Daily Action Plan (NEW format) — $DATE"
FOLDER_ID=$(cat 1-meta-ads/meta-ads-daily-action-plan-new/outputs/folder_id.txt)

# 1. Markdown → .docx
python3 jay-skills/md-to-gdocs/convert.py \
    "1-meta-ads/meta-ads-daily-action-plan-new/outputs/${DATE}.md" \
    "$TITLE"
mv "$TITLE" "${TITLE}.docx"

# 2. Upload .docx
DOCX_ID=$(gws drive files create \
    --upload "${TITLE}.docx" \
    --params "{\"name\":\"$TITLE\",\"parents\":[\"$FOLDER_ID\"]}" \
    --format json \
    | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

# 3. Copy with mimeType conversion → native Google Doc
GDOC_ID=$(gws drive files copy \
    --params "{\"fileId\":\"$DOCX_ID\"}" \
    --json "{\"name\":\"$TITLE\",\"mimeType\":\"application/vnd.google-apps.document\",\"parents\":[\"$FOLDER_ID\"]}" \
    --format json \
    | grep -o '"id": "[^"]*"' | head -1 | cut -d'"' -f4)

echo "Google Doc: https://docs.google.com/document/d/${GDOC_ID}/edit"

# 4. Cleanup
gws drive files delete --params "{\"fileId\":\"$DOCX_ID\"}"
rm -f "${TITLE}.docx" download.html
```

**Folder ID:** stored in `outputs/folder_id.txt`. For TCC the value is `1pduNpfkMt3HQRs2t0z5e3L3_R5prdwUs` ("Daily Action Plans" — same folder the v1 skill uses).

**Why three steps and not one upload-with-conversion:** `gws drive files create` does NOT honour `mimeType=google-apps.document` on upload. Conversion only happens via `files.copy` with a target mimeType.

## Local output (always)

Mirror to `outputs/{YYYY-MM-DD}.md` for:
- Yesterday's plan readability for tomorrow's carry-forward.
- Git diffs to show how the brief evolves.
- Drive write fallback.

## When to invoke

- Manually today: `Use the meta-ads-daily-action-plan-new skill to generate today's brief for {YYYY-MM-DD}.`
- Run alongside v1 for at least 3 days. Ship both Docs to the team. Get format feedback before flipping the cron.
- Once validated, replace `meta-ads-daily-action-plan` cron target with this skill, archive the v1 folder.

## Pre-ship checklist

Before writing any Doc to Drive, verify:

- Bookings come from Calendly, revenue from `sheet_revenue.json` email-matched, Meta pixel only for ad-set health.
- Every Kill / Scale verdict declares its stage (BOF / MOF / WEBINAR / TOF).
- Per-stage metrics applied. No BOF thresholds on TOF / MOF / WEBINAR.
- Kill verdicts exclude `PAUSED` ad sets.
- No team names, no snake_case, no "simplify form", no "kill immediately", no en-dashes.
- Every Kill / Scale Reason / Why passes the three-sub-question depth test (metric, strategic context, implicit hypothesis if Mahmoud disagrees).
- Pain-angle context cited in at least one Kill or Scale line.
- Today's Priority is one paragraph, one thing.
- `paid_pipeline_breakdown_source` read with `.startswith("ghl")`, not `==`.
- `validation_deltas` read if present, tolerated if absent.
- `paid_calls_booked_28d` drop versus yesterday is contextualised as a recalibration, not a collapse, on the cron-refresh day.
- Webinar ad sets sit in their own stage bucket, not lumped into MOF.

If any check fails, fix before shipping.

## Reference output

`outputs/2026-05-07.md` is the canonical reference (written 7 May 2026). Match that file's structure exactly. Live Google Doc: https://docs.google.com/document/d/1VU5ZQDy-0Vsv6ezBsmPqqe8InIXe-_7sBcfXGTKWoT0/edit

## Version

**v1.1 (2026-05-08)** — incorporates Antonio's 7 May feedback.

- Schema resilience for the 7 May dashboard refactor: `paid_pipeline_breakdown_source` startswith check, `validation_deltas` field, `paid_calls_booked_28d` recalibration tolerance, Webinar as a distinct stage.
- Reasoning depth requirement: every Kill / Scale Reason / Why must pass the three-sub-question depth test (metric, strategic context, implicit hypothesis if disagree). Mahmoud's 5 May call feedback baked in.
- Length cap relaxed: 1-2 pages, depth over brevity.
- Visual treatment specified: kicker + H1 + subtitle + 3-cell snapshot table + H2 sections, mirroring Antonio's 7 May Internal Setup Guide layout.
- Strategist layer: Pass A (vertical-scaling pain coverage), Pass B (scale-the-winner discipline), Pass C (close-rate ladder awareness). The AI should think like a sharp media buyer, not a threshold reader.

**v1.0 (2026-05-07)** — initial new-format skill. One-page output mimicking Ben's hand-written 5 May example. Inherits all v1 framework rules from `meta-ads-daily-action-plan/skill.md` and `1-meta-ads/CLAUDE.md`. Adds vertical-scaling pain-angle layer.
