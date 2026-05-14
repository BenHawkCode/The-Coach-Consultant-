#!/usr/bin/env python3
"""
Render the weekly Ben Video Idea Bank as a styled Google Doc.

Reads: data/idea_bank-{date}.json
Output: a Google Doc titled "Video Idea Bank for Ben - Week of {date}" in the
YouTube competitor analysis Drive folder.

Magazine-style treatment mirroring meta-ads-daily-action-plan-new (kicker, serif H1,
teal subtitle, snapshot table, serif H2 sections). Per-channel entries each with
the competitor video card, Ben's idea title, hook, structure beats, CTA, and a
"why this works for Sam" line.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from _shared import DATA_DIR, OUTPUTS_DIR, today_str, read_json

# --- palette, mirrors meta-ads-daily-action-plan-new ---
TEAL = "#5C8B7F"
DARK = "#0a0a0a"
TEAL_LIGHT_BG = "#e8f0ed"
RED = "#d63b2f"
RED_LIGHT_BG = "#fff0ee"
LIGHT_GREY = "#f5f5f5"


def gws(cmd_args):
    cmd = ["gws"] + cmd_args
    result = subprocess.run(cmd, capture_output=True, text=True)
    out = re.sub(r"^Using keyring backend.*\n", "", result.stdout)
    out = re.sub(r"^Warning:.*\n", "", out, flags=re.MULTILINE)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        print(f"[fail] {' '.join(cmd_args)}", file=sys.stderr)
        print(out, file=sys.stderr)
        raise


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


def escape(text: str) -> str:
    if text is None:
        return ""
    return str(text).replace("<", "&lt;").replace(">", "&gt;")


def humanise_format(f: str) -> str:
    return {
        "long_form": "Long-form",
        "short": "Short",
        "podcast_clip": "Podcast clip",
    }.get(f, f)


def fmt_upload_date(s: str) -> str:
    if not s or len(s) < 8:
        return "n/a"
    try:
        return datetime.strptime(s, "%Y%m%d").strftime("%d %b")
    except Exception:
        return s


def fmt_count(n) -> str:
    if not n:
        return "0"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(n)


def build_html(bank: dict, pretty_date: str) -> str:
    entries = bank.get("entries", [])

    entries_html = ""
    for i, entry in enumerate(entries, 1):
        comp = entry.get("competitor_video", {})
        idea = entry.get("ben_idea", {})
        channel_name = entry.get("channel_name", "")
        handle = entry.get("handle", "")
        comp_title = escape(comp.get("title"))
        comp_url = comp.get("url", "")
        views = fmt_count(comp.get("view_count"))
        likes = fmt_count(comp.get("like_count"))
        upload_d = fmt_upload_date(comp.get("upload_date"))
        is_short = comp.get("is_short")
        comp_format = "Short" if is_short else "Long-form"

        ben_title = escape(idea.get("ben_title"))
        ben_hook = escape(idea.get("ben_hook"))
        ben_pain = humanise_pain(idea.get("pain_anchor", "no_anchor"))
        ben_format = humanise_format(idea.get("format", "long_form"))
        ben_cta = escape(idea.get("cta"))
        takeaway = escape(idea.get("competitor_takeaway"))
        why_sam = escape(idea.get("why_this_works_for_sam"))

        beats = idea.get("structure_beats") or []
        beats_html = "".join([f'<li style="margin:0 0 4px 0;">{escape(b)}</li>' for b in beats])

        entries_html += f"""
<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:36px 0 10px 0; line-height:1.1;">
{i}. {channel_name}
</h2>

<p style="margin:0 0 14px 0; padding:12px 16px; background-color:{LIGHT_GREY}; border-left:3px solid {DARK};">
<strong>What they posted:</strong> "{comp_title}"<br>
<span style="color:{TEAL}; font-size:10pt;">{handle} · {upload_d} · {views} views · {likes} likes · {comp_format}</span> <a href="{comp_url}" style="color:{TEAL}; font-size:10pt;">[link]</a>
</p>

<p style="margin:0 0 12px 0;"><strong style="color:{TEAL};">Why it works.</strong> {takeaway}</p>

<p style="margin:18px 0 6px 0; font-size:14pt; font-weight:700; color:{DARK};">
Ben's video: {ben_title}
</p>

<p style="margin:0 0 8px 0;"><strong style="color:{TEAL};">Hook (first 8-15 seconds).</strong> "{ben_hook}"</p>

