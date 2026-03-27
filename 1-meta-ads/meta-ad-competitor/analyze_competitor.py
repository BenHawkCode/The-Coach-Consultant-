#!/usr/bin/env python3
"""
Meta Ad Competitor Analysis Script
The Coach Consultant - AI Content Generation System

Pulls competitor ads from Meta Ad Library API, analyzes patterns,
cross-references with your own top performers, and generates hybrid variations.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import time

# Load environment variables
def load_env():
    """Load credentials from .env file"""
    env_path = Path(__file__).parent.parent.parent / '.env'
    env_vars = {}

    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                env_vars[key] = value

    return env_vars

# Meta Ad Library API - Pull Competitor Ads
def get_competitor_ads(competitor_name: str, countries: List[str], access_token: str, limit: int = 50) -> List[Dict]:
    """
    Query Meta Ad Library API for competitor's active ads

    Args:
        competitor_name: Name to search for (e.g., "Alex Hormozi")
        countries: List of country codes (e.g., ['GB', 'US', 'AU'])
        access_token: Meta API access token
        limit: Maximum number of ads to retrieve

    Returns:
        List of ad objects with metadata
    """
    url = "https://graph.facebook.com/v19.0/ads_archive"

    params = {
        'access_token': access_token,
        'search_terms': competitor_name,
        'ad_reached_countries': countries,
        'ad_active_status': 'ACTIVE',
        'limit': limit,
        'fields': 'id,ad_creative_body,ad_creative_link_captions,ad_snapshot_url,page_name,ad_delivery_start_time,publisher_platforms'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'data' in data:
            return data['data']
        else:
            print(f"Warning: No ads found for {competitor_name}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching competitor ads: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return []

# Meta Marketing API - Pull Your Own Top Performers
def get_your_top_ads(account_id: str, access_token: str, objective: str, limit: int = 10) -> List[Dict]:
    """
    Query Meta Marketing API for your own top-performing ads

    Args:
        account_id: Your Meta ad account ID
        access_token: Meta API access token
        objective: Campaign objective to filter by
        limit: Number of top ads to retrieve

    Returns:
        List of your top-performing ads
    """
    url = f"https://graph.facebook.com/v19.0/act_{account_id}/ads"

    # Map friendly names to Meta API objective values
    objective_mapping = {
        'lead generation': 'OUTCOME_LEADS',
        'webinar': 'OUTCOME_LEADS',
        'course': 'OUTCOME_SALES',
        'consultation': 'OUTCOME_LEADS',
        'awareness': 'OUTCOME_AWARENESS'
    }

    objective_value = objective_mapping.get(objective.lower(), 'OUTCOME_LEADS')

    params = {
        'access_token': access_token,
        'fields': 'id,name,creative{body,link_caption,title,image_url},insights{ctr,clicks,conversions,spend}',
        'filtering': json.dumps([
            {
                'field': 'effective_status',
                'operator': 'IN',
                'value': ['ACTIVE', 'PAUSED']
            }
        ]),
        'limit': limit,
        'time_range': json.dumps({
            'since': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
            'until': datetime.now().strftime('%Y-%m-%d')
        })
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'data' in data:
            # Sort by CTR (engagement proxy)
            ads_with_insights = [ad for ad in data['data'] if 'insights' in ad and ad['insights']['data']]
            sorted_ads = sorted(ads_with_insights,
                              key=lambda x: float(x['insights']['data'][0].get('ctr', 0)),
                              reverse=True)
            return sorted_ads[:limit]
        else:
            print(f"Warning: No ads found in your account for {objective}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching your ads: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return []

# Hook Classification
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
    elif any(word in opening for word in ['struggling', 'problem', 'challenge', 'frustrated', 'stuck']):
        return "Pain Point"
    elif any(char.isdigit() for char in opening) and any(word in opening for word in ['£', '$', 'x', 'grew', 'added', 'made']):
        return "Metric/Result"
    elif any(word in opening for word in ['secret', 'hidden', 'nobody', 'most people', 'everyone']):
        return "Bold Statement"
    elif any(word in opening for word in ['when i', 'i was', 'my first', 'back in']):
        return "Story"
    else:
        return "Statement"

# Calculate run duration
def calculate_run_duration(start_time: str) -> int:
    """
    Calculate how many days an ad has been running

    Args:
        start_time: ISO format timestamp from Meta API

    Returns:
        Number of days running
    """
    try:
        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        now = datetime.now(start.tzinfo)
        duration = (now - start).days
        return max(0, duration)
    except:
        return 0

# Extract key elements from ad
def extract_ad_elements(ad: Dict, is_competitor: bool = True) -> Dict:
    """
    Extract 7 key elements from an ad object

    Args:
        ad: Ad object from Meta API
        is_competitor: True if competitor ad, False if your own ad

    Returns:
        Dictionary with extracted elements
    """
    if is_competitor:
        ad_text = ad.get('ad_creative_body', '')
        caption = ad.get('ad_creative_link_captions', '')
        start_time = ad.get('ad_delivery_start_time', '')
        snapshot_url = ad.get('ad_snapshot_url', '')

        return {
            'ad_text': ad_text,
            'opening_line': ad_text[:125] if ad_text else '',
            'caption': caption,
            'hook_type': classify_hook_type(ad_text),
            'run_duration': calculate_run_duration(start_time),
            'snapshot_url': snapshot_url,
            'page_name': ad.get('page_name', 'Unknown')
        }
    else:
        # Your own ads (different API structure)
        creative = ad.get('creative', {})
        insights = ad.get('insights', {}).get('data', [{}])[0]

        ad_text = creative.get('body', '')

        return {
            'ad_text': ad_text,
            'opening_line': ad_text[:125] if ad_text else '',
            'caption': creative.get('link_caption', ''),
            'hook_type': classify_hook_type(ad_text),
            'ctr': insights.get('ctr', 0),
            'clicks': insights.get('clicks', 0),
            'conversions': insights.get('conversions', 0),
            'spend': insights.get('spend', 0)
        }

# Generate analysis report
def generate_report(competitor_name: str, competitor_ads: List[Dict], your_ads: List[Dict],
                   objective: str, offer: str) -> str:
    """
    Generate the complete markdown analysis report

    Args:
        competitor_name: Name of competitor analyzed
        competitor_ads: List of competitor ad objects with extracted elements
        your_ads: List of your ad objects with extracted elements
        objective: Campaign objective
        offer: User's offer being promoted

    Returns:
        Formatted markdown report
    """
    report = f"""# Meta Ad Analysis: {competitor_name}

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Campaign Objective:** {objective}
**Your Offer:** {offer}

