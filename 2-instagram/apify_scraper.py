#!/usr/bin/env python3
"""
Instagram Scraper using Apify
Scrapes Ben Hawksworth's Instagram profile using Apify's Instagram Profile Scraper
"""

from apify_client import ApifyClient
import json
import csv
from datetime import datetime
from pathlib import Path

# Apify API token
APIFY_API_TOKEN = "REMOVED_USE_ENV"

def scrape_instagram_with_apify(username, max_posts=100):
    """
    Scrape Instagram profile using Apify

    Args:
        username: Instagram username
        max_posts: Maximum number of posts to scrape

    Returns:
        List of post data
    """
    print(f"🔍 Scraping Instagram with Apify: @{username}")
    print(f"📊 Max posts: {max_posts}\n")

    # Initialize Apify client
    client = ApifyClient(APIFY_API_TOKEN)

    # Instagram Scraper actor ID
    actor_id = "apify/instagram-scraper"

    # Run input
    run_input = {
        "username": [username],
        "resultsLimit": max_posts,
    }

    print("🚀 Starting Apify actor...\n")

    try:
        # Run the actor and wait for completion
        run = client.actor(actor_id).call(run_input=run_input)

        print("✅ Actor run completed!")
        print(f"📦 Fetching results...\n")

        # Fetch results from dataset
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        print(f"✅ Retrieved {len(items)} posts!\n")

        # Process and structure data
        posts_data = []

        for idx, item in enumerate(items, 1):
            # Extract engagement metrics
            likes = item.get('likesCount', 0)
            comments = item.get('commentsCount', 0)

            post_data = {
                'post_number': idx,
                'id': item.get('id', ''),
                'shortcode': item.get('shortCode', ''),
                'url': item.get('url', ''),
                'type': item.get('type', ''),
                'caption': item.get('caption', ''),
                'caption_length': len(item.get('caption', '')),
                'timestamp': item.get('timestamp', ''),
                'date': datetime.fromisoformat(item.get('timestamp', '').replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S') if item.get('timestamp') else '',
                'likes': likes,
                'comments': comments,
                'engagement': likes + comments,
                'is_video': item.get('type', '') == 'Video',
                'display_url': item.get('displayUrl', ''),
                'video_url': item.get('videoUrl', ''),
                'video_view_count': item.get('videoViewCount', 0),
                'hashtags': item.get('hashtags', []),
                'hashtag_count': len(item.get('hashtags', [])),
                'mentions': item.get('mentions', []),
            }

            posts_data.append(post_data)

        return posts_data

    except Exception as e:
        print(f"❌ Error running Apify actor: {e}")
        return []

def save_to_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to JSON: {filename}")

def save_to_csv(data, filename):
    """Save data to CSV file"""
    if not data:
        print("❌ No data to save to CSV")
        return

    # CSV headers
    headers = ['post_number', 'date', 'caption', 'likes', 'comments',
               'engagement', 'is_video', 'video_view_count', 'hashtag_count', 'url']

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for post in data:
            # Only write selected fields for CSV
            row = {k: post[k] for k in headers if k in post}
            writer.writerow(row)

    print(f"💾 Saved to CSV: {filename}")

def analyze_posts(data):
    """Analyze post performance"""
    if not data:
        print("❌ No data to analyze")
        return

    print("\n" + "="*80)
    print("📊 INSTAGRAM PERFORMANCE ANALYSIS")
    print("="*80 + "\n")

    # Overall stats
    total_posts = len(data)
    total_likes = sum(p['likes'] for p in data)
    total_comments = sum(p['comments'] for p in data)
    total_engagement = total_likes + total_comments

    avg_likes = total_likes / total_posts if total_posts > 0 else 0
    avg_comments = total_comments / total_posts if total_posts > 0 else 0
    avg_engagement = total_engagement / total_posts if total_posts > 0 else 0

    print(f"📈 OVERALL STATS:")
    print(f"   Total posts: {total_posts}")
    print(f"   Total likes: {total_likes:,}")
    print(f"   Total comments: {total_comments:,}")
    print(f"   Total engagement: {total_engagement:,}")
    print(f"   Avg likes per post: {avg_likes:,.0f}")
    print(f"   Avg comments per post: {avg_comments:,.0f}")
    print(f"   Avg engagement per post: {avg_engagement:,.0f}")

    # Video vs Photo performance
    videos = [p for p in data if p['is_video']]
    photos = [p for p in data if not p['is_video']]

    print(f"\n📹 VIDEO vs 📸 PHOTO:")
    print(f"   Videos: {len(videos)} ({len(videos)/total_posts*100:.1f}%)")
    print(f"   Photos: {len(photos)} ({len(photos)/total_posts*100:.1f}%)")

    if videos:
        avg_video_engagement = sum(v['engagement'] for v in videos) / len(videos)
        print(f"   Avg video engagement: {avg_video_engagement:,.0f}")

    if photos:
        avg_photo_engagement = sum(p['engagement'] for p in photos) / len(photos)
        print(f"   Avg photo engagement: {avg_photo_engagement:,.0f}")

    # Top 10 performing posts
    print(f"\n🏆 TOP 10 PERFORMING POSTS:")
    print("-" * 80)

    sorted_posts = sorted(data, key=lambda x: x['engagement'], reverse=True)[:10]

    for i, post in enumerate(sorted_posts, 1):
        print(f"\n#{i} - {post['date']}")
        print(f"   👍 {post['likes']:,} likes | 💬 {post['comments']:,} comments | 📊 {post['engagement']:,} total")
        print(f"   📝 {post['caption'][:100]}...")
        print(f"   🔗 {post['url']}")

    print("\n" + "="*80 + "\n")

def main():
    """Main execution"""
    username = "benhawksworth_"
    max_posts = 100

    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Scrape with Apify
    posts_data = scrape_instagram_with_apify(username, max_posts)

    if not posts_data:
        print("❌ No data scraped. Exiting.")
        return

    # Generate filenames with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = data_dir / f"instagram_apify_{timestamp}.json"
    csv_file = data_dir / f"instagram_apify_{timestamp}.csv"

    # Save data
    save_to_json(posts_data, json_file)
    save_to_csv(posts_data, csv_file)

    # Analyze posts
    analyze_posts(posts_data)

    print(f"✅ Scraping complete!")
    print(f"📁 Files saved in: {data_dir.absolute()}")

if __name__ == "__main__":
    main()
