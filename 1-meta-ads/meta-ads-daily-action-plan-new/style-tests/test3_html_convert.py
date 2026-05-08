#!/usr/bin/env python3
"""
TEST 3 v3: HTML → Google Doc with inline styles only.

Tweaks vs v2:
- ZERO em-dashes (—). Use commas, full stops, parentheses, or colons.
- Anomaly Alert as a red-bordered alert box (mimics Antonio's "If Internal greyed out" callout).
- Long paragraphs broken into 2-3 line paragraphs or bullet lists under the same heading.

Strategy: skip <style> blocks entirely, write everything inline. Google Docs' HTML
import drops most external CSS but honours inline color, background-color, font-family,
font-size, weight, table border/padding, h1/h2, ul/li.
"""
import json
import subprocess
import sys
import re
import os

FOLDER_ID = "1pduNpfkMt3HQRs2t0z5e3L3_R5prdwUs"
DATE = "2026-05-08"
TITLE = f"TEST 3 v3, HTML Inline (no em-dash, red anomaly box, short paragraphs), {DATE}"

# Color palette
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
        print(f"FAIL: {' '.join(cmd_args)}", file=sys.stderr)
        print(out, file=sys.stderr)
        raise


# Build HTML with inline styles only — no <style> block
HTML = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Daily Action Plan</title></head>
<body style="font-family:'Helvetica Neue',Arial,sans-serif; font-size:11pt; color:{DARK}; line-height:1.6;">

<p style="font-size:10pt; font-weight:700; color:{TEAL}; letter-spacing:0.5px; margin:0 0 24px 0;">
THE COACH CONSULTANT · DAILY ACTION PLAN
</p>

<h1 style="font-family:'Playfair Display',Georgia,serif; font-size:36pt; font-weight:800; color:{DARK}; margin:0 0 12px 0; line-height:1.1;">
08 May 2026
</h1>

<p style="font-family:'Helvetica Neue',Arial,sans-serif; font-size:14pt; color:{TEAL}; margin:0 0 28px 0; line-height:1.4;">
First paid booking of the week landed overnight at £356.72 cost per real call. Pixel still blind on day seven, six new pain-anchored reels in the pool starting to bite.
</p>

<table style="border-collapse:collapse; width:100%; margin:0 0 32px 0; border:1px solid {TEAL};">
  <tr>
    <td style="border:1px solid {TEAL}; padding:14px 18px; vertical-align:top; width:33%;">
      <p style="margin:0 0 6px 0; font-size:9pt; font-weight:700; color:{DARK}; letter-spacing:0.5px;">TODAY'S SPEND</p>
      <p style="margin:0; font-size:13pt; color:{DARK};">£356.72 <span style="color:{TEAL}; font-size:10pt;">(live, 7d)</span></p>
    </td>
    <td style="border:1px solid {TEAL}; padding:14px 18px; vertical-align:top; width:33%;">
      <p style="margin:0 0 6px 0; font-size:9pt; font-weight:700; color:{DARK}; letter-spacing:0.5px;">CALLS</p>
      <p style="margin:0; font-size:13pt; color:{DARK};">1 in 7d <span style="color:{TEAL}; font-size:10pt;">/ 10 in 28d</span></p>
    </td>
    <td style="border:1px solid {TEAL}; padding:14px 18px; vertical-align:top; width:33%;">
      <p style="margin:0 0 6px 0; font-size:9pt; font-weight:700; color:{DARK}; letter-spacing:0.5px;">ROAS</p>
      <p style="margin:0; font-size:13pt; color:{DARK};">Pending</p>
    </td>
  </tr>
</table>

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
Yesterday's Number
</h2>

<ul style="margin:0 0 16px 0; padding-left:22px;">
  <li style="margin:0 0 6px 0;">Spend: £87.00 (Warm V2 day four burn, 7d total now £356.72, +£87 vs yesterday)</li>
  <li style="margin:0 0 6px 0;">Calendly calls: 1 in 7d (first paid booking back inside the rolling window since 28 April), 10 in 28d (master sheet, Week 4)</li>
  <li style="margin:0 0 6px 0;">Cost per call: £356.72 (single booking inside the 7d window, take directionally)</li>
  <li style="margin:0 0 6px 0;">ROAS: Pending (cash maturing, 7-14 day lag, no email-matched signups against this booking yet)</li>
  <li style="margin:0 0 6px 0;">Cash sales: Pending (cash maturing, 7-14 day lag)</li>
</ul>