<p style="margin:0 0 6px 0;"><strong style="color:{TEAL};">Structure beats.</strong></p>
<ul style="margin:0 0 12px 18px; padding-left:18px;">
{beats_html}
</ul>

<p style="margin:0 0 8px 0;"><strong style="color:{TEAL};">CTA.</strong> {ben_cta}</p>

<p style="margin:0 0 8px 0;"><strong style="color:{TEAL};">Pain anchor.</strong> {ben_pain} &nbsp; · &nbsp; <strong style="color:{TEAL};">Format.</strong> {ben_format}</p>

<p style="margin:0 0 24px 0; padding:10px 14px; background-color:{TEAL_LIGHT_BG}; border-left:3px solid {TEAL};">
<strong>Why this works for Sam.</strong> {why_sam}
</p>
"""

    if not entries_html:
        entries_html = "<p>No idea bank entries this week. Check that the scrape ran and produced raw video files.</p>"

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Video Idea Bank for Ben</title></head>
<body style="font-family:'Helvetica Neue',Arial,sans-serif; font-size:11pt; color:{DARK}; line-height:1.6;">

<p style="font-size:10pt; font-weight:700; color:{TEAL}; letter-spacing:0.5px; margin:0 0 24px 0;">
THE COACH CONSULTANT · VIDEO IDEA BANK
</p>

<h1 style="font-family:'Playfair Display',Georgia,serif; font-size:36pt; font-weight:800; color:{DARK}; margin:0 0 12px 0; line-height:1.1;">
Week of {pretty_date}
</h1>

<p style="font-family:'Helvetica Neue',Arial,sans-serif; font-size:14pt; color:{TEAL}; margin:0 0 28px 0; line-height:1.4;">
Five video ideas Ben can shoot this week, each built from the latest video posted by a TCC-aligned competitor. Hook, structure, and CTA already in TCC voice and mapped to Sam's pain layers.
</p>

<p style="margin:0 0 28px 0; padding:14px 16px; background-color:{LIGHT_GREY}; border-left:3px solid {DARK};">
<strong>How to use this brief.</strong> Each section is one shootable idea. The hook is verbatim, the structure beats are the spine of the video, the CTA always references the Growth Intelligence Audit or the 4-Step Programme. Pick the one or two you want this week. Voice is already TCC, no rewriting needed before recording.
</p>

{entries_html}

</body>
</html>
"""
    return html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, default=today_str())
    parser.add_argument("--folder-id", type=str, default=None)
    args = parser.parse_args()

    date = args.date
    bank = read_json(DATA_DIR / f"idea_bank-{date}.json")
    if not bank:
        print(f"[fatal] no idea bank file at data/idea_bank-{date}.json", file=sys.stderr)
        sys.exit(1)

    dt = datetime.strptime(date, "%Y-%m-%d")
    pretty_date = dt.strftime("%d %B %Y")

    folder_id = args.folder_id
    if not folder_id:
        fid_path = OUTPUTS_DIR / "folder_id.txt"
        if fid_path.exists():
            folder_id = fid_path.read_text().strip()
        else:
            print("[fatal] no folder_id", file=sys.stderr)
            sys.exit(1)

    title = f"Video Idea Bank for Ben - Week of {date}"
    html = build_html(bank, pretty_date)

    html_path = "yt_idea_bank_doc.html"
    Path(html_path).write_text(html, encoding="utf-8")

    upload = gws([
        "drive", "files", "create",
        "--upload", html_path,
        "--params", json.dumps({
            "name": title,
            "mimeType": "application/vnd.google-apps.document",
            "parents": [folder_id],
        }),
        "--format", "json",
    ])
    doc_id = upload["id"]
    mime = upload.get("mimeType", "?")

    if mime != "application/vnd.google-apps.document":
        converted = gws([
            "drive", "files", "copy",
            "--params", json.dumps({"fileId": doc_id}),
            "--json", json.dumps({
                "name": title,
                "mimeType": "application/vnd.google-apps.document",
                "parents": [folder_id],
            }),
            "--format", "json",
        ])
        gws(["drive", "files", "delete", "--params", json.dumps({"fileId": doc_id})])
        doc_id = converted["id"]

    Path(html_path).unlink()
    Path("download.html").unlink(missing_ok=True)

    print(f"GDOC: https://docs.google.com/document/d/{doc_id}/edit")


if __name__ == "__main__":
    main()
