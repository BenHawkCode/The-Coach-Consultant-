# The Coach Consultant - Setup Guide

Complete setup instructions for The Coach Consultant AI automation system.

---

## What You'll Need

- **GitHub Token:** Provided by development team
- **Claude Account:** Sign up at https://claude.ai (if you don't have one)
- **Choose one platform:**
  - Claude Code CLI (recommended for power users)
  - VS Code with Claude extension (recommended for most users)
  - Claude CoWork (for team collaboration)

---

## Option 1: Claude Code (Recommended for Power Users)

### Step 1: Install Claude Code

**macOS/Linux:**
```bash
curl -fsSL https://claude.ai/install.sh | sh
```

**Windows:**
Download from: https://claude.ai/download

### Step 2: Authenticate

```bash
claude auth
```

Follow the prompts to sign in with your Claude account (claude.ai).

### Step 3: Clone the Repository

```bash
git clone https://github.com/TCC58/the-coach-consultant.git
cd "The Coach Consultant"
```

**If prompted for GitHub credentials:**
- **Username:** `TCC58`
- **Password:** Use the GitHub token provided by the development team

### Step 4: Start Claude Code

```bash
claude code
```

This will:
- ✅ Auto-load `CLAUDE.md` (brand context and instructions)
- ✅ Make all skills available from `/skills/` directory
- ✅ Load brand voice documentation from `/docs/`

### Step 5: Test the System

Try generating Meta ad copy:

```
Generate Meta ad copy for:
- Target audience: Solo coaches scaling to £100K
- Campaign: Free masterclass sign-ups
- Benefits: AI automation, time freedom, proven results
```

Claude will automatically use the Meta Ad Copy skill and Ben's voice.

---

## Option 2: VS Code with Claude Extension (Recommended for Most Users)

### Step 1: Install VS Code

Download from: https://code.visualstudio.com/

### Step 2: Install Claude Extension

1. Open VS Code
2. Click Extensions icon (left sidebar) or press:
   - **Mac:** `⌘ + Shift + X`
   - **Windows:** `Ctrl + Shift + X`
3. Search for **"Claude"** or **"Anthropic"**
4. Click **"Install"**

### Step 3: Authenticate Claude Extension

1. Open Command Palette:
   - **Mac:** `⌘ + Shift + P`
   - **Windows:** `Ctrl + Shift + P`
2. Type: **"Claude: Sign In"**
3. Follow the authentication flow (sign in to claude.ai)

### Step 4: Clone the Repository

**Option A: Using VS Code Terminal**

1. Open Terminal in VS Code: `` Ctrl + ` `` (backtick)
2. Run:
```bash
git clone https://github.com/TCC58/the-coach-consultant.git
cd "The Coach Consultant"
```

**Option B: Using VS Code UI**

1. View → Command Palette (`⌘/Ctrl + Shift + P`)
2. Type: **"Git: Clone"**
3. Paste: `https://github.com/TCC58/the-coach-consultant.git`
4. Choose a folder location
5. Click **"Open"** when prompted

**If prompted for GitHub credentials:**
- **Username:** `TCC58`
- **Password:** Use the GitHub token provided

### Step 5: Open Project

1. File → Open Folder
2. Select **"The Coach Consultant"** folder
3. The `CLAUDE.md` file will auto-load (brand context + skills)

### Step 6: Test the System

1. Open the Claude panel (usually on the right sidebar)
2. Try generating content:

```
Generate Meta ad copy for:
- Target audience: Solo coaches scaling to £100K
- Campaign: Free masterclass sign-ups
- Benefits: AI automation, time freedom, proven results
```

Claude will use the Meta Ad Copy Generator skill automatically.

---

## Option 3: Claude CoWork (Team Collaboration)

### Step 1: Access Claude CoWork

Go to: https://claude.ai/cowork

### Step 2: Create Team Workspace

1. Click **"New Workspace"**
2. Name it: **"The Coach Consultant"**
3. Invite team members:
   - Rob Sturman (COO)
   - Ben Mahmoud (Sales Director)
   - Beth Rendell (Client Success)
   - Others as needed

### Step 3: Import Project Context

Upload these files to the workspace:

1. **`CLAUDE.md`** - Core brand context (REQUIRED)
2. **`docs/Ben-Claude-Projects-Instructions.txt`** - Channel rules
3. **`docs/deep-dive/`** folder - Voice samples
4. **`prompts/marketing/`** - Example prompts

### Step 4: Load Skills

For each skill in `/skills/` (e.g., `meta-ad-copy`):

1. Open the skill folder
2. Copy the skill content
3. Create a new **"Skill"** in Claude CoWork
4. Paste the content
5. Name it (e.g., "Meta Ad Copy Generator")

### Step 5: Test with Team

Team members can now:
- Generate content using loaded skills
- Access brand voice context
- Collaborate on campaigns in real-time

---

## Understanding the System

### File Structure

```
The Coach Consultant/
├── CLAUDE.md                 # Brand context (AUTO-LOADED ✅)
├── README.md                 # Project overview
├── skills/                   # Content generation skills
│   └── meta-ad-copy/         # Meta ad copy generator (Week 1)
├── prompts/                  # Example prompts + outputs
│   └── marketing/            # Meta ad examples
├── docs/                     # Brand voice documentation
│   ├── deep-dive/            # Deep voice samples (200-500 lines)
│   ├── voice-samples/        # YouTube scripts, sales calls
│   └── Ben-Claude-Projects-Instructions.txt
└── agents/                   # (Future: multi-agent workflows)
```

