// Render a built WHC report (.html) to a print-ready A4 PDF.
// Usage: node reports/whc-brand/pdf.js <report.html> <out.pdf> "<footer label>"
// Keeps each section heading with the block after it, keeps any block that fits on a page
// in one piece, lets only page-taller tables break (between rows, header repeated).
const { chromium } = require('playwright');
const path = require('path');
const [, , src, out, label = 'Web Hosting Canada'] = process.argv;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(() => document.fonts.ready);
  // A4 content box at 96 dpi: 210-28 mm wide, 297-32 mm tall.
  const PAGE_H = (297 - 32) / 25.4 * 96, PAGE_W = (210 - 28) / 25.4 * 96;
  await page.setViewportSize({ width: Math.round(PAGE_W), height: 1200 });
  await page.evaluate((PAGE_H) => {
    const h = el => el.getBoundingClientRect().height;
    // 1) small blocks stay whole; large ones flow and break between rows / cards (each of which is whole)
    document.querySelectorAll('.tbl, .co, .f, .phase, .strip, section > ul, section > p').forEach(el => {
      if (h(el) < PAGE_H * 0.45) el.style.breakInside = 'avoid';
    });
    // 2) never leave a section label / heading alone at the foot of a page:
    //    wrap label + heading (+ short intro) + the next block when that bundle is short;
    //    otherwise keep the heading with the top of the next block (caption + first row / first card row).
    document.querySelectorAll('section, .doc').forEach(sec => {
      const kids = [...sec.children];
      for (let i = 0; i < kids.length; i++) {
        const el = kids[i];
        if (!el.matches('.sl, h2, h3')) continue;
        const group = [el];
        let j = i + 1;
        while (kids[j] && (kids[j].matches('h2, h3') || (kids[j].matches('p') && h(kids[j]) < 110 && group.length < 3))) group.push(kids[j++]);
        const next = kids[j];
        const total = group.reduce((a, g) => a + h(g), 0) + (next ? h(next) : 0);
        if (next && total < PAGE_H * 0.4) {
          group.push(next);
          const wrap = document.createElement('div');
          wrap.style.display = 'grid';
          wrap.style.gap = getComputedStyle(sec).rowGap;
          wrap.style.breakInside = 'avoid';
          el.before(wrap); group.forEach(g => wrap.appendChild(g));
        } else {
          group.forEach(g => g.style.breakAfter = 'avoid');
          if (next) {
            next.style.breakBefore = 'avoid';
            // keep the caption and first two rows / first row of cards with the heading
            const cap = next.querySelector('.cap'); if (cap) cap.style.breakAfter = 'avoid';
          }
        }
        i = j - 1;
      }
    });
  }, PAGE_H);
  await page.pdf({
    path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `<div style="width:100%;font-family:'IBM Plex Mono',Menlo,monospace;font-size:7px;color:#6b707c;padding:0 14mm;display:flex;justify-content:space-between"><span>${label}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`,
  });
  await browser.close();
  console.log('wrote', out);
})();
