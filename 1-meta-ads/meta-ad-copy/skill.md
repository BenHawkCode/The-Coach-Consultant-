---
name: meta-ad-copy
description: Generate performance-optimized Meta ad copy using data from 29 competitors (561 ads). Proven patterns - 60% Statement, 16% Metric/Result, 14% Question hooks. Creates variations optimized for business owners and service providers in Ben's voice with data-backed conversion strategies.
---

# Meta Ad Copy Generator

Generate high-converting Meta ad copy optimized for The Coach Consultant's target audience of business owners and service providers.

## ✅ POWERED BY COMPETITOR INTELLIGENCE
**29 Top Performers Analyzed | 561 Active Ads | March 2026**

This skill uses proven patterns from:
- Alex Hormozi, Dan Martell, Russell Brunson (Tier 1)
- Billy Gene, Molly Pittman, Cat Howell (Tier 2)
- Gary Vee, Ali Abdaal, Iman Gadzhi (Tier 3)
- Stefan Georgi, Justin Goff (Tier 4)
- UK-specific: James Sinclair, Rob Moore (Tier 5)

**Reference files:**
- `/1-meta-ads/meta-ad-competitor/outputs/CONSOLIDATED-ANALYSIS-29-COMPETITORS.md`
- `/1-meta-ads/meta-ad-competitor/outputs/TOP-50-HOOKS-SWIPE-FILE.md`

## Instructions for Claude

When this skill is invoked:

1. **MANDATORY: Ask the user for campaign details FIRST (DO NOT SKIP THIS STEP):**

   Use the AskUserQuestion tool to gather:

   **Question 0: Competitor Style (Optional)**
   - Header: "Match Competitor Style?"
   - Options:
     - "General Best Practices" (Use patterns from all 29 competitors)
     - "Alex Hormozi" (65% Metric/Result hooks, 65% Hard CTA, aggressive)
     - "Dan Martell" (55% Statement, 40% Question, 70% No CTA, conversational)
     - "Russell Brunson" (40% Statement, 30% Metric, balanced)
     - "Gary Vaynerchuk" (Statement + Story, 80% No CTA, pure value)
     - "Billy Gene" (How-To/Framework, educational, entertaining)
     - [Show all 29 if user asks]

   **If competitor selected:** Read their specific patterns from `/1-meta-ads/meta-ad-competitor/outputs/ad-library-analysis/[name]-ad-library-2026-03-24.md`

   **Question 1: Campaign Objective**
   - Header: "Campaign Goal"
   - Options:
     - "Book a Call" (Lead generation for 1-1 consultations)
     - "Webinar/Masterclass Registration" (Event sign-ups)
     - "Free Resource Download" (Lead magnet - guide, template, toolkit)
     - "Course/Product Launch" (Paid offering promotion)

   **Question 2: Target Audience Pain Point** (from new IP — May 2026)
   - Header: "Main Pain"
   - Options (ordered by hero → secondary → niche, per `docs/new-ip/06-pain-isolation.md`):
     - "Guesswork Tax" (HERO — every content/acquisition/sales decision is a guess, no AI intelligence)
     - "Bottleneck Identity" (everything runs through them, cannot step back without dropping balls)
     - "AI Era Anxiety" (knows AI is the answer, cannot tell tools from intelligence, frozen)
     - "Trust Trauma" (burnt by mentors before, frameworks just the same, debt to show for it)
     - "Plate Anxiety" (cannot add more stress to the plate, even when it would lighten it)
     - "Revenue Plateau" (£100K-£500K stuck in £8.5K-£30K monthly, should be scaling without hiring)

   **Question 3: Main Offer/Value Proposition**
   - Header: "Core Offer"
   - Text input field for user to describe the main offer (e.g., "Free 45-min strategy call to build AI-powered content system")

   **Question 4 (Optional): Additional Elements**
   - Header: "Include"
   - Multi-select options:
     - "Social Proof" (300+ business owners using frameworks)
     - "Urgency" (Limited spots, event date, bonus deadline)
     - "Specific Metrics" (10x output, 90% less time, £50K→£200K transformations)
     - "Authority Signals" (Industry recognition, case studies)

   **CRITICAL**: Do NOT generate any ad copy until ALL questions are answered. If user provides vague answers, ask follow-up clarification questions.

