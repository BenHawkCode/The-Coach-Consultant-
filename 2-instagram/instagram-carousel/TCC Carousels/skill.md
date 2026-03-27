---
name: instagram-carousel
description: Generate branded Instagram carousel slides as a single HTML file (1080x1080 square format). Uses TCC brand colours, Poppins font, and embedded logo. Outputs ready-to-screenshot slides.
---

# Instagram Carousel Generator

Generate branded Instagram carousel posts as a single HTML page with 1080x1080px square slides, ready to screenshot for posting.

## Instructions for Claude

When this skill is invoked:

### Step 1: Ask the user for carousel details

Use the AskUserQuestion tool to gather:

**Question 1: Carousel Topic**
- Header: "What's the carousel about?"
- Text input for the user to describe the topic, message, or angle

**Question 2: Carousel Type**
- Header: "Carousel Type"
- Options:
  - "Educational" (Teach something — tips, steps, how-to)
  - "Pain → Solution" (Problem awareness → your fix)
  - "Myth Busting" (Common mistakes or myths debunked)
  - "Case Study / Results" (Client transformation or proof)
  - "Offer / Promotion" (Sell a product, service, or lead magnet)

**Question 3: Number of Slides**
- Header: "How many slides?"
- Options:
  - "5 slides" (Quick punchy carousel)
  - "7 slides" (Standard carousel)
  - "10 slides" (Full deep-dive carousel)

**Question 4: CTA Style**
- Header: "Call to Action"
- Options:
  - "Comment a keyword" (e.g. Comment "SYSTEM" below)
  - "Link in bio" (Direct to website/landing page)
  - "Book a call" (Direct to booking)
  - "DM me" (Start a conversation)
  - "Custom" (User specifies)

If user selects "Custom", ask a follow-up for the specific CTA text.

**CRITICAL**: Do NOT generate the carousel until all questions are answered.

### Step 2: Read the template and brand assets

1. Read the carousel HTML template:
   ```
   the-coach-consultant/2-instagram/instagram-carousel/carousel-template.html
   ```

2. Read the base64 logo files for embedding:
   ```
   the-coach-consultant/2-instagram/instagram-carousel/logo-white-base64.txt
   the-coach-consultant/2-instagram/instagram-carousel/logo-black-base64.txt
   ```

3. Reference the design system from `Presentation Creator/design-assets/DESIGN-SYSTEM.md`:
   - **Fonts**: Space Grotesk (headings) + Inter (body)
   - **Teal**: `#5B9A9A` (dark: `#3d7a7a`, light: `#7abfbf`)
   - **Accents**: Orange `#FF6B35`, Yellow `#FFD166`
   - **Dark backgrounds**: `linear-gradient(135deg, #0a0a0a 0%, #1a2a2a 100%)`
   - **Cards**: `rgba(255,255,255,0.04)` bg, `16px` radius

4. Reference brand voice rules from `the-coach-consultant/CLAUDE.md`:
   - British English always
   - No forbidden AI phrases
   - Ben's natural phrases and tone
   - Short punchy sentences, one per line
   - Direct, Yorkshire straight-talking

### Step 3: Generate the carousel content

Write the slide content following this structure:

**Slide 1 — Hook (CRITICAL: must stop the scroll)**
- Bold, provocative statement or question
- Large text, high contrast
- Logo in top corner
- "Swipe →" indicator at bottom
- Dark background (black/dark grey)

**Slides 2 to N-1 — Value slides**
- One key point per slide
- Alternate between dark and light backgrounds for visual rhythm
- Use teal accent (`#6B9B9B`) for highlights and emphasis
- Keep text concise — max 3-4 short lines per slide
- Use icons, numbered lists, or visual elements where appropriate
- Pain points use red X marks, solutions use teal tick marks

**Final Slide — CTA**
- Clear call to action matching user's chosen CTA style
- Logo at bottom
- Teal accent on CTA element
- Dark background

### Step 4: Build the HTML file

Using the template structure from `carousel-template.html`:

