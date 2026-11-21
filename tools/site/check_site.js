// Optional local QA for the online book (not run in CI).
// 1) python3 tools/build_site.py
// 2) serve it under the project sub-path, e.g.
//    S=/tmp/srv; mkdir -p $S && ln -sfn "$PWD/_site" "$S/TRB-OOW-Borune" && python3 -m http.server 8765 -d "$S"
// 3) node tools/site/check_site.js [http://localhost:8765/TRB-OOW-Borune/]
// Uses the globally installed Playwright (npm root -g) and its bundled Chromium.
'use strict';
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const { chromium } = require(`${execSync('npm root -g').toString().trim()}/playwright`);

const BASE = process.argv[2] || 'http://localhost:8765/TRB-OOW-Borune/';
const SITE = path.resolve(__dirname, '..', '..', '_site');
const ORIGIN = new URL(BASE).origin;
const COLREG = 'chapters/01-navigation/1.2.1-A-colregs.html';
const P = {
  cover: 'index.html', colreg: COLREG, c111: 'chapters/01-navigation/1.1.1-celestial-navigation.html',
  c321: 'chapters/03-ship-operation/3.2.1-ship-stability.html', c17: 'chapters/01-navigation/1.7-english-and-smcp.html',
  appA: 'appendices/A-glossary.html', appB: 'appendices/B-oral-exam-question-bank.html', search: 'search.html?q=Rule%2019',
};
const results = [];
function check(name, ok, detail) {
  results.push({ name, ok: !!ok, detail });
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail !== undefined ? '  — ' + (typeof detail === 'string' ? detail : JSON.stringify(detail)) : ''}`);
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function newPage(browser, opts = {}) {
  const ctx = await browser.newContext({
    viewport: { width: opts.width || 1280, height: opts.height || (opts.width && opts.width < 600 ? 812 : 860) },
    colorScheme: opts.scheme || 'light', reducedMotion: opts.reducedMotion || 'no-preference', javaScriptEnabled: opts.js !== false,
  });
  if (opts.prefs) await ctx.addInitScript(p => { try { localStorage.setItem('oow703:prefs', JSON.stringify(p)); } catch (e) {} }, opts.prefs);
  if (opts.init) await ctx.addInitScript(opts.init);
  const page = await ctx.newPage();
  page.errors = [];
  page.external = [];
  page.on('console', m => { if (m.type() === 'error') page.errors.push(m.text()); });
  page.on('pageerror', e => page.errors.push(e.message));
  page.on('request', r => { const u = r.url(); if (!u.startsWith(ORIGIN) && !u.startsWith('file:') && !u.startsWith('data:')) page.external.push(u); });
  return page;
}
async function open(page, rel, wait = 'load') {
  await page.goto(BASE + rel, { waitUntil: wait });
  await page.evaluate(() => document.fonts.ready);
}

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });

  // ---- R2: every page, no external requests, no console errors
  {
    const page = await newPage(browser);
    const htmls = [];
    (function walk(d) { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); if (fs.statSync(p).isDirectory()) walk(p); else if (f.endsWith('.html') && f !== '404.html') htmls.push(path.relative(SITE, p)); } })(SITE);
    for (const h of htmls.sort()) { await open(page, h.split(path.sep).join('/')); }
    await open(page, 'search.html?q=ไฟเรือ'); await sleep(600);
    check('R2 no external requests on all pages', page.external.length === 0, page.external.slice(0, 3));
    check('R2 no console/page errors on all pages', page.errors.length === 0, page.errors.slice(0, 3));
    await page.context().close();
  }

  // ---- R1: no horizontal page scroll
  {
    const bad = [];
    for (const scheme of ['light', 'sepia', 'dark']) {
      for (const width of [360, 390, 768, 1024, 1280, 1440]) {
        const page = await newPage(browser, { width, scheme: scheme === 'dark' ? 'dark' : 'light', prefs: scheme === 'sepia' ? { theme: 'sepia' } : undefined });
        for (const [k, rel] of Object.entries(P)) {
          await open(page, rel); await sleep(150);
          const [sw, iw] = await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
          if (sw > iw) bad.push(`${scheme} ${width} ${k} ${sw}>${iw}`);
        }
        await page.context().close();
      }
    }
    for (const width of [390, 1280]) {
      const page = await newPage(browser, { width, prefs: { step: 4 } });
      for (const [k, rel] of Object.entries(P)) {
        await open(page, rel); await sleep(150);
        const [sw, iw] = await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
        if (sw > iw) bad.push(`135% ${width} ${k} ${sw}>${iw}`);
      }
      await page.context().close();
    }
    check('R1 no horizontal page scroll (6 widths × 3 themes × 8 pages + 135%)', bad.length === 0, bad.slice(0, 5));
    const sp = await newPage(browser);
    await open(sp, 'chapters/01-navigation/1.1.0-passage-planning.html');
    const zero = await sp.evaluate(() => [...document.querySelectorAll('main > :is(p,ul,ol,blockquote,pre,.table-wrap) + :is(p,ul,ol,blockquote,pre,.table-wrap)')]
      .filter(e => parseFloat(getComputedStyle(e).marginTop) < 8).map(e => e.previousElementSibling.tagName + '>' + e.tagName));
    check('R7 consecutive paragraphs, lists, tables and pre blocks are spaced apart', zero.length === 0, zero.slice(0, 5));
    await sp.context().close();
  }

  // ---- R3, R4, R5, R6
  {
    const page = await newPage(browser, { width: 1280 });
    await open(page, COLREG); await sleep(300);
    const f = await page.evaluate(() => ({
      trirong: document.fonts.check('400 1em Trirong'), sarabun: document.fonts.check('700 1em Sarabun'),
      td: getComputedStyle(document.querySelector('main td')).fontFamily,
      fs: getComputedStyle(document.querySelector('main')).fontSize,
      col: document.querySelector('main > p:not(.endmark)').getBoundingClientRect().width,
      blend: getComputedStyle(document.querySelector('.fig img')).mixBlendMode,
    }));
    check('R3 Trirong 400 and Sarabun 700 loaded', f.trirong && f.sarabun, f);
    check('R3 table cells use Sarabun', /^"?Sarabun/.test(f.td), f.td);
    check('R4 1280: column 600–700px at 19px', f.col >= 600 && f.col <= 700 && f.fs === '19px', { col: f.col, fs: f.fs });
    check('R5 light figures multiply', f.blend === 'multiply', f.blend);
    await page.context().close();
    const m = await newPage(browser, { width: 390 });
    await open(m, P.c111); await sleep(200);
    const g = await m.evaluate(() => {
      const p = document.querySelector('main > p:not(.endmark)').getBoundingClientRect();
      const t = [...document.querySelectorAll('.table-wrap')].find(w => w.querySelectorAll('thead th').length === 12);
      return { fs: getComputedStyle(document.querySelector('main')).fontSize, left: p.left, right: innerWidth - p.right,
        tw: t && [t.scrollWidth, t.clientWidth], page: [document.documentElement.scrollWidth, innerWidth] };
    });
    check('R4 390: 17px, gutters ≥16px', g.fs === '17px' && g.left >= 16 && g.right >= 16, g);
    check('R6 12-column table scrolls inside its wrapper at 390px', g.tw && g.tw[0] > g.tw[1] && g.page[0] <= g.page[1], g);
    await m.context().close();
    const dk = await newPage(browser, { width: 1280, scheme: 'dark' });
    await open(dk, COLREG);
    const k = await dk.evaluate(() => ({ filter: getComputedStyle(document.querySelector('.fig-link')).filter, img: getComputedStyle(document.querySelector('.fig img')).filter,
      plate: getComputedStyle(document.querySelector('.fig-link')).backgroundColor, edge: getComputedStyle(document.documentElement).getPropertyValue('--edge') }));
    check('R5 dark: plate and figure dimmed together (no seam), no invert/hue-rotate', /brightness/.test(k.filter) && k.img === 'none' && !/invert|hue-rotate/.test(k.filter) && k.plate === 'rgb(255, 255, 255)', k);
    check('R5 dark: table/pre scroll shadow is light on the dark page', /255\s*,\s*255\s*,\s*255/.test(k.edge), k.edge);
    await dk.context().close();
  }

  // ---- R7: CLS
  for (const width of [390, 1280]) {
    const page = await newPage(browser, { width, init: () => {
      window.__cls = 0;
      new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
    } });
    await page.goto(BASE + COLREG, { waitUntil: 'load' }); await sleep(1500);
    const cls = await page.evaluate(() => window.__cls);
    check(`R7 CLS on COLREG at ${width}px ≤ 0.1`, cls <= 0.1, cls.toFixed(4));
    await page.context().close();
  }

  // ---- F1 theme
  {
    const page = await newPage(browser, { scheme: 'dark' });
    await open(page, COLREG);
    const auto = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    check('F1 auto follows prefers-color-scheme: dark', auto === 'rgb(4, 12, 24)', auto);
    await page.click('.aa-btn');
    await page.click('label:has(input[value="sepia"])');
    const meta = await page.evaluate(() => [document.documentElement.dataset.theme, document.querySelector('meta[name=theme-color]').content]);
    check('F1 sepia sets data-theme and theme-color', meta[0] === 'sepia' && meta[1].toUpperCase() === '#F3EBD9', meta);
    await page.keyboard.press('Escape');
    let atDCL = null;
    page.once('domcontentloaded', async () => {});
    await page.goto(BASE + P.c111, { waitUntil: 'domcontentloaded' });
    atDCL = await page.evaluate(() => document.documentElement.dataset.theme);
    check('F1 sepia persists across navigation, applied at DOMContentLoaded', atDCL === 'sepia', atDCL);
    await page.reload({ waitUntil: 'domcontentloaded' });
    check('F1 sepia persists after reload', (await page.evaluate(() => document.documentElement.dataset.theme)) === 'sepia');
    await page.context().close();
  }

  // ---- F2 size and face
  {
    const page = await newPage(browser);
    await open(page, COLREG);
    const fs0 = await page.evaluate(() => parseFloat(getComputedStyle(document.querySelector('main')).fontSize));
    await page.click('.aa-btn');
    const plus = page.locator('#prefs button[data-step="1"]'), minus = page.locator('#prefs button[data-step="-1"]');
    const seen = [];
    for (let i = 0; i < 3; i++) { await plus.click(); seen.push(await page.textContent('#prefs output')); }
    const isOff = l => l.getAttribute('aria-disabled').then(v => v === 'true');
    const plusDisabled = await isOff(plus);
    await plus.focus(); await page.keyboard.press('Enter');
    const kept0 = await page.evaluate(() => [document.querySelector('#prefs output').textContent, document.activeElement.getAttribute('data-step')]);
    check('F2 at 135% ก+ does nothing and keeps keyboard focus', kept0[0] === '135%' && kept0[1] === '1', kept0);
    const fs1 = await page.evaluate(() => parseFloat(getComputedStyle(document.querySelector('main')).fontSize));
    for (let i = 0; i < 4; i++) { if (!(await isOff(minus))) await minus.click(); }
    seen.push(await page.textContent('#prefs output'));
    const minusDisabled = await isOff(minus);
    check('F2 steps 110/120/135 … 90 and disables at ends', seen.join(',') === '110%,120%,135%,90%' && plusDisabled && minusDisabled, seen);
    check('F2 font size grows', fs1 > fs0 * 1.3, [fs0, fs1]);
    await page.click('label:has(input[value="sans"])');
    const fam = await page.evaluate(() => getComputedStyle(document.querySelector('main p')).fontFamily);
    check('F2 แบบเรียบ switches prose to Sarabun', /^"?Sarabun/.test(fam), fam);
    await page.reload();
    const kept = await page.evaluate(() => [document.documentElement.style.getPropertyValue('--scale'), document.documentElement.dataset.face]);
    check('F2 size and face persist', kept[0] === '0.9' && kept[1] === 'sans', kept);
    await page.context().close();
  }

  // ---- F3 drawer
  {
    const page = await newPage(browser, { width: 1280 });
    await open(page, COLREG);
    await page.click('.toc-btn'); await sleep(350);
    const st = await page.evaluate(() => ({ open: document.getElementById('toc-drawer').open, cur: document.activeElement.getAttribute('aria-current'), href: document.activeElement.getAttribute('href') }));
    check('F3 drawer opens modal with focus on current row', st.open && st.cur === 'page', st);
    await page.keyboard.press('Escape'); await sleep(400);
    const cl = await page.evaluate(() => ({ open: document.getElementById('toc-drawer').open, focus: document.activeElement.classList.contains('toc-btn') }));
    check('F3 Esc closes and returns focus to the button', !cl.open && cl.focus, cl);
    await page.keyboard.press('t'); await sleep(350);
    const t1 = await page.evaluate(() => document.getElementById('toc-drawer').open);
    await page.keyboard.press('t'); await sleep(400);
    const t2 = await page.evaluate(() => document.getElementById('toc-drawer').open);
    check('F3 t toggles the drawer', t1 && !t2, [t1, t2]);
    await page.focus('.toc-btn'); await page.keyboard.press('Enter'); await sleep(400);
    await page.evaluate(() => { const a = [...document.querySelectorAll('#toc-drawer a[href^="#"]')].find(x => /Part B/.test(x.textContent)); a.focus(); });
    await page.keyboard.press('Enter'); await sleep(700);
    const fo = await page.evaluate(() => [location.hash.slice(1), document.activeElement.id]);
    check('F3 choosing a section in the drawer moves keyboard focus to it', fo[0] && decodeURIComponent(fo[0]) === fo[1], fo);
    await page.click('.aa-btn'); await page.click('label:has(input[name="keys"][value="off"])'); await page.keyboard.press('Escape'); await sleep(200);
    await page.evaluate(() => document.activeElement.blur()); await page.keyboard.press('t'); await sleep(350);
    const off = await page.evaluate(() => document.getElementById('toc-drawer').open);
    await page.keyboard.press('Slash'); await sleep(300);
    check('F3 แป้นลัด ปิด turns off t and /', !off && !page.url().includes('search.html'), [off, page.url()]);
    await page.context().close();
    const narrow = await newPage(browser, { width: 360 });
    await open(narrow, COLREG);
    await narrow.evaluate(() => window.scrollTo({ top: 6000, behavior: 'instant' })); await sleep(300);
    await narrow.evaluate(() => window.scrollBy({ top: -40, behavior: 'instant' })); await sleep(300);
    const hit = await narrow.evaluate(() => { const b = document.querySelector('.toc-btn').getBoundingClientRect(); const e = document.elementFromPoint(b.left + b.width / 2, b.top + b.height / 2); return !!(e && e.closest('.toc-btn')); });
    check('F3 360px: running head never covers the สารบัญ button', hit, hit);
    await narrow.click('.toc-btn'); await sleep(400);
    const y0 = await narrow.evaluate(() => scrollY);
    await narrow.mouse.move(345, 400); await narrow.mouse.wheel(0, 600); await sleep(300);
    const nd = await narrow.evaluate(() => ({ here: !!document.activeElement.closest('.toc-here'), exp: document.querySelector('.toc-btn').getAttribute('aria-expanded') }));
    nd.dy = (await narrow.evaluate(() => scrollY)) - y0;
    check('F3 360px: drawer opens at ในบทนี้, page behind does not scroll, aria-expanded', nd.here && nd.dy === 0 && nd.exp === 'true', nd);
    await narrow.context().close();
    const nj = await newPage(browser, { js: false });
    await open(nj, COLREG);
    await nj.click('.toc-btn');
    await nj.waitForLoadState('load');
    check('F3 without JS the button goes to index.html#toc', nj.url().endsWith('/index.html#toc'), nj.url());
    await nj.context().close();
  }

  // ---- F4 outline, F5 progress/header/runhead
  {
    const page = await newPage(browser, { width: 1280 });
    await open(page, COLREG); await sleep(300);
    const o = await page.evaluate(() => {
      const a = document.querySelector('aside.outline'), r = a.getBoundingClientRect();
      const text = document.querySelector('.opener').getBoundingClientRect();
      const figs = [...document.querySelectorAll('.fig')].map(f => f.getBoundingClientRect().right);
      return { vis: getComputedStyle(a).display !== 'none', left: r.left, textRight: text.right, figRight: Math.max(...figs),
        run: document.querySelector('.runhead').textContent, p: getComputedStyle(document.querySelector('.progress span')).transform };
    });
    check('F4 outline visible at 1280 and clear of text/figures', o.vis && o.left >= o.textRight && o.left >= o.figRight, o);
    const clash = [];
    for (const width of [1280, 1366, 1440, 1920, 2560]) for (const step of [0, 1, 4]) {
      const wp = await newPage(browser, { width, prefs: { step } });
      for (const rel of [COLREG, P.c111]) {
        await open(wp, rel); await sleep(250);
        const r = await wp.evaluate(() => {
          const a = document.querySelector('aside.outline').getBoundingClientRect();
          if (!a.width) return null;
          const right = Math.max(...[...document.querySelectorAll('.prose > .fig, .prose > .t-wide, .prose > pre')].map(e => e.getBoundingClientRect().right));
          return { gap: Math.round(a.left - right), out: Math.round(a.right), vw: document.documentElement.clientWidth };
        });
        if (r && (r.gap < 16 || r.out > r.vw)) clash.push({ width, step, rel, ...r });
      }
      await wp.context().close();
    }
    check('F4 outline never overlaps wide figures/tables/pre (1280–2560px, 90–135%)', clash.length === 0, clash.slice(0, 3));
    check('F5 running head empty while opener is visible', o.run === '', o.run);
    await page.evaluate(() => { const h = document.querySelector('#rule-10--traffic-separation-schemes-เขตแบ่งแนวจราจร'); window.scrollTo({ top: h.getBoundingClientRect().top + scrollY - 100, behavior: 'instant' }); });
    await sleep(500);
    const s1 = await page.evaluate(() => ({ active: (document.querySelector('aside .is-active') || {}).textContent, run: document.querySelector('.runhead').textContent, hidden: document.documentElement.classList.contains('header-hidden') }));
    check('F4 scrolling updates active outline item and running head', /Rule 10/.test(s1.active || '') && /^1\.2\.1-A · /.test(s1.run), s1);
    check('F5 header hides on scroll down', s1.hidden, s1.hidden);
    await page.evaluate(() => window.scrollBy({ top: -300, behavior: 'instant' })); await sleep(500);
    check('F5 header returns on scroll up', !(await page.evaluate(() => document.documentElement.classList.contains('header-hidden'))));
    await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' })); await sleep(300);
    const p0 = await page.evaluate(() => getComputedStyle(document.querySelector('.progress span')).getPropertyValue('--p'));
    await page.evaluate(() => window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'instant' })); await sleep(400);
    const p1 = await page.evaluate(() => getComputedStyle(document.querySelector('.progress span')).getPropertyValue('--p'));
    check('F5 progress ~0 at top and ~1 at end', parseFloat(p0) < 0.02 && parseFloat(p1) > 0.98, [p0, p1]);
    await page.context().close();
    const sm = await newPage(browser, { width: 1024 });
    await open(sm, COLREG);
    const hidden = await sm.evaluate(() => getComputedStyle(document.querySelector('aside.outline')).display === 'none');
    await sm.click('.toc-btn'); await sleep(300);
    const here = await sm.evaluate(() => !!document.querySelector('#toc-drawer .toc-here .ol-list a'));
    check('F4 below 1280 the aside is hidden and the drawer has ในบทนี้', hidden && here, { hidden, here });
    await sm.context().close();
  }

  // ---- F6 self-test
  {
    const nj = await newPage(browser, { js: false });
    await open(nj, COLREG);
    const vis = await nj.evaluate(() => [...document.querySelectorAll('.qa-a')].every(a => a.getBoundingClientRect().height > 0));
    check('F6 answers visible without JS', vis);
    await nj.context().close();
    const page = await newPage(browser);
    await open(page, COLREG);
    const v0 = await page.evaluate(() => [...document.querySelectorAll('.qa-a')].every(a => !a.hasAttribute('hidden')));
    check('F6 answers visible by default', v0);
    await page.click('.qa-switch');
    const st = await page.evaluate(() => ({ n: document.querySelectorAll('.qa-a').length, hidden: document.querySelectorAll('.qa-a[hidden]').length, btn: document.querySelectorAll('.qa-reveal').length, txt: (document.querySelector('.qa-reveal') || {}).textContent }));
    check('F6 switch hides every answer and adds reveal buttons', st.hidden === st.n && st.btn === st.n && st.txt === 'ดูแนวตอบ', st);
    await page.click('.qa-reveal');
    const one = await page.evaluate(() => document.querySelectorAll('.qa-a[hidden]').length);
    check('F6 a reveal button shows only that answer', one === st.n - 1, one);
    const desc = await page.evaluate(() => { const ids = [...document.querySelectorAll('.qa-reveal')].map(b => b.getAttribute('aria-describedby')); return ids.every(i => i && document.getElementById(i)) && new Set(ids).size === ids.length; });
    check('F6 each reveal button is described by its own question', desc);
    await page.emulateMedia({ media: 'print' });
    const pr = await page.evaluate(() => [...document.querySelectorAll('.qa-a')].every(a => a.getBoundingClientRect().height > 0)
      && ['.site-header', '.drawer', '.outline', '.pager', '.qa-tools'].every(s => getComputedStyle(document.querySelector(s)).display === 'none'));
    check('F6/F11 print shows all answers and hides chrome', pr);
    await page.emulateMedia({ media: 'screen' });
    await open(page, P.c111);
    const persisted = await page.evaluate(() => document.querySelectorAll('.qa-a[hidden]').length > 0 && document.querySelector('.qa-switch').getAttribute('aria-checked') === 'true');
    check('F6 self-test mode persists to another chapter', persisted);
    await page.context().close();
    const bp = await newPage(browser, { reducedMotion: 'reduce' });
    await open(bp, P.appB);
    const jump = await bp.evaluate(async () => {
      const s = document.querySelectorAll('.qa-switch')[20];
      s.scrollIntoView({ block: 'center' }); await new Promise(r => setTimeout(r, 150));
      const a = s.getBoundingClientRect().top; s.click(); await new Promise(r => setTimeout(r, 200));
      const b = s.getBoundingClientRect().top; s.click(); await new Promise(r => setTimeout(r, 200));
      return [a, b, s.getBoundingClientRect().top].map(Math.round);
    });
    check('F6 a switch far down appendix B stays under the pointer when toggled', Math.abs(jump[1] - jump[0]) <= 2 && Math.abs(jump[2] - jump[0]) <= 2, jump);
    const sec = await bp.evaluate(() => {
      const bad = []; let cur = null;
      for (const el of document.getElementById('main').children) {
        if (/^H[23]$/.test(el.tagName)) { cur = { h: el.textContent.slice(0, 40), qa: 0, n: null }; bad.push(cur); }
        else if (cur && el.classList.contains('qa-tools')) cur.n = parseInt(el.textContent, 10);
        else if (cur && el.classList.contains('qa')) cur.qa++;
      }
      return bad.filter(x => x.qa && x.n !== x.qa);
    });
    check('F6 every heading section with Q&A has a tools bar with the right count', sec.length === 0, sec.slice(0, 3));
    await bp.context().close();
  }

  // ---- F7 keyboard
  {
    const page = await newPage(browser);
    await open(page, COLREG);
    await Promise.all([page.waitForURL(/1\.2\.1-B/, { timeout: 5000 }).catch(() => {}), page.keyboard.press('ArrowRight')]);
    const r = page.url();
    await open(page, COLREG);
    await Promise.all([page.waitForURL(/1\.1\.7/, { timeout: 5000 }).catch(() => {}), page.keyboard.press('ArrowLeft')]);
    const l = page.url();
    check('F7 → 1.2.1-B, ← 1.1.7', r.endsWith('1.2.1-B-watchkeeping-principles.html') && l.endsWith('1.1.7-meteorology.html'), [r, l]);
    await open(page, COLREG);
    await page.focus('.table-wrap');
    await page.keyboard.press('ArrowRight'); await sleep(300);
    const t = page.url();
    await page.evaluate(() => document.activeElement.blur());
    await page.keyboard.press('Alt+ArrowRight'); await sleep(300);
    const m = page.url();
    check('F7 ignored inside .table-wrap and with modifiers', t.endsWith(COLREG) && m.endsWith(COLREG), [t, m]);
    await Promise.all([page.waitForURL(/search\.html$/, { timeout: 5000 }).catch(() => {}), page.keyboard.press('/')]);
    check('F7 / opens search', page.url().endsWith('/search.html'), page.url());
    await page.focus('#q'); await page.keyboard.press('ArrowLeft'); await sleep(300);
    check('F7 ignored in the search input', page.url().endsWith('/search.html'));
    await page.context().close();
  }

  // ---- F8 continue reading + broken storage
  {
    const page = await newPage(browser);
    await open(page, COLREG);
    await page.evaluate(() => window.scrollTo({ top: document.documentElement.scrollHeight / 2, behavior: 'instant' })); await sleep(2600);
    await open(page, 'index.html'); await sleep(200);
    const c = await page.evaluate(() => { const a = document.querySelector('.continue'); return { shown: getComputedStyle(a).display !== 'none', href: a.getAttribute('href'), s: a.querySelector('.c-s').textContent, t: a.querySelector('.c-t').textContent }; });
    check('F8 continue card links to COLREG#heading with %', c.shown && c.href.startsWith(COLREG + '#') && /อ่านแล้ว \d+%/.test(c.s), c);
    await page.context().close();
    const broken = await newPage(browser, { init: () => { Storage.prototype.getItem = () => { throw new Error('blocked'); }; Storage.prototype.setItem = () => { throw new Error('blocked'); }; } });
    for (const rel of Object.values(P)) await open(broken, rel);
    await open(broken, COLREG);
    await broken.click('.aa-btn'); await broken.click('label:has(input[value="dark"])'); await broken.keyboard.press('Escape');
    await broken.click('.qa-switch');
    await broken.evaluate(() => window.scrollTo({ top: 3000, behavior: 'instant' })); await sleep(2300);
    check('F8 pages work with throwing Storage, no console errors', broken.errors.length === 0 && (await broken.evaluate(() => document.documentElement.dataset.theme)) === 'dark', broken.errors.slice(0, 3));
    await broken.context().close();
  }

  // ---- F9 search
  {
    const page = await newPage(browser);
    await open(page, 'search.html?q=Rule%2019'); await page.waitForSelector('.sr-doc', { timeout: 5000 });
    const r = await page.evaluate(() => ({ docs: [...document.querySelectorAll('.sr-doc a')].map(a => a.getAttribute('href')), first: document.querySelector('.sr-title').getAttribute('href') }));
    check('F9 Rule 19 lists COLREG', r.docs.includes(COLREG), r.docs.slice(0, 3));
    const links = await page.evaluate(() => [...document.querySelectorAll('.sr-title')].slice(0, 40).map(a => a.getAttribute('href')));
    const missing = [];
    for (const href of links) {
      const [p, frag] = href.split('#');
      const id = decodeURIComponent((frag || '').split(':~:')[0]);
      const html = fs.readFileSync(path.join(SITE, p), 'utf8');
      if (id && !html.includes(`id="${id}"`)) missing.push(href);
    }
    check('F9 result link targets exist', missing.length === 0, missing.slice(0, 3));
    await page.fill('#q', 'ไฟเรือ'); await sleep(700);
    const th = await page.evaluate(() => ({ n: document.querySelectorAll('.sr-list li').length, marks: document.querySelectorAll('.sr-snip mark').length,
      badStart: [...document.querySelectorAll('.sr-snip')].filter(s => /^…?[ัิ-ฺ็-๎]/.test(s.textContent)).length,
      d: [...document.querySelectorAll('.sr-doc a')].some(a => /D-review/.test(a.getAttribute('href'))) }));
    check('F9 Thai query with <mark>, no snippet starts with a combining mark', th.n > 0 && th.marks > 0 && th.badStart === 0, th);
    await page.fill('#q', 'COLREG'); await sleep(700);
    const qa = await page.evaluate(() => { const t = document.querySelector('.sr-tag'); const a = t && t.parentNode.querySelector('.sr-title'); return { tag: t && t.textContent, href: a && a.getAttribute('href'), d: [...document.querySelectorAll('.sr-doc a')].some(a => /D-review/.test(a.getAttribute('href'))) }; });
    check('F9 Q&A hit is tagged คำถาม and links to #qa-…', qa.tag === 'คำถาม' && /#qa-[0-9a-f]{8}/.test(qa.href || ''), qa);
    check('F9 appendix D never appears', !th.d && !qa.d);
    await page.context().close();
    const fp = await newPage(browser);
    await fp.goto('file://' + path.join(SITE, 'search.html') + '?q=COLREG'); await sleep(1200);
    const fr = await fp.evaluate(() => document.querySelectorAll('.sr-list li').length);
    check('F9/L5 search works from file://', fr > 0, fr);
    await fp.goto('file://' + path.join(SITE, 'index.html'));
    const css = await fp.evaluate(() => getComputedStyle(document.body).backgroundColor);
    await fp.click('.toc-btn'); await sleep(300);
    const dopen = await fp.evaluate(() => document.getElementById('toc-drawer').open);
    await fp.goto('file://' + path.join(SITE, COLREG)); await fp.evaluate(() => document.fonts.ready);
    const imgs = await fp.evaluate(async () => { const i = document.querySelector('.fig img'); i.loading = 'eager'; await i.decode().catch(() => {}); return [i.naturalWidth, document.fonts.check('400 1em Trirong')]; });
    check('L5 file:// no console errors (font preloads are skipped off http)', fp.errors.length === 0, fp.errors.slice(0, 3));
    check('L5 file:// css, drawer, images and fonts', css === 'rgb(244, 247, 250)' && dopen && imgs[0] > 0 && imgs[1], { css, dopen, imgs });
    await fp.context().close();
  }

  // ---- F10 404
  {
    const page = await newPage(browser);
    const four = fs.readFileSync(path.join(SITE, '404.html'), 'utf8');
    await page.route('**/*', async (route) => {
      const resp = await route.fetch();
      if (resp.status() === 404) await route.fulfill({ status: 404, contentType: 'text/html', body: four }); else await route.fulfill({ response: resp });
    });
    await page.goto(BASE + 'nope');
    const home = await page.evaluate(() => document.getElementById('go-home').getAttribute('href'));
    check('F10 404 home link under sub-path', home === new URL(BASE).pathname + 'index.html', home);
    await page.goto(BASE + 'chapters/01-navigation/1.2.1-A-colregs.md'); await page.waitForLoadState('load'); await sleep(300);
    check('F10 .md redirects to .html', page.url().endsWith('1.2.1-A-colregs.html'), page.url());
    await page.goto(BASE + 'appendices/B-oral-exam-question-bank.md?x=1#q-1-4-ecdis'); await page.waitForLoadState('load'); await sleep(300);
    check('F10 .md redirect keeps ?query and #fragment', page.url().endsWith('B-oral-exam-question-bank.html?x=1#q-1-4-ecdis'), page.url());
    await page.context().close();
  }

  // ---- A1, A2, A4
  {
    const page = await newPage(browser);
    await open(page, COLREG);
    const lm = await page.evaluate(() => ({ lang: document.documentElement.lang, banner: !!document.querySelector('body > header.site-header'), main: !!document.querySelector('main'),
      foot: !!document.querySelector('body > footer'), aside: !!document.querySelector('aside[aria-label]'), pager: !!document.querySelector('nav.pager[aria-label]') }));
    check('A1 lang=th and landmarks', lm.lang === 'th' && Object.values(lm).every(Boolean), lm);
    await page.keyboard.press('Tab');
    const first = await page.evaluate(() => document.activeElement.className);
    await page.keyboard.press('Enter'); await sleep(200);
    const tgt = await page.evaluate(() => document.activeElement.id);
    check('A1 skip link is the first Tab stop and moves focus to #main', first === 'skip' && tgt === 'main', [first, tgt]);
    const rings = [];
    await page.keyboard.press('Shift+Tab');
    for (let i = 0; i < 8; i++) {
      await page.keyboard.press('Tab');
      rings.push(await page.evaluate(() => { const e = document.activeElement, s = getComputedStyle(e); return [e.tagName + '.' + e.className, s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2]; }));
    }
    check('A2 focus ring on interactive elements', rings.every(r => r[1]), rings.filter(r => !r[1]));
    const names = await page.evaluate(() => [...document.querySelectorAll('button')].map(b => {
      const vis = b.textContent.replace(/\s+/g, ' ').trim(); const lbl = b.getAttribute('aria-label');
      return { vis, ok: !lbl || lbl.includes(vis) };
    }).filter(b => !b.vis || !b.ok));
    check('A2 buttons have accessible names containing visible text', names.length === 0, names.slice(0, 3));
    await page.context().close();
    const rm = await newPage(browser, { reducedMotion: 'reduce' });
    await open(rm, COLREG);
    const mo = await rm.evaluate(() => ({ drawer: getComputedStyle(document.querySelector('.drawer')).transitionDuration, header: getComputedStyle(document.querySelector('.site-header')).transitionDuration, sb: getComputedStyle(document.documentElement).scrollBehavior }));
    check('A4 reduced motion: no transitions, scroll-behavior auto', /^0s/.test(mo.drawer) && /^0s/.test(mo.header) && mo.sb === 'auto', mo);
    await rm.context().close();
  }

  // ---- A3 contrast tokens
  {
    const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16) / 255).map(c => c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
    const L = h => { const [r, g, b] = hex(h); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
    const ratio = (a, b) => { const x = L(a), y = L(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
    const css = fs.readFileSync(path.join(SITE, 'assets/style.css'), 'utf8');
    const block = sel => { const i = css.indexOf(sel + '{'); const s = css.slice(i, css.indexOf('}', i)); const o = {}; for (const m of s.matchAll(/--([a-z-0-9]+):(#[0-9A-Fa-f]{6})/g)) o[m[1]] = m[2]; return o; };
    const light = block(':root'), sepia = { ...light, ...block(':root[data-theme="sepia"]') }, dark = block(':root[data-theme="dark"]');
    const low = [];
    for (const [n, t] of Object.entries({ light, sepia, dark })) for (const fg of ['ink', 'muted', 'link', 'rubric']) for (const bg of ['paper', 'paper-2']) {
      const r = ratio(t[fg], t[bg]); if (r < 4.5) low.push(`${n} ${fg}/${bg} ${r.toFixed(2)}`);
    }
    check('A3 text tokens ≥ 4.5:1 in all themes', low.length === 0, low);
  }

  await browser.close();
  const failed = results.filter(r => !r.ok);
  console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
  process.exit(failed.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
