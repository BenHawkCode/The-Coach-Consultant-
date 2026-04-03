---
name: instagram-page-spy
description: Spy on any Instagram profile - scrape posts and generate a full intelligence report. Covers content breakdown (carousel/image/video), engagement rates, top posts, hook/CTA patterns, posting schedule, caption analysis, and hashtag strategy. Use this whenever the user wants to analyze a competitor's Instagram, spy on an IG profile, understand what someone is doing on Instagram, or research content strategy. Triggers on "spy on [username] instagram", "analyze [username] IG", "what is [name] posting on instagram", or /instagram-page-spy.
---

# Instagram Page Spy - Profile Intelligence

## Purpose

Scrape any Instagram profile and generate a comprehensive intelligence report. Content breakdown, engagement metrics, top posts, hook patterns, CTA analysis, posting schedule, caption length insights, and hashtag strategy - everything you need to understand how a profile operates.

## When to Use

- User wants to analyse a specific Instagram profile
- "Spy on @username"
- "What is [name] doing on Instagram"
- "Analyze [name]'s Instagram strategy"
- "Scrape [username] IG"
- Researching competitor content strategy on Instagram

## Workflow

### Step 1: Ask for the Target

Ask the user which Instagram profile they want to spy on. Accept either:
- A username (e.g. `danmartell` or `@danmartell`)
- A full Instagram URL (e.g. `https://instagram.com/danmartell`)

Example prompt:
> "Which Instagram profile do you want to spy on? Give me the username or URL."

### Step 2: Run the Scraper

Execute the ig_spy.py script:

```bash
cd /Users/learnai/Desktop/The\ Coach\ Consultant/2-instagram/instagram-page-spy
/opt/homebrew/opt/python@3.14/Frameworks/Python.framework/Versions/3.14/bin/python3 ig_spy.py "<username>"
```

This runs Apify's `apify/instagram-scraper` to pull up to 50 recent posts with full engagement data.

Requires `APIFY_API_TOKEN` in the project root `.env` file.

### Step 3: Present Findings

After the script completes, read the generated report from `outputs/[username]-[date].md` and present key findings:

1. **Posting frequency** - how often they post, trending up or down
2. **Content mix** - carousel vs image vs video/reel breakdown + which performs best
3. **Top performing posts** - what's getting the most engagement and why
4. **Hook patterns** - what opening styles they use in captions
5. **CTA patterns** - how they drive action
6. **Posting schedule** - when they post (days + times)
7. **Caption length** - short vs long captions and what works better
8. **Hashtag strategy** - which hashtags they use most

Focus on actionable insights: what can Ben learn and apply.

## Report Sections

| # | Section | What it Covers |
|---|---------|---------------|
| 1 | Posting Frequency | Posts/week, posts/month, trend |
| 2 | Content Type Breakdown | Carousel/Image/Video % + avg engagement per type |
| 3 | Top 10 Posts by Engagement | Full caption, metrics, hook type, URL |
| 4 | Hook Pattern Analysis | Distribution + avg engagement per hook type |
| 5 | CTA Pattern Analysis | Hard/Soft/Engagement/Follow/None distribution |
| 6 | Posting Schedule | Day-of-week + time-of-day breakdown |
| 7 | Caption Analysis | Length vs engagement correlation |
| 8 | Hashtag Analysis | Top 15 most used hashtags |
| 9 | Key Takeaways | Actionable bullet points |

## Output

Reports are saved to:
```
2-instagram/instagram-page-spy/outputs/[username]-[YYYY-MM-DD].md
```

## Dependencies

- Python 3.x
- `apify_client` library
- `APIFY_API_TOKEN` in `.env` (project root)

## Example Usage

**User:** "Spy on @danmartell's Instagram"

**Claude:**
1. Runs `python ig_spy.py danmartell`
2. Waits for scraping to complete
3. Reads the report from `outputs/danmartell-2026-04-01.md`
4. Presents: "Dan Martell posts 4.2 times per week (stable). 60% carousels, 30% reels, 10% images. Carousels get 2x the engagement. Statement hooks at 45% but Question hooks drive highest engagement. Posts mostly on Tuesday and Thursday at 15:00 UTC..."
