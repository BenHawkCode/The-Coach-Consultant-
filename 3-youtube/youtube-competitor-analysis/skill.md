---
name: youtube-competitor-analysis
description: Weekly YouTube competitor analysis for TCC. Scrapes 10 selected channels from the master 31-competitor list (Hormozi, Dan Martell, Iman Gadzhi, Russell Brunson, Sam Ovens, Steven Bartlett, Chris Williamson, Ali Abdaal, GaryVee, James Sinclair), runs the top 5 videos per channel through Gemini multimodal for hook / framework / CTA / pain-angle analysis, writes a one-page magazine-style Google Doc into the Drive folder, and emits a `youtube_competitors.json` artefact for the dashboard widget. Mirrors `meta-ads-daily-action-plan-new` visual treatment exactly: kicker, serif H1, teal subtitle, 3-cell snapshot table, serif H2 sections, red-bordered insight boxes, no em-dashes.
---

# YouTube Competitor Analysis

Weekly intelligence brief on what 10 selected YouTube competitors are doing with hooks, frameworks, CTAs, and which pain angles they hit. Output is the same magazine-style Google Doc treatment as `meta-ads-daily-action-plan-new`. Sister analytics skill alongside `ig-competitor-analysis` — same competitor universe, different platform.

## Why this exists

Ben asked for a weekly competitor view on the dashboard. The IG competitor analysis already covers Instagram. YouTube is the second-highest signal source for long-form hook patterns and offer-framing language. Selected 10 channels from the master 31-profile list (see `competitor-list.md`) where the content fit and ICP overlap is highest for Sam (35-50, £100K-£500K, open business owner).

The skill answers three questions every Monday:

1. **What are the strongest hooks competitors used in the last 7 days?** Lifted verbatim, mapped to new IP pain anchors.
2. **What frameworks or offer-structures keep showing up?** Pattern-spotted across the top 5 per channel.
3. **Where is the gap?** Pain angles or formats competitors are not covering that TCC could own.

## Inputs

| File / source | Purpose |
|---|---|
| `competitor-list.md` | 10 selected channels (handles, why study) |
| YouTube Data API or Apify (scraper layer) | Pulls per-channel video metadata (title, views, likes, comments, duration, publish date, thumbnail, description, captions if available) |
| Gemini 2.x multimodal (`GEMINI_API_KEY` in root `.env`) | Per-video strategic analysis on the top 5 by engagement |
| `docs/new-ip/06-pain-isolation.md` | Six pain layers — used to tag every hook and surface coverage gaps |
| `docs/new-ip/10-pain-point-articulation.md` | Verbatim hook bank for "gap" recommendations |
| Last week's `outputs/{YYYY-MM-DD}.md` | For week-over-week deltas on hook patterns and framework adoption |

## What the skill does

When invoked (manually `Use the youtube-competitor-analysis skill to generate this week's brief` or via the weekly cron):

1. **Resolve channel handles** to channel IDs once per quarter (cache to `data/channel_ids.json`). Skip any channel that doesn't resolve.
2. **Pull last 30 days of long-form videos plus last 30 Shorts per channel.** Save raw JSON to `data/{handle}-raw-{YYYY-MM-DD}.json`. Apify path is the fallback; the YouTube Data API quota is cheaper for metadata-only.
3. **Rank by engagement** — `views * like_rate` (likes / views), top 5 per channel. Total = 50 videos for deep analysis.
4. **For each top-5 video, run Gemini multimodal pass:**
   - Input: title + description + first 60 seconds of transcript + thumbnail image
   - Output (structured JSON): hook verbatim, hook type (statement / question / statistic / story / pattern interrupt), framework spotted (if any), CTA verbatim, pain anchor tag (one of the six new IP pain layers + "no pain anchor"), production format (long-form / Short / podcast clip), one-sentence summary
5. **Aggregate** — count hook types, count pain anchors, count framework appearances, surface week-over-week deltas vs last week's brief.
6. **Generate the Google Doc** using the HTML inline-style render path (binding spec lives below in §Google Doc writing).
7. **Emit `youtube_competitors.json`** to `data/` with the aggregated insights for the dashboard widget. Antonio's pipeline will read it.

## Reasoning framework (mirrors `meta-ads-daily-action-plan-new`)

Three reasoning passes on top of the raw metrics:

### Pass A — Pain coverage across competitors

Tag every analysed hook against one of the six new IP pain layers. Across the 50-video pool, count which layers competitors are over-indexing on and which are missing. Surface gap analysis explicitly: "Eight of ten competitors led with AI Era Anxiety hooks this week. None used Bottleneck Identity. Brief one for TCC."

### Pass B — Format and framework patterns

Spot which production formats are converting (long-form essay-style versus Shorts versus podcast clip uploads). Track which frameworks keep recurring (PAS, 3-act story, problem-agitate-reveal, framework-named-after-author). Recommend the one to test for TCC's next batch.

### Pass C — Verbatim hook bank

Lift the top 10 hooks verbatim across all channels. These become raw material for the TCC content team. Mark each with its source competitor and the pain anchor it hit.

## Output structure (binding)

