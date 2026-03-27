#!/usr/bin/env node
/**
 * Render carousel HTML slides to individual PNG files.
 *
 * Usage:
 *   node render-slides.js <path-to-carousel.html>
 *
 * Outputs slide-1.png, slide-2.png, etc. in the same directory as the HTML file.
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function renderSlides(htmlPath, outputDirOverride) {
  const absolutePath = path.resolve(htmlPath);
  if (!fs.existsSync(absolutePath)) {
    console.error(`File not found: ${absolutePath}`);
    process.exit(1);
  }

  const outputDir = outputDirArg ? path.resolve(outputDirArg) : path.dirname(absolutePath);
  if (!fs.existsSync(outputDir)) { fs.mkdirSync(outputDir, { recursive: true }); }
  const fileUrl = `file://${absolutePath}`;

  console.log(`Rendering slides from: ${absolutePath}`);

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Initial viewport — width to fit slides, 2x scale for crisp output
  await page.setViewport({ width: 1200, height: 1200, deviceScaleFactor: 2 });

  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });

  // Wait for fonts to load
  await page.evaluateHandle('document.fonts.ready');

  // Find all slide elements
  const slides = await page.$$('.slide');
  console.log(`Found ${slides.length} slides`);

  // Expand viewport to fit all slides so they render fully
  const totalHeight = await page.evaluate(() => document.body.scrollHeight);
  await page.setViewport({ width: 1200, height: totalHeight, deviceScaleFactor: 2 });

  // Brief pause to let the expanded viewport render
  await new Promise(r => setTimeout(r, 500));

  for (let i = 0; i < slides.length; i++) {
    const slideNum = i + 1;
    const outputPath = path.join(outputDir, `slide-${slideNum}.png`);

    // Use element screenshot (auto-crops to element bounds)
    await slides[i].screenshot({
      path: outputPath,
      type: 'png'
    });

    console.log(`  ✓ slide-${slideNum}.png (1080x1080)`);
  }

  await browser.close();
  console.log(`\nDone! ${slides.length} PNG files saved to: ${outputDir}`);
}

const htmlFile = process.argv[2];
const outputDirArg = process.argv[3]; // optional output directory
if (!htmlFile) {
  console.error('Usage: node render-slides.js <path-to-carousel.html> [output-dir]');
  process.exit(1);
}

renderSlides(htmlFile, outputDirArg).catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
