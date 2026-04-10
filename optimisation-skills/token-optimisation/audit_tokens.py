#!/usr/bin/env python3
"""
Token Optimisation Audit Script
Scans the workspace and generates a token usage report.

Usage:
    python audit_tokens.py                    # Full audit
    python audit_tokens.py --claude-only      # CLAUDE.md only
    python audit_tokens.py --skills-only      # skill.md files only
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = Path(__file__).parent / "outputs"

# Approximate: 1 token ≈ 4 chars for English text
CHARS_PER_TOKEN = 4


def estimate_tokens(text: str) -> int:
    """Estimate token count from character count."""
    return len(text) // CHARS_PER_TOKEN


def analyze_file(filepath: Path) -> dict:
    """Analyze a single file for token metrics."""
    if not filepath.exists():
        return None

    text = filepath.read_text(encoding="utf-8", errors="ignore")
    lines = text.split("\n")

    # Count sections (## headers)
    sections = [l.strip() for l in lines if l.strip().startswith("##")]

    # Detect patterns
    duplicate_markers = []
    verbose_patterns = []

    # Check for repeated "NEVER" / "CRITICAL" warnings
    never_lines = [l for l in lines if "NEVER" in l.upper() and not l.strip().startswith("#")]
    if len(never_lines) > 3:
        verbose_patterns.append(f"{len(never_lines)} NEVER/CRITICAL warnings (consider consolidating)")

    # Check for example blocks
    example_blocks = text.count("```")
    if example_blocks > 10:
        verbose_patterns.append(f"{example_blocks // 2} code/example blocks (consider reducing)")

    # Check for markdown tables
    table_lines = [l for l in lines if l.strip().startswith("|") and "|" in l[1:]]
    if len(table_lines) > 20:
        verbose_patterns.append(f"{len(table_lines)} table rows (consider compressing)")

    # Check for repeated file paths
    path_refs = re.findall(r'`[a-zA-Z0-9_\-/]+\.[a-z]+`', text)
    path_counts = defaultdict(int)
    for p in path_refs:
        path_counts[p] += 1
    repeated_paths = {k: v for k, v in path_counts.items() if v > 2}
    if repeated_paths:
        verbose_patterns.append(f"{len(repeated_paths)} file paths referenced 3+ times")

    return {
        "path": str(filepath.relative_to(PROJECT_ROOT)),
        "chars": len(text),
        "lines": len(lines),
        "tokens": estimate_tokens(text),
        "sections": len(sections),
        "section_names": sections[:10],
        "verbose_patterns": verbose_patterns,
        "never_warnings": len(never_lines),
        "example_blocks": example_blocks // 2,
        "table_rows": len(table_lines),
    }


def find_duplicates(claude_md_text: str, skill_files: list) -> list:
    """Find content duplicated between CLAUDE.md and skill files."""
    duplicates = []

    # Extract key phrases from CLAUDE.md (lines > 30 chars, not headers/formatting)
    claude_lines = claude_md_text.split("\n")
    claude_phrases = set()
    for line in claude_lines:
        clean = line.strip().strip("-").strip("*").strip()
        if len(clean) > 40 and not clean.startswith("#") and not clean.startswith("|"):
            claude_phrases.add(clean[:80])

    # Check each skill file for matches
    for skill_info in skill_files:
        skill_path = PROJECT_ROOT / skill_info["path"]
        if not skill_path.exists():
            continue
        skill_text = skill_path.read_text(encoding="utf-8", errors="ignore")

        matches = []
        for phrase in claude_phrases:
            if phrase in skill_text:
                matches.append(phrase[:60] + "...")

        if matches:
            duplicates.append({
                "skill": skill_info["path"],
                "matches": matches[:5],
                "count": len(matches),
                "est_wasted_tokens": len(matches) * 20,  # ~20 tokens per duplicated line
            })

    return duplicates


def generate_report(claude_info: dict, skill_infos: list, doc_infos: list, duplicates: list) -> str:
    """Generate the full audit report."""
    now = datetime.now().strftime("%Y-%m-%d")

    total_skill_chars = sum(s["chars"] for s in skill_infos)
    total_skill_tokens = sum(s["tokens"] for s in skill_infos)
    total_doc_chars = sum(d["chars"] for d in doc_infos)
    total_doc_tokens = sum(d["tokens"] for d in doc_infos)
    total_dup_tokens = sum(d["est_wasted_tokens"] for d in duplicates)

    report = f"""# Token Optimisation Audit Report

