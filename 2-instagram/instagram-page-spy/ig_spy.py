#!/usr/bin/env python3
"""
Instagram Page Spy - Competitor Profile Intelligence Tool
The Coach Consultant - AI Content Generation System

Scrapes any Instagram profile and generates a comprehensive intelligence report:
- Content type breakdown (carousel, image, video/reel)
- Engagement metrics (likes, comments, engagement rate)
- Top performing posts
- Hook pattern analysis (caption openings)
- CTA pattern analysis
- Posting frequency and schedule
- Hashtag analysis
- Actionable insights

Uses Apify actor: apify/instagram-scraper

Usage:
    python ig_spy.py <instagram_username>
    python ig_spy.py danmartell
    python ig_spy.py "benhawksworth_"
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter
from apify_client import ApifyClient


# --- Configuration ---

DEFAULT_MAX_POSTS = 50


# --- Environment ---

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


# --- Scraping ---

def scrape_instagram_profile(client: ApifyClient, username: str, max_posts: int = DEFAULT_MAX_POSTS) -> List[Dict]:
    """
    Scrape Instagram profile using apify/instagram-scraper.

    Args:
        client: Authenticated ApifyClient
        username: Instagram username (without @)
        max_posts: Maximum number of posts to scrape

    Returns:
        List of post objects from Apify
    """
    run_input = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": max_posts,
        "searchType": "user",
        "searchLimit": 1,
    }

    print(f"Scraping @{username} (up to {max_posts} posts)...")

    try:
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        posts = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        print(f"  Found {len(posts)} posts")
        return posts
    except Exception as e:
        print(f"  Error scraping @{username}: {e}")
        return []


# --- Classification ---

def classify_hook_type(text: str) -> str:
    """Classify the hook type based on the first 125 characters of caption."""
    if not text:
        return "Unknown"

    opening = text[:125].lower()

    if '?' in opening:
        return "Question"
    elif any(w in opening for w in ['struggling', 'problem', 'challenge', 'frustrated', 'stuck', 'tired of', 'stop', "don't", 'never']):
        return "Pain Point"
    elif any(c.isdigit() for c in opening) and any(w in opening for w in ['£', '$', '%', 'x', 'grew', 'added', 'made', 'increase', 'revenue', 'million', 'k', 'clients']):
        return "Metric/Result"
    elif any(w in opening for w in ['secret', 'hidden', 'nobody', 'most people', 'everyone', 'truth', 'lie', 'myth']):
        return "Bold Statement"
    elif any(w in opening for w in ['when i', 'i was', 'my first', 'back in', 'i remember', 'story', 'last year', 'years ago']):
        return "Story"
    elif any(w in opening for w in ['how to', "here's how", '3 ways', '5 steps', 'framework', 'step 1', 'guide']):
        return "How-To/Framework"
    elif any(w in opening for w in ['comment', 'save this', 'tag someone', 'share this', 'dm me', 'drop a']):
        return "Engagement Bait"
    else:
        return "Statement"


def classify_cta(text: str) -> str:
    """Classify the CTA style from caption text."""
    if not text:
        return "No CTA"

    lower = text.lower()

    if any(p in lower for p in ['link in bio', 'click the link', 'dm me', 'dm us', 'book a call', 'sign up', 'download', 'register', 'apply now']):
        return "Hard CTA"
    elif any(p in lower for p in ['comment', 'tag someone', 'tag a friend', 'share this', 'save this', 'drop a', 'type', 'say']):
        return "Engagement CTA"
    elif any(p in lower for p in ['follow', 'turn on notifications', 'hit the bell']):
        return "Follow CTA"
    elif any(p in lower for p in ['what do you think', 'let me know', 'thoughts?', 'agree?', 'do you agree']):
        return "Soft CTA"
    else:
        return "No CTA"


def classify_content_type(post: Dict) -> str:
    """Classify the content type of an Instagram post."""
    post_type = post.get('type', '').lower()

    if post_type == 'sidecar':
        return "Carousel"
    elif post_type == 'video':
        return "Video/Reel"
    elif post_type == 'image':
        return "Image"
    else:
        # Fallback detection
        if post.get('videoUrl'):
            return "Video/Reel"
        return "Image"


# --- Analysis ---

def analyze_post(post: Dict) -> Dict:
    """Extract and analyze key data from a single Instagram post."""
    caption = post.get('caption', '') or ''
    likes = post.get('likesCount', 0) or 0
    comments = post.get('commentsCount', 0) or 0
    timestamp = post.get('timestamp', '')

    # Parse timestamp
    parsed_date = None
    if timestamp:
        try:
            parsed_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            pass

    # Engagement score: likes + (comments * 3) - comments are higher intent on IG
    engagement_score = likes + (comments * 3)

    return {
        'caption': caption,
        'opening_line': caption[:125] if caption else '',
        'caption_length': len(caption),
        'hook_type': classify_hook_type(caption),
        'cta_style': classify_cta(caption),
        'content_type': classify_content_type(post),
        'likes': likes,
        'comments': comments,
        'engagement_score': engagement_score,
        'video_views': post.get('videoViewCount', 0) or 0,
        'url': post.get('url', ''),
        'timestamp': timestamp,
        'parsed_date': parsed_date,
        'hashtags': post.get('hashtags', []) or [],
        'mentions': post.get('mentions', []) or [],
    }


def compute_posting_frequency(posts: List[Dict]) -> Dict:
    """Calculate posting frequency from post timestamps."""
    dates = [p['parsed_date'] for p in posts if p.get('parsed_date')]

    if len(dates) < 2:
        return {'per_week': 0, 'per_month': 0, 'trend': 'insufficient data', 'total_days': 0}

    dates.sort()
    total_days = (dates[-1] - dates[0]).days or 1
    total_posts = len(dates)
    per_week = total_posts / (total_days / 7) if total_days >= 7 else total_posts
    per_month = total_posts / (total_days / 30) if total_days >= 30 else total_posts

    # Trend: compare first half vs second half
    mid = len(dates) // 2
    first_half_span = (dates[mid] - dates[0]).days or 1
    second_half_span = (dates[-1] - dates[mid]).days or 1
    first_rate = mid / first_half_span
    second_rate = (len(dates) - mid) / second_half_span

    if second_rate > first_rate * 1.2:
        trend = "increasing"
    elif second_rate < first_rate * 0.8:
        trend = "decreasing"
    else:
        trend = "stable"

    return {
        'per_week': round(per_week, 1),
        'per_month': round(per_month, 1),
        'trend': trend,
        'total_days': total_days,
    }


def compute_posting_schedule(posts: List[Dict]) -> Dict:
    """Calculate posting schedule (day-of-week and hour distribution)."""
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = Counter()
    hour_counts = Counter()

    for p in posts:
        dt = p.get('parsed_date')
        if not dt:
            continue
        day_counts[day_names[dt.weekday()]] += 1
        hour_counts[dt.hour] += 1

    return {
        'by_day': {day: day_counts.get(day, 0) for day in day_names},
        'by_hour': dict(sorted(hour_counts.items())) if hour_counts else {},
    }


def compute_distribution(items: List[str]) -> Dict[str, Dict]:
    """Compute percentage distribution from a list of categories."""
    counts = Counter(items)
    total = len(items) or 1
    return {
        k: {'count': v, 'percentage': round(v / total * 100, 1)}
        for k, v in counts.most_common()
    }


def compute_engagement_by_type(posts: List[Dict]) -> Dict[str, Dict]:
    """Compute average engagement metrics grouped by content type."""
    type_groups = {}
    for p in posts:
        ct = p['content_type']
        if ct not in type_groups:
            type_groups[ct] = []
        type_groups[ct].append(p)

    result = {}
    for ct, group in type_groups.items():
        avg_likes = sum(p['likes'] for p in group) / len(group)
        avg_comments = sum(p['comments'] for p in group) / len(group)
        avg_score = sum(p['engagement_score'] for p in group) / len(group)
        result[ct] = {
            'count': len(group),
            'avg_likes': round(avg_likes, 1),
            'avg_comments': round(avg_comments, 1),
            'avg_engagement_score': round(avg_score, 1),
        }

    return result


# --- Report Generation ---

def generate_report(username: str, posts: List[Dict]) -> str:
    """Generate the Instagram Page Spy markdown report."""

    sorted_by_engagement = sorted(posts, key=lambda x: x['engagement_score'], reverse=True)

    # Metrics
    freq = compute_posting_frequency(posts)
    schedule = compute_posting_schedule(posts)
    content_types = compute_distribution([p['content_type'] for p in posts])
    engagement_by_type = compute_engagement_by_type(posts)
    hook_dist = compute_distribution([p['hook_type'] for p in posts])
    cta_dist = compute_distribution([p['cta_style'] for p in posts])

    # Averages
    total = len(posts) or 1
    avg_likes = sum(p['likes'] for p in posts) / total
    avg_comments = sum(p['comments'] for p in posts) / total
    avg_engagement = sum(p['engagement_score'] for p in posts) / total

    # Hashtag analysis
    all_hashtags = []
    for p in posts:
        all_hashtags.extend(p.get('hashtags', []))
    top_hashtags = Counter(all_hashtags).most_common(15)

    # Caption length analysis
    avg_caption_length = sum(p['caption_length'] for p in posts) / total

    # Hook engagement averages
    hook_engagement = Counter()
    hook_count = Counter()
    for p in posts:
        hook_engagement[p['hook_type']] += p['engagement_score']
        hook_count[p['hook_type']] += 1

    # --- Build Report ---

    report = f"""# @{username} - Instagram Page Spy Report

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Profile:** https://instagram.com/{username}
**Posts Analyzed:** {len(posts)}
**Average Engagement:** {avg_likes:.0f} likes | {avg_comments:.0f} comments per post

