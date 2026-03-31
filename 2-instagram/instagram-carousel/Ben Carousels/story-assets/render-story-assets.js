#!/usr/bin/env node
/**
 * Render portrait story asset HTML files to 1080x1920 PNG files.
 *
 * Usage:
 *   node render-story-assets.js                     # renders all HTML in assets/
 *   node render-story-assets.js assets/AI-ST-01.html  # renders one file
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const VIEWPORT = { width: 1080, height: 1920, deviceScaleFactor: 2 };

async function renderAsset(browser, htmlPath, outputDir) {
  const absolutePath = path.resolve(htmlPath);
  if (!fs.existsSync(absolutePath)) {
    console.error(`  File not found: ${absolutePath}`);
    return;
  }

  const baseName = path.basename(absolutePath, '.html');
  const fileUrl = `file://${absolutePath}`;

  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });
  await page.evaluateHandle('document.fonts.ready');
  await new Promise(r => setTimeout(r, 300));

  const element = await page.$('.story-asset');
  if (!element) {
    console.error(`  No .story-asset element found in ${baseName}`);
    await page.close();
    return;
  }

  const outputPath = path.join(outputDir, `${baseName}.png`);
  await element.screenshot({ path: outputPath, type: 'png' });
  console.log(`  \u2713 ${baseName}.png`);

  await page.close();
}

async function main() {
  const arg = process.argv[2];
  const scriptDir = __dirname;
  const assetsDir = path.join(scriptDir, 'assets');
  const outputDir = path.join(scriptDir, 'outputs');

  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  let htmlFiles = [];
  if (arg && fs.existsSync(path.resolve(arg))) {
    htmlFiles = [path.resolve(arg)];
  } else {
    if (!fs.existsSync(assetsDir)) {
      console.error('No assets/ directory found.');
      process.exit(1);
    }
    htmlFiles = fs.readdirSync(assetsDir)
      .filter(f => f.endsWith('.html'))
      .sort()
      .map(f => path.join(assetsDir, f));
  }

  console.log(`Rendering ${htmlFiles.length} story assets at 1080x1920 (2x)...\n`);

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  for (const htmlFile of htmlFiles) {
    await renderAsset(browser, htmlFile, outputDir);
  }

  await browser.close();
  console.log(`\nDone! ${htmlFiles.length} PNGs saved to: ${outputDir}`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