<p style="margin:16px 0 8px 0; padding:12px 16px; background-color:{TEAL_LIGHT_BG}; border-left:3px solid {TEAL};">
<strong>Status: Watch.</strong> BOF the only stage delivering, Warm V2 - Retargeting 30% on day four of fresh delivery. Click side healthy at 2.21% CTR, conversion side improving with submit rate up from 0.34% to 0.52% and the first paid booking landed overnight.
</p>
<p style="margin:0 0 16px 0; padding:12px 16px; background-color:{TEAL_LIGHT_BG}; border-left:3px solid {TEAL};">
The booking pixel still reads zero across the campaign so per-ad-set kill anchors stay blind. The 28d paid bookings count has stepped down from 13 yesterday to 10 today, ahead of Antonio's planned dashboard recalibration. This is a counting fix evolving, not a campaign drop.
</p>

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
Kill Today
</h2>

<p style="margin:18px 0 6px 0; font-size:13pt; font-weight:700; color:{DARK};">
1. No kill today
</p>
<p style="margin:0 0 8px 0;"><strong style="color:{TEAL};">Reason.</strong> Yesterday's brief held the line on pulling underperforming Identity callout creatives (If you're consultant WHITE, If you're SP WHITE) on the grounds that Warm V2 is the only delivering ad set in the account, and the pixel-blind window is no place to throw away signal.</p>
<p style="margin:0 0 8px 0;">That logic still holds today. The day-four data has produced its first paid booking and a doubling of submit rate, so the pool as a whole is converting better. Pulling any creative now risks destroying the lift before we know which one drove it.</p>
<p style="margin:0 0 8px 0;"><strong style="color:{TEAL};">Implicit hypothesis if you disagree.</strong> Kill the two zero-CTR identity callouts to clean the ad set. Trade-off: lose two more days of data on whether identity callouts ever earn their place. Hold today, revisit Friday.</p>
<p style="margin:0 0 16px 0;"><strong style="color:{TEAL};">Daily saving.</strong> £0/day, this is a deliberate hold.</p>

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
Scale Today
</h2>

<p style="margin:18px 0 6px 0; font-size:13pt; font-weight:700; color:{DARK};">
1. Reel NEW, 100k staff wages <span style="color:{TEAL}; font-weight:400;">(Warm, Retargeting 30%)</span>. Soften hook variant briefed today.
</p>
<p style="margin:0 0 8px 0;"><strong style="color:{TEAL};">Budget change.</strong> Hold the original creative live, brief a softer-hook variant of the same Cost-of-Inaction angle today. Plan to pause the original once the variant clears Meta's quality review and starts spending.</p>
<p style="margin:0 0 8px 0;"><strong style="color:{TEAL};">Why.</strong> 4.80% CTR remains the strongest in the account on the warm audience, but the BELOW_AVERAGE_35 quality flag is now into its third day. Meta is throttling delivery of clickbait-flagged hooks regardless of click strength.</p>
<p style="margin:0 0 8px 0;">The Cost-of-Inaction pain anchor (£100K+/month staff wages, lifted from new IP) is a hero angle in the playbook, the second-strongest pain after Guesswork Tax. Killing the angle outright leaves a gap; softening the hook keeps the pain in the pool.</p>
<p style="margin:0 0 16px 0;"><strong style="color:{TEAL};">Headroom.</strong> Warm audience absorbed £307 over 7d without saturation. <strong style="color:{TEAL};">Hedge.</strong> Reel NEW, intelligence predictability is the strongest day-three signal at 2.16% CTR with no quality flag.</p>

<p style="margin:18px 0 6px 0; font-size:13pt; font-weight:700; color:{DARK};">
2. Six new "Reel NEW" creatives <span style="color:{TEAL}; font-weight:400;">(Warm V2, Retargeting 30%)</span>
</p>
<p style="margin:0 0 8px 0;"><strong style="color:{TEAL};">Budget change.</strong> Hold Warm V2 daily budget at current level, do not pause any new reel before day five (Friday).</p>
<p style="margin:0 0 8px 0;"><strong style="color:{TEAL};">Why.</strong> New IP pain coverage broadens for the second day running. Five distinct pain layers now represented after two weeks of identity-callout-only mix.</p>
<ul style="margin:0 0 8px 0; padding-left:22px;">
  <li style="margin:0 0 4px 0;">Reel NEW, Knowing what to do (Guesswork Tax, hero pain)</li>
  <li style="margin:0 0 4px 0;">Reel NEW, Predictability</li>
  <li style="margin:0 0 4px 0;">Reel NEW, Guessing growth (Guesswork Tax)</li>
  <li style="margin:0 0 4px 0;">Reel NEW, intelligence predictability (AI Intelligence pillar)</li>
  <li style="margin:0 0 4px 0;">Reel NEW, Complicated (Plate Anxiety / AI Era)</li>
  <li style="margin:0 0 4px 0;">Reel NEW, 100k staff wages (Cost-of-Inaction)</li>
