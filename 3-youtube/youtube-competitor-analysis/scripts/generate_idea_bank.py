#!/usr/bin/env python3
"""
Ben Video Idea Bank.

For each of the 5 IDEA_BANK_HANDLES, pick the single most recent video from
the raw scrape, fetch its transcript + thumbnail, send to Gemini with a
specialised prompt that returns a fully briefed video idea for Ben.

Output: data/idea_bank-{date}.json with one entry per channel.

Usage:
    python3 scripts/generate_idea_bank.py
"""
import argparse
import base64
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from _shared import IDEA_BANK_HANDLES, CHANNELS, DATA_DIR, ENV, today_str, write_json, read_json, PAIN_LAYERS

GEMINI_API_KEY = ENV.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


def handle_to_filename(handle: str) -> str:
    return handle.lstrip("@").lower()


def fetch_transcript(video_id: str) -> str:
    """Pull auto-subtitle via yt-dlp, return as plain text (first 2500 chars for idea bank — longer than analyse_top5)."""
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
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            return ""
        vtts = list(Path(td).glob(f"{video_id}*.vtt"))
        if not vtts:
            return ""
        raw = vtts[0].read_text(errors="ignore")

    import re
    lines = []
    for ln in raw.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("WEBVTT") or "-->" in ln or ln.isdigit():
            continue
        ln = re.sub(r"<[^>]+>", "", ln)
        lines.append(ln)

    deduped = []
    for ln in lines:
        if not deduped or deduped[-1] != ln:
            deduped.append(ln)

    return " ".join(deduped)[:2500]


def fetch_thumbnail_bytes(url: str) -> bytes | None:
    if not url:
        return None
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return resp.read()
    except Exception:
        return None


IDEA_BANK_PROMPT = """You are a senior content strategist for Ben Hawksworth at The Coach Consultant (TCC).

Ben's audience and brand context:
- Audience (avatar name: Sam): open business owners and service providers, 35-50 years old, £100K-£500K annual revenue, founder-led service businesses across coaching, agency, consulting, course creation, health, B2B. UK-heavy plus Dubai/Spain/Australia. Men and women equally.
- Hero pain: The Guesswork Tax (every business decision is a guess because they have no AI intelligence behind it).
- Close-second pain: Bottleneck Identity (founder is the bottleneck, everything runs through them).
- Six pain layers: guesswork_tax, bottleneck_identity, ai_era_anxiety, trust_trauma, plate_anxiety, partner_pressure.
- Offer: 4-Step Programme — (1) Growth Intelligence Audit, (2) Claude AI Specialist Setup, (3) Personal Brand and AI Adoption Roadmap, (4) 90-Day Growth Map.
- Voice: Yorkshire-direct, mate-to-mate, British English. NEVER em-dashes. Signature phrases include "You are the bottleneck of your business", "Stop guessing growth", "AI intelligence not AI tools", "Personal brand plus AI adoption", "Done-with-you, not done-by-yourself, not done-to-you".
- FORBIDDEN phrases: "transformation journey", "unlock", "level up", "dive in", "game changer", "leverage", "here's the thing".

A competitor just posted a YouTube video. Your job: brief Ben a TCC video idea he could shoot this week that takes inspiration from the competitor's hook, structure, or angle, but rewrites everything into TCC voice + Sam pain + TCC offer.

Return ONLY a valid JSON object with these fields:

{
  "competitor_takeaway": "one sentence: what makes the competitor's video work (the hook angle, the structure move, the psychological lever they pulled)",
  "ben_title": "the video title Ben could shoot (max 80 chars, sounds like Ben, no em-dashes, no forbidden phrases)",
  "ben_hook": "the first 8-15 seconds of Ben's video, verbatim script (Yorkshire-direct, opens with a TCC signature phrase or a Sam-pain line)",
  "pain_anchor": "one of: guesswork_tax | bottleneck_identity | ai_era_anxiety | trust_trauma | plate_anxiety | partner_pressure",
  "format": "long_form | short | podcast_clip",
  "structure_beats": ["bullet 1 (Sam-pain agitate)", "bullet 2 (insight or proof)", "bullet 3 (4-Step Programme reference)", "bullet 4 (CTA)"],
  "cta": "one sentence Ben says at the end (always references the Growth Intelligence Audit or the 4-Step Programme)",
  "why_this_works_for_sam": "one sentence explaining why this resonates with the avatar profile above"
}

Output JSON only. No markdown fences."""


