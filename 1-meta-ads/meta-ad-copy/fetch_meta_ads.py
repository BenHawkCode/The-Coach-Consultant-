#!/usr/bin/env python3
"""
Meta Ads Performance Fetcher
Fetches top performing ads from Meta API with real-time metrics
"""

import os
import sys
import json
import requests
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
META_ACCOUNT_ID = os.getenv('META_ACCOUNT_ID', '208457557796486')

COACH_KEYWORDS = [
    'coach', 'consultant', 'service provider',
    'business owner', 'bof', 'masterclass', 'strategies'
]

def fetch_ads(limit=100, campaign=None, days=None):
    """Fetch ads from Meta API"""
    url = f'https://graph.facebook.com/v21.0/act_{META_ACCOUNT_ID}/ads'

    params = {
        'access_token': META_ACCESS_TOKEN,
        'fields': 'name,status,creative{title,body},insights{impressions,clicks,ctr,spend}',
        'limit': limit
    }

    # Add date filter if specified
    if days:
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        params['filtering'] = json.dumps([{
            'field': 'ad.created_time',
            'operator': 'GREATER_THAN',
            'value': start_date
        }])

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.json()}")
        sys.exit(1)

    return response.json().get('data', [])


def filter_coach_ads(ads):
    """Filter for Coach Consultant related ads"""
    coach_ads = []

    for ad in ads:
        name = ad.get('name', '').lower()
        body = ad.get('creative', {}).get('body', '').lower() if 'creative' in ad else ''

        # Check if ad is Coach Consultant related
        is_coach_ad = any(keyword in name or keyword in body for keyword in COACH_KEYWORDS)

        if is_coach_ad:
            coach_ads.append(ad)

    return coach_ads


def extract_performance(ads):
    """Extract ads with performance data"""
    ads_with_performance = []

    for ad in ads:
        if 'insights' not in ad or not ad['insights'].get('data'):
            continue

        insights = ad['insights']['data'][0]
        clicks = int(insights.get('clicks', 0))

        if clicks == 0:
            continue

        ads_with_performance.append({
            'name': ad.get('name', 'N/A'),
            'title': ad.get('creative', {}).get('title', 'N/A'),
            'body': ad.get('creative', {}).get('body', 'N/A'),
            'status': ad.get('status', 'N/A'),
            'clicks': clicks,
            'ctr': float(insights.get('ctr', 0)),
            'impressions': int(insights.get('impressions', 0)),
            'spend': float(insights.get('spend', 0))
        })

    return ads_with_performance


def main():
    parser = argparse.ArgumentParser(description='Fetch Meta Ads performance data')
    parser.add_argument('--top', type=int, default=10, help='Number of top performers to show')
    parser.add_argument('--sort', choices=['clicks', 'ctr', 'spend'], default='clicks', help='Sort by metric')
    parser.add_argument('--campaign', type=str, help='Filter by campaign name')
    parser.add_argument('--days', type=int, help='Filter by days back (e.g., 90)')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='Output format')

    args = parser.parse_args()

    # Check credentials
    if not META_ACCESS_TOKEN:
        print("Error: META_ACCESS_TOKEN not found in .env file")
        sys.exit(1)

    # Fetch ads
    print(f"Fetching ads from Meta account {META_ACCOUNT_ID}...")
    all_ads = fetch_ads(limit=100, campaign=args.campaign, days=args.days)
    print(f"Total ads fetched: {len(all_ads)}")

    # Filter Coach Consultant ads
    coach_ads = filter_coach_ads(all_ads)
    print(f"Coach Consultant ads: {len(coach_ads)}")

    # Extract performance
    ads_with_performance = extract_performance(coach_ads)
    print(f"Ads with performance data: {len(ads_with_performance)}")

    # Sort by metric
    ads_with_performance.sort(key=lambda x: x[args.sort], reverse=True)

    # Output
    top_ads = ads_with_performance[:args.top]

    if args.format == 'json':
        print(json.dumps(top_ads, indent=2))
    else:
        print(f"\n=== TOP {args.top} PERFORMING ADS (by {args.sort}) ===\n")
        for i, ad in enumerate(top_ads, 1):
            print(f"{i}. {ad['name']} - {ad['status']}")
            print(f"   Title: {ad['title']}")
            print(f"   Body: {ad['body'][:100]}...")
            print(f"   📊 {ad['clicks']} clicks | {ad['ctr']:.2f}% CTR | {ad['impressions']} imp | £{ad['spend']:.2f}")
            print()


if __name__ == '__main__':
    main()
