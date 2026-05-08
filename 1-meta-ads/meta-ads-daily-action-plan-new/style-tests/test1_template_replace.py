#!/usr/bin/env python3
"""
TEST 1: Template + duplicate + batchUpdate replace.

Step A. Create a master template Google Doc with full Antonio-style formatting.
Step B. Copy the template, run replaceAllText with today's data.

Outputs the URL of the generated Doc.
"""
import os
import json
import subprocess
import sys
import re

FOLDER_ID = "1pduNpfkMt3HQRs2t0z5e3L3_R5prdwUs"
DATE = "2026-05-08"
TITLE = f"TEST 1 — Template Replace — {DATE}"

# Antonio palette (extracted from screenshots)
TEAL = {"red": 0.36, "green": 0.55, "blue": 0.50}  # ~ #5C8B7F kicker / banners
DARK = {"red": 0.0, "green": 0.0, "blue": 0.0}
LIGHT_GREY = {"red": 0.9, "green": 0.9, "blue": 0.9}


def gws(cmd_args, json_input=None):
    """Run a gws command and return parsed JSON output."""
    cmd = ["gws"] + cmd_args
    result = subprocess.run(cmd, capture_output=True, text=True)
    out = result.stdout
    # Strip the keyring banner if present
    out = re.sub(r"^Using keyring backend.*\n", "", out)
    out = re.sub(r"^Warning:.*\n", "", out, flags=re.MULTILINE)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        print(f"FAIL: {' '.join(cmd_args)}", file=sys.stderr)
        print(out, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise


def create_template():
    """Step A: build the master template once. Returns its file ID."""
    # Create empty doc
    doc = gws([
        "docs", "documents", "create",
        "--params", json.dumps({"title": "Daily Action Plan TEMPLATE"}),
        "--format", "json"
    ])
    doc_id = doc["documentId"]

    # Move to target folder (default is My Drive root)
    gws([
        "drive", "files", "update",
        "--params", json.dumps({"fileId": doc_id, "addParents": FOLDER_ID, "removeParents": "root"}),
    ])

    # Build the doc content with batchUpdate
    # Layout: KICKER / H1 DATE / SUBTITLE / SNAPSHOT TABLE / sections...
    requests = []
    pos = 1

    # Helper: insert text + remember its range
    def push(text, style_type="NORMAL_TEXT", text_style=None, named_style=None):
        nonlocal pos
        requests.append({"insertText": {"location": {"index": pos}, "text": text}})
        start = pos
        end = pos + len(text)
        # Apply paragraph style
        if named_style:
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": named_style},
                    "fields": "namedStyleType"
                }
            })
        # Apply inline text style
        if text_style:
            requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "textStyle": text_style,
                    "fields": ",".join(text_style.keys())
                }
            })
        pos = end

    # KICKER
    push("The Coach Consultant · Daily Action Plan\n",
         text_style={"foregroundColor": {"color": {"rgbColor": TEAL}}, "bold": True, "fontSize": {"magnitude": 10, "unit": "PT"}})
    push("\n")

    # H1 DATE
    push("{{DATE}}\n", named_style="HEADING_1",
         text_style={"weightedFontFamily": {"fontFamily": "Playfair Display"}, "fontSize": {"magnitude": 32, "unit": "PT"}, "bold": True})
    push("\n")

    # SUBTITLE
    push("{{SUBTITLE}}\n",
         text_style={"foregroundColor": {"color": {"rgbColor": TEAL}}, "fontSize": {"magnitude": 13, "unit": "PT"}})
    push("\n")

    # SNAPSHOT TABLE — insert a 1x3 table, fill cells
    # Insert table; once table is inserted, indices shift, this is fragile but workable.
    requests.append({"insertTable": {"location": {"index": pos}, "rows": 2, "columns": 3}})
    # We'll defer cell-fill to a second batchUpdate.

    # Run first batch
    gws([
        "docs", "documents", "batchUpdate",
        "--params", json.dumps({"documentId": doc_id, "requests": requests}),
        "--format", "json"
    ])

    # Now re-fetch and locate the table
    fresh = gws([
        "docs", "documents", "get",
        "--params", json.dumps({"documentId": doc_id}),
        "--format", "json"
    ])
    # Find table indices
    table_cells = []
    for el in fresh["body"]["content"]:
        if "table" in el:
            for row in el["table"]["tableRows"]:
                for cell in row["tableCells"]:
                    # Each cell has a startIndex; insert text at startIndex+1
                    table_cells.append(cell["startIndex"] + 1)

    # Fill cells: header row + data row
    cell_texts = ["Today's Spend", "Calls", "ROAS",
                  "{{SPEND}}", "{{CALLS}}", "{{ROAS}}"]
    # Insert in REVERSE order so indices don't shift
    fill_requests = []
    for idx, text in zip(reversed(table_cells), reversed(cell_texts)):
        fill_requests.append({"insertText": {"location": {"index": idx}, "text": text}})
    gws([
        "docs", "documents", "batchUpdate",
        "--params", json.dumps({"documentId": doc_id, "requests": fill_requests}),
        "--format", "json"
    ])

    # Now append the rest after the table.
    # Re-fetch to know current end of body.
    fresh = gws([
        "docs", "documents", "get",
        "--params", json.dumps({"documentId": doc_id}),
        "--format", "json"
    ])
    # End of body is the last segment endIndex - 1
    end_index = fresh["body"]["content"][-1]["endIndex"] - 1

    rest_requests = []
    rpos = end_index

    def rpush(text, named_style=None, text_style=None):
        nonlocal rpos
        rest_requests.append({"insertText": {"location": {"index": rpos}, "text": text}})
        start = rpos
        end = rpos + len(text)
        if named_style:
            rest_requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": named_style},
                    "fields": "namedStyleType"
                }
            })
        if text_style:
            rest_requests.append({
                "updateTextStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "textStyle": text_style,
                    "fields": ",".join(text_style.keys())
                }
            })
        rpos = end

    h2_style = {"weightedFontFamily": {"fontFamily": "Playfair Display"}, "fontSize": {"magnitude": 22, "unit": "PT"}, "bold": True}

    rpush("\n\n")
    rpush("Yesterday's Number\n", named_style="HEADING_2", text_style=h2_style)
    rpush("\n")
    rpush("{{YESTERDAY_BULLETS}}\n")
    rpush("\n")
    rpush("Status: {{STATUS}}\n")
    rpush("\n")

    rpush("Kill Today\n", named_style="HEADING_2", text_style=h2_style)
    rpush("\n")
    rpush("1. {{KILL_1_TITLE}}\n", text_style={"bold": True})
    rpush("Reason: {{KILL_1_REASON}}\n")
    rpush("Daily saving: {{KILL_1_SAVING}}\n")
    rpush("\n")
    rpush("2. {{KILL_2_TITLE}}\n", text_style={"bold": True})
    rpush("Reason: {{KILL_2_REASON}}\n")
    rpush("Daily saving: {{KILL_2_SAVING}}\n")
    rpush("\n")

    rpush("Scale Today\n", named_style="HEADING_2", text_style=h2_style)
    rpush("\n")
    rpush("1. {{SCALE_1_TITLE}}\n", text_style={"bold": True})
    rpush("Budget change: {{SCALE_1_BUDGET}}\n")
    rpush("Why: {{SCALE_1_WHY}}\n")
    rpush("\n")
    rpush("2. {{SCALE_2_TITLE}}\n", text_style={"bold": True})
    rpush("Budget change: {{SCALE_2_BUDGET}}\n")
    rpush("Why: {{SCALE_2_WHY}}\n")
    rpush("\n")

    rpush("Anomaly Alert\n", named_style="HEADING_2", text_style=h2_style)
    rpush("\n")
    rpush("{{ANOMALY}}\n")
    rpush("\n")

    rpush("Today's Priority\n", named_style="HEADING_2", text_style=h2_style)
    rpush("\n")
    rpush("{{PRIORITY}}\n")

    gws([
        "docs", "documents", "batchUpdate",
        "--params", json.dumps({"documentId": doc_id, "requests": rest_requests}),
        "--format", "json"
    ])

    return doc_id


