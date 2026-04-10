# Token Optimisation Audit Report

**Date:** 2026-04-10
**Project:** The Coach Consultant

---

## Summary

| Component | Characters | Est. Tokens | Loaded When |
|-----------|-----------|-------------|-------------|
| CLAUDE.md | 13,871 | ~3,467 | Every conversation |
| skill.md files (14) | 101,160 | ~25,287 | Skill invocation |
| docs/ files (22) | 252,627 | ~63,150 | Explicit read |
| **Total workspace** | **367,658** | **~91,904** | |

**Estimated daily cost (20 conversations):** ~69,340 tokens just from CLAUDE.md

---

## 1. CLAUDE.md Analysis

- **Size:** 13,871 chars / 352 lines / ~3,467 tokens
- **Sections:** 36
- **NEVER/CRITICAL warnings:** 4
- **Code/example blocks:** 1
- **Table rows:** 0

### Sections
- ## Project Overview
- ## Project Structure
- ## Core Directive: Sound Like Ben
- ## Brand Voice Rules (Core Only)
- ### British English Always
- ### Forbidden AI Phrases (NEVER USE)
- ### Ben's Natural Phrases (USE THESE)
- ### Punctuation & Tone
- ## Channel-Specific Rules
- ### Instagram Page Spy

### Verbose Patterns Found
- ⚠️ 4 NEVER/CRITICAL warnings (consider consolidating)
- ⚠️ 2 file paths referenced 3+ times

---

## 2. Skill Files (Ranked by Size)

| Skill | Characters | Tokens | Verbose? |
|-------|-----------|--------|----------|
| 1-meta-ads/meta-ad-copy/skill.md | 17,989 | ~4,497 | ⚠️ |
| 4-emails/email-campaign-skill/skill.md | 16,873 | ~4,218 | ⚠️ |
| 1-meta-ads/meta-ad-competitor/skill.md | 11,612 | ~2,903 | ⚠️ |
| 2-instagram/instagram-caption/SKILL.md | 7,764 | ~1,941 | ✅ |
| 2-instagram/instagram-carousel/TCC Carousels/skill.md | 7,509 | ~1,877 | ✅ |
| 4-emails/email-competitor-spy/skill.md | 7,063 | ~1,765 | ✅ |
| jay-skills/token-optimisation/skill.md | 6,728 | ~1,682 | ✅ |
| 2-instagram/ig-competitor-analysis/skill.md | 6,673 | ~1,668 | ✅ |
| jay-skills/gws-cli/SKILL.md | 5,104 | ~1,276 | ✅ |
| 1-meta-ads/meta-page-spy/skill.md | 4,126 | ~1,031 | ✅ |
| 2-instagram/instagram-page-spy/skill.md | 4,002 | ~1,000 | ✅ |
| jay-skills/md-transformation/skill.md | 3,256 | ~814 | ✅ |
| jay-skills/sync-jay-notes/skill.md | 1,824 | ~456 | ✅ |
| jay-skills/md-to-gdocs/skill.md | 637 | ~159 | ✅ |

---

## 3. Duplicated Content

**Estimated wasted tokens from duplication:** ~240

### 4-emails/email-campaign-skill/skill.md
**4 duplicated phrases** (~80 wasted tokens)

- ""Game changer" / "Unlock" / "Leverage" / "Journey"..."
- ""Here's the thing" / "Here's the reality" / "Here's how"..."
- "`docs/deep-dive/voice-samples/voice-characteristics.md`..."
- ""I see this constantly" / "I see this all the time"..."

### 4-emails/email-competitor-spy/skill.md
**1 duplicated phrases** (~20 wasted tokens)

- ""business owners and service providers" (NEVER say "coaches"..."

### 1-meta-ads/meta-ad-copy/skill.md
**6 duplicated phrases** (~120 wasted tokens)

- "Direct, straight-talking, Yorkshire influence..."
- ""Game changer" / "Unlock" / "Leverage" / "Journey"..."
- ""Here's the thing" / "Here's the reality" / "Here's how"..."
- "Authority through personal experience (not theory)..."
- ""business owners and service providers" (NEVER say "coaches"..."

### 2-instagram/ig-competitor-analysis/skill.md
**1 duplicated phrases** (~20 wasted tokens)

- ""business owners and service providers" (NEVER say "coaches"..."


---

## 4. Docs Files (Reference)

| File | Characters | Tokens |
|------|-----------|--------|
| docs/deep-dive/philosophy/50-50-book-FULL.md | 28,244 | ~7,061 |
| docs/Client Dashboard - Lovable Build Guide.md | 24,930 | ~6,232 |
| docs/deep-dive/voice-samples/sales-calls-FULL.md | 23,452 | ~5,863 |
| docs/deep-dive/philosophy/human-knowledge-FULL.md | 21,687 | ~5,421 |
| docs/Ben-Claude-Projects-Instructions.txt | 17,663 | ~4,415 |
| docs/Ben-Claude-Projects-Scraped-ARCHIVE.txt | 17,250 | ~4,312 |
| docs/IP-Folder-Summary.md | 13,388 | ~3,347 |
| docs/deep-dive/voice-samples/youtube-scripts-FULL.md | 12,025 | ~3,006 |
| docs/setup-guide.md | 10,166 | ~2,541 |
| docs/deep-dive/target-audience/alex-morgan-persona.md | 7,900 | ~1,975 |
| docs/deep-dive/target-audience/pain-points.md | 7,884 | ~1,971 |
| docs/deep-dive/philosophy/core-beliefs.md | 7,881 | ~1,970 |
| docs/deep-dive/frameworks/niche-domination.md | 7,246 | ~1,811 |
| docs/deep-dive/target-audience/emotional-triggers.md | 7,233 | ~1,808 |
| docs/deep-dive/voice-samples/ben-claude-projects.md | 7,172 | ~1,793 |

---

## 5. Recommendations

### High Impact (CLAUDE.md — affects every conversation)

**1. [HIGH] Compress CLAUDE.md channel-specific rules**
- Move detailed channel rules to skill.md files. CLAUDE.md only needs a one-line pointer per channel.
- Estimated savings: ~1,500-2,000 tokens

**2. [HIGH] Remove duplicated content between CLAUDE.md and skill files**
- Found ~240 wasted tokens from content appearing in both places.
- Estimated savings: ~240 tokens

**3. [MEDIUM] Compress oversized skill files: email-campaign-skill, meta-ad-copy**
- Remove verbose examples, compress tables, eliminate repeated instructions.
- Estimated savings: ~2,000-4,000 tokens per skill invocation


---

## 6. Projected Savings

| Metric | Current | After Optimisation |
|--------|---------|-------------------|
| CLAUDE.md tokens | ~3,467 | ~1,733 |
| Per conversation | ~3,467 tokens | ~1,733 tokens |
| Daily (20 convos) | ~69,340 | ~34,660 |
| Monthly (600 convos) | ~2,080,200 | ~1,039,800 |

---

*Report generated by Token Optimisation Skill — 2026-04-10*
