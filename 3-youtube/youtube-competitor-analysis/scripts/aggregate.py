#!/usr/bin/env python3
"""
Read every *-analysed-{date}.json in data/, compute aggregates, write youtube_competitors.json.

Output:
- channels_tracked: 10
- videos_analysed: int
- hook_type_distribution: {statement: N, question: M, ...}
- pain_coverage: {guesswork_tax: N, bottleneck_identity: M, ...}
- format_mix: {long_form: 0.55, shorts: 0.35, podcast_clip: 0.10}
- top_hooks: top 10 verbatim hooks ranked by views * like_rate
- frameworks: count by name
- priority_move: derived from gap analysis
"""
import argparse
import sys
from collections import Counter

from _shared import DATA_DIR, PAIN_LAYERS, today_str, now_iso, write_json, read_json, CHANNELS


HOOK_TYPES = ["statement", "question", "statistic", "story", "pattern_interrupt"]
FORMATS = ["long_form", "short", "podcast_clip"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default=today_str())
    args = parser.parse_args()

    date = args.date
    all_videos = []
    channels_seen = set()

    for ch in CHANNELS:
        handle = ch["handle"]
        fname = handle.lstrip("@").lower()
        path = DATA_DIR / f"{fname}-analysed-{date}.json"
        data = read_json(path)
        if not data:
            print(f"[skip] {handle}: no analysed file at {path.name}", file=sys.stderr)
            continue
        channels_seen.add(handle)
        for v in data.get("videos", []):
            all_videos.append(v)

    if not all_videos:
        print("[fatal] no analysed videos found, aborting aggregate", file=sys.stderr)
        sys.exit(1)

    # Distributions
    hook_counts = Counter()
    pain_counts = Counter()
    format_counts = Counter()
    framework_counts = Counter()

    for v in all_videos:
        ht = v.get("hook_type")
        if ht in HOOK_TYPES:
            hook_counts[ht] += 1
        pa = v.get("pain_anchor")
        if pa in PAIN_LAYERS:
            pain_counts[pa] += 1
        fmt = v.get("format")
        if fmt in FORMATS:
            format_counts[fmt] += 1
        fw = (v.get("framework") or "").strip().lower()
        if fw and fw != "none":
            framework_counts[fw] += 1

    # Format mix as ratios
    total_videos = len(all_videos)
    format_mix = {f: round(format_counts.get(f, 0) / total_videos, 2) for f in FORMATS}

    # Top 10 hooks ranked by views * like_rate
    def score(v):
        views = v.get("view_count") or 0
        likes = v.get("like_count") or 0
        if views < 100:
            return 0
        return views * (likes / max(views, 1))

    ranked = sorted(all_videos, key=score, reverse=True)
    top_hooks = []
    top_ideas = []
    for v in ranked[:10]:
        top_hooks.append({
            "hook": v.get("hook"),
            "channel": v.get("handle"),
            "channel_name": v.get("channel_name"),
            "pain": v.get("pain_anchor"),
            "hook_type": v.get("hook_type"),
            "url": v.get("url"),
            "view_count": v.get("view_count"),
            "like_count": v.get("like_count"),
            "upload_date": v.get("upload_date"),
        })
        top_ideas.append({
            "summary": v.get("summary"),
            "title": v.get("title"),
            "channel": v.get("handle"),
            "channel_name": v.get("channel_name"),
            "pain": v.get("pain_anchor"),
            "url": v.get("url"),
            "view_count": v.get("view_count"),
        })

    # Pain coverage gap analysis -> priority_move
    missing_pains = [p for p in PAIN_LAYERS if p != "no_anchor" and pain_counts.get(p, 0) == 0]
    over_indexed = pain_counts.most_common(1)[0] if pain_counts else (None, 0)

    if missing_pains and over_indexed[0]:
        priority_move = (
            f"Competitor pool over-indexed on {over_indexed[0].replace('_', ' ')} this week "
            f"({over_indexed[1]} hits) and missed {', '.join(p.replace('_', ' ') for p in missing_pains[:2])}. "
            f"Ship two TCC pieces against {missing_pains[0].replace('_', ' ')} this week to own the lane."
        )
    elif over_indexed[0]:
        priority_move = (
            f"{over_indexed[0].replace('_', ' ').title()} is the dominant pain anchor across competitors "
            f"({over_indexed[1]}/{total_videos} videos). "
            f"Lean into Personal Brand plus AI Adoption framing on TCC content to differentiate."
        )
    else:
        priority_move = "No clear pattern. Default to Guesswork Tax content this week."

    out = {
        "week_of": date,
        "generated_at": now_iso(),
        "channels_tracked": len(channels_seen),
        "channels_skipped": sorted([ch["handle"] for ch in CHANNELS if ch["handle"] not in channels_seen]),
        "videos_analysed": total_videos,
        "hook_type_distribution": dict(hook_counts),
        "pain_coverage": {p: pain_counts.get(p, 0) for p in PAIN_LAYERS},
        "format_mix": format_mix,
        "framework_counts": dict(framework_counts.most_common()),
        "top_hooks": top_hooks,
        "top_ideas": top_ideas,
        "missing_pains": missing_pains,
        "priority_move": priority_move,
    }

    out_path = DATA_DIR / "youtube_competitors.json"
    write_json(out_path, out)
    print(f"[ok] aggregated -> {out_path}")
    print(f"     channels={out['channels_tracked']}, videos={out['videos_analysed']}, missing_pains={missing_pains}")


if __name__ == "__main__":
    main()
