#!/usr/bin/env python3
"""
Apify Facebook Ad Library Scraper - Competitor Analysis
The Coach Consultant - AI Content Generation System

Uses Apify's curious_coder/facebook-ads-library-scraper to analyze competitor ads
from Facebook Ad Library and extract hook patterns, offers, and CTA styles.

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

# Configuration - FULL LIST (31 competitors from competitor-list.md)
COMPETITORS_FULL = [
    # Tier 1: Business Education & Coaching (10)
    {'name': 'Alex Hormozi', 'search_term': 'Alex Hormozi', 'tier': 1, 'why_study': 'Master of direct response hooks, metric-led copy, and pattern interrupts'},
    {'name': 'Dan Martell', 'search_term': 'Dan Martell', 'tier': 1, 'why_study': 'SaaS and coaching ads. Brilliant at framework hooks and authority positioning'},
    {'name': 'Russell Brunson', 'search_term': 'Russell Brunson', 'tier': 1, 'why_study': 'ClickFunnels. One of the best funnel-based ad systems in the world'},
    {'name': 'Sam Ovens', 'search_term': 'Sam Ovens', 'tier': 1, 'why_study': 'Consulting.com / Skool. Clean, direct, high-converting copy'},
    {'name': 'Frank Kern', 'search_term': 'Frank Kern', 'tier': 1, 'why_study': 'OG direct response. His retargeting sequences are worth studying'},
    {'name': 'Myron Golden', 'search_term': 'Myron Golden', 'tier': 1, 'why_study': 'High-ticket offer positioning. Bold hooks, strong authority framing'},
    {'name': 'Leila Hormozi', 'search_term': 'Leila Hormozi', 'tier': 1, 'why_study': 'Different angle to Alex. More operational/team-building hooks'},
    {'name': 'Pedro Adao', 'search_term': 'Pedro Adao', 'tier': 1, 'why_study': 'Challenge funnel ads. Studies in urgency and event-based creative'},
    {'name': 'Brendon Burchard', 'search_term': 'Brendon Burchard', 'tier': 1, 'why_study': 'High Performance. Polished creative with strong emotional hooks'},
    {'name': 'Tony Robbins', 'search_term': 'Tony Robbins', 'tier': 1, 'why_study': 'Scale-level brand advertising meets direct response'},

    # Tier 2: Marketing & Agency Operators (7)
    {'name': 'Billy Gene', 'search_term': 'Billy Gene', 'tier': 2, 'why_study': 'Known for creative that stops the scroll'},
    {'name': 'Molly Pittman', 'search_term': 'Molly Pittman', 'tier': 2, 'why_study': 'Ex-DigitalMarketer. Teaches Meta ads and runs excellent creative'},
    {'name': 'Cat Howell', 'search_term': 'Cat Howell', 'tier': 2, 'why_study': 'Agency owner focused on Meta ads for coaches'},
    {'name': 'Nick Shackelford', 'search_term': 'Nick Shackelford', 'tier': 2, 'why_study': 'DTC and performance creative specialist'},
    {'name': 'Khalid Hamadeh', 'search_term': 'Khalid Hamadeh', 'tier': 2, 'why_study': 'Structured Media. Runs massive ad spend'},
    {'name': 'Andrew Hubbard', 'search_term': 'Andrew Hubbard', 'tier': 2, 'why_study': 'Webinar and course ads specialist'},
    {'name': 'Depesh Mandalia', 'search_term': 'Depesh Mandalia', 'tier': 2, 'why_study': 'UK-based Meta ads expert'},

    # Tier 3: Content-First Entrepreneurs (6)
    {'name': 'Gary Vaynerchuk', 'search_term': 'Gary Vaynerchuk', 'tier': 3, 'why_study': 'Content volume king. His team repurposes content into ads at scale'},
    {'name': 'Chris Williamson', 'search_term': 'Chris Williamson', 'tier': 3, 'why_study': 'Modern Wisdom. UK-based. Strong hook writing for male 25-40 audience'},
    {'name': 'Steven Bartlett', 'search_term': 'Steven Bartlett', 'tier': 3, 'why_study': 'Diary of a CEO. UK entrepreneur. His ad creative is worth studying'},
    {'name': 'Ali Abdaal', 'search_term': 'Ali Abdaal', 'tier': 3, 'why_study': 'Course creator ads. Clean, educational hooks'},
    {'name': 'Iman Gadzhi', 'search_term': 'Iman Gadzhi', 'tier': 3, 'why_study': 'Agency/education. Aggressive hooks, strong proof-led creative'},

    # Tier 4: Direct Response Copywriters (5)
    {'name': 'Stefan Georgi', 'search_term': 'Stefan Georgi', 'tier': 4, 'why_study': 'One of the highest-paid copywriters alive'},
    {'name': 'Justin Goff', 'search_term': 'Justin Goff', 'tier': 4, 'why_study': 'Email and ad copy. Studies in long-form ad creative'},
    {'name': 'Dara Denney', 'search_term': 'Dara Denney', 'tier': 4, 'why_study': 'Performance creative strategist'},
    {'name': 'Barry Hott', 'search_term': 'Barry Hott', 'tier': 4, 'why_study': 'Meta ads creative analyst'},
    {'name': 'Sarah Levinger', 'search_term': 'Sarah Levinger', 'tier': 4, 'why_study': 'Consumer psychology meets ad creative'},

    # Tier 5: UK-Specific (3)
    {'name': 'Andrew and Pete', 'search_term': 'Andrew and Pete', 'tier': 5, 'why_study': 'UK content marketing'},
    {'name': 'Rob Moore', 'search_term': 'Rob Moore', 'tier': 5, 'why_study': 'Progressive Property / Rob Moore brand. High-volume UK entrepreneur ads'},
    {'name': 'James Sinclair', 'search_term': 'James Sinclair', 'tier': 5, 'why_study': 'UK business owner. Down-to-earth creative style similar to our positioning'},
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

def scrape_facebook_ads(apify_token: str, search_term: str, max_ads: int = 20) -> List[Dict]:
    """
    Scrape Facebook Ad Library using Apify's curious_coder/facebook-ads-library-scraper

    Args:
        apify_token: Apify API token
        search_term: Search term (competitor name)
        max_ads: Maximum number of ads to scrape (minimum 10)

    Returns:
        List of ad objects
    """
    client = ApifyClient(apify_token)

    # Build Ad Library search URL
    ad_library_url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q={search_term.replace(' ', '%20')}&search_type=keyword_unordered&media_type=all"

    # Prepare Actor input (must be minimum 10 ads)
    run_input = {
        "urls": [
            {"url": ad_library_url}
        ],
        "count": max(10, max_ads),  # Minimum 10
        "scrapePageAds.period": "",
        "scrapePageAds.activeStatus": "all",
        "scrapePageAds.sortBy": "impressions_desc",
        "scrapePageAds.countryCode": "ALL"
    }

    print(f"🔄 Starting Ad Library scrape for '{search_term}'...")
    print(f"   URL: {ad_library_url}")

    try:
        # Run the Actor and wait for it to finish
        run = client.actor("curious_coder/facebook-ads-library-scraper").call(run_input=run_input)

        # Fetch results from the run's dataset
        ads = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            # Skip error items
            if 'error' not in item:
                ads.append(item)

        print(f"✅ Scraped {len(ads)} ads")
        return ads

    except Exception as e:
        print(f"❌ Error scraping ads for '{search_term}': {e}")
        return []

def classify_hook_type(ad_text: str) -> str:
    """
    Classify the hook type based on ad copy opening

    Args:
        ad_text: Ad primary text

    Returns:
        Hook type classification
    """
    if not ad_text:
        return "Unknown"

    opening = ad_text[:125].lower()

    # Check for patterns
    if '?' in opening:
        return "Question"
    elif any(word in opening for word in ['struggling', 'problem', 'challenge', 'frustrated', 'stuck', 'tired of', 'stop']):
        return "Pain Point"
    elif any(char.isdigit() for char in opening) and any(word in opening for word in ['£', '$', '%', 'x', 'grew', 'added', 'made', 'increase', 'revenue', 'million']):
        return "Metric/Result"
    elif any(word in opening for word in ['secret', 'hidden', 'nobody', 'most people', 'everyone', 'truth', 'lie']):
        return "Bold Statement"
    elif any(word in opening for word in ['when i', 'i was', 'my first', 'back in', 'i remember', 'story']):
        return "Story"
    elif any(word in opening for word in ['how to', 'here\'s how', '3 ways', '5 steps', 'framework']):
        return "How-To/Framework"
    else:
        return "Statement"

def extract_cta_style(ad_text: str) -> str:
    """
    Extract CTA style from ad

    Args:
        ad_text: Ad primary text

    Returns:
        CTA style classification
    """
    if not ad_text:
        return "None"

    lower_text = ad_text.lower()

    # Check for common CTAs
    if any(phrase in lower_text for phrase in ['book a call', 'schedule a call', 'apply now', 'download', 'register', 'sign up', 'get started']):
        return "Hard CTA"
    elif any(phrase in lower_text for phrase in ['learn more', 'discover', 'find out', 'see how']):
        return "Soft CTA"
    elif any(phrase in lower_text for phrase in ['comment', 'tag', 'share']):
        return "Engagement CTA"
    else:
        return "No CTA"

def calculate_run_duration(start_date: str) -> int:
    """
    Calculate how many days an ad has been running

    Args:
        start_date: Start date string

    Returns:
        Number of days running
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        now = datetime.now()
        duration = (now - start).days
        return max(0, duration)
    except:
        return 0

