# The Coach Consultant - AI Content Generation Skills

Channel-organised content generation skills for The Coach Consultant.

**Navigation:** Each channel contains tested, production-ready skills that match Ben's authentic voice.

---

## 1. Meta Ads

Facebook and Instagram paid advertising content.

- **[Meta Ad Copy](1-meta-ads/meta-ad-copy/)** - Generate performance-optimised Meta ad copy based on historical campaign data with real-time API analysis
- **[Meta Ad Competitor](1-meta-ads/meta-ad-competitor/)** - ⏳ **Awaiting API Approval** - Analyse competitor Meta ads (Alex Hormozi, Dan Martell, etc.), extract winning hooks, generate hybrid variations in Ben's voice
- **[Meta Page Spy](1-meta-ads/meta-page-spy/)** ✅ **READY** - Spy on any Facebook page: organic posts + paid ads combined intelligence report. Posting frequency, content types, engagement metrics, hook/CTA patterns, posting schedule, offer positioning.

---

## 2. Instagram

Organic Instagram content (captions, stories, reels).

- **[Instagram Page Spy](2-instagram/instagram-page-spy/)** ✅ **READY** - Spy on any Instagram profile: content breakdown, engagement rates, top posts, hook/CTA patterns, posting schedule, caption analysis, hashtag strategy.
- **[Instagram Caption](2-instagram/instagram-caption/)** ✅ **DATA LOADED** - Generate Instagram captions matching Ben's exact voice. 41 posts analyzed, top hooks identified (808 engagement!), proven patterns documented. Carousel posts perform best (161 avg). Use 800+ character captions for max engagement.
- **[IG Competitor Analysis](2-instagram/ig-competitor-analysis/)** ✅ **DATA LOADED** - 31 verified profiles, 847 posts analysed. Story hooks get 70K avg engagement, Carousel posts dominate (37K avg), 78% posts have no CTA. Cross-competitor hook patterns, format performance, CTA strategies, top 30 hooks swipe file.

---

## 3. YouTube

Long-form video scripts and supporting content.

- **[Thumbnail Generator](3-youtube/thumbnail-generator/)** ✅ **READY** — Local Streamlit app that generates YouTube thumbnails via Gemini 3.1 Flash Image Preview. Three modes: Clone Reference (copy a thumbnail's style), Preset Style (Hormozi / MrBeast / Podcast / Minimal / Alex Hormozi Black), Hybrid (custom overrides). Seeded face library, generation history, metadata sidecars. Run: `cd 3-youtube/thumbnail-generator && streamlit run app.py`.

---

## 4. Emails

Email campaigns, newsletters, and automation sequences.

- **[Email Campaign Generation](4-emails/email-campaign-skill/)** ✅ **DATA LOADED** - Generate email campaigns with 9.6/10 voice accuracy. 471 emails analyzed (353 unique subjects). Proven patterns: #theGAPyoumiss (16 sends), BadBizAdvice (23 sends). Systematic voice verification enforced. Auto-triggers for all email generation tasks.
- **[Email Competitor Spy](4-emails/email-competitor-spy/)** ✅ **READY** - Analyse competitor email newsletters (10 senders tracked via Antonio's pipeline). Extract hook patterns, subject line formulas, CTA strategies, tone profiles, and offer positioning. Feeds directly into email campaign generation.

---

## 5. LinkedIn

Professional networking content and thought leadership.

- Coming soon...

---

## 6. Website/SEO

Website copy, landing pages, and SEO-optimised content.

- Coming soon...

---

## Optimisation Skills

Tools for optimising the AI content generation system itself.

- **[Token Optimisation](optimisation-skills/token-optimisation/)** ✅ **READY** - Audit CLAUDE.md and workspace for token waste. Identifies duplicated content, verbose patterns, oversized files. Interactive 3-5 question discovery, then generates optimised versions. Current CLAUDE.md: ~3,467 tokens per conversation.

---

## How to Use These Skills

### 1. Via Claude Code CLI

```bash
# Invoke a skill by name
/meta-ad-copy

# Or via natural language
"Generate Meta ad copy for my new coaching offer"
```

### 2. Each Skill Folder Contains

- `skill.md` - Full documentation and instructions for Claude
- `README.md` - Human-readable overview and setup guide
- `outputs/` - Generated content examples
- Scripts/tools (Python, Bash) for API integration where applicable

### 3. Brand Voice Integration

All skills automatically reference:
- [CLAUDE.md](CLAUDE.md) for brand voice rules
- [docs/Ben-Claude-Projects-Instructions.txt](docs/Ben-Claude-Projects-Instructions.txt) for channel-specific formatting
- [docs/deep-dive/](docs/deep-dive/) for deep brand context

---

## Skill Development Status

| Channel | Skills Available | Status |
|---------|------------------|--------|
| 1. Meta Ads | 2 | ✅ Live |
| 2. Instagram | 2 | ✅ Live |
| 3. YouTube | 0 | 🚧 Planning |
| 4. Emails | 2 | ✅ Live |
| 5. LinkedIn | 0 | 🚧 Planning |
| 6. Website/SEO | 0 | 🚧 Planning |

---

## Quick Start

1. **Read the brand guidelines:** [CLAUDE.md](CLAUDE.md)
2. **Choose your channel** from 1-6 above
3. **Navigate to the skill folder** you need
4. **Invoke via Claude Code** or follow the skill's README

---

## Notes for Ben

- **jay-skills/** folder remains separate (developer utilities, not client-facing content)
- All content skills organised by channel (1-6) for easy Google Drive sync
- Each skill folder is self-contained and portable
- British English throughout (organisation, optimise, behaviour)

---

**Last Updated:** 2026-04-07
**Maintained By:** Claude Code + Jay (developer utilities)
