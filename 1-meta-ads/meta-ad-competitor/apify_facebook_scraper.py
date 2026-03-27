#!/usr/bin/env python3
"""
Apify Facebook Posts Scraper - Competitor Analysis
The Coach Consultant - AI Content Generation System

Uses Apify's facebook-posts-scraper to analyze competitor Facebook profiles
and extract hook patterns, engagement data, and content strategies.

Test version: Analyzes 2-3 competitors only.
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from apify_client import ApifyClient

# Configuration
COMPETITORS_TEST = [
    {
        'name': 'Dan Martell',
        'facebook_url': 'https://www.facebook.com/DanMartell',
        'tier': 1,
        'why_study': 'SaaS and coaching ads. Brilliant at framework hooks and authority positioning'
    }
]

def load_env():
    """Load environment variables from .env file"""
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

def scrape_facebook_profile(apify_token: str, facebook_url: str, max_posts: int = 20) -> List[Dict]:
    """
    Scrape Facebook profile using Apify's facebook-posts-scraper

    Args:
        apify_token: Apify API token
        facebook_url: Facebook profile/page URL
        max_posts: Maximum number of posts to scrape

    Returns:
        List of post objects
    """
    client = ApifyClient(apify_token)

    # Prepare Actor input
    run_input = {
        "startUrls": [{"url": facebook_url}],
        "resultsLimit": max_posts,  # Use resultsLimit instead of deprecated maxPosts
        "scrapePostComments": False,  # We don't need comments for now
        "scrapePostReactions": True,   # Get engagement metrics
        "scrapeReelsData": True,       # Include reels
    }

    print(f"🔄 Starting scrape for {facebook_url}...")

    try:
        # Run the Actor and wait for it to finish
        run = client.actor("apify/facebook-posts-scraper").call(run_input=run_input)

        # Fetch results from the run's dataset
        posts = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            posts.append(item)

        print(f"✅ Scraped {len(posts)} posts")
        return posts

    except Exception as e:
        print(f"❌ Error scraping {facebook_url}: {e}")
        return []

def classify_hook_type(post_text: str) -> str:
    """
    Classify the hook type based on post opening

    Args:
        post_text: Post text content

    Returns:
        Hook type classification
    """
    if not post_text:
        return "Unknown"

    opening = post_text[:125].lower()

    # Check for patterns
    if '?' in opening:
        return "Question"
    elif any(word in opening for word in ['struggling', 'problem', 'challenge', 'frustrated', 'stuck', 'tired of', 'stop']):
        return "Pain Point"
    elif any(char.isdigit() for char in opening) and any(word in opening for word in ['£', '$', '%', 'x', 'grew', 'added', 'made', 'increase', 'revenue']):
        return "Metric/Result"
    elif any(word in opening for word in ['secret', 'hidden', 'nobody', 'most people', 'everyone', 'truth', 'lie']):
        return "Bold Statement"
    elif any(word in opening for word in ['when i', 'i was', 'my first', 'back in', 'i remember', 'story']):
        return "Story"
    elif any(word in opening for word in ['how to', 'here\'s how', '3 ways', '5 steps', 'framework']):
        return "How-To/Framework"
    else:
        return "Statement"

def extract_cta_style(post_text: str) -> str:
    """
    Extract CTA style from post

    Args:
        post_text: Post text content

    Returns:
        CTA style classification
    """
    if not post_text:
        return "None"

    lower_text = post_text.lower()

    # Check for common CTAs
    if any(phrase in lower_text for phrase in ['click the link', 'link in bio', 'link in comments', 'dm me']):
        return "Hard CTA"
    elif any(phrase in lower_text for phrase in ['comment', 'tag', 'share', 'save this', 'drop a']):
        return "Engagement CTA"
    elif any(phrase in lower_text for phrase in ['what do you think', 'let me know', 'thoughts?']):
        return "Soft CTA"
    else:
        return "No CTA"

def analyze_post(post: Dict) -> Dict:
    """
    Analyze a single Facebook post and extract key elements

    Args:
        post: Post object from Apify scraper

    Returns:
        Dictionary with analyzed elements
    """
    text = post.get('text', '')

    # Extract engagement metrics
    reactions = post.get('reactions', 0)
    comments = post.get('comments', 0)
    shares = post.get('shares', 0)

    # Calculate engagement score (simple metric)
    engagement_score = reactions + (comments * 2) + (shares * 3)

    return {
        'post_text': text,
        'opening_line': text[:125] if text else '',
        'hook_type': classify_hook_type(text),
        'cta_style': extract_cta_style(text),
        'reactions': reactions,
        'comments': comments,
        'shares': shares,
        'engagement_score': engagement_score,
        'post_url': post.get('url', ''),
        'post_date': post.get('time', ''),
        'media_type': post.get('type', 'text')
    }

def generate_competitor_report(competitor: Dict, analyzed_posts: List[Dict]) -> str:
    """
    Generate markdown report for a single competitor

    Args:
        competitor: Competitor metadata
        analyzed_posts: List of analyzed post objects

    Returns:
        Formatted markdown report
    """
    # Sort posts by engagement score
    sorted_posts = sorted(analyzed_posts, key=lambda x: x['engagement_score'], reverse=True)

    # Hook type distribution
    hook_types = [p['hook_type'] for p in analyzed_posts]
    hook_distribution = {hook: hook_types.count(hook) for hook in set(hook_types)}
    total_posts = len(analyzed_posts)

    report = f"""# {competitor['name']} - Facebook Content Analysis

