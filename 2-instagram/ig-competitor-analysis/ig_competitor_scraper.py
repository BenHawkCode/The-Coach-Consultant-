#!/usr/bin/env python3
"""
IG Competitor Analysis - Multi-Profile Scraper & Analyser
The Coach Consultant - AI Content Generation System

Scrapes multiple Instagram competitor profiles and generates a consolidated
analysis report comparing hook patterns, caption structures, engagement data,
content formats, and posting strategies across all competitors.

Uses Apify actor: apify/instagram-scraper

Usage:
    python ig_competitor_scraper.py                          # Scrape all competitors
    python ig_competitor_scraper.py --sender "danmartell"    # Single competitor
    python ig_competitor_scraper.py --analyze-only           # Skip scraping, analyze existing data
    python ig_competitor_scraper.py --max-posts 30           # Limit posts per profile
"""

import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from collections import Counter
from apify_client import ApifyClient


SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
OUTPUT_DIR = SCRIPT_DIR / "outputs"

# Competitor list - mirrors meta-ad-competitor swipe list (31 profiles)
COMPETITORS = [
    # Tier 1: Business Education & Coaching (Direct Competitors)
    {"username": "benhawksworth_", "name": "Ben Hawksworth", "tier": 0, "why": "Our own account — benchmark"},
    {"username": "hormozi", "name": "Alex Hormozi", "tier": 1, "why": "Master of direct response hooks, metric-led copy"},
    {"username": "danmartell", "name": "Dan Martell", "tier": 1, "why": "SaaS and coaching, framework hooks, authority positioning"},
    {"username": "russellbrunson", "name": "Russell Brunson", "tier": 1, "why": "ClickFunnels, funnel-based ad systems"},
    {"username": "sam.ovens", "name": "Sam Ovens", "tier": 1, "why": "Consulting.com / Skool, data-driven creative"},
    {"username": "frankkern", "name": "Frank Kern", "tier": 1, "why": "OG direct response, retargeting sequences"},
    {"username": "myrongolden", "name": "Myron Golden", "tier": 1, "why": "High-ticket offer positioning, bold hooks"},
    {"username": "leilahormozi", "name": "Leila Hormozi", "tier": 1, "why": "Operational/team-building hooks, female audience"},
    {"username": "pedromadao", "name": "Pedro Adao", "tier": 1, "why": "Challenge funnel ads, urgency and event-based creative"},
    {"username": "brendonburchard", "name": "Brendon Burchard", "tier": 1, "why": "Polished creative with strong emotional hooks"},
    {"username": "tonyrobbins", "name": "Tony Robbins", "tier": 1, "why": "Scale-level brand advertising meets direct response"},

    # Tier 2: Marketing & Agency Operators
    {"username": "billygeneismarketing", "name": "Billy Gene Shaw", "tier": 2, "why": "Scroll-stopping creative, entertaining hooks"},
    {"username": "mollypittmandigital", "name": "Molly Pittman", "tier": 2, "why": "Ex-DigitalMarketer, Meta ads expert"},
    {"username": "cathowell", "name": "Cat Howell", "tier": 2, "why": "Agency owner, Meta ads for business owners"},
    {"username": "iamnickshackelford", "name": "Nick Shackelford", "tier": 2, "why": "DTC performance creative, UGC-style ads"},
    {"username": "thekhalidh", "name": "Khalid Hamadeh", "tier": 2, "why": "Structured Media, methodical creative testing"},
    {"username": "andrewnhubbard", "name": "Andrew Hubbard", "tier": 2, "why": "Webinar and course ads specialist"},
    {"username": "depeshmandalia", "name": "Depesh Mandalia", "tier": 2, "why": "UK-based Meta ads expert, scaling creative"},

    # Tier 3: Content-First Entrepreneurs
    {"username": "garyvee", "name": "Gary Vaynerchuk", "tier": 3, "why": "Content volume king, repurposes content to ads at scale"},
    {"username": "chriswillx", "name": "Chris Williamson", "tier": 3, "why": "Modern Wisdom, UK-based, strong hooks for male 25-40"},
    {"username": "steven", "name": "Steven Bartlett", "tier": 3, "why": "Diary of a CEO, UK entrepreneur"},
    {"username": "aliabdaal", "name": "Ali Abdaal", "tier": 3, "why": "Course creator, clean educational hooks"},
    {"username": "imangadzhi", "name": "Iman Gadzhi", "tier": 3, "why": "Agency/education, aggressive hooks, proof-led creative"},

    # Tier 4: Direct Response Copywriters & Creative Strategists
    {"username": "stefangeorgi", "name": "Stefan Georgi", "tier": 4, "why": "Highest-paid copywriter, exceptional ad frameworks"},
    {"username": "itsjgoff", "name": "Justin Goff", "tier": 4, "why": "Email and ad copy, long-form ad creative"},
    {"username": "daradenney", "name": "Dara Denney", "tier": 4, "why": "Performance creative strategist, public ad breakdowns"},
    {"username": "binghott", "name": "Barry Hott", "tier": 4, "why": "Meta ads creative analyst, winning ad breakdowns"},
    {"username": "sarah.levinger", "name": "Sarah Levinger", "tier": 4, "why": "Consumer psychology meets ad creative"},

    # Tier 5: UK-Specific (Closest to Our Market)
    {"username": "andrewandpete", "name": "Andrew & Pete", "tier": 5, "why": "UK content marketing, coaching market ads"},
    {"username": "robmooreprogressive", "name": "Rob Moore", "tier": 5, "why": "Progressive Property, high-volume UK entrepreneur ads"},
    {"username": "jamessinclairentrepreneur", "name": "James Sinclair", "tier": 5, "why": "UK business owner, down-to-earth creative"},
]

