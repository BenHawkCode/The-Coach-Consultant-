# 05. API Data Analysis First

**What This Does:** Analyze your Meta account's top performers BEFORE generating copy

---

## Prompt

```
Read skills/meta-ad-copy/skill.md and follow the instructions. Before generating variations, first analyze the Meta API data you fetch and show me a detailed breakdown of winning patterns (hooks, CTAs, metrics, character counts, what to avoid). Then generate copy based on those patterns.
```

---

## What Happens

1. Skill asks 4 questions (same as always)

2. **BUT:** Add instruction in prompt to analyze first:
   - Fetches Meta API data
   - Shows you winning hooks (question vs statement vs stat)
   - Shows high-CTR headlines
   - Shows proven CTAs
   - Shows metrics usage patterns
   - Identifies forbidden phrases to avoid

3. Generates 3-5 variations using those exact patterns

---

## Expected Output

**First: Analysis Report**
```markdown
## Winning Patterns from Your Account

**Top Hooks:**
- "Sound familiar?" (question) → 4.2% CTR avg
- "Most coaches waste £X..." (statement) → 3.8% CTR
- "300+ coaches use..." (social proof) → 3.5% CTR

**High-CTR Headlines:**
- "Predictable Client Flow for Coaches" → 5.1% CTR
- "Cut Admin Time by 90%" → 4.7% CTR

**Proven CTAs:**
- "Book a Call" → 12% conversion
- "Register Now" → 9% conversion

**Avoid (low performers):**
- "Unlock your potential" → 0.8% CTR
- Generic "Learn More" CTA → 3% conversion
```

**Then: Copy Variations**
3-5 variations using those winning patterns

---

## When to Use

- Want data-driven decisions (not guessing)
- Planning campaign strategy based on past performance
- Understanding what actually works in your account
- Optimizing based on proven patterns