**Analyzed:** {datetime.now().strftime('%Y-%m-%d')}
**Tier:** {competitor['tier']}
**Why Study:** {competitor['why_study']}
**Total Posts Analyzed:** {total_posts}

---

## Top 5 High-Engagement Posts

"""

    for i, post in enumerate(sorted_posts[:5], 1):
        report += f"""### Post #{i} - {post['hook_type']} | {post['engagement_score']} engagement

**Opening Line:**
{post['opening_line']}

**Full Post:**
{post['post_text'][:500]}{"..." if len(post['post_text']) > 500 else ""}

**Metrics:**
- Reactions: {post['reactions']}
- Comments: {post['comments']}
- Shares: {post['shares']}
- CTA Style: {post['cta_style']}
- Media Type: {post['media_type']}

**URL:** {post['post_url']}

---

"""

    report += f"""## Hook Pattern Analysis

### Hook Type Distribution
"""

    for hook, count in sorted(hook_distribution.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_posts * 100) if total_posts > 0 else 0
        report += f"- **{hook}:** {percentage:.1f}% ({count} posts)\n"

    # CTA analysis
    cta_styles = [p['cta_style'] for p in analyzed_posts]
    cta_distribution = {cta: cta_styles.count(cta) for cta in set(cta_styles)}

    report += f"""
### CTA Style Distribution
"""

    for cta, count in sorted(cta_distribution.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_posts * 100) if total_posts > 0 else 0
        report += f"- **{cta}:** {percentage:.1f}% ({count} posts)\n"

    # Average engagement
    avg_engagement = sum(p['engagement_score'] for p in analyzed_posts) / total_posts if total_posts > 0 else 0

    report += f"""
### Key Insights
- Average engagement score: {avg_engagement:.0f}
- Most common hook: {max(hook_distribution, key=hook_distribution.get)}
- Most common CTA style: {max(cta_distribution, key=cta_distribution.get)}
- Highest performing hook: {sorted_posts[0]['hook_type'] if sorted_posts else 'N/A'}

---

*Report generated by The Coach Consultant Meta Ad Competitor Analysis*
"""

    return report

def main():
    """Main script execution"""

    # Load environment variables
    env = load_env()
    apify_token = env.get('APIFY_API_TOKEN')

    if not apify_token:
        print("❌ Error: APIFY_API_TOKEN not found in .env file")
        print("\nTo set up:")
        print("1. Get your Apify API token from https://console.apify.com/account/integrations")
        print("2. Add to .env file: APIFY_API_TOKEN=your_token_here")
        sys.exit(1)

    print(f"\n🚀 Starting Facebook competitor analysis (Test Mode)")
    print(f"📊 Analyzing {len(COMPETITORS_TEST)} competitors\n")

    output_dir = Path(__file__).parent / 'outputs' / 'facebook-analysis'
    output_dir.mkdir(parents=True, exist_ok=True)

    all_results = []

    for competitor in COMPETITORS_TEST:
        print(f"\n{'='*60}")
        print(f"Analyzing: {competitor['name']}")
        print(f"{'='*60}\n")

        # Scrape posts
        posts = scrape_facebook_profile(
            apify_token=apify_token,
            facebook_url=competitor['facebook_url'],
            max_posts=20  # Test with 20 posts per competitor
        )

        if not posts:
            print(f"⚠️  No posts found for {competitor['name']}, skipping...\n")
            continue

        # Analyze posts
        analyzed_posts = [analyze_post(post) for post in posts]

        # Generate report
        report = generate_competitor_report(competitor, analyzed_posts)

        # Save individual report
        filename = f"{competitor['name'].lower().replace(' ', '-')}-{datetime.now().strftime('%Y-%m-%d')}.md"
        report_path = output_dir / filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✅ Report saved: {report_path}")

        # Store results
        all_results.append({
            'competitor': competitor['name'],
            'posts_analyzed': len(analyzed_posts),
            'report_path': str(report_path)
        })

        # Rate limiting (be nice to Apify)
        if competitor != COMPETITORS_TEST[-1]:
            print(f"\n⏳ Waiting 10 seconds before next competitor...")
            time.sleep(10)

    # Generate summary
    print(f"\n{'='*60}")
    print(f"✅ Analysis Complete!")
    print(f"{'='*60}\n")

    print("📊 Summary:")
    for result in all_results:
        print(f"  - {result['competitor']}: {result['posts_analyzed']} posts analyzed")

    print(f"\n📁 All reports saved to: {output_dir}")
    print(f"\n💡 Next Steps:")
    print(f"  1. Review individual competitor reports")
    print(f"  2. Identify winning hook patterns")
    print(f"  3. Use meta-ad-copy skill to generate new ads based on insights")

if __name__ == "__main__":
    main()
