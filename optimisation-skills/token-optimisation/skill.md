---
name: token-optimisation
description: Audit CLAUDE.md and workspace for token waste, ask 3-5 discovery questions, then generate an optimised version. Reduces token usage per conversation by removing duplicated content, compressing verbose sections, and restructuring files. Use when token costs are too high, conversations feel slow, or CLAUDE.md has grown too large. Triggers on "optimise tokens", "reduce token usage", "CLAUDE.md is too big", "lower tokens", or /token-optimisation.
---

# Token Optimisation Skill

## Purpose

Audit CLAUDE.md and the full workspace to identify token waste, then produce optimised versions that reduce per-conversation token cost without losing functionality. Every token in CLAUDE.md is loaded on every conversation — waste here multiplies across every single interaction.

## Why This Matters

CLAUDE.md is loaded into context on **every conversation**. If CLAUDE.md is 14,000 characters (~3,500 tokens), and Ben runs 20 conversations per day, that's 70,000 tokens/day just on CLAUDE.md alone. Reducing it by 40% saves ~28,000 tokens/day.

skill.md files are loaded when a skill is invoked. Oversized skill files slow down responses and increase costs.

## When to Use

- "Optimise tokens" / "Reduce token usage"
- "CLAUDE.md is too big"
- "Conversations feel slow"
- "Lower costs"
- After adding new skills or expanding CLAUDE.md
- Quarterly workspace audit

## Workflow

### Step 1: Audit (Automatic)

Scan the workspace and calculate token estimates:

```bash
cd /path/to/project
python jay-skills/token-optimisation/audit_tokens.py
```

The script measures:
1. **CLAUDE.md** — chars, lines, estimated tokens, section breakdown
2. **All skill.md files** — size per skill, ranked by token cost
3. **docs/ folder** — files referenced by CLAUDE.md vs orphaned
4. **Duplicated content** — same info appearing in CLAUDE.md AND skill files
5. **Verbose patterns** — unnecessary examples, repeated rules, long tables

### Step 2: Discovery Questions (Interactive)

Ask the user 3-5 questions via AskUserQuestion:

**Q1: Priority**
"What matters more — keeping all detail available, or minimising token cost?"
- "Minimum tokens" → aggressive compression
- "Balance" → compress duplicates, keep key details
- "Keep everything" → only remove true duplicates

**Q2: Skill Usage**
"Which skills does Ben use most often?"
- Identifies which skill.md files to prioritise for optimisation
- Rarely-used skills can have lighter documentation

**Q3: Deep-Dive Docs**
"Does Ben ever ask Claude to read the deep-dive docs (voice samples, frameworks, persona)?"
- If yes → keep references in CLAUDE.md
- If no → remove section, save ~500 tokens

**Q4: Forbidden Phrases**
"Is the forbidden phrases list still needed in CLAUDE.md, or has the model learned Ben's voice?"
- If still needed → keep but compress
- If stable → move to skill files only, remove from CLAUDE.md

**Q5: Channel Rules**
"Are the channel-specific rules in CLAUDE.md useful, or does Ben always invoke skills directly?"
- If skills handle it → remove channel rules from CLAUDE.md, save ~2,000 tokens
- If Ben reads CLAUDE.md directly → keep compressed version

### Step 3: Generate Optimisation Report

Produce a structured report:

```
TOKEN AUDIT REPORT
==================
Current State:
  CLAUDE.md:        14,000 chars (~3,500 tokens)
  skill.md (total): 94,000 chars (~23,500 tokens)
  docs/ (total):    180,000 chars (~45,000 tokens)

Issues Found:
  1. DUPLICATED: Brand voice rules appear in CLAUDE.md AND 6 skill files (est. 2,100 wasted tokens)
  2. VERBOSE: Channel-specific rules in CLAUDE.md duplicate skill.md content (est. 1,800 wasted tokens)
  3. UNUSED: Deep-dive docs referenced but never loaded (est. 500 wasted tokens in pointers)
  4. OVERSIZED: meta-ad-copy/skill.md is 18,108 chars — largest skill file

Recommendations:
  1. Move channel rules to skill files → save ~1,800 tokens from CLAUDE.md
  2. Compress brand voice rules → single source of truth → save ~800 tokens
  3. Remove example outputs from skill files → save ~3,000 tokens across skills
  4. ...

Projected Savings:
  CLAUDE.md: 14,000 → 8,400 chars (40% reduction, ~1,400 tokens saved per conversation)
  Daily savings (20 convos): ~28,000 tokens
  Monthly savings: ~840,000 tokens
```

### Step 4: Apply Optimisations

After user approval, apply changes:

1. **Generate optimised CLAUDE.md** — compressed version with same functionality
2. **Update skill files** — move content from CLAUDE.md into relevant skills
3. **Remove duplicates** — single source of truth for each piece of info
4. **Archive originals** — keep backup before applying changes

## Optimisation Techniques

### 1. Deduplication
Content that exists in both CLAUDE.md and skill.md files:
- Brand voice rules → keep in CLAUDE.md (loaded always), remove from individual skills
- Channel-specific rules → keep in skill.md (loaded on demand), remove from CLAUDE.md
- Forbidden phrases → keep in CLAUDE.md, reference from skills

### 2. Compression
Verbose patterns that can be shortened:
- Long examples → replace with short inline examples
- Markdown tables → compress to bullet lists
- Repeated "see file X" pointers → consolidate into one reference section
- Multiple "NEVER do X" warnings → merge into one list

### 3. Restructuring
Move content to where it's needed:
- **Always-loaded content** (CLAUDE.md) → only brand rules, project overview, critical warnings
- **On-demand content** (skill.md) → channel rules, examples, detailed workflows
- **Reference content** (docs/) → deep-dive material loaded only when explicitly needed

### 4. Pruning
Remove content that no longer adds value:
- Outdated status updates
- Completed setup instructions
- Historical notes that are now in git history
- Redundant file path references

## Token Estimation

Rule of thumb: **1 token ≈ 4 characters** (English text)

| File | Characters | Est. Tokens | Loaded When |
|------|-----------|-------------|-------------|
| CLAUDE.md | 14,000 | ~3,500 | Every conversation |
| skill.md (per skill) | 4,000-18,000 | ~1,000-4,500 | Skill invocation |
| docs/ (total) | 180,000+ | ~45,000 | Explicit read |

## Output

The skill produces:
1. `TOKEN-AUDIT-REPORT-[date].md` — full audit with recommendations
2. `CLAUDE-OPTIMISED.md` — compressed version (user reviews before replacing)
3. `CHANGELOG.md` — what was changed and why

Files saved to:
```
jay-skills/token-optimisation/outputs/
```

## Safety

- **Never overwrite CLAUDE.md directly** — always generate a separate optimised version
- **User must review and approve** before replacing
- **Keep backup** of original CLAUDE.md before any changes
- **Test** — run a sample skill invocation after optimisation to verify nothing broke
