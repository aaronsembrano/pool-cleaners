import puppeteer from 'puppeteer';
import { writeFile, readFile } from 'fs/promises';
import { existsSync } from 'fs';
import { resolve } from 'path';

const BASE = '/Users/aaronsembrano/Desktop/Pool Cleaners';

// Read all sites that need logos
const sites = JSON.parse(process.argv[2] || '[]');

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

for (const site of sites) {
  const { folder, url, name } = site;
  const logoPath = resolve(BASE, folder, 'logo.png');

  // Skip if logo already exists and is a real image (not HTML)
  if (existsSync(logoPath)) {
    const buf = await readFile(logoPath);
    const header = buf.toString('utf8', 0, 15);
    if (!header.includes('<!') && !header.includes('<html') && buf.length > 1000) {
      console.log(`⏭️  ${name} — already has valid logo`);
      continue;
    }
  }

  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1440, height: 900 });
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 15000 });

    // Try to find the logo image in common locations
    const logoUrl = await page.evaluate(() => {
      // Common selectors for logos
      const selectors = [
        'header img[src*="logo"]',
        'header img[alt*="logo"]',
        'nav img[src*="logo"]',
        '.logo img',
        '#logo img',
        'a[class*="logo"] img',
        'div[class*="logo"] img',
        'header img:first-of-type',
        'nav img:first-of-type',
        '.header img:first-of-type',
        'img[src*="logo"]',
        'img[alt*="logo"]',
        'img[class*="logo"]',
      ];

      for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el && el.src && el.naturalWidth > 50) {
          return el.src;
        }
      }

      // Fallback: first image in the header area
      const headerImg = document.querySelector('header img, nav img');
      if (headerImg && headerImg.src) return headerImg.src;

      return null;
    });

    if (logoUrl) {
      // Download the logo via the browser (handles auth, CORS, etc)
      const response = await page.goto(logoUrl, { timeout: 10000 });
      const buffer = await response.buffer();

      if (buffer.length > 500) {
        await writeFile(logoPath, buffer);
        console.log(`✅ ${name} — logo downloaded (${Math.round(buffer.length/1024)}KB)`);
      } else {
        console.log(`⚠️  ${name} — logo too small (${buffer.length}B), keeping text`);
      }
    } else {
      console.log(`⚠️  ${name} — no logo found on page`);
    }

    await page.close();
  } catch (err) {
    console.log(`❌ ${name} — error: ${err.message.slice(0, 60)}`);
  }
}

await browser.close();
console.log('\nDone!');