DEFAULT_MAX_POSTS = 30


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


def scrape_profile(client: ApifyClient, username: str, max_posts: int = DEFAULT_MAX_POSTS) -> List[Dict]:
    """Scrape a single Instagram profile."""
    run_input = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": max_posts,
        "searchType": "user",
        "searchLimit": 1,
    }
    print(f"  Scraping @{username} (up to {max_posts} posts)...")
    try:
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        posts = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        print(f"    Found {len(posts)} posts")
        return posts
    except Exception as e:
        print(f"    Error: {e}")
        return []


def classify_hook(text: str) -> str:
    """Classify hook type from caption opening."""
    if not text:
        return "Unknown"
    opening = text[:125].lower()
    if '?' in opening:
        return "Question"
    elif any(w in opening for w in ['struggling', 'problem', 'stuck', 'tired of', 'stop', "don't", 'never', 'frustrated']):
        return "Pain Point"
    elif any(c.isdigit() for c in opening) and any(w in opening for w in ['£', '$', '%', 'x', 'grew', 'added', 'made', 'increase', 'revenue', 'k', 'clients']):
        return "Metric/Result"
    elif any(w in opening for w in ['secret', 'hidden', 'nobody', 'most people', 'everyone', 'truth', 'lie', 'myth']):
        return "Bold Statement"
    elif any(w in opening for w in ['when i', 'i was', 'my first', 'back in', 'i remember', 'story', 'last year']):
        return "Story"
    elif any(w in opening for w in ['how to', "here's how", '3 ways', '5 steps', 'framework', 'step 1']):
        return "How-To"
    elif any(w in opening for w in ['comment', 'save this', 'tag someone', 'share this', 'dm me', 'drop a']):
        return "Engagement Bait"
    return "Statement"


def classify_cta(text: str) -> str:
    """Classify CTA style."""
    if not text:
        return "No CTA"
    lower = text.lower()
    if any(p in lower for p in ['link in bio', 'click the link', 'dm me', 'book a call', 'sign up', 'download']):
        return "Hard CTA"
    elif any(p in lower for p in ['comment', 'tag someone', 'share this', 'save this', 'drop a', 'type']):
        return "Engagement CTA"
    elif any(p in lower for p in ['what do you think', 'let me know', 'thoughts?', 'agree?']):
        return "Soft CTA"
    return "No CTA"


def classify_content_type(post: Dict) -> str:
    """Classify content type."""
    post_type = post.get('type', '').lower()
    if post_type == 'sidecar':
        return "Carousel"
    elif post_type == 'video':
        return "Video/Reel"
    elif post_type == 'image':
        return "Image"
    return "Video/Reel" if post.get('videoUrl') else "Image"


