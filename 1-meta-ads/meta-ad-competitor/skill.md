---
name: meta-ad-competitor
description: Analyze competitor Meta ads from 29 top performers. 561 ads analyzed. Proven hook patterns - 60% Statement hooks, 16% Metric/Result, 14% Question. Generate hybrid ad variations in Ben's voice using data-backed winning patterns.
---

# Meta Ad Competitor Analysis Skill

## Purpose
Analyze competitor Meta ads from 29 top performers (Alex Hormozi, Dan Martell, Russell Brunson, etc.), extract winning hooks and creative patterns using actual Facebook Ad Library data (561 ads analyzed), and generate hybrid ad variations in Ben's voice.

## ✅ DATA ALREADY COLLECTED
**29 Competitors | 561 Active Ads Analyzed | March 2026**

Key findings available in:
- `/outputs/CONSOLIDATED-ANALYSIS-29-COMPETITORS.md` - Full pattern analysis
- `/outputs/TOP-50-HOOKS-SWIPE-FILE.md` - Copy-paste hooks
- `/outputs/ad-library-analysis/` - Individual competitor reports

## Trigger Phrases
- `/meta-ad-competitor`
- "analyze competitor ads"
- "scrape [competitor name] ads"
- "what is [competitor] doing on Meta"
- "I want to use meta-ad-competitor skill"

## Required Setup
- Meta Ad Library API access (must be approved first)
- Meta Marketing API access (for pulling your own ad performance data)
- `.env` file with credentials:
  - `META_ACCESS_TOKEN`
  - `META_APP_ID`
  - `META_APP_SECRET`
  - `META_ACCOUNT_ID`

## Workflow

### Step 1: User Input
Ask the user:
1. **Which competitor?** (Dropdown from 29-name list below OR "All" for general patterns)
2. **Campaign objective?** (Lead Gen, Webinar, Course, Consultation, Awareness)
3. **What offer are you promoting?** (So we can adapt competitor hooks to your context)

**If specific competitor selected:** Read their individual report from `/outputs/ad-library-analysis/[competitor-name]-ad-library-2026-03-24.md`

**If "All" or general:** Use consolidated patterns from `/outputs/CONSOLIDATED-ANALYSIS-29-COMPETITORS.md`

### Step 2: Data Collection

**OPTION A: Use Existing Data (Recommended)**
- Reference `/outputs/CONSOLIDATED-ANALYSIS-29-COMPETITORS.md` for patterns
- Reference `/outputs/TOP-50-HOOKS-SWIPE-FILE.md` for specific hooks
- Reference individual competitor reports in `/outputs/ad-library-analysis/`

**OPTION B: Fresh Scrape (If needed)**
- Use `/apify_ad_library_scraper.py` to pull fresh data from Facebook Ad Library
- Requires `APIFY_API_TOKEN` in `.env`
- Scrapes 20 ads per competitor using Apify's facebook-ads-library-scraper
- Extract 7 key elements per ad:
  1. Hook type (Statement, Metric/Result, Question, Bold Statement, Pain Point, Story, How-To)
  2. Opening line (first 125 characters)
  3. CTA style (No CTA, Hard CTA, Soft CTA, Engagement CTA)
  4. Offer positioning
  5. Run duration
  6. Page name
  7. Platforms (Facebook, Instagram, Messenger, etc.)

**Known Pattern Distribution (from 561 ads):**
- **Statement:** 59.4% (most common)
- **Metric/Result:** 16.2% (high-converting)
- **Question:** 13.7% (engagement driver)
- **Bold Statement:** 3.4% (pattern interrupt)
- **Pain Point:** 2.5% (problem-aware audience)
- **Story/How-To:** <1% each

**CTA Patterns (from 561 ads):**
- **No CTA:** 67.2% (content-first approach)
- **Hard CTA:** 13.7% (direct conversion)
- **Engagement CTA:** 9.6% (social proof play)
- **Soft CTA:** 6.4% (consideration stage)

### Step 3: Analysis & Pattern Extraction

**IF SPECIFIC COMPETITOR SELECTED (e.g., "Alex Hormozi"):**

1. **Read their individual report:** `/outputs/ad-library-analysis/[competitor-name]-ad-library-2026-03-24.md`
2. **Extract their specific patterns:**
   - Their dominant hook type (from Hook Pattern Analysis section)
   - Their most common CTA style
   - Their top 5 longest-running ads (best performers)
   - Their specific opening lines and copy structure