def gemini_idea(competitor_video, transcript_text, thumbnail_bytes) -> dict | None:
    if not GEMINI_API_KEY:
        print("[fatal] GEMINI_API_KEY not in .env", file=sys.stderr)
        sys.exit(1)

    parts = [
        {"text": IDEA_BANK_PROMPT},
        {"text": f"\n\nCompetitor channel: {competitor_video.get('channel', '')}"},
        {"text": f"\nCompetitor video title: {competitor_video.get('title', '')}"},
        {"text": f"\nCompetitor video URL: {competitor_video.get('webpage_url', '')}"},
        {"text": f"\nCompetitor description (truncated): {(competitor_video.get('description') or '')[:1000]}"},
        {"text": f"\n\nCompetitor transcript snippet (first 2500 chars):\n{transcript_text}\n"},
    ]
    if thumbnail_bytes:
        parts.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": base64.standard_b64encode(thumbnail_bytes).decode(),
            }
        })

    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": 0.4,
            "response_mime_type": "application/json",
        },
    }

    req = urllib.request.Request(
        f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"[warn] Gemini call failed for {competitor_video.get('id')}: {e}", file=sys.stderr)
        return None

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(text)
        if parsed.get("pain_anchor") not in PAIN_LAYERS:
            parsed["pain_anchor"] = "no_anchor"
        return parsed
    except Exception as e:
        print(f"[warn] parse failed for {competitor_video.get('id')}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default=today_str())
    args = parser.parse_args()

    date = args.date
    bank_entries = []

    for handle in IDEA_BANK_HANDLES:
        ch_meta = next((c for c in CHANNELS if c["handle"] == handle), None)
        if not ch_meta:
            continue
        raw_path = DATA_DIR / f"{handle_to_filename(handle)}-raw-{date}.json"
        raw = read_json(raw_path)
        if not raw or not raw.get("videos"):
            print(f"[skip] {handle}: no raw scrape", file=sys.stderr)
            continue

        # Most recent video by upload_date (YYYYMMDD)
        videos = raw["videos"]
        videos_sorted = sorted(videos, key=lambda v: v.get("upload_date") or "00000000", reverse=True)
        latest = videos_sorted[0]

        print(f"[idea] {handle} :: {latest.get('title', '')[:60]}", file=sys.stderr)
        transcript = fetch_transcript(latest["id"])
        thumb = fetch_thumbnail_bytes(latest.get("thumbnail"))
        idea = gemini_idea(latest, transcript, thumb)
        if not idea:
            continue

        bank_entries.append({
            "handle": handle,
            "channel_name": ch_meta["name"],
            "competitor_video": {
                "id": latest["id"],
                "title": latest.get("title"),
                "url": latest.get("webpage_url"),
                "upload_date": latest.get("upload_date"),
                "view_count": latest.get("view_count"),
                "like_count": latest.get("like_count"),
                "is_short": latest.get("is_short"),
                "thumbnail": latest.get("thumbnail"),
            },
            "ben_idea": idea,
        })
        time.sleep(0.5)

    out_path = DATA_DIR / f"idea_bank-{date}.json"
    write_json(out_path, {
        "generated_for_date": date,
        "entries": bank_entries,
    })
    print(f"[ok] idea bank -> {out_path}  ({len(bank_entries)} entries)")


if __name__ == "__main__":
    main()
