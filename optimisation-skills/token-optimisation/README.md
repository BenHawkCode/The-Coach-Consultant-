# Token Optimisation Skill

Audit and optimise CLAUDE.md and workspace for lower token usage per conversation.

## What It Does

1. Scans CLAUDE.md, all skill.md files, and docs/ for token waste
2. Identifies duplicated content, verbose patterns, oversized files
3. Asks 3-5 discovery questions to understand priorities
4. Generates an optimisation report with projected savings
5. Produces an optimised CLAUDE.md for review

## Quick Start

```bash
# Full audit
python jay-skills/token-optimisation/audit_tokens.py

# CLAUDE.md only
python jay-skills/token-optimisation/audit_tokens.py --claude-only

# Skill files only
python jay-skills/token-optimisation/audit_tokens.py --skills-only
```

## Output

Reports saved to `jay-skills/token-optimisation/outputs/`

## Why It Matters

CLAUDE.md is loaded on every conversation. At ~3,500 tokens, 20 conversations/day = 70,000 tokens/day just on context. A 40% reduction saves ~28,000 tokens/day.
