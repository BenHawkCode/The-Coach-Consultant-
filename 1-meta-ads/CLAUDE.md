# TCC Meta Ads — Build Guide for Claude Code

This document is the framework reference for anyone (or any Claude Code) building analysis, automations, or reports on top of TCC's Meta Ads data.

Applies specifically to TCC Meta Ads work. Inherits all rules from parent CLAUDE.md layers (global voice, format, git discipline). Does not repeat them.

---

## 1. The map — what exists, who reads what

### Two repos in the TCC ecosystem

- **`antonio-gasso/tcc-dashboard`** (this repo): pipeline + dashboard + canonical JSONs + SCHEMA.md
  - Collects Meta / Calendly / Sheet / GHL / GA4 / YouTube / LinkedIn data once a week
  - Runs Opus analysis (strategic brain + 6 channel specialists)
  - Outputs to `dashboard/public/data/*.json`
  - Serves dashboard at tcc-dashboard.netlify.app
- **`BenHawkCode/The-Coach-Consultant-`** (sister repo): skills + brand voice + content generation
  - Jay's skills for each channel (1-meta-ads, 2-instagram, 3-youtube, 4-emails, 5-linkedin, 6-website-seo)
  - Reads from this repo's JSONs OR hits source APIs directly
  - Most skills produce markdown / HTML reports

### Weekly data flow

```
Monday 06:00 UTC cron →  collectors fetch (Meta API, Calendly API, Sheet, GHL, GA4, YouTube, LinkedIn) →
  generate_intelligence.py runs (Opus Layer 1 strategy + Layer 2 × 6 specialists) →
  writes JSONs to public/data/ →
  commits + pushes →
  Netlify redeploy (manual) →
  dashboard live + Jay's skills read the fresh data
```

### Audience map

- **Ben H** (founder): weekly strategic intelligence, ROAS widget, creative direction. Reads dashboard + weekly brief from Jay's `meta-ads-weekly-intelligence` skill.
- **Mahmoud** (media buyer): daily operational review, ad set health, kill / scale / watch, anomalies. Reads Jay's `meta-ads-daily-review` skill output.
- **Rob** (revenue lead): updates the client tracker sheet with amounts post-signup. The sheet is the ground truth for paid revenue.
- **Jay** (skills builder): maintains all 6 channel skills in the sister repo.

### Channels at a glance (Meta Ads deep below, others pointers)

| Channel | Skill location | JSON source |
|---|---|---|
| Meta Ads | `1-meta-ads/meta-ads-daily-review/`, `meta-ads-weekly-intelligence/` | `meta_ads_campaigns.json` + `calendly_bookings.json` + `sheet_revenue.json` |
| Instagram | `2-instagram/` | `ig_own_data.json`, `x30_profiles.json` |
| YouTube | `3-youtube/` | `youtube_data.json`, `youtube_transcriptions.json` |
| Email | `4-emails/` | `ghl_email_data.json`, `competitor_newsletters.json` |
| LinkedIn | `5-linkedin/` | `competitor_linkedin.json` |
| Website / SEO | `6-website-seo/` | `ga4_data.json`, `ghl_data.json` |

If the task is non-Meta-Ads, the corresponding Jay skill folder is the reference implementation. Do not rebuild analysis from scratch. Adapt the skill output, or ask Ben before designing a new analysis layer for that channel.

---

## 2. Before you build — discovery checklist

Before writing any code or generating any output for TCC Meta Ads, answer these five questions.

### 1. Does a Jay skill already do this?

Two Meta Ads skills exist at `BenHawkCode/The-Coach-Consultant-/1-meta-ads/`:

- **`meta-ads-daily-review`** — Mahmoud's daily operational review. Per-campaign, per-ad-set, per-creative breakdown. Kill / scale / watch verdicts. Quality flags. Anomalies. Top priorities. Pulls Meta API + Calendly live. Already per-stage aware. Already uses Calendly as ground truth for bookings. Output: markdown per campaign.
- **`meta-ads-weekly-intelligence`** — Ben H's weekly strategic brief. Reads `intelligence.json` (pre-analyzed by Opus). Outputs markdown + auto-generated HTML dashboard.

