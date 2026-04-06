---
name: instagram-caption
description: Generate Instagram captions matching Ben Hawksworth's authentic voice with Meta API performance analysis and engagement prediction. No AI fluff, pure authenticity backed by real data.
---

# Instagram Caption Generator

Generate Instagram captions that sound exactly like Ben Hawksworth - no AI fluff, pure authenticity, backed by real performance data.

## Core Mission

Create captions matching Ben's voice while analyzing past post performance via Meta API to optimize engagement, reach, and conversions.

## What This Skill Does

1. **Analyzes Real Performance Data** - Uses 41 historical Instagram posts scraped from @benhawksworth_
2. **Identifies Top Performers** - Patterns from posts with 2.5x higher engagement than average
3. **Generates Authentic Captions** - Creates content matching Ben's exact speaking style
4. **Performance Prediction** - Estimates engagement based on proven patterns
5. **A/B Testing Variants** - Generates multiple versions optimized for engagement

## Performance Data Summary

**Based on 41 posts analyzed:**
- Average engagement: 107 (likes + comments)
- Top 10 average: 268 (2.5x higher)
- Best performing type: **Carousel posts** (161 avg engagement)
- Optimal caption length: **800+ characters** (219 avg engagement for long captions)
- Top engagement trigger: **"Comment [WORD]" CTAs** (808 engagement on best post)

## Prerequisites

### Meta API Setup Required

You need:
- Meta Business Account with Instagram Business/Creator account connected
- Meta App with Instagram Basic Display API access
- Access Token with `instagram_basic` and `pages_read_engagement` permissions

**Quick Setup:**
1. Go to developers.facebook.com
2. Create app → Business → Instagram API
3. Get your Instagram Business Account ID
4. Generate access token with required permissions
5. Store credentials in `.env` file (see below)

### Environment Variables

Create `.env` file in project root:

```bash
# Meta API Credentials
META_ACCESS_TOKEN=your_access_token_here
INSTAGRAM_BUSINESS_ID=your_instagram_business_id_here

# Optional: For extended access
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
```

**Never commit `.env` to git** - already in `.gitignore`

## How It Works

### Step 1: Data Collection

Fetches last 50-100 posts with metrics:
- Caption text
- Engagement (likes, comments, saves, shares)
- Reach and impressions
- Post type (carousel, single image, reel mention)
- Timestamp

### Step 2: Performance Analysis

Identifies patterns:
- **Top 10 performers** (engagement rate basis)
- **Hook patterns** (first line analysis)
- **Length correlation** (line count vs engagement)
- **CTA effectiveness** (thecoachconsultant.uk click patterns)
- **Topic themes** (what content resonates)

### Step 3: Caption Generation

Creates captions matching:
- Ben's sentence structure (one per line)
- Forbidden phrase avoidance
- British English spelling
- Natural conversational flow
- Proven hook patterns from top posts

### Step 4: Performance Prediction

Estimates likely engagement based on:
- Historical similar content performance
- Hook strength score
- Length optimization
- CTA placement
- Topic relevance

## Usage

### Generate Single Caption

```bash
# Generate caption for specific topic
Generate Instagram caption about "client onboarding automation"
```

### Generate with Performance Analysis

```bash
# Analyze past posts first, then generate
Generate Instagram caption with performance analysis about "pricing strategy"
```

### A/B Testing Variants

```bash
# Create 3 variations for testing
Generate 3 Instagram caption variants about "Meta ads for business owners"
```

### Performance Report Only

```bash
# Just show me what's working
Show Instagram performance analysis for last 50 posts
```

## Brand Voice Guardrails

### Ben's Natural Style (From Performance Data)
✅ Direct address: "You are...", "You think..."
✅ Confrontational opening: "Do you genuinely still think..."
✅ Urgency triggers: "NOT behind (yet!)", "still"
✅ Personal storytelling: "I don't really have the words..."
✅ Strong language: "fuck comparing", "stop being a victim"
✅ Short paragraphs with line breaks
✅ One powerful sentence per line

