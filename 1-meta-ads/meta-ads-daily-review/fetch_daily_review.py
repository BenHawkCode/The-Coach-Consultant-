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

# IG follower snapshot file. Each run appends {date, followers_count}. The
# delta between the current API value and the most recent prior snapshot is
# "followers acquired" for the Profile Visits campaign KPI.
IG_BUSINESS_ACCOUNT_ID = os.getenv("IG_BUSINESS_ACCOUNT_ID", "17841400157052776")
IG_SNAPSHOT_PATH = SKILL_DIR / "ig_followers_baseline.json"

# Antonio's dashboard clone — source of truth for real Calendly bookings
# (calendly_bookings.json) and stage-tagged paid ROAS (roas_snapshot). The
# weekly cron commits fresh data here every Monday 06:00 UTC.
TCC_DASHBOARD_PATH = Path(os.getenv("TCC_DASHBOARD_PATH", "/tmp/tcc-dashboard"))
CALENDLY_BOOKINGS_PATH = TCC_DASHBOARD_PATH / "public" / "data" / "calendly_bookings.json"

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


# Fallback form-to-book ratio. Only used when Antonio's calendly_bookings.json
# isn't reachable. When it is, we use the real paid_ads counts instead.
FORM_TO_BOOK_RATIO = 4.5


