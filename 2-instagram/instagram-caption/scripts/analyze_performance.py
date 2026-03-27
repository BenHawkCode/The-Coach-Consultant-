#!/usr/bin/env python3
"""
Instagram Performance Analyzer
Identifies patterns in top-performing posts
"""

import json
import re
from collections import Counter
from datetime import datetime

def load_posts():
    """Load fetched Instagram posts"""

    try:
        with open('2-instagram/instagram-caption/outputs/instagram_posts.json', 'r') as f:
            data = json.load(f)
            return data.get('posts', [])
    except FileNotFoundError:
        print("❌ No posts found. Run fetch_posts.py first.")
        return []

def extract_hook(caption):
    """Extract first line (hook) from caption"""
    if not caption:
        return ""
    return caption.split('\n')[0].strip()

def count_lines(caption):
    """Count lines in caption"""
    if not caption:
        return 0
    return len([line for line in caption.split('\n') if line.strip()])

def has_cta(caption):
    """Check if caption has CTA (thecoachconsultant.uk)"""
    if not caption:
        return False
    return 'thecoachconsultant.uk' in caption.lower()

def extract_topic_keywords(caption):
    """Extract potential topic keywords"""
    if not caption:
        return []

    # Common business/coaching keywords
    keywords = [
        'coach', 'consultant', 'client', 'business', 'marketing',
        'sales', 'content', 'automation', 'lead', 'ads', 'meta',
        'instagram', 'email', 'funnel', 'offer', 'pricing', 'niche',
        'onboarding', 'retention', 'conversion', 'pipeline', 'crm',
        'strategy', 'system', 'process', 'template', 'framework'
    ]

    caption_lower = caption.lower()
    found = [kw for kw in keywords if kw in caption_lower]
    return found

def analyze_hook_patterns(posts):
    """Analyze common hook patterns"""

    hooks = [extract_hook(p['caption']) for p in posts if p['caption']]

    # Hook starters
    hook_starters = []
    for hook in hooks:
        words = hook.split()
        if len(words) >= 2:
            hook_starters.append(f"{words[0]} {words[1]}")

    common_starters = Counter(hook_starters).most_common(10)

    return {
        'total_hooks': len(hooks),
        'common_starters': common_starters,
        'avg_hook_length': sum(len(h.split()) for h in hooks) / len(hooks) if hooks else 0
    }

def analyze_length_correlation(posts):
    """Analyze correlation between length and engagement"""

    length_buckets = {
        'short (1-8 lines)': [],
        'medium (9-15 lines)': [],
        'long (16+ lines)': []
    }

    for post in posts:
        lines = count_lines(post['caption'])
        engagement = post.get('engagement_rate', 0)

        if lines <= 8:
            length_buckets['short (1-8 lines)'].append(engagement)
        elif lines <= 15:
            length_buckets['medium (9-15 lines)'].append(engagement)
        else:
            length_buckets['long (16+ lines)'].append(engagement)

    results = {}
    for bucket, rates in length_buckets.items():
        if rates:
            results[bucket] = {
                'count': len(rates),
                'avg_engagement': round(sum(rates) / len(rates), 2),
                'max_engagement': round(max(rates), 2)
            }

    return results

def analyze_cta_impact(posts):
    """Analyze CTA effectiveness"""

    with_cta = [p for p in posts if has_cta(p['caption'])]
    without_cta = [p for p in posts if not has_cta(p['caption'])]

    avg_with = sum(p.get('engagement_rate', 0) for p in with_cta) / len(with_cta) if with_cta else 0
    avg_without = sum(p.get('engagement_rate', 0) for p in without_cta) / len(without_cta) if without_cta else 0

    return {
        'with_cta': {
            'count': len(with_cta),
            'avg_engagement': round(avg_with, 2)
        },
        'without_cta': {
            'count': len(without_cta),
            'avg_engagement': round(avg_without, 2)
        },
        'difference': round(avg_with - avg_without, 2)
    }

def analyze_topic_themes(posts):
    """Identify top-performing topics"""

    topic_performance = {}

    for post in posts:
        keywords = extract_topic_keywords(post['caption'])
        engagement = post.get('engagement_rate', 0)

        for keyword in keywords:
            if keyword not in topic_performance:
                topic_performance[keyword] = []
            topic_performance[keyword].append(engagement)

    # Calculate average for each topic
    topic_averages = {}
    for topic, rates in topic_performance.items():
        if len(rates) >= 3:  # Only topics with 3+ mentions
            topic_averages[topic] = {
                'mentions': len(rates),
                'avg_engagement': round(sum(rates) / len(rates), 2)
            }

    # Sort by engagement
    sorted_topics = sorted(
        topic_averages.items(),
        key=lambda x: x[1]['avg_engagement'],
        reverse=True
    )

    return dict(sorted_topics[:10])

