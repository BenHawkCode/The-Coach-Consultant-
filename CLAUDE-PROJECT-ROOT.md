# Claude Code Projects - GitHub Auto-Sync

## GitHub Account
- Username: BenHawkCode
- Auth: GitHub CLI (`gh`) authenticated

## Auto-Sync Rule

Every subfolder in this directory is a project that MUST be connected to GitHub under the `BenHawkCode` account. When working in any subfolder, Claude Code must:

### 1. Ensure it's a Git repo
If the subfolder is not yet a git repository:
```bash
cd <subfolder>
git init
git add -A
git commit -m "Initial commit"
```

### 2. Ensure it has a GitHub remote
If no remote exists:
```bash
gh repo create BenHawkCode/<folder-name> --private --source=. --push
```
- Default to **private** repos unless the user says otherwise
- Use the folder name (kebab-case) as the repo name

### 3. Push changes on every session
At the end of any work session in a subfolder, or when asked to save/sync:
```bash
git add -A
git commit -m "<descriptive message>"
git push origin main
```
If the branch is not `main`, push to whatever branch is checked out.

### 4. Existing repos
If a subfolder already has a remote (like `the-coach-consultant`), respect the existing remote and push there. Do not create a duplicate repo.

## Folder-to-Repo Mapping
| Folder | GitHub Repo | Status |
|--------|------------|--------|
| the-coach-consultant | BenHawkCode/The-Coach-Consultant- | Connected |
| Claude-Projects-Client-Pack | BenHawkCode/Claude-Projects-Client-Pack | Needs init |
| Presentation Creator | BenHawkCode/presentation-creator | Needs init |
| Titan Clients | BenHawkCode/titan-clients | Needs init |

## Important
- Always commit with clear, descriptive messages
- Never force push without explicit user permission
- Keep repos private by default
- Do not commit sensitive files (.env, credentials, API keys) - add them to .gitignore

---

## Project Directory
Each subfolder is a distinct project. Always read the subfolder's CLAUDE.md before starting work there.

| Folder | Purpose |
|--------|---------|
| the-coach-consultant | TCC brand - content generation, marketing, personal brand |
| Titan Clients | Client deliverables - one subfolder per coaching client |
| Claude-Projects-Client-Pack | Sellable resource pack - templates and frameworks |
| Presentation Creator | Design assets, icon libraries, carousel rendering |

## Document Formatting - Minimal Mode (SAVE CREDITS)
- Poppins font on all text (one API call).
- Bold titles, subtitles, and section headings.
- Circular bullet points on lists.
- Do NOT insert logos, brand colours, font colours, or per-element formatting.
- Maximum 3-5 formatting API calls per document, not 30-50.
- Content first, formatting second. This applies to all document types.

## Branding References (Load Only When Asked)
- **`BRANDING.md`** - TCC branding guidelines (logos, colours, typography). Only apply when full branding is explicitly requested.
- **`DESIGN-SYSTEM.md`** - Visual design rules, carousel rendering. Only apply for carousel/presentation work.