Example - Alex Hormozi:
```
Hook Distribution: 65% Metric/Result, 30% Statement, 5% Question
CTA Style: 65% Hard CTA, 35% No CTA
Top Hook: "👉 Join 171.9k community builders collectively earning over $1 billion per year..."
Pattern: Lead with big number → Social proof → Simple setup → Clear CTA
```

**IF "ALL" OR GENERAL PATTERNS:**

1. **Use consolidated analysis:** `/outputs/CONSOLIDATED-ANALYSIS-29-COMPETITORS.md`
2. **Apply general patterns:** 60% Statement, 16% Metric/Result, 14% Question
3. **Reference Top 50 Hooks:** `/outputs/TOP-50-HOOKS-SWIPE-FILE.md`

### Step 4: Generate Ad Variations

Generate 5 new ad variations using:

**Priority 1: Competitor-Specific Patterns** (if specific competitor selected)
- Use their dominant hook type
- Match their CTA style
- Adapt their proven opening lines to Ben's offer
- Keep their structural patterns (number of bullets, emoji usage, etc.)

**Priority 2: Ben's Voice Guidelines** (ALWAYS)
- British English throughout
- No AI jargon ("Here's the thing", "Let's dive in")
- Yorkshire directness, short punchy sentences
- One sentence per line

**Priority 3: Your Objective** (ALWAYS)
- Match campaign objective (Lead Gen vs Awareness)
- Adapt to your specific offer
- Keep target audience (coaches/consultants) in mind

Each variation includes:
- Primary text (under 125 chars for optimal performance)
- Full ad copy
- Headline (5-7 words)
- CTA (matched to competitor style + campaign objective)
- Recommended creative format
- **Why This Works:** Explanation of which competitor pattern was used

### Step 4: Save Output
Save analysis to `outputs/[competitor-name]-[date].md`

## 🎯 PROVEN HOOK FORMULAS (Data-Backed)

Based on 561 ads analyzed, here are the highest-performing patterns:

### Formula 1: Statement Hook (59.4% success rate)
```
[Direct Value Proposition] + [Simple Process] + [Clear Outcome]
```
**Example:** "Here's the biz plan: 1. Business owners need content. 2. They'd rather pay someone to do it. 3. Use A.I. to create it."

### Formula 2: Metric/Result Hook (16.2% usage, high conversion)
```
[Specific Number] + [Target Audience] + [Achieving Result]
```
**Example:** "👉 Join 171.9k community builders collectively earning over $1 billion per year on the Skool platform TODAY."

### Formula 3: Question Hook (13.7% usage, high engagement)
```
[Relatable Situation] + [Question that triggers self-reflection]
```
**Example:** "Starting a service business? Make this one 45 second video and send it to every person in your contact list"

### Formula 4: Bold Statement Hook (3.4% usage, pattern interrupt)
```
[Controversial/Unexpected Statement] + [Why it matters]
```
**Example:** "How To Get Consulting Clients Using Ugly Ads. I got served this ad and I thought it didn't work... Until I looked behind the scenes."

### Formula 5: Pain Point Hook (2.5% usage, problem-aware)
```
[Most people struggle with X] → [Here's the real problem] → [Here's the solution]
```
**Example:** "Most brands don't have an ad problem — they have a creative problem. At CreativeCon, you'll learn how top brands..."

## 📊 TIER-SPECIFIC STRATEGIES

### Tier 1: Business Education & Coaching (Alex Hormozi, Dan Martell, Russell Brunson)
- **Dominant Hook:** Metric/Result (60% of their ads)
- **CTA Mix:** 50% Hard CTA, 50% No CTA
- **Offer Type:** High-ticket consulting, platforms, courses
- **Strategy:** Lead with proof, numbers, social validation

### Tier 2: Marketing & Agency Operators (Billy Gene, Molly Pittman, Cat Howell)
- **Dominant Hook:** How-To/Framework (educational)
- **CTA Mix:** 70% No CTA (authority building)
- **Offer Type:** Training programs, agency services
- **Strategy:** Teach first, sell second

### Tier 3: Content-First Entrepreneurs (Gary Vee, Ali Abdaal, Iman Gadzhi)
- **Dominant Hook:** Statement + Story blend
- **CTA Mix:** 80% No CTA (pure value)
- **Offer Type:** Books, courses, memberships
- **Strategy:** Value-first, long-form content repurposed

