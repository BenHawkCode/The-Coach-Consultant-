#!/usr/bin/env python3
"""
Simple Apify Instagram Scraper
Using direct URL approach
"""

from apify_client import ApifyClient
import json
from pathlib import Path
from datetime import datetime

# Apify API token
APIFY_API_TOKEN = "apify_api_gD5KBMOt4nG3h22oqbj9IjLKYvtZvc2gTvhr"

def scrape_instagram_posts():
    """Scrape Instagram posts using Apify"""

    print("🔍 Testing Apify Instagram scraper...")
    print("📱 Profile: @benhawksworth_\n")

    # Initialize client
    client = ApifyClient(APIFY_API_TOKEN)

    # Use Apify's official Instagram Scraper
    actor_id = "apify/instagram-scraper"

    # Run input according to docs
    run_input = {
        "directUrls": ["https://www.instagram.com/benhawksworth_/"],
        "resultsType": "posts",
        "resultsLimit": 100,
        "searchType": "user",
        "searchLimit": 1,
    }

    print("🚀 Starting Apify actor: zuzka/instagram-posts-scraper\n")

    try:
        # Run actor
        run = client.actor(actor_id).call(run_input=run_input)

        print("✅ Actor completed!")
        print("📦 Fetching results...\n")

        # Get results
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        print(f"✅ Retrieved {len(items)} items!\n")

        if items:
            # Save raw data
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = data_dir / f"instagram_raw_{timestamp}.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=2, ensure_ascii=False)

            print(f"💾 Saved to: {output_file}\n")

            # Print first item to see structure
            print("📋 First item structure:")
            print(json.dumps(items[0], indent=2)[:500] + "...\n")

        return items

    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    scrape_instagram_posts()
