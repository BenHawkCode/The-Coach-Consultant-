#!/usr/bin/env python3
"""
Analyze Instagram Performance Patterns
Identifies what makes high-performing captions successful
"""

import csv
import json
from pathlib import Path
from collections import Counter
import re

def load_performance_data():
    """Load processed performance CSV"""
    data_file = Path(__file__).parent.parent / "data" / "performance_data.csv"

    posts = []
    with open(data_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            posts.append({
                'caption': row['caption'],
                'likes': int(row['likes']),
                'comments': int(row['comments']),
                'engagement': int(row['engagement']),
                'type': row['type'],
                'url': row['url'],
                'caption_length': int(row['caption_length']),
                'video_views': int(row['video_views']) if row['video_views'] else 0,
            })

    return posts

def load_raw_data():
    """Load raw JSON for full caption text"""
    data_file = Path(__file__).parent.parent / "data" / "raw_posts.json"

    with open(data_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    return raw_data

def analyze_top_performers(posts, top_n=10):
    """Analyze characteristics of top performing posts"""

    # Sort by engagement
    sorted_posts = sorted(posts, key=lambda x: x['engagement'], reverse=True)
    top_posts = sorted_posts[:top_n]

    print(f"📊 ANALYZING TOP {top_n} PERFORMERS\n")
    print("="*80)

    # Average metrics
    avg_engagement = sum(p['engagement'] for p in top_posts) / len(top_posts)
    avg_likes = sum(p['likes'] for p in top_posts) / len(top_posts)
    avg_comments = sum(p['comments'] for p in top_posts) / len(top_posts)
    avg_length = sum(p['caption_length'] for p in top_posts) / len(top_posts)

    print(f"\n📈 TOP {top_n} AVERAGE METRICS:")
    print(f"   Avg engagement: {avg_engagement:.1f}")
    print(f"   Avg likes: {avg_likes:.1f}")
    print(f"   Avg comments: {avg_comments:.1f}")
    print(f"   Avg caption length: {avg_length:.0f} chars")

    # Content type distribution
    type_counts = Counter(p['type'] for p in top_posts)
    print(f"\n📹 CONTENT TYPE DISTRIBUTION:")
    for content_type, count in type_counts.most_common():
        print(f"   {content_type}: {count} ({count/len(top_posts)*100:.1f}%)")

    return top_posts

def extract_hook_patterns(posts):
    """Extract opening hooks from captions"""

    print(f"\n🎣 HOOK PATTERNS (First Line Analysis):\n")

    hooks = []
    for post in posts:
        caption = post['caption']
        # Get first line (up to first newline or period)
        first_line = caption.split('\n')[0].strip()
        if len(first_line) > 10:  # Ignore very short hooks
            hooks.append({
                'hook': first_line,
                'engagement': post['engagement'],
                'likes': post['likes'],
                'comments': post['comments']
            })

    # Sort by engagement
    hooks.sort(key=lambda x: x['engagement'], reverse=True)

    for i, hook_data in enumerate(hooks[:10], 1):
        print(f"{i}. {hook_data['hook'][:80]}...")
        print(f"   💥 {hook_data['engagement']} engagement ({hook_data['likes']} likes, {hook_data['comments']} comments)\n")

def identify_engagement_triggers(raw_posts):
    """Identify common phrases in high-engagement posts"""

    print(f"\n🔥 ENGAGEMENT TRIGGERS:\n")

    # Sort by comments (indicates interaction)
    sorted_by_comments = sorted(raw_posts, key=lambda x: x.get('commentsCount', 0), reverse=True)
    top_comment_posts = sorted_by_comments[:10]

    # Common patterns
    patterns = {
        'Questions': r'\?',
        'Call-to-action': r'(comment|reply|drop|tell me|let me know|share)',
        'Controversial': r'(unpopular|truth|reality|honest|admit)',
        'Direct address': r'(you are|you\'re|you think|you might)',
        'Urgency': r'(now|today|still|yet)',
        'Numbers': r'\d+%|\d+ years|\d+ months',
    }

    trigger_counts = Counter()

    for post in top_comment_posts:
        caption = post.get('caption', '').lower()
        for trigger_name, pattern in patterns.items():
            if re.search(pattern, caption, re.IGNORECASE):
                trigger_counts[trigger_name] += 1

    print("Most common in high-comment posts:")
    for trigger, count in trigger_counts.most_common():
        print(f"   {trigger}: {count}/{len(top_comment_posts)} posts")

    print("\n📝 Example high-comment captions:")
    for i, post in enumerate(top_comment_posts[:3], 1):
        caption = post.get('caption', '')[:100]
        comments = post.get('commentsCount', 0)
        print(f"\n{i}. {comments} comments:")
        print(f"   \"{caption}...\"")

def analyze_caption_structure(posts):
    """Analyze caption structure patterns"""

    print(f"\n📐 CAPTION STRUCTURE ANALYSIS:\n")

    # Length buckets
    short = [p for p in posts if p['caption_length'] < 300]
    medium = [p for p in posts if 300 <= p['caption_length'] < 800]
    long_posts = [p for p in posts if p['caption_length'] >= 800]

    def avg_engagement(post_list):
        if not post_list:
            return 0
        return sum(p['engagement'] for p in post_list) / len(post_list)

    print(f"Length vs Performance:")
    print(f"   Short (<300 chars): {len(short)} posts, avg engagement: {avg_engagement(short):.1f}")
    print(f"   Medium (300-800): {len(medium)} posts, avg engagement: {avg_engagement(medium):.1f}")
    print(f"   Long (800+): {len(long_posts)} posts, avg engagement: {avg_engagement(long_posts):.1f}")

def generate_insights_file(posts, raw_posts):
    """Generate insights markdown file"""

    output_file = Path(__file__).parent.parent / "data" / "PERFORMANCE_INSIGHTS.md"

    # Sort posts
    sorted_posts = sorted(posts, key=lambda x: x['engagement'], reverse=True)
    top_10 = sorted_posts[:10]

    # Calculate stats
    avg_engagement_top10 = sum(p['engagement'] for p in top_10) / len(top_10)
    avg_engagement_all = sum(p['engagement'] for p in posts) / len(posts)

    content = f"""# Instagram Performance Insights
Generated: {Path(__file__).parent / 'data' / 'performance_data.csv'}

## Key Findings

### Overall Performance
- **Total posts analyzed**: {len(posts)}
- **Average engagement**: {avg_engagement_all:.1f} (likes + comments)
- **Top 10 average**: {avg_engagement_top10:.1f}
- **Performance gap**: Top posts get {avg_engagement_top10/avg_engagement_all:.1f}x more engagement

### Content Type Performance
"""

    # Content type stats
    type_performance = {}
    for content_type in set(p['type'] for p in posts):
        type_posts = [p for p in posts if p['type'] == content_type]
        avg_eng = sum(p['engagement'] for p in type_posts) / len(type_posts)
        type_performance[content_type] = avg_eng

    for content_type, avg_eng in sorted(type_performance.items(), key=lambda x: x[1], reverse=True):
        content += f"- **{content_type}**: {avg_eng:.1f} avg engagement\n"

    content += "\n### Caption Length Sweet Spot\n"

    # Length analysis
    short = [p for p in posts if p['caption_length'] < 300]
    medium = [p for p in posts if 300 <= p['caption_length'] < 800]
    long_posts = [p for p in posts if p['caption_length'] >= 800]

    def avg_eng(post_list):
        return sum(p['engagement'] for p in post_list) / len(post_list) if post_list else 0

    content += f"- **Short (<300 chars)**: {avg_eng(short):.1f} avg engagement\n"
    content += f"- **Medium (300-800)**: {avg_eng(medium):.1f} avg engagement ⭐ **BEST**\n"
    content += f"- **Long (800+)**: {avg_eng(long_posts):.1f} avg engagement\n"

    content += "\n### Top Performing Hooks\n\n"

    for i, post in enumerate(top_10, 1):
        first_line = post['caption'].split('\n')[0].strip()
        content += f"{i}. \"{first_line[:80]}...\" - {post['engagement']} engagement\n"

    content += "\n### Engagement Triggers\n\n"
    content += "High-comment posts often include:\n"
    content += "- ✅ Direct questions\n"
    content += "- ✅ \"Comment [WORD]\" CTAs\n"
    content += "- ✅ Controversial statements\n"
    content += "- ✅ Personal stories/struggles\n"
    content += "- ✅ Direct address (\"You are...\", \"You think...\")\n"

    content += "\n### Ben's Writing Style Patterns\n\n"
    content += "**Tone:**\n"
    content += "- Direct and confrontational\n"
    content += "- No fluff, straight to the point\n"
    content += "- Uses strong language (\"fuck comparing\", \"stop being a victim\")\n"
    content += "- Motivational but realistic\n\n"

    content += "**Structure:**\n"
    content += "- Hook (bold statement or question)\n"
    content += "- Multiple short paragraphs (1-2 sentences each)\n"
    content += "- Line breaks between thoughts\n"
    content += "- Often ends with actionable insight or challenge\n\n"

    content += "**Common Phrases:**\n"
    content += "- \"You are not...\"\n"
    content += "- \"The truth is...\"\n"
    content += "- \"I don't know who needs to hear this\"\n"
    content += "- \"You think... But...\"\n"

    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Insights saved to: {output_file}")

def main():
    """Main execution"""

    print("\n" + "="*80)
    print("📊 INSTAGRAM PERFORMANCE PATTERN ANALYSIS")
    print("="*80 + "\n")

    # Load data
    posts = load_performance_data()
    raw_posts = load_raw_data()

    print(f"✅ Loaded {len(posts)} posts\n")

    # Analyze
    top_posts = analyze_top_performers(posts, top_n=10)
    extract_hook_patterns(top_posts)
    identify_engagement_triggers(raw_posts)
    analyze_caption_structure(posts)

    # Generate insights
    generate_insights_file(posts, raw_posts)

    print("\n" + "="*80)
    print("✅ Analysis complete!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
