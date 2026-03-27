# Email Campaign Generation - The Coach Consultant

Generate email campaigns that sound EXACTLY like Ben Hawksworth with systematic voice verification and data-driven subject lines.

---

## Quick Stats

- **471 emails analyzed** (23 months: April 2024 - March 2026)
- **353 unique subject lines** documented
- **Voice accuracy:** 9.6/10 (vs 4.7/10 baseline)
- **Zero AI phrases** enforced
- **Auto-triggers:** All email generation tasks

---

## What This Skill Does

### Core Features

1. **Systematic Voice Verification**
   - Reads voice files BEFORE writing
   - Checks 20+ forbidden AI phrases
   - Enforces 12+ Ben natural phrases
   - Objective scoring (8+/10 required)

2. **Data-Driven Subject Lines**
   - References 471 real emails
   - Uses proven patterns (#theGAPyoumiss: 16 sends, BadBizAdvice: 23 sends)
   - Never invents generic headlines
   - Psychology triggers from actual data

3. **Campaign Templates (A-E)**
   - A) Free Consult Call Claim Nurture (4-5 emails)
   - B) No Show Nurture (2-3 emails)
   - C) Not Yet Ready (5-7 emails)
   - D) Booking Requested Reply (1-2 emails)
   - E) Appointment Reminders (2-3 emails)

4. **Performance Optimization**
   - British English enforcement (systematise, whilst)
   - Specific CTAs (Reply READY, Reply MOVE)
   - One sentence per line structure
   - 20-30+ lines minimum

5. **Anti-Rationalization Guards**
   - "Ready to send" → RED FLAG (verify first!)
   - "Zero AI phrases" → PROVE IT (run checklist)
   - "Matches voice" → SCORE IT (8+/10 required)
   - Time pressure ≠ skip quality

---

## How to Use

### Via Claude Code

```bash
# Auto-triggers when you mention email generation
"Write 3 emails for Free Consult Call Claim Nurture campaign"

# Or explicit skill invocation
/email-campaign-ben-hawksworth
```

The skill automatically:
1. Reads voice-characteristics.md
2. Checks forbidden phrases list
3. Writes email → verifies → scores
4. Repeats per email (not batch)
5. Delivers with verification checklist

### Example Output Quality

**Baseline (WITHOUT skill):**
- 4.7/10 voice score
- 8+ forbidden AI phrases
- Generic subject lines
- "Ready to send" without verification

**With skill:**
- 9.6/10 voice score
- ZERO forbidden phrases
- Data-driven subjects from 471 emails
- Systematic verification checklist

---

## Available Data

### Performance Analysis
- [COMPLETE_EMAIL_STATISTICS.md](ghl-data/COMPLETE_EMAIL_STATISTICS.md) - Full 471 email analysis
- [REAL_EMAIL_DATA.md](ghl-data/REAL_EMAIL_DATA.md) - Current campaign status
- [EMAIL_STATS_REALITY.md](ghl-data/EMAIL_STATS_REALITY.md) - Reality check vs assumptions

### Testing Documentation
- [baseline-test-scenario.md](email-campaign-skill/baseline-test-scenario.md) - Pressure test scenarios
- [baseline-results.md](email-campaign-skill/baseline-results.md) - Agent behavior WITHOUT skill
- [green-test-results.md](email-campaign-skill/green-test-results.md) - Agent behavior WITH skill

### Skill Files
- [skill.md](email-campaign-skill/skill.md) - Full skill documentation (deployed to `~/.claude/skills/`)

---

## Key Insights from 471 Emails

### Top Subject Line Patterns

1. **"Your guide is inside"** (13x) - Lead magnet delivery
2. **#theGAPyoumiss series** (16x) - Educational blind spots
3. **BadBizAdvice series** (23x) - Contrarian positioning
4. **Workshop/Event invites** (15x) - Live engagement
5. **Personal stories** (20+x) - Authenticity hooks

### Email Volume Trends

- **Average:** 20.5 emails/month
- **Peak:** November 2025 (61 emails)
- **Recent:** Q1 2026 (92 emails)
- **Growth:** 522% increase Q3→Q4 2025

### Campaign Structure

**Current campaigns (all DRAFT except lead magnet):**
- A) Free Consult Call Claim Nurture
- B) No Show Nurture
- C) Not Yet Ready
- D) Booking Requested Reply
- E) Appointment Reminders

**Only active automation:**
- Lead magnet delivery ("Your guide is inside")

---

## Email Performance Benchmarks

### Industry Standards (Coaching/Consulting)

| Metric | Industry Avg | Target |
|--------|--------------|--------|
| Open Rate | 20-30% | 30-40% |
| Click Rate | 2-5% | 5-10% |
| Reply Rate | 1-2% | 3-5% |
| Booking Rate | 10-15% | 15-20% |
| Show-up Rate | 60-70% | 70-80% |

**Note:** Open/click data not available via API - need GHL dashboard access

### Current List Health

- **Total contacts:** 100
- **With email:** 39 (39%)
- **Active recipients:** 12
- **Bounce rate:** 16.7% ⚠️ (target: <2%)
- **Unsubscribe rate:** 8.3% ⚠️ (target: <0.5%)

**Action needed:** List hygiene, remove bounced emails, respect DND settings

---

## Voice Rules Quick Reference

### Forbidden AI Phrases (NEVER)

❌ "Here's the thing" / "Let's dive in"
❌ "Game changer" / "Unlock" / "Leverage"
❌ "Move the needle" / "Circle back"
❌ "slip through the cracks"

### Ben's Natural Phrases (ALWAYS 3-5 per email)