ONE Google Doc per week. Filename: `YouTube Competitor Analysis — Week of {YYYY-MM-DD}`. Local mirror at `outputs/{YYYY-MM-DD}.md` for git diff and next-week carry-forward.

### Markdown template

```markdown
The Coach Consultant · YouTube Competitor Analysis

# Week of {DD Month YYYY}

{One-sentence subtitle summarising the strongest pattern this week. Example: "Hormozi and Dan Martell both led with Bottleneck Identity hooks. Eight of ten channels skipped AI Era Anxiety entirely."}

| Channels Tracked | Videos Analysed | Top Hook Type |
|---|---|---|
| 10 | 50 (top 5 per channel) | {Statement / Question / Statistic} |

## This Week's Number

- Total videos pulled: {N} across {M} channels (some channels under cap when output volume was low this week)
- Videos analysed in depth: 50 (top 5 by engagement per channel)
- Hook types observed: {Statement N, Question M, Statistic K, Story L, Pattern interrupt J}
- Pain anchors hit: {Guesswork Tax N, Bottleneck Identity M, AI Era Anxiety K, Trust Trauma L, Plate Anxiety J, Partner Pressure I, No anchor R}
- Production format mix: long-form {X%}, Shorts {Y%}, podcast clips {Z%}

Status: {one-sentence read of the week, ties to whether the competitor pool is shifting toward or away from TCC's positioning angle. Example: "Watch. Pain coverage skews heavily toward AI Era Anxiety this week (six of ten channels), giving TCC a clean lane on Bottleneck Identity if we ship two pieces against that angle by Friday."}

## Top Hooks This Week (verbatim swipe file)

1. "{verbatim hook}" — {Channel} ({pain anchor})
2. "{verbatim hook}" — {Channel} ({pain anchor})
3. ... (10 total)

## Framework Patterns

{Two or three paragraphs. Which frameworks recurred. Which competitor used what. Whether TCC's 4-Step Programme has any positional advantage relative to what competitors are running this week.}

## Pain Coverage Gaps

{Red-bordered box, magazine-style alert.}

{Lead in red: "Missing this week: Bottleneck Identity, Trust Trauma."} {Body: which channels skipped these, what hooks TCC could ship to own the lane this week. Lift verbatim from docs/new-ip/10 where the gap maps to an existing pain quote.}

## This Week's Priority

{One paragraph in a teal-bordered box. The single move TCC should make this week off the back of the analysis. Specific. Includes the pain anchor, the hook approach, the video format to test, and which competitor's structure to study most closely for the next 7 days.}
```

### Hard formatting rules

Identical to `meta-ads-daily-action-plan-new` §Visual treatment. All inline styling lives in the HTML render step. Same teal / dark / red palette. Same kicker / H1 / subtitle / snapshot table / H2 / status box / anomaly red box / priority teal box structure.

**No em-dashes (—) or en-dashes (–) anywhere.** Hard rule.

## Visual treatment

Mirrors `1-meta-ads/meta-ads-daily-action-plan-new/skill.md` §Visual treatment specification exactly. Same colour palette, same fonts, same structural shapes. Reference Doc to match: https://docs.google.com/document/d/1bNNS9JbdagQE0ZDTDDfcKhSKFHnxxWqbArafmf2Oe20/edit

Kicker reads "The Coach Consultant · YouTube Competitor Analysis" instead of "Daily Action Plan". Everything else identical.

## Google Doc writing

