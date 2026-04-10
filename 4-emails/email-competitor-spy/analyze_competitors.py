#!/usr/bin/env python3
"""
Email Competitor Spy - Newsletter Analysis Script
Analyses competitor_newsletters.json and generates an intelligence report.

Usage:
    python analyze_competitors.py                    # Full report
    python analyze_competitors.py --sender "Alex Hormozi"  # Single sender
    python analyze_competitors.py --focus hooks       # Focus area only
"""

import json
import os
import sys
import argparse
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "data" / "competitor_newsletters.json"
OUTPUT_DIR = SCRIPT_DIR / "outputs"


def load_data():
    """Load competitor newsletter data."""
    if not DATA_FILE.exists():
        print(f"Error: Data file not found at {DATA_FILE}")
        print("Pull latest from Antonio's repo or place competitor_newsletters.json in data/")
        sys.exit(1)

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def classify_subject_type(subject):
    """Classify subject line into pattern types."""
    subject_lower = subject.lower()

    if any(c in subject_lower for c in ["?", "how to", "what", "why", "do you"]):
        return "Question"
    if any(c in subject_lower for c in ["%", "x ", "£", "$", "k ", "million"]):
        return "Metric/Result"
    if ":" in subject and subject.index(":") < 15:
        return "Named Format"
    if any(w in subject_lower for w in ["only", "never", "won't", "don't", "lie", "myth"]):
        return "Contrarian"
    if subject[0].islower():
        return "Lowercase Casual"
    if any(w in subject_lower for w in ["free", "get", "your"]):
        return "Direct Offer"

    return "Statement"


def classify_hook_type(hook):
    """Classify hook into opening style."""
    hook_lower = hook.lower()

    if any(w in hook_lower for w in ["picture this", "when i", "this weekend", "real relationships"]):
        return "Story"
    if any(w in hook_lower for w in ["some days", "you close", "overwhelmed", "struggling"]):
        return "Pain Paint"
    if any(w in hook_lower for w in ["here's my prediction", "you can only", "half the"]):
        return "Contrarian"
    if any(w in hook_lower for w in ["how one", "here's the biggest", "the best way"]):
        return "Value Drop"
    if any(w in hook_lower for w in ["i'm taking a break", "do you want to see", "you asked me"]):
        return "Pattern Interrupt"
    if any(w in hook_lower for w in ["as leaders", "it's not about", "in this world"]):
        return "Authority Statement"

    return "Direct Opening"


def classify_cta_type(cta):
    """Classify CTA strategy."""
    cta_lower = cta.lower()

    if "no" in cta_lower and ("cta" in cta_lower or "explicit" in cta_lower):
        return "No CTA"
    if "reply" in cta_lower:
        return "Reply CTA"
    if "ps:" in cta_lower or "ps " in cta_lower:
        return "PS Soft Sell"
    if any(w in cta_lower for w in ["apply", "book", "register", "get", "click"]):
        return "Direct CTA"
    if any(w in cta_lower for w in ["youtube", "spotify", "apple", "watch", "listen"]):
        return "Multi-Platform"
    if "story" in cta_lower:
        return "Story (No Sell)"

    return "Soft CTA"


def classify_offer_type(offer):
    """Classify offer positioning."""
    offer_lower = offer.lower()

    if "none" in offer_lower and "value" in offer_lower:
        return "Pure Value"
    if "none" in offer_lower and ("story" in offer_lower or "motivation" in offer_lower):
        return "Pure Content"
    if "none" in offer_lower and "thought" in offer_lower:
        return "Thought Leadership"
    if "free" in offer_lower:
        return "Free Resource"
    if any(w in offer_lower for w in ["agency", "program", "coaching", "course"]):
        return "Paid Offer"
    if "affiliate" in offer_lower:
        return "Affiliate"
    if any(w in offer_lower for w in ["ticket", "event"]):
        return "Event"
    if "product" in offer_lower:
        return "Product"

    return "Mixed"


def analyze_all(data):
    """Run full analysis on all competitors."""
    total_senders = len(data)
    total_newsletters = sum(len(s["newsletters"]) for s in data)

    # Collect all classifications
    subject_types = Counter()
    hook_types = Counter()
    cta_types = Counter()
    offer_types = Counter()
    platforms = Counter()
    frequencies = {}
    tones = []
    all_subjects = []
    all_hooks = []

    for sender in data:
        platforms[sender["platform"]] += 1
        frequencies[sender["sender"]] = sender["frequency"]

        for nl in sender["newsletters"]:
            subject_types[classify_subject_type(nl["subject"])] += 1
            hook_types[classify_hook_type(nl["hook"])] += 1
            cta_types[classify_cta_type(nl["cta"])] += 1
            offer_types[classify_offer_type(nl["offer"])] += 1
            tones.append(nl["tone"])
            all_subjects.append({"sender": sender["sender"], "subject": nl["subject"], "type": classify_subject_type(nl["subject"])})
            all_hooks.append({"sender": sender["sender"], "hook": nl["hook"][:100], "type": classify_hook_type(nl["hook"])})

    # Subject line length analysis
    subject_lengths = [len(s["subject"]) for s in all_subjects]
    avg_length = sum(subject_lengths) / len(subject_lengths) if subject_lengths else 0

    return {
        "total_senders": total_senders,
        "total_newsletters": total_newsletters,
        "subject_types": subject_types,
        "hook_types": hook_types,
        "cta_types": cta_types,
        "offer_types": offer_types,
        "platforms": platforms,
        "frequencies": frequencies,
        "all_subjects": all_subjects,
        "all_hooks": all_hooks,
        "avg_subject_length": avg_length,
        "tones": tones,
    }


