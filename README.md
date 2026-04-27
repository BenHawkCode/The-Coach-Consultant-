# The Coach Consultant - AI Automation System

## Overview

AI automation system built exclusively within the Claude ecosystem to scale The Coach Consultant's marketing, content, and operations.

**Built with:** Claude, Claude Projects, Claude Code, Claude CoWork

## What This System Does

### Content Generation
Automated, brand-aligned content creation for marketing channels:
- **Meta Ads**: Performance-optimized ad copy (2 skills live)
- **Instagram**: Captions, carousels, and stories (1 skill live, 41 posts analyzed)
- **Email Campaigns**: Nurture sequences and broadcasts ✨ **NEW: 1 skill live, 471 emails analyzed**
- **LinkedIn**: Professional posts and articles (coming soon)
- **YouTube**: Video scripts and descriptions (coming soon)
- **Podcasts**: Show scripts and episode outlines (coming soon)

### Prompt Vault
Categorized, ready-to-use prompts with sample outputs:
- Marketing campaigns (Meta ads, social media, email)
- Operational workflows
- Content creation
- Performance reporting

## Project Structure

```
The Coach Consultant/
├── 1-meta-ads/               # Meta Ads content generation skills
├── 2-instagram/              # Instagram content generation skills
├── 3-youtube/                # YouTube content generation skills
├── 4-emails/                 # Email content generation skills
├── 5-linkedin/               # LinkedIn content generation skills
├── 6-website-seo/            # Website/SEO content generation skills
├── agents/                   # Multi-agent orchestration (future)
├── prompts/                  # Prompt vault & examples
├── docs/                     # Documentation and brand context
├── jay-skills/               # Developer utilities (internal use)
├── CLAUDE.md                 # Brand context and AI instructions
├── README.md                 # This file (project overview)
└── SKILLS-README.md          # Complete skills catalog by channel
```

**Key Files:**
- **[CLAUDE.md](CLAUDE.md)** - Brand voice rules and AI instructions for content generation
- **[SKILLS-README.md](SKILLS-README.md)** - Complete catalog of all available skills organised by channel (1-6)

## Getting Started

### Prerequisites
- Claude Code installed
- GitHub access to this repository
- Meta Business Manager API access (for ad performance data)

### Initial Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/TCC58/the-coach-consultant.git
   cd "The Coach Consultant"
   ```

2. **Review brand context**
   - Read [CLAUDE.md](CLAUDE.md) for brand voice, tone, and guidelines
   - Review [docs/Ben-Claude-Projects-Instructions.txt](docs/Ben-Claude-Projects-Instructions.txt) for channel-specific rules
   - Explore [docs/deep-dive/](docs/deep-dive/) for deep brand voice samples

3. **Load skills into Claude Code**
   - Skills are organised by channel (1-meta-ads, 2-instagram, etc.)
   - See [SKILLS-README.md](SKILLS-README.md) for full documentation
   - Each skill has documentation and usage examples

4. **Configure environment**
   - Add Meta API credentials to `.env` file (if needed)
   - Ensure all required access tokens are configured

5. **Test the system**
   - Try generating sample content using available skills
   - Review output for brand alignment
   - Check `/prompts/marketing/` directory for example prompts and outputs

### Usage

**Generate Meta Ad Copy:**
```
Use the Meta Ad Copy skill with:
- Target audience segment
- Campaign objective
- Key benefits to highlight
```

Generated content samples with prompts are saved in the `/prompts/` directory (organised by category).

See [SKILLS-README.md](SKILLS-README.md) for a complete list of available skills organised by channel.

**Access Other Content Skills:**
- **Instagram:** Captions and carousels (✅ live, data-driven)
- **Email Campaigns:** Nurture sequences ✨ **NEW: 9.6/10 voice accuracy, 353 proven subject lines**
- **LinkedIn:** Professional posts (🚧 coming soon)
- **YouTube:** Video scripts (🚧 coming soon)
- **Podcast:** Episode scripts (🚧 coming soon)

Each skill includes documentation, usage examples, and sample outputs.

### Latest: Email Campaign Skill (2026-03-24)

**What's new:**
- 471 emails analyzed from GHL (23 months of data)
- 353 unique subject lines documented
- Proven patterns: #theGAPyoumiss (16x), BadBizAdvice (23x)
- Systematic voice verification (9.6/10 accuracy)
- Zero AI phrases enforced
- Auto-triggers for all email generation

**Campaigns ready:**
- A) Free Consult Call Claim Nurture
- B) No Show Nurture
- C) Not Yet Ready (long-term)
- D) Booking Requested Reply
- E) Appointment Reminders

See [4-emails/README.md](4-emails/README.md) for full documentation.

## Team

**The Coach Consultant:**
- Rob Sturman - Chief Operating Officer (Primary Contact)
- Ben Mahmoud - Sales Director & Paid Ads (Primary Contact)
- Beth Rendell - Client Success Director
- Alex Whitehead - Web Development & Graphics
- Charlie Munns - Success Coach
- Drew McNeill - Success Coach

**Automation Partners:**
- Dual Synergy AI - AI automation system development and support

## Important Links

- **Website:** https://thecoachconsultant.uk/
- **Brand Guidelines:** See [CLAUDE.md](CLAUDE.md)
- **Documentation:** [docs/](docs/)

## Updates & Maintenance

This system is actively maintained and updated based on:
- Performance data from campaigns
- New channel requirements
- Team feedback
- Market trends

For questions or support, contact your AI automation team.

---

## Related Repositories

The BenHawkCode account is organised into three sections via GitHub topics. Filter the account by topic to see each section.

### TCC — `topic:tcc`
The Coach Consultant brand work — content automations, lead magnets, products, internal tooling.

| Repo | Purpose |
|---|---|
| [The-Coach-Consultant-](https://github.com/BenHawkCode/The-Coach-Consultant-) | This repo — content engine and skill catalogue (hub) |
| [tcc-presentation-creator](https://github.com/BenHawkCode/tcc-presentation-creator) | Design system, icon library, carousel rendering |
| [tcc-meta-ads-daily-brief](https://github.com/BenHawkCode/tcc-meta-ads-daily-brief) | Daily Meta Ads brief automation, GitHub Actions cron 06:00 UTC |
| [tcc-cowork-system](https://github.com/BenHawkCode/tcc-cowork-system) | Cowork product — assessment, functionality list, SOPs |
| [tcc-client-pack](https://github.com/BenHawkCode/tcc-client-pack) | Sellable resource pack for clients |
| [tcc-projects-guide](https://github.com/BenHawkCode/tcc-projects-guide) | Smart Scaling System SOP |
| [tcc-accelerator-roi](https://github.com/BenHawkCode/tcc-accelerator-roi) | ROI assessment lead magnet |
| [tcc-recipe-image-generator](https://github.com/BenHawkCode/tcc-recipe-image-generator) | Image generation utility |
| [claude-code-projects](https://github.com/BenHawkCode/claude-code-projects) | Stale backup — early Brand Assets / Content / Client Work folders, kept inactive |

### Titan Clients — `topic:titan-clients`
Per-client deliverables for Titan coaching clients. Index lives at [titan-clients](https://github.com/BenHawkCode/titan-clients).

### Live Links — `topic:live-link`
Hostable HTML pages — landing pages, decks, scorecards, interactive tools. Index lives at [live-links](https://github.com/BenHawkCode/live-links).