Same flow as `meta-ads-daily-action-plan-new`. HTML with inline styles, uploaded via gws, mimeType-converted to a native Google Doc. Reference implementation in `scripts/render_gdoc.py` (to be built; the meta-ads version's `style-tests/test3_html_convert.py` is the donor template).

```bash
DATE=$(date +%Y-%m-%d)
TITLE="YouTube Competitor Analysis — Week of $DATE"
FOLDER_ID=$(cat 3-youtube/youtube-competitor-analysis/outputs/folder_id.txt)

python3 3-youtube/youtube-competitor-analysis/scripts/render_gdoc.py \
    --input "outputs/${DATE}.md" \
    --title "$TITLE" \
    --folder "$FOLDER_ID"
```

`folder_id.txt` holds the Drive folder ID this skill writes to. First-run: create a "YouTube Competitor Analysis" folder under TCC's automation parent, store its ID here. Same pattern as the meta-ads skills.

## Dashboard hook (built last, per Ben's brief)

After the Google Doc lands, emit `data/youtube_competitors.json` with the aggregated metrics:

```json
{
  "week_of": "2026-05-12",
  "generated_at": "2026-05-12T08:00:00Z",
  "channels_tracked": 10,
  "videos_analysed": 50,
  "hook_type_distribution": { "statement": 18, "question": 12, "statistic": 8, "story": 7, "pattern_interrupt": 5 },
  "pain_coverage": {
    "guesswork_tax": 4,
    "bottleneck_identity": 0,
    "ai_era_anxiety": 28,
    "trust_trauma": 0,
    "plate_anxiety": 3,
    "partner_pressure": 0,
    "no_anchor": 15
  },
  "format_mix": { "long_form": 0.55, "shorts": 0.35, "podcast_clip": 0.10 },
  "top_hooks": [ { "hook": "...", "channel": "@AlexHormozi", "pain": "ai_era_anxiety" }, ... ],
  "priority_move": "Ship two Bottleneck Identity hooks this week",
  "doc_url": "https://docs.google.com/document/d/.../edit"
}
```

Antonio's pipeline reads this from the repo (or we push it to `tcc-dashboard/public/data/` directly, like the IG output). Dashboard widget shape lives in the React layer — that's an Antonio-side build once this JSON is stable.

**Order: ship the Google Doc first, run weekly for two weeks, then wire the JSON to the dashboard.** Ben prioritises Doc visibility over widget completeness for the first cycle.

## Tone & output rules

Inherits from global CLAUDE.md + `1-meta-ads/CLAUDE.md` §6:

**Hard nevers:**
- Em-dashes (—) and en-dashes (–) anywhere.
- Team-member names (Mahmoud, Ben, Rob, Jay, Antonio) in free-text.
- Internal snake_case in prose. Use natural language.
- Paraphrase competitor quotes from their hooks. If we cite the hook, cite it verbatim. If the source is unclear, mark "{paraphrase}" and flag for re-verification.
- Recommend mimicking competitor hook word-for-word. We swipe the structure, not the language. Language comes from `docs/new-ip/10-pain-point-articulation.md` (the TCC-voice version).
- Treat YouTube view count as a quality signal in isolation. Big channels generate big numbers regardless of hook quality. Always pair view count with like-rate (likes / views) and recency.
- Ship a brief that doesn't name at least three verbatim hooks. The swipe file is the table-stakes deliverable.

**Hard alwayses:**
- British English. £ for money. "Optimise", "behaviour", "organisation".
- Pain-anchor tag on every hook in the swipe file.
- One named priority move at the end of the brief.
- Source channel cited next to every verbatim hook.
- Recency note where relevant (a 6-month-old viral video is not the same signal as a 7-day-old one).

## Implementation plan

Build order:

1. **`scripts/resolve_handles.py`** — one-off, takes the 10 handles from `competitor-list.md`, returns channel IDs, writes `data/channel_ids.json`. Quarterly re-run.
2. **`scripts/scrape_channels.py`** — pulls 30 days of videos per channel via YouTube Data API. Apify fallback if quota hits. Writes per-channel raw JSON to `data/`.
3. **`scripts/analyse_top5.py`** — per channel, sorts by `views * like_rate`, takes top 5, calls Gemini multimodal with structured prompt (returns JSON: hook verbatim, hook type, framework, CTA, pain anchor, format, summary). Writes `data/{handle}-analysed-{date}.json`.
4. **`scripts/aggregate.py`** — reads all `*-analysed-*` files, builds the week-of aggregate, writes `data/youtube_competitors.json`.
5. **`scripts/render_md.py`** — generates the markdown brief from the aggregate, writes to `outputs/{YYYY-MM-DD}.md`.
6. **`scripts/render_gdoc.py`** — markdown brief plus aggregate metadata → styled HTML → Drive upload → mimeType convert. Donor: `1-meta-ads/meta-ads-daily-action-plan-new/style-tests/test3_html_convert.py`.
7. **`scripts/run_weekly.sh`** — orchestrator. One shell command to run the full pipeline. Wired to launchd for the weekly cron once the format is validated by Ben.
8. **Dashboard JSON push** (final step, after Ben validates) — write `data/youtube_competitors.json` into `tcc-dashboard/public/data/` so Antonio's React layer can read it.

## Pre-ship checklist

Before writing any Doc to Drive, verify:

- Channel handles resolved. Any that failed are explicitly flagged in the brief, not silently dropped.
- Top 5 per channel selected by `views * like_rate`, not raw views alone.
- 50 videos analysed in total. If fewer, flag the gap in Status.
- Pain anchor tag present on every hook in the verbatim swipe file.
- Gemini outputs structurally validated (each video has hook, hook_type, framework, cta, pain_anchor, format, summary fields). Drop any that fail validation, log to `cron-logs/`.
- Week-over-week delta written explicitly (versus last week's brief) where one exists.
- One priority move named, specific, time-bound to this week.
- No em-dashes. No team names. British English.
- `data/youtube_competitors.json` written and parseable, even if the dashboard widget isn't live yet.

If any check fails, fix before shipping.

## When to invoke

- **Manually:** `Use the youtube-competitor-analysis skill to generate this week's brief for {YYYY-MM-DD}.`
- **Weekly cron:** Monday morning, 07:00 UK time (after IG competitor cron lands the same morning). Wired via `scripts/run_weekly.sh` and a launchd plist following the meta-ads-daily-action-plan-new pattern.
- **First three weeks: parallel-validate output with Ben before flipping to cron.** Ship the Doc manually each Monday, get feedback, refine the Gemini prompt, then go autonomous.

## Version

**v1.0 (2026-05-13)** — initial skill. 10 channels, top 5 per channel through Gemini multimodal, magazine-style Google Doc output mirroring `meta-ads-daily-action-plan-new` visual treatment. Dashboard widget wiring deferred to v1.1 after first two weeks of validation with Ben.
