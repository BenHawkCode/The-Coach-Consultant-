# The Coach Consultant - AI Content Generation System

## Project Overview

**Company:** The Coach Consultant
**Founder:** Ben Hawksworth
**Website:** https://thecoachconsultant.uk/
**GitHub:** https://github.com/BenHawkCode/The-Coach-Consultant-

**Business Model:**
- Info-course products
- Agency services
- 1-1 consulting for business owners and service providers

**Primary Mission:**
Generate content that sounds EXACTLY like Ben speaks and writes - no AI-sounding phrases, no corporate jargon, pure authenticity.

**Target Audience (NEW IP — May 2026 refresh):**
Open business owners and service providers, men and women equally, 35-50 years old (mostly mid-40s), £100K-£500K annual revenue (high-heat zone £8.5K-£30K monthly), founder-led service businesses across coaching, agency, consulting, course creation, health, B2B. UK-heavy (Manchester, Leeds, Birmingham, Sheffield) plus international slice (Dubai, Spain, Australia). Avatar name: **Sam**. Hero pain: **The Guesswork Tax** (every growth decision is a guess because they have no AI intelligence behind it). See `docs/new-ip/02-dream-client-avatar.md` and `docs/new-ip/09-targeting-dream-customer.md` for full ICP.

---

## Project Structure

