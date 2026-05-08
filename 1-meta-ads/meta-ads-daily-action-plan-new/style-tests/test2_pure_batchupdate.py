#!/usr/bin/env python3
"""
TEST 2: Pure documents.batchUpdate, no template, no copy.

Build the doc paragraph-by-paragraph with full inline styling. More work per run
but no fragile template state to maintain.
"""
import json
import subprocess
import sys
import re

FOLDER_ID = "1pduNpfkMt3HQRs2t0z5e3L3_R5prdwUs"
DATE = "2026-05-08"
TITLE = f"TEST 2 — Pure batchUpdate — {DATE}"

TEAL = {"red": 0.36, "green": 0.55, "blue": 0.50}
TEAL_LIGHT = {"red": 0.85, "green": 0.92, "blue": 0.89}
DARK = {"red": 0.05, "green": 0.05, "blue": 0.05}


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


# Create empty doc
doc = gws([
    "docs", "documents", "create",
    "--params", json.dumps({"title": TITLE}),
    "--format", "json"
])
doc_id = doc["documentId"]

# Move to folder
gws([
    "drive", "files", "update",
    "--params", json.dumps({"fileId": doc_id, "addParents": FOLDER_ID, "removeParents": "root"}),
])

# Build content. Strategy: insert all text first, then apply styles in a second batch
# (so indices don't shift mid-update).

