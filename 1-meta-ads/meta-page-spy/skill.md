---
name: meta-page-spy
description: Spy on any Facebook page - scrape organic posts AND paid ads to produce a combined intelligence report. Covers posting frequency, content types, engagement metrics, hook/CTA patterns, posting schedule, and offer positioning. Use this whenever the user wants to analyze a competitor's Facebook page, spy on a page, understand what someone is doing on Facebook, or compare organic vs paid strategy. Triggers on "spy on", "analyze [page] Facebook", "what is [name] doing on Facebook", "scrape [page]", or /meta-page-spy.
---

# Meta Page Spy - Facebook Page Intelligence

## Purpose

Scrape any Facebook page's organic posts AND paid ads from Ad Library, then produce a single combined intelligence report. This gives you a full picture of how a page operates: what they post organically, how often, what hooks work, and what they're running as paid ads.

## When to Use

- User wants to analyse a specific Facebook page
- "Spy on [page name]"
- "What is [name] doing on Facebook"
- "Analyze [name]'s Facebook strategy"
- "Scrape [page URL]"
- Comparing organic vs paid content strategy for a competitor

## Workflow

### Step 1: Ask for the Target

Ask the user which Facebook page they want to spy on. Accept either:
- A Facebook page URL (e.g. `https://www.facebook.com/DanMartell`)
- A page name (e.g. "Dan Martell")

Example prompt:
> "Which Facebook page do you want to spy on? Give me the URL or page name."

### Step 2: Run the Scraper

Execute the page_spy.py script:

```bash
cd /Users/learnai/Desktop/The\ Coach\ Consultant/1-meta-ads/meta-page-spy
python page_spy.py "<page_url_or_name>"
```

This runs two Apify actors sequentially:
1. `apify/facebook-posts-scraper` - scrapes 50 organic posts
2. `curious_coder/facebook-ads-library-scraper` - scrapes 20 paid ads from Ad Library

Requires `APIFY_API_TOKEN` in the project root `.env` file.

### Step 3: Present Findings

After the script completes, read the generated report from `outputs/[page-name]-[date].md` and present key findings to the user:

1. **Posting frequency** - how often they post, trending up or down
2. **Content mix** - what types of content dominate
3. **Top performing posts** - what's getting the most engagement and why
4. **Hook patterns** - what opening styles they use most
5. **Posting schedule** - when they post
6. **Paid strategy** - what hooks they use in ads and what they're selling

Focus on actionable insights: what can Ben learn and apply from this page's strategy.

## Report Sections

The generated report contains 9 sections:

| # | Section | What it Covers |
|---|---------|---------------|
| 1 | Posting Frequency | Posts/week, posts/month, trend |
| 2 | Content Type Breakdown | Video, image, text, reel, carousel % |
| 3 | Top 10 Posts by Engagement | Full text, metrics, hook type, URL |
| 4 | Hook Pattern Analysis (Organic) | Distribution + avg engagement per hook type |
| 5 | CTA Pattern Analysis (Organic) | Hard/Soft/Engagement/None distribution |
| 6 | Posting Schedule | Day-of-week + time-of-day breakdown |
| 7 | Paid Ads Hook & CTA Patterns | Hook/CTA distribution from ads + top examples |
| 8 | Paid Ads Offer Positioning | CTA buttons, link captions, detected offers |
| 9 | Key Takeaways | 5-7 actionable bullet points |

## Output

Reports are saved to:
```
1-meta-ads/meta-page-spy/outputs/[page-name]-[YYYY-MM-DD].md
```

## Dependencies

- Python 3.x
- `apify_client` library
- `APIFY_API_TOKEN` in `.env` (project root)

## Example Usage

**User:** "Spy on Dan Martell's Facebook page"

**Claude:**
1. Runs `python page_spy.py "Dan Martell"`
2. Waits for scraping to complete
3. Reads the report from `outputs/dan-martell-2026-04-01.md`
4. Presents: "Dan Martell posts 5.2 times per week (stable trend). 68% video content. Statement hooks dominate at 55% but Question hooks get 2x the engagement. Posts most on Tuesday and Thursday. In paid ads, he's running Hard CTAs to a free training offer..."

**User:** "Spy on https://www.facebook.com/AlexHormoziYT"

**Claude:**
1. Runs `python page_spy.py "https://www.facebook.com/AlexHormoziYT"`
2. Same flow as above