---

## 1. Posting Frequency

- **Posts per week:** {freq['per_week']}
- **Posts per month:** {freq['per_month']}
- **Trend:** {freq['trend']}
- **Period analyzed:** {freq['total_days']} days

---

## 2. Content Type Breakdown

"""

    for ct, data in content_types.items():
        eng = engagement_by_type.get(ct, {})
        report += f"- **{ct}:** {data['percentage']}% ({data['count']} posts) | Avg engagement: {eng.get('avg_engagement_score', 0):.0f}\n"

    best_type = max(engagement_by_type.items(), key=lambda x: x[1]['avg_engagement_score'])[0] if engagement_by_type else 'N/A'
    report += f"\n**Best performing type:** {best_type}\n"

    report += """
---

## 3. Top 10 Posts by Engagement

"""

    for i, post in enumerate(sorted_by_engagement[:10], 1):
        truncated = post['caption'][:500] + ('...' if len(post['caption']) > 500 else '') if post['caption'] else '(no caption)'
        views_str = f"\n- Video Views: {post['video_views']:,}" if post['video_views'] > 0 else ''
        report += f"""### Post #{i} | {post['content_type']} | {post['hook_type']} | Score: {post['engagement_score']:,}

**Opening Line:**
{post['opening_line']}

**Full Caption:**
{truncated}

