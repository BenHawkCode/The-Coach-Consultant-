# 01. Basic Ad Generation

**What This Does:** Standard workflow - answer 4 questions, get 3-5 variations

---

## Prompt

```
Read the skill instructions in skills/meta-ad-copy/skill.md and follow them to generate meta ad copy for my campaign.
```

---

## What Happens

1. Skill asks 4 questions:
   - **Campaign Goal:** Book a Call / Webinar / Resource / Course
   - **Main Pain:** Manual Overwhelm / Invisibility / AI Paralysis / Revenue Plateau
   - **Core Offer:** Your specific offer description
   - **Include (optional):** Social Proof / Urgency / Metrics / Authority

2. Fetches Meta API data (top 10 performers)

3. Analyzes winning patterns (hooks, CTAs, metrics)

4. Generates 3-5 variations with different hook types

5. Saves to `skills/meta-ad-copy/outputs/META-AD-COPY-[campaign].md`

---

## Example

**User:** "Generate meta ad copy"

**Skill asks 4 questions, user answers:**
- Campaign Goal: Book a Call
- Main Pain: Manual Overwhelm
- Core Offer: Free 45-min strategy call to build AI operations system
- Include: Social Proof, Specific Metrics

**Output:** 3-5 variations (Question hook, Statement hook, Statistic hook, etc.)

---

## When to Use

- First time using the skill
- Standard lead gen campaign
- Need multiple hook variations for same offer