If the task resembles either, use the skill as the reference implementation. Adapt output format, reuse the analysis engine. Do not rewrite the analysis logic in your own code.

### 2. What data does it need? Is it already in the JSONs?

Before fetching anything new, check which of these JSONs already has what you need:

- `dashboard/public/data/calendly_bookings.json` — real booked calls, by channel (paid / organic / email / etc.) for 7d and 28d windows
- `dashboard/public/data/sheet_revenue.json` — new client signups this week with amounts (ground truth for revenue)
- `dashboard/public/data/meta_ads_campaigns.json` — ad-set level Meta data (spend, CTR, CPC, form submits, quality rankings) for 7d and 28d
- `dashboard/public/data/intelligence.json` — Opus-analyzed output for all 6 channels including Meta Ads `roas_snapshot`, verdicts, priorities, anomalies
- `dashboard/public/data/ghl_data.json` — GHL pipeline + contacts (use with the caveat in §4)

Fresh data refreshes weekly (Monday 06:00 UTC cron). If you need live data, Jay's daily-review skill calls Meta + Calendly APIs directly.

### 3. What funnel stage does it touch?

Every Meta campaign classifies as TOF, MOF, or BOF based on its objective (see §5). The metric that matters depends on the stage. The most common mistake is applying BOF metrics to TOF campaigns. Always classify first.

### 4. Who consumes the output?

- Ben H → strategic summary, creative direction, ROAS read, scale decisions. Terse, actionable, no jargon.
- Mahmoud → per-campaign operational details, ad-set-level verdicts, creative-level kill / scale. Assumes domain knowledge.
- Rob → revenue-side cross-checks.
- Jay → may consume as reference for future skills.

Format should match the audience.

### 5. What freshness is required?

- **Live** (seconds to minutes old) — run collectors or hit APIs directly. Cost: API calls, time, rate limits.
- **Weekly fresh** (up to 7 days old) — read JSONs in `public/data/`. Zero cost, zero latency, guaranteed availability.
- **On-demand refresh of just one source** — Jay's daily-review has an on-demand Calendly fetch pattern (tries live, falls back to JSON snapshot). Follow that pattern if you need a specific collector fresh.

Default to JSONs unless the task genuinely requires live data.

---

## 3. When to ask Ben vs decide yourself

### Ask Ben when

- **Scope is ambiguous**. "Build me a dashboard" is not enough. Dashboard of what? For whom? With which metrics?
- **New data source is needed**. If what you need isn't in the JSONs and isn't a simple API extension, ask before building a collector. Data source additions affect the whole ecosystem.
- **New campaign type appears**. If a Meta campaign has an objective that doesn't cleanly map to TOF / MOF / BOF (see §5), check with Ben rather than guess.
- **Output goes to a new audience**. If it's not Ben H or Mahmoud, confirm what they expect.
- **Output format changes something he ships to clients**. Client deliverables have branding rules (see global CLAUDE.md). Confirm before deviating.

### Decide yourself on

- Default output formats when not specified (markdown for internal, Google Doc for Drive per global rules).
- Which existing skill or data source to adapt when the task maps cleanly to an existing pattern.
- Framework application. The rules in §5 and §6 are non-negotiable. Apply them without asking.
- Edge cases within the framework. A TOF campaign with no recent data gets "insufficient signal", not a guess.

### Never do silently

- Skip an existing Jay skill that already solves the task.
- Invent new metrics or thresholds not grounded in this doc or the source code.
- Use Meta pixel `lead` events as a booked-call count (see §4).
- Drop the data caveat from any output that quotes numbers.

---

## 4. Data source contract — what to trust for what

### Calendly = bookings (real)

- Path: `dashboard/public/data/calendly_bookings.json`
- Fields: `summary.paid_ads_7d`, `summary.paid_ads_28d`, `summary.organic_7d`, `bookings[]`
- Channel attribution via Calendly event type slug suffix:
  - `-pa` paid ads
  - `-or` / `-or1` organic
  - `-in` Instagram DM
  - `-li` LinkedIn
  - `-yt` YouTube
  - `-e` email
  - full map in `channel_map` + `slug_map` fields of the JSON