**Date:** {now}
**Project:** The Coach Consultant

---

## Summary

| Component | Characters | Est. Tokens | Loaded When |
|-----------|-----------|-------------|-------------|
| CLAUDE.md | {claude_info['chars']:,} | ~{claude_info['tokens']:,} | Every conversation |
| skill.md files ({len(skill_infos)}) | {total_skill_chars:,} | ~{total_skill_tokens:,} | Skill invocation |
| docs/ files ({len(doc_infos)}) | {total_doc_chars:,} | ~{total_doc_tokens:,} | Explicit read |
| **Total workspace** | **{claude_info['chars'] + total_skill_chars + total_doc_chars:,}** | **~{claude_info['tokens'] + total_skill_tokens + total_doc_tokens:,}** | |

**Estimated daily cost (20 conversations):** ~{claude_info['tokens'] * 20:,} tokens just from CLAUDE.md

---

## 1. CLAUDE.md Analysis

- **Size:** {claude_info['chars']:,} chars / {claude_info['lines']} lines / ~{claude_info['tokens']:,} tokens
- **Sections:** {claude_info['sections']}
- **NEVER/CRITICAL warnings:** {claude_info['never_warnings']}
- **Code/example blocks:** {claude_info['example_blocks']}
- **Table rows:** {claude_info['table_rows']}

### Sections
"""

    for s in claude_info["section_names"]:
        report += f"- {s}\n"

    if claude_info["verbose_patterns"]:
        report += "\n### Verbose Patterns Found\n"
        for p in claude_info["verbose_patterns"]:
            report += f"- ⚠️ {p}\n"

    report += f"""
---

## 2. Skill Files (Ranked by Size)

| Skill | Characters | Tokens | Verbose? |
|-------|-----------|--------|----------|
"""

    for s in sorted(skill_infos, key=lambda x: x["chars"], reverse=True):
        flag = "⚠️" if s["chars"] > 10000 else "✅"
        report += f"| {s['path']} | {s['chars']:,} | ~{s['tokens']:,} | {flag} |\n"

    report += f"""
---

## 3. Duplicated Content

**Estimated wasted tokens from duplication:** ~{total_dup_tokens:,}

"""

    if duplicates:
        for d in duplicates:
            report += f"### {d['skill']}\n"
            report += f"**{d['count']} duplicated phrases** (~{d['est_wasted_tokens']} wasted tokens)\n\n"
            for m in d["matches"]:
                report += f"- \"{m}\"\n"
            report += "\n"
    else:
        report += "No significant duplicates found.\n"

    report += f"""
---

## 4. Docs Files (Reference)

| File | Characters | Tokens |
|------|-----------|--------|
"""

    for d in sorted(doc_infos, key=lambda x: x["chars"], reverse=True)[:15]:
        report += f"| {d['path']} | {d['chars']:,} | ~{d['tokens']:,} |\n"

    # Recommendations
    report += f"""
---

## 5. Recommendations

### High Impact (CLAUDE.md — affects every conversation)

"""

    recommendations = []

    if claude_info["chars"] > 10000:
        recommendations.append({
            "action": "Compress CLAUDE.md channel-specific rules",
            "detail": "Move detailed channel rules to skill.md files. CLAUDE.md only needs a one-line pointer per channel.",
            "savings": "~1,500-2,000 tokens",
            "priority": "HIGH",
        })

    if claude_info["never_warnings"] > 5:
        recommendations.append({
            "action": "Consolidate NEVER/CRITICAL warnings",
            "detail": f"Found {claude_info['never_warnings']} warning lines. Merge into a single 'Rules' section.",
            "savings": "~200-400 tokens",
            "priority": "MEDIUM",
        })

    if total_dup_tokens > 100:
        recommendations.append({
            "action": "Remove duplicated content between CLAUDE.md and skill files",
            "detail": f"Found ~{total_dup_tokens} wasted tokens from content appearing in both places.",
            "savings": f"~{total_dup_tokens} tokens",
            "priority": "HIGH",
        })

    oversized_skills = [s for s in skill_infos if s["chars"] > 12000]
    if oversized_skills:
        names = ", ".join(s["path"].split("/")[-2] for s in oversized_skills)
        recommendations.append({
            "action": f"Compress oversized skill files: {names}",
            "detail": "Remove verbose examples, compress tables, eliminate repeated instructions.",
            "savings": "~2,000-4,000 tokens per skill invocation",
            "priority": "MEDIUM",
        })

    if not recommendations:
        report += "No major issues found. Workspace is reasonably optimised.\n"
    else:
        for i, r in enumerate(recommendations, 1):
            report += f"**{i}. [{r['priority']}] {r['action']}**\n"
            report += f"- {r['detail']}\n"
            report += f"- Estimated savings: {r['savings']}\n\n"

    # Projected savings
    total_saveable = sum(int(re.search(r'(\d+)', r["savings"].replace(",", "")).group(1)) for r in recommendations if re.search(r'(\d+)', r["savings"]))
    if total_saveable > 0:
        report += f"""
