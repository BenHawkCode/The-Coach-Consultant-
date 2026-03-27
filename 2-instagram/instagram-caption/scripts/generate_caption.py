#!/usr/bin/env python3
"""
Instagram Caption Generator
Creates captions matching Ben's voice with performance prediction
UPDATED: Now uses real scraped data from @benhawksworth_ (41 posts)
"""

import json
import sys
import csv
import argparse
from datetime import datetime
from pathlib import Path

# Ben's voice patterns
# Updated based on 41 posts performance analysis
BEN_NATURAL_PHRASES = [
    "You are not",
    "You think",
    "Do you genuinely still think",
    "I don't know who needs to hear this",
    "I don't really have the words",
    "You are NOT behind (yet!)",
    "Comment [WORD]",  # Highest engagement pattern (808 engagement)
    "Genuinely interested",
    "The truth is",
    "fuck comparing",  # Ben uses strong language
    "stop being a victim"
]

FORBIDDEN_PHRASES = [
    "Here's the thing",
    "Here's the reality",
    "Here's how",
    "Let's dive in",
    "In this comprehensive guide",
    "It's important to note",
    "At the end of the day",
    "In conclusion",
    "To summarise",
    "First and foremost",
    "Game changer",
    "Unlock",
    "Leverage",
    "Journey"
]

def load_performance_data():
    """Load performance data from CSV (41 posts analyzed)"""

    script_dir = Path(__file__).parent
    csv_file = script_dir.parent / "data" / "performance_data.csv"

    try:
        posts = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                posts.append({
                    'caption': row['caption'],
                    'engagement': int(row['engagement']),
                    'likes': int(row['likes']),
                    'comments': int(row['comments']),
                    'type': row['type'],
                    'url': row['url'],
                    'caption_length': int(row['caption_length']),
                    'video_views': int(row['video_views']) if row['video_views'] else 0
                })

        # Calculate average metrics
        total_engagement = sum(p['engagement'] for p in posts)
        avg_engagement = total_engagement / len(posts)

        # Sort by engagement
        posts.sort(key=lambda x: x['engagement'], reverse=True)

        return {
            'posts': posts,
            'total_posts': len(posts),
            'avg_engagement': avg_engagement,
            'top_10': posts[:10]
        }

    except FileNotFoundError:
        print("⚠️  Performance data not found. Run analyze_patterns.py first.")
        return None

def find_similar_top_post(topic, report):
    """Find top-performing post similar to topic"""

    if not report:
        return None

    topic_lower = topic.lower()
    topic_words = set(topic_lower.split())

    for post in report['top_10_performers']:
        caption_lower = post['caption_preview'].lower()
        caption_words = set(caption_lower.split())

        # Check for keyword overlap
        overlap = topic_words & caption_words
        if len(overlap) >= 1:
            return post

    # Return top performer if no match
    return report['top_10_performers'][0] if report['top_10_performers'] else None

def predict_engagement(caption, report):
    """Predict engagement based on patterns"""

    if not report:
        return {
            'rate': 0,
            'confidence': 'Low',
            'reasoning': 'No historical data'
        }

    # Factors
    line_count = len([l for l in caption.split('\n') if l.strip()])
    has_cta = 'thecoachconsultant.uk' in caption.lower()

    # Base prediction on average
    base_rate = report['overall_metrics']['avg_engagement_rate']

    # Adjust based on length
    length_data = report['patterns']['length_correlation']
    if line_count <= 8 and 'short (1-8 lines)' in length_data:
        length_factor = length_data['short (1-8 lines)']['avg_engagement'] / base_rate
    elif line_count <= 15 and 'medium (9-15 lines)' in length_data:
        length_factor = length_data['medium (9-15 lines)']['avg_engagement'] / base_rate
    elif 'long (16+ lines)' in length_data:
        length_factor = length_data['long (16+ lines)']['avg_engagement'] / base_rate
    else:
        length_factor = 1.0

    # Adjust for CTA
    cta_data = report['patterns']['cta_impact']
    cta_factor = 1.0
    if has_cta and cta_data['difference'] > 0:
        cta_factor = 1 + (cta_data['difference'] / base_rate)

    # Calculate prediction
    predicted_rate = round(base_rate * length_factor * cta_factor, 2)

    # Confidence based on data quality
    confidence = 'Medium'
    if report['total_posts_analyzed'] >= 30:
        confidence = 'High'
    elif report['total_posts_analyzed'] < 15:
        confidence = 'Low'

    return {
        'rate': predicted_rate,
        'confidence': confidence,
        'reasoning': f"Length factor: {length_factor:.2f}x | CTA factor: {cta_factor:.2f}x"
    }