2. **Fetch top performing ads from Meta API:**
   ```bash
   cd 1-meta-ads/meta-ad-copy && bash setup.sh --top 10 --format json
   ```

   Note: `setup.sh` automatically handles dependencies (creates venv on first run)

3. **Analyze winning patterns (DATA-BACKED):**
   - Use competitor intelligence from `/1-meta-ads/meta-ad-competitor/outputs/`
   - Apply proven hook distribution: 60% Statement, 16% Metric/Result, 14% Question
   - Reference CTA patterns: 67% No CTA (content-first), 14% Hard CTA (conversion)
   - Extract hooks, CTAs, pain points from API data
   - Identify forbidden phrases used (to avoid)
   - Note high-CTR patterns

4. **Generate 3-5 ad copy variations using proven formulas:**

   **Formula 1: Statement Hook (59.4% success rate)**
   ```
   [Direct Value Proposition] + [Simple Process] + [Clear Outcome]
   ```
   Example: "Right so here's what I see constantly working for business owners hitting £10K months..."

   **Formula 2: Metric/Result Hook (16.2%, high conversion)**
   ```
   [Specific Number] + [Target Audience] + [Achieving Result]
   ```
   Example: "147 business owners used this system to add £5K-£15K/month in 90 days"

   **Formula 3: Question Hook (13.7%, high engagement)**
   ```
   [Relatable Situation] + [Question that triggers self-reflection]
   ```
   Example: "Why do some business owners hit £10K months while others stay stuck at £2K?"

   **Formula 4: Bold Statement Hook (3.4%, pattern interrupt)**
   ```
   [Controversial/Unexpected Statement] + [Why it matters]
   ```
   Example: "Most 'business consultants' have never built a real business. Here's the difference..."

   **Formula 5: Pain Point Hook (2.5%, problem-aware)**
   ```
   [Most people struggle with X] → [Here's the real problem] → [Solution]
   ```
   Example: "You're not failing because of effort. You're failing because of systems."

   **Apply These Rules:**
   - Ben's voice rules (British English, no AI phrases, Yorkshire tone)
   - Different hook types per variation (test multiple)
   - Character limits: Primary text <125 chars for optimal performance, Headlines 5-7 words
   - Match CTA to stage: Awareness = No CTA, Conversion = Hard CTA

5. **Output formatted markdown file:**
   - Save to `outputs/META-AD-COPY-[campaign-name].md`
   - Include performance predictions and A/B test recommendations

## Purpose

This skill generates Meta ad copy variations that:
- Align with The Coach Consultant brand voice
- Target business owners and service providers pain points and goals
- Follow Meta best practices (character limits, hooks, CTAs)
- Include A/B test variations for optimization
- Reference brand context from CLAUDE.md
- Use real-time performance data from Meta API

## Usage

### How It Works

**Step 1:** User invokes skill
```
Generate meta ad copy
```
or
```
/meta-ad-copy
```

**Step 2:** Claude asks 4 questions via AskUserQuestion tool:
1. Campaign objective (Book a Call, Webinar, Resource, Course)
2. Target pain point (Manual Overwhelm, Invisibility, AI Paralysis, Revenue Plateau)
3. Main offer description (user provides specific offer details)
4. Optional elements (Social Proof, Urgency, Metrics, Authority)

**Step 3:** Claude fetches real Meta API performance data

**Step 4:** Claude generates 3-5 ad variations optimized for selected pain point + objective

**Step 5:** Output saved to `outputs/META-AD-COPY-[campaign-name].md`

### Example User Flow

**User:** "Generate meta ad copy"

**Claude:** *[Displays AskUserQuestion with 4 questions]*

**User selects:**
- Campaign Goal: Book a Call
- Main Pain: Manual Overwhelm
- Core Offer: "Free 45-min clarity call to systematize client operations with AI"
- Include: Social Proof, Specific Metrics

