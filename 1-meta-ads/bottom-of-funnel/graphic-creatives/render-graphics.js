const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const files = [
    'graphic-1-ai-systems-stack.html',
    'graphic-2-claude-specialist.html',
    'graphic-3-brand-moat.html',
    'graphic-4-visibility-gap.html',
    'graphic-5-the-numbers.html',
    'graphic-6-old-vs-ai.html'
];

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const dir = __dirname;

    for (const file of files) {
        const filePath = path.join(dir, file);
        const outName = file.replace('.html', '.png');
        const outPath = path.join(dir, outName);

        const page = await browser.newPage();
        await page.setViewport({ width: 1080, height: 1080, deviceScaleFactor: 2 });
        await page.goto('file://' + filePath, { waitUntil: 'networkidle0', timeout: 30000 });
        await page.screenshot({ path: outPath, type: 'png' });
        await page.close();
        console.log(`Rendered: ${outName}`);
    }

    await browser.close();
    console.log('All 6 graphics rendered.');
})();