def check_brand_voice_compliance(caption):
    """Check if caption follows brand voice rules"""

    issues = []
    caption_lower = caption.lower()

    # Check forbidden phrases
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in caption_lower:
            issues.append(f"❌ Contains forbidden phrase: '{phrase}'")

    # Check for dashes
    if ' - ' in caption or ' – ' in caption:
        issues.append("❌ Contains dashes (use line breaks instead)")

    # Check for emojis
    emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]'
    import re
    if re.search(emoji_pattern, caption):
        issues.append("❌ Contains emojis (avoid unless user requests)")

    # Check line count
    lines = len([l for l in caption.split('\n') if l.strip()])
    if lines > 20:
        issues.append(f"⚠️  Too long ({lines} lines, max 15-20)")

    # Check for headers
    if '#' in caption or caption.count('\n\n') > lines / 2:
        issues.append("⚠️  Possible headers or excessive line breaks")

    return issues

def generate_caption_structure(topic, report):
    """Generate caption following Ben's structure"""

    # This is a template - actual generation would use Claude API
    # For now, return structure guidance

    similar_post = find_similar_top_post(topic, report) if report else None

    structure = {
        'hook_options': [
            f"Right so {topic}",
            f"I see this all the time with {topic}",
            f"Sound familiar with {topic}",
            f"The problem with {topic}",
            f"What actually works for {topic}"
        ],
        'body_guidelines': [
            "Single short sentences",
            "One sentence per line",
            "No full stops overused",
            "Personal experience examples",
            "Direct, straight-talking tone",
            "No corporate jargon"
        ],
        'cta_template': "www.thecoachconsultant.uk",
        'optimal_length': "12-15 lines" if not report else "Based on analysis: 9-15 lines performs best",
        'similar_top_post': similar_post
    }

    return structure

def create_output(topic, caption, report):
    """Create formatted output with prediction"""

    prediction = predict_engagement(caption, report)
    similar_post = find_similar_top_post(topic, report)
    voice_issues = check_brand_voice_compliance(caption)

    output = []
    output.append("\n" + "=" * 70)
    output.append("📝 INSTAGRAM CAPTION GENERATED")
    output.append("=" * 70)

    # Performance prediction
    output.append("\n📊 PERFORMANCE PREDICTION")
    output.append(f"Estimated engagement rate: {prediction['rate']}%")
    if similar_post:
        output.append(f"Based on: {similar_post['caption_preview'][:60]}...")
        output.append(f"           (Top post: {similar_post['engagement_rate']}% engagement)")
    output.append(f"Confidence: {prediction['confidence']}")
    output.append(f"Reasoning: {prediction['reasoning']}")

    # Caption
    output.append("\n📝 CAPTION")
    output.append("-" * 70)
    output.append(caption)
    output.append("-" * 70)

    # Optimization notes
    output.append("\n🎯 OPTIMIZATION NOTES")
    line_count = len([l for l in caption.split('\n') if l.strip()])
    output.append(f"- Line count: {line_count} lines")
    output.append(f"- CTA included: {'Yes' if 'thecoachconsultant.uk' in caption.lower() else 'No'}")
    output.append(f"- Hook: {caption.split(chr(10))[0] if caption else 'N/A'}")

    if similar_post:
        output.append(f"- Similar top post: {similar_post['engagement_rate']}% engagement")

    # Voice compliance
    if voice_issues:
        output.append("\n⚠️  BRAND VOICE ISSUES")
        for issue in voice_issues:
            output.append(f"  {issue}")
    else:
        output.append("\n✅ Brand voice compliance: PASSED")

    return "\n".join(output)

def save_caption(topic, caption, output_text):
    """Save generated caption to file"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"2-instagram/instagram-caption/outputs/caption_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"TOPIC: {topic}\n")
        f.write(f"GENERATED: {datetime.now().isoformat()}\n\n")
        f.write(output_text)

    print(f"\n💾 Saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Generate Instagram captions')
    parser.add_argument('--topic', type=str, required=True, help='Caption topic')
    parser.add_argument('--variants', type=int, default=1, help='Number of variants to generate')

    args = parser.parse_args()

    # Load performance data
    report = load_performance_report()

    print(f"\n🎯 Generating caption for: {args.topic}")

    if args.variants > 1:
        print(f"Creating {args.variants} variants for A/B testing")

    # For now, show structure guidance
    # In production, this would call Claude API with context
    structure = generate_caption_structure(args.topic, report)

    print("\n📋 CAPTION STRUCTURE GUIDANCE")
    print("=" * 70)
    print(f"\n🎣 Hook Options:")
    for hook in structure['hook_options']:
        print(f"   - {hook}")

    print(f"\n📝 Body Guidelines:")
    for guideline in structure['body_guidelines']:
        print(f"   - {guideline}")

    print(f"\n🎯 CTA: {structure['cta_template']}")
    print(f"\n📏 Optimal Length: {structure['optimal_length']}")

    if structure['similar_top_post']:
        post = structure['similar_top_post']
        print(f"\n🔥 Similar Top Post ({post['engagement_rate']}% engagement):")
        print(f"   Hook: {post['hook']}")
        print(f"   Lines: {post['line_count']}")
        print(f"   CTA: {post['has_cta']}")

    print("\n" + "=" * 70)
    print("📌 NOTE: Actual caption generation requires Claude API integration")
    print("Use this structure guidance to write the caption manually, or")
    print("integrate with Claude Code's generation capabilities.")
    print("=" * 70)

if __name__ == "__main__":
    main()