def fill_template(template_id, data):
    """Step B: copy template, run replaceAllText with today's data."""
    # Copy
    copy = gws([
        "drive", "files", "copy",
        "--params", json.dumps({"fileId": template_id}),
        "--json", json.dumps({
            "name": TITLE,
            "parents": [FOLDER_ID]
        }),
        "--format", "json"
    ])
    new_id = copy["id"]

    # Replace placeholders
    requests = []
    for k, v in data.items():
        requests.append({
            "replaceAllText": {
                "containsText": {"text": "{{" + k + "}}", "matchCase": True},
                "replaceText": v
            }
        })

    gws([
        "docs", "documents", "batchUpdate",
        "--params", json.dumps({"documentId": new_id, "requests": requests}),
        "--format", "json"
    ])

    return new_id


# Today's data (from outputs/2026-05-08.md)
DATA = {
    "DATE": "08 May 2026",
    "SUBTITLE": "First paid booking of the week landed overnight at £356.72 cost per real call. Pixel still blind on day seven, six new pain-anchored reels in the pool starting to bite.",
    "SPEND": "£356.72 (live, 7d)",
    "CALLS": "1 in 7d, 10 in 28d",
    "ROAS": "Pending",
    "YESTERDAY_BULLETS": (
        "• Spend: £87.00 (Warm V2 day four burn, 7d total now £356.72, +£87 vs yesterday)\n"
        "• Calendly calls: 1 in 7d (first paid booking back inside the rolling window since 28 April), 10 in 28d (master sheet, Week 4)\n"
        "• Cost per call: £356.72 (single booking inside the 7d window, take directionally)\n"
        "• ROAS: Pending (cash maturing, 7-14 day lag, no email-matched signups against this booking yet)\n"
        "• Cash sales: Pending (cash maturing, 7-14 day lag)"
    ),
    "STATUS": "Watch (BOF the only stage delivering, Warm V2 - Retargeting 30% on day four of fresh delivery, click side healthy at 2.21% CTR, conversion side improving — submit rate up from 0.34% to 0.52% and the first paid booking landed overnight, but the booking pixel still reads zero across the campaign so per-ad-set kill anchors stay blind. The 28d paid bookings count has stepped down from 13 yesterday to 10 today, ahead of Antonio's planned dashboard recalibration — this is a counting fix evolving, not a campaign drop).",
    "KILL_1_TITLE": "No kill today",
    "KILL_1_REASON": "Yesterday's brief held the line on pulling underperforming Identity callout creatives (If you're consultant WHITE, If you're SP WHITE) on the grounds that Warm V2 is the only delivering ad set in the account and the pixel-blind window is no place to throw away signal. That logic still holds today. The day-four data has produced its first paid booking and a doubling of submit rate, so the pool as a whole is converting better, not worse. Pulling any creative now risks destroying the lift before we know which one drove it. Implicit hypothesis if you disagree: kill the two zero-CTR identity callouts to clean the ad set. Trade-off: lose two more days of data on whether identity callouts ever earn their place in a pain-anchored pool. Hold today, revisit Friday.",
    "KILL_1_SAVING": "£0/day, this is a deliberate hold",
    "KILL_2_TITLE": "—",
    "KILL_2_REASON": "Single kill recommendation today.",
    "KILL_2_SAVING": "—",
    "SCALE_1_TITLE": "Reel NEW - 100k staff wages (Warm - Retargeting 30%) — soften hook variant briefed today",
    "SCALE_1_BUDGET": "Hold the original creative live, brief a softer-hook variant of the same Cost-of-Inaction angle today. Plan to pause the original once the variant clears Meta's quality review and starts spending.",
    "SCALE_1_WHY": "4.80% CTR remains the strongest in the account on the warm audience but the BELOW_AVERAGE_35 quality flag is now into its third day — Meta is throttling delivery of clickbait-flagged hooks regardless of click strength. The Cost-of-Inaction pain anchor (£100K+/month staff wages, lifted from new IP) is a hero angle in the playbook, the second-strongest pain after Guesswork Tax. Killing the angle outright leaves a gap; softening the hook keeps the pain in the pool. Headroom on the variant: the warm audience absorbed £307 over 7d without saturation, so the variant has 4-5x the historical creative-level burn before it hits ceiling. Hedge if the variant under-performs: Reel NEW - intelligence predictability is the strongest day-three signal at 2.16% CTR with no quality flag.",
    "SCALE_2_TITLE": "Six new \"Reel NEW\" creatives in Warm V2 - Retargeting 30%",
    "SCALE_2_BUDGET": "Hold Warm V2 daily budget at current level, do not pause any new reel before day five (Friday).",
    "SCALE_2_WHY": "New IP pain coverage broadens for the second day running. Reel NEW - Knowing what to do (Guesswork Tax — hero pain), Reel NEW - Predictability, Reel NEW - Guessing growth, Reel NEW - intelligence predictability, Reel NEW - Complicated, Reel NEW - 100k staff wages — five distinct pain layers represented after two weeks of identity-callout-only mix. Form submit rate has risen from 0.34% to 0.52% (1 → 2 submits) and the first paid Calendly booking inside the 7d window landed overnight. Day four is too early to single out a winner yet; the right move is to let the cohort run through Friday, then read which creatives carried the conversion lift. Implicit hypothesis if you disagree: cut Warm V2 budget by 30% per yesterday's brief. Trade-off: that move was right under day-three logic when nothing was converting; today's 1-booking signal flips the calculus.",
    "ANOMALY": "The 28d paid bookings count has stepped from 13 (5 May) to 12 (6 May) to 10 (8 May) — directionally consistent with the dashboard refactor Antonio is rolling out, where the previous email-match count was inflated. Once next week's cron lands the new validation_deltas field, the recalibrated baseline will be the new ground truth. Treat today's 10 as the cleaner number, do not flag this as a campaign collapse. Pixel match-rate gap remains the single highest-leverage open loop on the account.",
    "PRIORITY": "Fix the booking pixel today. Open the booking-confirmation page on the URL pattern containing thank-you-for-booking-a-call-pa in a fresh ad-blocker-free browser session, run Meta Pixel Helper, confirm a Schedule event fires on the URL match, fix the snippet routing if it isn't. Day seven on the carry-forward — every additional day costs another £80-90 of pixel-blind spend. Once the pixel reads, the per-ad-set kill / scale anchor comes online and we can sequence the Cold - Interest Based 40% reactivation on a clean signal. The pixel fix is upstream of every other media-buying decision this week."
}


if __name__ == "__main__":
    print("Creating template...", file=sys.stderr)
    template_id = create_template()
    print(f"Template ID: {template_id}", file=sys.stderr)
    print("Filling template...", file=sys.stderr)
    new_id = fill_template(template_id, DATA)
    print(f"GDOC: https://docs.google.com/document/d/{new_id}/edit")
    # Don't delete the template — we'll reuse it.
    print(f"TEMPLATE: https://docs.google.com/document/d/{template_id}/edit")
