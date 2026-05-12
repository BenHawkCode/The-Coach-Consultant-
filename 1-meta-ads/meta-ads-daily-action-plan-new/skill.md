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
- Per-stage metrics:
  - **BOF** on cost per real Calendly call (account headline) + `cost_per_booking_pixel_7d` (per ad set).
  - **TOF dual-purpose (updated 2026-05-12, Ben's Monday meeting):** TOF now also produces direct booked calls and revenue, not just followers. Read the three new columns Ben added to the TCC Master Dashboard sheet: Booked calls (TOF), Sales (TOF), TOF ROAS. Judge the long-term audience-build job with cost per follower; judge the direct-response job with the new TOF columns when populated.
  - **MOF** on cost per opt-in / DM conversation.
- BOF kill/scale/watch thresholds anchored on `cost_per_booking_pixel_7d`: ≤ £150 with ≥ 2 bookings = scale, ≤ £200 = healthy, £200-£300 = watch, > £300 sustained = kill candidate.
- **TOF kill/scale rule (dual-purpose):**
  - Cost per follower hitting target AND TOF ROAS positive (sheet) → scale candidate.
  - Cost per follower fine but TOF ROAS negative → do NOT kill on ROAS alone; the follower job may still be feeding BOF audience. Cross-check downstream BOF spend before pulling.
  - Both metrics bad → kill candidate.
- CTR link < 0.8% kill candidate, ≥ 1.5% healthy, ≥ 2.5% scale signal.
- Min 1,000 impressions per ad set for a verdict.
- Never kill in `LEARNING` / `LEARNING_LIMITED`.
- Pixel match-rate edge case: 0 pixel bookings + non-zero applications + non-zero Calendly = ad blocker / cookie loss, NOT a kill.
- ROAS: numerator = sheet revenue email-matched to Calendly paid_ads_28d, denominator = BOF spend only for account-level ROAS. **TOF ROAS is computed separately from the master sheet's TOF columns** and reported alongside, not blended into the BOF ROAS headline.
- Read `intelligence._metadata.meta_ads_staleness_warning`. If `CRITICAL`, abort.

## Strategist layer (this skill's main upgrade)

The v1 skill answered "what does the data say?" This skill must answer "what would a sharp media buyer do, and why?" That requires three new reasoning passes layered on top of the framework.

### Pass A — Vertical-scaling pain coverage

Tag every active creative against one of the six new IP pain layers (Guesswork Tax, Bottleneck Identity, AI Era Anxiety, Trust Trauma, Plate Anxiety, Partner Pressure). When an active creative is an "identity callout" (e.g. "If you're coach WHITE") with no specific pain anchor, label it explicitly and flag that the pool is under-anchored.

Across the active BOF creative pool, count which layers are represented and which are missing. If a hero pain (Guesswork Tax) or close-second pain (Bottleneck Identity) is missing, that surfaces inside Today's Priority as a brief proposal — propose a new creative angle using a verbatim hook from `docs/new-ip/10-pain-point-articulation.md`. Never invent pain language; lift it.

### Pass B — Scale-the-winner discipline

When a creative or ad set sits in the scale band — BOF: `cost_per_booking_pixel_7d ≤ £150` with ≥ 2 bookings; or CTR ≥ 2.5% sustained across ≥ 1,000 impressions; TOF: strongest cost per follower AND positive TOF ROAS on the master sheet's new columns (dual-purpose rule) — the skill should:

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

The skill writes markdown locally (for git diff and tomorrow's carry-forward) AND renders styled HTML that Drive imports as a native Google Doc. See §Google Doc writing for the binding render rules and §Visual treatment for the spec the HTML must satisfy. Markdown is the audit artefact; the Google Doc is the deliverable Mahmoud reads.

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

Status: {Watch / Healthy / Concern} ({one-sentence rationale tying to BOF stage spend, pixel match rate, TOF cost per follower AND TOF ROAS from the master sheet's new columns if applicable, and any 7 May 2026 schema-refactor recalibration note}).

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
- **Em-dashes (—) and en-dashes (–) NEVER.** Hard rule, no exceptions. Use commas, full stops, parentheses, colons. Override of any earlier v1.0/v1.1 "exception" text.
- **Total length target: 1-2 pages of styled Google Doc** (roughly 50-90 lines of markdown). Mahmoud is fine with two pages so long as every Kill / Scale Reason / Why passes the three-sub-question depth test.

## Visual treatment

Rendered to a styled Google Doc via the HTML-inline-style flow in §Google Doc writing. The structural / styling spec for the HTML output is binding and lives in §Google Doc writing → "Visual treatment specification". Read that block as the source of truth for kicker / H1 / subtitle / snapshot table / H2 / status box / anomaly box / priority box.

The Doc should *feel* like Antonio's 7 May Internal Setup Guide: confident, calm, slightly editorial. Mahmoud should want to open it. The reference for "what the right brief looks like" is the live 8 May 2026 brief at https://docs.google.com/document/d/1bNNS9JbdagQE0ZDTDDfcKhSKFHnxxWqbArafmf2Oe20/edit.

## Tone & output rules (binding, see `1-meta-ads/CLAUDE.md` §6)

**Hard nevers:**
- Kill verdicts on `status=PAUSED` ad sets.
- "Simplify the form" / "reduce LP friction".
- Treat Meta pixel `lead` events as booked calls.
- Team-member names (Mahmoud, Ben, Rob, Jay, Antonio) in free-text.
- Internal snake_case in prose.
- Em-dashes (—) AND en-dashes (–) anywhere. NEVER. Use commas, full stops, parentheses, colons.
- Pad numbers to look precise on directional data.
- Paraphrase signup names from email handles (use literal `name` field).
- Word "baseline" for the 8% form-submit threshold.
- Invent pain-angle mappings when the creative content isn't visible. If unsure, label "identity callout (pain unspecified)" and ask for confirmation in Today's Priority.
- Equate `paid_pipeline_breakdown_source == "ghl"` (use `startswith` instead).
- Flag a `paid_calls_booked_28d` drop as a campaign collapse on the day the post-7-May cron lands. The drop is a counting recalibration, not a performance problem.

**Em-dash rule (revised v1.2):** NEVER use em-dash (—) or en-dash (–) in this skill output. Override of any v1.1 "exception" — the production format Antonio approved on 8 May has zero em-dashes. Substitute commas, full stops, parentheses, or colons.

**Hard alwayses:**
- British English. £ for money. "Optimise", "behaviour", "organisation".
- Stage-aware verdicts (TOF / MOF / WEBINAR / BOF).
- Per-stage reasoning when relevant.
- Pixel staleness gate (read `intelligence._metadata.meta_ads_staleness_warning`).
- Pain-angle context cited in at least one Kill or Scale Reason / Why line.
- Three-sub-question depth test on every Kill / Scale Reason or Why (metric, strategic context, implicit hypothesis if Mahmoud disagrees).
- Schema resilience: `.startswith("ghl")` for `paid_pipeline_breakdown_source`; tolerate missing / present `validation_deltas`; surface but never panic on `paid_calls_booked_28d` recalibration.

## Google Doc writing

The flow is `build HTML with inline styles → upload via gws → convert to Google Doc via mimeType=google-apps.document`. Reference implementation lives in `style-tests/test3_html_convert.py` (winner of the 8 May 2026 style-test bake-off).

**Why HTML, not markdown:** The `md-to-gdocs` converter strips most styling — only basic H1/H2/bullet shapes survive. Antonio's 8 May reference (`The Coach Consultant · Internal Setup Guide`) is magazine-style: teal kicker, serif H1, teal subtitle, 3-cell snapshot table, red-bordered alert boxes, teal highlights. None of that survives md→docx→Doc conversion. HTML with **inline styles** does survive Google Docs' HTML import, so that's the path.

**What survives Google Docs' HTML import:**

- Inline `style="color:...; background-color:...; font-family:...; font-size:...pt; font-weight:..."`
- `<h1>` and `<h2>` tags (map to Heading 1/2)
- `<table>` with inline `border` and `padding` on `<td>`
- `<ul>` / `<li>` bullet lists
- `<strong>`, `<em>`, `<u>`, `<code>` inline tags

**What does NOT survive:**

- External `<style>` blocks (use inline only)
- `<div>` containers — converter unwraps them, so use `<p>` with full inline styling on the paragraph itself
- CSS classes (use inline `style="..."` per element)
- `border-radius`, `box-shadow`, complex flexbox layouts
- Custom fonts outside Google Docs' built-in library — Playfair Display, Georgia, Helvetica Neue, Inter, Roboto all work; obscure fonts do not

### Implementation

The skill produces local markdown at `outputs/{YYYY-MM-DD}.md` (for git diffs and tomorrow's carry-forward). The Google Doc gets built by a separate render step that consumes the same data and emits styled HTML. Reference: `style-tests/test3_html_convert.py`.

Pseudocode for the render step:

```python
DATE = "2026-05-08"
TITLE = f"Meta Ads Daily Action Plan — {DATE}"
FOLDER_ID = open("outputs/folder_id.txt").read().strip()

TEAL = "#5C8B7F"
DARK = "#0a0a0a"
TEAL_LIGHT_BG = "#e8f0ed"
RED = "#d63b2f"
RED_LIGHT_BG = "#fff0ee"

# Build HTML with inline styles per element.
# Kicker, H1, subtitle, snapshot table, H2 sections, status/priority highlight
# boxes (teal left border + light teal bg), anomaly red-border box.
html = build_html_from_brief_data(...)

# Write to a CWD-relative file (gws --upload rejects /tmp or absolute paths)
with open("daily_action_plan.html", "w") as f:
    f.write(html)

# Upload with target mimeType — Drive converts HTML to native Google Doc on import
upload = gws_drive_files_create(
    upload="daily_action_plan.html",
    params={
        "name": TITLE,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [FOLDER_ID],
    },
)

# If upload kept mimeType=text/html (some Drive versions do), do a copy with conversion
if upload["mimeType"] != "application/vnd.google-apps.document":
    converted = gws_drive_files_copy(
        params={"fileId": upload["id"]},
        json={
            "name": TITLE,
            "mimeType": "application/vnd.google-apps.document",
            "parents": [FOLDER_ID],
        },
    )
    gws_drive_files_delete(params={"fileId": upload["id"]})
    doc_id = converted["id"]
else:
    doc_id = upload["id"]

os.unlink("daily_action_plan.html")
print(f"https://docs.google.com/document/d/{doc_id}/edit")
```

**Folder ID:** stored in `outputs/folder_id.txt`. For TCC the value is `1pduNpfkMt3HQRs2t0z5e3L3_R5prdwUs` ("Daily Action Plans" — same folder the v1 skill uses).

### Visual treatment specification (binding)

Render the HTML to match these conventions exactly. Reference: 8 May 2026 brief at https://docs.google.com/document/d/1bNNS9JbdagQE0ZDTDDfcKhSKFHnxxWqbArafmf2Oe20/edit

- **Kicker** (top of doc): `<p>` inline style `color:#5C8B7F; font-size:10pt; font-weight:700; letter-spacing:0.5px;` — text `THE COACH CONSULTANT · DAILY ACTION PLAN`.
- **H1 date**: `<h1>` inline `font-family:'Playfair Display',Georgia,serif; font-size:36pt; font-weight:800; color:#0a0a0a;`.
- **Subtitle**: `<p>` inline `color:#5C8B7F; font-size:14pt;` — one sentence summarising today's account state.
- **Snapshot table**: 3-cell `<table>` with `border-collapse:collapse; border:1px solid #5C8B7F;`. Each `<td>` has `padding:14px 18px; border:1px solid #5C8B7F;`. Cell content: label (`<p style="font-size:9pt; font-weight:700; letter-spacing:0.5px;">`) then value (`<p style="font-size:13pt;">`).
- **H2 section headings**: `<h2>` inline `font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:#0a0a0a;`.
- **Status block (Yesterday's Number)**: `<p>` inline `padding:12px 16px; background-color:#e8f0ed; border-left:3px solid #5C8B7F;`. Lead in `<strong>Status: Watch.</strong>` then body. Split into 2-3 line paragraphs, each in its own styled `<p>`.
- **Kill / Scale items**: numbered `<p>` lead with `font-size:13pt; font-weight:700;`. Below, each Reason / Why / Budget change / Daily saving as separate `<p>` with `<strong style="color:#5C8B7F;">Reason.</strong>` lead-in.
- **Anomaly Alert**: red-bordered box, each anomaly bullet as its own paragraph. Use `<p>` (NOT `<div>`) with inline `padding:16px 20px; background-color:#fff0ee; border:2px solid #d63b2f;`. Lead-in `<strong style="color:#d63b2f;">Pixel match-rate gap, day 7.</strong>` then body. **Important:** because `<div>` gets unwrapped by Drive's HTML import, the red-border style must sit on the `<p>` itself or on each paragraph individually. If multiple paragraphs need to share the box, repeat the border style per paragraph or accept that the box visually breaks between paragraphs.
- **Today's Priority**: teal-bordered box like Status, on separate `<p>` paragraphs. Lead-in `<strong>Fix the booking pixel today.</strong>`.
- **No em-dashes (—) anywhere.** Use commas, full stops, parentheses, colons. Hard global rule for this skill.
- **Paragraph length:** 2-3 lines max per `<p>`. If longer, split into a new paragraph under the same logical block. If even longer or genuinely list-like, use `<ul>` / `<li>` instead of prose.

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

**v1.3 (2026-05-12)** — TOF dual-purpose rule per Ben's Monday meeting roundup.

- TOF stage now scored on two axes, not one. Long-term audience build via cost per follower (unchanged) PLUS direct-response via three new master sheet columns: Booked calls (TOF), Sales (TOF), TOF ROAS.
- TOF scale band requires BOTH cost per follower healthy AND TOF ROAS positive. Scale call cannot rely on one axis alone.
- TOF kill rule explicit: don't kill on negative TOF ROAS alone if the follower job is still feeding downstream BOF audience. Both metrics need to be bad for a kill verdict.
- TOF ROAS reported separately from BOF ROAS. The two are never blended.
- Account-level ROAS headline remains BOF spend / paid revenue (unchanged).
- Framework parent (`1-meta-ads/CLAUDE.md` §5 Step 2) updated to match.

**v1.2 (2026-05-08, late)** — HTML-inline-style render path replaces md-to-gdocs.

- Google Doc render switched from `markdown → docx → upload → copy with mimeType` (md-to-gdocs) to `HTML with inline styles → upload via gws --upload → mimeType conversion`. The md path lost too much styling for Antonio's magazine-style brief.
- Visual treatment spec (kicker / H1 / subtitle / snapshot table / H2 / status box / anomaly red-border box / priority teal-border box) is now binding. Reference implementation: `style-tests/test3_html_convert.py`.
- "What survives Google Docs' HTML import" rules documented so future variants don't accidentally fall back to broken patterns (external `<style>` blocks, `<div>` wrappers that get unwrapped, custom fonts outside Google's library).
- Em-dash rule made absolute: NEVER. Replaced the v1.1 "em-dash exception". Use commas, full stops, parentheses, colons.

**v1.1 (2026-05-08)** — incorporates Antonio's 7 May feedback.

- Schema resilience for the 7 May dashboard refactor: `paid_pipeline_breakdown_source` startswith check, `validation_deltas` field, `paid_calls_booked_28d` recalibration tolerance, Webinar as a distinct stage.
- Reasoning depth requirement: every Kill / Scale Reason / Why must pass the three-sub-question depth test (metric, strategic context, implicit hypothesis if disagree). Mahmoud's 5 May call feedback baked in.
- Length cap relaxed: 1-2 pages, depth over brevity.
- Visual treatment specified: kicker + H1 + subtitle + 3-cell snapshot table + H2 sections, mirroring Antonio's 7 May Internal Setup Guide layout.
- Strategist layer: Pass A (vertical-scaling pain coverage), Pass B (scale-the-winner discipline), Pass C (close-rate ladder awareness). The AI should think like a sharp media buyer, not a threshold reader.

**v1.0 (2026-05-07)** — initial new-format skill. One-page output mimicking Ben's hand-written 5 May example. Inherits all v1 framework rules from `meta-ads-daily-action-plan/skill.md` and `1-meta-ads/CLAUDE.md`. Adds vertical-scaling pain-angle layer.
