#!/usr/bin/env python3
"""
Meta API Instagram Post Fetcher
Fetches historical Instagram posts with engagement metrics
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
INSTAGRAM_BUSINESS_ID = os.getenv('INSTAGRAM_BUSINESS_ID')

if not ACCESS_TOKEN or not INSTAGRAM_BUSINESS_ID:
    print("❌ Error: META_ACCESS_TOKEN and INSTAGRAM_BUSINESS_ID required in .env")
    exit(1)

BASE_URL = "https://graph.facebook.com/v21.0"

def fetch_instagram_posts(limit=50):
    """
    Fetch Instagram posts with engagement metrics

    Returns:
        list: Posts with caption, metrics, timestamp
    """

    print(f"📡 Fetching last {limit} Instagram posts...")

    # Fields to retrieve
    fields = [
        "id",
        "caption",
        "media_type",
        "media_url",
        "permalink",
        "timestamp",
        "like_count",
        "comments_count",
        "insights.metric(engagement,impressions,reach,saves,shares)"
    ]

    url = f"{BASE_URL}/{INSTAGRAM_BUSINESS_ID}/media"
    params = {
        "fields": ",".join(fields),
        "limit": limit,
        "access_token": ACCESS_TOKEN
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        posts = []

        for item in data.get('data', []):
            # Extract insights
            insights = {}
            if 'insights' in item and 'data' in item['insights']:
                for insight in item['insights']['data']:
                    metric_name = insight['name']
                    metric_value = insight['values'][0]['value'] if insight.get('values') else 0
                    insights[metric_name] = metric_value

            post = {
                'id': item.get('id'),
                'caption': item.get('caption', ''),
                'media_type': item.get('media_type'),
                'permalink': item.get('permalink'),
                'timestamp': item.get('timestamp'),
                'likes': item.get('like_count', 0),
                'comments': item.get('comments_count', 0),
                'engagement': insights.get('engagement', 0),
                'impressions': insights.get('impressions', 0),
                'reach': insights.get('reach', 0),
                'saves': insights.get('saves', 0),
                'shares': insights.get('shares', 0)
            }

            # Calculate engagement rate
            if post['reach'] > 0:
                # Weighted engagement: comments*3 + saves*5 + shares*7 + likes
                weighted_engagement = (
                    post['likes'] +
                    post['comments'] * 3 +
                    post['saves'] * 5 +
                    post['shares'] * 7
                )
                post['engagement_rate'] = round((weighted_engagement / post['reach']) * 100, 2)
            else:
                post['engagement_rate'] = 0

            posts.append(post)

        print(f"✅ Fetched {len(posts)} posts")

        # Save to JSON
        output_file = "2-instagram/instagram-caption/outputs/instagram_posts.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'fetched_at': datetime.now().isoformat(),
                'total_posts': len(posts),
                'posts': posts
            }, f, indent=2, ensure_ascii=False)

        print(f"💾 Saved to {output_file}")

        return posts

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return []

def print_summary(posts):
    """Print quick summary of fetched posts"""

    if not posts:
        return

    print("\n📊 QUICK SUMMARY")
    print("=" * 50)

    # Top 5 by engagement rate
    sorted_posts = sorted(posts, key=lambda x: x.get('engagement_rate', 0), reverse=True)

    print("\n🔥 Top 5 Posts by Engagement Rate:")
    for i, post in enumerate(sorted_posts[:5], 1):
        caption_preview = post['caption'][:60].replace('\n', ' ') if post['caption'] else 'No caption'
        print(f"{i}. {post['engagement_rate']}% - {caption_preview}...")
        print(f"   👍 {post['likes']} | 💬 {post['comments']} | 💾 {post['saves']} | 👁️ {post['reach']}")

    # Average metrics
    avg_engagement = sum(p.get('engagement_rate', 0) for p in posts) / len(posts)
    avg_reach = sum(p.get('reach', 0) for p in posts) / len(posts)

    print(f"\n📈 Averages:")
    print(f"   Engagement Rate: {avg_engagement:.2f}%")
    print(f"   Reach: {int(avg_reach):,}")
    print(f"   Likes: {int(sum(p['likes'] for p in posts) / len(posts)):,}")
    print(f"   Comments: {int(sum(p['comments'] for p in posts) / len(posts)):,}")

if __name__ == "__main__":
    posts = fetch_instagram_posts(limit=50)
    if posts:
        print_summary(posts)
