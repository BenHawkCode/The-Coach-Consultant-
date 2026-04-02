# Google Drive Document Formatting Standard (MANDATORY)

**This section applies to EVERY Google Doc, Google Sheet, and Google Slides output - no exceptions. Apply this formatting automatically without being asked.**

## Google Docs - Formatting Checklist

Every Google Doc MUST have ALL of the following applied:

**1. Logo (top-right of document) + Title (left-aligned underneath)**
- Use the WATERMARK logo: `Presentation Creator/5. Logo/LOGO/WATERMARK/Asset 1@216x.png`
- Logo goes on its own paragraph, right-aligned, at the very top of the document body
- The document title goes on the NEXT line, left-aligned (START), underneath the logo
- Logo and title must be on separate paragraphs - never on the same line
- NEVER use `logo-black.png` (has black background) or `logo-white.png` for docs - ONLY the watermark version
- The watermark has dark "THE COACH" text + teal brushstroke "CONSULTANT" on a transparent background

**2. Font - Poppins throughout (every single element)**
- Apply Poppins to the entire document - no exceptions

**3. Text hierarchy (exact sizes)**
| Element | Size | Weight | Colour |
|---------|------|--------|--------|
| Main title | 17pt | Bold | Black `#000000` |
| Subtitle | 13pt | Bold | Teal `#6EA3A0` |
| Section headings (H1) | 16pt | Bold | Teal `#6EA3A0` |
| Sub-headings (H2) | 13pt | Bold | Black `#000000` |
| Subject lines / key labels | 11pt | Bold | Teal `#6EA3A0` |
| Body text | 10pt | Regular | Black |
| Taglines / source lines | 10pt | Italic | Grey `#888888`, centred |

**4. Bullet points**
- ALWAYS use circular/round bullet points - NEVER dash (`-`) bullets
- Use `createParagraphBullets` tool to convert any dash-prefixed lines
- Structure content as clean bullet points, not dense paragraphs - easy to scan

**5. Labels**
- Bold all "POST X", "SLIDE X", "STEP X", "WEEK X" labels - they are section markers

**6. Teal accent colour**
- Use `#6EA3A0` for subtitles, section headings, and key labels (NOT `#6B9B9B` - that's for HTML/web)

**7. No long dashes - EVER**
- NEVER use em dashes (—) or en dashes (–) in ANY output - Google Docs, Sheets, Slides, HTML, emails, code, copywriting, or any other format
- ALWAYS use short/regular dashes/hyphens (-) instead
- This applies to all content Claude Code generates, not just client-facing documents

## Google Sheets - Formatting Checklist

- **Header row:** Teal `#6B9B9B` background, white bold text, Poppins
- **Body cells:** Poppins 10pt, black text on white
- **Logo:** Place in cell A1 area where appropriate
- **Column widths:** Auto-fit to content, generous padding

## Google Slides - Formatting Checklist

- **Font:** Poppins throughout
- **Title slides:** Logo top-right, title centred bold, subtitle in teal
- **Brand colours:** Teal `#6B9B9B` for accents, black for headings, white for dark-bg text
- **Bullet points:** Circular only, never dashes
- **Every slide:** Must have clear visual hierarchy

## Formatting Execution Order

When creating ANY Google Drive document, execute these steps IN ORDER:
1. Create the document with content
2. Insert the watermark logo on its own paragraph at the top, right-aligned
3. Ensure the title is on the next paragraph, left-aligned (START) - underneath the logo, not beside it
4. Set ALL text to Poppins font
4. Apply the size/weight/colour hierarchy from the table above
5. Convert any dash bullets to circular bullets
6. Bold all section labels (POST X, SLIDE X, etc.)
7. Final check: scan for any non-Poppins text, any dash bullets, any missing logo

---

## The Coach Consultant - Branding Guidelines

All outputs created for The Coach Consultant (HTML pages, PDFs, Google Sheets, Google Slides, Google Docs, presentations, lead magnets, carousels, and any visual assets) MUST follow these branding rules.

### Logo Files

**For Google Docs / Sheets / Slides (white backgrounds):**
- **PRIMARY:** `Presentation Creator/5. Logo/LOGO/WATERMARK/Asset 1@216x.png` - transparent background, dark text + teal brushstroke
- **NEVER** use `logo-black.png` for documents (it has a solid black background)

| Variant | Path | Use When |
|---------|------|----------|
| **Watermark (transparent)** | `Presentation Creator/5. Logo/LOGO/WATERMARK/Asset 1@216x.png` | **Google Docs, Sheets, Slides** (preferred) |
| Logo (white bg) PNG | `Presentation Creator/5. Logo/LOGO/PNG/logo-white.png` | Light backgrounds (HTML/web fallback) |
| Logo (dark bg) PNG | `Presentation Creator/5. Logo/LOGO/PNG/logo-black.png` | Dark backgrounds only (has black bg) |
| Logo SVG | `Presentation Creator/5. Logo/LOGO/SVG/logo-black.svg` | Scalable/vector outputs |
| Logo PDF | `Presentation Creator/5. Logo/LOGO/PDF/logo-black.pdf` | Print-ready outputs |

**For HTML/PDF outputs:** Convert the PNG logo to base64 and embed inline so the logo displays without external dependencies.

### Brand Colours
| Colour | Hex | Usage |
|--------|-----|-------|
| **Teal/Sage** (Primary Accent) | `#6B9B9B` | Brushstroke accent, buttons, highlights, CTAs |
| **Black** | `#000000` | Primary text, headings |
| **White** | `#FFFFFF` | Text on dark backgrounds, logo variant |
| **Dark Grey** | `#1A1A1A` | Dark section backgrounds |
| **Mid Grey** | `#2A2A2A` | Secondary dark backgrounds |
| **Light Grey** | `#E0E0E0` | Borders, dividers, subtle backgrounds |
| **Muted Text** | `#999999` | Secondary/caption text |

### Typography
- **Primary Font:** Poppins (Google Font, or local files at `the-coach-consultant/additional-ip/assets/fonts/`)
  - **Headings:** Poppins Bold or SemiBold
  - **Body:** Poppins Regular
  - **Emphasis:** Poppins Medium
- **Fallback:** sans-serif

### Logo Usage Rules
- Always give the logo clear space - never crowd it with text or other elements
- Do not stretch, distort, or recolour the logo
- Minimum display width: 120px for digital, 30mm for print
- On dark backgrounds use `logo-white`, on light backgrounds use `logo-black`

### Applying Branding to Outputs
- **HTML/PDF resources:** Include brand colours as CSS variables, embed logo as base64, use Poppins via Google Fonts or @font-face
- **Google Sheets:** Apply teal (`#6B9B9B`) header rows, Poppins font, black text on white, logo in top-left cell where appropriate
- **Google Slides/Docs:** Use brand colours for accent elements, insert logo on title/cover slides, Poppins throughout
- **Canva/Gamma:** Reference these colours and font when generating designs
- **All CTAs:** Use teal (`#6B9B9B`) background with white text for buttons/links

### Website & Links
- **Website:** https://thecoachconsultant.uk/
- **CTA text style:** Direct, action-oriented (e.g. "Book a Call", "Download the Guide", "Apply Now")