content_blocks = [
    # (text, kind)
    ("The Coach Consultant · Daily Action Plan\n", "kicker"),
    ("\n", "spacer"),
    ("08 May 2026\n", "h1"),
    ("\n", "spacer"),
    ("First paid booking of the week landed overnight at £356.72 cost per real call. Pixel still blind on day seven, six new pain-anchored reels in the pool starting to bite.\n", "subtitle"),
    ("\n", "spacer"),
    ("Today's Spend: £356.72 (live, 7d)  ·  Calls: 1 in 7d, 10 in 28d  ·  ROAS: Pending\n", "snapshot"),
    ("\n", "spacer"),

    ("Yesterday's Number\n", "h2"),
    ("\n", "spacer"),
    ("Spend: £87.00 (Warm V2 day four burn, 7d total now £356.72, +£87 vs yesterday)\n", "bullet"),
    ("Calendly calls: 1 in 7d (first paid booking back inside the rolling window since 28 April), 10 in 28d (master sheet, Week 4)\n", "bullet"),
    ("Cost per call: £356.72 (single booking inside the 7d window, take directionally)\n", "bullet"),
    ("ROAS: Pending (cash maturing, 7-14 day lag, no email-matched signups against this booking yet)\n", "bullet"),
    ("Cash sales: Pending (cash maturing, 7-14 day lag)\n", "bullet"),
    ("\n", "spacer"),
    ("Status: Watch (BOF the only stage delivering, Warm V2 - Retargeting 30% on day four of fresh delivery, click side healthy at 2.21% CTR, conversion side improving — submit rate up from 0.34% to 0.52% and the first paid booking landed overnight, but the booking pixel still reads zero across the campaign so per-ad-set kill anchors stay blind. The 28d paid bookings count has stepped down from 13 yesterday to 10 today, ahead of Antonio's planned dashboard recalibration — this is a counting fix evolving, not a campaign drop).\n", "body"),
    ("\n", "spacer"),

    ("Kill Today\n", "h2"),
    ("\n", "spacer"),
    ("1. No kill today\n", "kill_title"),
    ("Reason: Yesterday's brief held the line on pulling underperforming Identity callout creatives (If you're consultant WHITE, If you're SP WHITE) on the grounds that Warm V2 is the only delivering ad set in the account and the pixel-blind window is no place to throw away signal. That logic still holds today. The day-four data has produced its first paid booking and a doubling of submit rate, so the pool as a whole is converting better. Implicit hypothesis if you disagree: kill the two zero-CTR identity callouts to clean the ad set. Trade-off: lose two more days of data on whether identity callouts ever earn their place. Hold today, revisit Friday.\n", "body"),
    ("Daily saving: £0/day, this is a deliberate hold\n", "body"),
    ("\n", "spacer"),

    ("Scale Today\n", "h2"),
    ("\n", "spacer"),
    ("1. Reel NEW - 100k staff wages (Warm - Retargeting 30%) — soften hook variant briefed today\n", "kill_title"),
    ("Budget change: Hold the original creative live, brief a softer-hook variant of the same Cost-of-Inaction angle today. Plan to pause the original once the variant clears Meta's quality review.\n", "body"),
    ("Why: 4.80% CTR remains the strongest in the account on the warm audience but the BELOW_AVERAGE_35 quality flag is now into its third day — Meta is throttling delivery of clickbait-flagged hooks regardless of click strength. The Cost-of-Inaction pain anchor (£100K+/month staff wages, lifted from new IP) is a hero angle in the playbook, the second-strongest pain after Guesswork Tax. Killing the angle outright leaves a gap; softening the hook keeps the pain in the pool. Headroom: warm audience absorbed £307 over 7d without saturation. Hedge: Reel NEW - intelligence predictability is the strongest day-three signal at 2.16% CTR with no quality flag.\n", "body"),
    ("\n", "spacer"),
    ("2. Six new \"Reel NEW\" creatives in Warm V2 - Retargeting 30%\n", "kill_title"),
    ("Budget change: Hold Warm V2 daily budget at current level, do not pause any new reel before day five (Friday).\n", "body"),
    ("Why: New IP pain coverage broadens for the second day running. Reel NEW - Knowing what to do (Guesswork Tax — hero pain), Predictability, Guessing growth, intelligence predictability, Complicated, 100k staff wages — five distinct pain layers represented after two weeks of identity-callout-only mix. Form submit rate has risen from 0.34% to 0.52% and the first paid Calendly booking inside the 7d window landed overnight. Day four is too early to single out a winner; the right move is to let the cohort run through Friday. Implicit hypothesis if you disagree: cut Warm V2 budget by 30% per yesterday's brief. Trade-off: that move was right under day-three logic when nothing was converting; today's 1-booking signal flips the calculus.\n", "body"),
    ("\n", "spacer"),

    ("Anomaly Alert\n", "h2"),
    ("\n", "spacer"),
    ("The 28d paid bookings count has stepped from 13 (5 May) to 12 (6 May) to 10 (8 May) — directionally consistent with the dashboard refactor Antonio is rolling out, where the previous email-match count was inflated. Once next week's cron lands the new validation_deltas field, the recalibrated baseline will be the new ground truth. Treat today's 10 as the cleaner number, do not flag this as a campaign collapse. Pixel match-rate gap remains the single highest-leverage open loop on the account.\n", "body"),
    ("\n", "spacer"),

    ("Today's Priority\n", "h2"),
    ("\n", "spacer"),
    ("Fix the booking pixel today. Open the booking-confirmation page on the URL pattern containing thank-you-for-booking-a-call-pa in a fresh ad-blocker-free browser session, run Meta Pixel Helper, confirm a Schedule event fires on the URL match, fix the snippet routing if it isn't. Day seven on the carry-forward — every additional day costs another £80-90 of pixel-blind spend. Once the pixel reads, the per-ad-set kill / scale anchor comes online and we can sequence the Cold - Interest Based 40% reactivation on a clean signal. The pixel fix is upstream of every other media-buying decision this week.\n", "body"),
]

# Phase 1: insert all text in one go (in reverse so indices stay simple)
# Actually, easier: build a single big text and remember each block's range.
ranges = []
combined = ""
pos = 1
for text, kind in content_blocks:
    start = pos + len(combined)
    end = start + len(text)
    ranges.append((start, end, kind, text))
    combined += text

requests = [{"insertText": {"location": {"index": 1}, "text": combined}}]
gws([
    "docs", "documents", "batchUpdate",
    "--params", json.dumps({"documentId": doc_id, "requests": requests}),
    "--format", "json"
])

