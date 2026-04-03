#!/usr/bin/env node
/**
 * Render reel cover HTML to individual 1080x1920 PNG files.
 *
 * Usage:
 *   node render-reel-covers.js <path-to-html>
 *   node render-reel-covers.js reel-cover-template.html
 *
 * Outputs cover-1.png, cover-2.png, etc. into the outputs/ directory.
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const VIEWPORT = { width: 1080, height: 1920, deviceScaleFactor: 2 };

async function renderCovers(htmlPath) {
  const absolutePath = path.resolve(htmlPath);
  if (!fs.existsSync(absolutePath)) {
    console.error(`File not found: ${absolutePath}`);
    process.exit(1);
  }

  const scriptDir = __dirname;
  const outputDir = path.join(scriptDir, 'reel covers');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  // Read the HTML and inject the logo base64
  let html = fs.readFileSync(absolutePath, 'utf8');

  // Try to find and inject logo
  // Prefer watermark (transparent bg), fallback to white logo
  const logoWatermarkPath = path.join(scriptDir, '..', 'instagram-carousel', 'TCC Carousels', 'logo-watermark-base64.txt');
  const logoBase64Path = fs.existsSync(logoWatermarkPath) ? logoWatermarkPath : path.join(scriptDir, '..', 'instagram-carousel', 'TCC Carousels', 'logo-white-base64.txt');
  if (fs.existsSync(logoBase64Path)) {
    const logoBase64 = fs.readFileSync(logoBase64Path, 'utf8').trim();
    html = html.replace(/\[LOGO-PATH\]/g, `data:image/png;base64,${logoBase64}`);
    console.log('Logo injected from logo-white-base64.txt');
  } else {
    // Fallback to PNG file
    const logoPngPath = path.join(scriptDir, '..', 'instagram-carousel', 'TCC Carousels', '..', '..', '..', 'Presentation Creator', '5. Logo', 'LOGO', 'PNG', 'logo-white.png');
    if (fs.existsSync(logoPngPath)) {
      html = html.replace(/\[LOGO-PATH\]/g, `file://${path.resolve(logoPngPath)}`);
      console.log('Logo injected from logo-white.png');
    } else {
      console.warn('Warning: No logo file found. Covers will render without logo.');
    }
  }

  // Resolve relative image paths to absolute file:// paths
  html = html.replace(/src="([^"]+\.(jpg|JPG|jpeg|png|PNG))"/g, (match, filename) => {
    if (filename.startsWith('file://') || filename.startsWith('data:')) return match;
    const imgPath = path.join(scriptDir, filename);
    if (fs.existsSync(imgPath)) {
      return `src="file://${imgPath}"`;
    }
    console.warn(`Warning: Image not found: ${imgPath}`);
    return match;
  });

  // Write the processed HTML to a temp file
  const tempPath = path.join(scriptDir, '_temp-render.html');
  fs.writeFileSync(tempPath, html);

  console.log(`\nRendering reel covers at 1080x1920 (2x)...\n`);

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);

  const fileUrl = `file://${tempPath}`;
  await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 60000 });

  // Wait for fonts and images to load
  await page.evaluateHandle('document.fonts.ready');
  await new Promise(r => setTimeout(r, 1000));

  // Expand viewport to fit all covers
  const totalHeight = await page.evaluate(() => document.body.scrollHeight);
  await page.setViewport({ width: 1080, height: totalHeight, deviceScaleFactor: 2 });
  await new Promise(r => setTimeout(r, 500));

  // Find all reel-cover elements
  const covers = await page.$$('.reel-cover');
  console.log(`Found ${covers.length} reel covers\n`);

  for (let i = 0; i < covers.length; i++) {
    const num = i + 1;
    const baseName = path.basename(htmlPath, '.html');
    const prefix = baseName.includes('day-series') ? 'day' : 'cover';
    const outputPath = path.join(outputDir, `${prefix}-${num}.png`);
    await covers[i].screenshot({ path: outputPath, type: 'png' });
    console.log(`  \u2713 ${prefix}-${num}.png (1080x1920)`);
  }

  await browser.close();

  // Clean up temp file
  fs.unlinkSync(tempPath);

  console.log(`\nDone! ${covers.length} reel cover PNGs saved to: ${outputDir}`);
}

const htmlFile = process.argv[2];
if (!htmlFile) {
  console.error('Usage: node render-reel-covers.js <path-to-html>');
  process.exit(1);
}

renderCovers(htmlFile).catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
