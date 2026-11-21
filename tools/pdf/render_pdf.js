// แปลงไฟล์ HTML ของสมุดเป็น PDF ด้วย Chromium (Playwright)
// ใช้: PWPATH=$(npm root -g)/playwright node tools/pdf/render_pdf.js <input.html> <output.pdf>
const { chromium } = require(process.env.PWPATH || 'playwright');
const path = require('path');

const header = `<div style="width:100%;font-size:7.5px;color:#64748b;padding:0 16mm;display:flex;justify-content:space-between;font-family:'Sarabun','DejaVu Sans',sans-serif;">
  <span>OOW Training Notebook · IMO Model Course 7.03 / STCW A-II/1</span><span>TIRAPHONG NANTAPAN</span></div>`;
const footer = `<div style="width:100%;font-size:8px;color:#475569;text-align:center;font-family:'Sarabun','DejaVu Sans',sans-serif;">
  <span class="pageNumber"></span> / <span class="totalPages"></span></div>`;

(async () => {
  const [input, output] = process.argv.slice(2);
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'load', timeout: 0 });
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all(Array.from(document.images).map(img => img.complete ? null : new Promise(r => { img.onload = img.onerror = r; })));
  });
  await page.pdf({
    path: output, format: 'A4', printBackground: true, outline: true, tagged: true,
    displayHeaderFooter: true, headerTemplate: header, footerTemplate: footer,
    margin: { top: '17mm', bottom: '16mm', left: '16mm', right: '16mm' }, timeout: 0,
  });
  await browser.close();
  console.log('pdf written', output);
})();
