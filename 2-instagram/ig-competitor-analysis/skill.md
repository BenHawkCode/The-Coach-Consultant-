---
name: ig-competitor-analysis
description: Scrape multiple Instagram competitor profiles and generate a consolidated analysis report. 31 profiles verified, 847 posts analysed (April 2026). Compares hook patterns, caption structures, engagement data, content formats, CTA strategies across all competitors. Key findings - Story hooks get 70K avg engagement, Carousel posts outperform (37K avg), 78% of posts have no CTA. Triggers on "analyse Instagram competitors", "IG competitor analysis", "what are competitors doing on Instagram", or /ig-competitor-analysis.
---

# IG Competitor Analysis - Instagram Competitive Intelligence

## Purpose

Scrape multiple Instagram competitor profiles using Apify, then generate a consolidated cross-competitor analysis report. Identifies winning hook patterns, best-performing content formats, CTA strategies, caption length insights, and actionable patterns for Ben's Instagram strategy.

**Key Difference from Instagram Page Spy:** Page Spy analyses a single profile in depth. This skill compares multiple competitors side-by-side to find market-wide patterns.

## Data Source

**Scraper:** `ig_competitor_scraper.py` (Apify `apify/instagram-scraper`)
**Competitor List:** 31 verified profiles across 5 tiers (see `competitor-list.md`)
**Requires:** `APIFY_API_TOKEN` in project root `.env`

## ✅ DATA ALREADY COLLECTED
**31 Profiles | 847 Posts Analysed | April 2026**

Key findings available in:
- `outputs/IG-COMPETITOR-ANALYSIS-2026-04-07.md` — Full consolidated report
- `outputs/IG-COMPETITOR-ANALYSIS-tier1-2026-04-07.md` — Direct competitors only
- `data/[username]-raw.json` — Raw scraped data per profile

**Known Pattern Distribution (from 847 posts):**
- **Hook:** Story hooks get highest engagement (70,375 avg) but only 3.2% of posts. Statement is most common (51.4%).
- **Format:** Carousel dominates engagement (37,340 avg) despite Video/Reel being most posted (59.5%).
- **CTA:** 77.7% of posts have NO CTA. Only 5.5% use Hard CTA.
- **Caption Length:** Long captions (800+) get 2x engagement (34,977) vs short (<300 at 16,413).
- **Top Performers:** Iman Gadzhi (181K avg), Steven Bartlett (156K avg), Chris Williamson (53K avg).

## When to Use

- "Analyse Instagram competitors"
- "What are competitors doing on Instagram?"
- "Compare our IG strategy to competitors"
- "Which hooks work best on Instagram right now?"
- "IG competitor analysis"
- Before planning a new Instagram content strategy
- Quarterly competitive review

## Workflow

### Step 1: Ask Scope

Use AskUserQuestion:

**Question 1: Scope**
- "All competitors" (full 12-profile analysis)
- "Tier 1 only" (top 5 direct competitors)
- "Specific profile" (deep dive on one competitor)
- "Custom username" (analyse any Instagram profile)

**Question 2: Purpose**
- "Content strategy" (what formats and hooks to use)
- "Competitive benchmark" (how Ben compares)
- "Hook inspiration" (swipe file of best hooks)
- "Posting schedule" (when to post)

### Step 2: Run Scraper

```bash
cd /Users/learnai/Desktop/The\ Coach\ Consultant/2-instagram/ig-competitor-analysis

# Full analysis (all 12 competitors)
python ig_competitor_scraper.py

# Single competitor
python ig_competitor_scraper.py --sender "hormozi"

# Custom username (not in list)
python ig_competitor_scraper.py --sender "newcompetitor"

# Limit posts per profile
python ig_competitor_scraper.py --max-posts 20

# Re-analyze existing data (no API calls)
python ig_competitor_scraper.py --analyze-only
```

### Step 3: Present Report

Read the generated report from `outputs/IG-COMPETITOR-ANALYSIS-[date].md` and present key findings:

1. **Competitor ranking** by average engagement
2. **Hook patterns** that drive the most engagement
3. **Content format** winners (carousel vs video vs image)
4. **CTA strategy** distribution across competitors
5. **Caption length** correlation with engagement
6. **Top 20 posts** across all competitors with hooks
7. **Swipe file** of 30 best-performing hooks
8. **Actionable takeaways** for Ben's strategy

## Report Sections

| # | Section | What it Covers |
|---|---------|---------------|
| 1 | Competitor Overview | All profiles ranked by engagement with key stats |
| 2 | Hook Pattern Analysis | Distribution + avg engagement per hook type |
| 3 | Content Format Analysis | Carousel/Video/Image performance comparison |
| 4 | CTA Strategy | Hard/Soft/Engagement/No CTA distribution |
| 5 | Caption Length Analysis | Short/Medium/Long performance comparison |
| 6 | Top 20 Posts | Best performing posts across all competitors |
| 7 | Top 30 Hooks Swipe File | Copy-paste hooks ranked by engagement |
| 8 | Key Takeaways for Ben | 7 actionable recommendations |

## Hook Classification

| Type | Example | Trigger Words |
|------|---------|--------------|
| Question | "Are you still doing this manually?" | ?, how, what, why |
| Pain Point | "You're stuck at £5K months..." | struggling, stuck, tired of |
| Metric/Result | "147 business owners added £5K/month" | £, $, %, numbers |
| Bold Statement | "Most people get this completely wrong" | secret, truth, myth, lie |
| Story | "When I started, I had zero clients..." | when I, I was, my first |
| How-To | "3 steps to predictable client flow" | how to, steps, framework |
| Engagement Bait | "Comment SYSTEM if you want this" | comment, save this, tag |
| Statement | Direct opening without pattern trigger | (default) |

## Integration with Other Skills

**Feeds into:**
- `instagram-caption` — use winning hooks from competitor analysis
- `instagram-carousel` — use best-performing formats identified

**Complements:**
- `instagram-page-spy` — deep dive on individual profiles found interesting
- `meta-page-spy` — cross-channel competitor view (IG + FB)
- `meta-ad-competitor` — compare organic IG strategy vs paid Meta strategy

## Competitor Profiles

See `competitor-list.md` for the full list with tiers and rationale.

**Current tracking:** 31 profiles across 5 tiers
- Tier 1: Direct competitors (Ben, Hormozi, Martell, Brunson, Leila)
- Tier 2: Marketing operators (UK-focused where possible)
- Tier 3: Authority benchmarks

## Output

Reports saved to:
```
2-instagram/ig-competitor-analysis/outputs/IG-COMPETITOR-ANALYSIS-[YYYY-MM-DD].md
```

Individual raw data cached in:
```
2-instagram/ig-competitor-analysis/data/[username]-raw.json
```

## Ben's Voice Application

When presenting findings or generating content based on competitor patterns:
- British English always
- "business owners and service providers" (NEVER say "coaches")
- Ben's natural phrases: "Right so", "Sound familiar", "I see this constantly"
- No forbidden AI phrases
- Direct, Yorkshire straight-talking tone