def load_calendly_bookings():
    """Pull real Calendly paid-ads bookings from Antonio's pipeline.

    Returns None if the dashboard clone isn't available — callers must
    fall back to the 4.5:1 directional estimate in that case.
    """
    if not CALENDLY_BOOKINGS_PATH.exists():
        return None
    try:
        data = json.loads(CALENDLY_BOOKINGS_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    summary = data.get("summary", {})
    return {
        "source": "calendly_bookings.json (Antonio pipeline)",
        "fetched_at": data.get("fetched_at"),
        "paid_ads_7d": summary.get("paid_ads_7d"),
        "paid_ads_28d": summary.get("paid_ads_28d"),
        "total_7d": summary.get("total_7d"),
        "total_28d": summary.get("total_28d"),
    }


def extract_form_submits(insights):
    """Pull unique Meta pixel lead events from the 'actions' array.

    Meta returns the same lead under multiple labels (`lead`,
    `offsite_conversion.fb_pixel_lead`, `onsite_conversion.lead_grouped`).
    Summing them triple-counts — that was the 2026-04-17 incident (36 vs
    real 18). Take the max across the pixel-lead family; scheduled-call
    events are counted separately via extract_meta_pixel_calls().

    These are FORM SUBMISSIONS, not booked calls. Ground truth for
    bookings is tracked manually by Mahmoud.
    """
    by_type = {}
    for a in insights.get("actions", []) or []:
        try:
            by_type[a.get("action_type")] = int(a.get("value", 0))
        except (TypeError, ValueError):
            continue
    return max(
        by_type.get("lead", 0),
        by_type.get("offsite_conversion.fb_pixel_lead", 0),
        by_type.get("onsite_conversion.lead_grouped", 0),
    )


def extract_meta_pixel_calls(insights):
    """Narrow Meta-side schedule/booking events, separate from form submits."""
    by_type = {}
    for a in insights.get("actions", []) or []:
        try:
            by_type[a.get("action_type")] = int(a.get("value", 0))
        except (TypeError, ValueError):
            continue
    return by_type.get("schedule_total", 0) + by_type.get(
        "omni_scheduled_conversation", 0
    )


# ---------------------------------------------------------------------------
# IG follower tracking (for TOF Profile Visits campaigns)
#
# Meta Ads API doesn't expose "Instagram follows" per campaign — it's a custom
# column Mahmoud added to the Ads Manager KPI set. Workaround (per Antonio,
# 2026-04-20): hit the IG Business Account endpoint directly, store a daily
# snapshot, and derive `followers_acquired` as the delta between today's
# follower count and the most recent prior snapshot. Cost per follower is
# then `spend / followers_acquired`.
#
# First run creates the baseline (0 acquired). Subsequent runs produce real
# deltas. Snapshot file is committed so the baseline persists across
# machines.
# ---------------------------------------------------------------------------
def fetch_ig_followers_count():
    data = api_get(IG_BUSINESS_ACCOUNT_ID, {"fields": "followers_count,username"})
    return {
        "followers_count": int(data.get("followers_count", 0)),
        "username": data.get("username"),
    }


def load_ig_snapshots():
    if not IG_SNAPSHOT_PATH.exists():
        return []
    try:
        return json.loads(IG_SNAPSHOT_PATH.read_text())
    except json.JSONDecodeError:
        return []


def save_ig_snapshots(snapshots):
    IG_SNAPSHOT_PATH.write_text(json.dumps(snapshots, indent=2))


def record_ig_follower_snapshot(today_iso):
    current = fetch_ig_followers_count()
    snapshots = load_ig_snapshots()
    prior = [s for s in snapshots if s["date"] < today_iso]
    baseline = prior[-1] if prior else None

    # Replace today's snapshot if it already exists (idempotent re-runs)
    snapshots = [s for s in snapshots if s["date"] != today_iso]
    snapshots.append(
        {
            "date": today_iso,
            "followers_count": current["followers_count"],
            "username": current["username"],
        }
    )
    snapshots.sort(key=lambda s: s["date"])
    save_ig_snapshots(snapshots)

    if baseline is None:
        return {
            "current": current["followers_count"],
            "baseline": None,
            "baseline_date": None,
            "followers_acquired": 0,
            "first_run": True,
        }
    return {
        "current": current["followers_count"],
        "baseline": baseline["followers_count"],
        "baseline_date": baseline["date"],
        "followers_acquired": current["followers_count"] - baseline["followers_count"],
        "first_run": False,
    }


# Map Meta's campaign objective to our funnel stage. Profile Visits sits at
# TOF (objective OUTCOME_TRAFFIC) and must be judged on cost per follower,
# not CTR / form submits.
OBJECTIVE_STAGE = {
    "OUTCOME_AWARENESS": "TOF",
    "OUTCOME_TRAFFIC": "TOF",
    "OUTCOME_VIDEO_VIEWS": "TOF",
    "OUTCOME_ENGAGEMENT": "MOF",
    "OUTCOME_LEADS": "BOF",
    "OUTCOME_SALES": "BOF",
}


def fetch_campaign_meta(campaign_id):
    data = api_get(campaign_id, {"fields": "id,name,objective,effective_status"})
    objective = data.get("objective", "UNKNOWN")
    return {
        "id": data.get("id"),
        "name": data.get("name"),
        "objective": objective,
        "stage": OBJECTIVE_STAGE.get(objective, "UNKNOWN"),
        "effective_status": data.get("effective_status"),
    }


def build_adset_health(adsets, stage="BOF", followers_acquired=None, total_campaign_spend=None):
    rows = []
    tof = stage == "TOF"
    for a in adsets:
        ins = a.get("insights", {})
        spend = float(ins.get("spend", 0) or 0)
        clicks = int(ins.get("clicks", 0) or 0)
        form_submits = extract_form_submits(ins)
        meta_pixel_calls = extract_meta_pixel_calls(ins)

        row = {
            "adset_id": a["id"],
            "adset_name": a["name"],
            "audience_type": a["audience_type"],
            "audience_label": AUDIENCE_LABELS.get(a["audience_type"], a["name"]),
            "stage": stage,
            "impressions": int(ins.get("impressions", 0) or 0),
            "clicks": clicks,
            "ctr": float(ins.get("ctr", 0) or 0) / 100,
            "cpc": float(ins.get("cpc", 0) or 0),
            "spend": spend,
            "form_submits": form_submits,
            "cost_per_form_submit": (spend / form_submits) if form_submits > 0 else None,
            "form_submit_rate": (form_submits / clicks) if clicks > 0 else None,
            "estimated_bookings": round(form_submits / FORM_TO_BOOK_RATIO, 1) if form_submits > 0 else 0,
            "meta_pixel_calls": meta_pixel_calls,
            "status": a.get("effective_status", "UNKNOWN"),
        }

        # TOF Profile Visits: cost per IG follower is the scale KPI.
        # Followers acquired is campaign-level (account-level IG snapshot
        # delta), so we pro-rate to the ad set by its spend share.
        if tof and followers_acquired and followers_acquired > 0 and total_campaign_spend:
            share = spend / total_campaign_spend if total_campaign_spend > 0 else 0
            adset_followers = followers_acquired * share
            row["ig_followers_acquired_share"] = round(adset_followers, 2)
            row["cost_per_ig_follower"] = (
                (spend / adset_followers) if adset_followers > 0 else None
            )

        rows.append(row)
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
        total_submits = sum(r.get("form_submits", 0) for r in active_rows)
        if any_learning and total_submits < min_conversions:
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

    # Form-submit / booking anomalies only apply at BOF. At TOF (Profile
    # Visits / Awareness) there's no booking CTA by design, so flagging
    # "clicks with no submits" is a category error per Mahmoud 2026-04-20.
    for row in adset_health:
        if row.get("stage") != "BOF":
            continue
        if row["clicks"] >= 200 and row["form_submits"] == 0:
            anomalies.append(
                {
                    "type": "click_but_no_form_submit",
                    "adset": row["adset_name"],
                    "detail": (
                        f"{row['clicks']} clicks, 0 form submits in {row['audience_label']}. "
                        "Landing page signal, not ad signal."
                    ),
                }
            )

    # Cost-per-form-submit threshold check (£50) — BOF only
    cost_target = t["cost_per_form_submit_target_gbp"]
    for row in adset_health:
        if row.get("stage") != "BOF":
            continue
        cpfs = row.get("cost_per_form_submit")
        if cpfs is not None and cpfs > cost_target:
            anomalies.append(
                {
                    "type": "cost_per_form_submit_high",
                    "adset": row["adset_name"],
                    "detail": (
                        f"£{cpfs:.2f}/form submit in {row['audience_label']} exceeds the £{cost_target} target. "
                        f"Spend £{row['spend']:.2f} / {row['form_submits']} submits."
                    ),
                }
            )

    # Landing page form-submit rate check (8%) — BOF only
    submit_rate_target = t["landing_page_form_submit_rate"]
    for row in adset_health:
        if row.get("stage") != "BOF":
            continue
        fsr = row.get("form_submit_rate")
        if fsr is not None and row["clicks"] >= 100 and fsr < submit_rate_target:
            anomalies.append(
                {
                    "type": "form_submit_rate_low",
                    "adset": row["adset_name"],
                    "detail": (
                        f"Form submit rate {fsr*100:.2f}% in {row['audience_label']} below {submit_rate_target*100:.0f}% target. "
                        f"{row['form_submits']} submits / {row['clicks']} clicks. Landing page or offer signal."
                    ),
                }
            )

    # Budget split check (50/30/20 Warm/LAL/Interest) — BOF only.
    # Other stages have different audience structures, split check doesn't
    # apply (TOF is cold-only, MOF is its own thing).
    split_target = t["budget_split"]
    tolerance = t["budget_split_tolerance"]
    bof_rows = [r for r in adset_health if r.get("stage") == "BOF"]
    total_active_spend = sum(r["spend"] for r in bof_rows if r["status"] in ("ACTIVE", "LEARNING", "LEARNING_LIMITED"))
    if total_active_spend > 0:
        spend_by_audience = {}
        for r in bof_rows:
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
        if a["type"] == "click_but_no_form_submit":
            priorities.append(
                f"Check the landing page — {a['adset']} is clicking but not submitting. "
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
    campaign_meta = fetch_campaign_meta(campaign_id)
    stage = campaign_meta["stage"]

    # IG follower delta is only relevant for TOF Profile Visits. Snapshot
    # always runs so the baseline builds up over time regardless of which
    # campaign we're reviewing.
    today_iso = datetime.now().strftime("%Y-%m-%d")
    ig_snapshot = record_ig_follower_snapshot(today_iso)

    adsets = fetch_adsets(campaign_id, since, until)
    for adset in adsets:
        adset["ads"] = fetch_ads_for_adset(adset["id"], since, until)

    followers_acquired = ig_snapshot["followers_acquired"] if stage == "TOF" else None
    total_campaign_spend = sum(
        float(a.get("insights", {}).get("spend", 0) or 0) for a in adsets
    )
    adset_health = build_adset_health(
        adsets,
        stage=stage,
        followers_acquired=followers_acquired,
        total_campaign_spend=total_campaign_spend,
    )
    creatives = build_creative_matrix(adsets)

    for c in creatives:
        c["signal"] = assign_signal(c, config)

    buckets = bucket_verdicts(creatives, config, week, adset_health=adset_health)
    anomalies = detect_anomalies(adset_health, creatives, config)
    priorities = build_priorities(adset_health, buckets, anomalies, config, week)

    # TOF: override the BOF-flavoured CTR/CPC scale priority with the correct
    # cost-per-follower framing per Mahmoud 2026-04-20.
    if stage == "TOF":
        if ig_snapshot["first_run"]:
            priorities.insert(
                0,
                "IG follower snapshot created today (baseline). Re-run tomorrow "
                "for the first real cost-per-follower reading.",
            )
        elif followers_acquired and followers_acquired > 0 and total_campaign_spend > 0:
            cpf = total_campaign_spend / followers_acquired
            priorities.insert(
                0,
                f"Profile Visits — £{cpf:.2f} per IG follower "
                f"({followers_acquired} followers acquired since "
                f"{ig_snapshot['baseline_date']}, spend £{total_campaign_spend:.2f}). "
                "This is the scale KPI for TOF, not CTR/CPC.",
            )
        else:
            priorities.insert(
                0,
                "Profile Visits — no follower growth measured since last snapshot. "
                "Cost per follower unavailable.",
            )

    # Real booked calls from Antonio's Calendly pipeline. Falls back to the
    # 4.5:1 directional estimate only when the dashboard clone isn't present.
    calendly = load_calendly_bookings()
    total_form_submits = sum(r.get("form_submits", 0) for r in adset_health)

    if stage == "BOF" and calendly is not None:
        paid_7d = calendly["paid_ads_7d"] or 0
        if paid_7d > 0 and total_campaign_spend > 0:
            priorities.insert(
                0,
                f"Real Calendly bookings (paid-ads, 7d): {paid_7d} at "
                f"£{total_campaign_spend/paid_7d:.2f}/call "
                f"(spend £{total_campaign_spend:.2f}). "
                f"28d pipeline: {calendly['paid_ads_28d']} bookings. "
                "Ground truth — use this over form_submits-based estimates.",
            )
        elif paid_7d == 0:
            priorities.insert(
                0,
                "Real Calendly bookings (paid-ads, 7d): 0. "
                "Paid ads driving clicks but no booked calls yet — "
                "landing page / offer / follow-up check.",
            )
    elif stage == "BOF" and calendly is None:
        priorities.insert(
            0,
            "Calendly bookings file not found (is tcc-dashboard cloned at "
            f"{TCC_DASHBOARD_PATH}?). Falling back to 4.5:1 directional "
            "estimate from form submits. Pull the dashboard repo for real numbers.",
        )

    bookings_block = {
        "source": None,
        "paid_ads_7d": None,
        "paid_ads_28d": None,
        "cost_per_paid_call_7d": None,
        "roas_display": None,  # "Pending" when 0 revenue + >0 calls, else numeric
        "estimated_bookings_fallback": round(total_form_submits / FORM_TO_BOOK_RATIO, 1),
    }
    if calendly is not None and stage == "BOF":
        paid_7d = calendly["paid_ads_7d"] or 0
        bookings_block["source"] = calendly["source"]
        bookings_block["paid_ads_7d"] = paid_7d
        bookings_block["paid_ads_28d"] = calendly["paid_ads_28d"]
        bookings_block["fetched_at"] = calendly["fetched_at"]
        if paid_7d > 0 and total_campaign_spend > 0:
            bookings_block["cost_per_paid_call_7d"] = round(total_campaign_spend / paid_7d, 2)
            # ROAS needs revenue which daily-review doesn't have; weekly does.
            # Per Antonio 2026-04-20: when paid calls > 0 and revenue = 0,
            # show "Pending" rather than "0.00x" so Ben doesn't misread the
            # pipeline-pending state as "ads don't work".
            bookings_block["roas_display"] = "Pending"

    campaign_summary = {
        "stage": stage,
        "objective": campaign_meta["objective"],
        "total_spend": total_campaign_spend,
        "bookings": bookings_block,
    }
    if stage == "TOF":
        campaign_summary["ig_followers"] = {
            "account_id": IG_BUSINESS_ACCOUNT_ID,
            "username": ig_snapshot.get("baseline") and None,
            "current_total": ig_snapshot["current"],
            "baseline_date": ig_snapshot["baseline_date"],
            "baseline_total": ig_snapshot["baseline"],
            "followers_acquired": ig_snapshot["followers_acquired"],
            "first_run": ig_snapshot["first_run"],
            "cost_per_follower_campaign": (
                round(total_campaign_spend / ig_snapshot["followers_acquired"], 2)
                if ig_snapshot["followers_acquired"] and ig_snapshot["followers_acquired"] > 0
                else None
            ),
            "source": "IG Business Account API + daily snapshot delta",
        }

    return {
        "meta": {
            "campaign_id": campaign_id,
            "campaign_name": campaign_name,
            "week": week,
            "week_label": config["week_phases"].get(week, {}).get("label", ""),
            "date_range": {"since": since, "until": until},
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "campaign_summary": campaign_summary,
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