1. All slides are 1080x1080px (square Instagram format)
2. Embed the correct logo as base64 (white logo on dark backgrounds, black logo on light backgrounds)
3. Use Poppins font via Google Fonts import
4. Apply design system colours as CSS variables:
   - `--teal: #5B9A9A` (primary accent)
   - `--teal-dark: #3d7a7a` (gradient endpoint)
   - `--teal-light: #7abfbf` (highlight text on dark)
   - `--orange: #FF6B35` (secondary accent)
   - `--yellow: #FFD166` (stats, highlights)
   - `--black: #0a0a0a` (dark backgrounds)
   - `--dark-grey: #141414` (secondary dark)
   - `--white: #ffffff` (light backgrounds)
   - `--muted: #aaaaaa` (secondary text)
5. Include page dot indicators on each slide showing position
6. Each slide has a label above it (e.g. "Slide 1 — Hook") for easy identification when screenshotting

### Step 5: Save and render to PNG

1. Save the generated HTML file to:
   ```
   the-coach-consultant/2-instagram/instagram-carousel/outputs/CAROUSEL-[topic-slug]-[date].html
   ```

2. Create the `outputs/` directory if it doesn't exist.

3. **Render to PNG files** by running the render script:
   ```bash
   cd the-coach-consultant/2-instagram/instagram-carousel && node render-slides.js "outputs/CAROUSEL-[topic-slug]-[date].html"
   ```

   This generates individual `slide-1.png`, `slide-2.png`, etc. in the outputs folder — each 1080x1080px, ready to upload directly to Instagram.

4. Tell the user their PNG files are ready at `the-coach-consultant/2-instagram/instagram-carousel/outputs/` and can be posted directly to Instagram as a carousel.

## Slide Design Rules

### Typography Scale
- **Hook headline**: 56-72px, font-weight 900
- **Slide headlines**: 46-52px, font-weight 900
- **Body text**: 22-26px, font-weight 500
- **Labels/categories**: 15px uppercase, letter-spacing 4px
- **Captions/small text**: 16-18px

### Colour Patterns
- **Dark slides**: Black/dark grey background, white text, teal accents
- **Light slides**: White background, black text, teal accents
- **Accent slide**: Teal background, white text (use sparingly — 1 per carousel max)
- **Highlight text**: Teal (`#6B9B9B`) for key words or phrases

### Layout Rules
- 80-90px padding on all slides
- Content vertically centred
- Logo: top-right on slide 1, bottom-centre on final slide
- Page dots: bottom-centre on every slide
- Max 6 bullet points per slide
- Generous spacing between elements

### Visual Elements
- Red X (`✗`) for pain points / problems
- Teal tick (`✓`) for solutions / benefits
- Numbered circles for steps
- Cards/boxes with subtle borders for grouping content
- Radial gradient overlays on dark slides for depth

## Brand Voice for Carousel Copy

### Do:
- Write like Ben speaks — direct, punchy, no fluff
- Use "coaches, consultants and service providers"
- British English (£, organisation, behaviour)
- Short sentences, one idea per line
- Include specific numbers and metrics where relevant
- Make the hook slide impossible to scroll past

### Don't:
- Use forbidden AI phrases (see CLAUDE.md)
- Use emojis in the slides
- Write paragraphs — keep it scannable
- Use dashes or excessive punctuation
- Sound corporate or generic
- Use more than 4 lines of text on any single slide

## Example Carousel Structures

### Educational (7 slides)
1. Hook: "Most coaches waste 70% of their week on admin"
2. Problem: "Sound familiar?" + pain point list
3-6. Tips/steps (one per slide, numbered)
7. CTA: "Comment SYSTEM and I'll send you the full breakdown"

### Pain → Solution (5 slides)
1. Hook: Bold problem statement
2. Pain amplification with specific examples
3. The shift / what actually works
4. The solution with proof/metrics
5. CTA

### Myth Busting (10 slides)
1. Hook: "Stop believing these myths about scaling"
2-9. One myth per slide (myth → reality format)
10. CTA

## Usage

```
/instagram-carousel
```

Or naturally:
```
Create an Instagram carousel about [topic]
```