def analyze_ad(ad: Dict) -> Dict:
    """
    Analyze a single Facebook ad and extract key elements

    Args:
        ad: Ad object from Apify scraper (curious_coder format)

    Returns:
        Dictionary with analyzed elements
    """
    # Extract snapshot data (defensive - body can be None)
    snapshot = ad.get('snapshot', {})
    body = snapshot.get('body') if snapshot else None

    # Extract text from snapshot.body.text (handle None)
    text = body.get('text', '') if body and isinstance(body, dict) else ''

    # Extract dates
    start_date = ad.get('start_date_formatted', '')
    end_date = ad.get('end_date_formatted', '')
    run_duration = calculate_run_duration(ad.get('start_date', ''))

    return {
        'ad_text': text,
        'opening_line': text[:125] if text else '',
        'hook_type': classify_hook_type(text),
        'cta_style': extract_cta_style(text),
        'run_duration': run_duration,
        'start_date': start_date,
        'end_date': end_date,
        'page_name': ad.get('page_name', 'Unknown'),
        'ad_snapshot_url': ad.get('ad_library_url', ''),
        'platforms': ad.get('publisher_platform', []),
        'link_caption': snapshot.get('caption', ''),
        'cta_text': snapshot.get('cta_text', ''),
        'impressions': ad.get('impressions_with_index', 'Unknown'),
        'spend': ad.get('spend', {}),
        'currency': ad.get('currency', 'Unknown'),
    }

