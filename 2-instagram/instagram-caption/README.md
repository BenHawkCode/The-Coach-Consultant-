# Instagram Caption Generator

Generate Instagram captions that sound exactly like Ben Hawksworth, backed by real performance data.

**✅ Status:** Performance data loaded (41 posts analyzed via Apify scraper)
**📊 Data Source:** @benhawksworth_ Instagram profile (scraped March 24, 2026)
**🎯 Average Engagement:** 107 per post | Top 10 average: 268 (2.5x better)

## Quick Start

### 1. Setup Meta API Access

**Prerequisites:**
- Meta Business Account
- Instagram Business or Creator account connected
- Meta Developer account

**Steps:**

1. **Create Meta App**
   - Go to [developers.facebook.com](https://developers.facebook.com/)
   - Create New App → Business
   - Add Instagram Basic Display API

2. **Get Instagram Business ID**
   ```bash
   # Test API access
   curl -X GET "https://graph.facebook.com/v21.0/me/accounts?access_token=YOUR_TOKEN"

   # Get Instagram Business ID
   curl -X GET "https://graph.facebook.com/v21.0/{PAGE_ID}?fields=instagram_business_account&access_token=YOUR_TOKEN"
   ```

3. **Setup Environment**
   ```bash
   # Copy template
   cp .env.example .env

   # Edit with your credentials
   nano .env
   ```

4. **Install Dependencies**
   ```bash
   pip install requests python-dotenv pandas
   ```

### 2. Fetch Historical Posts

```bash
python scripts/fetch_posts.py
```

**What it does:**
- Fetches last 50 Instagram posts
- Pulls engagement metrics (likes, comments, saves, shares)
- Calculates weighted engagement rate
- Saves to `outputs/instagram_posts.json`

**Output:**
```
📡 Fetching last 50 Instagram posts...
✅ Fetched 50 posts
💾 Saved to 2-instagram/instagram-caption/outputs/instagram_posts.json

📊 QUICK SUMMARY
🔥 Top 5 Posts by Engagement Rate:
1. 8.45% - Right so here's what nobody tells you about client onboarding...
   👍 234 | 💬 18 | 💾 42 | 👁️ 3,421
...
```

### 3. Analyze Performance Patterns

```bash
python scripts/analyze_performance.py
```

**What it does:**
- Identifies top 10 performers
- Analyzes hook patterns
- Correlates length vs engagement
- Measures CTA impact
- Extracts topic themes
- Saves to `outputs/performance_report.json`

**Output:**
```
📊 INSTAGRAM PERFORMANCE ANALYSIS

📈 Overall Metrics (50 posts)
   Avg Engagement Rate: 5.67%
   Avg Reach: 2,845
   Avg Likes: 156
   ...

🔥 Top 10 Performers
1. Engagement: 8.45% | Lines: 12 | CTA: True
   Hook: Right so here's what nobody tells you about client onboarding
   ...

💡 Hook Patterns
   Common starters:
     - 'Right so' (12 times)
     - 'I see' (8 times)
     - 'Sound familiar' (6 times)
   ...
```

### 4. Generate Captions

```bash
# Single caption
python scripts/generate_caption.py --topic "email marketing automation"

# Multiple variants for A/B testing
python scripts/generate_caption.py --topic "pricing strategy" --variants 3
```

**What it does:**
- Loads performance patterns
- Finds similar top-performing posts
- Predicts engagement rate
- Provides structure guidance
- Checks brand voice compliance

**Output:**
```
======================================================================
📝 INSTAGRAM CAPTION GENERATED
======================================================================

📊 PERFORMANCE PREDICTION
Estimated engagement rate: 6.8%
Based on: Right so here's the pricing mistake I see constantly...
           (Top post: 7.2% engagement)
Confidence: High
Reasoning: Length factor: 1.12x | CTA factor: 1.05x

📝 CAPTION
----------------------------------------------------------------------
[Your generated caption here]
----------------------------------------------------------------------

🎯 OPTIMIZATION NOTES
- Line count: 13 lines
- CTA included: Yes
- Hook: Right so email marketing in 2026
- Similar top post: 7.2% engagement

✅ Brand voice compliance: PASSED
```

## Performance Metrics Explained

### Engagement Rate Formula

```
Engagement Rate = (Likes + Comments*3 + Saves*5 + Shares*7) / Reach * 100
```

**Why this weighting?**
- **Likes (1x)** - Passive engagement
- **Comments (3x)** - Active conversation
- **Saves (5x)** - High intent (bookmarking for later)
- **Shares (7x)** - Maximum value (amplification + endorsement)

### What Makes a Top Performer

Posts ranked by:
1. **Engagement rate** (primary metric)
2. **Reach** (secondary - audience size)
3. **Saves rate** (quality signal)
4. **Profile visits** (conversion indicator)

## Brand Voice Rules

### ✅ Ben's Natural Phrases
- "Right so"
- "gonna" / "kinda"
- "I see this all the time"
- "Sound familiar"
- "The shift is simple"
- "What actually works"

### ❌ Forbidden AI Phrases
- "Here's the thing" / "Let's dive in"
- "In this comprehensive guide"
- "At the end of the day"
- "Game changer" / "Unlock" / "Leverage"

### Format Rules
- Single short sentences, one per line
- No full stops overused, no dashes
- Max 15-20 lines
- British English (organisation, behaviour)
- CTA: www.thecoachconsultant.uk

## Files Structure

```
2-instagram/instagram-caption/
├── SKILL.md                    # Skill documentation
├── README.md                   # This file
├── .env.example                # Environment template
├── scripts/
│   ├── fetch_posts.py          # Meta API data fetcher
│   ├── analyze_performance.py  # Pattern analyzer
│   └── generate_caption.py     # Caption generator
└── outputs/
    ├── instagram_posts.json    # Fetched posts data
    ├── performance_report.json # Analysis results
    └── caption_*.txt           # Generated captions
```

## Workflow Example

```bash
# Weekly routine
python scripts/fetch_posts.py          # Update data
python scripts/analyze_performance.py  # Find patterns

# When creating content
python scripts/generate_caption.py --topic "Meta ads for coaches"

# A/B testing
python scripts/generate_caption.py --topic "client retention" --variants 3
```

## Troubleshooting

### "No module named 'requests'"
```bash
pip install requests python-dotenv pandas
```

### "META_ACCESS_TOKEN required"
- Check `.env` file exists (not `.env.example`)
- Verify credentials are correct
- Ensure no spaces around `=` in .env

### "API Error: Invalid OAuth access token"
- Token may be expired
- Regenerate token in Meta Developer Console
- Ensure token has required permissions

### "No posts found"
- Run `fetch_posts.py` first
- Check if `outputs/instagram_posts.json` exists
- Verify Instagram Business account has posts

## Meta API Rate Limits

- **200 calls per hour** per app
- **200 calls per user per hour**
- Use caching (already implemented)
- Run fetch weekly, not on every generation

## Advanced Usage

### Custom Analysis Period

Edit `fetch_posts.py`:
```python
posts = fetch_instagram_posts(limit=100)  # Fetch last 100 posts
```

### Export for Other Tools

```python
import json

with open('outputs/performance_report.json', 'r') as f:
    report = json.load(f)

# Use in other scripts
top_hooks = [p['hook'] for p in report['top_10_performers']]
```

### Integration with Other Skills

```bash
# Use with meta-ad-copy for consistent voice
python ../meta-ad-copy/scripts/generate_ad.py --reference-instagram

# Combine insights across channels
python scripts/analyze_cross_channel.py
```

## Next Steps

1. **Test generated captions** - Post and track actual performance
2. **Refine predictions** - Compare predictions vs actual results
3. **A/B test hooks** - Try different proven patterns
4. **Monitor trends** - Re-run analysis weekly
5. **Update voice rules** - Add new patterns from top performers

## Related Skills

- **meta-ad-copy** - Paid ads with same voice
- **youtube-scripts** - Long-form content
- **email-campaigns** - Newsletter writing

## Support

Questions? Check:
- [Meta API Documentation](https://developers.facebook.com/docs/instagram-basic-display-api/)
- [Instagram Insights API](https://developers.facebook.com/docs/instagram-api/reference/ig-media/insights)
- Main project: `docs/CLAUDE.md`

---

**Version:** 1.0.0
**Last Updated:** 2026-03-19
**Maintained by:** Claude Code
