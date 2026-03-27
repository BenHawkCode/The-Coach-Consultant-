#!/usr/bin/env node
/**
 * Export all icons/emblems from icon-emblem-library.html as individual files.
 *
 * Outputs:
 *   exported-icons/png/<category>/<name>.png   — 512x512 transparent PNGs
 *   exported-icons/svg/<category>/<name>.svg   — standalone SVG files (pure SVG icons only)
 *
 * Usage:
 *   node export-icons.js
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const HTML_FILE = path.join(__dirname, 'icon-emblem-library.html');
const OUTPUT_DIR = path.join(__dirname, 'exported-icons');
const PNG_DIR = path.join(OUTPUT_DIR, 'png');
const SVG_DIR = path.join(OUTPUT_DIR, 'svg');

// CSS variable values for standalone SVG resolution
const CSS_VARS = {
  'var(--teal)': '#5B9A9A',
  'var(--dark-teal)': '#3d7a7a',
  'var(--light-teal)': '#7abfbf',
  'var(--accent)': '#FF6B35',
  'var(--accent2)': '#FFD166',
  'var(--bg)': '#0a0a0a',
  'var(--bg2)': '#141414',
  'var(--bg3)': '#1a1a1a',
  'var(--white)': '#ffffff',
  'var(--gray)': '#aaaaaa',
  'var(--gray-light)': '#cccccc',
  'var(--red)': '#ff4444',
  'var(--green)': '#44ff88',
  'var(--purple)': '#9B6DFF',
  'var(--blue)': '#4D9FFF',
};

function toKebab(str) {
  return str
    .toLowerCase()
    .replace(/[&]/g, 'and')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

function resolveCssVars(svgMarkup) {
  let resolved = svgMarkup;
  for (const [varRef, hex] of Object.entries(CSS_VARS)) {
    resolved = resolved.split(varRef).join(hex);
  }
  return resolved;
}

function wrapSvg(innerSvg) {
  // The inner SVGs already have width/height/viewBox — just add XML header
  return `<?xml version="1.0" encoding="UTF-8"?>\n${innerSvg}`;
}

async function main() {
  if (!fs.existsSync(HTML_FILE)) {
    console.error(`File not found: ${HTML_FILE}`);
    process.exit(1);
  }

  // Clean output dirs
  if (fs.existsSync(OUTPUT_DIR)) {
    fs.rmSync(OUTPUT_DIR, { recursive: true });
  }
  fs.mkdirSync(PNG_DIR, { recursive: true });
  fs.mkdirSync(SVG_DIR, { recursive: true });

  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 1200, deviceScaleFactor: 4 });

  const fileUrl = `file://${HTML_FILE}`;
  console.log('Loading icon library...');
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.evaluateHandle('document.fonts.ready');

  // Expand viewport to render everything
  const totalHeight = await page.evaluate(() => document.body.scrollHeight);
  await page.setViewport({ width: 1600, height: totalHeight, deviceScaleFactor: 4 });
  await new Promise(r => setTimeout(r, 1000));

  // Extract all items with their category and metadata (BEFORE style override)
  const items = await page.evaluate(() => {
    const results = [];
    // Walk through all category sections
    const categorySeps = document.querySelectorAll('.category-sep');

    categorySeps.forEach(sep => {
      const h2 = sep.querySelector('h2');
      if (!h2) return;
      const categoryName = h2.textContent.trim();

      // Find the next .section sibling(s) until the next .category-sep
      let section = sep.nextElementSibling;
      while (section && !section.classList.contains('category-sep')) {
        // Find all .ic and .ec elements in this section
        const cells = section.querySelectorAll('.ic, .ec');
        cells.forEach(cell => {
          const label = cell.querySelector('.ic-label');
          const labelText = label ? label.textContent.trim() : '';
          const svg = cell.querySelector('svg');
          const hasPureSvg = svg && svg.getAttribute('width') && !cell.classList.contains('ec');

          // Get the sub-heading if present (for emblems: Stamps, Number Circles, CTAs, Watermarks)
          let subCategory = '';
          // Walk backwards from cell to find h3
          let prevEl = cell.parentElement;
          while (prevEl) {
            const h3 = prevEl.previousElementSibling;
            if (h3 && h3.tagName === 'H3') {
              subCategory = h3.textContent.trim();
              break;
            }
            if (h3 && h3.classList && h3.classList.contains('ig')) {
              prevEl = h3;
              continue;
            }
            break;
          }

          results.push({
            categoryName,
            subCategory,
            labelText,
            hasPureSvg,
            svgOuterHTML: svg ? svg.outerHTML : null,
            // Store a selector path so we can find the element again for screenshots
            index: results.length,
          });
        });
        section = section.nextElementSibling;
      }
    });

    return results;
  });

  console.log(`Found ${items.length} items to export.\n`);

  // NOW inject global style to nuke all backgrounds for transparent screenshots
  await page.evaluate(() => {
    const style = document.createElement('style');
    style.id = 'export-override';
    style.textContent = `
      html, body, .header, .section, .category-sep,
      .ig, .ig-wide, .ig-xl,
      nav, .top-nav {
        background: transparent !important;
        background-color: transparent !important;
        box-shadow: none !important;
      }
      .ic, .ec {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 8px !important;
      }
      .ic-label { display: none !important; }
      .top-nav, .header, .nav-links, .cat-head, .category-sep { visibility: hidden !important; height: 0 !important; overflow: hidden !important; }
    `;
    document.head.appendChild(style);
  });
  await new Promise(r => setTimeout(r, 500));

  // Track filenames per category to handle duplicates
  const usedNames = {};
  let pngCount = 0;
  let svgCount = 0;

  // Get all .ic and .ec elements for screenshotting
  const allCells = await page.$$('.ic, .ec');

  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    const catFolder = toKebab(item.categoryName);
    let baseName = toKebab(item.labelText || `item-${i + 1}`);

    // Prefix with sub-category for emblems
    if (item.subCategory) {
      const subPrefix = toKebab(item.subCategory);
      // Only prefix if sub-category adds clarity (stamps, ctas, number-circles, watermarks)
      if (['stamps', 'number-circles', 'ctas-and-buttons', 'watermarks'].includes(subPrefix)) {
        baseName = `${subPrefix.replace('and-', '')}-${baseName}`;
      }
    }

    // Handle duplicate names within same category
    const nameKey = `${catFolder}/${baseName}`;
    if (usedNames[nameKey]) {
      usedNames[nameKey]++;
      baseName = `${baseName}-${usedNames[nameKey]}`;
    } else {
      usedNames[nameKey] = 1;
    }

    // Create category folders
    const pngCatDir = path.join(PNG_DIR, catFolder);
    const svgCatDir = path.join(SVG_DIR, catFolder);
    if (!fs.existsSync(pngCatDir)) fs.mkdirSync(pngCatDir, { recursive: true });

    // --- PNG EXPORT ---
    const pngPath = path.join(pngCatDir, `${baseName}.png`);

    if (allCells[i]) {
      try {
        await allCells[i].screenshot({
          path: pngPath,
          type: 'png',
          omitBackground: true,
        });
        pngCount++;

        if (pngCount % 50 === 0) {
          console.log(`  ... exported ${pngCount} PNGs so far`);
        }
      } catch (err) {
        console.error(`  ✗ Failed PNG for "${item.labelText}" in ${catFolder}: ${err.message}`);
      }
    }

    // --- SVG EXPORT ---
    if (item.hasPureSvg && item.svgOuterHTML) {
      if (!fs.existsSync(svgCatDir)) fs.mkdirSync(svgCatDir, { recursive: true });
      const svgPath = path.join(svgCatDir, `${baseName}.svg`);
      const resolvedSvg = resolveCssVars(item.svgOuterHTML);
      // Add xmlns for standalone SVG
      const svgWithNs = resolvedSvg.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ');
      fs.writeFileSync(svgPath, wrapSvg(svgWithNs));
      svgCount++;
    }
  }

  await browser.close();

  console.log(`\n✓ Export complete!`);
  console.log(`  ${pngCount} PNG files → ${PNG_DIR}`);
  console.log(`  ${svgCount} SVG files → ${SVG_DIR}`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