def generate_competitor_report(competitor: Dict, analyzed_ads: List[Dict]) -> str:
    """
    Generate markdown report for a single competitor

    Args:
        competitor: Competitor metadata
        analyzed_ads: List of analyzed ad objects

    Returns:
        Formatted markdown report
    """
    # Sort ads by run duration (longer = better performing)
    sorted_ads = sorted(analyzed_ads, key=lambda x: x['run_duration'], reverse=True)

    # Hook type distribution
    hook_types = [a['hook_type'] for a in analyzed_ads]
    hook_distribution = {hook: hook_types.count(hook) for hook in set(hook_types)}
    total_ads = len(analyzed_ads)

    report = f"""# {competitor['name']} - Facebook Ad Library Analysis

**Analyzed:** {datetime.now().strftime('%Y-%m-%d')}
**Tier:** {competitor['tier']}
**Why Study:** {competitor['why_study']}
**Total Ads Analyzed:** {total_ads}

---

## Top 10 Longest-Running Ads (Performance Indicator)

"""

    for i, ad in enumerate(sorted_ads[:10], 1):
        report += f"""### Ad #{i} - {ad['hook_type']} | Running {ad['run_duration']} days

**Opening Line (First 125 chars):**
{ad['opening_line']}

**Full Ad Copy:**
{ad['ad_text'][:1000]}{"..." if len(ad['ad_text']) > 1000 else ""}

**Details:**
- **CTA Style:** {ad['cta_style']}
- **CTA Text:** {ad.get('cta_text', 'N/A')}
- **Page Name:** {ad['page_name']}
- **Platforms:** {', '.join(ad['platforms']) if isinstance(ad['platforms'], list) else ad['platforms']}
- **Start Date:** {ad['start_date']}
- **End Date:** {ad.get('end_date', 'Active')}
- **Link Caption:** {ad['link_caption']}
- **Impressions:** {ad.get('impressions', 'N/A')}
- **Spend:** {ad.get('spend', 'N/A')} {ad.get('currency', '')}

**Ad Snapshot:** {ad['ad_snapshot_url']}

---

"""

    report += f"""## Hook Pattern Analysis

### Hook Type Distribution
"""

    for hook, count in sorted(hook_distribution.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_ads * 100) if total_ads > 0 else 0
        report += f"- **{hook}:** {percentage:.1f}% ({count} ads)\n"

    # CTA analysis
    cta_styles = [a['cta_style'] for a in analyzed_ads]
    cta_distribution = {cta: cta_styles.count(cta) for cta in set(cta_styles)}

    report += f"""
### CTA Style Distribution
"""

    for cta, count in sorted(cta_distribution.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_ads * 100) if total_ads > 0 else 0
        report += f"- **{cta}:** {percentage:.1f}% ({count} ads)\n"

    # Average run duration
    avg_duration = sum(a['run_duration'] for a in analyzed_ads) / total_ads if total_ads > 0 else 0

    report += f"""
### Key Insights
- Average ad run duration: {avg_duration:.0f} days
- Most common hook: {max(hook_distribution, key=hook_distribution.get)}
- Most common CTA style: {max(cta_distribution, key=cta_distribution.get)}
- Longest running hook type: {sorted_ads[0]['hook_type'] if sorted_ads else 'N/A'}

---

## Offer Positioning Patterns

"""

    # Extract offer mentions
    offers = []
    for ad in analyzed_ads[:10]:
        text_lower = ad['ad_text'].lower()
        if any(word in text_lower for word in ['free', 'download', 'guide', 'masterclass', 'training', 'webinar', 'call', 'consultation']):
            offers.append(ad.get('cta_text') or ad.get('link_caption') or 'Unknown offer')

    if offers:
        report += "Common lead magnets/offers mentioned:\n"
        for offer in set(offers[:5]):
            report += f"- {offer}\n"
    else:
        report += "No obvious lead magnets detected in top ads.\n"

    report += f"""
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

    print(f"\n🚀 Starting Facebook Ad Library competitor analysis (FULL MODE)")
    print(f"📊 Analyzing {len(COMPETITORS_FULL)} competitors (31 total)\n")

    output_dir = Path(__file__).parent / 'outputs' / 'ad-library-analysis'
    output_dir.mkdir(parents=True, exist_ok=True)

    all_results = []

    for competitor in COMPETITORS_FULL:
        print(f"\n{'='*60}")
        print(f"Analyzing: {competitor['name']}")
        print(f"{'='*60}\n")

        # Scrape ads
        ads = scrape_facebook_ads(
            apify_token=apify_token,
            search_term=competitor['search_term'],
            max_ads=20  # Test with 20 ads per competitor
        )

        if not ads:
            print(f"⚠️  No ads found for {competitor['name']}, skipping...\n")
            continue

        # Analyze ads
        analyzed_ads = [analyze_ad(ad) for ad in ads]

        # Generate report
        report = generate_competitor_report(competitor, analyzed_ads)

        # Save individual report
        filename = f"{competitor['name'].lower().replace(' ', '-')}-ad-library-{datetime.now().strftime('%Y-%m-%d')}.md"
        report_path = output_dir / filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✅ Report saved: {report_path}")

        # Store results
        all_results.append({
            'competitor': competitor['name'],
            'ads_analyzed': len(analyzed_ads),
            'report_path': str(report_path)
        })

        # Rate limiting (be nice to Apify)
        if competitor != COMPETITORS_FULL[-1]:
            print(f"\n⏳ Waiting 10 seconds before next competitor...")
            time.sleep(10)

    # Generate summary
    print(f"\n{'='*60}")
    print(f"✅ Analysis Complete!")
    print(f"{'='*60}\n")

    print("📊 Summary:")
    for result in all_results:
        print(f"  - {result['competitor']}: {result['ads_analyzed']} ads analyzed")

    print(f"\n📁 All reports saved to: {output_dir}")
    print(f"\n💡 Next Steps:")
    print(f"  1. Review individual competitor reports")
    print(f"  2. Identify winning hook patterns and offer positioning")
    print(f"  3. Use meta-ad-copy skill to generate new ads based on insights")

if __name__ == "__main__":
    main()
