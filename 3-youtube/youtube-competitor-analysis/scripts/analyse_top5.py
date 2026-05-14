#!/usr/bin/env python3
"""
Pick top 5 videos per channel by views * like_rate, fetch transcript + thumbnail,
send to Gemini for structured analysis.

Output per channel: data/{handle_clean}-analysed-{date}.json with one entry per
top-5 video, each containing: hook verbatim, hook_type, framework, cta_verbatim,
pain_anchor, format, summary.

Usage:
    python3 scripts/analyse_top5.py [--top 5] [--only @handle]
"""
import argparse
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from _shared import CHANNELS, DATA_DIR, ENV, PAIN_LAYERS, today_str, write_json, read_json

GEMINI_API_KEY = ENV.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"  # fast multimodal
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


def handle_to_filename(handle: str) -> str:
    return handle.lstrip("@").lower()


def fetch_transcript(video_id: str) -> str:
    """Pull auto-subtitle via yt-dlp, return as plain text (first 1500 chars)."""
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-auto-subs",
        "--sub-lang", "en.*",
        "--sub-format", "vtt",
        "--output", f"-",  # we'll use --print to grab subtitle path differently
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    # Simpler: dump captions to a temp path
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-subs",
            "--sub-lang", "en.*",
            "--sub-format", "vtt",
            "--paths", td,
            "-o", "%(id)s.%(ext)s",
            f"https://www.youtube.com/watch?v={video_id}",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if r.returncode != 0:
            return ""
        # Find any .vtt file
        vtts = list(Path(td).glob(f"{video_id}*.vtt"))
        if not vtts:
            return ""
        raw = vtts[0].read_text(errors="ignore")

    # Strip VTT cues (timestamps + WEBVTT header)
    lines = []
    for ln in raw.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("WEBVTT") or "-->" in ln or ln.isdigit():
            continue
        # Strip inline tags like <c> </c> and timestamp tags
        import re
        ln = re.sub(r"<[^>]+>", "", ln)
        lines.append(ln)

    # Deduplicate consecutive identical lines (VTT often repeats)
    deduped = []
    for ln in lines:
        if not deduped or deduped[-1] != ln:
            deduped.append(ln)

    text = " ".join(deduped)
    return text[:1500]  # cap to keep Gemini cost down


def fetch_thumbnail_bytes(url: str) -> bytes | None:
    if not url:
        return None
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return resp.read()
    except Exception:
        return None


GEMINI_PROMPT = """You are a senior media buyer and content strategist analysing a competitor's YouTube video.

Goal: extract structured insights for a weekly competitor brief. Be precise, terse, and only fill fields you can ground in the title, description, transcript snippet, and thumbnail provided.

Return ONLY a valid JSON object with exactly these fields:

{
  "hook": "the first sentence or line of the video, verbatim from the transcript (max 200 chars). If unclear, use the first 8-12 words of the title.",
  "hook_type": "one of: statement | question | statistic | story | pattern_interrupt",
  "framework": "named framework or structure spotted (e.g. PAS, 3-act story, problem-agitate-reveal, Hormozi value equation, before/after/bridge). 'none' if no clear framework.",
  "cta_verbatim": "the call-to-action verbatim if present, else 'implicit' or 'none'",
  "pain_anchor": "one of: guesswork_tax | bottleneck_identity | ai_era_anxiety | trust_trauma | plate_anxiety | partner_pressure | no_anchor",
  "format": "long_form | short | podcast_clip",
  "summary": "one sentence (max 30 words) describing what the video does"
}

Pain anchor definitions (use these to tag):
- guesswork_tax: every business decision is a guess, lack of data/intelligence
- bottleneck_identity: founder is the bottleneck, everything runs through them
- ai_era_anxiety: AI is coming, competitors pulling ahead, fear of being replaced
- trust_trauma: burnt by mentors/courses before, debt, frameworks just the same
- plate_anxiety: cannot add more to my plate, already overloaded
- partner_pressure: relationship/family stress from business rollercoaster
- no_anchor: hook doesn't map cleanly to any of the above (identity callouts, generic motivation, etc.)

Output JSON only. No explanation, no markdown fences."""


