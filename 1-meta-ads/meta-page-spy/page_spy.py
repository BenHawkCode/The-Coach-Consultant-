#!/usr/bin/env python3
"""
Meta Page Spy - Facebook Page Intelligence Tool
The Coach Consultant - AI Content Generation System

Scrapes a Facebook page's organic posts AND paid ads from Ad Library,
then generates a combined intelligence report with:
- Posting frequency
- Content type breakdown
- Engagement metrics (top 10)
- Hook pattern analysis
- CTA pattern analysis
- Posting schedule
- Paid ads hook/CTA patterns
- Offer positioning

Uses two Apify actors:
- apify/facebook-posts-scraper (organic posts)
- curious_coder/facebook-ads-library-scraper (paid ads)

Usage:
    python page_spy.py <facebook_page_url_or_name>
    python page_spy.py https://www.facebook.com/DanMartell
    python page_spy.py "Dan Martell"
"""

import sys
import json
import time
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import Counter
from apify_client import ApifyClient


# --- Configuration ---

DEFAULT_ORGANIC_POSTS = 50
DEFAULT_PAID_ADS = 20
PAUSE_BETWEEN_SCRAPERS = 5  # seconds


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

def scrape_organic_posts(client: ApifyClient, page_url: str, max_posts: int = DEFAULT_ORGANIC_POSTS) -> List[Dict]:
    """
    Scrape organic posts from a Facebook page using apify/facebook-posts-scraper.

    Args:
        client: Authenticated ApifyClient
        page_url: Facebook page URL (e.g. https://www.facebook.com/DanMartell)
        max_posts: Maximum number of posts to scrape

    Returns:
        List of post objects from Apify
    """
    run_input = {
        "startUrls": [{"url": page_url}],
        "resultsLimit": max_posts,
        "scrapePostComments": False,
        "scrapePostReactions": True,
        "scrapeReelsData": True,
    }

    print(f"Phase 1: Scraping organic posts from {page_url}...")

    try:
        run = client.actor("apify/facebook-posts-scraper").call(run_input=run_input)
        posts = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        print(f"  Found {len(posts)} organic posts")
        return posts
    except Exception as e:
        print(f"  Error scraping organic posts: {e}")
        return []


def scrape_paid_ads(client: ApifyClient, search_term: str, max_ads: int = DEFAULT_PAID_ADS) -> List[Dict]:
    """
    Scrape paid ads from Facebook Ad Library using curious_coder/facebook-ads-library-scraper.

    Args:
        client: Authenticated ApifyClient
        search_term: Page name to search in Ad Library
        max_ads: Maximum number of ads to scrape

    Returns:
        List of ad objects from Apify
    """
    ad_library_url = (
        f"https://www.facebook.com/ads/library/"
        f"?active_status=all&ad_type=all&country=ALL"
        f"&q={search_term.replace(' ', '%20')}"
        f"&search_type=keyword_unordered&media_type=all"
    )

    run_input = {
        "urls": [{"url": ad_library_url}],
        "count": max(10, max_ads),
        "scrapePageAds.period": "",
        "scrapePageAds.activeStatus": "all",
        "scrapePageAds.sortBy": "impressions_desc",
        "scrapePageAds.countryCode": "ALL",
    }

    print(f"Phase 2: Scraping paid ads for '{search_term}'...")

    try:
        run = client.actor("curious_coder/facebook-ads-library-scraper").call(run_input=run_input)
        ads = [
            item for item in client.dataset(run["defaultDatasetId"]).iterate_items()
            if 'error' not in item
        ]
        print(f"  Found {len(ads)} paid ads")
        return ads
    except Exception as e:
        print(f"  Error scraping paid ads: {e}")
        return []


# --- Classification ---

def classify_hook_type(text: str) -> str:
    """Classify the hook type based on the first 125 characters of text."""
    if not text:
        return "Unknown"

    opening = text[:125].lower()

    if '?' in opening:
        return "Question"
    elif any(w in opening for w in ['struggling', 'problem', 'challenge', 'frustrated', 'stuck', 'tired of', 'stop']):
        return "Pain Point"
    elif any(c.isdigit() for c in opening) and any(w in opening for w in ['£', '$', '%', 'x', 'grew', 'added', 'made', 'increase', 'revenue', 'million']):
        return "Metric/Result"
    elif any(w in opening for w in ['secret', 'hidden', 'nobody', 'most people', 'everyone', 'truth', 'lie']):
        return "Bold Statement"
    elif any(w in opening for w in ['when i', 'i was', 'my first', 'back in', 'i remember', 'story']):
        return "Story"
    elif any(w in opening for w in ['how to', "here's how", '3 ways', '5 steps', 'framework']):
        return "How-To/Framework"
    else:
        return "Statement"