### Top Performing Hook Patterns (Proven)
🏆 **"Comment [WORD]" CTAs** - 808 engagement
🏆 **"You are NOT [belief]"** - 198 engagement
🏆 **Question hooks** - "Do you genuinely still think..."
🏆 **Quote + Context** - "Rise from the ashes..."
🏆 **Controversial statements** - "Evil has existed for 300,000 years"

### Forbidden AI Phrases
❌ "Here's the thing" / "Let's dive in"
❌ "In this comprehensive guide"
❌ "At the end of the day"
❌ "Game changer" / "Unlock" / "Leverage"
❌ Dashes or excessive punctuation
❌ Emojis, hashtags, headers (Ben never uses these)

### Format Rules
- Single short sentences, one per line
- No full stops, no headers
- Max 15-20 lines
- British English (organisation, behaviour)
- Target: business owners and service providers
- CTA: www.thecoachconsultant.uk

## Performance Metrics Tracked

### Engagement Score Formula

```
Engagement Rate = (Likes + Comments*3 + Saves*5 + Shares*7) / Reach * 100
```

**Why this weighting?**
- Comments = 3x value (actual conversation)
- Saves = 5x value (bookmarking for later)
- Shares = 7x value (amplification + endorsement)

### Top Performer Criteria

Posts ranked by:
1. Engagement rate (primary)
2. Reach (secondary)
3. Saves rate (quality signal)
4. Profile visits (conversion indicator)

## Output Format

Every generated caption includes:

```
📊 PERFORMANCE PREDICTION
Estimated engagement rate: X.X%
Based on: [similar top post reference]
Confidence: [High/Medium/Low]

📝 CAPTION
[Generated caption here]
[One sentence per line]
[Max 15-20 lines]
[CTA at end]

🎯 OPTIMIZATION NOTES
- Hook pattern: [type identified]
- Length: [X lines - optimal/too short/too long]
- CTA: [placement recommendation]
- Similar top post: [caption preview] (X.X% engagement)

💡 A/B TEST SUGGESTION
[Optional variation to test against]
```

## Files Structure

```
2-instagram/instagram-caption/
├── SKILL.md                    # This file
├── data/
│   ├── performance_data.csv    # 41 posts analyzed (scraped via Apify)
│   ├── raw_posts.json          # Full post data with comments
│   └── PERFORMANCE_INSIGHTS.md # Pattern analysis summary
├── scripts/
│   ├── analyze_patterns.py     # Performance pattern analyzer
│   └── generate_caption.py     # Caption generator (coming soon)
├── outputs/
│   └── generated_captions.md   # Caption history
└── .env.example                # Environment template
```

## Python Dependencies

```bash
pip install requests python-dotenv pandas
```

## Example Workflow

```python
# 1. Fetch latest posts
python scripts/fetch_posts.py

# 2. Analyze performance patterns
python scripts/analyze_performance.py

# 3. Generate caption with context
python scripts/generate_caption.py --topic "email marketing" --variants 3
```

## Success Metrics

Track over time:
- **Engagement rate improvement** (vs baseline)
- **Reach growth** (vs previous avg)
- **Profile visits increase** (conversion indicator)
- **CTA click rate** (thecoachconsultant.uk traffic)

## Notes

- Run performance analysis weekly to catch emerging patterns
- Test new hooks against proven winners
- Monitor competitor posts for inspiration (voice extraction only)
- Never use AI-sounding phrases - authenticity > perfection
- When in doubt, sound more human, less polished

## Related Skills

- `meta-ad-copy` - Same performance analysis for paid ads
- `youtube-scripts` - Long-form content generation
- `email-campaigns` - Newsletter writing with Ben's voice

---

**Maintained by:** Claude Code (Jay)
**Last updated:** 2026-03-24
**Version:** 1.1.0 (Real performance data integrated)
