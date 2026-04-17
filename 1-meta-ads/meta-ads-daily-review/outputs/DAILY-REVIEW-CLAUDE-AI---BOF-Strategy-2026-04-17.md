# Daily Review — CLAUDE.AI - BOF Strategy

**Date:** 2026-04-17
**Week:** Week 2 (First decisions)
**Date Range:** Last 7 days (2026-04-10 → 2026-04-17)
**Analyst:** Ben Mahmoud (via meta-ads-daily-review skill)

---

## ⚠️ DATA CAVEAT — READ FIRST

The "calls booked" numbers below come from Meta's `lead` / `fb_pixel_lead` action events. They are **not yet validated against ground truth** (Calendly bookings or GHL pipeline stage).

**What's been fixed:** The earlier 2x inflation bug is resolved — Meta was returning the same lead under two labels (`lead` + `offsite_conversion.fb_pixel_lead`) and the pipeline was summing both. We now take the max. That dropped the weekly total from 36 to 18.

**What's still pending:**
- Ground truth source confirmation (Calendly / GHL stage / manual)
- Whether a "lead" event in Meta is a form submit or an actual booked call
- Attribution window alignment (we currently use Meta default)

**Until confirmed:** treat the 18 number and the cost/call numbers as **directional, not exact**. Ben should cross-check against Ads Manager before acting on cost/call thresholds.

Antonio's dashboard still shows 36 — same root-cause bug in `collect_own_meta.py:91`. Flagged separately.

---

## AD SET LEVEL — HEALTH CHECK

All three ad sets ACTIVE. CTR is strong across the board (1.82% to 2.17%). The booking side is where the real picture changes after the fix — Warm drops from "hitting target" to "below target" once the count is halved, and Interest is now clearly broken.

| Ad set | Impressions | CTR | CPC | Spend | Leads (7d) | Cost/lead | Booking rate | Status |
|---|---|---|---|---|---|---|---|---|
| Warm — Retargeting 30% | 15,065 | 1.82% | £0.81 | £222.88 | 11 | £20.26 | 4.01% | Watch |
| Cold — Lookalike 30% | 10,846 | 1.90% | £1.18 | £242.80 | 5 | £48.56 | 2.43% | Concerning |
| Cold — Interest Based 40% | 13,062 | 2.17% | £1.02 | £289.14 | 2 | £144.57 | 0.70% | Concerning |

**Read:** Warm is the best audience but it is no longer hitting the 8% booking rate target (4.01%). Lookalike at £48.56/lead is borderline. Interest at £144.57/lead and 0.70% booking rate is the clear money leak — £289 spent, 2 leads. Funnel issue, not a creative issue.

---

## CREATIVE ANALYSIS — ACROSS ALL 3 AD SETS

Only creatives with material volume (≥1,000 impressions on at least one audience) shown below.

| Creative | Warm | Lookalike | Interest | Signal |
|---|---|---|---|---|
| Graphic 2 — Claude specialist | 2.15% (5,161) | 1.61% (867) | 2.75% (4,650) | ⭐ Strongest overall |
| Reel 5 — 9pm doing admin | 2.51% (1,472) | 2.70% (1,742) | 2.38% (1,049) | ⭐ Consistent across all 3 |
| Reel 6 — Results & re-invest | 1.76% (1,818) | 2.07% (1,932) | 2.06% (1,361) | Solid, watch |
| Graphic 5 — the numbers | 1.95% (719) | 1.54% (2,076) | 2.29% (1,005) | Solid, watch |
| Graphic 1 — AI systems stack | 1.18% (1,098) | 1.66% (1,508) | 1.02% (979) | Mixed |
| Graphic 6 — old vs AI | 1.16% (2,240) | 1.77% (790) | 2.06% (1,359) | Mixed |
| Graphic 3 — Brand moat | 1.33% (980) | 1.59% (692) | 2.34% (512) | Too little data |

Everything else (Reels 1-4, Graphic 4, B-variants) is under 500 impressions per placement — not enough signal.

---

## KILL / SCALE / WATCH VERDICTS

