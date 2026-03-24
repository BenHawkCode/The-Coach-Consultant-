# Meta Ad Copy Prompts

**5 prompts for the `/meta-ad-copy` skill**

Each prompt uses the skill's **actual features** (4-question flow, API data, 3-5 variations, Ben's voice).

---

## Quick Reference

| # | Prompt | What It Does | When to Use |
|---|--------|--------------|-------------|
| 01 | Basic Generation | Standard workflow - 4 questions, get variations | First time, standard campaigns |
| 02 | Manual Overwhelm Campaign | Target coaches drowning in admin | Pain: Time waste, 60% admin work |
| 03 | Invisibility Campaign | Target brilliant but invisible coaches | Pain: Zero visibility, 100% referrals |
| 04 | Webinar Registration | Generate event promo copy | Campaign goal: Event sign-ups |
| 05 | API Data Analysis First | Analyze patterns before generating | Data-driven decisions, strategy planning |

---

## Skill Features (What's Actually Supported)

✅ **4-Question Flow:**
- Campaign Goal (Book Call / Webinar / Resource / Course)
- Pain Point (Manual Overwhelm / Invisibility / AI Paralysis / Revenue Plateau)
- Core Offer (your specific offer)
- Optional Elements (Social Proof / Urgency / Metrics / Authority)

✅ **Meta API Integration:**
- Fetches top 10 performing ads
- Analyzes winning patterns (hooks, CTAs, metrics)
- Identifies high-CTR headlines

✅ **3-5 Variations:**
- Different hook types (question, statement, statistic)
- Character limit compliance (<125 chars primary text)
- Ben's voice rules applied (British English, no AI buzzwords)

✅ **Output File:**
- Saves to `1-meta-ads/meta-ad-copy/outputs/META-AD-COPY-[campaign].md`
- Includes A/B test recommendations
- Performance predictions

---

## How to Use These Prompts

### Step 1: Pick Your Scenario

- **New campaign, not sure where to start?** → [01-basic-generation.md](01-basic-generation.md)
- **Target admin-overwhelmed coaches?** → [02-manual-overwhelm-campaign.md](02-manual-overwhelm-campaign.md)
- **Target invisible coaches (no online presence)?** → [03-invisibility-campaign.md](03-invisibility-campaign.md)
- **Promoting a webinar/masterclass?** → [04-webinar-registration.md](04-webinar-registration.md)
- **Want to see what's working in your account first?** → [05-api-data-analysis-first.md](05-api-data-analysis-first.md)

### Step 2: Copy the Prompt

Open the .md file, copy the full prompt text (including "Read 1-meta-ads/meta-ad-copy/skill.md...").

### Step 3: Paste to Claude Code

Paste the prompt directly to Claude Code. It will read the skill instructions and follow them.

### Step 4: Answer the Questions

Skill will ask 4 questions. Use the "Pre-filled Context" section in each prompt as a guide.

### Step 5: Review Output

Output saved to `1-meta-ads/meta-ad-copy/outputs/META-AD-COPY-[campaign].md`

---

## What This Skill Does NOT Do

❌ Competitor ad analysis (you manually provide competitor ad if needed)
❌ Ad fatigue detection (Meta API doesn't return CTR decline data)
❌ Retargeting-specific mode (same flow for all audiences)
❌ Budget optimization mode (generates same variations regardless of budget)
❌ Seasonal awareness (you manually mention timing in your offer description)

**These are manual workflows** - you provide context in your prompt or answers.

---

## Tips

✅ **Do:**
- Be specific in Question 3 (Core Offer) - the more detail, the better output
- Select relevant Optional Elements (Question 4) - they improve copy quality
- Use prompt #05 when planning campaigns (see what works first)
- Test multiple pain points for same offer (run skill 4 times with different pain points)

❌ **Don't:**
- Skip Question 3 or be vague ("increase revenue" is too generic)
- Expect skill to detect retargeting audiences automatically (mention in offer description)
- Expect seasonal context without mentioning it ("Q1 planning masterclass" vs "masterclass")

---

## Skill Location

`/Users/learnai/Desktop/The Coach Consultant/1-meta-ads/meta-ad-copy/`

Full skill documentation: [../../1-meta-ads/meta-ad-copy/skill.md](../../1-meta-ads/meta-ad-copy/skill.md)

---

Version: v1.0 (March 2026)