### Tier 4: Copywriters & Strategists (Stefan Georgi, Justin Goff)
- **Dominant Hook:** Pain Point → Solution
- **CTA Mix:** Balanced (authority + conversion)
- **Offer Type:** Events, workshops, high-ticket services
- **Strategy:** Demonstrate expertise through copy quality

### Tier 5: UK-Specific (James Sinclair, Rob Moore, Andrew & Pete)
- **Dominant Hook:** Statement (conversational, less aggressive)
- **CTA Mix:** More Soft CTAs (UK market preference)
- **Offer Type:** UK-focused programs, local events
- **Strategy:** British tone, less "American hustle"

## Competitor Swipe List (31 Total)

**Tier 1: Business Education & Coaching**
1. Alex Hormozi
2. Dan Martell
3. Russell Brunson
4. Sam Ovens
5. Frank Kern
6. Myron Golden
7. Leila Hormozi
8. Pedro Adao
9. Brendon Burchard
10. Tony Robbins

**Tier 2: Marketing & Agency Operators**
11. Billy Gene Shaw
12. Molly Pittman
13. Cat Howell
14. Nick Shackelford
15. Khalid Hamadeh
16. Andrew Hubbard
17. Depesh Mandalia

**Tier 3: Content-First Entrepreneurs**
18. Gary Vaynerchuk
19. Hormozi Media Team
20. Chris Williamson
21. Steven Bartlett
22. Ali Abdaal
23. Iman Gadzhi

**Tier 4: Copywriters & Creative Strategists**
24. Stefan Georgi
25. Justin Goff
26. Dara Denney
27. Barry Hott
28. Sarah Levinger

**Tier 5: UK-Specific**
29. Andrew & Pete
30. Rob Moore
31. James Sinclair

## Example Usage

### Example 1: Specific Competitor Style

**User:** `/meta-ad-competitor` "Alex Hormozi" "lead generation" "Free Coaching Scorecard"

**What Claude Does:**
1. Reads `/outputs/ad-library-analysis/alex-hormozi-ad-library-2026-03-24.md`
2. Extracts Alex's patterns:
   - 65% Metric/Result hooks
   - 65% Hard CTA
   - Emoji usage (👉 ❤️‍🔥 🤝 💙 ✅)
   - Structure: Big number → Mission → Simple setup → CTA
3. Generates 5 ads in "Alex Hormozi style" but for Ben's coaching scorecard offer
4. Example output:
```
👉 Join 300+ coaches, consultants and service providers collectively adding £2.5M+ in revenue using this exact system.

🎯 Our mission: Help 10,000 UK coaches escape manual overwhelm
⚡ Simple setup: Download scorecard, implement 3 changes, see results in 7 days
💰 Proven method: Top performers use this to identify their biggest revenue leak

Get your free Coaching Business Scorecard now: thecoachconsultant.uk/scorecard

✅ 15-min assessment
✅ Personalised action plan
✅ £50K→£150K roadmap
```

### Example 2: General Patterns

**User:** `/meta-ad-competitor` "All" "webinar" "Systems Automation Masterclass"

**What Claude Does:**
1. Reads `/outputs/CONSOLIDATED-ANALYSIS-29-COMPETITORS.md`
2. Uses general distribution: 60% Statement, 16% Metric, 14% Question
3. References `/outputs/TOP-50-HOOKS-SWIPE-FILE.md` for proven hooks
4. Generates 5 variations (3 Statement, 1 Metric, 1 Question) in Ben's voice

### Example 3: Natural Language

**User:** "I want to create ads like Dan Martell for my free systems audit"

**What Claude Does:**
1. Detects competitor: Dan Martell
2. Reads `/outputs/ad-library-analysis/dan-martell-ad-library-2026-03-24.md`
3. Extracts Dan's patterns:
   - 55% Statement, 40% Question
   - 70% No CTA (content-first)
   - Conversational, less aggressive
4. Generates ads matching Dan's softer approach but for Ben's offer

## Output Format
- Markdown report saved to `outputs/`
- Includes competitor analysis + your data + hybrid ad variations
- All new ad copy written in Ben's voice (per CLAUDE.md guidelines)

## Dependencies
- Python 3.x
- `requests` library
- Access to Meta Ad Library API (requires approval)
- Access to Meta Marketing API (already configured)

## Notes
- Longer ad run duration = proxy for performance (Meta keeps winners running)
- Focus on UK/US/AU markets (Ben's primary audiences)
- All generated ad copy must pass Ben's voice quality control checklist
- Cross-reference with `/Jay-Notes/meta-ad-competitor-swipe-list.md` for full competitor context
