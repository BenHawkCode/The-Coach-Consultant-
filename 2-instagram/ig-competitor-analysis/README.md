# IG Competitor Analysis

Scrape and analyse multiple Instagram competitor profiles to find winning patterns for The Coach Consultant.

## What It Does

Scrapes 12 competitor profiles (configurable), analyses their posts, and generates a consolidated report comparing:
- Hook patterns and engagement per hook type
- Content format performance (carousel vs video vs image)
- CTA strategies
- Caption length vs engagement
- Top performing posts and hooks across all competitors
- Actionable recommendations for Ben

## Quick Start

```bash
# Full analysis (all 12 competitors, ~30 posts each)
python ig_competitor_scraper.py

# Single competitor
python ig_competitor_scraper.py --sender "hormozi"

# Re-analyze cached data (no API calls)
python ig_competitor_scraper.py --analyze-only

# Limit posts per profile
python ig_competitor_scraper.py --max-posts 20
```

## Requirements

- `APIFY_API_TOKEN` in project root `.env`
- Python 3.8+
- `apify-client` package (`pip install apify-client`)

## Output

Reports: `outputs/IG-COMPETITOR-ANALYSIS-[date].md`
Raw data cache: `data/[username]-raw.json`

## Files

```
ig-competitor-analysis/
├── README.md                      # This file
├── skill.md                       # Full skill documentation for Claude
├── competitor-list.md             # Tracked profiles with rationale
├── ig_competitor_scraper.py       # Multi-profile scraper + analyser
├── data/                          # Cached raw scraped data
│   └── [username]-raw.json
└── outputs/                       # Generated reports
    └── IG-COMPETITOR-ANALYSIS-*.md
```

## Competitor List

12 profiles across 3 tiers. See `competitor-list.md` for full details.

Edit `COMPETITORS` in `ig_competitor_scraper.py` to add/remove profiles.
