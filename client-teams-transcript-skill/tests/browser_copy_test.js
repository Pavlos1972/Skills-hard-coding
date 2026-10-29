// Opens the generated Planner page in a real browser at phone width, clicks Copy note and reports what
// landed on the clipboard. Usage: node browser_copy_test.js <planner_note.html> <screenshot.png>
const { chromium } = require('playwright');
(async () => {
  const file = 'file://' + process.argv[2];
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 375, height: 800 }, permissions: ['clipboard-read', 'clipboard-write'] });
  const page = await ctx.newPage();
  const errors = []; page.on('pageerror', e => errors.push(String(e))); page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(file);
  const title = await page.title();
  const hscroll = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  await page.click('#copy-note');
  await page.waitForTimeout(300);
  const status = await page.textContent('#msg');
  const clip = await page.evaluate(async () => {
    const items = await navigator.clipboard.read(); const out = {};
    for (const it of items) for (const ty of it.types) out[ty] = await (await it.getType(ty)).text();
    return out;
  });
  await page.screenshot({ path: process.argv[3], fullPage: true });
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.screenshot({ path: process.argv[3].replace('.png', '-dark.png'), fullPage: true });
  console.log(JSON.stringify({
    title, horizontalScroll: hscroll, errors, status,
    htmlHasBold: /<b>/.test(clip['text/html'] || ''), htmlHasBullet: (clip['text/html'] || '').includes('•'),
    plainHasMarkdownStars: /\*\*/.test(clip['text/plain'] || ''), plainFirstLines: (clip['text/plain'] || '').split('\n').slice(0, 4),
    plainHasAction: (clip['text/plain'] || '').includes('Sitamah to get the credit-life details from Sam'),
  }, null, 1));
  await browser.close();
})();
