#!/usr/bin/env python3
"""
Pull last 30 days of videos per channel with yt-dlp.

For each handle in CHANNELS, fetches metadata for every upload posted in the last 30 days
(long-form + Shorts). Saves raw JSON per channel to data/{handle_clean}-raw-{date}.json.

yt-dlp's `--dateafter`, `--flat-playlist`, and `--print-json` give us metadata-only
without downloading any media. Transcript pulling happens in the analyse step (only
the top 5 per channel need captions, no point pulling captions for all 30).

Usage:
    python3 scripts/scrape_channels.py [--days 30] [--max-videos 50]
"""
import argparse
import subprocess
import sys
import re
from datetime import datetime, timedelta, timezone

from _shared import CHANNELS, DATA_DIR, today_str, write_json


def handle_to_filename(handle: str) -> str:
    return handle.lstrip("@").lower()


def fetch_channel_videos(handle: str, days: int, max_videos: int):
    """Return a list of video metadata dicts for one channel."""
    date_after = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y%m%d")

    # yt-dlp by channel handle URL. The /videos tab gives long-form, /shorts the shorts.
    # Combining both via dump-single-json then a search through entries.
    urls = [
        f"https://www.youtube.com/{handle}/videos",
        f"https://www.youtube.com/{handle}/shorts",
    ]

    all_entries = []
    for url in urls:
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--dump-single-json",
            "--playlist-end", str(max_videos),
            "--dateafter", date_after,
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        if result.returncode != 0:
            print(f"[warn] {handle} on {url}: yt-dlp failed", file=sys.stderr)
            print(result.stderr[:400], file=sys.stderr)
            continue
        try:
            import json as _json
            data = _json.loads(result.stdout)
        except Exception as e:
            print(f"[warn] {handle} on {url}: could not parse yt-dlp output: {e}", file=sys.stderr)
            continue
        entries = data.get("entries") or []
        all_entries.extend(entries)

    # Re-fetch full metadata per video (flat-playlist gives only IDs and basic stats).
    # We need view_count, like_count, publish date, description, channel name.
    enriched = []
    for entry in all_entries:
        video_id = entry.get("id")
        if not video_id:
            continue
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--dump-single-json",
            "--no-warnings",
            f"https://www.youtube.com/watch?v={video_id}",
        ]
        r2 = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if r2.returncode != 0:
            continue
        try:
            import json as _json
            v = _json.loads(r2.stdout)
        except Exception:
            continue
        enriched.append({
            "id": video_id,
            "title": v.get("title"),
            "description": (v.get("description") or "")[:2000],  # cap description size
            "channel": v.get("channel"),
            "channel_id": v.get("channel_id"),
            "duration_sec": v.get("duration"),
            "upload_date": v.get("upload_date"),  # YYYYMMDD
            "timestamp": v.get("timestamp"),
            "view_count": v.get("view_count"),
            "like_count": v.get("like_count"),
            "comment_count": v.get("comment_count"),
            "thumbnail": v.get("thumbnail"),
            "webpage_url": v.get("webpage_url"),
            "is_short": (v.get("duration") or 0) < 70,  # heuristic
            "tags": v.get("tags") or [],
        })

    # Filter to only those posted within the date window
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y%m%d")
    enriched = [v for v in enriched if (v.get("upload_date") or "00000000") >= cutoff]

    return enriched


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--max-videos", type=int, default=50)
    parser.add_argument("--only", type=str, default=None,
                        help="Run for a single handle (e.g. @AlexHormozi) for debugging")
    args = parser.parse_args()

    date = today_str()
    targets = [c for c in CHANNELS if (args.only is None or c["handle"] == args.only)]
    if not targets:
        print(f"[fatal] no channels matched --only={args.only}", file=sys.stderr)
        sys.exit(1)

    summary = {}
    for ch in targets:
        handle = ch["handle"]
        print(f"[scrape] {handle} ({ch['name']})", file=sys.stderr)
        videos = fetch_channel_videos(handle, args.days, args.max_videos)
        out_path = DATA_DIR / f"{handle_to_filename(handle)}-raw-{date}.json"
        write_json(out_path, {
            "handle": handle,
            "channel_name": ch["name"],
            "tier": ch["tier"],
            "scraped_at": date,
            "days_window": args.days,
            "videos": videos,
        })
        print(f"[ok] {handle}: {len(videos)} videos -> {out_path.name}", file=sys.stderr)
        summary[handle] = len(videos)

    print()
    print("Scrape summary:")
    for h, n in summary.items():
        print(f"  {h}: {n}")


if __name__ == "__main__":
    main()
