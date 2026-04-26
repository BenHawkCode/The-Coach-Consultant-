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

**Target Audience:**
Business owners and service providers (28-35 years old, £50K-£150K revenue, kitchen table entrepreneurs scaling their businesses).

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
├── prompts/                       # Prompt vault
├── .env                           # API tokens (Meta, GitHub, Apify, TCC dashboard)
└── SKILLS-README.md               # Full skills documentation
```

**See [SKILLS-README.md](SKILLS-README.md) for complete list of available skills.**

---

## Core Directive: Sound Like Ben

**Your ONE job:** Match Ben's voice, tone, speaking patterns, sentence structure, energy, and natural flow.

**Voice Source Priority:**
1. **PRIMARY:** `docs/Ben-Claude-Projects-Instructions.txt` (Ben's actual Claude Projects rules)
2. **SECONDARY:** `docs/deep-dive/voice-samples/` (voice characteristics, YouTube scripts, sales calls)

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
- "Let's dive in"
- "In this comprehensive guide"
- "It's important to note"
- "At the end of the day"
- "In conclusion" / "To summarise"
- "First and foremost"
- "Game changer" / "Unlock" / "Leverage" / "Journey"

### Ben's Natural Phrases (USE THESE)
- "Right so" (to start explanations)
- "gonna" (not "going to")
- "kinda"
- "From that point"
- "I see this constantly" / "I see this all the time"
- "Sound familiar"
- "The shift is simple"
- "The problem is"
- "What actually works"
- "That's how you"
- "Remember"
- "The thing is"

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

## Deep-Dive Documentation Reference

When you need deep brand context, reference **`docs/deep-dive/`**:

### Voice & Tone
- `voice-samples/voice-characteristics.md` - Quick voice guide
- `voice-samples/youtube-scripts-FULL.md` - 300 lines script sample
- `voice-samples/sales-calls-FULL.md` - 400 lines sales call sample

### Target Audience
- `target-audience/alex-morgan-persona.md` - ICP profile (28-35, £50K-£150K)
- `target-audience/pain-points.md` - 3-tier pain structure
- `target-audience/emotional-triggers.md` - 10 marketing triggers

### Philosophy & Beliefs
- `philosophy/core-beliefs.md` - Quick summary
- `philosophy/human-knowledge-FULL.md` - Ben's life story (507 lines)
- `philosophy/50-50-book-FULL.md` - Book intro (500 lines)

### Business Frameworks
- `frameworks/niche-domination.md`
- `frameworks/offer-waterfall.md`
- `frameworks/brand-positioning.md`
- `frameworks/value-proposition.md`

**Full structure:** See `docs/deep-dive/README.md`

---

## Content Generation Workflow

**Step 1:** Read quick references first
- `docs/deep-dive/voice-samples/voice-characteristics.md`
- `docs/deep-dive/target-audience/alex-morgan-persona.md`
- `docs/deep-dive/philosophy/core-beliefs.md`

**Step 2:** Check channel-specific rules
- `docs/Ben-Claude-Projects-Instructions.txt` (for format, structure, CTAs)

**Step 3:** Reference FULL files when needed
- Deep context for authentic voice matching
- Specific examples for tone calibration

**Step 4:** Generate content matching Ben's voice exactly

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

## Quality Control Checklist

Before finalising ANY output, verify:

✅ Does this sound like a human or AI?
✅ Would this flow naturally when read aloud?
✅ Have I avoided all forbidden AI phrases?
✅ Does this match Ben's energy and style?
✅ Is this targeting business owners and service providers?
✅ British English spelling throughout?
✅ Does it sound exactly like Ben would say it?

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

