---
name: meta-ad-copy
description: Generate performance-optimized Meta ad copy for The Coach Consultant based on brand voice, target audience, and campaign objectives. Creates multiple variations with headlines, primary text, and CTAs optimized for coaches and consultants.
---

# Meta Ad Copy Generator

Generate high-converting Meta ad copy optimized for The Coach Consultant's target audience of coaches and consultants.

## Instructions for Claude

When this skill is invoked:

1. **Ask the user for campaign details:**
   - Campaign objective (e.g., "Webinar registration", "Free resource download", "Book a call")
   - Target audience (e.g., "Solo coaches £50K-£150K revenue struggling with client acquisition")
   - Main offer/hook (e.g., "Free masterclass on AI for coaches")
   - Optional: Tone modifier, urgency element, social proof

2. **Fetch top performing ads from Meta API:**
   ```bash
   cd skills/meta-ad-copy && bash setup.sh --top 10 --format json
   ```

   Note: `setup.sh` automatically handles dependencies (creates venv on first run)

3. **Analyze winning patterns:**
   - Extract hooks, CTAs, pain points from API data
   - Identify forbidden phrases used (to avoid)
   - Note high-CTR patterns

4. **Generate 3-5 ad copy variations:**
   - Use proven patterns from API data
   - Apply Ben's voice rules (British English, no AI phrases, Yorkshire tone)
   - Different hook types (question, statement, statistic)
   - Character limits: Primary text <125 chars, Headlines 5-7 words

5. **Output formatted markdown file:**
   - Save to `outputs/META-AD-COPY-[campaign-name].md`
   - Include performance predictions and A/B test recommendations

## Purpose

This skill generates Meta ad copy variations that:
- Align with The Coach Consultant brand voice
- Target coaches/consultants pain points and goals
- Follow Meta best practices (character limits, hooks, CTAs)
- Include A/B test variations for optimization
- Reference brand context from CLAUDE.md
- Use real-time performance data from Meta API

## Usage

### Basic Usage
```
Generate meta ad copy for [campaign objective]
Target: [audience segment]
Offer: [main offer/hook]
```

### Advanced Usage
```
Create 3 meta ad variations for:
- Campaign: New course launch
- Audience: Solo coaches struggling with client acquisition
- Offer: Free masterclass on predictable client flow
- Tone: Professional but supportive
- Include: Social proof, urgency
```

## Required Inputs

1. **Campaign Objective**
   - Lead generation
   - Course/product launch
   - Event registration
   - Free resource download
   - Consultation booking

2. **Target Audience**
   - Business stage (revenue, team size)
   - Main pain point
   - Coaching niche (if specific)

3. **Main Offer/Hook**
   - What you're promoting
   - Key benefit
   - Call-to-action

## Optional Inputs

- **Tone modifier**: More formal / More casual
- **Elements to include**: Social proof, urgency, stats, testimonials
- **Competitor differentiation**: What makes this unique
- **Budget range**: For context on offer positioning

## Output Format

The skill generates:

### META-AD-COPY-[CAMPAIGN].md

For each variation:

```markdown
## Variation 1: [Hook Type]

**Primary Text** (125 chars max)
[Pain point or opportunity-focused opening]

**Headline** (5-7 words, benefit-focused)
[Clear value proposition]

**Description** (Optional, 27 chars)
[Supporting detail or urgency element]

**Call-to-Action**
[Specific action: Book a Call, Download Guide, Register Now, etc.]

---

**Performance Notes:**
- Hook type: [Question / Statement / Statistic]
- Pain point addressed: [Specific pain]
- Urgency element: [Yes/No - what type]
- Social proof: [Yes/No - what type]

**A/B Test Recommendation:**
Test against Variation [X] to compare [hook type] vs [alternative]
```

## Meta Best Practices (Built-in)

### Character Limits
- **Primary Text**: 125 characters optimal (before "see more")
- **Headline**: 5-7 words, benefit-focused
- **Description**: 27 characters (optional)
- **CTA**: Standard Meta buttons (Book Now, Learn More, Download, etc.)

### Copy Structure
1. **Hook** (First line): Pain point, question, or bold statement
2. **Value Prop** (Middle): What they get, why it matters
3. **CTA** (End): Clear next step with urgency/benefit

### Hook Types
- **Question**: "Tired of feast-or-famine client flow?"
- **Statement**: "Most coaches make this fatal mistake..."
- **Statistic**: "73% of coaches struggle with consistent revenue."
- **Social Proof**: "1,200+ coaches transformed their business with..."