**Metrics:**
- Likes: {post['likes']:,}
- Comments: {post['comments']:,}{views_str}
- Caption Length: {post['caption_length']} chars

**URL:** {post['url']}

---

"""

    report += """## 4. Hook Pattern Analysis

"""

    best_hook = None
    best_eng = 0
    for h in hook_engagement:
        avg = hook_engagement[h] / hook_count[h]
        if avg > best_eng:
            best_eng = avg
            best_hook = h

    for hook, data in hook_dist.items():
        avg_eng = hook_engagement[hook] / hook_count[hook] if hook_count[hook] else 0
        report += f"- **{hook}:** {data['percentage']}% ({data['count']} posts) | Avg engagement: {avg_eng:,.0f}\n"

    report += f"\n**Highest engagement hook:** {best_hook} (avg {best_eng:,.0f})\n"

    report += """
---

## 5. CTA Pattern Analysis

"""

    for cta, data in cta_dist.items():
        report += f"- **{cta}:** {data['percentage']}% ({data['count']} posts)\n"

    report += """
---

## 6. Posting Schedule

### Day of Week
"""

    for day, count in schedule['by_day'].items():
        bar = '#' * count
        report += f"- **{day}:** {count} posts {bar}\n"

    if schedule['by_hour']:
        report += "\n### Time of Day (hour, UTC)\n"
        for hour, count in schedule['by_hour'].items():
            report += f"- **{hour:02d}:00:** {count} posts\n"

    report += f"""
---

## 7. Caption Analysis

- **Average caption length:** {avg_caption_length:.0f} characters
"""

    # Caption length vs engagement correlation
    short_posts = [p for p in posts if p['caption_length'] < 300]
    medium_posts = [p for p in posts if 300 <= p['caption_length'] < 800]
    long_posts = [p for p in posts if p['caption_length'] >= 800]

    if short_posts:
        avg_short = sum(p['engagement_score'] for p in short_posts) / len(short_posts)
        report += f"- **Short (<300 chars):** {len(short_posts)} posts | Avg engagement: {avg_short:,.0f}\n"
    if medium_posts:
        avg_med = sum(p['engagement_score'] for p in medium_posts) / len(medium_posts)
        report += f"- **Medium (300-800 chars):** {len(medium_posts)} posts | Avg engagement: {avg_med:,.0f}\n"
    if long_posts:
        avg_long = sum(p['engagement_score'] for p in long_posts) / len(long_posts)
        report += f"- **Long (800+ chars):** {len(long_posts)} posts | Avg engagement: {avg_long:,.0f}\n"

    report += """