def classify_cta(text: str) -> str:
    """Classify the CTA style from text content."""
    if not text:
        return "No CTA"

    lower = text.lower()

    if any(p in lower for p in ['book a call', 'schedule a call', 'apply now', 'download', 'register', 'sign up', 'get started', 'click the link', 'link in bio', 'link in comments', 'dm me']):
        return "Hard CTA"
    elif any(p in lower for p in ['learn more', 'discover', 'find out', 'see how', 'what do you think', 'let me know', 'thoughts?']):
        return "Soft CTA"
    elif any(p in lower for p in ['comment', 'tag', 'share', 'save this', 'drop a']):
        return "Engagement CTA"
    else:
        return "No CTA"


# --- Analysis ---

def analyze_organic_post(post: Dict) -> Dict:
    """Extract and analyze key data from a single organic post."""
    text = post.get('text', '')
    reactions = post.get('reactions', 0) or 0
    comments = post.get('comments', 0) or 0
    shares = post.get('shares', 0) or 0

    return {
        'text': text,
        'opening_line': text[:125] if text else '',
        'hook_type': classify_hook_type(text),
        'cta_style': classify_cta(text),
        'reactions': reactions,
        'comments': comments,
        'shares': shares,
        'engagement_score': reactions + (comments * 2) + (shares * 3),
        'url': post.get('url', ''),
        'timestamp': post.get('time', ''),
        'media_type': post.get('type', 'text'),
    }


def analyze_paid_ad(ad: Dict) -> Dict:
    """Extract and analyze key data from a single paid ad."""
    snapshot = ad.get('snapshot', {}) or {}
    body = snapshot.get('body')
    text = body.get('text', '') if body and isinstance(body, dict) else ''

    return {
        'text': text,
        'opening_line': text[:125] if text else '',
        'hook_type': classify_hook_type(text),
        'cta_style': classify_cta(text),
        'page_name': ad.get('page_name', 'Unknown'),
        'cta_text': snapshot.get('cta_text', ''),
        'link_caption': snapshot.get('caption', ''),
        'platforms': ad.get('publisher_platform', []),
        'start_date': ad.get('start_date_formatted', ''),
    }


def compute_posting_frequency(posts: List[Dict]) -> Dict:
    """Calculate posting frequency from post timestamps."""
    dates = []
    for p in posts:
        ts = p.get('timestamp', '')
        if not ts:
            continue
        try:
            if isinstance(ts, str):
                # Try common formats
                for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                    try:
                        dates.append(datetime.strptime(ts[:19], fmt))
                        break
                    except ValueError:
                        continue
        except Exception:
            continue

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
    """Calculate posting schedule (day-of-week distribution)."""
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = Counter()
    hour_counts = Counter()

    for p in posts:
        ts = p.get('timestamp', '')
        if not ts:
            continue
        try:
            if isinstance(ts, str):
                for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                    try:
                        dt = datetime.strptime(ts[:19], fmt)
                        day_counts[day_names[dt.weekday()]] += 1
                        if len(ts) > 10:  # has time component
                            hour_counts[dt.hour] += 1
                        break
                    except ValueError:
                        continue
        except Exception:
            continue

    return {
        'by_day': {day: day_counts.get(day, 0) for day in day_names},
        'by_hour': dict(sorted(hour_counts.items())) if hour_counts else {},
    }


def compute_content_types(posts: List[Dict]) -> Dict:
    """Calculate content type breakdown."""
    types = Counter(p.get('media_type', 'unknown') for p in posts)
    total = len(posts) or 1
    return {
        t: {'count': c, 'percentage': round(c / total * 100, 1)}
        for t, c in types.most_common()
    }


def compute_distribution(items: List[str]) -> Dict[str, Dict]:
    """Compute percentage distribution from a list of categories."""
    counts = Counter(items)
    total = len(items) or 1
    return {
        k: {'count': v, 'percentage': round(v / total * 100, 1)}
        for k, v in counts.most_common()
    }


def extract_offer_positioning(ads: List[Dict]) -> List[str]:
    """Extract offer mentions from paid ads."""
    offers = []
    offer_keywords = ['free', 'download', 'guide', 'masterclass', 'training', 'webinar', 'call', 'consultation', 'challenge', 'workshop', 'course', 'audit', 'template']

    for ad in ads:
        text_lower = ad.get('text', '').lower()
        if any(kw in text_lower for kw in offer_keywords):
            cta = ad.get('cta_text') or ad.get('link_caption') or ''
            if cta:
                offers.append(cta)

    return list(set(offers))[:10]


# --- Report Generation ---