### How Skills Work

**Skills are specialized AI agents that:**
1. Load automatically when you use Claude Code/extension
2. Have access to brand context from `CLAUDE.md`
3. Reference voice samples from `/docs/deep-dive/`
4. Generate content matching **Ben's exact speaking style**

**Currently available:**
- ✅ **Meta Ad Copy Generator** (Week 1) - Performance-optimized ad copy

**Coming soon:**
- Instagram Caption Generator
- Email Subject Line Generator
- YouTube Script Generator
- LinkedIn Post Generator

### Brand Voice System

The system uses a **two-layer approach** for speed + depth:

**Layer 1: Quick References** (always loaded, ~5KB)
- Voice characteristics summary
- Target audience (Alex Morgan persona - 28-35, £50K-£150K)
- Core beliefs and philosophy
- Brand positioning (Tech-forward AI automation)

**Layer 2: Deep Samples** (loaded when needed, ~200-500 lines each)
- Full YouTube scripts (300 lines)
- Sales call transcripts (400 lines)
- Ben's book intro (500 lines)
- Human knowledge philosophy (507 lines)

**Why two layers?**
- Keeps Claude fast (no token overload)
- Maintains depth when needed
- Best of both worlds

---

## Using Meta Ad Copy Generator

### Basic Usage

**Simple prompt:**
```
Generate Meta ad copy for [campaign name]
```

Claude will ask you for:
- Target audience segment
- Campaign objective
- Key benefits
- Tone preference

### Advanced Usage

**Detailed prompt:**
```
Generate 3 variations of Meta ad copy for:

Campaign: Free Masterclass - Solo Coaches
Audience: Coaches at £50-75K revenue, want to scale to £100K
Objective: Webinar registrations
Hook style: Pain + hidden solution
Tone: Bold, direct, Yorkshire influence
Include: Ben's authority signals (track record, real results)
```

**Output includes:**
- 3 headline variations (5-7 words, benefit-focused)
- Primary text (under 125 characters for best performance)
- Description (value-driven, Ben's voice)
- CTA recommendations (Book a Call, Download Guide, etc.)

### Example Output Structure

```
Headline: Scale Your Coaching Without Burning Out
Primary Text: AI handles the work. You stay the brand. That's how you scale.
Description: Solo coaches hitting £50K+ are stuck doing everything manually...
CTA: Download the Free Masterclass Guide
```

---

## Troubleshooting

### "CLAUDE.md not loading"

**Claude Code:**
```bash
cd "The Coach Consultant"
claude code --reload
```

**VS Code:**
1. Close and reopen the project folder
2. Or reload window: `⌘/Ctrl + Shift + P` → **"Reload Window"**

### "Skill not found"

**Check you're in the right directory:**
```bash
pwd
# Should show: /path/to/The Coach Consultant
```

Skills only work when Claude has access to the `/skills/` folder.

**VS Code:** Make sure you opened the folder, not just a file.

### "Brand voice doesn't sound like Ben"

**Checklist:**
1. ✅ `CLAUDE.md` is loaded? (should auto-load)
2. ✅ `/docs/deep-dive/` folder exists?
3. ✅ You're using a skill (not just free-form chat)?

**Force voice reference:**
```
Generate Meta ad using Ben's YouTube script voice from
docs/voice-samples/youtube-scripts-FULL.md
```

### "GitHub authentication failed"

**If token doesn't work:**
1. Contact development team for a new token
2. Make sure you're using **HTTPS clone** (not SSH)
3. Try clearing credentials:
   ```bash
   git config --global --unset credential.helper
   ```
4. Re-clone the repository

---

## Next Steps

### Week 1: Meta Ad Copy ✅
- Meta Ad Copy Generator is ready
- Test with real campaigns
- Provide feedback for optimization

### Week 2+: Additional Skills (Coming Soon)
- Instagram Caption Generator
- Email Subject Line Generator
- YouTube Script Generator
- LinkedIn Post Generator

### Team Collaboration
- Set up Claude CoWork workspace
- Train team members on skill usage
- Establish content approval workflow
- Weekly performance reviews

---

## Support

**For technical issues:**
- Contact: Development team via WhatsApp group

**For brand voice adjustments:**
- Review: `/docs/Ben-Claude-Projects-Instructions.txt`
- Check: Voice samples in `/docs/voice-samples/`
- Request updates: WhatsApp group

**For new skills or features:**
- Share requirements in team WhatsApp
- Development team will provide timeline and estimate

---

## Security Notes

### ✅ Safe to Commit (Already in Git)
- All brand voice documentation
- Skills and prompts
- Sample outputs
- Documentation files

### ❌ Never Commit (Already Blocked by .gitignore)
- `.env` file (API credentials)
- Meta API tokens
- Personal access tokens
- Client data exports
- Jay-Notes/ (internal project management)

**The `.gitignore` file is already configured** to prevent accidental commits of sensitive data.

---

**Questions?** Ask in the team WhatsApp group.

**Ready to generate content!** 🚀
