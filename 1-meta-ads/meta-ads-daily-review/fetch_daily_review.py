#!/usr/bin/env python3
"""
Meta Ads Daily Review — Data Fetcher + Analysis Runner

Replaces Ben Mahmoud's manual screenshot-to-Claude workflow. Pulls live
campaign data from the Meta Ads API and produces a structured JSON payload
that the skill's Claude prompt can turn into a formatted daily review.

Usage:
    python fetch_daily_review.py --campaign "BOF Q2" --week 2 --days 7
    python fetch_daily_review.py --list-campaigns
    python fetch_daily_review.py --campaign-id 23851234567890 --week 2
"""

import os
import sys
import json
import yaml
import argparse
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv

SKILL_DIR = Path(__file__).parent
PROJECT_ROOT = SKILL_DIR.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
META_ACCOUNT_ID = os.getenv("META_ACCOUNT_ID", "208457557796486")
API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

CONFIG_PATH = SKILL_DIR / "config.yaml"
OUTPUTS_DIR = SKILL_DIR / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

AUDIENCE_LABELS = {
    "warm": "Warm — Retargeting",
    "lookalike": "Cold — Lookalike",
    "interest": "Cold — Interest",
}


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def api_get(path, params=None):
    params = params or {}
    params["access_token"] = META_ACCESS_TOKEN
    resp = requests.get(f"{BASE_URL}/{path}", params=params, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Meta API error {resp.status_code}: {resp.text}")
    return resp.json()


def list_active_campaigns():
    data = api_get(
        f"act_{META_ACCOUNT_ID}/campaigns",
        {
            "fields": "id,name,effective_status,objective",
            "limit": 100,
        },
    )
    return [
        c
        for c in data.get("data", [])
        if c.get("effective_status") in ("ACTIVE", "LEARNING", "LEARNING_LIMITED")
    ]


def resolve_campaign(args):
    if args.campaign_id:
        return args.campaign_id
    campaigns = list_active_campaigns()
    if args.campaign:
        match = [c for c in campaigns if args.campaign.lower() in c["name"].lower()]
        if not match:
            raise SystemExit(f"No active campaign matches '{args.campaign}'")
        return match[0]["id"]
    raise SystemExit("Specify --campaign <name> or --campaign-id <id>")


def fetch_adsets(campaign_id, since, until):
    data = api_get(
        f"{campaign_id}/adsets",
        {
            "fields": "id,name,effective_status,daily_budget,lifetime_budget",
            "limit": 50,
        },
    )
    adsets = data.get("data", [])
    for adset in adsets:
        insights = api_get(
            f"{adset['id']}/insights",
            {
                "fields": "impressions,clicks,ctr,cpc,spend,actions,frequency",
                "time_range": json.dumps({"since": since, "until": until}),
                "level": "adset",
            },
        ).get("data", [])
        adset["insights"] = insights[0] if insights else {}
        adset["audience_type"] = classify_audience(adset["name"])
    return adsets


def classify_audience(adset_name):
    n = adset_name.lower()
    if "retarget" in n or "warm" in n:
        return "warm"
    if "lookalike" in n or "lal" in n:
        return "lookalike"
    if "interest" in n or "cold" in n:
        return "interest"
    return "unknown"


def fetch_ads_for_adset(adset_id, since, until):
    data = api_get(
        f"{adset_id}/ads",
        {
            "fields": "id,name,effective_status,creative{id,name,thumbnail_url}",
            "limit": 200,
        },
    )
    ads = data.get("data", [])
    for ad in ads:
        insights = api_get(
            f"{ad['id']}/insights",
            {
                "fields": (
                    "impressions,clicks,ctr,cpc,spend,actions,"
                    "quality_ranking,engagement_rate_ranking,conversion_rate_ranking"
                ),
                "time_range": json.dumps({"since": since, "until": until}),
                "level": "ad",
            },
        ).get("data", [])
        ad["insights"] = insights[0] if insights else {}
    return ads


def extract_calls_booked(insights):
    """Pull booked calls / leads from the 'actions' array."""
    actions = insights.get("actions", [])
    relevant_types = {
        "lead",
        "onsite_conversion.lead_grouped",
        "offsite_conversion.fb_pixel_lead",
        "schedule_total",
        "offsite_conversion.custom",
    }
    total = 0
    for a in actions:
        if a.get("action_type") in relevant_types:
            try:
                total += int(a.get("value", 0))
            except (TypeError, ValueError):
                pass
    return total


def build_adset_health(adsets):
    rows = []
    for a in adsets:
        ins = a.get("insights", {})
        spend = float(ins.get("spend", 0) or 0)
        clicks = int(ins.get("clicks", 0) or 0)
        calls = extract_calls_booked(ins)
        rows.append(
            {
                "adset_id": a["id"],
                "adset_name": a["name"],
                "audience_type": a["audience_type"],
                "audience_label": AUDIENCE_LABELS.get(a["audience_type"], a["name"]),
                "impressions": int(ins.get("impressions", 0) or 0),
                "clicks": clicks,
                "ctr": float(ins.get("ctr", 0) or 0) / 100,  # Meta returns percent
                "cpc": float(ins.get("cpc", 0) or 0),
                "spend": spend,
                "calls_booked": calls,
                "cost_per_call": (spend / calls) if calls > 0 else None,
                "booking_rate": (calls / clicks) if clicks > 0 else None,
                "status": a.get("effective_status", "UNKNOWN"),
            }
        )
    return rows


def build_creative_matrix(adsets_with_ads):
    """Pivot: creative_name -> {audience_type: ctr_data}"""
    matrix = {}
    for adset in adsets_with_ads:
        audience = adset["audience_type"]
        for ad in adset.get("ads", []):
            ins = ad.get("insights", {})
            creative_name = ad["name"]
            if creative_name not in matrix:
                matrix[creative_name] = {
                    "creative_name": creative_name,
                    "audiences": {},
                    "quality_flags": [],
                }
            impressions = int(ins.get("impressions", 0) or 0)
            clicks = int(ins.get("clicks", 0) or 0)
            matrix[creative_name]["audiences"][audience] = {
                "ctr": float(ins.get("ctr", 0) or 0) / 100,
                "cpc": float(ins.get("cpc", 0) or 0),
                "spend": float(ins.get("spend", 0) or 0),
                "impressions": impressions,
                "clicks": clicks,
                "adset_name": adset["name"],
            }
            for field in ("quality_ranking", "engagement_rate_ranking", "conversion_rate_ranking"):
                rank = ins.get(field)
                if rank and "BELOW" in str(rank).upper():
                    matrix[creative_name]["quality_flags"].append(
                        {
                            "audience": audience,
                            "adset_name": adset["name"],
                            "field": field,
                            "value": rank,
                        }
                    )
    return list(matrix.values())


def assign_signal(creative, config):
    t = config["thresholds"]
    ctrs = {aud: data["ctr"] for aud, data in creative["audiences"].items()}
    impressions = {aud: data["impressions"] for aud, data in creative["audiences"].items()}

    min_imp = t["min_impressions_per_adset"]
    if all(imp < min_imp for imp in impressions.values()):
        return "Too little data"

    above_scale = sum(1 for c in ctrs.values() if c >= t["ctr_scale_signal"])
    above_target = sum(1 for c in ctrs.values() if c >= t["ctr_target"])
    below_target = sum(
        1
        for aud, c in ctrs.items()
        if c < t["ctr_target"] and impressions.get(aud, 0) >= min_imp
    )

    if above_scale >= 2 and above_target == len(ctrs):
        return "⭐ Consistent across all 3"
    if above_scale >= 1 and above_target >= 2:
        return "⭐ Strongest overall"
    if above_scale == 1 and len(ctrs) > 1:
        top_aud = max(ctrs, key=ctrs.get)
        return f"⭐ {AUDIENCE_LABELS.get(top_aud, top_aud)} standout"
    if below_target >= 2:
        return "Below target across board"
    if above_target >= 1 and below_target >= 1:
        return "Mixed"
    return "Solid, watch"


def bucket_verdicts(creatives, config, week, adset_health=None):
    t = config["thresholds"]
    max_week = max(config["week_phases"].keys())
    phase_key = min(max(week, 1), max_week)
    week_rules = config["week_phases"][phase_key]
    learning_cfg = config.get("learning_phase", {})
    directional_only = learning_cfg.get("directional_verdicts_only", False)
    min_conversions = learning_cfg.get("min_conversions_before_changes", 50)

    # Learning-phase guardrail: if any ACTIVE ad set is still in learning AND
    # hasn't cleared the min conversions floor, downgrade all kill/scale to watch
    learning_guardrail_active = False
    if adset_health:
        active_rows = [r for r in adset_health if r["status"] in ("ACTIVE", "LEARNING", "LEARNING_LIMITED")]
        any_learning = any("LEARNING" in r["status"] for r in active_rows)
        total_calls = sum(r.get("calls_booked", 0) for r in active_rows)
        if any_learning and total_calls < min_conversions:
            learning_guardrail_active = True

    scale_bucket = []
    watch_bucket = []
    concern_bucket = []

    for creative in creatives:
        signal = creative.get("signal", "")
        ctrs = {aud: data["ctr"] for aud, data in creative["audiences"].items()}
        impressions = {aud: data["impressions"] for aud, data in creative["audiences"].items()}

        if directional_only or learning_guardrail_active:
            creative["directional"] = True

        allow_scale_now = week_rules["allow_scale"] and not learning_guardrail_active
        allow_kill_now = week_rules["allow_kill"] and not learning_guardrail_active

        if "⭐" in signal and allow_scale_now:
            scale_bucket.append(creative)
        elif signal == "Below target across board" and allow_kill_now:
            if any(imp >= t["min_impressions_per_adset"] * 2 for imp in impressions.values()):
                concern_bucket.append(creative)
            else:
                watch_bucket.append(creative)
        elif signal in ("Mixed", "Solid, watch", "Too little data"):
            watch_bucket.append(creative)
        else:
            watch_bucket.append(creative)

    return {
        "scale": scale_bucket,
        "watch": watch_bucket,
        "concern": concern_bucket,
        "learning_guardrail_active": learning_guardrail_active,
    }


def detect_anomalies(adset_health, creatives, config):
    t = config["thresholds"]
    anomalies = []

    for creative in creatives:
        ctrs = {aud: data["ctr"] for aud, data in creative["audiences"].items()}
        max_ctr = max(ctrs.values()) if ctrs else 0
        if max_ctr >= t["ctr_scale_signal"] and creative["quality_flags"]:
            anomalies.append(
                {
                    "type": "ctr_quality_mismatch",
                    "creative": creative["creative_name"],
                    "detail": (
                        f"High CTR ({max_ctr*100:.2f}%) but Meta flagged below-average quality "
                        f"on {len(creative['quality_flags'])} ad set(s). Clickbait risk."
                    ),
                }
            )

    for creative in creatives:
        imps = [data["impressions"] for data in creative["audiences"].values()]
        if imps and max(imps) > 0:
            min_imp = min(imps)
            max_imp = max(imps)
            if max_imp > 5000 and min_imp < 500:
                anomalies.append(
                    {
                        "type": "delivery_starvation",
                        "creative": creative["creative_name"],
                        "detail": (
                            f"Delivery imbalance: max {max_imp:,} vs min {min_imp:,} impressions. "
                            "Meta starving this creative in at least one audience."
                        ),
                    }
                )

    for row in adset_health:
        if row["clicks"] >= 200 and row["calls_booked"] == 0:
            anomalies.append(
                {
                    "type": "click_but_no_booking",
                    "adset": row["adset_name"],
                    "detail": (
                        f"{row['clicks']} clicks, 0 bookings in {row['audience_label']}. "
                        "Landing page signal, not ad signal."
                    ),
                }
            )

    # Cost-per-call threshold check (£50)
    cost_target = t["cost_per_call_target_gbp"]
    for row in adset_health:
        cpc_call = row.get("cost_per_call")
        if cpc_call is not None and cpc_call > cost_target:
            anomalies.append(
                {
                    "type": "cost_per_call_high",
                    "adset": row["adset_name"],
                    "detail": (
                        f"£{cpc_call:.2f}/call in {row['audience_label']} exceeds the £{cost_target} target. "
                        f"Spend £{row['spend']:.2f} / {row['calls_booked']} calls."
                    ),
                }
            )

    # Landing page booking rate check (8%)
    booking_target = t["landing_page_booking_rate"]
    for row in adset_health:
        br = row.get("booking_rate")
        if br is not None and row["clicks"] >= 100 and br < booking_target:
            anomalies.append(
                {
                    "type": "booking_rate_low",
                    "adset": row["adset_name"],
                    "detail": (
                        f"Booking rate {br*100:.2f}% in {row['audience_label']} below {booking_target*100:.0f}% target. "
                        f"{row['calls_booked']} bookings / {row['clicks']} clicks. Landing page or offer signal."
                    ),
                }
            )

    # Budget split check (50/30/20)
    split_target = t["budget_split"]
    tolerance = t["budget_split_tolerance"]
    total_active_spend = sum(r["spend"] for r in adset_health if r["status"] in ("ACTIVE", "LEARNING", "LEARNING_LIMITED"))
    if total_active_spend > 0:
        spend_by_audience = {}
        for r in adset_health:
            if r["status"] in ("ACTIVE", "LEARNING", "LEARNING_LIMITED"):
                aud = r["audience_type"]
                spend_by_audience[aud] = spend_by_audience.get(aud, 0) + r["spend"]
        audience_to_target_key = {
            "warm": "warm_retargeting",
            "lookalike": "cold_lookalike",
            "interest": "cold_interest",
        }
        for aud, target_key in audience_to_target_key.items():
            actual_share = spend_by_audience.get(aud, 0) / total_active_spend
            target_share = split_target[target_key]
            if abs(actual_share - target_share) > tolerance:
                direction = "over" if actual_share > target_share else "under"
                anomalies.append(
                    {
                        "type": "budget_split_off",
                        "audience": aud,
                        "detail": (
                            f"{AUDIENCE_LABELS.get(aud, aud)} at {actual_share*100:.1f}% of spend, "
                            f"{direction} target {target_share*100:.0f}% by "
                            f"{abs(actual_share-target_share)*100:.1f} pts."
                        ),
                    }
                )

    # Spend concentration check (>40% of ad set spend on one creative)
    concentration_threshold = t["spend_concentration_warn"]
    adset_spend_map = {r["adset_id"]: r["spend"] for r in adset_health}
    creative_spend_by_adset = {}
    for creative in creatives:
        for aud, data in creative["audiences"].items():
            adset_name = data.get("adset_name", aud)
            creative_spend_by_adset.setdefault(adset_name, []).append(
                (creative["creative_name"], data["spend"])
            )
    for r in adset_health:
        entries = creative_spend_by_adset.get(r["adset_name"], [])
        if not entries or r["spend"] <= 0:
            continue
        for creative_name, spend in entries:
            share = spend / r["spend"]
            if share > concentration_threshold:
                anomalies.append(
                    {
                        "type": "spend_concentration",
                        "creative": creative_name,
                        "adset": r["adset_name"],
                        "detail": (
                            f"{creative_name} consumes {share*100:.1f}% of {r['adset_name']} spend "
                            f"(£{spend:.2f} of £{r['spend']:.2f}). Diversify creative load."
                        ),
                    }
                )

    return anomalies


def build_priorities(adset_health, buckets, anomalies, config, week):
    priorities = []
    for a in anomalies:
        if a["type"] == "click_but_no_booking":
            priorities.append(
                f"Check the landing page — {a['adset']} is clicking but not booking. "
                "Post-click problem. Review load speed, above-the-fold CTA, and mobile autoplay/captions."
            )

    learning = [r for r in adset_health if "LEARNING" in r["status"]]
    if learning:
        priorities.append(
            "Let learning complete before making budget moves — "
            f"{len(learning)} ad set(s) still in learning. Avoid changing budgets or pausing creatives "
            "until Meta exits learning (~50 conversion events per ad set)."
        )

    if buckets.get("learning_guardrail_active"):
        priorities.append(
            "Learning-phase guardrail active: all kill/scale verdicts downgraded to watch "
            "until ad sets clear 50 conversion events. Verdicts are directional only."
        )

    if buckets["scale"]:
        names = ", ".join(c["creative_name"] for c in buckets["scale"][:3])
        priorities.append(f"Flag {names} as likely week {week+1} winners to scale.")

    quality_creatives = [c["creative_name"] for c in buckets["scale"] + buckets["watch"] if c.get("quality_flags")]
    if quality_creatives:
        unique = list(dict.fromkeys(quality_creatives))[:3]
        priorities.append(
            f"Review 'below average' quality ranking creatives — {', '.join(unique)}. "
            "Check if the hook could be perceived as clickbait by Meta's system."
        )

    if buckets["concern"]:
        names = ", ".join(c["creative_name"] for c in buckets["concern"][:3])
        priorities.append(
            f"Kill candidates for next review: {names}. "
            "Below 1.5% CTR in 2+ ad sets with sufficient impressions."
        )

    return priorities


def build_report_payload(campaign_id, campaign_name, week, since, until):
    config = load_config()

    adsets = fetch_adsets(campaign_id, since, until)
    for adset in adsets:
        adset["ads"] = fetch_ads_for_adset(adset["id"], since, until)

    adset_health = build_adset_health(adsets)
    creatives = build_creative_matrix(adsets)

    for c in creatives:
        c["signal"] = assign_signal(c, config)

    buckets = bucket_verdicts(creatives, config, week, adset_health=adset_health)
    anomalies = detect_anomalies(adset_health, creatives, config)
    priorities = build_priorities(adset_health, buckets, anomalies, config, week)

    return {
        "meta": {
            "campaign_id": campaign_id,
            "campaign_name": campaign_name,
            "week": week,
            "week_label": config["week_phases"].get(week, {}).get("label", ""),
            "date_range": {"since": since, "until": until},
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "adset_health": adset_health,
        "creative_matrix": creatives,
        "verdicts": buckets,
        "anomalies": anomalies,
        "priorities": priorities,
        "config_thresholds": config["thresholds"],
    }


def save_payload(payload, campaign_name):
    date = datetime.now().strftime("%Y-%m-%d")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "-" for c in campaign_name).strip("-")
    path = OUTPUTS_DIR / f"DAILY-REVIEW-{safe_name}-{date}.json"
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path


def main():
    parser = argparse.ArgumentParser(description="Meta Ads Daily Review — data fetcher")
    parser.add_argument("--campaign", help="Campaign name (partial match)")
    parser.add_argument("--campaign-id", help="Exact campaign ID")
    parser.add_argument("--week", type=int, default=1, help="Current week number (1-6+)")
    parser.add_argument("--days", type=int, default=7, help="Date range in days (default 7)")
    parser.add_argument("--list-campaigns", action="store_true", help="List active campaigns and exit")
    parser.add_argument("--format", choices=["json", "pretty"], default="pretty")
    args = parser.parse_args()

    if not META_ACCESS_TOKEN:
        raise SystemExit("META_ACCESS_TOKEN missing from .env")

    if args.list_campaigns:
        campaigns = list_active_campaigns()
        for c in campaigns:
            print(f"{c['id']}  {c['effective_status']:20s}  {c['name']}")
        return

    campaign_id = resolve_campaign(args)
    campaigns = list_active_campaigns()
    campaign_name = next(
        (c["name"] for c in campaigns if c["id"] == campaign_id),
        args.campaign or campaign_id,
    )

    until = datetime.now().strftime("%Y-%m-%d")
    since = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    payload = build_report_payload(campaign_id, campaign_name, args.week, since, until)
    path = save_payload(payload, campaign_name)

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"Saved: {path}")
        print(f"Ad sets: {len(payload['adset_health'])}")
        print(f"Creatives analysed: {len(payload['creative_matrix'])}")
        print(f"Scale candidates: {len(payload['verdicts']['scale'])}")
        print(f"Concern: {len(payload['verdicts']['concern'])}")
        print(f"Anomalies: {len(payload['anomalies'])}")
        print(f"Priorities: {len(payload['priorities'])}")


if __name__ == "__main__":
    main()