def generate_report(
    page_name: str,
    page_url: str,
    organic_posts: List[Dict],
    paid_ads: List[Dict],
) -> str:
    """Generate the combined Meta Page Spy markdown report."""

    # Sort organic by engagement
    sorted_organic = sorted(organic_posts, key=lambda x: x['engagement_score'], reverse=True)

    # Posting frequency
    freq = compute_posting_frequency(organic_posts)

    # Content types
    content_types = compute_content_types(organic_posts)

    # Hook/CTA distributions (organic)
    organic_hooks = compute_distribution([p['hook_type'] for p in organic_posts])
    organic_ctas = compute_distribution([p['cta_style'] for p in organic_posts])

    # Posting schedule
    schedule = compute_posting_schedule(organic_posts)

    # Paid ads analysis
    paid_hooks = compute_distribution([a['hook_type'] for a in paid_ads]) if paid_ads else {}
    paid_ctas = compute_distribution([a['cta_style'] for a in paid_ads]) if paid_ads else {}
    offers = extract_offer_positioning(paid_ads)

    # --- Build Report ---

    report = f"""# {page_name} - Meta Page Spy Report

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Page URL:** {page_url}
**Posts Analyzed:** {len(organic_posts)} organic | {len(paid_ads)} paid ads

---

## 1. Posting Frequency

- **Posts per week:** {freq['per_week']}
- **Posts per month:** {freq['per_month']}
- **Trend:** {freq['trend']}
- **Period analyzed:** {freq['total_days']} days

---

## 2. Content Type Breakdown

"""

    for ctype, data in content_types.items():
        report += f"- **{ctype.title()}:** {data['percentage']}% ({data['count']} posts)\n"

    report += """
---

## 3. Top 10 Posts by Engagement

"""

    for i, post in enumerate(sorted_organic[:10], 1):
        truncated = post['text'][:500] + ('...' if len(post['text']) > 500 else '') if post['text'] else '(no text)'
        report += f"""### Post #{i} | {post['hook_type']} | Score: {post['engagement_score']}

**Opening Line:**
{post['opening_line']}

**Full Post:**
{truncated}

**Metrics:**
- Reactions: {post['reactions']}
- Comments: {post['comments']}
- Shares: {post['shares']}
- Content Type: {post['media_type']}
- CTA Style: {post['cta_style']}

**URL:** {post['url']}

---

"""

    report += """## 4. Hook Pattern Analysis (Organic)

"""

    if organic_hooks:
        best_hook = None
        best_eng = 0
        hook_engagement = Counter()
        hook_count = Counter()
        for p in organic_posts:
            hook_engagement[p['hook_type']] += p['engagement_score']
            hook_count[p['hook_type']] += 1
        for h in hook_engagement:
            avg = hook_engagement[h] / hook_count[h]
            if avg > best_eng:
                best_eng = avg
                best_hook = h

        for hook, data in organic_hooks.items():
            avg_eng = hook_engagement[hook] / hook_count[hook] if hook_count[hook] else 0
            report += f"- **{hook}:** {data['percentage']}% ({data['count']} posts) | Avg engagement: {avg_eng:.0f}\n"

        report += f"\n**Highest engagement hook type:** {best_hook} (avg {best_eng:.0f})\n"
    else:
        report += "No organic posts to analyze.\n"

    report += """
---

## 5. CTA Pattern Analysis (Organic)

"""

    for cta, data in organic_ctas.items():
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
        report += "\n### Time of Day (hour)\n"
        for hour, count in schedule['by_hour'].items():
            report += f"- **{hour:02d}:00:** {count} posts\n"

    report += """
---

## 7. Paid Ads - Hook & CTA Patterns

"""

    if paid_hooks:
        report += "### Hook Types\n"
        for hook, data in paid_hooks.items():
            report += f"- **{hook}:** {data['percentage']}% ({data['count']} ads)\n"

        report += "\n### CTA Styles\n"
        for cta, data in paid_ctas.items():
            report += f"- **{cta}:** {data['percentage']}% ({data['count']} ads)\n"

        report += "\n### Top Ad Hooks\n"
        for ad in paid_ads[:5]:
            if ad['opening_line']:
                report += f"- \"{ad['opening_line']}\" ({ad['hook_type']})\n"
    else:
        report += "No paid ads found in Ad Library.\n"

    report += """
---

## 8. Paid Ads - Offer Positioning

"""

    if paid_ads:
        # CTA buttons
        cta_texts = [a['cta_text'] for a in paid_ads if a.get('cta_text')]
        if cta_texts:
            report += "### CTA Buttons\n"
            for cta, count in Counter(cta_texts).most_common(5):
                report += f"- **{cta}** ({count} ads)\n"

        # Link captions
        captions = [a['link_caption'] for a in paid_ads if a.get('link_caption')]
        if captions:
            report += "\n### Link Captions\n"
            for cap, count in Counter(captions).most_common(5):
                report += f"- {cap} ({count} ads)\n"

        # Offers
        if offers:
            report += "\n### Detected Offers\n"
            for offer in offers:
                report += f"- {offer}\n"

        if not cta_texts and not captions and not offers:
            report += "No clear offer positioning detected.\n"
    else:
        report += "No paid ads found in Ad Library.\n"

    report += """
---

## 9. Key Takeaways

"""

    # Generate actionable takeaways
    takeaways = []

    if freq['per_week'] > 0:
        takeaways.append(f"Posts ~{freq['per_week']} times per week ({freq['trend']} trend)")

    if content_types:
        top_type = list(content_types.keys())[0]
        takeaways.append(f"Primary content format: {top_type.title()} ({content_types[top_type]['percentage']}%)")

    if organic_hooks:
        top_hook = list(organic_hooks.keys())[0]
        takeaways.append(f"Most used hook type: {top_hook} ({organic_hooks[top_hook]['percentage']}%)")

    if organic_ctas:
        top_cta = list(organic_ctas.keys())[0]
        takeaways.append(f"Dominant CTA style: {top_cta} ({organic_ctas[top_cta]['percentage']}%)")

    if schedule['by_day']:
        best_day = max(schedule['by_day'], key=schedule['by_day'].get)
        takeaways.append(f"Most active day: {best_day} ({schedule['by_day'][best_day]} posts)")

    if paid_hooks:
        top_paid_hook = list(paid_hooks.keys())[0]
        takeaways.append(f"Paid ads favour {top_paid_hook} hooks ({paid_hooks[top_paid_hook]['percentage']}%)")

    if offers:
        takeaways.append(f"Key offers: {', '.join(offers[:3])}")

    for t in takeaways:
        report += f"- {t}\n"

    report += f"""
---

*Report generated by Meta Page Spy | The Coach Consultant*
"""

    return report