---

## 6. Projected Savings

| Metric | Current | After Optimisation |
|--------|---------|-------------------|
| CLAUDE.md tokens | ~{claude_info['tokens']:,} | ~{max(claude_info['tokens'] - total_saveable, claude_info['tokens'] // 2):,} |
| Per conversation | ~{claude_info['tokens']:,} tokens | ~{max(claude_info['tokens'] - total_saveable, claude_info['tokens'] // 2):,} tokens |
| Daily (20 convos) | ~{claude_info['tokens'] * 20:,} | ~{max(claude_info['tokens'] - total_saveable, claude_info['tokens'] // 2) * 20:,} |
| Monthly (600 convos) | ~{claude_info['tokens'] * 600:,} | ~{max(claude_info['tokens'] - total_saveable, claude_info['tokens'] // 2) * 600:,} |
"""

    report += f"""
---

*Report generated by Token Optimisation Skill — {now}*
"""

    return report


def main():
    parser = argparse.ArgumentParser(description="Token Optimisation Audit")
    parser.add_argument("--claude-only", action="store_true", help="Audit CLAUDE.md only")
    parser.add_argument("--skills-only", action="store_true", help="Audit skill files only")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"  Token Optimisation Audit")
    print(f"  Project: The Coach Consultant")
    print(f"{'='*50}\n")

    # 1. Analyze CLAUDE.md
    claude_path = PROJECT_ROOT / "CLAUDE.md"
    claude_info = analyze_file(claude_path)
    if claude_info:
        print(f"CLAUDE.md: {claude_info['chars']:,} chars / ~{claude_info['tokens']:,} tokens")

    if args.claude_only:
        print("\n(Claude-only mode — skipping skill and doc files)")
        skill_infos = []
        doc_infos = []
        duplicates = []
    else:
        # 2. Find and analyze skill files
        skill_files = list(PROJECT_ROOT.rglob("skill.md")) + list(PROJECT_ROOT.rglob("SKILL.md"))
        skill_infos = []
        for sf in skill_files:
            info = analyze_file(sf)
            if info:
                skill_infos.append(info)
                print(f"  {info['path']}: {info['chars']:,} chars / ~{info['tokens']:,} tokens")

        if args.skills_only:
            doc_infos = []
            duplicates = []
        else:
            # 3. Find and analyze doc files
            doc_files = list((PROJECT_ROOT / "docs").rglob("*.md")) + list((PROJECT_ROOT / "docs").rglob("*.txt"))
            doc_infos = []
            for df in doc_files:
                info = analyze_file(df)
                if info:
                    doc_infos.append(info)

            print(f"\n  docs/ total: {sum(d['chars'] for d in doc_infos):,} chars / ~{sum(d['tokens'] for d in doc_infos):,} tokens")

            # 4. Find duplicates
            claude_text = claude_path.read_text(encoding="utf-8")
            duplicates = find_duplicates(claude_text, skill_infos)
            if duplicates:
                print(f"\n  Duplicates found: {sum(d['count'] for d in duplicates)} phrases across {len(duplicates)} skill files")

    # Generate report
    report = generate_report(claude_info, skill_infos, doc_infos, duplicates)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d")
    output_path = OUTPUT_DIR / f"TOKEN-AUDIT-REPORT-{now}.md"
    with open(output_path, "w") as f:
        f.write(report)

    print(f"\n{'='*50}")
    print(f"  Report saved: {output_path}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
