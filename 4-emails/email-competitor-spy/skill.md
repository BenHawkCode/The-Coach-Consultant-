---
name: email-competitor-spy
description: Analyse competitor email newsletters to extract hook patterns, subject line formulas, CTA strategies, tone profiles, and offer positioning. Uses data from Antonio's scraping pipeline (competitor_newsletters.json). Produces a combined intelligence report with actionable patterns Ben can apply to his own email campaigns. Triggers on "spy on emails", "analyse competitor emails", "email competitor analysis", or /email-competitor-spy.
---

# Email Competitor Spy - Newsletter Intelligence

## Purpose

Analyse competitor email newsletters scraped by Antonio's pipeline to extract winning patterns: subject line formulas, hook styles, CTA strategies, tone profiles, offer positioning, and sending frequency. Produces a single intelligence report that feeds directly into Ben's email campaign skill.

## Data Source

**Primary:** `4-emails/email-competitor-spy/data/competitor_newsletters.json`
- Scraped and maintained by Antonio's pipeline (auto-updated weekly)
- Currently tracking 10 senders, 18 newsletters
- Each entry includes: sender, platform, frequency, subject, hook, body excerpt, CTA, offer, tone, format, key_pattern

**To refresh data:** Antonio's pipeline auto-commits updates to `competitor_newsletters.json`. Pull latest from the shared repo.

## When to Use

- User wants to analyse competitor email strategies
- "Spy on competitor emails"
- "What are competitors doing in email?"
- "Analyse [sender name]'s newsletter"
- "What hooks are working in email right now?"
- Before writing a new email campaign (competitive context)
- Comparing Ben's email performance against competitors

## Workflow

### Step 1: Load Competitor Data

Read the competitor newsletter data:

```bash
cd /Users/learnai/Desktop/The\ Coach\ Consultant/4-emails/email-competitor-spy
python analyze_competitors.py
```

Or read the JSON directly:
```
4-emails/email-competitor-spy/data/competitor_newsletters.json
```

### Step 2: Ask What They Want

Use AskUserQuestion to determine scope:

**Question 1: Analysis Scope**
- "All competitors" (full landscape report)
- "Specific sender" (deep dive on one competitor)
- "Pattern focus" (hooks only, CTAs only, subject lines only)

**Question 2: Purpose**
- "Campaign inspiration" (feed into email-campaign skill)
- "Competitive intelligence" (understand landscape)
- "Subject line ideas" (focus on open rate patterns)
- "CTA strategies" (focus on conversion patterns)

### Step 3: Run Analysis

Execute the analysis script:

```bash
python analyze_competitors.py --scope all --output report
```

Or for a specific sender:
```bash
python analyze_competitors.py --sender "Alex Hormozi"
```

### Step 4: Present Intelligence Report

Generate a structured report covering:

1. **Sender Landscape** - who's sending, how often, what platforms
2. **Subject Line Patterns** - formulas that work, length analysis, punctuation patterns
3. **Hook Analysis** - opening styles ranked by pattern type
4. **CTA Strategy** - hard sell vs soft sell vs no CTA distribution
5. **Offer Positioning** - what they sell and how they position it
6. **Tone Profiles** - voice characteristics per sender
7. **Key Patterns for Ben** - actionable takeaways mapped to Ben's voice

## Report Sections

| # | Section | What it Covers |
|---|---------|---------------|
| 1 | Competitor Overview | 10 senders, platforms, frequency, positioning |
| 2 | Subject Line Formulas | Pattern types, length, punctuation, capitalisation |
| 3 | Hook Pattern Analysis | Opening styles: story, contrarian, pain, curiosity, value |
| 4 | CTA Distribution | Hard CTA / Soft CTA / Reply CTA / No CTA breakdown |
| 5 | Offer Positioning | Free value vs product pitch vs agency vs event |
| 6 | Tone & Voice Profiles | Per-sender voice characteristics |
| 7 | Sending Frequency & Schedule | Daily/weekly/2-3x patterns, day-of-week trends |
| 8 | Top Patterns for Ben | 7 actionable recommendations in Ben's voice |

## Pattern Classification

### Subject Line Types
- **Curiosity Gap**: "it was a lie, but it worked" (Dan Martell)
- **Metric/Result**: "700% more email revenue" (Ezra Firestone)
- **Named Format**: "Mozi Minute:" prefix (Alex Hormozi), "3MM:" (Chris Williamson)
- **Contrarian**: "You can only be CEO alone" (Alex Hormozi)
- **Question**: "You get automation stuff you asked for?" (Frank Kern)
- **Pain Point**: "you're closer than you think" (Dan Martell)
- **Bold Statement**: "The $0 habit that can make you a millionaire" (Tony Robbins)

### Hook Types
- **Contrarian Opening**: Challenge a common belief immediately
- **Story Hook**: Start with a personal narrative
- **Pain Paint**: Describe the reader's current struggle
- **Value Drop**: Lead with the insight upfront
- **Pattern Interrupt**: Break expected email format
- **Curiosity Tease**: Open a loop that demands reading on

### CTA Types
- **Reply CTA**: "Reply COACH" (Dan Martell) - one word trigger
- **Link CTA**: Direct link to offer/resource
- **Multi-Platform**: YouTube / Spotify / Apple (Andrew & Pete, Chris Williamson)
- **PS Sell**: Main email is value, offer hidden in PS
- **No CTA**: Pure value, no ask (Alex Hormozi, James Sinclair)

## Integration with Email Campaign Skill

This skill feeds directly into `email-campaign-ben-hawksworth`:

1. Run email-competitor-spy to identify winning patterns
2. Select patterns that align with Ben's voice
3. Feed selected patterns into email campaign generation
4. The campaign skill applies Ben's voice rules on top

**Example flow:**
```
/email-competitor-spy → identifies "Reply CTA" pattern from Dan Martell
→ /email-campaign → generates Ben's version: "Reply READY and I'll send you the framework"
```

## Competitor Profiles (Current Data)

| Sender | Platform | Frequency | Style |
|--------|----------|-----------|-------|
| Alex Hormozi | HubSpot | 2-3x/week | Short, punchy, pure value |
| Dan Martell | GoHighLevel | Daily (M-F) | Motivational + urgency sells |
| Andrew & Pete | ActiveCampaign | Daily | Fun, British, YouTube funnel |
| Ezra Firestone | Klaviyo | Daily | Data-driven, agency pitch |
| Molly Pittman | Klaviyo | 1-2x/week | Welcome sequences, free products |
| James Sinclair | Squarespace | Weekly (Mon) | British storytelling, long-form |
| Chris Williamson | ConvertKit | Weekly (Mon) | Intellectual, curated format |
| Frank Kern | Custom (GHL) | 2-3x/week | Ultra-casual, affiliate |
| Tony Robbins | HubSpot | Weekly (Sun) | Inspirational, multi-CTA funnel |
| Leila Hormozi | beehiiv | Weekly | CEO memo style, systems thinking |

## Output

Reports saved to:
```
4-emails/email-competitor-spy/outputs/EMAIL-SPY-REPORT-[YYYY-MM-DD].md
```

## Ben's Voice Application

When mapping competitor patterns to Ben's voice, always apply:

- British English (organisation, behaviour, colour)
- "business owners and service providers" (NEVER say "coaches")
- Ben's natural phrases: "Right so", "Sound familiar", "The thing is"
- No forbidden AI phrases
- One sentence per line
- Soft reply CTAs (CHAT, CONNECT, START, READY)
- Sign off: Ben + www.thecoachconsultant.uk