---

## Section 1: {competitor_name}'s Top Ads

"""

    # Sort competitor ads by run duration
    sorted_ads = sorted(competitor_ads, key=lambda x: x.get('run_duration', 0), reverse=True)

    for i, ad in enumerate(sorted_ads[:10], 1):
        report += f"""### Ad #{i} - {ad['hook_type']} | Running {ad['run_duration']} days

**Opening Line:**
{ad['opening_line']}

**Full Ad Copy:**
{ad['ad_text']}

**Caption:** {ad['caption']}
**Page:** {ad['page_name']}
**Ad Library Link:** {ad['snapshot_url']}

---

"""

    # Hook pattern analysis
    hook_types = [ad['hook_type'] for ad in competitor_ads]
    hook_distribution = {hook: hook_types.count(hook) for hook in set(hook_types)}
    total_ads = len(competitor_ads)

    report += f"""## Section 2: Hook Pattern Analysis

### Most Common Hook Types
"""

    for hook, count in sorted(hook_distribution.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_ads * 100) if total_ads > 0 else 0
        report += f"{hook}: {percentage:.1f}% ({count} ads)\n"

    report += f"""
### Key Insights
- Average ad run duration: {sum(ad['run_duration'] for ad in competitor_ads) / len(competitor_ads):.0f} days
- Most successful hook type: {max(hook_distribution, key=hook_distribution.get)}
- Total active ads analyzed: {len(competitor_ads)}

---