# --- URL Helpers ---

def normalize_page_url(input_str: str) -> Tuple[str, str]:
    """
    Normalize user input into a Facebook page URL and a search-friendly name.

    Returns:
        (page_url, search_name)
    """
    input_str = input_str.strip().strip('"').strip("'")

    # Already a Facebook URL
    if 'facebook.com' in input_str:
        page_url = input_str
        # Extract page name from URL
        match = re.search(r'facebook\.com/([^/?]+)', input_str)
        search_name = match.group(1).replace('-', ' ') if match else input_str
        return page_url, search_name

    # Just a name - build URL
    slug = input_str.replace(' ', '')
    page_url = f"https://www.facebook.com/{slug}"
    search_name = input_str

    return page_url, search_name


# --- Main ---

def main():
    if len(sys.argv) < 2:
        print("Usage: python page_spy.py <facebook_page_url_or_name>")
        print("  python page_spy.py https://www.facebook.com/DanMartell")
        print('  python page_spy.py "Dan Martell"')
        sys.exit(1)

    user_input = ' '.join(sys.argv[1:])
    page_url, search_name = normalize_page_url(user_input)

    print(f"\n{'='*60}")
    print(f"  Meta Page Spy")
    print(f"  Target: {search_name}")
    print(f"  URL: {page_url}")
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

    # Phase 1: Organic posts
    raw_posts = scrape_organic_posts(client, page_url)
    organic_posts = [analyze_organic_post(p) for p in raw_posts]

    # Pause between scrapers
    if raw_posts:
        print(f"\n  Pausing {PAUSE_BETWEEN_SCRAPERS}s before Ad Library scrape...")
        time.sleep(PAUSE_BETWEEN_SCRAPERS)

    # Phase 2: Paid ads
    raw_ads = scrape_paid_ads(client, search_name)
    paid_ads = [analyze_paid_ad(a) for a in raw_ads]

    # Phase 3: Generate report
    print(f"\nPhase 3: Generating report...")

    report = generate_report(
        page_name=search_name,
        page_url=page_url,
        organic_posts=organic_posts,
        paid_ads=paid_ads,
    )

    # Save report
    output_dir = Path(__file__).parent / 'outputs'
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = re.sub(r'[^a-z0-9]+', '-', search_name.lower()).strip('-')
    filename = f"{safe_name}-{datetime.now().strftime('%Y-%m-%d')}.md"
    report_path = output_dir / filename

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n{'='*60}")
    print(f"  Report saved: {report_path}")
    print(f"  Organic posts: {len(organic_posts)}")
    print(f"  Paid ads: {len(paid_ads)}")
    print(f"{'='*60}\n")

    # Print summary to stdout
    print("Key findings:")
    freq = compute_posting_frequency(organic_posts)
    print(f"  Posts/week: {freq['per_week']} ({freq['trend']})")
    print(f"  Top hook: {Counter(p['hook_type'] for p in organic_posts).most_common(1)[0][0] if organic_posts else 'N/A'}")
    print(f"  Top CTA: {Counter(p['cta_style'] for p in organic_posts).most_common(1)[0][0] if organic_posts else 'N/A'}")

    return str(report_path)


if __name__ == "__main__":
    main()