def analyze_post(post: Dict) -> Dict:
    """Extract key data from a single post."""
    caption = post.get('caption', '') or ''
    likes = post.get('likesCount', 0) or 0
    comments = post.get('commentsCount', 0) or 0
    timestamp = post.get('timestamp', '')

    parsed_date = None
    if timestamp:
        try:
            parsed_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            pass

    return {
        'caption': caption,
        'opening_line': caption[:125] if caption else '',
        'caption_length': len(caption),
        'hook_type': classify_hook(caption),
        'cta_style': classify_cta(caption),
        'content_type': classify_content_type(post),
        'likes': likes,
        'comments': comments,
        'engagement_score': likes + (comments * 3),
        'video_views': post.get('videoViewCount', 0) or 0,
        'url': post.get('url', ''),
        'timestamp': timestamp,
        'parsed_date': parsed_date,
        'hashtags': post.get('hashtags', []) or [],
    }


def scrape_all_competitors(client: ApifyClient, competitors: List[Dict], max_posts: int) -> Dict[str, List[Dict]]:
    """Scrape all competitors and return analyzed posts per profile."""
    all_data = {}

    for i, comp in enumerate(competitors, 1):
        username = comp["username"]
        print(f"\n[{i}/{len(competitors)}] {comp['name']} (@{username})")

        raw_posts = scrape_profile(client, username, max_posts)
        if raw_posts:
            analyzed = [analyze_post(p) for p in raw_posts]
            all_data[username] = {
                "name": comp["name"],
                "tier": comp["tier"],
                "why": comp["why"],
                "posts": analyzed,
                "raw_count": len(raw_posts),
            }

            # Save individual raw data
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(DATA_DIR / f"{username}-raw.json", "w") as f:
                json.dump(raw_posts, f, default=str, indent=2)

    return all_data