## Section 3: Your Top-Performing Ads ({objective})

"""

    if your_ads:
        for i, ad in enumerate(your_ads[:5], 1):
            report += f"""### Your Ad #{i} - {ad['hook_type']}

**Ad Copy:**
{ad['ad_text']}

**Performance:**
- CTR: {ad.get('ctr', 0)}%
- Clicks: {ad.get('clicks', 0)}
- Conversions: {ad.get('conversions', 0)}
- Spend: £{ad.get('spend', 0)}

---

"""
    else:
        report += "No matching campaigns found in your account for comparison.\n\n---\n\n"

    report += """## Section 4: Hybrid Approach - New Ad Variations

*Note: These variations combine competitor-proven hooks with your patterns, written in Ben's voice.*
*For full ad copy generation, use the main skill agent with this analysis.*

### Recommended Next Steps:
1. Review competitor hook patterns above
2. Identify 2-3 hooks that align with your offer
3. Generate full ad variations using meta-ad-copy skill
4. Test in your account with £20-50 daily budget per variation

---

*Report generated by The Coach Consultant Meta Ad Competitor Analysis skill*
"""

    return report

# Main execution
def main():
    """Main script execution"""

    # Load environment variables
    env = load_env()
    access_token = env.get('META_ACCESS_TOKEN')
    account_id = env.get('META_ACCOUNT_ID')

    if not access_token or not account_id:
        print("Error: Missing META_ACCESS_TOKEN or META_ACCOUNT_ID in .env file")
        sys.exit(1)

    # Get command line arguments
    if len(sys.argv) < 4:
        print("Usage: python analyze_competitor.py <competitor_name> <objective> <offer>")
        print("Example: python analyze_competitor.py 'Alex Hormozi' 'lead generation' 'Free Coaching Scorecard'")
        sys.exit(1)

    competitor_name = sys.argv[1]
    objective = sys.argv[2]
    offer = sys.argv[3]

    print(f"Analyzing {competitor_name}'s Meta ads...")
    print(f"Objective: {objective}")
    print(f"Your Offer: {offer}\n")

    # Pull competitor ads
    print("Step 1: Pulling competitor ads from Meta Ad Library API...")
    competitor_ads_raw = get_competitor_ads(
        competitor_name=competitor_name,
        countries=['GB', 'US', 'AU'],
        access_token=access_token,
        limit=50
    )

    if not competitor_ads_raw:
        print(f"\nNo ads found for {competitor_name}. This could mean:")
        print("1. Meta Ad Library API access not yet approved")
        print("2. No active ads from this advertiser in GB/US/AU")
        print("3. Try searching by company/page name instead of person name")
        sys.exit(1)

    print(f"Found {len(competitor_ads_raw)} competitor ads\n")

    # Extract elements from competitor ads
    competitor_ads = [extract_ad_elements(ad, is_competitor=True) for ad in competitor_ads_raw]

    # Pull your own ads
    print("Step 2: Pulling your top-performing ads...")
    time.sleep(1)  # Rate limit prevention

    your_ads_raw = get_your_top_ads(
        account_id=account_id,
        access_token=access_token,
        objective=objective,
        limit=10
    )

    your_ads = [extract_ad_elements(ad, is_competitor=False) for ad in your_ads_raw]
    print(f"Found {len(your_ads)} of your ads\n")

    # Generate report
    print("Step 3: Generating analysis report...")
    report = generate_report(
        competitor_name=competitor_name,
        competitor_ads=competitor_ads,
        your_ads=your_ads,
        objective=objective,
        offer=offer
    )

    # Save report
    output_dir = Path(__file__).parent / 'outputs'
    output_dir.mkdir(exist_ok=True)

    filename = f"{competitor_name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y-%m-%d')}-analysis.md"
    output_path = output_dir / filename

    with open(output_path, 'w') as f:
        f.write(report)

    print(f"\n✅ Analysis complete!")
    print(f"📄 Report saved to: {output_path}")
    print(f"\nNext: Review the report and generate full ad variations using the meta-ad-copy skill.")

if __name__ == "__main__":
    main()