Content generation skills are organised by channel (matching Ben's Google Drive master dashboard):

```
The Coach Consultant/
├── 1-meta-ads/                    # Meta Ads skills
│   ├── meta-ad-copy/              # Ad copy generator (competitor-backed)
│   ├── meta-ad-competitor/        # Competitor ad scraper
│   ├── meta-ads-daily-review/     # Daily campaign review for Ben Mahmoud (NEW)
│   ├── meta-ads-weekly-intelligence/  # Weekly strategic report for Ben (NEW)
│   ├── meta-page-spy/            # Facebook page spy
│   └── bottom-of-funnel/         # BOF ad assets
├── 2-instagram/                   # Instagram skills
├── 3-youtube/                     # YouTube skills
├── 4-emails/                      # Email skills
├── 5-linkedin/                    # LinkedIn skills
├── 6-website-seo/                 # Website/SEO skills
├── optimisation-skills/           # Token optimisation, system tools
├── docs/                          # Brand documentation
│   ├── new-ip/                    # MASTER — new IP bank (May 2026 refresh, 11 docs)
│   ├── Ben-Claude-Projects-Instructions.txt  # Channel format rules
│   ├── IP-Folder-Summary.md       # Index of new IP + what stayed from old
│   └── deep-dive/                 # Limited use — voice samples (verbatim quotes), philosophy (biography), archive (do not read)
├── prompts/                       # Prompt vault
├── .env                           # API tokens (Meta, GitHub, Apify, TCC dashboard)
└── SKILLS-README.md               # Full skills documentation
```

**See [SKILLS-README.md](SKILLS-README.md) for complete list of available skills.**

---

## Core Directive: Sound Like Ben

**Your ONE job:** Match Ben's voice, tone, speaking patterns, sentence structure, energy, and natural flow.

**Source Authority (HARD RULES):**

1. **MASTER — `docs/new-ip/`** is the only source for positioning, ICP, pain, voice rules, signature phrases, forbidden phrases, offer structure, and content strategy. **Always use new IP. Do not fall back to anything else for these topics.**
2. **`docs/Ben-Claude-Projects-Instructions.txt`** is the only source for channel format rules (YouTube script structure, email layout, podcast formatting, carousel slide structure). Format-only — never voice or positioning.
3. **`docs/deep-dive/voice-samples/`** is a real-transcript library (YouTube scripts, sales calls). Use ONLY when you need to lift a literal speaking-pattern example. Never use it for ICP, positioning, or voice rules — those come from new IP.
4. **`docs/deep-dive/philosophy/`** is Ben's personal narrative (50/50 book, life story). Use ONLY when content explicitly requires Ben's biography. Never use it for positioning or voice rules.

**Archived — DO NOT READ:** `docs/deep-dive/_archive_old-icp/` and `docs/deep-dive/_archive_old-frameworks/`. Superseded by new IP. Treat as deleted for content generation purposes.

**The hard rule:** if a question is about who we sell to (ICP), what we sell (offer), how we sound (voice), what to say (signature phrases), or what not to say (forbidden phrases) — the answer comes from `docs/new-ip/`. Period.

**Critical Rule:**
Use transcripts for VOICE EXTRACTION ONLY. Never use them for informational content. Use your own knowledge for facts, strategies, and insights.

---

**CRITICAL: NEVER use the word "coaches" in any generated content. Always use "business owners and service providers".**

## Brand Voice Rules (Core Only)

### British English Always
- organisation (not organization)
- behaviour, colour, optimise, summarise
- "business owners and service providers" (NEVER say "coaches")

### Forbidden AI Phrases (NEVER USE)
- "Here's the thing" / "Here's the reality" / "Here's how"
- "Let's dive in" / "Dive in"
- "In this comprehensive guide"
- "It's important to note"
- "At the end of the day"
- "In conclusion" / "To summarise"
- "First and foremost"
- "Game changer" / "Game-changing" / "Ground-breaking"
- "Unlock" / "Unlock potential"
- "Leverage"
- "Journey" / "Transformation journey"
- "Level up"
- "Ladies and gentlemen"
- Em-dashes / en-dashes (use short dashes only)
- Gendered defaults ("the bloke", "the guy", "him") — speak to men + women equally

### Ben's Natural Phrases (USE THESE)
**General voice (from old + new IP):**
- "Right so" / "Right, so..." (to start explanations)
- "gonna" (not "going to")
- "kinda"
- "Look, here's the thing..."
- "Mate, the truth is..."
- "Doing my head in..."
- "Proper" (as adverb — "proper good", "proper honest")
- "From that point"
- "Sound familiar"

**New IP signature phrases (USE OFTEN — these are the spine of all content):**
- "You are the bottleneck of your business"
- "Stop guessing growth"
- "AI intelligence, not AI tools"
- "Personal brand plus AI adoption"
- "Done-with-you, not done-by-yourself, not done-to-you"
- "Built for you, used by you, owned by you"
- "Frameworks just the same"
- "Promised the world before"
- "I cannot add any more stress to my plate"
- "Predictability is the new growth metric"
- "Replace £100K+/month in staff wages with copy-paste SOPs"
- "Two things separate winners right now: Personal Brand and AI Adoption"
- "Manual processes aren't authentic. They're inefficient."

**Cost-of-inaction stack (use real numbers, not vague claims):**
- £120K — annual cost of staying manual
- 1,820 hours/year — admin time AI intelligence replaces
- £2,300/week — revenue left on the table
- 50+ pieces/week — content competitors produce while you guess
- 12 months — gap with AI-forward competitors that compounds

**The 4-Step Programme (reference where logical):**
1. Growth Intelligence Audit (45 min, no obligation)
2. Claude AI Specialist Setup (custom-built, trained on operator)
3. Personal Brand and AI Adoption Roadmap (90-day path)
4. 90-Day Growth Map (copy-paste SOPs, owned forever)

### Punctuation & Tone
- **Never use dashes** or excessive punctuation (sounds robotic)
- **No full stops overused** (keep it conversational)
- Short punchy sentences, one per line
- Line breaks between thoughts
- Direct, straight-talking, Yorkshire influence
- No corporate fluff or buzzwords
- Authority through personal experience (not theory)

---

## Channel-Specific Rules

For detailed channel rules (Instagram Captions, YouTube Scripts, Email Campaigns, Podcast Scripts, Carousel Posts), reference:

📄 **`docs/Ben-Claude-Projects-Instructions.txt`** (PRIMARY - Ben's actual rules)

Quick summary per channel:

### Instagram Page Spy
- **SKILL AVAILABLE:** `instagram-page-spy` - Spy on any Instagram profile
- **Scraper:** `2-instagram/instagram-page-spy/ig_spy.py` (Apify instagram-scraper)
- Combined intelligence report: content types, engagement metrics, hook/CTA patterns, posting schedule, caption analysis, hashtags
- Single profile deep-dive per run
- Outputs to `2-instagram/instagram-page-spy/outputs/`
- See `2-instagram/instagram-page-spy/skill.md` for full workflow

### IG Competitor Analysis
- **SKILL AVAILABLE:** `ig-competitor-analysis` - Multi-profile competitive intelligence
- **Scraper:** `2-instagram/ig-competitor-analysis/ig_competitor_scraper.py` (Apify instagram-scraper)
- **DATA LOADED:** 31 verified profiles, 847 posts analysed (April 2026)
- **Key findings:** Story hooks = 70K avg engagement, Carousel = best format (37K avg), 78% posts have no CTA, Long captions (800+) = 2x engagement
- **Top performers:** Iman Gadzhi (181K avg), Steven Bartlett (156K avg), Chris Williamson (53K avg)
- Top 30 hooks swipe file, actionable takeaways for Ben
- Outputs to `2-instagram/ig-competitor-analysis/outputs/`
- See `2-instagram/ig-competitor-analysis/skill.md` for full workflow

### Instagram Captions
- **Performance data loaded** - 41 posts analyzed from @benhawksworth_ via Apify Instagram scraper
- **Data sources:** `2-instagram/data/` (JSON exports, processed analytics)
- **Optimal length:** 800+ characters (NOT 15-20 lines - longer performs better!)
- **Top hooks:** "Comment [WORD]" (808 engagement), "You are NOT..." (198), Direct questions
- **Best type:** Carousel posts (161 avg engagement vs 74 for videos)
- One sentence per line, no emojis, no hashtags, no headers
- See `docs/Ben-Claude-Projects-Instructions.txt` lines 1-75
- **Performance insights:** `2-instagram/data/INSTAGRAM_DATA_OPTIONS.md`
- **Scrapers available:** `2-instagram/scrapers/apify_scraper.py`, `apify_simple.py`, `instagram_scraper.py`, `process_data.py`

### YouTube Scripts
- 12-15 min scripts (12,000-15,000 chars)
- Teleprompter format with timestamps
- Supporting assets first (title, thumbnail, description, timestamps)
- CTA: www.thecoachconsultant.uk
- See `docs/Ben-Claude-Projects-Instructions.txt` lines 77-287

### YouTube Thumbnail Generator
- **SKILL AVAILABLE:** `youtube-thumbnail-generator` — local Streamlit app powered by Gemini 3.1 Flash Image Preview
- **Skill location:** `3-youtube/thumbnail-generator/` (skill.md, app.py, thumbnail_engine.py, prompts/style_presets.py)
- **API key:** reads `GEMINI_API_KEY` from project-root `.env` (alongside Meta, GitHub, Apify, Calendly tokens)
- **Three modes:** Clone Reference (upload competitor thumbnail, copy style), Preset Style (Hormozi Bold / MrBeast Reaction / Podcast Split / Minimal Text / Alex Hormozi Black), Hybrid (full overrides — bg colour, text position, expression)
- **Face library:** seeded with 2 Ben photos at `assets/ben-faces/` — extras can be uploaded via sidebar
- **Outputs:** `outputs/YYYY-MM-DD/HHMMSS-<hash>-vN.png` + sibling `metadata.json`
- **Negative prompts enforced:** Gemini blocked from copying timestamps, duration overlays, YouTube UI, watermarks
- **Invocation:** when user says "thumbnail", "/thumbnail", "open thumbnail generator" → run pre-flight checks (venv/deps/.env), launch on port 8520 in background, hand off URL
- See `3-youtube/thumbnail-generator/skill.md` for the full pre-flight + launch workflow

### Email Campaigns
- **SKILL AVAILABLE:** `email-campaign-ben-hawksworth` - Auto-triggers for email generation
- **Skill location:** `4-emails/email-campaign-skill/` (complete skill with agent.md, prompt.md, examples)
- **Performance data:** 471 emails analyzed + 65 campaigns with real metrics (184K delivered, 43.76% avg open rate)
- **Data sources:** `4-emails/ghl-data/` (GoHighLevel exports, campaign analytics)
- **WINNING FORMULAS** (data-backed):
  - **BadBizAdvice series:** 59.49% avg open, £9,116 from ONE email 🏆
  - **#theGAPyoumiss series:** 56.16% avg open, £11,217 total revenue
  - **Personal transformation:** 46% open, 1%+ CTR (best engagement)
- Start: `Hi {{first_name}},`
- One sentence per line, 20-30 lines minimum
- Subject: Use proven formulas from `4-emails/ghl-data/PERFORMANCE_INSIGHTS.md`
- Soft reply CTA (CHAT, CONNECT, START)
- Sign off: `Ben` + `www.thecoachconsultant.uk`
- See `docs/Ben-Claude-Projects-Instructions.txt` lines 291-461
- **Full analysis:** `4-emails/ghl-data/COMPLETE_EMAIL_STATISTICS.md` + `PERFORMANCE_INSIGHTS.md`
- **SKILL AVAILABLE:** `email-competitor-spy` - Analyse 10 competitor newsletters (Antonio's pipeline data)
- **Competitors tracked:** Alex Hormozi, Dan Martell, Andrew & Pete, Ezra Firestone, Molly Pittman, James Sinclair, Chris Williamson, Frank Kern, Tony Robbins, Leila Hormozi
- **Data source:** `4-emails/email-competitor-spy/data/competitor_newsletters.json` (auto-updated weekly)
- **Script:** `4-emails/email-competitor-spy/analyze_competitors.py`

### Podcast Scripts
- 4,200-4,500 words
- ElevenLabs formatting (line breaks for pauses)
- Minimal punctuation, no semicolons
- See `docs/Ben-Claude-Projects-Instructions.txt` lines 463-683

### Carousel Posts
- 10 slides (Slide 1 = hook, Slides 2-9 = value, Slide 10 = CTA)
- See `docs/Ben-Claude-Projects-Instructions.txt` lines 797-825
- **Visual Asset Library:** 384 transparent PNGs at `2-instagram/instagram-carousel/TCC Carousels/Interactive Assets/exported-icons/png/`
  - Use icons, system diagrams, comparison tables, and infographics as slide elements
  - Key folders: `ai-systems-and-architecture/`, `flow-charts-and-processes/`, `personal-branding-systems/`, `lead-gen-and-sales-systems/`, `claude-ai-product-visuals/`
  - Re-export with `node export-icons.js` if the HTML source is updated

### Meta Ad Copy
- **SKILL AVAILABLE:** `meta-ad-copy` - Generates ad copy with user discovery questions
- **Competitor Analysis:** Apify Facebook scraper available (`1-meta-ads/meta-ad-competitor/apify_facebook_scraper.py`)
- Lead with pain point or opportunity
- Include specific metrics when available
- Strong CTA (Book a Call, Download Guide, etc.)
- Test different hooks: question, statement, statistic
- Keep primary text under 125 characters for optimal performance
- Headlines: 5-7 words, benefit-focused
- See `1-meta-ads/meta-ad-copy/skill.md` for full prompt library

### Meta Ads Daily Review
- **SKILL AVAILABLE:** `meta-ads-daily-review` - Daily campaign review for Ben Mahmoud (Ads Manager)
- **Purpose:** Replaces manual screenshot-to-Claude workflow for BOF campaign analysis
- **Data:** Pulls live data from Meta Ads API (reads root `.env` for `META_ACCESS_TOKEN` + `META_ACCOUNT_ID` — no skill-local `.env`)
- **Output:** Ad set health check, creative × audience matrix, kill/scale/watch verdicts, Meta quality flags, anomaly detection, top priorities
- **Thresholds:** 0.8% CTR kill, 1.5% target, £50 cost/call, 8% booking rate, 50/30/20 budget split
- **Week phase logic:** Week 1 = watch only, Week 2+ = kill/scale decisions, Weeks 3-5 = copy testing
- **Files:** `1-meta-ads/meta-ads-daily-review/` (skill.md, fetch_daily_review.py, config.yaml, setup.sh)
- Outputs to `1-meta-ads/meta-ads-daily-review/outputs/`

### Meta Ads Weekly Intelligence
- **SKILL AVAILABLE:** `meta-ads-weekly-intelligence` - Strategic weekly report for Ben (founder)
- **Purpose:** Birds-eye funnel view answering Ben's 6 requirements: funnel gaps, BOF booking growth, creative needs, spend scaling, weekly feedback, dashboard-connected
- **Data:** Reads from Antonio's `tcc-dashboard` GitHub repo (`SudhakaPr/tcc-dashboard` fork)
  - `public/data/intelligence.json` → Opus strategic analysis (verdicts, anomalies, priorities, TOF/MOF/BOF recommendations)
  - `public/data/meta_ads_campaigns.json` → ad set × creative breakdown (7d + 28d metrics, creative audience matrix)
  - Schema: `public/data/SCHEMA.md`
- **GitHub access:** PAT in `.env` as `TCC_GITHUB_TOKEN`, repo as `TCC_GITHUB_REPO`
- **Weekly cron:** Antonio's pipeline runs Monday 06:00 UTC, commits fresh data to GitHub
- **Output sections:** Executive summary, funnel health check, BOF booking growth levers, creative kill/scale/isolate lists + new creative briefs, spend scaling guidance with budget bars, anomalies + quality flags, weekly priorities, cross-platform context
- **Dashboard mode:** After generating markdown report, offers to convert to HTML dashboard (Tailwind CSS, colour-coded verdicts, heatmap, collapsible sections)
- **Files:** `1-meta-ads/meta-ads-weekly-intelligence/` (skill.md)
- Outputs to `1-meta-ads/meta-ads-weekly-intelligence/outputs/`

### Meta Page Spy
- **SKILL AVAILABLE:** `meta-page-spy` - Spy on any Facebook page (organic + paid)
- **Scraper:** `1-meta-ads/meta-page-spy/page_spy.py` (Apify facebook-posts-scraper + Ad Library scraper)
- Combined intelligence report: posting frequency, content types, engagement, hooks, CTAs, schedule, offer positioning
- Single page deep-dive per run
- Outputs to `1-meta-ads/meta-page-spy/outputs/`
- See `1-meta-ads/meta-page-spy/skill.md` for full workflow

### LinkedIn Posts
- Professional but personal
- Share insights, not just promotions
- Include a story or example
- Ask a question to drive engagement
- Use 3-5 relevant hashtags
- Tag people/companies when relevant

---

## Content Categories

### Marketing
- Meta ads optimization (with competitor analysis via Apify scraper)
- Instagram content strategy (performance data-driven)
- Email marketing and automation (471 emails analyzed, winning formulas identified)
- LinkedIn lead generation
- YouTube content systems

### Operations
- Client onboarding automation
- CRM and pipeline management
- Performance tracking
- Team workflows
- Process documentation

### Strategy
- Offer positioning
- Pricing strategies
- Sales systems
- Retention and referrals
- Business model optimization

---

## Competitor Analysis

**Benchmark Against:**
- Other coaching consultancies
- Business coaching programs
- Marketing agencies for business owners and service providers
- Course creators in the coaching space

**Differentiation:**
- Tech-forward AI automation approach
- Data-driven systems over theory
- Implementation support, not just strategy
- Claude ecosystem integration

---

## Documentation Reference

### MASTER — `docs/new-ip/` (THE source for positioning, ICP, pain, voice, offer, content strategy)

The new IP bank (May 2026 refresh). Eleven docs. **Use these for any content task. Do not pull from anywhere else for these topics.**

- `01-offer-waterfall.md` — top-line positioning (read first when writing anything for TCC)
- `02-dream-client-avatar.md` — Sam persona (chaotic Tuesday, ideal Wednesday, decision criteria)
- `03-brand-identity.md` — voice rules, signature phrases, philosophy, four brand pillars
- `04-offer-positioning.md` — ten-step tactical positioning playbook
- `05-niche-domination.md` — owning the conversation in our niche
- `06-pain-isolation.md` — deep emotional pain analysis (six layers, 3 AM thoughts)
- `07-value-proposition.md` — what we're selling, financial impact, competitive comparison
- `08-content-categories.md` — five content categories with weekly rotation
- `09-targeting-dream-customer.md` — tactical ICP (use with #2 for full picture)
- `10-pain-point-articulation.md` — copy-ready pain articulation, hooks, urgency frames
- `11-emotional-triggering.md` — ten emotional triggers with ready-to-use templates

**See `docs/IP-Folder-Summary.md` for index.**

### CHANNEL FORMATS — `docs/Ben-Claude-Projects-Instructions.txt`
Format-only rules: YouTube script structure, email layout, podcast formatting, carousel slides. Use this for HOW to structure a piece of content, never for what it should say or sound like.

### LIMITED-USE REFERENCES — `docs/deep-dive/`

These are NOT alternatives to new IP. They have narrow purposes:

**`voice-samples/`** — real transcript library (YouTube + sales calls). Pull from here ONLY when you need a literal speaking-pattern example to lift verbatim. Never use it for ICP, positioning, or voice rules — new IP defines those.

**`philosophy/`** — Ben's personal narrative (50/50 book, life story). Pull from here ONLY when content explicitly requires Ben's biography or the 50/50 framework. Never use it for positioning, offer, or voice rules — new IP defines those.

### ARCHIVED — DO NOT READ
- `docs/deep-dive/_archive_old-icp/` — old Alex Morgan persona, superseded
- `docs/deep-dive/_archive_old-frameworks/` — old offer waterfall, niche domination, brand positioning, value proposition, all superseded

Treat the archive folders as deleted. Never open them for content generation.

---

## Content Generation Workflow

**Step 1 — Always start with new IP:**
- ICP question → `docs/new-ip/02-dream-client-avatar.md` + `09-targeting-dream-customer.md`
- Voice/tone/signature phrases → `docs/new-ip/03-brand-identity.md`
- Pain/copy/hooks → `docs/new-ip/06-pain-isolation.md` + `10-pain-point-articulation.md`
- Offer/positioning → `docs/new-ip/01-offer-waterfall.md` + `04-offer-positioning.md`
- Content planning/categories → `docs/new-ip/08-content-categories.md` + `11-emotional-triggering.md`
- Niche/authority → `docs/new-ip/05-niche-domination.md`
- Value prop/financial impact → `docs/new-ip/07-value-proposition.md`

**Step 2 — Check channel format rules:** `docs/Ben-Claude-Projects-Instructions.txt` (only for HOW to structure the format).

**Step 3 — Generate content** using new IP signature phrases, new IP forbidden-word list, new IP cost-of-inaction stack, and the 4-step programme reference where logical.

**Do NOT** consult `docs/deep-dive/` unless the task explicitly needs (a) a verbatim transcript quote or (b) Ben's biography. Those are the only two exceptions.

---

## AI Automation Guidelines

### Skills & Agents Usage
1. **Research Agent**: Analyze competitor content, market trends, audience insights
2. **Fact-Check Agent**: Verify claims, statistics, and statements for accuracy
3. **Tone Agent**: Ensure content matches brand voice and target audience
4. **Conversion Agent**: Optimize for engagement and conversion

### Quality Standards
- All generated content must be reviewed by human before publishing
- Citations required for statistics and claims
- Brand voice consistency across all channels
- Mobile-first formatting for all content
- Accessibility considerations (alt text, clear language)

---

## Quality Control Checklist (from new IP)

Before finalising ANY output, verify:

✅ Does it speak directly to Sam (the avatar)?
✅ Does it lead with the guesswork tax or the bottleneck identity?
✅ Does it frame AI as intelligence, not just tools?
✅ Does it reference predictability as the goal, not just growth?
✅ Does it position personal brand and AI adoption together?
✅ Does it use mate-to-mate Yorkshire voice, not corporate?
✅ Does it reference the 4-step programme structure where logical?
✅ Does it use real numbers (£100K, £120K, 1,820 hours), not vague claims?
✅ Does it speak to men and women equally (no gendered defaults)?
✅ Does it use British English, no em-dashes?
✅ Does it avoid forbidden phrases ("transformation journey", "unlock", "level up", "dive in", "game changer")?
✅ Does it sound like Ben, not a strategy template?
✅ Would this flow naturally when read aloud?

If yes to all, ship. If any are off, rewrite.

---

## Data Infrastructure

**Performance Data Available:**
- **Instagram:** 41 posts from @benhawksworth_ (scraped via Apify, stored in `2-instagram/data/`)
- **Email:** 471 emails + 65 campaigns from GoHighLevel (stored in `4-emails/ghl-data/`)
- **Meta Ads:** Competitor analysis scraper ready (`1-meta-ads/meta-ad-competitor/apify_facebook_scraper.py`)
- **Meta Ads (Own):** Live campaign data via Antonio's weekly pipeline → `tcc-dashboard` GitHub repo
  - `intelligence.json` — Opus strategic analysis (6 channels + cross-platform)
  - `meta_ads_campaigns.json` — ad set × creative breakdown with 7d/28d metrics
  - `meta_ads_raw.json` — raw Meta API dump for debugging
  - Schema: `public/data/SCHEMA.md`
  - Pipeline runs Monday 06:00 UTC via GitHub Action

**TCC Dashboard (Antonio's repo):**
- **Upstream:** `antonio-gasso/tcc-dashboard` (private)
- **Fork:** `SudhakaPr/tcc-dashboard` (our access)
- **Dashboard URL:** https://tcc-dashboard.netlify.app (password-gated)
- **Stack:** React 19 + TypeScript + Tailwind v4 + Recharts + Vite
- **Pipeline scripts:** `.claude/skills/creative-engine/scripts/` (collect_own_meta.py, collect_ga4.py, collect_ghl_data.py, generate_intelligence.py, etc.)
- **Access tokens in `.env`:** `TCC_GITHUB_TOKEN`, `TCC_GITHUB_REPO`, `TCC_META_ACCESS_TOKEN`

**Data Processing Scripts:**
- `2-instagram/scrapers/apify_scraper.py` - Main Instagram scraper
- `2-instagram/scrapers/apify_simple.py` - Simplified scraper
- `2-instagram/scrapers/instagram_scraper.py` - Alternative scraper
- `2-instagram/scrapers/process_data.py` - Data processing pipeline
- `1-meta-ads/meta-ad-competitor/apify_facebook_scraper.py` - Facebook ads scraper
- `1-meta-ads/meta-ads-daily-review/fetch_daily_review.py` - Live Meta API fetcher for daily review
- `1-meta-ads/meta-ads-daily-review/setup.sh` - Venv + dependency installer

---

## Important Notes

- This file defines brand context for ALL AI-generated content
- Update when brand guidelines, tone, or strategy changes
- All skills and agents reference this file + deep-dive docs
- Channel rules live in `docs/Ben-Claude-Projects-Instructions.txt` to save tokens
- Performance data drives content optimization across all channels