def generate_performance_report(posts):
    """Generate comprehensive performance report"""

    if not posts:
        return None

    # Sort by engagement rate
    sorted_posts = sorted(posts, key=lambda x: x.get('engagement_rate', 0), reverse=True)

    # Top performers
    top_10 = sorted_posts[:10]

    # Calculate overall metrics
    total_engagement = sum(p.get('engagement_rate', 0) for p in posts)
    avg_engagement = total_engagement / len(posts)

    report = {
        'generated_at': datetime.now().isoformat(),
        'total_posts_analyzed': len(posts),
        'overall_metrics': {
            'avg_engagement_rate': round(avg_engagement, 2),
            'avg_reach': int(sum(p.get('reach', 0) for p in posts) / len(posts)),
            'avg_likes': int(sum(p.get('likes', 0) for p in posts) / len(posts)),
            'avg_comments': int(sum(p.get('comments', 0) for p in posts) / len(posts)),
            'avg_saves': int(sum(p.get('saves', 0) for p in posts) / len(posts))
        },
        'top_10_performers': [
            {
                'caption_preview': p['caption'][:100].replace('\n', ' ') if p['caption'] else 'No caption',
                'engagement_rate': p['engagement_rate'],
                'hook': extract_hook(p['caption']),
                'line_count': count_lines(p['caption']),
                'has_cta': has_cta(p['caption']),
                'likes': p['likes'],
                'comments': p['comments'],
                'saves': p['saves'],
                'reach': p['reach']
            }
            for p in top_10
        ],
        'patterns': {
            'hook_analysis': analyze_hook_patterns(posts),
            'length_correlation': analyze_length_correlation(posts),
            'cta_impact': analyze_cta_impact(posts),
            'topic_themes': analyze_topic_themes(posts)
        }
    }

    return report

def print_report(report):
    """Print readable report"""

    if not report:
        return

    print("\n📊 INSTAGRAM PERFORMANCE ANALYSIS")
    print("=" * 70)

    # Overall metrics
    metrics = report['overall_metrics']
    print(f"\n📈 Overall Metrics ({report['total_posts_analyzed']} posts)")
    print(f"   Avg Engagement Rate: {metrics['avg_engagement_rate']}%")
    print(f"   Avg Reach: {metrics['avg_reach']:,}")
    print(f"   Avg Likes: {metrics['avg_likes']:,}")
    print(f"   Avg Comments: {metrics['avg_comments']:,}")
    print(f"   Avg Saves: {metrics['avg_saves']:,}")

    # Top performers
    print(f"\n🔥 Top 10 Performers")
    for i, post in enumerate(report['top_10_performers'], 1):
        print(f"\n{i}. Engagement: {post['engagement_rate']}% | Lines: {post['line_count']} | CTA: {post['has_cta']}")
        print(f"   Hook: {post['hook'][:80]}")
        print(f"   📊 {post['likes']} likes | {post['comments']} comments | {post['saves']} saves")

    # Hook patterns
    print(f"\n💡 Hook Patterns")
    hook_data = report['patterns']['hook_analysis']
    print(f"   Avg hook length: {hook_data['avg_hook_length']:.1f} words")
    print(f"   Common starters:")
    for starter, count in hook_data['common_starters'][:5]:
        print(f"     - '{starter}' ({count} times)")

    # Length correlation
    print(f"\n📏 Length vs Engagement")
    for bucket, data in report['patterns']['length_correlation'].items():
        print(f"   {bucket}: {data['avg_engagement']}% avg ({data['count']} posts)")

    # CTA impact
    print(f"\n🎯 CTA Impact")
    cta_data = report['patterns']['cta_impact']
    print(f"   With CTA: {cta_data['with_cta']['avg_engagement']}% ({cta_data['with_cta']['count']} posts)")
    print(f"   Without CTA: {cta_data['without_cta']['avg_engagement']}% ({cta_data['without_cta']['count']} posts)")
    print(f"   Difference: {cta_data['difference']:+.2f}%")

    # Top topics
    print(f"\n🎪 Top Topics by Engagement")
    for i, (topic, data) in enumerate(list(report['patterns']['topic_themes'].items())[:5], 1):
        print(f"   {i}. {topic}: {data['avg_engagement']}% ({data['mentions']} posts)")

def save_report(report):
    """Save report to JSON"""

    if not report:
        return

    output_file = '2-instagram/instagram-caption/outputs/performance_report.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Report saved to {output_file}")

if __name__ == "__main__":
    posts = load_posts()

    if posts:
        report = generate_performance_report(posts)
        print_report(report)
        save_report(report)
