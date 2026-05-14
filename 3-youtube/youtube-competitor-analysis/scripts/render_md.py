#!/usr/bin/env python3
"""
Generate the weekly markdown brief from data/youtube_competitors.json.

Output: outputs/{YYYY-MM-DD}.md
"""
import sys
from datetime import datetime, timezone

from _shared import DATA_DIR, OUTPUTS_DIR, today_str, read_json, PAIN_LAYERS


def humanise_pain(p: str) -> str:
    return {
        "guesswork_tax": "Guesswork Tax",
        "bottleneck_identity": "Bottleneck Identity",
        "ai_era_anxiety": "AI Era Anxiety",
        "trust_trauma": "Trust Trauma",
        "plate_anxiety": "Plate Anxiety",
        "partner_pressure": "Partner Pressure",
        "no_anchor": "No anchor",
    }.get(p, p)


def main():
    date = today_str()
    aggregate = read_json(DATA_DIR / "youtube_competitors.json")
    if not aggregate:
        print("[fatal] no aggregate at data/youtube_competitors.json", file=sys.stderr)
        sys.exit(1)

    dt = datetime.strptime(date, "%Y-%m-%d")
    pretty_date = dt.strftime("%d %B %Y")

    hook_dist = aggregate.get("hook_type_distribution", {})
    pain_cov = aggregate.get("pain_coverage", {})
    format_mix = aggregate.get("format_mix", {})
    top_hooks = aggregate.get("top_hooks", [])
    framework_counts = aggregate.get("framework_counts", {})
    missing_pains = aggregate.get("missing_pains", [])
    priority = aggregate.get("priority_move", "")

    dominant_hook = max(hook_dist, key=hook_dist.get) if hook_dist else "n/a"
    dominant_pain = max(pain_cov, key=pain_cov.get) if pain_cov else "n/a"

    # Subtitle: one sentence summarising the strongest pattern
    if missing_pains and dominant_pain != "n/a":
        subtitle = (
            f"Competitors led with {humanise_pain(dominant_pain)} this week. "
            f"Pain coverage missing: {', '.join(humanise_pain(p) for p in missing_pains[:2])}."
        )
    else:
        subtitle = f"Strongest hook type this week: {dominant_hook}. Dominant pain anchor: {humanise_pain(dominant_pain)}."

    lines = []
    lines.append("The Coach Consultant · YouTube Competitor Analysis")
    lines.append("")
    lines.append(f"# Week of {pretty_date}")
    lines.append("")
    lines.append(subtitle)
    lines.append("")
    lines.append("| Channels Tracked | Videos Analysed | Top Hook Type |")
    lines.append("|---|---|---|")
    lines.append(f"| {aggregate.get('channels_tracked', 0)} | {aggregate.get('videos_analysed', 0)} | {dominant_hook.title()} |")
    lines.append("")

    # This Week's Number
    lines.append("## This Week's Number")
    lines.append("")
    hook_summary = ", ".join([f"{k.title()} {v}" for k, v in hook_dist.items()])
    pain_summary = ", ".join([f"{humanise_pain(k)} {v}" for k, v in pain_cov.items() if v > 0])
    fmt_summary = ", ".join([f"{k.replace('_', ' ').title()} {int(v * 100)}%" for k, v in format_mix.items() if v > 0])
    lines.append(f"- Videos analysed: {aggregate.get('videos_analysed', 0)} across {aggregate.get('channels_tracked', 0)} channels")
    lines.append(f"- Hook types: {hook_summary or 'no clear pattern'}")
    lines.append(f"- Pain anchors hit: {pain_summary or 'no clear pattern'}")
    lines.append(f"- Format mix: {fmt_summary or 'no clear pattern'}")
    skipped = aggregate.get("channels_skipped") or []
    if skipped:
        lines.append(f"- Channels skipped this week (no recent uploads or scrape failed): {', '.join(skipped)}")
    lines.append("")

    # Top Hooks
    lines.append("## Top Hooks This Week (verbatim swipe file)")
    lines.append("")
    for i, h in enumerate(top_hooks, 1):
        hook_text = (h.get("hook") or "").strip().strip('"').strip("'")
        ch_name = h.get("channel_name") or h.get("channel") or ""
        pain = humanise_pain(h.get("pain") or "no_anchor")
        lines.append(f"{i}. \"{hook_text}\" ({ch_name}, {pain})")
    lines.append("")

    # Top Ideas from These Videos (summaries, not verbatim hooks)
    lines.append("## Top Ideas from These Videos")
    lines.append("")
    top_ideas = aggregate.get("top_ideas") or []
    if top_ideas:
        for i, idea in enumerate(top_ideas, 1):
            summary = (idea.get("summary") or "").strip()
            ch_name = idea.get("channel_name") or idea.get("channel") or ""
            pain = humanise_pain(idea.get("pain") or "no_anchor")
            title = (idea.get("title") or "").strip()
            lines.append(f"{i}. {summary} ({ch_name} — \"{title}\", {pain})")
    else:
        lines.append("No video summaries available this week.")
    lines.append("")

    # Pain Points Covered This Week
    lines.append("## Pain Points Covered This Week")
    lines.append("")
    pain_cov = aggregate.get("pain_coverage", {})
    hit_pains = sorted(
        [(p, c) for p, c in pain_cov.items() if c > 0 and p != "no_anchor"],
        key=lambda x: x[1],
        reverse=True,
    )
    if hit_pains:
        lines.append("Hit this week:")
        for i, (p, c) in enumerate(hit_pains):
            tag = " (most over-indexed)" if i == 0 else ""
            lines.append(f"- {humanise_pain(p)}: {c} hits{tag}")
        lines.append("")
    no_anchor = pain_cov.get("no_anchor", 0)
    if no_anchor:
        lines.append(f"- No clear pain anchor: {no_anchor} hits (generic motivation / identity callouts)")
        lines.append("")
    if missing_pains:
        lines.append("Missing this week (TCC opportunity):")
        for p in missing_pains:
            lines.append(f"- {humanise_pain(p)}: 0 hits")
        lines.append("")
    else:
        lines.append("All six pain layers represented across the competitor pool this week. No clear gap.")
        lines.append("")

    # Framework Patterns
    lines.append("## Framework Patterns")
    lines.append("")
    if framework_counts:
        top_fw = list(framework_counts.items())[:5]
        fw_text = ", ".join([f"{name} ({count})" for name, count in top_fw])
        lines.append(f"Frameworks spotted across the 50-video pool: {fw_text}.")
    else:
        lines.append("No named frameworks recurred enough this week to flag.")
    lines.append("")
    lines.append(
        f"Production format mix tells the story too. {fmt_summary or 'No clear pattern'} suggests where competitors are placing their volume bets this week."
    )
    lines.append("")

    # This Week's Priority
    lines.append("## This Week's Priority")
    lines.append("")
    lines.append(priority)
    lines.append("")

    out_path = OUTPUTS_DIR / f"{date}.md"
    out_path.write_text("\n".join(lines))
    print(f"[ok] markdown -> {out_path}")


if __name__ == "__main__":
    main()