## Brand Context Integration

The skill automatically references:

### From CLAUDE.md:
- Brand voice (Professional, Direct, Supportive, Action-oriented)
- Target audience (Coaches, consultants, and service providers - £50K-£150K revenue, 28-35 years old)
- Pain points (Inconsistent client flow, marketing doesn't convert, etc.)
- Goals (Predictable acquisition, higher conversion, automated systems)
- Differentiation (Tech-forward AI automation, implementation support)

### Ben's Voice Rules (CRITICAL):

**Forbidden AI Phrases (NEVER USE):**
- "Here's the thing" / "Here's the reality" / "Here's how"
- "Let's dive in"
- "In this comprehensive guide"
- "It's important to note"
- "At the end of the day"
- "In conclusion" / "To summarise"
- "First and foremost"
- "Game changer" / "Unlock" / "Leverage" / "Journey"

**Ben's Natural Phrases (USE THESE):**
- "Right so" (to start explanations)
- "Sound familiar"
- "The shift is simple"
- "The problem is"
- "What actually works"
- "That's how you"
- "I see this constantly" / "I see this all the time"
- "Remember"
- "The thing is"

**Tone & Style:**
- British English always (£, organisation, optimise, behaviour)
- Always say "coaches, consultants and service providers" (not just "coaches")
- Direct, straight-talking, Yorkshire influence
- Short punchy sentences
- No dashes or excessive punctuation (sounds robotic)
- No corporate fluff or buzzwords
- Authority through personal experience (not theory)
- Sound human, not AI

### Language Preferences:
- UK English (£, programme, optimise)
- Direct, value-the-reader's-time approach
- "You" focused (speak directly to coaches)
- Specific numbers and metrics when available
- Real examples over theory

## Performance Scoring

Each variation includes:

| Element | Score | Notes |
|---------|-------|-------|
| Hook Strength | ✅ Pass / ⚠️ Warning / ❌ Fail | Clarity, pain-point relevance |
| Benefit Clarity | ✅ Pass / ⚠️ Warning / ❌ Fail | Is value proposition clear? |
| CTA Strength | ✅ Pass / ⚠️ Warning / ❌ Fail | Specific, urgent, benefit-driven? |
| Brand Alignment | ✅ Pass / ⚠️ Warning / ❌ Fail | Matches voice/tone guidelines |
| Character Limits | ✅ Pass / ⚠️ Warning / ❌ Fail | Within Meta optimal ranges |

**Overall Score**: 0-100 (weighted average)

## Example Output

```markdown
# Meta Ad Copy - Client Acquisition Masterclass

Generated: 2026-03-09
Campaign: Free Masterclass Registration
Audience: Solo coaches, £50K-£200K revenue, struggling with consistent client flow

---

## Variation 1: Pain Point Question

**Primary Text**
Sound familiar? Feast or famine client flow. Most coaches waste £1000s on ads that don't work. The 3-step system 1,200+ use.

**Headline**
Predictable Client Flow for Coaches

**Description**
Free masterclass - March 15

**Call-to-Action**
Register Now

---

**Performance Notes:**
- Hook type: Question (pain point)
- Pain point: Inconsistent revenue, ad waste
- Urgency: Event date (March 15)
- Social proof: 1,200+ coaches
- Differentiation: 3-step system (specific)

**A/B Test Recommendation:**
Test against Variation 2 (Statistic hook) to compare emotional vs. data-driven appeal.

**Score Breakdown:**
- Hook Strength: ✅ Pass (8/10) - Clear pain point, relatable question
- Benefit Clarity: ✅ Pass (9/10) - "Predictable client flow" is specific
- CTA Strength: ✅ Pass (8/10) - Clear action, tied to urgency
- Brand Alignment: ✅ Pass (9/10) - Supportive, action-oriented, data-backed
- Character Limits: ✅ Pass (10/10) - 118 chars (optimal range)

**Overall Score: 88/100** (Grade: B+)
```

## Customization with Client Data

When Rob provides:

### Meta Ad Performance Data:
- Top performing ads (copy + metrics)
- Worst performing ads (to avoid patterns)
- Audience segments and targeting
- Historical CTR, conversion rates

**The skill will**:
1. Analyze winning patterns (hooks, CTAs, length)
2. Identify fatigue indicators (declining CTR)
3. Suggest refresh cadence based on performance
4. Generate copy variations matching proven patterns

### Brand Voice Examples:
- Existing ad copy, emails, social posts
- Blog content, course descriptions
- Client testimonials, case studies

**The skill will**:
1. Extract tone patterns and vocabulary
2. Match sentence structure and pacing
3. Replicate successful messaging angles
4. Maintain authentic brand voice

## Quick Wins (Before Client Data)

Based on industry best practices:

1. **Test Multiple Hooks**: Question vs. Statement vs. Statistic
2. **Vary CTAs**: "Book a Call" vs. "Download Guide" vs. "Watch Masterclass"
3. **Social Proof Elements**: "1,200+ coaches" vs. "Featured in..." vs. Testimonial quote
4. **Urgency Types**: Event date vs. Limited spots vs. Bonus deadline
5. **Benefit Framing**: Problem-solution vs. Transformation vs. System/framework

## Files Generated

- `META-AD-COPY-[CAMPAIGN].md` - Full copy variations with scoring
- `AD-PERFORMANCE-NOTES.md` - Recommendations and A/B test strategy (optional)

## Integration with Agents

This skill can be enhanced by:

1. **Research Agent**: Analyze competitor ads, identify trends
2. **Fact-Check Agent**: Verify any stats or claims used
3. **Tone Agent**: Ensure brand voice consistency
4. **Conversion Agent**: Optimize hooks and CTAs for performance

See `/agents/` for multi-agent orchestration setup.

## Best Practices

### Do:
✅ Lead with pain point or opportunity
✅ Include specific metrics when available (£, %, #)
✅ Use UK English for The Coach Consultant
✅ Keep primary text under 125 characters
✅ Make CTA specific and benefit-driven
✅ Include urgency or scarcity elements
✅ Reference real results or social proof

### Don't:
❌ Use generic hooks ("Are you ready to...")
❌ Exceed character limits (hurts mobile display)
❌ Mix US/UK English
❌ Make unverifiable claims
❌ Use jargon or buzzwords
❌ Copy competitor ads verbatim
❌ Forget mobile-first formatting

## Updates & Optimization

This skill will be updated when:
- Rob provides actual ad performance data
- New high-performing patterns emerge
- Meta best practices change
- Brand voice guidelines are refined
- New target audience segments added

Current version: **v2.0 (Live API Integration)**
- ✅ Real-time Meta API data fetching
- ✅ Ben's voice rules integrated
- ✅ Top performer analysis (automatic)
- ✅ Winning patterns extraction
- ✅ British English + Yorkshire tone

## Using This Skill

When invoked, this skill automatically:

**Step 1: Fetch real-time ad performance**
```bash
cd skills/meta-ad-copy && bash setup.sh --top 10 --format json
```
Returns top 10 performing Coach Consultant ads with:
- Full ad copy (title, body)
- Performance metrics (clicks, CTR, spend, impressions)
- Filtered for Coach Consultant keywords only

**Step 2: Analyze winning patterns**
Extract from API data:
- Hooks (pain point, question, statistic, bold statement)
- High-CTR headlines (what works)
- Proven CTAs ("Book a call", "Register now", etc.)
- Metrics usage (%, £, numbers)
- **Forbidden phrases to avoid** ("Unlock", "Leverage", "10×")

**Step 3: Generate new variations**
Apply Ben's voice rules:
- Replace forbidden phrases → Ben's natural phrases
- British English (£, organisation, optimise)
- Short punchy sentences (no dashes)
- "Coaches, consultants and service providers" (not just "coaches")
- Direct, Yorkshire straight-talking tone

**Step 4: Output formatted copy**
Generate 3-5 variations with:
- Performance predictions (based on similar patterns)
- A/B test recommendations
- Character limit compliance (125 chars primary text)
- Scoring (Hook Strength, CTA Quality, Brand Alignment)

## Script Details

**fetch_meta_ads.py** (included in this skill folder)

**Filter logic:**
- Keywords: `coach`, `consultant`, `service provider`, `business owner`, `bof`, `masterclass`, `strategies`
- Only returns ads matching these keywords (Coach Consultant ads only)
- Performance required: `clicks > 0`

**Usage options:**
```bash
# Top 10 by clicks
bash setup.sh --top 10

# Top 5 by CTR
bash setup.sh --top 5 --sort ctr

# Last 90 days only
bash setup.sh --days 90

# JSON output (for parsing)
bash setup.sh --format json
```

**Note:** `setup.sh` automatically creates a virtual environment and installs dependencies on first run. Subsequent runs use the existing environment.
