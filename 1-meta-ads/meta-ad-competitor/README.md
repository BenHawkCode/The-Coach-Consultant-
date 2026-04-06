# Meta Ad Competitor Analysis Skill

## Overview
Analyze competitor Meta ads from top performers in the coaching/business space, extract winning hooks and creative patterns, and generate hybrid ad variations combining competitor insights with The Coach Consultant's proven patterns—all in Ben's voice.

## Status
⏳ **Awaiting Meta Ad Library API Access**

Currently waiting for Meta to approve Ad Library API access. Once approved, this skill will be fully operational.

## What This Skill Does

### Input
1. Competitor name (from 31-name swipe list or custom)
2. Campaign objective (Lead Gen, Webinar, Course, etc.)
3. Your offer (to adapt competitor hooks to your context)

### Process
1. Pulls competitor's active Meta ads via Ad Library API
2. Pulls your own top-performing ads via Marketing API
3. Extracts 7 key elements from each ad:
   - Hook type
   - Opening line (first 125 chars)
   - Creative format
   - CTA style
   - Offer positioning
   - Emotional trigger
   - Run duration (performance proxy)

### Output
Markdown report with 4 sections:
1. **Competitor's Top 10 Ads** (sorted by run duration)
2. **Hook Pattern Analysis** (what's working for them)
3. **Your Top-Performing Ads** (for comparison)
4. **Hybrid Approach** (recommendations for combining insights)

## Files Structure

```
meta-ad-competitor/
├── README.md                  # This file
├── skill.md                   # Skill definition and triggers
├── system-prompt.md           # Agent instructions
├── competitor-list.md         # 31-name swipe list
├── analyze_competitor.py      # Python script (API integration)
└── outputs/                   # Generated reports saved here
```

## Usage

### Via Slash Command
```bash
/meta-ad-competitor
```

### Via Natural Language
- "Analyze Alex Hormozi's Meta ads"
- "What is Dan Martell doing on Facebook ads"
- "I want to use meta-ad-competitor skill for Russell Brunson"

### Direct Script Usage (Advanced)
```bash
cd 1-meta-ads/meta-ad-competitor
python analyze_competitor.py "Alex Hormozi" "lead generation" "Free Coaching Scorecard"
```

## Example Workflow

**Step 1: User triggers skill**
```
User: "Analyze what Alex Hormozi is doing for lead gen campaigns"
```

**Step 2: Agent asks clarifying questions**
```
Agent: "Right, analysing Alex Hormozi's Meta ads. Quick questions:
1. What offer are you promoting? (This helps me adapt his hooks to your context)"
```

**Step 3: User provides context**
```
User: "My free coaching scorecard"
```

**Step 4: Agent pulls data & generates report**
```
Agent: "Perfect. Pulling Alex's active lead gen ads + your top performers. This'll take about 30 seconds..."

[Generates report with competitor analysis + your data + recommendations]

Agent: "Done. Report saved to outputs/alex-hormozi-2026-03-19-analysis.md

Key findings:
- Alex is crushing it with metric-led hooks (70% of his ads)
- His average ad runs 45+ days (yours average 12 days)
- Generated recommendations for 5 hybrid variations

Check the report for full details."
```

## Prerequisites

### 1. Meta Ad Library API Access (REQUIRED)
**Status:** ⏳ Pending approval

**How to apply:**
1. Go to developers.facebook.com/apps
2. Open App ID: `2652379865148307`
3. Navigate to "Use cases" or "App Review"
4. Request "Ads Library API" permission
5. Justification: "Competitor research and market analysis for advertising strategy"

**Expected approval time:** 3-7 days

### 2. Environment Variables (CONFIGURED ✅)
Already set in `.env`:
- `META_ACCESS_TOKEN` ✅
- `META_APP_ID` ✅
- `META_APP_SECRET` ✅
- `META_ACCOUNT_ID` ✅

### 3. Python Dependencies
```bash
pip install requests
```

## Competitor Swipe List (31 Total)

**Tier 1:** Alex Hormozi, Dan Martell, Russell Brunson, Sam Ovens, Frank Kern, Myron Golden, Leila Hormozi, Pedro Adao, Brendon Burchard, Tony Robbins

**Tier 2:** Billy Gene Shaw, Molly Pittman, Cat Howell, Nick Shackelford, Khalid Hamadeh, Andrew Hubbard, Depesh Mandalia

**Tier 3:** Gary Vaynerchuk, Hormozi Media Team, Chris Williamson, Steven Bartlett, Ali Abdaal, Iman Gadzhi

**Tier 4:** Stefan Georgi, Justin Goff, Dara Denney, Barry Hott, Sarah Levinger

**Tier 5:** Andrew & Pete, Rob Moore, James Sinclair

Full details in [competitor-list.md](competitor-list.md)

## API Rate Limits
- **Meta Ad Library API:** 200 calls/hour
- **Meta Marketing API:** Account-dependent

Script includes 1-second delays between batch requests to prevent rate limiting.

## Output Example

```markdown
# Meta Ad Analysis: Alex Hormozi

**Date:** 2026-03-19
**Campaign Objective:** Lead Generation
**Your Offer:** Free Coaching Scorecard

---

## Section 1: Alex Hormozi's Top Ads

### Ad #1 - Metric/Result | Running 67 days

**Opening Line:**
I added £127K in 90 days using this simple lead gen system...

**Full Ad Copy:**
[Full competitor ad copy]

**Ad Library Link:** [URL]

---

[9 more competitor ads]

---

## Section 2: Hook Pattern Analysis

### Most Common Hook Types
Metric/Result: 70% (7 ads)
Pain Point: 20% (2 ads)
Question: 10% (1 ad)

### Key Insights
- Average ad run duration: 45 days
- Most successful hook type: Metric/Result
- Total active ads analyzed: 50

---

## Section 3: Your Top-Performing Ads (Lead Generation)

[Your ads with performance data]

---

## Section 4: Hybrid Approach - Recommendations

[Strategic recommendations for combining insights]
```

## Next Steps (Once API Approved)

1. ✅ Skill structure built
2. ⏳ Waiting for API approval
3. ⏸️ Test with live competitor data
4. ⏸️ Refine hook classification logic
5. ⏸️ Add full ad variation generation (integrate with meta-ad-copy skill)

## Integration with Other Skills

This skill is designed to work alongside:
- **meta-ad-copy**: Generate full ad variations based on competitor insights
- **instagram-caption**: Adapt competitor hooks for Instagram
- **Future skills**: Email campaigns, YouTube scripts, etc.

## Technical Notes

### Market Focus
- Primary: UK (GB) - Ben's home market
- Secondary: US, AU
- Currency: GBP (£) not USD ($)

### Data Freshness
- Competitor ads: Live/current (updated when API is called)
- Your ads: Last 90 days
- Performance metrics: Daily updates from Meta

### Hook Classification Logic
The script automatically classifies hooks into 6 types:
1. **Pain Point** - "Struggling with X?"
2. **Metric/Result** - "I added £50K in 90 days"
3. **Question** - "Want to know how?"
4. **Bold Statement** - "Most business owners are doing this wrong"
5. **Story** - "When I first started..."
6. **Statement** - General statements

## Troubleshooting

### "Application does not have permission for this action"
**Cause:** Ad Library API not yet approved
**Solution:** Complete API approval process (see Prerequisites)

### "No ads found for [competitor]"
**Cause:** Competitor may not be running ads in GB/US/AU markets, or search term doesn't match page name
**Solution:** Try alternative spellings or company/page name instead

### "No matching campaigns found in your account"
**Cause:** No ads in your account match the specified objective
**Solution:** Try a different objective, or review competitor-only analysis

## Support
For issues or questions about this skill, contact Jay or reference:
- [system-prompt.md](system-prompt.md) for agent behavior
- [skill.md](skill.md) for triggers and workflow
- [competitor-list.md](competitor-list.md) for full swipe file

---

*Skill created: 2026-03-19*
*Status: Awaiting API approval*
*Ready to deploy once Meta Ad Library API access is granted*