**Note:** Week 2 — verdicts are directional. No ad set budget changes until we've cleared enough conversion events per ad set and the ground truth call number is confirmed.

### Watch closely for scaling

- **Graphic 2 — Claude specialist** — 2.15% / 1.61% / 2.75% on meaningful volume (10,678 impressions total). Warm and Interest both above the 2% target. Strongest absolute winner. Quality ranking below average on Warm → flag before scaling.
- **Reel 5 — 9pm doing admin** — 2.51% / 2.70% / 2.38% across all three. Consistency is the story. Quality ranking below average on Warm and Interest → audit the hook.

Action next week: queue both for creative-level budget increase, contingent on quality-ranking review.

### Watch — need more data

- **Reel 6 — Results & re-invest** — close to target on Lookalike and Interest. Warm lagging at 1.76%.
- **Graphic 5 — the numbers** — Interest pulling 2.29%, Lookalike underperforming at 1.54%.
- **Graphic 6 — old vs AI** — 1.16% Warm is weak on 2,240 impressions. Lookalike and Interest compensating.
- **Graphic 1 — AI systems stack** — Weak on Warm and Interest. One more week before a call.
- **Graphic 3, Reels 1-4, B-variants** — insufficient volume.

### Concern — underperforming

None hitting the CTR kill threshold (<1.5% on 2+ audiences with sufficient impressions). The booking-side conversion gap is the bigger concern than any individual creative CTR.

---

## META QUALITY FLAGS TO ACT ON

- **Reel 5 — 9pm doing admin** in Warm and Interest — Meta flagging despite 2.5%+ CTR. Classic clickbait-risk signal. Audit the opening 3 seconds.
- **Reel 6 — Results & re-invest** in all three audiences — flagged everywhere. More serious.
- **Graphic 2 — Claude specialist** in Warm only — the winner has a quality issue. Interest version is clean, so the Warm placement is the one to investigate.
- **Graphic 1, Graphic 5, Graphic 6** — below-average on one audience each. Less urgent.

Why it matters: Meta deprioritises delivery on below-average creatives even when CTR is healthy.

---

## ANOMALIES WORTH FLAGGING

- **CTR + quality mismatch on Reel 5 (2.67% CTR)** — strongest performer technically but flagged below-average on two audiences. Clickbait risk.
- **CTR + quality mismatch on Graphic 2 (2.72% CTR)** — same pattern. The two scale candidates both have this issue.
- **Cost per lead in Interest is £144.57** — almost 3x the £50 ceiling. £289 spent, 2 leads. Single biggest money leak right now.
- **Booking rate in Warm is 4.01%** — previously looked like it was hitting target, but the corrected count reveals it's below the 8% benchmark. 11 leads / 274 clicks.
- **Booking rate in Lookalike is 2.43%** — 206 clicks, 5 leads. Well under target.
- **Booking rate in Interest is 0.70%** — 284 clicks, 2 leads. Landing page / offer mismatch for cold-interest traffic.
- **Budget split off** — Warm at 29.5% of spend (target 50%), Interest at 38.3% (target 20%). Budget flowing to the worst-converting audience.

---

## TOP PRIORITIES FOR THIS WEEK

1. **Confirm the ground truth for call bookings** — Calendly, GHL stage, or manual? Until this is answered, every cost/call number here and on the dashboard is directional. This is the Monday-morning blocker.
2. **Fix the budget split.** Interest eating 38% of spend at £144.57/lead while Warm sits at 29% at £20.26/lead. Rebalance toward 50/30/20 — Warm gets more budget, Interest gets cut back.
3. **Audit the landing page / offer signal for cold traffic.** Interest booking rate at 0.70% on 284 clicks isn't a creative problem, it's a funnel problem. Pull session recordings or check where cold traffic drops off.
4. **Quality-ranking review on Reel 5 and Graphic 2** before any budget increase. Check if the hook reads as clickbait to Meta's classifier — swap the first 3 seconds if needed.
5. **Let Reel 6 and Graphic 5 run another 7 days** — both close to the scaling line.

---

**Next review:** 2026-04-18
