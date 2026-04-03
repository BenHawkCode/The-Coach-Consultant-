# Meta Page Spy - Design Spec

**Date:** 2026-04-01
**Status:** Approved
**Approach:** A - Single script, sequential execution

---

## Purpose

Spy on any Facebook page: scrape organic posts + paid ads from Ad Library, produce a single combined intelligence report with posting frequency, content types, engagement metrics, hook/CTA patterns, posting schedule, and offer positioning.

## Scope

- Single page analysis per run (no multi-page comparison)
- Organic side: posting frequency, content type breakdown, engagement metrics (top 10), hook patterns, CTA patterns, posting schedule
- Paid side: hook/CTA patterns from ads, offer positioning
- Excluded from paid: active ad count, longest-running ads ranking

## Folder Structure

```
1-meta-ads/meta-page-spy/
├── skill.md              # Claude Code skill definition
├── page_spy.py           # Main scraper + analysis script
└── outputs/              # Reports saved here
    └── .gitkeep
```

## Trigger & Flow

### Triggers
- `/meta-page-spy`
- "spy on [page name]"
- "analyze [page name] Facebook page"
- "what is [page name] doing on Facebook"

### Workflow
1. User triggers skill
2. Claude asks: "Which Facebook page do you want to spy on? Give me the URL or page name."
3. User provides URL or name
4. Claude runs `page_spy.py` with the page URL/name
5. Script executes two Apify actors sequentially:
   - Phase 1: `apify/facebook-posts-scraper` - organic posts (50 posts default)
   - Phase 2: `curious_coder/facebook-ads-library-scraper` - paid ads (20 ads default)
   - Phase 3: Combined analysis + report generation
6. Report saved to `outputs/[page-name]-[YYYY-MM-DD].md`
7. Claude presents key findings summary to user

## Report Structure

```markdown
# [Page Name] - Meta Page Spy Report

**Date:** YYYY-MM-DD
**Page URL:** https://facebook.com/...
**Posts Analyzed:** X organic | Y paid ads

---

## 1. Posting Frequency
- Posts per week (average over analyzed period)
- Posts per month
- Trend indication (increasing/decreasing/stable)

## 2. Content Type Breakdown
- Video: X% (N posts)
- Image: X% (N posts)
- Text: X% (N posts)
- Reel: X% (N posts)
- Carousel/Album: X% (N posts)
- Link: X% (N posts)

## 3. Top 10 Posts by Engagement
For each post:
- Opening line (first 125 chars)
- Full text (truncated at 500 chars)
- Reactions / Comments / Shares
- Engagement score
- Content type
- Post URL

## 4. Hook Pattern Analysis (Organic)
- Hook type distribution with percentages
- Highest engagement hook type
- Examples from top posts

## 5. CTA Pattern Analysis (Organic)
- CTA style distribution (Hard, Soft, Engagement, None)
- Most used CTA type

## 6. Posting Schedule
- Day-of-week breakdown (Mon-Sun post counts)
- Time-of-day if available from scraper data

## 7. Paid Ads - Hook & CTA Patterns
- Hook type distribution from ads
- CTA style distribution from ads
- Top hook examples

## 8. Paid Ads - Offer Positioning
- What they're selling (lead magnet, course, call, etc.)
- Link captions
- CTA button texts
- Common offer types

## 9. Key Takeaways
- 5-7 bullet points
- Actionable insights for Ben's content strategy
```

## Technical Details

### Apify Actors
- **Organic:** `apify/facebook-posts-scraper`
  - Input: `startUrls` with page URL, `resultsLimit: 50`
  - Output: posts with text, reactions, comments, shares, type, time
- **Paid:** `curious_coder/facebook-ads-library-scraper`
  - Input: Ad Library search URL with page name
  - Output: ads with snapshot.body.text, start_date, platforms, cta_text

### Configuration
- `APIFY_API_TOKEN` from `.env` file (existing pattern from project root)
- Default: 50 organic posts, 20 paid ads
- 5-second pause between the two scraper runs

### Hook Classification (same logic, fresh implementation)
- Question: `?` in first 125 chars
- Pain Point: struggling, problem, frustrated, stuck, tired of, stop
- Metric/Result: digits + money/percentage keywords
- Bold Statement: secret, hidden, nobody, most people, truth
- Story: when i, i was, my first, back in, i remember
- How-To/Framework: how to, here's how, 3 ways, 5 steps, framework
- Statement: default fallback

### CTA Classification
- Hard CTA: book a call, sign up, download, register, apply now, get started, click the link, link in bio, dm me
- Soft CTA: learn more, discover, find out, see how, what do you think, let me know, thoughts?
- Engagement CTA: comment, tag, share, save this, drop a
- No CTA: default fallback

### Engagement Score Formula
```
engagement_score = reactions + (comments * 2) + (shares * 3)
```
Comments weighted 2x (higher intent), shares weighted 3x (highest distribution value).

### Posting Frequency Calculation
- Parse post dates from scraper output
- Group by week/month
- Calculate average posts per week and per month

### Posting Schedule Calculation
- Extract day-of-week from post timestamps
- Count posts per day (Mon=0 through Sun=6)
- Extract hour if timestamp granularity allows

## Integration Points

### Files to Update After Implementation
- `CLAUDE.md` - Add Meta Page Spy to channel rules section
- `SKILLS-README.md` - Add to Meta Ads section

### skill.md Format
Follow existing skill format from `4-emails/email-campaign-skill/skill.md`:
- Frontmatter with name + description
- When to use
- Workflow steps
- Output format
- Dependencies

### Dependencies
- Python 3.x
- `apify_client` library (already installed in project)
- `APIFY_API_TOKEN` in `.env` (already exists)