# Phase 2: apply styles for each range
style_requests = []

def apply_text_style(start, end, style):
    style_requests.append({
        "updateTextStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "textStyle": style,
            "fields": ",".join(style.keys())
        }
    })

def apply_para_style(start, end, named):
    style_requests.append({
        "updateParagraphStyle": {
            "range": {"startIndex": start, "endIndex": end},
            "paragraphStyle": {"namedStyleType": named},
            "fields": "namedStyleType"
        }
    })

# Reset NORMAL_TEXT default first by clearing any inherited style on whole range
total_end = pos + len(combined) - 1
apply_para_style(1, total_end, "NORMAL_TEXT")
apply_text_style(1, total_end, {
    "fontSize": {"magnitude": 11, "unit": "PT"},
    "weightedFontFamily": {"fontFamily": "Inter"},
    "foregroundColor": {"color": {"rgbColor": DARK}}
})

for start, end, kind, text in ranges:
    if kind == "kicker":
        apply_text_style(start, end, {
            "fontSize": {"magnitude": 10, "unit": "PT"},
            "weightedFontFamily": {"fontFamily": "Inter"},
            "bold": True,
            "foregroundColor": {"color": {"rgbColor": TEAL}},
        })
    elif kind == "h1":
        apply_para_style(start, end, "HEADING_1")
        apply_text_style(start, end, {
            "fontSize": {"magnitude": 36, "unit": "PT"},
            "weightedFontFamily": {"fontFamily": "Playfair Display"},
            "bold": True,
            "foregroundColor": {"color": {"rgbColor": DARK}},
        })
    elif kind == "subtitle":
        apply_text_style(start, end, {
            "fontSize": {"magnitude": 13, "unit": "PT"},
            "weightedFontFamily": {"fontFamily": "Inter"},
            "foregroundColor": {"color": {"rgbColor": TEAL}},
        })
    elif kind == "snapshot":
        apply_text_style(start, end, {
            "fontSize": {"magnitude": 11, "unit": "PT"},
            "weightedFontFamily": {"fontFamily": "Inter"},
            "bold": True,
            "backgroundColor": {"color": {"rgbColor": TEAL_LIGHT}},
        })
    elif kind == "h2":
        apply_para_style(start, end, "HEADING_2")
        apply_text_style(start, end, {
            "fontSize": {"magnitude": 22, "unit": "PT"},
            "weightedFontFamily": {"fontFamily": "Playfair Display"},
            "bold": True,
            "foregroundColor": {"color": {"rgbColor": DARK}},
        })
    elif kind == "bullet":
        # Bullet via createParagraphBullets
        style_requests.append({
            "createParagraphBullets": {
                "range": {"startIndex": start, "endIndex": end},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
            }
        })
        apply_text_style(start, end, {
            "fontSize": {"magnitude": 11, "unit": "PT"},
            "weightedFontFamily": {"fontFamily": "Inter"},
        })
    elif kind == "kill_title":
        apply_text_style(start, end, {
            "fontSize": {"magnitude": 12, "unit": "PT"},
            "weightedFontFamily": {"fontFamily": "Inter"},
            "bold": True,
            "foregroundColor": {"color": {"rgbColor": DARK}},
        })
    elif kind == "body":
        apply_text_style(start, end, {
            "fontSize": {"magnitude": 11, "unit": "PT"},
            "weightedFontFamily": {"fontFamily": "Inter"},
            "foregroundColor": {"color": {"rgbColor": DARK}},
        })

# Apply styles in chunks (Google API has limits)
for i in range(0, len(style_requests), 100):
    chunk = style_requests[i:i+100]
    gws([
        "docs", "documents", "batchUpdate",
        "--params", json.dumps({"documentId": doc_id, "requests": chunk}),
        "--format", "json"
    ])

print(f"GDOC: https://docs.google.com/document/d/{doc_id}/edit")
