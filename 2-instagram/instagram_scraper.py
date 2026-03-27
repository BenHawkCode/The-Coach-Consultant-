#!/usr/bin/env python3
"""
Instagram Public Profile Scraper
Scrapes Ben Hawksworth's public Instagram posts for engagement analysis
"""

import instaloader
import json
import csv
from datetime import datetime
from pathlib import Path

def scrape_instagram_profile(username, max_posts=100):
    """
    Scrape public Instagram profile data

    Args:
        username: Instagram username
        max_posts: Maximum number of posts to scrape

    Returns:
        List of post data dictionaries
    """
    print(f"🔍 Scraping Instagram profile: @{username}")
    print(f"📊 Max posts: {max_posts}\n")

    # Initialize Instaloader
    L = instaloader.Instaloader()

    # Disable download features (we only want metadata)
    L.download_pictures = False
    L.download_videos = False
    L.download_video_thumbnails = False
    L.download_geotags = False
    L.download_comments = False
    L.save_metadata = False

    try:
        # Load profile
        profile = instaloader.Profile.from_username(L.context, username)

        print(f"✅ Profile found: {profile.full_name}")
        print(f"👥 Followers: {profile.followers:,}")
        print(f"📸 Total posts: {profile.mediacount:,}\n")

        # Scrape posts
        posts_data = []
        count = 0

        print("🚀 Starting scrape...\n")

        for post in profile.get_posts():
            if count >= max_posts:
                break

            count += 1

            # Extract caption (handle None)
            caption = post.caption if post.caption else ""

            # Extract hashtags
            hashtags = post.caption_hashtags if post.caption_hashtags else []

            # Calculate engagement rate
            engagement = post.likes + post.comments
            engagement_rate = (engagement / profile.followers * 100) if profile.followers > 0 else 0

            post_data = {
                'post_number': count,
                'shortcode': post.shortcode,
                'url': f"https://www.instagram.com/p/{post.shortcode}/",
                'date': post.date_utc.strftime('%Y-%m-%d %H:%M:%S'),
                'caption': caption,
                'caption_length': len(caption),
                'likes': post.likes,
                'comments': post.comments,
                'engagement': engagement,
                'engagement_rate': round(engagement_rate, 2),
                'is_video': post.is_video,
                'hashtags': list(hashtags),
                'hashtag_count': len(hashtags),
                'mentions': post.caption_mentions if post.caption_mentions else [],
            }

            posts_data.append(post_data)

            # Progress update
            if count % 10 == 0:
                print(f"✅ Scraped {count} posts...")

        print(f"\n✅ Successfully scraped {len(posts_data)} posts!\n")
        return posts_data

    except Exception as e:
        print(f"❌ Error scraping profile: {e}")
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
               'engagement', 'engagement_rate', 'is_video', 'hashtag_count', 'url']

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for post in data:
            # Only write selected fields for CSV
            row = {k: post[k] for k in headers if k in post}
            writer.writerow(row)

    print(f"💾 Saved to CSV: {filename}")

def analyze_top_posts(data, top_n=10):
    """Analyze top performing posts"""
    if not data:
        print("❌ No data to analyze")
        return

    print(f"\n📊 TOP {top_n} PERFORMING POSTS (by engagement):\n")
    print("-" * 80)

    # Sort by engagement
    sorted_posts = sorted(data, key=lambda x: x['engagement'], reverse=True)

    for i, post in enumerate(sorted_posts[:top_n], 1):
        print(f"\n#{i} - {post['date']}")
        print(f"👍 {post['likes']:,} likes | 💬 {post['comments']:,} comments | 📊 {post['engagement_rate']}% engagement rate")
        print(f"📝 Caption preview: {post['caption'][:100]}...")
        print(f"🔗 {post['url']}")

    print("\n" + "-" * 80)

def main():
    """Main execution"""
    username = "benhawksworth_"
    max_posts = 100

    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Scrape profile
    posts_data = scrape_instagram_profile(username, max_posts)

    if not posts_data:
        print("❌ No data scraped. Exiting.")
        return

    # Generate filenames with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = data_dir / f"instagram_data_{timestamp}.json"
    csv_file = data_dir / f"instagram_data_{timestamp}.csv"

    # Save data
    save_to_json(posts_data, json_file)
    save_to_csv(posts_data, csv_file)

    # Analyze top posts
    analyze_top_posts(posts_data, top_n=10)

    print(f"\n✅ Scraping complete!")
    print(f"📁 Files saved in: {data_dir.absolute()}")

if __name__ == "__main__":
    main()