- `paid_ads_7d` and `paid_ads_28d` are the ONLY trustworthy source for "calls booked from paid ads".
- Window choice: `7d` for "this week booked" displays, `28d` for revenue joins (sales-cycle lag).
- Update: weekly cron (Monday 06:00 UTC).

### Client tracker sheet = revenue

- Path: `dashboard/public/data/sheet_revenue.json`
- Source: Google Sheet "Rob TCC - Master Client Tracker", ID `1DQmN40LFoTHGrRYG0sNFpfzyK8qXPm0rYDZW3K1DNGY`
- 4 active tabs scanned: Bens 1-1 Clients, Propel Prog Clients, Propel Project, Members Association
- Fields: `summary.new_signups_7d`, `summary.total_revenue_7d`, `signups_7d[]` (each has email, name, tab, start_date, mrr, pif, total)
- Mahmoud fills amounts manually post-call. Stripe auto-populates the row. This sheet is the ground truth for revenue.
- Join pattern: email-match against `calendly_bookings.json` with 28-day window to attribute revenue to paid ads.
- Update: weekly cron.

### Meta pixel = form submits, NEVER booked calls

- Path: `dashboard/public/data/meta_ads_campaigns.json`
- Fields: `summary.total_form_submits_7d`, `ad_sets[].ads[].form_submits_7d`, etc.
- Semantics: `actions.lead` events only (de-duped from the triple-labelled lead / fb_pixel_lead / lead_grouped family).
- `form_submits` are NOT booked calls. They are application-form submissions. Historical form-to-book ratio is roughly 4.5:1 but varies by campaign type.
- On webinar funnels, pixel `lead` fires on webinar registration. Never treat those as booked discovery calls.
- `meta_pixel_calls` (schedule + omni_scheduled_conversation) is a separate pixel signal that is often 0 or low and still not ground truth.
- Use Meta pixel for ad-set-level health signals only (is the ad converting clicks to form submissions?). For any call count or revenue attribution, cross-reference Calendly and the sheet.
- See `dashboard/public/data/SCHEMA.md` section "Two definitions of calls booked" for the full explanation.

### GHL = unreliable, use with caveat

- Path: `dashboard/public/data/ghl_data.json`, `dashboard/public/data/ghl_dms.json`
- Contains: contacts, opportunities, form submissions, DMs.
- Issue: tagging is inconsistent. Mahmoud flagged this as a known issue.
- Use for DM count, contact search, form cross-reference. Do not use for booked-call counts or revenue attribution (use Calendly + sheet instead).

### intelligence.json = pre-analyzed Opus output

- Path: `dashboard/public/data/intelligence.json`
- Contains: cross-platform strategy + per-channel analysis (meta_ads, instagram, linkedin, email, youtube, website).
- `intelligence.meta_ads.roas_snapshot` has deterministic numbers computed in Python (paid_spend_7d, paid_calls_booked_7d / 28d, paid_revenue_7d, cost_per_paid_call_7d, roas_7d, paid_pipeline_breakdown_28d). These are injected into the Opus prompt and then overwritten after Opus runs to guarantee consistency.
- Use this when you want pre-analyzed data without re-running the framework yourself.
- Freshness: weekly cron + occasional `--only-channel` reruns.

---

## 5. The framework — Meta Ads stage-aware analysis

### Step 1. Classify every campaign

Read `campaign_objective` and the ad-set-level `optimization_goal` (or the `stage` field already computed by the pipeline). Map to TOF / MOF / BOF:

- `OUTCOME_AWARENESS`, `OUTCOME_VIDEO_VIEWS` → **TOF**
- `OUTCOME_ENGAGEMENT` with optimisation `PROFILE_VISITS` / `THRUPLAY` / `VIDEO_VIEWS` → **TOF**; otherwise → **MOF**
- `OUTCOME_TRAFFIC` → **MOF** (unless specifically optimised for profile visits, in which case TOF — check)
- `OUTCOME_LEADS`, `OUTCOME_SALES` → **BOF**

`meta_ads_campaigns.json` already has the `stage` field computed for each ad set. Use it. Do not re-derive.

### Step 2. Judge each stage by its own metric