✅ "Right so" / "gonna" / "kinda"
✅ "I see this constantly"
✅ "Sound familiar"
✅ "What actually works"
✅ "The shift is simple"

### Structure Requirements

- Opening: `Hi {{first_name}},`
- One sentence per line
- 20-30 lines minimum
- British English (organisation, whilst, systematise)
- Soft CTA (Reply READY, Reply MOVE, Reply LINK)
- Sign off: `Ben` + `www.thecoachconsultant.uk`
- Subject: `CampaignName | Headline`

---

## Campaign-Specific Guidelines

### A) Free Consult Call Claim Nurture (4-5 emails)

**Recipients:** Just booked free consult
**Goal:** Reduce no-shows, prep for call

1. Confirmation + Expectation (Day 0)
2. Pattern Recognition (Day 1-2)
3. Pre-Call Prep (Day before)
4. 2-Hour Reminder (Day of)

### B) No Show Nurture (2-3 emails)

**Recipients:** Missed their call
**Goal:** Re-book without guilt trip

1. We Missed You (Immediate)
2. Value Drop (2 days later)
3. Last Chance (5 days later, optional)

### C) Not Yet Ready (5-7 emails, weekly)

**Recipients:** Cold leads
**Goal:** Nurture to booking

Weekly themes: Success story → Free resource → Contrarian take → Case study → Direct offer → Re-engagement → Final pitch

### D) Booking Requested Reply (1-2 emails)

**Recipients:** Just submitted request
**Goal:** Instant confirmation

1. Got Your Request (Immediate)
2. Calendar link + next steps

### E) Appointment Reminders (2-3 emails)

**Recipients:** Booked calls
**Goal:** Reduce no-shows

1. 48-hour: Prep guide
2. 24-hour: Zoom + agenda
3. 2-hour: Final reminder

---

## Integration with GHL

### API Configuration

```bash
# Already configured
GHL_API_KEY=pit-a5d0b4ae-297d-405c-bceb-562aa16244b3
GHL_LOCATION_ID=4pEp1NDve1Vg3Hx08Mmb
```

### Available Endpoints (readonly)

- ✅ Campaigns list
- ✅ Contacts data
- ✅ Opportunities pipeline
- ✅ Conversations history
- ✅ Calendars & appointments
- ✅ Forms submissions
- ✅ Workflows automation

**Note:** Open/click metrics require dashboard access (not in API)

---

## Quality Standards

### Voice Accuracy Threshold

**Minimum 8/10 required to deliver:**

| Score | Meaning | Action |
|-------|---------|--------|
| 1-3 | AI-sounding | Full rewrite |
| 4-6 | Generic | Major revisions |
| 7 | Acceptable | Minor tweaks |
| 8-9 | Good | Deliver |
| 10 | Perfect | Rare but possible |

### Verification Checklist (Every Email)

- [ ] Read voice-characteristics.md
- [ ] Checked forbidden phrases (zero violations)
- [ ] Used 3-5 Ben's natural phrases
- [ ] Subject from proven patterns (not invented)
- [ ] Structure: Hi {{first_name}}, one per line, 20-30+ lines
- [ ] British English (organisation, whilst)
- [ ] CTA present and specific
- [ ] Sign off: Ben + URL
- [ ] Voice score 8+/10
- [ ] NO "ready to send" without verification

---

## Next Steps

### Immediate (Priority 1)

1. ✅ Email generation skill deployed
2. ⏳ Activate campaigns A-E (write content)
3. ⏳ Clean email list (remove bounced)
4. ⏳ Set up GHL dashboard tracking

### Short-term (Priority 2)

1. A/B test subject lines
2. Optimize CTAs per campaign
3. Track open/click rates
4. Build segmentation strategy

### Long-term (Priority 3)

1. Scale list to 100+ subscribers
2. Automate performance reporting
3. Build email-to-booking attribution
4. Create referral incentive system

---

## Files Structure

```
4-emails/
├── README.md                           # This file
├── email-campaign-skill/
│   ├── skill.md                        # Main skill (deployed)
│   ├── baseline-test-scenario.md       # Test scenarios
│   ├── baseline-results.md             # Baseline behavior
│   └── green-test-results.md           # Skill effectiveness
├── ghl-data/
│   ├── COMPLETE_EMAIL_STATISTICS.md    # 471 emails analyzed
│   ├── REAL_EMAIL_DATA.md              # Current status
│   ├── EMAIL_STATS_REALITY.md          # Reality check
│   ├── campaigns.json                  # Campaign list
│   ├── contacts.json                   # Contact data
│   ├── opportunities.json              # Pipeline data
│   ├── conversations.json              # Message history
│   ├── calendars.json                  # Appointments
│   ├── forms.json                      # Form submissions
│   ├── workflows.json                  # Automation
│   └── messages-*.json                 # Conversation details (12 files)
└── outputs/                            # Generated campaigns (coming soon)
```

---

## Support

**Questions?** Reference:
- [CLAUDE.md](../CLAUDE.md) - Brand voice rules
- [docs/Ben-Claude-Projects-Instructions.txt](../docs/Ben-Claude-Projects-Instructions.txt) - Email format (lines 291-461)
- [docs/deep-dive/voice-samples/](../docs/deep-dive/voice-samples/) - Deep voice context

**Issues?** Check:
- Skill is deployed: `~/.claude/skills/email-campaign-ben-hawksworth/skill.md`
- Voice files accessible: `docs/deep-dive/voice-samples/voice-characteristics.md`
- Data files present: `4-emails/ghl-data/COMPLETE_EMAIL_STATISTICS.md`

---

**Status:** ✅ Live and tested (RED-GREEN-REFACTOR cycle completed)
**Version:** 1.0.0
**Last Updated:** 2026-03-24
