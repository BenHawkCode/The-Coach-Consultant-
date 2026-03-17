s# The Coach Consultant - AI Automation System

## Overview

AI automation system built exclusively within the Claude ecosystem to scale The Coach Consultant's marketing, content, and operations.

**Built with:** Claude, Claude Projects, Claude Code, Claude CoWork

## What This System Does

### Content Generation
Automated, brand-aligned content creation for marketing channels:
- **Meta Ads**: Performance-optimized ad copy
- **Instagram**: Captions, carousels, and stories
- **Email Campaigns**: Nurture sequences and broadcasts
- **LinkedIn**: Professional posts and articles
- **YouTube**: Video scripts and descriptions
- **Podcasts**: Show scripts and episode outlines

### Prompt Vault
Categorized, ready-to-use prompts with sample outputs:
- Marketing campaigns (Meta ads, social media, email)
- Operational workflows
- Content creation
- Performance reporting

## Project Structure

```
The Coach Consultant/
├── CLAUDE.md                 # Brand context and AI instructions
├── README.md                 # This file
├── skills/                   # Content generation skills
│   └── meta-ad-copy/         # Meta ad copy generator
├── agents/                   # Multi-agent orchestration (future)
├── prompts/                  # Prompt vault & examples
│   ├── marketing/            # Marketing prompts + sample outputs
│   ├── operations/
│   ├── content/
│   └── reporting/
└── docs/                     # Documentation and brand context
    ├── deep-dive/            # Deep brand voice samples & frameworks
    └── Ben-Claude-Projects-Instructions.txt
```

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
   - Skills are located in `/skills/` directory
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

Generated content samples with prompts are saved in the `/prompts/` directory (organized by category).

**Access Other Content Skills:**
- Instagram captions and carousels
- Email campaign sequences
- LinkedIn professional posts
- YouTube video scripts
- Podcast episode scripts

Each skill includes documentation, usage examples, and sample outputs.

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
