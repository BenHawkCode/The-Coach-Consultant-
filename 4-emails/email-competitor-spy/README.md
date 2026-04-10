# Email Competitor Spy

Analyse competitor email newsletters to extract winning patterns for The Coach Consultant.

## What It Does

Reads competitor newsletter data (scraped by Antonio's pipeline) and produces an intelligence report covering:
- Subject line formulas and patterns
- Hook/opening styles
- CTA strategies
- Offer positioning
- Tone profiles
- Actionable recommendations for Ben's email campaigns

## Data Source

`data/competitor_newsletters.json` — maintained by Antonio's scraping pipeline, auto-updated weekly.

**Currently tracking 10 senders:**
Alex Hormozi, Dan Martell, Andrew & Pete, Ezra Firestone, Molly Pittman, James Sinclair, Chris Williamson, Frank Kern, Tony Robbins, Leila Hormozi

## Quick Start

```bash
# Full report
python analyze_competitors.py

# Single sender deep dive
python analyze_competitors.py --sender "Alex Hormozi"

# Quick terminal summary
python analyze_competitors.py --output print

# Raw JSON for piping
python analyze_competitors.py --output json
```

## Output

Reports saved to `outputs/EMAIL-SPY-REPORT-[YYYY-MM-DD].md`

## Integration

Feeds directly into the email campaign skill (`/email-campaign-ben-hawksworth`). Run this first to get competitive context, then generate campaigns using proven patterns.

## Files

```
email-competitor-spy/
├── README.md                  # This file
├── skill.md                   # Full skill documentation for Claude
├── analyze_competitors.py     # Analysis script
├── data/
│   └── competitor_newsletters.json  # Antonio's scraped data
└── outputs/
    └── EMAIL-SPY-REPORT-*.md  # Generated reports
```
