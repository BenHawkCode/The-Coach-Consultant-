# Baseline Test Scenario - Email Campaign Generation

**Purpose:** Test agent WITHOUT skill to document baseline behavior

**Date:** 2026-03-24

---

## Pressure Scenario 1: Time Pressure + Brand Voice

**Context:**
- User needs 3 emails for "Free Consult Call Claim Nurture" campaign
- User says "quick, need this in 10 minutes"
- Agent has access to CLAUDE.md and docs but NOT to email skill

**Expected Failure Modes:**
- Generic AI phrasing ("Here's the thing", "Let's dive in")
- Not using Ben's natural phrases ("Right so", "gonna", "kinda")
- Corporate buzzwords instead of Yorkshire straight-talk
- Missing Ben's contrarian positioning
- Wrong email structure (not one sentence per line)

**Test Prompt:**
```
I need 3 emails for the "Free Consult Call Claim Nurture" campaign - these go to people who just booked a free consult call with Ben. Need them quick, can you write them in 10 minutes? Make sure they sound like Ben.
```

---

## Pressure Scenario 2: Performance Optimization Pressure

**Context:**
- User wants subject lines that get high open rates
- Agent has stats showing 353 unique subjects used
- Pressure: "Our open rates are low, need subject lines that CONVERT"

**Expected Failure Modes:**
- Generic clickbait ("You won't believe...", "Secret to...")
- Not referencing Ben's proven patterns (#theGAPyoumiss, BadBizAdvice)
- Missing Ben's contrarian style
- Not using psychology triggers from actual data

**Test Prompt:**
```
Write subject lines for a 5-email nurture sequence. Our current open rates are terrible, I need subject lines that actually get people to open. Look at what's worked before.
```

---

## Pressure Scenario 3: Sunk Cost + Authority Pressure

**Context:**
- User already wrote draft emails but they're too "AI sounding"
- User asks agent to "just fix the voice quickly"
- Pressure: Don't want to rewrite from scratch (sunk cost)

**Expected Failure Modes:**
- Light editing instead of full rewrite
- Keeping AI phrases and just tweaking
- Not reading voice samples deeply
- "Good enough" mentality under time pressure

**Test Prompt:**
```
I already wrote these 3 emails but they sound too AI. Can you quickly fix the voice to match Ben's style? Here are the drafts:

Email 1:
"Hi there! I hope this email finds you well. I wanted to reach out and thank you for booking your consultation call with us. We're excited to dive deep into your business challenges and explore how we can help you scale. Here's what you can expect on our call..."

Email 2:
"Hello again! Just wanted to circle back and share some valuable insights before our upcoming call. At the end of the day, success in coaching comes down to three key factors..."

Email 3:
"Greetings! As we approach your scheduled consultation, I wanted to provide you with a comprehensive guide to help you maximize the value of our time together..."
```

---

## What to Document

For each scenario, record:

1. **Exact output** (first 200 words of each email)
2. **AI phrases used** (list every forbidden phrase)
3. **Ben's phrases missing** (which natural phrases weren't used)
4. **Structure violations** (not one sentence per line, etc.)
5. **Rationalizations** (what did agent say when asked about choices)
6. **Time taken** (did pressure cause shortcuts)

---

## Success Criteria for Baseline

Test is "successful" if agent:
- ❌ Uses forbidden AI phrases
- ❌ Doesn't sound like Ben
- ❌ Takes shortcuts under pressure
- ❌ Doesn't reference 471 emails of data
- ❌ Doesn't use proven subject line patterns

**This confirms we NEED the skill.**

---

## Post-Baseline Next Steps

After documenting failures:
1. Write skill that addresses THOSE SPECIFIC failures
2. Run same scenarios WITH skill
3. Verify agent now complies
4. Find new loopholes → refactor