def generate_report(data, analysis, sender_filter=None):
    """Generate markdown intelligence report."""
    now = datetime.now().strftime("%Y-%m-%d")
    title = f"Email Competitor Spy Report — {now}"

    lines = []
    lines.append(f"# {title}\n")
    lines.append(f"**Data Source:** Antonio's scraping pipeline (`competitor_newsletters.json`)")
    lines.append(f"**Senders Tracked:** {analysis['total_senders']}")
    lines.append(f"**Newsletters Analysed:** {analysis['total_newsletters']}")
    lines.append(f"**Generated:** {now}\n")
    lines.append("---\n")

    # Section 1: Competitor Overview
    lines.append("## 1. Competitor Overview\n")
    lines.append("| Sender | Platform | Frequency | Style |")
    lines.append("|--------|----------|-----------|-------|")
    for s in data:
        tone = s["newsletters"][0]["tone"][:50] if s["newsletters"] else "—"
        lines.append(f"| {s['sender']} | {s['platform']} | {s['frequency']} | {tone} |")
    lines.append("")

    # Section 2: Subject Line Formulas
    lines.append("## 2. Subject Line Formulas\n")
    lines.append(f"**Average subject length:** {analysis['avg_subject_length']:.0f} characters\n")
    lines.append("### Pattern Distribution\n")
    lines.append("| Pattern | Count | % |")
    lines.append("|---------|-------|---|")
    total_nl = analysis["total_newsletters"]
    for pattern, count in analysis["subject_types"].most_common():
        pct = (count / total_nl * 100)
        lines.append(f"| {pattern} | {count} | {pct:.0f}% |")
    lines.append("")

    lines.append("### Subject Line Examples by Type\n")
    for stype in analysis["subject_types"]:
        lines.append(f"**{stype}:**")
        examples = [s for s in analysis["all_subjects"] if s["type"] == stype]
        for ex in examples[:3]:
            lines.append(f"- \"{ex['subject']}\" — {ex['sender']}")
        lines.append("")

    # Section 3: Hook Analysis
    lines.append("## 3. Hook Pattern Analysis\n")
    lines.append("| Hook Type | Count | % |")
    lines.append("|-----------|-------|---|")
    for htype, count in analysis["hook_types"].most_common():
        pct = (count / total_nl * 100)
        lines.append(f"| {htype} | {count} | {pct:.0f}% |")
    lines.append("")

    lines.append("### Top Hooks\n")
    for h in analysis["all_hooks"][:10]:
        lines.append(f"- **{h['sender']}** ({h['type']}): \"{h['hook']}...\"")
    lines.append("")

    # Section 4: CTA Distribution
    lines.append("## 4. CTA Strategy\n")
    lines.append("| CTA Type | Count | % |")
    lines.append("|----------|-------|---|")
    for ctype, count in analysis["cta_types"].most_common():
        pct = (count / total_nl * 100)
        lines.append(f"| {ctype} | {count} | {pct:.0f}% |")
    lines.append("")

    # Section 5: Offer Positioning
    lines.append("## 5. Offer Positioning\n")
    lines.append("| Offer Type | Count | % |")
    lines.append("|------------|-------|---|")
    for otype, count in analysis["offer_types"].most_common():
        pct = (count / total_nl * 100)
        lines.append(f"| {otype} | {count} | {pct:.0f}% |")
    lines.append("")

    # Section 6: Platform Distribution
    lines.append("## 6. Sending Platforms\n")
    lines.append("| Platform | Senders |")
    lines.append("|----------|---------|")
    for platform, count in analysis["platforms"].most_common():
        lines.append(f"| {platform} | {count} |")
    lines.append("")

    # Section 7: Key Patterns for Ben
    lines.append("## 7. Key Patterns for Ben\n")
    lines.append("**Actionable takeaways mapped to The Coach Consultant's email strategy:**\n")

    patterns = [
        "**Reply CTAs work.** Dan Martell uses single-word reply triggers ('Reply COACH'). Ben already uses soft reply CTAs (CHAT, CONNECT, START). Keep this — it's proven across the market.",
        "**Pure value emails build trust.** 40%+ of competitor emails have zero CTA. Alex Hormozi's 'Mozi Minute' is pure value with no ask. Ben's BadBizAdvice series follows the same pattern and gets 59% open rates. Double down.",
        "**Lowercase subject lines signal authenticity.** Dan Martell ('you're closer than you think'), Frank Kern ('You get automation stuff you asked for?') — lowercase feels personal, not corporate. Ben should test this.",
        "**Named series create habit.** 'Mozi Minute' (Hormozi), '3MM' (Chris Williamson), '#theGAPyoumiss' (Ben). Named series build reader habit and recognition. Ben's existing series are strong.",
        "**Story hooks outperform direct hooks.** Dan Martell and James Sinclair lead with personal stories before any business lesson. Ben's personal transformation emails get 46% open rate — stories work.",
        "**Contrarian statements drive opens.** 'You can only be CEO alone' (Hormozi), 'It's a Systems Issue' (Leila). Ben's BadBizAdvice is inherently contrarian. Use this pattern more in subject lines.",
        "**PS section for soft sells.** Andrew & Pete put their offer in the PS, keeping the main email pure value. Ben could use PS for Vault mentions or upcoming events without breaking the value email format.",
    ]
    for i, p in enumerate(patterns, 1):
        lines.append(f"{i}. {p}")
    lines.append("")

    # Section 8: Ben-Voice Hybrid Examples
    lines.append("## 8. Ben-Voice Hybrid Examples\n")
    lines.append("Competitor patterns rewritten in Ben's voice:\n")

    hybrids = [
        {
            "source": "Alex Hormozi: 'Cut anything that doesn't change behavior'",
            "ben_version": "Right so I see this constantly with business owners and service providers\n\nYou're writing 2000 word emails that say nothing\n\nEvery sentence should make someone do something different\n\nIf it doesn't change behaviour delete it\n\nSound familiar",
        },
        {
            "source": "Dan Martell: 'Reply COACH'",
            "ben_version": "I built something for business owners stuck in the manual grind\n\nNot a course\n\nNot a webinar\n\nAn actual system you can plug into your business this week\n\nReply READY and I'll send it over",
        },
        {
            "source": "James Sinclair: Long-form storytelling",
            "ben_version": "Last Tuesday I sat with a service provider doing £80K a year\n\nBrilliant at what she does\n\nAbsolutely invisible online\n\nBy Friday she had her first inbound lead from content she didn't write\n\nThe shift is simple when you know what to build",
        },
    ]

    for h in hybrids:
        lines.append(f"**Source:** {h['source']}")
        lines.append(f"**Ben's version:**\n```\n{h['ben_version']}\n```\n")

    lines.append("---\n")
    lines.append(f"*Report generated by Email Competitor Spy skill — {now}*")
    lines.append(f"*Data source: Antonio's scraping pipeline (auto-updated weekly)*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Email Competitor Spy - Newsletter Analysis")
    parser.add_argument("--sender", type=str, help="Analyse a specific sender only")
    parser.add_argument("--focus", type=str, choices=["hooks", "subjects", "ctas", "offers"],
                        help="Focus on a specific analysis area")
    parser.add_argument("--output", type=str, default="report", choices=["report", "json", "print"],
                        help="Output format")
    args = parser.parse_args()

    data = load_data()

    # Filter by sender if specified
    if args.sender:
        data = [s for s in data if args.sender.lower() in s["sender"].lower()]
        if not data:
            print(f"No sender found matching '{args.sender}'")
            sys.exit(1)

    analysis = analyze_all(data)

    if args.output == "json":
        # Output raw analysis as JSON
        output = {
            "total_senders": analysis["total_senders"],
            "total_newsletters": analysis["total_newsletters"],
            "subject_types": dict(analysis["subject_types"]),
            "hook_types": dict(analysis["hook_types"]),
            "cta_types": dict(analysis["cta_types"]),
            "offer_types": dict(analysis["offer_types"]),
            "avg_subject_length": analysis["avg_subject_length"],
        }
        print(json.dumps(output, indent=2))
    elif args.output == "print":
        # Quick summary to terminal
        print(f"\n📧 Email Competitor Spy")
        print(f"{'='*40}")
        print(f"Senders: {analysis['total_senders']}")
        print(f"Newsletters: {analysis['total_newsletters']}")
        print(f"Avg subject length: {analysis['avg_subject_length']:.0f} chars")
        print(f"\nSubject types: {dict(analysis['subject_types'])}")
        print(f"Hook types: {dict(analysis['hook_types'])}")
        print(f"CTA types: {dict(analysis['cta_types'])}")
        print(f"Offer types: {dict(analysis['offer_types'])}")
    else:
        # Generate full markdown report
        report = generate_report(data, analysis, args.sender)
        OUTPUT_DIR.mkdir(exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d")
        suffix = f"-{args.sender.lower().replace(' ', '-')}" if args.sender else ""
        filename = f"EMAIL-SPY-REPORT{suffix}-{now}.md"
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w") as f:
            f.write(report)

        print(f"\n✅ Report generated: {output_path}")
        print(f"   Senders: {analysis['total_senders']}")
        print(f"   Newsletters: {analysis['total_newsletters']}")


if __name__ == "__main__":
    main()
