#!/usr/bin/env python3
"""
Verify Instagram usernames from the competitor list.
Checks if each username exists and grabs basic profile info.

Uses Apify actor: apify/instagram-scraper (profile info only, no posts)

Usage:
    python verify_usernames.py              # Verify all
    python verify_usernames.py --tier 1     # Verify specific tier only
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from apify_client import ApifyClient


SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"

# Import competitor list from main scraper
from ig_competitor_scraper import COMPETITORS


def load_env() -> Dict[str, str]:
    """Load environment variables from project root .env file."""
    env_path = Path(__file__).parent.parent.parent / '.env'
    env_vars = {}
    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        return env_vars
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value.strip('"').strip("'")
    return env_vars


def verify_username(client: ApifyClient, username: str) -> Dict:
    """Check if an Instagram username exists and get basic info."""
    run_input = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "details",
        "resultsLimit": 1,
        "searchType": "user",
        "searchLimit": 1,
    }

    try:
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        if items:
            profile = items[0]
            return {
                "username": username,
                "status": "FOUND",
                "full_name": profile.get("fullName", ""),
                "followers": profile.get("followersCount", 0),
                "following": profile.get("followsCount", 0),
                "posts": profile.get("postsCount", 0),
                "bio": (profile.get("biography", "") or "")[:100],
                "verified": profile.get("verified", False),
                "actual_username": profile.get("username", username),
            }
        else:
            return {"username": username, "status": "NOT_FOUND"}

    except Exception as e:
        return {"username": username, "status": "ERROR", "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Verify Instagram usernames")
    parser.add_argument("--tier", type=int, help="Verify specific tier only")
    args = parser.parse_args()

    competitors = COMPETITORS
    if args.tier is not None:
        competitors = [c for c in COMPETITORS if c["tier"] == args.tier]

    print(f"\n{'='*60}")
    print(f"  Instagram Username Verification")
    print(f"  Checking {len(competitors)} profiles")
    print(f"{'='*60}\n")

    env = load_env()
    apify_token = env.get('APIFY_API_TOKEN')
    if not apify_token:
        print("Error: APIFY_API_TOKEN not found in .env")
        return

    client = ApifyClient(apify_token)

    results = []
    found = 0
    not_found = 0
    errors = 0

    for i, comp in enumerate(competitors, 1):
        username = comp["username"]
        print(f"[{i}/{len(competitors)}] @{username} ({comp['name']})...", end=" ", flush=True)

        result = verify_username(client, username)
        result["name"] = comp["name"]
        result["tier"] = comp["tier"]
        results.append(result)

        if result["status"] == "FOUND":
            found += 1
            actual = result.get("actual_username", username)
            mismatch = f" (actual: @{actual})" if actual != username else ""
            print(f"✅ {result['followers']:,} followers, {result['posts']} posts{mismatch}")
        elif result["status"] == "NOT_FOUND":
            not_found += 1
            print(f"❌ NOT FOUND")
        else:
            errors += 1
            print(f"⚠️ ERROR: {result.get('error', 'unknown')}")

    # Save results
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime('%Y-%m-%d')
    output_path = DATA_DIR / f"username-verification-{now}.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    # Print summary
    print(f"\n{'='*60}")
    print(f"  Results: {found} found | {not_found} not found | {errors} errors")
    print(f"  Saved to: {output_path}")
    print(f"{'='*60}\n")

    # Print not found list for fixing
    if not_found > 0 or errors > 0:
        print("NEEDS FIXING:")
        for r in results:
            if r["status"] != "FOUND":
                print(f"  - @{r['username']} ({r['name']}) — {r['status']}")

    # Print username corrections if any
    corrections = [r for r in results if r["status"] == "FOUND" and r.get("actual_username") != r["username"]]
    if corrections:
        print("\nUSERNAME CORRECTIONS:")
        for r in corrections:
            print(f"  - @{r['username']} → @{r['actual_username']} ({r['name']})")


if __name__ == "__main__":
    main()