def generate_consolidated_report(all_data: Dict) -> str:
    """Generate a consolidated analysis report across all competitors."""
    now = datetime.now().strftime('%Y-%m-%d')
    total_profiles = len(all_data)
    total_posts = sum(d["raw_count"] for d in all_data.values())

    # Aggregate all posts with sender info
    all_posts = []
    for username, data in all_data.items():
        for post in data["posts"]:
            post["sender"] = data["name"]
            post["sender_username"] = username
            all_posts.append(post)

    # --- Compute Metrics ---

    # Hook distribution (global)
    hook_counts = Counter(p["hook_type"] for p in all_posts)
    hook_engagement = {}
    for hook in hook_counts:
        posts_with_hook = [p for p in all_posts if p["hook_type"] == hook]
        avg_eng = sum(p["engagement_score"] for p in posts_with_hook) / len(posts_with_hook)
        hook_engagement[hook] = round(avg_eng)

    # Content type distribution
    content_counts = Counter(p["content_type"] for p in all_posts)
    content_engagement = {}
    for ct in content_counts:
        posts_with_ct = [p for p in all_posts if p["content_type"] == ct]
        avg_eng = sum(p["engagement_score"] for p in posts_with_ct) / len(posts_with_ct)
        content_engagement[ct] = round(avg_eng)

    # CTA distribution
    cta_counts = Counter(p["cta_style"] for p in all_posts)

    # Caption length analysis
    avg_caption = sum(p["caption_length"] for p in all_posts) / len(all_posts) if all_posts else 0

    # Per-sender stats
    sender_stats = {}
    for username, data in all_data.items():
        posts = data["posts"]
        if not posts:
            continue
        avg_eng = sum(p["engagement_score"] for p in posts) / len(posts)
        top_hook = Counter(p["hook_type"] for p in posts).most_common(1)[0][0] if posts else "—"
        top_content = Counter(p["content_type"] for p in posts).most_common(1)[0][0] if posts else "—"
        avg_cap = sum(p["caption_length"] for p in posts) / len(posts)
        sender_stats[username] = {
            "name": data["name"],
            "tier": data["tier"],
            "posts": len(posts),
            "avg_engagement": round(avg_eng),
            "top_hook": top_hook,
            "top_content": top_content,
            "avg_caption_length": round(avg_cap),
        }

    # Top 20 posts across all competitors
    top_posts = sorted(all_posts, key=lambda x: x["engagement_score"], reverse=True)[:20]

    # Top hooks (best opening lines by engagement)
    top_hooks = sorted(all_posts, key=lambda x: x["engagement_score"], reverse=True)[:30]

    # --- Build Report ---

    report = f"""# IG Competitor Analysis — Consolidated Report

**Date:** {now}
**Profiles Analysed:** {total_profiles}
**Total Posts Analysed:** {total_posts}

---

## 1. Competitor Overview

| Sender | Posts | Avg Engagement | Top Hook | Top Format | Avg Caption |
|--------|-------|---------------|----------|------------|-------------|
"""

    for username in sorted(sender_stats, key=lambda x: sender_stats[x]["avg_engagement"], reverse=True):
        s = sender_stats[username]
        report += f"| {s['name']} | {s['posts']} | {s['avg_engagement']:,} | {s['top_hook']} | {s['top_content']} | {s['avg_caption_length']} chars |\n"

    report += f"""
---

## 2. Hook Pattern Analysis (All Competitors)

| Hook Type | Count | % | Avg Engagement |
|-----------|-------|---|---------------|
"""

    for hook, count in hook_counts.most_common():
        pct = round(count / len(all_posts) * 100, 1)
        avg_eng = hook_engagement.get(hook, 0)
        report += f"| {hook} | {count} | {pct}% | {avg_eng:,} |\n"

    best_hook = max(hook_engagement, key=hook_engagement.get) if hook_engagement else "—"
    report += f"\n**Highest engagement hook:** {best_hook} (avg {hook_engagement.get(best_hook, 0):,})\n"

    report += f"""
---

## 3. Content Format Analysis

| Format | Count | % | Avg Engagement |
|--------|-------|---|---------------|
"""

    for ct, count in content_counts.most_common():
        pct = round(count / len(all_posts) * 100, 1)
        avg_eng = content_engagement.get(ct, 0)
        report += f"| {ct} | {count} | {pct}% | {avg_eng:,} |\n"

    best_format = max(content_engagement, key=content_engagement.get) if content_engagement else "—"
    report += f"\n**Best performing format:** {best_format} (avg {content_engagement.get(best_format, 0):,})\n"

    report += f"""
---

## 4. CTA Strategy

| CTA Type | Count | % |
|----------|-------|---|
"""

    for cta, count in cta_counts.most_common():
        pct = round(count / len(all_posts) * 100, 1)
        report += f"| {cta} | {count} | {pct}% |\n"

    report += f"""
---

## 5. Caption Length Analysis

**Average across all competitors:** {avg_caption:.0f} characters

| Length | Posts | Avg Engagement |
|--------|-------|---------------|
"""

    short = [p for p in all_posts if p["caption_length"] < 300]
    medium = [p for p in all_posts if 300 <= p["caption_length"] < 800]
    long = [p for p in all_posts if p["caption_length"] >= 800]

    if short:
        avg_s = sum(p["engagement_score"] for p in short) / len(short)
        report += f"| Short (<300) | {len(short)} | {avg_s:,.0f} |\n"
    if medium:
        avg_m = sum(p["engagement_score"] for p in medium) / len(medium)
        report += f"| Medium (300-800) | {len(medium)} | {avg_m:,.0f} |\n"
    if long:
        avg_l = sum(p["engagement_score"] for p in long) / len(long)
        report += f"| Long (800+) | {len(long)} | {avg_l:,.0f} |\n"

    report += f"""
---

## 6. Top 20 Posts Across All Competitors

"""

    for i, p in enumerate(top_posts, 1):
        opening = p["opening_line"][:100] if p["opening_line"] else "(no caption)"
        report += f"**#{i}** | @{p['sender_username']} | {p['content_type']} | {p['hook_type']}\n"
        report += f"- Engagement: {p['engagement_score']:,} ({p['likes']:,} likes, {p['comments']:,} comments)\n"
        report += f"- Hook: \"{opening}...\"\n"
        if p["url"]:
            report += f"- URL: {p['url']}\n"
        report += "\n"

    report += f"""---

## 7. Top 30 Hooks — Swipe File

"""

    for i, p in enumerate(top_hooks, 1):
        opening = p["opening_line"] if p["opening_line"] else "(no caption)"
        report += f"{i}. **@{p['sender_username']}** ({p['hook_type']}, {p['engagement_score']:,} eng)\n"
        report += f"   \"{opening}\"\n\n"

    report += f"""---

## 8. Key Takeaways for Ben

**Actionable patterns for The Coach Consultant's Instagram strategy:**

"""

    # Generate takeaways
    takeaways = []

    if best_format:
        takeaways.append(f"**{best_format} posts dominate.** Across all competitors, {best_format} gets the highest average engagement ({content_engagement.get(best_format, 0):,}). Ben should prioritise this format.")

    if best_hook:
        takeaways.append(f"**{best_hook} hooks drive engagement.** The most effective opening style is {best_hook} with {hook_engagement.get(best_hook, 0):,} average engagement. Use this more often.")

    most_used_hook = hook_counts.most_common(1)[0][0] if hook_counts else "—"
    takeaways.append(f"**Most used hook is {most_used_hook}.** Competitors lean on {most_used_hook} hooks ({hook_counts[most_used_hook]} posts). Consider if Ben is using enough variety.")

    top_cta = cta_counts.most_common(1)[0][0] if cta_counts else "—"
    takeaways.append(f"**CTA pattern: {top_cta} leads.** Most competitor posts use {top_cta} ({cta_counts[top_cta]} posts). Ben's 'Comment [WORD]' pattern aligns with engagement-first approach.")

    if long:
        avg_long_eng = sum(p["engagement_score"] for p in long) / len(long)
        takeaways.append(f"**Long captions work.** Posts with 800+ chars average {avg_long_eng:,.0f} engagement. Ben's data confirms this — 800+ chars is optimal.")

    # Top performer
    if sender_stats:
        top_sender = max(sender_stats.values(), key=lambda x: x["avg_engagement"])
        takeaways.append(f"**Study @{[k for k,v in sender_stats.items() if v == top_sender][0]}.** {top_sender['name']} has the highest avg engagement ({top_sender['avg_engagement']:,}) using {top_sender['top_hook']} hooks and {top_sender['top_content']} format.")

    takeaways.append("**Differentiation opportunity.** Ben's authentic, no-BS Yorkshire voice stands out against polished US competitors. Lean into this — authenticity is the gap.")

    for i, t in enumerate(takeaways, 1):
        report += f"{i}. {t}\n\n"

    report += f"""---

*Report generated by IG Competitor Analysis | The Coach Consultant*
*Data source: Apify instagram-scraper*
"""

    return report


