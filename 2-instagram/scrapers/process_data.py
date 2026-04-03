#!/usr/bin/env python3
"""
Process Instagram raw data and create analysis
"""

import json
import csv
from pathlib import Path
from datetime import datetime

def process_instagram_data(json_file):
    """Process raw Instagram JSON data"""

    with open(json_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    print(f"📊 Processing {len(raw_data)} posts...\n")

    posts_data = []

    for idx, item in enumerate(raw_data, 1):
        # Extract metrics
        likes = item.get('likesCount', 0)
        comments = item.get('commentsCount', 0)
        video_views = item.get('videoViewCount', 0) or item.get('videoPlayCount', 0)

        # Parse timestamp
        timestamp_str = item.get('timestamp', '')
        try:
            date = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
        except:
            date = ''

        # Extract caption
        caption = item.get('caption', '')

        # Calculate engagement
        engagement = likes + comments

        # Determine type
        post_type = item.get('type', '')
        is_video = post_type == 'Video'

        post_data = {
            'post_number': idx,
            'date': date,
            'type': post_type,
            'caption': caption,
            'caption_length': len(caption),
            'likes': likes,
            'comments': comments,
            'video_views': video_views,
            'engagement': engagement,
            'is_video': is_video,
            'url': item.get('url', ''),
            'shortcode': item.get('shortCode', ''),
            'hashtags': ', '.join(item.get('hashtags', [])),
            'hashtag_count': len(item.get('hashtags', [])),
        }

        posts_data.append(post_data)

    return posts_data

def save_to_csv(data, filename):
    """Save to CSV"""
    headers = ['post_number', 'date', 'type', 'caption', 'caption_length',
               'likes', 'comments', 'video_views', 'engagement', 'url']

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for post in data:
            row = {k: post[k] for k in headers if k in post}
            writer.writerow(row)

    print(f"💾 Saved CSV: {filename}")

def analyze_performance(data):
    """Analyze post performance"""

    print("\n" + "="*80)
    print("📊 BEN HAWKSWORTH - INSTAGRAM PERFORMANCE ANALYSIS")
    print("="*80 + "\n")

    # Overall stats
    total_posts = len(data)
    total_likes = sum(p['likes'] for p in data)
    total_comments = sum(p['comments'] for p in data)
    total_engagement = total_likes + total_comments
    total_video_views = sum(p['video_views'] for p in data)

    avg_likes = total_likes / total_posts
    avg_comments = total_comments / total_posts
    avg_engagement = total_engagement / total_posts

    print(f"📈 OVERALL STATS:")
    print(f"   Total posts analyzed: {total_posts}")
    print(f"   Total likes: {total_likes:,}")
    print(f"   Total comments: {total_comments:,}")
    print(f"   Total engagement: {total_engagement:,}")
    print(f"   Total video views: {total_video_views:,}")
    print(f"   Avg likes per post: {avg_likes:,.1f}")
    print(f"   Avg comments per post: {avg_comments:,.1f}")
    print(f"   Avg engagement per post: {avg_engagement:,.1f}")

    # Video vs Photo
    videos = [p for p in data if p['is_video']]
    photos = [p for p in data if not p['is_video']]

    print(f"\n📹 VIDEO vs 📸 PHOTO:")
    print(f"   Videos: {len(videos)} ({len(videos)/total_posts*100:.1f}%)")
    print(f"   Photos: {len(photos)} ({len(photos)/total_posts*100:.1f}%)")

    if videos:
        avg_video_engagement = sum(v['engagement'] for v in videos) / len(videos)
        avg_video_views = sum(v['video_views'] for v in videos) / len(videos)
        print(f"   Avg video engagement: {avg_video_engagement:,.1f}")
        print(f"   Avg video views: {avg_video_views:,.1f}")

    if photos:
        avg_photo_engagement = sum(p['engagement'] for p in photos) / len(photos)
        print(f"   Avg photo engagement: {avg_photo_engagement:,.1f}")

    # Top 10 posts
    print(f"\n🏆 TOP 10 PERFORMING POSTS (by engagement):")
    print("-" * 80)

    sorted_posts = sorted(data, key=lambda x: x['engagement'], reverse=True)[:10]

    for i, post in enumerate(sorted_posts, 1):
        print(f"\n#{i} - {post['date']} ({post['type']})")
        print(f"   👍 {post['likes']:,} likes | 💬 {post['comments']:,} comments | 📊 {post['engagement']:,} total")
        if post['video_views'] > 0:
            print(f"   📹 {post['video_views']:,} video views")
        print(f"   📝 {post['caption'][:100]}...")
        print(f"   🔗 {post['url']}")

    print("\n" + "="*80 + "\n")

    # Caption analysis
    print("📝 CAPTION ANALYSIS:")
    caption_lengths = [p['caption_length'] for p in data if p['caption_length'] > 0]
    if caption_lengths:
        avg_caption_length = sum(caption_lengths) / len(caption_lengths)
        min_caption = min(caption_lengths)
        max_caption = max(caption_lengths)
        print(f"   Avg caption length: {avg_caption_length:.0f} characters")
        print(f"   Min caption length: {min_caption}")
        print(f"   Max caption length: {max_caption}")

    print("\n" + "="*80 + "\n")

def main():
    """Main execution"""

    # Find latest JSON file
    data_dir = Path("data")
    json_files = list(data_dir.glob("instagram_raw_*.json"))

    if not json_files:
        print("❌ No Instagram raw data found")
        return

    latest_json = max(json_files, key=lambda p: p.stat().st_mtime)

    print(f"📂 Processing: {latest_json.name}\n")

    # Process data
    posts_data = process_instagram_data(latest_json)

    # Save CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = data_dir / f"instagram_processed_{timestamp}.csv"
    save_to_csv(posts_data, csv_file)

    # Analyze
    analyze_performance(posts_data)

    print(f"✅ Analysis complete!")
    print(f"📁 Files saved in: {data_dir.absolute()}")

if __name__ == "__main__":
    main()