</ul>
<p style="margin:0 0 8px 0;">Form submit rate has risen from 0.34% to 0.52% (1 to 2 submits) and the first paid Calendly booking inside the 7d window landed overnight. Day four is too early to single out a winner; let the cohort run through Friday, then read which creatives carried the conversion lift.</p>
<p style="margin:0 0 16px 0;"><strong style="color:{TEAL};">Implicit hypothesis if you disagree.</strong> Cut Warm V2 budget by 30% per yesterday's brief. Trade-off: that move was right under day-three logic when nothing was converting; today's 1-booking signal flips the calculus.</p>

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
Anomaly Alert
</h2>

<div style="margin:0 0 16px 0; padding:16px 20px; background-color:{RED_LIGHT_BG}; border:2px solid {RED}; border-radius:2px;">
<p style="margin:0 0 8px 0;"><strong style="color:{RED};">Pixel match-rate gap, day 7.</strong> £356.72 of BOF spend in 7d, 1 Calendly paid booking inside the window, 0 pixel-tracked bookings ever. Real bookings are happening, the pixel is not seeing them.</p>
<p style="margin:0 0 8px 0;">Until this is fixed, the per-ad-set kill / scale anchor (cost_per_booking_pixel_7d) reads blind across the entire campaign. Meta is optimising Warm V2 against the 0.52% form-submit rate as its conversion baseline, not against real bookings.</p>
<p style="margin:0;"><strong style="color:{RED};">28d count recalibration in progress.</strong> 13 (5 May) to 12 (6 May) to 10 (8 May), consistent with the dashboard refactor where the previous email-match count was inflated. Treat today's 10 as the cleaner number, not a campaign collapse.</p>
</div>

<h2 style="font-family:'Playfair Display',Georgia,serif; font-size:24pt; font-weight:800; color:{DARK}; margin:32px 0 12px 0; line-height:1.1;">
Today's Priority
</h2>

<p style="margin:0 0 8px 0; padding:14px 16px; background-color:{TEAL_LIGHT_BG}; border-left:3px solid {TEAL};">
<strong>Fix the booking pixel today.</strong> Open the booking-confirmation page on the URL pattern containing <code style="background-color:#f0f0f0; padding:2px 4px;">thank-you-for-booking-a-call-pa</code> in a fresh ad-blocker-free browser session, run Meta Pixel Helper, confirm a <code style="background-color:#f0f0f0; padding:2px 4px;">Schedule</code> event fires on the URL match. Fix the snippet routing if it isn't.
</p>
<p style="margin:0 0 16px 0; padding:14px 16px; background-color:{TEAL_LIGHT_BG}; border-left:3px solid {TEAL};">
Day seven on the carry-forward. Every additional day costs another £80 to £90 of pixel-blind spend. Once the pixel reads, the per-ad-set kill / scale anchor comes online and we can sequence the Cold, Interest Based 40% reactivation on a clean signal. The pixel fix is upstream of every other media-buying decision this week.
</p>

</body>
</html>
"""

# Write to local file (gws --upload requires CWD-relative paths)
html_path = "test3v3_doc.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HTML)

# Upload + convert
upload = gws([
    "drive", "files", "create",
    "--upload", html_path,
    "--params", json.dumps({
        "name": TITLE,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [FOLDER_ID]
    }),
    "--format", "json"
])

doc_id = upload["id"]
mime = upload.get("mimeType", "?")

if mime != "application/vnd.google-apps.document":
    converted = gws([
        "drive", "files", "copy",
        "--params", json.dumps({"fileId": doc_id}),
        "--json", json.dumps({
            "name": TITLE,
            "mimeType": "application/vnd.google-apps.document",
            "parents": [FOLDER_ID]
        }),
        "--format", "json"
    ])
    new_id = converted["id"]
    gws(["drive", "files", "delete", "--params", json.dumps({"fileId": doc_id})])
    doc_id = new_id

os.unlink(html_path)
print(f"GDOC: https://docs.google.com/document/d/{doc_id}/edit")