def gemini_analyse(video, transcript_text: str, thumbnail_bytes: bytes | None) -> dict | None:
    """Call Gemini multimodal with title + description + transcript + thumbnail."""
    if not GEMINI_API_KEY:
        print("[fatal] GEMINI_API_KEY not in .env", file=sys.stderr)
        sys.exit(1)

    parts = [
        {"text": GEMINI_PROMPT},
        {"text": f"\n\nTitle: {video.get('title', '')}\n"},
        {"text": f"Description (truncated): {(video.get('description') or '')[:800]}\n"},
        {"text": f"Transcript snippet (first 1500 chars):\n{transcript_text}\n"},
    ]
    if thumbnail_bytes:
        import base64
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": base64.standard_b64encode(thumbnail_bytes).decode(),
            }
        })

    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": 0.2,
            "response_mime_type": "application/json",
        },
    }

    req = urllib.request.Request(
        f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"[warn] Gemini call failed for {video.get('id')}: {e}", file=sys.stderr)
        return None

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(text)
        # Validate pain_anchor
        if parsed.get("pain_anchor") not in PAIN_LAYERS:
            parsed["pain_anchor"] = "no_anchor"
        return parsed
    except Exception as e:
        print(f"[warn] Gemini parse failed for {video.get('id')}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--only", type=str, default=None)
    args = parser.parse_args()

    date = today_str()
    targets = [c for c in CHANNELS if (args.only is None or c["handle"] == args.only)]

    total_analysed = 0
    for ch in targets:
        handle = ch["handle"]
        raw_path = DATA_DIR / f"{handle_to_filename(handle)}-raw-{date}.json"
        raw = read_json(raw_path)
        if not raw:
            print(f"[skip] {handle}: no raw scrape at {raw_path.name}", file=sys.stderr)
            continue
        videos = raw.get("videos", [])
        if not videos:
            print(f"[skip] {handle}: 0 videos in raw scrape", file=sys.stderr)
            continue

        # Score: views * like_rate. Like rate = like_count / max(view_count, 1)
        def score(v):
            views = v.get("view_count") or 0
            likes = v.get("like_count") or 0
            if views < 100:
                return 0
            like_rate = likes / max(views, 1)
            return views * like_rate

        videos_sorted = sorted(videos, key=score, reverse=True)
        top = videos_sorted[: args.top]

        analysed = []
        for v in top:
            vid = v["id"]
            print(f"[analyse] {handle} :: {v.get('title', '')[:60]}", file=sys.stderr)
            transcript = fetch_transcript(vid)
            thumb = fetch_thumbnail_bytes(v.get("thumbnail"))
            insight = gemini_analyse(v, transcript, thumb)
            if not insight:
                continue
            insight["video_id"] = vid
            insight["title"] = v.get("title")
            insight["url"] = v.get("webpage_url")
            insight["view_count"] = v.get("view_count")
            insight["like_count"] = v.get("like_count")
            insight["upload_date"] = v.get("upload_date")
            insight["is_short"] = v.get("is_short")
            insight["channel_name"] = ch["name"]
            insight["handle"] = handle
            analysed.append(insight)
            total_analysed += 1
            time.sleep(0.5)  # gentle pacing

        out_path = DATA_DIR / f"{handle_to_filename(handle)}-analysed-{date}.json"
        write_json(out_path, {
            "handle": handle,
            "channel_name": ch["name"],
            "analysed_at": date,
            "top_n": args.top,
            "videos": analysed,
        })
        print(f"[ok] {handle}: analysed {len(analysed)}/{args.top} -> {out_path.name}", file=sys.stderr)

    print()
    print(f"Total videos analysed: {total_analysed}")


if __name__ == "__main__":
    main()