**Claude:** *[Fetches API data, analyzes patterns, generates 3-5 variations matching Manual Overwhelm pain point + Book a Call objective]*

### Quick Invocation (If User Provides All Details Upfront)

If user says:
```
Generate meta ad copy for a free strategy call targeting business owners
stuck in manual overwhelm. Include social proof and metrics.
```

Claude should still use AskUserQuestion but pre-fill obvious answers and only ask for missing details.

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
- **Statement**: "Most business owners make this fatal mistake..."
- **Statistic**: "73% of business owners struggle with consistent revenue."
- **Social Proof**: "1,200+ business owners transformed their business with..."

## Brand Context Integration

The skill automatically references:

### From CLAUDE.md + new IP (`docs/new-ip/`):
- Brand voice (Yorkshire-direct, mate-to-mate, with warmth)
- Target audience: Sam — open business owners and service providers, men + women equally, 35-50 years old, £100K-£500K (high-heat zone £8.5K-£30K monthly)
- Hero pain: Guesswork Tax (every growth decision is a guess)
- Secondary pain: Bottleneck Identity (everything runs through them)
- Goals: Predictability (the new growth metric), AI intelligence behind every decision, personal brand defence in AI era
- Differentiation: AI intelligence (NOT AI tools), done-with-you delivery, 4-step programme (Audit → Setup → Roadmap → 90-Day Growth Map)

### Ben's Voice Rules (CRITICAL — see CLAUDE.md for full list):

**Forbidden AI Phrases (NEVER USE):**
- "Here's the thing" / "Let's dive in" / "Dive in"
- "Transformation journey" / "Journey" / "Unlock" / "Level up"
- "Game changer" / "Game-changing" / "Ground-breaking"
- "In this comprehensive guide" / "In conclusion"
- Em-dashes / en-dashes
- Gendered defaults ("the bloke", "the guy", "him")

**Ben's Natural Phrases (USE THESE):**
- "Right, so..." (to start explanations)
- "Look, here's the thing..." / "Mate, the truth is..."
- "Doing my head in..."
- "Proper" (as adverb)

**New IP signature phrases (USE OFTEN — these are the spine):**
- "You are the bottleneck of your business"
- "Stop guessing growth"
- "AI intelligence, not AI tools"
- "Personal brand plus AI adoption"
- "Done-with-you, not done-by-yourself, not done-to-you"
- "Built for you, used by you, owned by you"
- "Frameworks just the same"
- "Replace £100K+/month in staff wages with copy-paste SOPs"
- "Predictability is the new growth metric"

**Tone & Style:**
- British English always (£, organisation, optimise, behaviour)
- Always say "business owners and service providers" (NEVER say "coaches")
- Direct, straight-talking, Yorkshire influence
- Short punchy sentences
- No dashes or excessive punctuation (sounds robotic)
- No corporate fluff or buzzwords
- Authority through personal experience (not theory)
- Sound human, not AI

### Language Preferences:
- UK English (£, programme, optimise)
- Direct, value-the-reader's-time approach
- "You" focused (speak directly to business owners)
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
Audience: Solo business owners, £50K-£200K revenue, struggling with consistent client flow

---

## Variation 1: Pain Point Question

**Primary Text**
Sound familiar? Feast or famine client flow. Most business owners waste £1000s on ads that don't work. The 3-step system 1,200+ use.

**Headline**
Predictable Client Flow for Business Owners

**Description**
Free masterclass - March 15

**Call-to-Action**
Register Now

---

**Performance Notes:**
- Hook type: Question (pain point)
- Pain point: Inconsistent revenue, ad waste
- Urgency: Event date (March 15)
- Social proof: 1,200+ business owners
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
3. **Social Proof Elements**: "1,200+ business owners" vs. "Featured in..." vs. Testimonial quote
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
cd 1-meta-ads/meta-ad-copy && bash setup.sh --top 10 --format json
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
- "Business owners and service providers" (NEVER say "coaches")
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