| Stage | Primary metric | Secondary | Never judge by |
|---|---|---|---|
| **TOF** | Cost per IG follower (spend / followers acquired) | ThruPlay rate, CPM (> £25 concern), frequency (> 3.5 fatigue) | CTR, form submits, cost per call |
| **MOF** | Cost per opt-in / DM conversation | Engagement rate, content relevance | Cost per booked call |
| **BOF** | Cost per real Calendly call (spend / `paid_ads_7d` from Calendly) | CTR link, form submit rate | Pixel `lead` events as calls |

### Step 3. Apply kill / scale / watch thresholds — BOF ONLY

These thresholds are BOF-specific. NEVER apply them to TOF or MOF.

- **CTR link < 0.8%** → kill candidate
- **CTR link ≥ 1.5%** → healthy baseline
- **CTR link ≥ 2.5% consistently across ad sets** → scale candidate
- **Cost per form submit ≤ £50** → healthy
- **Cost per form submit > £75** → problem
- **Landing page booking rate < 8%** → diagnostic flag (check creative-to-LP fit, never "LP friction"; see §6)
- **Budget split target**: 50% BOF / 30% MOF / 20% TOF (use `summary.stage_spend_7d` to check the current split)
- **Minimum impressions for verdict**: 1,000 per ad set. Below that, output "insufficient signal", not a verdict.
- **Learning phase**: never kill during `LEARNING` or `LEARNING_LIMITED`. Minimum 50 conversion events before a verdict.

### Step 4. Ground truth for ROAS

Always compute ROAS from:

- Numerator: `sheet_revenue` signups in the last N days whose email matches a `calendly_bookings.paid_ads_28d` entry (email join, 28-day window for sales-cycle lag).
- Denominator: paid-ads-attributable spend — BOF ad-set spend only from `meta_ads_campaigns.json`.

Never compute ROAS from pixel events.

If denominator > 0 and numerator = 0, UI state is "Pending" (not "0.0x"). There are bookings in the pipeline that haven't closed yet.

---

## 6. Output rules — hard nevers

These apply to any recommendation text, report, summary, or automation output. They are in addition to the tone rules in the global and project-level CLAUDE.md layers.

### Never in output

- **Kill recommendations on ad sets with `status=PAUSED`**. If it's already paused, there's nothing to kill. Filter by active status before issuing kill verdicts.
- **"Simplify the form" / "reduce landing page friction" / "remove qualification"**. The application form is the qualification filter by design. A form-submit-to-booking drop is the filter working as intended, not a UX problem.
- **Treat pixel `lead` events as booked calls**. Always cross-reference Calendly.
- **Team-member names** (Mahmoud, Ben, Rob, Jay, Antonio) in free-text recommendations. Write about the system and the data, not the people maintaining it.
- **Internal snake_case field names** (`paid_calls_booked`, `taken_no_outcome`, etc.) in prose. Use natural language.
- **Assert "the call happened" as fact**. The system sees scheduled events, not attendance. Write "scheduled calls" or "bookings", not "calls taken".
- **Speculate about sales-call quality, pitch clarity, onboarding friction**. The data shows scheduling and revenue, not conversation content.
- **Directive "kill immediately"**. Reframe as "watch closely" or "concern" with the reasoning.
- **Em-dashes (—), en-dashes (–)** anywhere.
- **Pad numbers to look precise** when the underlying data is directional. If the metric is ±10%, don't write it to the penny.

### Always in output

- **Data freshness stamp**. Reader knows when the numbers were last refreshed (read from `intelligence.json._metadata.generated_at` or collector `fetched_at` fields).
- **Data caveat block** for any Meta pixel number. The SCHEMA.md has canonical caveat text; use it or link to it.
- **Stage-aware verdicts**. Never issue a verdict without declaring the stage.
- **Per-stage reasoning**. If recommending kill / scale, explain which stage rule is being applied.
- **Pipeline state** when revenue-related. If there are pending paid bookings, say so explicitly rather than implying "0 revenue means ads don't convert".

---

## 7. Patterns — reference implementations

### Daily operational Meta Ads brief (Mahmoud use case)

