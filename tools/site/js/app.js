/* หน้ากระดาษ — reader behaviour (vanilla ES2018). Pages read fine without it. */
(function () {
  'use strict';
  var d = document, w = window, root = d.documentElement;
  var main = d.getElementById('main');
  var header = d.querySelector('.site-header');
  var isDoc = d.body.classList.contains('page-doc');
  var isCover = d.body.classList.contains('page-cover');
  var isSearch = d.body.classList.contains('page-search');
  var siteRoot = root.getAttribute('data-root') || '';
  var STEPS = [0.9, 1, 1.1, 1.2, 1.35];
  var motionQuery = w.matchMedia ? w.matchMedia('(prefers-reduced-motion: reduce)') : null;
  function reducedMotion() { return !!(motionQuery && motionQuery.matches); }

  /* 1. storage with an in-memory fallback */
  var memory = new Map();
  var store = {
    get: function (key, fallback) {
      var raw = null;
      try { raw = w.localStorage.getItem(key); } catch (e) { raw = null; }
      if (raw == null && memory.has(key)) raw = memory.get(key);
      if (raw == null) return fallback;
      try { var v = JSON.parse(raw); return v == null ? fallback : v; } catch (e) { return fallback; }
    },
    set: function (key, value) {
      var raw = JSON.stringify(value);
      memory.set(key, raw);
      try { w.localStorage.setItem(key, raw); } catch (e) {}
    }
  };

  var saved = store.get('oow703:prefs', {});
  if (typeof saved !== 'object' || saved === null) saved = {};
  var prefs = {
    theme: /^(auto|light|sepia|dark)$/.test(saved.theme) ? saved.theme : 'auto',
    step: (saved.step >= 0 && saved.step < STEPS.length && saved.step % 1 === 0) ? saved.step : 1,
    face: saved.face === 'sans' ? 'sans' : 'book',
    selftest: saved.selftest === true,
    keys: saved.keys === 'off' ? 'off' : 'on'      /* single-key shortcuts can be switched off (WCAG 2.1.4) */
  };
  function savePrefs() { store.set('oow703:prefs', prefs); }

  function anyDialogOpen() { return !!d.querySelector('dialog[open]'); }

  /* 2. reading preferences (Aa) */
  var prefsDialog = d.getElementById('prefs');
  var aaBtn = d.querySelector('.aa-btn');
  var themeMetas = d.querySelectorAll('meta[name="theme-color"]');

  function applyTheme() {
    if (prefs.theme === 'auto') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', prefs.theme);
    var paper = prefs.theme === 'auto' ? '' : getComputedStyle(root).getPropertyValue('--paper').trim();
    if (themeMetas[0]) themeMetas[0].setAttribute('content', paper || '#FCFBF8');
    if (themeMetas[1]) themeMetas[1].setAttribute('content', paper || '#1A1917');
  }
  function applyFace() {
    if (prefs.face === 'sans') root.setAttribute('data-face', 'sans');
    else root.removeAttribute('data-face');
  }
  function applySize() {
    var s = STEPS[prefs.step];
    if (s === 1) root.style.removeProperty('--scale');
    else root.style.setProperty('--scale', String(s));
    if (!prefsDialog) return;
    var out = prefsDialog.querySelector('output');
    if (out) out.textContent = Math.round(s * 100) + '%';
    var minus = prefsDialog.querySelector('[data-step="-1"]');
    var plus = prefsDialog.querySelector('[data-step="1"]');
    /* aria-disabled, not disabled: a disabled button would drop keyboard focus out of the open dialog */
    if (minus) minus.setAttribute('aria-disabled', prefs.step <= 0 ? 'true' : 'false');
    if (plus) plus.setAttribute('aria-disabled', prefs.step >= STEPS.length - 1 ? 'true' : 'false');
  }
  function syncPrefsForm() {
    if (!prefsDialog) return;
    var radios = prefsDialog.querySelectorAll('input[type="radio"]');
    for (var i = 0; i < radios.length; i++) {
      var r = radios[i];
      r.checked = prefs[r.name] === r.value;
    }
    applySize();
  }
  applyTheme();
  applyFace();
  syncPrefsForm();

  if (prefsDialog && aaBtn && typeof prefsDialog.showModal === 'function') {
    aaBtn.addEventListener('click', function () {
      syncPrefsForm();
      if (!prefsDialog.open) prefsDialog.showModal();
    });
    prefsDialog.addEventListener('change', function (e) {
      var t = e.target;
      if (t.name === 'theme') { prefs.theme = t.value; applyTheme(); }
      else if (t.name === 'face') { prefs.face = t.value; applyFace(); }
      else if (t.name === 'keys') { prefs.keys = t.value === 'off' ? 'off' : 'on'; }
      else return;
      savePrefs();
      layoutChanged();
    });
    prefsDialog.addEventListener('click', function (e) {
      if (e.target === prefsDialog) { prefsDialog.close(); return; }
      var b = e.target.closest('button[data-step]');
      if (!b) return;
      var next = Math.max(0, Math.min(STEPS.length - 1, prefs.step + Number(b.getAttribute('data-step'))));
      if (next === prefs.step) return;
      prefs.step = next;
      applySize();
      savePrefs();
      layoutChanged();
    });
    prefsDialog.addEventListener('close', function () { aaBtn.focus(); });
  }
  if (w.matchMedia) {
    var schemeQuery = w.matchMedia('(prefers-color-scheme: dark)');
    if (schemeQuery.addEventListener) schemeQuery.addEventListener('change', function () { if (prefs.theme === 'auto') applyTheme(); });
  }

  /* 3. TOC drawer */
  var drawer = d.getElementById('toc-drawer');
  var tocBtn = d.querySelector('.toc-btn');
  var drawerTimer = 0;
  var hasDialog = !!(drawer && typeof drawer.showModal === 'function');

  var pendingFocus = '';
  var outlineAside = d.querySelector('aside.outline');
  function outlineShown() { return !!(outlineAside && outlineAside.getClientRects().length); }
  function setExpanded(on) { if (hasDialog && tocBtn) tocBtn.setAttribute('aria-expanded', on ? 'true' : 'false'); }

  function openDrawer() {
    if (!hasDialog) return false;
    if (drawer.open) return true;
    clearTimeout(drawerTimer);
    drawer.showModal();
    void drawer.offsetWidth;
    drawer.classList.add('is-open');
    setExpanded(true);
    /* when the in-page outline is not on screen, the drawer is the way to it: open at "ในบทนี้" */
    var here = drawer.querySelector('.toc-here'), target = null, toTop = false;
    if (here && !outlineShown()) {
      target = here.querySelector('a.is-active');
      if (!target) { target = here.querySelector('a'); toTop = true; }
    }
    if (!target) target = drawer.querySelector('nav [aria-current="page"]') || drawer.querySelector('nav a');
    if (target) {
      target.focus({ preventScroll: true });
      if (toTop) drawer.querySelector('.drawer-in').scrollTop = 0;
      else target.scrollIntoView({ block: 'center' });
    }
    root.classList.remove('header-hidden');
    return true;
  }
  function focusTarget(id) {
    var el = null;
    try { el = d.getElementById(decodeURIComponent(id)); } catch (e) { el = d.getElementById(id); }
    if (!el) return false;
    if (!el.hasAttribute('tabindex') && !/^(A|BUTTON|INPUT|SELECT|TEXTAREA)$/.test(el.tagName)) el.setAttribute('tabindex', '-1');
    el.focus({ preventScroll: true });
    return true;
  }
  function closeDrawer(returnFocus) {
    if (!hasDialog || !drawer.open) return;
    drawer.classList.remove('is-open');
    setExpanded(false);
    var done = function () {
      if (drawer.open) drawer.close();
      /* an in-page link was chosen: keyboard focus continues from that section, not from the header button */
      if (pendingFocus) { var id = pendingFocus; pendingFocus = ''; if (focusTarget(id)) return; }
      if (returnFocus !== false && tocBtn) tocBtn.focus({ preventScroll: true });
    };
    if (reducedMotion()) done(); else drawerTimer = setTimeout(done, 220);
  }

  if (hasDialog && tocBtn) {
    /* with JS the link opens a modal dialog, so it is announced and operated as a button */
    tocBtn.setAttribute('role', 'button');
    tocBtn.setAttribute('aria-haspopup', 'dialog');
    setExpanded(false);
    tocBtn.addEventListener('click', function (e) { if (openDrawer()) e.preventDefault(); });
    tocBtn.addEventListener('keydown', function (e) {
      if (e.key === ' ' || e.code === 'Space') { e.preventDefault(); openDrawer(); }
    });
    drawer.addEventListener('cancel', function (e) { e.preventDefault(); closeDrawer(); });
    drawer.addEventListener('close', function () { drawer.classList.remove('is-open'); setExpanded(false); });
    drawer.addEventListener('click', function (e) {
      if (e.target === drawer || e.target.closest('.drawer-close')) { closeDrawer(); return; }
      var a = e.target.closest('a[href]');
      if (!a) return;
      var href = a.getAttribute('href');
      if (href.charAt(0) === '#') { pendingFocus = href.slice(1); closeDrawer(false); }
    });
  }

  /* 4-5. scroll: header, progress, scrollspy, running head */
  var progressBar = d.querySelector('.progress span');
  var runhead = d.querySelector('.runhead');
  var opener = d.querySelector('.opener');
  var docNum = main ? main.getAttribute('data-num') || '' : '';
  var docTitle = main ? main.getAttribute('data-title') || '' : '';
  var autoHide = isDoc || isSearch;
  var headerH = 48, lastY = w.scrollY || 0, mainTop = 0, mainHeight = 1, progress = 0;
  var heads = [], tops = [], linksById = {}, activeId = '', activeText = '', openerVisible = true, ticking = false;
  /* keyboard users keep the header (and the focused button in it) on screen; wheel, touch and mouse do not */
  var keyNav = false;
  d.addEventListener('keydown', function () { keyNav = true; }, true);
  ['pointerdown', 'wheel', 'touchstart'].forEach(function (t) {
    d.addEventListener(t, function () { keyNav = false; }, { capture: true, passive: true });
  });

  function measure() {
    headerH = header ? header.offsetHeight : 48;
    if (main) {
      var r = main.getBoundingClientRect();
      mainTop = r.top + (w.scrollY || 0);
      mainHeight = main.offsetHeight;
    }
    var y = w.scrollY || 0;
    tops = heads.map(function (h) { return h.getBoundingClientRect().top + y; });
  }

  if (isDoc && main) {
    var outlineLinks = d.querySelectorAll('.ol-list a[href^="#"]');
    for (var i = 0; i < outlineLinks.length; i++) {
      var id = outlineLinks[i].getAttribute('href').slice(1);
      (linksById[id] = linksById[id] || []).push(outlineLinks[i]);
    }
    heads = Array.prototype.slice.call(main.querySelectorAll('h2[id], h3[id]')).filter(function (h) {
      return !(h.closest && h.closest('.opener')) && linksById[h.id];
    });
  }

  function h2LinkFor(a) {
    var li = a.parentNode;
    var list = li && li.parentNode;
    if (list && !list.classList.contains('ol-list')) li = list.parentNode;
    return li;
  }

  function setActive(id) {
    if (id === activeId) return;
    var prev = linksById[activeId] || [];
    prev.forEach(function (a) { a.classList.remove('is-active'); });
    var opened = d.querySelectorAll('.ol-list li.is-open');
    for (var k = 0; k < opened.length; k++) opened[k].classList.remove('is-open');
    activeId = id;
    activeText = '';
    var links = linksById[id] || [];
    links.forEach(function (a) {
      a.classList.add('is-active');
      var li = h2LinkFor(a);
      if (li && li.tagName === 'LI') li.classList.add('is-open');
      if (outlineAside && outlineAside.contains(a)) {
        var top = a.offsetTop, ah = outlineAside.clientHeight;
        if (top < outlineAside.scrollTop + 24 || top > outlineAside.scrollTop + ah - 48) outlineAside.scrollTop = Math.max(0, top - ah / 3);
      }
    });
    if (links[0]) activeText = links[0].textContent.trim();
    updateRunhead();
  }

  function activeH2Text() {
    var links = linksById[activeId];
    if (!links || !links[0]) return '';
    var li = h2LinkFor(links[0]);
    var a = li && li.querySelector('a');
    return a ? a.textContent.trim() : '';
  }

  function updateRunhead() {
    if (!runhead || !isDoc) return;
    if (openerVisible) {
      if (runhead.textContent) runhead.textContent = '';
      runhead.classList.remove('is-on');
      return;
    }
    var h2 = activeH2Text();
    var text = h2 ? docNum + ' · ' + h2 : (docNum + ' ' + docTitle).trim();
    if (runhead.textContent !== text) runhead.textContent = text;
    runhead.classList.add('is-on');
  }

  function spy(y) {
    if (!heads.length) return;
    var line = y + headerH + w.innerHeight * 0.25;
    var idx = -1;
    for (var k = 0; k < tops.length; k++) { if (tops[k] <= line) idx = k; else break; }
    setActive(idx >= 0 ? heads[idx].id : '');
  }

  function update() {
    ticking = false;
    var y = w.scrollY || 0;
    root.classList.toggle('scrolled', y > 4);
    if (autoHide) {
      var dy = y - lastY;
      var keep = y < 2 * headerH || (keyNav && header && header.contains(d.activeElement)) || anyDialogOpen();
      if (keep) { root.classList.remove('header-hidden'); lastY = y; }
      else if (dy > 4) { if (y > 3 * headerH) root.classList.add('header-hidden'); lastY = y; }
      else if (dy < -4) { root.classList.remove('header-hidden'); lastY = y; }
    }
    if (isDoc) {
      var span = mainHeight - w.innerHeight;
      progress = span > 0 ? Math.min(1, Math.max(0, (y - mainTop) / span)) : 1;
      if (progressBar) progressBar.style.setProperty('--p', progress.toFixed(4));
      spy(y);
      saveSoon();
    }
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }

  /* the outline only shows when it fits: CSS places it beside the text or the wide column, whichever is wider,
     and narrows the wide column to leave room; here we only check that it does not run off the right edge */
  function fitOutline() {
    if (!outlineAside) return;
    root.classList.remove('no-outline');
    var r = outlineAside.getBoundingClientRect();
    root.classList.toggle('no-outline', r.width > 0 && r.right > root.clientWidth - 8);
  }
  /* tables and pre blocks are keyboard-scrollable regions only while they actually overflow */
  var scrollers = main ? main.querySelectorAll('.table-wrap, pre') : [];
  function updateScrollers() {
    var over = [], k, el;
    for (k = 0; k < scrollers.length; k++) over.push(scrollers[k].scrollWidth > scrollers[k].clientWidth + 1);
    for (k = 0; k < scrollers.length; k++) {
      el = scrollers[k];
      var wrap = el.classList.contains('table-wrap');
      if (over[k]) {
        el.setAttribute('tabindex', '0');
        if (wrap && el.hasAttribute('data-label')) {
          el.setAttribute('role', 'region');
          el.setAttribute('aria-label', el.getAttribute('data-label'));
          el.removeAttribute('data-label');
        }
      } else if (el.hasAttribute('tabindex') && el !== d.activeElement) {
        el.removeAttribute('tabindex');
        if (wrap && el.hasAttribute('aria-label')) {
          el.setAttribute('data-label', el.getAttribute('aria-label'));
          el.removeAttribute('aria-label');
          el.removeAttribute('role');
        }
      }
    }
  }
  var layoutTimer = 0;
  function layoutChanged() {
    clearTimeout(layoutTimer);
    layoutTimer = setTimeout(function () { fitOutline(); updateScrollers(); measure(); update(); }, 60);
  }

  w.addEventListener('scroll', onScroll, { passive: true });
  w.addEventListener('resize', layoutChanged, { passive: true });
  w.addEventListener('load', layoutChanged);
  w.addEventListener('load', function () { requestAnimationFrame(function () { root.classList.add('smooth-scroll'); }); });
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(layoutChanged);
  if (w.ResizeObserver && main) new ResizeObserver(layoutChanged).observe(main);
  d.addEventListener('focusin', function (e) {
    if (header && header.contains(e.target)) root.classList.remove('header-hidden');
  });

  if (isDoc && opener && runhead) {
    if (w.IntersectionObserver) {
      new IntersectionObserver(function (entries) {
        openerVisible = entries[entries.length - 1].isIntersecting;
        updateRunhead();
      }, { rootMargin: '-48px 0px 0px 0px' }).observe(opener);
    } else {
      openerVisible = false;
    }
  }
  fitOutline();
  measure();
  update();

  /* 6. keyboard */
  d.addEventListener('keydown', function (e) {
    if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey || e.isComposing || e.keyCode === 229) return;
    var t = e.target;
    if (t.closest && t.closest('input, textarea, select, [contenteditable]:not([contenteditable="false"])')) return;
    if (prefs.keys === 'off') return;
    var ae = d.activeElement;
    var inDrawer = drawer && drawer.open && ae && drawer.contains(ae);
    if (e.code === 'KeyT' && !e.shiftKey && inDrawer) { e.preventDefault(); closeDrawer(); return; }
    if (anyDialogOpen() || (ae && ae.closest && ae.closest('.table-wrap, pre'))) return;
    var link;
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
      if (e.shiftKey) return;
      link = d.querySelector(e.key === 'ArrowLeft' ? 'link[rel="prev"]' : 'link[rel="next"]');
      if (link) { e.preventDefault(); w.location.href = link.href; }
    } else if (e.key === '/' || (e.code === 'Slash' && !e.shiftKey)) {
      e.preventDefault();
      var q = d.getElementById('q');
      if (isSearch && q) { q.focus(); q.select(); }
      else w.location.href = siteRoot + 'search.html';
    } else if (e.code === 'KeyT' && !e.shiftKey) {
      if (hasDialog) { e.preventDefault(); openDrawer(); }
    }
  });

  /* 7. Q&A self-test */
  var switches = d.querySelectorAll('.qa-switch');
  var answers = d.querySelectorAll('.qa-a');
  function setSwitches(on) {
    for (var k = 0; k < switches.length; k++) switches[k].setAttribute('aria-checked', on ? 'true' : 'false');
  }
  function revealButton(a) {
    var b = a.previousElementSibling;
    return b && b.classList.contains('qa-reveal') ? b : null;
  }
  function hideAnswer(a) {
    a.setAttribute('hidden', 'until-found');
    a.removeAttribute('tabindex');
    if (!revealButton(a)) {
      var b = d.createElement('button');
      b.type = 'button';
      b.className = 'qa-reveal';
      b.setAttribute('aria-expanded', 'false');
      b.setAttribute('aria-controls', a.id);
      b.textContent = 'ดูแนวตอบ';
      var q = a.parentNode.querySelector('.qa-q');
      if (q) {
        if (!q.id) q.id = (a.parentNode.id || a.id) + '-q';
        b.setAttribute('aria-describedby', q.id);
      }
      a.parentNode.insertBefore(b, a);
    }
  }
  function revealAnswer(a, focus) {
    if (!a) return;
    a.removeAttribute('hidden');
    var b = revealButton(a);
    if (b) b.parentNode.removeChild(b);
    a.setAttribute('tabindex', '-1');
    if (focus) a.focus({ preventScroll: true });
  }
  function hideAll() { for (var k = 0; k < answers.length; k++) hideAnswer(answers[k]); layoutChanged(); }
  function showAll() {
    for (var k = 0; k < answers.length; k++) {
      answers[k].removeAttribute('hidden');
      var b = revealButton(answers[k]);
      if (b) b.parentNode.removeChild(b);
    }
    layoutChanged();
  }
  function revealFromHash() {
    var id = '';
    try { id = decodeURIComponent(w.location.hash.slice(1)); } catch (e) { id = w.location.hash.slice(1); }
    if (!id) return;
    var el = d.getElementById(id);
    if (!el) return;
    var box = el.closest('.qa'), qa = box && box.querySelector('.qa-a');
    if (qa && qa.hasAttribute('hidden')) revealAnswer(qa, false);
  }
  if (answers.length) {
    setSwitches(prefs.selftest);
    if (prefs.selftest) hideAll();
    revealFromHash();
    d.addEventListener('click', function (e) {
      if (!e.target.closest) return;
      var b = e.target.closest('.qa-reveal');
      if (b) { revealAnswer(d.getElementById(b.getAttribute('aria-controls')), true); layoutChanged(); return; }
      var s = e.target.closest('.qa-switch');
      if (s) {
        /* every switch on the page toggles every answer: keep the one that was pressed still on screen */
        var before = s.getBoundingClientRect().top;
        prefs.selftest = s.getAttribute('aria-checked') !== 'true';
        savePrefs();
        setSwitches(prefs.selftest);
        root.classList.toggle('selftest', prefs.selftest);
        if (prefs.selftest) hideAll(); else showAll();
        var dy = s.getBoundingClientRect().top - before;
        if (Math.abs(dy) > 1) {
          var sb = root.style.scrollBehavior;
          root.style.scrollBehavior = 'auto';
          w.scrollBy(0, dy);
          root.style.scrollBehavior = sb;
        }
      }
    });
    d.addEventListener('beforematch', function (e) {
      if (e.target.classList && e.target.classList.contains('qa-a')) revealAnswer(e.target, false);
    }, true);
    w.addEventListener('hashchange', revealFromHash);
    w.addEventListener('beforeprint', showAll);
    w.addEventListener('afterprint', function () { if (prefs.selftest) hideAll(); });
  }

  root.classList.add('qa-ready');

  /* 8. continue reading */
  var saveTimer = 0, lastSave = 0;
  function saveLast() {
    if (!isDoc) return;
    lastSave = Date.now();
    store.set('oow703:last', {
      p: root.getAttribute('data-page') || '', n: docNum, t: docTitle,
      h: activeId || '', ht: activeText || '', pct: Math.round(progress * 100), ts: lastSave
    });
  }
  function saveSoon() {
    if (saveTimer) return;
    var wait = Math.max(0, 2000 - (Date.now() - lastSave));
    saveTimer = setTimeout(function () { saveTimer = 0; saveLast(); }, wait);
  }
  if (isDoc) {
    w.addEventListener('pagehide', saveLast);
    d.addEventListener('visibilitychange', function () { if (d.visibilityState === 'hidden') saveLast(); });
  }
  if (isCover) {
    var card = d.querySelector('.continue');
    var last = store.get('oow703:last', null);
    var ok = last && typeof last.p === 'string' && /^[\w.\-\/]+\.html$/.test(last.p) && last.p.indexOf('..') < 0 && last.p.charAt(0) !== '/';
    if (card && ok) {
      var pct = Math.max(0, Math.min(100, Math.round(Number(last.pct) || 0)));
      card.href = siteRoot + last.p + (last.h ? '#' + encodeURIComponent(String(last.h)) : '');
      card.querySelector('.c-t').textContent = ((last.n || '') + ' ' + (last.t || '')).trim();
      card.querySelector('.c-sec').textContent = last.ht ? String(last.ht) : '';
      card.querySelector('.c-pct').textContent = (last.ht ? '· ' : '') + 'อ่านแล้ว ' + pct + '%';
      card.querySelector('.c-bar i').style.width = pct + '%';
      root.classList.add('has-last');
    } else {
      root.classList.remove('has-last');
    }
  }

  /* Cinematic luxury motion: subtle, progressive and fully optional */
  if (!reducedMotion()) {
    root.classList.add('cinematic');

    var revealTargets = d.querySelectorAll(
      '.titlepage > :is(.tp-monogram,.tp-kicker,.tp-title,.tp-sub,.tp-rule,.tp-desc,.tp-by,.tp-actions,.tp-panel), ' +
      '.toc-part,.opener,.prose > h2,.prose > h3,.prose > blockquote,.prose > .fig,.pager,.site-footer'
    );
    if ('IntersectionObserver' in w) {
      var revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
      for (var r = 0; r < revealTargets.length; r++) {
        revealTargets[r].classList.add('reveal-target');
        revealObserver.observe(revealTargets[r]);
      }
    } else {
      for (var a = 0; a < revealTargets.length; a++) revealTargets[a].classList.add('is-revealed');
    }

    var titlepage = d.querySelector('.titlepage');
    if (titlepage) {
      titlepage.addEventListener('pointermove', function (e) {
        if (e.pointerType === 'touch') return;
        var rect = titlepage.getBoundingClientRect();
        var x = (e.clientX - rect.left) / rect.width - 0.5;
        var y = (e.clientY - rect.top) / rect.height - 0.5;
        titlepage.style.setProperty('--mx', (x * 12).toFixed(2) + 'px');
        titlepage.style.setProperty('--my', (y * 12).toFixed(2) + 'px');
        titlepage.style.setProperty('--spot-x', ((e.clientX - rect.left) / rect.width * 100).toFixed(1) + '%');
        titlepage.style.setProperty('--spot-y', ((e.clientY - rect.top) / rect.height * 100).toFixed(1) + '%');
      });
      titlepage.addEventListener('pointerleave', function () {
        titlepage.style.setProperty('--mx', '0px');
        titlepage.style.setProperty('--my', '0px');
        titlepage.style.setProperty('--spot-x', '72%');
        titlepage.style.setProperty('--spot-y', '18%');
      });
    }
  }

  layoutChanged();
})();