---

## 8. Hashtag Analysis

"""

    if top_hashtags:
        report += f"**Total unique hashtags:** {len(set(all_hashtags))}\n\n"
        report += "### Most Used Hashtags\n"
        for tag, count in top_hashtags:
            report += f"- **#{tag}** ({count} times)\n"
    else:
        report += "No hashtags detected.\n"

    report += """
---

## 9. Key Takeaways

"""

    takeaways = []

    if freq['per_week'] > 0:
        takeaways.append(f"Posts ~{freq['per_week']} times per week ({freq['trend']} trend)")

    if content_types:
        top_type = list(content_types.keys())[0]
        takeaways.append(f"Primary content format: {top_type} ({content_types[top_type]['percentage']}%)")

    if best_type and engagement_by_type:
        takeaways.append(f"Best performing format: {best_type} (avg {engagement_by_type[best_type]['avg_engagement_score']:,.0f} engagement)")

    if hook_dist:
        top_hook = list(hook_dist.keys())[0]
        takeaways.append(f"Most used hook: {top_hook} ({hook_dist[top_hook]['percentage']}%)")

    if best_hook:
        takeaways.append(f"Highest engagement hook: {best_hook} (avg {best_eng:,.0f})")

    if cta_dist:
        top_cta = list(cta_dist.keys())[0]
        takeaways.append(f"Dominant CTA style: {top_cta} ({cta_dist[top_cta]['percentage']}%)")

    if schedule['by_day']:
        best_day = max(schedule['by_day'], key=schedule['by_day'].get)
        takeaways.append(f"Most active day: {best_day} ({schedule['by_day'][best_day]} posts)")

    takeaways.append(f"Average caption length: {avg_caption_length:.0f} chars")

    if top_hashtags:
        top_3_tags = ', '.join(f'#{t[0]}' for t in top_hashtags[:3])
        takeaways.append(f"Top hashtags: {top_3_tags}")

    for t in takeaways:
        report += f"- {t}\n"

    report += f"""
---

*Report generated by Instagram Page Spy | The Coach Consultant*
"""

    return report


# --- Main ---

def main():
    if len(sys.argv) < 2:
        print("Usage: python ig_spy.py <instagram_username>")
        print("  python ig_spy.py danmartell")
        print('  python ig_spy.py "benhawksworth_"')
        sys.exit(1)

    username = sys.argv[1].strip().strip('@').strip('"').strip("'")

    # Remove URL if full URL provided
    if 'instagram.com' in username:
        match = re.search(r'instagram\.com/([^/?]+)', username)
        username = match.group(1) if match else username

    print(f"\n{'='*60}")
    print(f"  Instagram Page Spy")
    print(f"  Target: @{username}")
    print(f"{'='*60}\n")

    # Load API token
    env = load_env()
    apify_token = env.get('APIFY_API_TOKEN')

    if not apify_token:
        print("Error: APIFY_API_TOKEN not found in .env file")
        print("\nSetup:")
        print("1. Get your token from https://console.apify.com/account/integrations")
        print("2. Add to .env: APIFY_API_TOKEN=your_token_here")
        sys.exit(1)

    client = ApifyClient(apify_token)

    # Scrape profile
    raw_posts = scrape_instagram_profile(client, username)

    if not raw_posts:
        print("No posts found. Check the username and try again.")
        sys.exit(1)

    # Analyze
    posts = [analyze_post(p) for p in raw_posts]

    # Generate report
    print(f"\nGenerating report...")

    report = generate_report(username, posts)

    # Save report
    output_dir = Path(__file__).parent / 'outputs'
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(r'[^a-z0-9]+', '-', username.lower()).strip('-')
    filename = f"{safe_name}-{datetime.now().strftime('%Y-%m-%d')}.md"
    report_path = output_dir / filename

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n{'='*60}")
    print(f"  Report saved: {report_path}")
    print(f"  Posts analyzed: {len(posts)}")
    print(f"{'='*60}\n")

    # Print summary
    freq = compute_posting_frequency(posts)
    print("Key findings:")
    print(f"  Posts/week: {freq['per_week']} ({freq['trend']})")
    print(f"  Top hook: {Counter(p['hook_type'] for p in posts).most_common(1)[0][0]}")
    print(f"  Top CTA: {Counter(p['cta_style'] for p in posts).most_common(1)[0][0]}")
    print(f"  Avg engagement: {sum(p['engagement_score'] for p in posts) / len(posts):,.0f}")

    return str(report_path)


if __name__ == "__main__":
    main()