def main():
    parser = argparse.ArgumentParser(description="IG Competitor Analysis - Multi-Profile Scraper")
    parser.add_argument("--sender", type=str, help="Scrape a specific username only")
    parser.add_argument("--max-posts", type=int, default=DEFAULT_MAX_POSTS, help="Max posts per profile")
    parser.add_argument("--analyze-only", action="store_true", help="Skip scraping, analyze existing data")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  IG Competitor Analysis")
    print(f"  The Coach Consultant")
    print(f"{'='*60}\n")

    competitors = COMPETITORS

    if args.sender:
        competitors = [c for c in COMPETITORS if args.sender.lower() in c["username"].lower() or args.sender.lower() in c["name"].lower()]
        if not competitors:
            # Treat as a new username
            competitors = [{"username": args.sender, "name": args.sender, "tier": 0, "why": "Custom analysis"}]

    if args.analyze_only:
        # Load existing data
        print("Analyzing existing data...")
        all_data = {}
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        for comp in competitors:
            raw_file = DATA_DIR / f"{comp['username']}-raw.json"
            if raw_file.exists():
                with open(raw_file) as f:
                    raw_posts = json.load(f)
                analyzed = [analyze_post(p) for p in raw_posts]
                all_data[comp["username"]] = {
                    "name": comp["name"],
                    "tier": comp["tier"],
                    "why": comp["why"],
                    "posts": analyzed,
                    "raw_count": len(raw_posts),
                }
                print(f"  Loaded {len(raw_posts)} posts for @{comp['username']}")
            else:
                print(f"  No data for @{comp['username']} — run without --analyze-only first")
    else:
        # Scrape fresh data
        env = load_env()
        apify_token = env.get('APIFY_API_TOKEN')
        if not apify_token:
            print("Error: APIFY_API_TOKEN not found in .env")
            sys.exit(1)

        client = ApifyClient(apify_token)
        all_data = scrape_all_competitors(client, competitors, args.max_posts)

    if not all_data:
        print("No data collected. Check usernames and API token.")
        sys.exit(1)

    # Generate report
    print(f"\nGenerating consolidated report...")
    report = generate_consolidated_report(all_data)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime('%Y-%m-%d')
    suffix = f"-{args.sender.lower()}" if args.sender else ""
    filename = f"IG-COMPETITOR-ANALYSIS{suffix}-{now}.md"
    output_path = OUTPUT_DIR / filename

    with open(output_path, 'w') as f:
        f.write(report)

    print(f"\n{'='*60}")
    print(f"  Report saved: {output_path}")
    print(f"  Profiles: {len(all_data)}")
    print(f"  Total posts: {sum(d['raw_count'] for d in all_data.values())}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
