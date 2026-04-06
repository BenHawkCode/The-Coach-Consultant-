# Instagram Caption Generator - Quick Start

**⚡ 2 Minute Setup Guide** (Performance data already loaded!)

## ✅ Skip Steps 1-2: Data Already Loaded!

**Good news:** We've already scraped and analyzed 41 posts from @benhawksworth_!

You can **skip Meta API setup** and start using the performance insights immediately.

## Step 1: Review Performance Insights (1 min)

```bash
cd "2-instagram/instagram-caption"

# See what's working
cat data/PERFORMANCE_INSIGHTS.md

# Run analysis
python3 scripts/analyze_patterns.py
```

**You'll see:**
- ✅ Top 10 performing posts (268 avg engagement)
- ✅ Best hook patterns ("Comment PROJECTS" = 808 engagement!)
- ✅ Optimal caption length (800+ chars = best)
- ✅ Engagement triggers (direct questions, urgency, CTAs)
- ✅ Ben's authentic voice patterns

## Step 2: Generate Caption Structure (1 min)

```bash
# Get caption structure guidance
python3 scripts/generate_caption.py --topic "your topic here"
```

**Output includes:**
- 🎣 Proven hook patterns from top posts
- 📝 Ben's voice guidelines (from real data)
- 📊 Engagement prediction
- ✅ Structure based on 268-engagement posts

## Example Output

```
📊 PERFORMANCE PREDICTION
Estimated engagement: 150-200 (based on proven patterns)
Best hook type: "Comment [WORD]" CTA or Direct Question

🎣 PROVEN HOOK PATTERNS (Use One):
1. "Comment PROJECTS" style - 808 engagement 🏆
2. "You are NOT behind (yet!)" - 198 engagement
3. "Do you genuinely still think..." - 204 engagement
4. "I don't really have the words..." - 673 engagement

📝 BEN'S AUTHENTIC VOICE (From Real Data):
✅ Direct address: "You are...", "You think..."
✅ Confrontational: "Do you genuinely still think..."
✅ Personal stories: "I don't really have the words..."
✅ Strong language: "fuck comparing", "stop being a victim"
✅ Short paragraphs with line breaks

STRUCTURE:
1. Hook (use proven pattern above)
2. Problem statement ("You think... But...")
3. Personal context/story
4. Solution/shift
5. CTA (if relevant)

LENGTH: 800+ characters (proven best - not 15-20 lines!)
```

## What's Already Available

✅ **Performance data loaded** - 41 posts analyzed
✅ **Pattern analysis complete** - Top hooks identified
✅ **Engagement insights** - 2.5x performance gap found
✅ **Voice patterns documented** - Real phrases from Ben's posts
✅ **Scripts ready** - analyze_patterns.py works

## Quick Reference

### Top Performing Hooks (Copy These!)

1. **"Comment [WORD]"** - 808 engagement (681 comments!)
2. **"I don't really have the words..."** - 673 engagement
3. **"You are NOT behind (yet!)"** - 198 engagement
4. **"Do you genuinely still think..."** - 204 engagement

### Engagement Triggers (Use These!)

- ✅ Direct questions
- ✅ "Comment [WORD]" CTAs
- ✅ Controversial statements
- ✅ Personal stories/struggles
- ✅ Direct address ("You are...", "You think...")
- ✅ Urgency words ("NOT", "yet!", "still")

### Content Type Performance

1. **Carousel** - 161 avg engagement ⭐ BEST
2. **Video** - 74 avg engagement
3. **Image** - 67 avg engagement

### Caption Length Performance

1. **Long (800+)** - 219 avg engagement ⭐ BEST
2. **Short (<300)** - 76 avg engagement
3. **Medium (300-800)** - 69 avg engagement

## Optional: Meta API Setup (For Auto-Refresh)

If you want live data updates, set up Meta API:

```bash
# Copy template
cp .env.example .env

# Add credentials
echo "META_ACCESS_TOKEN=your_token" >> .env
echo "INSTAGRAM_BUSINESS_ID=your_id" >> .env

# Refresh data
python3 scripts/fetch_posts.py  # (Not built yet)
```

**But this is optional!** Current data is recent (March 24, 2026) and comprehensive.

## Pro Tips

1. **Use proven hooks** - Don't reinvent, copy what works (808 engagement!)
2. **Write longer** - 800+ characters outperform short captions
3. **Carousels win** - 161 avg engagement vs 74 for videos
4. **Direct questions work** - "Do you...", "Are you..."
5. **Strong language OK** - Ben uses "fuck comparing", be authentic

## Example Caption Using Real Data

**Topic:** Client onboarding automation

**Hook (from top performer):**
```
You are NOT behind on client onboarding

Yet

But you will be if you keep doing it manually
```

**Body (Ben's style):**
```
I see this constantly

Business owners spending 3 hours per client
Setting up systems
Sending welcome emails
Scheduling calls

Sound familiar

The problem is not your process
It's that you're still doing it by hand

What actually works is automation

But not the robotic kind
The kind that feels personal

From that point
You're gonna save 10 hours a week
And give clients a better experience

Remember
The shift is simple
But most people won't do it

www.thecoachconsultant.uk
```

**Length:** ~650 characters (good, but could be longer for max engagement!)
**Predicted engagement:** ~120-150 (above average)

## Next Steps

1. Review `data/PERFORMANCE_INSIGHTS.md`
2. Run `python3 scripts/analyze_patterns.py`
3. Use proven hooks in your captions
4. Write 800+ character captions (not short!)
5. Test carousels over videos/images

---

**Full docs:** See README.md
**Skill guide:** See SKILL.md
**Performance insights:** See data/PERFORMANCE_INSIGHTS.md
**Current status:** See STATUS.md
