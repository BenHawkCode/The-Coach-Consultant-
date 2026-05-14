#!/usr/bin/env python3
"""
Render the weekly YouTube competitor analysis as a styled Google Doc.

Reads:
- data/youtube_competitors.json (the aggregate)
- outputs/{YYYY-MM-DD}.md (the markdown brief — for parity / git diff, not parsed)

Builds an HTML doc with full inline styling (mirrors meta-ads-daily-action-plan-new
visual treatment), uploads via gws, converts to native Google Doc via mimeType.

Folder ID: outputs/folder_id.txt (created on first run, manually if absent).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from _shared import DATA_DIR, OUTPUTS_DIR, today_str, read_json

# --- palette (mirrors meta-ads-daily-action-plan-new test3_html_convert.py) ---
TEAL = "#5C8B7F"
DARK = "#0a0a0a"
TEAL_LIGHT_BG = "#e8f0ed"
RED = "#d63b2f"
RED_LIGHT_BG = "#fff0ee"


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


def build_html(aggregate: dict, pretty_date: str) -> str:
    hook_dist = aggregate.get("hook_type_distribution", {})
    pain_cov = aggregate.get("pain_coverage", {})
    format_mix = aggregate.get("format_mix", {})
    top_hooks = aggregate.get("top_hooks", [])
    top_ideas = aggregate.get("top_ideas", [])
    framework_counts = aggregate.get("framework_counts", {})
    missing_pains = aggregate.get("missing_pains", [])
    priority = aggregate.get("priority_move", "")

    dominant_hook = max(hook_dist, key=hook_dist.get) if hook_dist else "n/a"
    dominant_pain = max(pain_cov, key=pain_cov.get) if pain_cov else "n/a"

    # Subtitle
    if missing_pains and dominant_pain != "n/a":
        subtitle = (
            f"Competitors led with {humanise_pain(dominant_pain)} this week. "
            f"Pain coverage missing: {', '.join(humanise_pain(p) for p in missing_pains[:2])}."
        )
    else:
        subtitle = f"Strongest hook type this week: {dominant_hook.title()}. Dominant pain anchor: {humanise_pain(dominant_pain)}."

    hook_summary_parts = [f"{k.title()} {v}" for k, v in hook_dist.items()]
    pain_summary_parts = [f"{humanise_pain(k)} {v}" for k, v in pain_cov.items() if v > 0]
    fmt_summary_parts = [f"{k.replace('_', ' ').title()} {int(v * 100)}%" for k, v in format_mix.items() if v > 0]

    # Top hooks list (verbatim swipe)
    top_hooks_html = ""
    for i, h in enumerate(top_hooks, 1):
        hook_text = (h.get("hook") or "").strip().strip('"').strip("'").replace("<", "&lt;").replace(">", "&gt;")
        ch_name = h.get("channel_name") or h.get("channel") or ""
        pain = humanise_pain(h.get("pain") or "no_anchor")
        url = h.get("url") or ""
        top_hooks_html += (
            f'<p style="margin:0 0 10px 0;"><strong>{i}.</strong> "{hook_text}" '
            f'<span style="color:{TEAL};">({ch_name}, {pain})</span> '
            f'<a href="{url}" style="color:{TEAL}; font-size:9pt;">[link]</a></p>\n'
        )

    # Top ideas list (video summaries, not verbatim hooks)
    top_ideas_html = ""
    for i, idea in enumerate(top_ideas, 1):
        summary = (idea.get("summary") or "").strip().replace("<", "&lt;").replace(">", "&gt;")
        title = (idea.get("title") or "").strip().replace("<", "&lt;").replace(">", "&gt;")
        ch_name = idea.get("channel_name") or idea.get("channel") or ""
        pain = humanise_pain(idea.get("pain") or "no_anchor")
        url = idea.get("url") or ""
        top_ideas_html += (
            f'<p style="margin:0 0 10px 0;"><strong>{i}.</strong> {summary} '
            f'<span style="color:{TEAL};">({ch_name}, "{title}", {pain})</span> '
            f'<a href="{url}" style="color:{TEAL}; font-size:9pt;">[link]</a></p>\n'
        )
    if not top_ideas_html:
        top_ideas_html = "<p>No video summaries available this week.</p>"

    # Pain Points Covered This Week
    hit_pains = sorted(
        [(p, c) for p, c in pain_cov.items() if c > 0 and p != "no_anchor"],
        key=lambda x: x[1],
        reverse=True,
    )
    pain_covered_html = ""
    if hit_pains:
        pain_covered_html += '<p style="margin:0 0 6px 0;"><strong>Hit this week:</strong></p>\n<ul style="margin:0 0 16px 18px; padding-left:18px;">\n'
        for i, (p, c) in enumerate(hit_pains):
            tag = ' <span style="color:' + TEAL + ';">(most over-indexed)</span>' if i == 0 else ""
            pain_covered_html += f'<li style="margin:0 0 4px 0;">{humanise_pain(p)}: <strong>{c}</strong> hits{tag}</li>\n'
        pain_covered_html += '</ul>\n'

    no_anchor = pain_cov.get("no_anchor", 0)
    if no_anchor:
        pain_covered_html += (
            f'<p style="margin:0 0 16px 0; color:#666;">'
            f'No clear pain anchor: <strong>{no_anchor}</strong> hits (generic motivation / identity callouts)'
            f'</p>\n'
        )

    if missing_pains:
        pain_covered_html += (
            f'<p style="margin:0 0 6px 0; padding:14px 16px; background-color:{RED_LIGHT_BG}; '
            f'border:2px solid {RED};"><strong style="color:{RED};">Missing this week '
            f'(TCC opportunity):</strong> '
            f'{", ".join(humanise_pain(p) for p in missing_pains)}. '
            f'Competitors are not anchoring these layers in their top-performing content. '
            f'Brief one piece per missing pain, lift verbatim hooks from '
            f'<code style="background-color:#f0f0f0; padding:2px 4px;">docs/new-ip/10-pain-point-articulation.md</code>.'
            f'</p>\n'
        )
    else:
        pain_covered_html += (
            '<p style="margin:0 0 16px 0;">All six pain layers represented in the competitor pool this week. '
            'No clear gap to claim.</p>\n'
        )

    # Framework summary
    if framework_counts:
        fw_list = list(framework_counts.items())[:5]
        framework_text = ", ".join([f"{n} ({c})" for n, c in fw_list])
    else:
        framework_text = "No named frameworks recurred enough this week to flag."

    channels_skipped = aggregate.get("channels_skipped") or []
    skipped_line = ""
    if channels_skipped:
        skipped_line = (
            f"<li style=\"margin:0 0 6px 0;\">Channels skipped this week: {', '.join(channels_skipped)}</li>"
        )

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>YouTube Competitor Analysis</title></head>
<body style="font-family:'Helvetica Neue',Arial,sans-serif; font-size:11pt; color:{DARK}; line-height:1.6;">

<p style="font-size:10pt; font-weight:700; color:{TEAL}; letter-spacing:0.5px; margin:0 0 24px 0;">
THE COACH CONSULTANT · YOUTUBE COMPETITOR ANALYSIS
</p>

<h1 style="font-family:'Playfair Display',Georgia,serif; font-size:36pt; font-weight:800; color:{DARK}; margin:0 0 12px 0; line-height:1.1;">
Week of {pretty_date}
</h1>

<p style="font-family:'Helvetica Neue',Arial,sans-serif; font-size:14pt; color:{TEAL}; margin:0 0 28px 0; line-height:1.4;">
{subtitle}
</p>

<table style="border-collapse:collapse; width:100%; margin:0 0 32px 0; border:1px solid {TEAL};">
  <tr>
    <td style="border:1px solid {TEAL}; padding:14px 18px; vertical-align:top; width:33%;">
      <p style="margin:0 0 6px 0; font-size:9pt; font-weight:700; color:{DARK}; letter-spacing:0.5px;">CHANNELS TRACKED</p>
      <p style="margin:0; font-size:13pt; color:{DARK};">{aggregate.get('channels_tracked', 0)}</p>
    </td>
    <td style="border:1px solid {TEAL}; padding:14px 18px; vertical-align:top; width:33%;">
      <p style="margin:0 0 6px 0; font-size:9pt; font-weight:700; color:{DARK}; letter-spacing:0.5px;">VIDEOS ANALYSED</p>
      <p style="margin:0; font-size:13pt; color:{DARK};">{aggregate.get('videos_analysed', 0)}</p>
    </td>
    <td style="border:1px solid {TEAL}; padding:14px 18px; vertical-align:top; width:33%;">
      <p style="margin:0 0 6px 0; font-size:9pt; font-weight:700; color:{DARK}; letter-spacing:0.5px;">TOP HOOK TYPE</p>
      <p style="margin:0; font-size:13pt; color:{DARK};">{dominant_hook.title()}</p>
    </td>
  </tr>
</table>

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
This Week's Number
</h2>

<ul style="margin:0 0 16px 0; padding-left:22px;">
  <li style="margin:0 0 6px 0;">Videos analysed: {aggregate.get('videos_analysed', 0)} across {aggregate.get('channels_tracked', 0)} channels</li>
  <li style="margin:0 0 6px 0;">Hook types: {', '.join(hook_summary_parts) or 'no clear pattern'}</li>
  <li style="margin:0 0 6px 0;">Pain anchors hit: {', '.join(pain_summary_parts) or 'no clear pattern'}</li>
  <li style="margin:0 0 6px 0;">Format mix: {', '.join(fmt_summary_parts) or 'no clear pattern'}</li>
  {skipped_line}
</ul>

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
Top Hooks This Week (verbatim swipe file)
</h2>

{top_hooks_html}

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
Top Ideas from These Videos
</h2>

{top_ideas_html}

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
Pain Points Covered This Week
</h2>

{pain_covered_html}

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
Framework Patterns
</h2>

<p style="margin:0 0 10px 0;">Frameworks spotted across the competitor pool: {framework_text}</p>
<p style="margin:0 0 16px 0;">Production format mix tells the story too. {', '.join(fmt_summary_parts) or 'No clear pattern'}, indicating where competitors are placing their volume bets this week.</p>

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
This Week's Priority
</h2>

<p style="margin:0 0 16px 0; padding:14px 16px; background-color:{TEAL_LIGHT_BG}; border-left:3px solid {TEAL};">
{priority}
</p>

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
    aggregate = read_json(DATA_DIR / "youtube_competitors.json")
    if not aggregate:
        print("[fatal] no aggregate at data/youtube_competitors.json", file=sys.stderr)
        sys.exit(1)

    dt = datetime.strptime(date, "%Y-%m-%d")
    pretty_date = dt.strftime("%d %B %Y")

    folder_id = args.folder_id
    if not folder_id:
        fid_path = OUTPUTS_DIR / "folder_id.txt"
        if fid_path.exists():
            folder_id = fid_path.read_text().strip()
        else:
            print("[fatal] no folder_id (pass --folder-id or create outputs/folder_id.txt)", file=sys.stderr)
            sys.exit(1)

    title = f"YouTube Competitor Analysis - Week of {date}"
    html = build_html(aggregate, pretty_date)

    # gws --upload demands a CWD-relative path
    html_path = "yt_competitor_doc.html"
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