Reference: `BenHawkCode/The-Coach-Consultant-/1-meta-ads/meta-ads-daily-review/fetch_daily_review.py`

That skill already handles:

- Meta API fetch (ad-set + ad level, with quality rankings and learning status)
- Calendly API live fetch (with snapshot fallback)
- IG follower tracking (for TOF Profile Visit campaigns)
- Per-stage classification (OBJECTIVE_STAGE mapping)
- Per-stage verdicts (BOF-only anomaly checks)
- Creative × audience matrix
- Markdown output

If the task is "generate today's Meta Ads brief", run that skill. Do not rebuild. If the output format needs to differ (for example push to Google Drive instead of local markdown), wrap the skill output and push. Do not rebuild the analysis.

### Weekly strategic intelligence (Ben H use case)

Reference: `BenHawkCode/The-Coach-Consultant-/1-meta-ads/meta-ads-weekly-intelligence/`

Reads `intelligence.json` directly. All analysis is pre-computed by the Monday cron. The skill formats into MD + auto-generates HTML dashboard.

Ship additions (new section, new metric) by updating the skill.md template, not by running separate analysis.

### Custom dashboard / Slack digest / Drive push

Pattern:

1. Consume existing skill output OR read `intelligence.json` directly.
2. Format for the target surface (Slack blocks / Drive Doc / HTML / whatever).
3. Apply §6 output rules before emitting.
4. Apply the build checklist in §8 before shipping.

Do not re-analyze raw Meta data for a new surface. One analysis, many presentations.

### New non-Meta channel request

If Ben asks for analysis of Instagram, YouTube, Email, LinkedIn, or Website, the corresponding Jay skill folder is the reference. Do not build a new analysis pipeline on the side without asking first.

---

## 8. Build checklist — anti-hallucination gate

Before shipping any output (text, report, automation run, dashboard update), verify:

- [ ] **Data sources are canonical**: bookings from Calendly (not Meta pixel), revenue from the client tracker sheet (not Stripe API, not GHL opportunities), Meta pixel used only for ad-set-level form-submit health.
- [ ] **Stage classification done first**: every campaign verdict declares its stage (TOF / MOF / BOF). No verdict without stage.
- [ ] **Per-stage metrics applied**: TOF on cost per IG follower, MOF on cost per opt-in, BOF on cost per real Calendly call. No BOF thresholds on TOF or MOF.
- [ ] **Kill verdicts exclude PAUSED ad sets**: only active ad sets are killable.
- [ ] **Existing Jay skill checked**: if the task looks like daily-review or weekly-intelligence, the corresponding skill is being reused or explicitly improved, not replaced silently.
- [ ] **Output rules respected**: no team names, no snake_case leakage, no "simplify the form", no "kill immediately" directives, no em-dashes.
- [ ] **Freshness stamp included**: reader knows when the data was refreshed.
- [ ] **Data caveat included**: where pixel numbers appear, the form-submit-not-a-call caveat is present.
- [ ] **Pending state handled**: if the revenue calc has a pipeline gap, UI shows "Pending", not "0.0x".
- [ ] **Cross-check numbers**: if Meta says X and Calendly says Y, explain the gap in-text. Never silently pick one.

If any item fails, fix before shipping. If something is genuinely new (doesn't fit an existing pattern), flag to Ben before proceeding rather than improvise.

---

## When in doubt — where to read

- `dashboard/scripts/generate_intelligence.py` — canonical analysis logic + Opus prompts + `_build_roas_snapshot`. Single source of truth for the framework.
- `dashboard/public/data/SCHEMA.md` — field-by-field schema reference, "Two definitions of calls booked" section.
- `BenHawkCode/The-Coach-Consultant-/1-meta-ads/meta-ads-daily-review/fetch_daily_review.py` — working reference implementation with live data fetch.
- `BenHawkCode/The-Coach-Consultant-/1-meta-ads/meta-ads-weekly-intelligence/skill.md` — reference for weekly brief structure.
- Global CLAUDE.md (`/Users/benhawksworth/.claude/CLAUDE.md`) — voice / format / tone rules that apply everywhere.

Never guess. Never improvise a threshold. Never invent a metric. If the framework doesn't cover a case, ask.
