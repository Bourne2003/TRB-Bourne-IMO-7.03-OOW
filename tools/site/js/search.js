/* หน้ากระดาษ — search page. The index is prebuilt by tools/build_site.py:
   assets/search-index.json over http(s), assets/search-index.js (window.OOW_SEARCH) on file:// or as a fallback. */
(function () {
  'use strict';
  var d = document, w = window;
  var input = d.getElementById('q');
  var statusEl = d.querySelector('.search-status');
  var results = d.querySelector('.search-results');
  if (!input || !statusEl || !results) return;
  var form = input.form;
  var version = d.documentElement.getAttribute('data-index-v') || '';
  var data = null, lc = null, loading = null, composing = false, timer = 0, lastQuery = null;
  var MAX = 200;
  var MARKS = /[ัิ-ฺ็-๎]/;

  function norm(s) {
    return String(s).normalize('NFC').replace(/[​-‍﻿­]/g, '')
      .replace(/ํา/g, 'ำ').replace(/\s+/g, ' ');
  }
  function esc(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function setStatus(t) { statusEl.textContent = t; }

  function viaScript() {
    return new Promise(function (resolve, reject) {
      if (w.OOW_SEARCH) { resolve(w.OOW_SEARCH); return; }
      var s = d.createElement('script');
      s.src = 'assets/search-index.js?v=' + encodeURIComponent(version);
      s.onload = function () { if (w.OOW_SEARCH) resolve(w.OOW_SEARCH); else reject(new Error('empty index')); };
      s.onerror = function () { reject(new Error('index script failed')); };
      d.head.appendChild(s);
    });
  }
  function load() {
    if (loading) return loading;
    setStatus('กำลังโหลดดัชนี…');
    var p = /^https?:$/.test(w.location.protocol) && w.fetch
      ? fetch('assets/search-index.json?v=' + encodeURIComponent(version)).then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.json();
        }).catch(viaScript)
      : viaScript();
    loading = p.then(function (j) {
      data = j;
      lc = j.recs.map(function (r) { return (r[2] + '\n' + r[3]).toLowerCase(); });
      return j;
    });
    loading.catch(function () { setStatus('โหลดดัชนีค้นหาไม่สำเร็จ — ลองโหลดหน้านี้ใหม่'); });
    return loading;
  }

  function count(hay, term, from, cap) {
    var n = 0, i = hay.indexOf(term, from);
    while (i >= 0 && n < cap) { n++; i = hay.indexOf(term, i + term.length); }
    return n;
  }

  function highlight(text, terms) {
    var low = text.toLowerCase(), ranges = [];
    terms.forEach(function (t) {
      var i = low.indexOf(t);
      while (i >= 0) { ranges.push([i, i + t.length]); i = low.indexOf(t, i + t.length); }
    });
    ranges.sort(function (a, b) { return a[0] - b[0] || b[1] - a[1]; });
    var out = '', pos = 0;
    ranges.forEach(function (r) {
      if (r[0] < pos) { if (r[1] > pos) { out += '<mark>' + esc(text.slice(pos, r[1])) + '</mark>'; pos = r[1]; } return; }
      out += esc(text.slice(pos, r[0])) + '<mark>' + esc(text.slice(r[0], r[1])) + '</mark>';
      pos = r[1];
    });
    return out + esc(text.slice(pos));
  }

  function snippet(text, terms) {
    var low = text.toLowerCase(), pos = low.indexOf(terms[0]), len = terms[0].length;
    if (pos < 0) {
      for (var k = 1; k < terms.length && pos < 0; k++) { pos = low.indexOf(terms[k]); len = terms[k].length; }
    }
    var start, end;
    if (pos < 0) { start = 0; end = Math.min(text.length, 140); }
    else { start = Math.max(0, pos - 60); end = Math.min(text.length, pos + len + 80); }
    while (start > 0 && MARKS.test(text.charAt(start))) start--;
    while (end < text.length && MARKS.test(text.charAt(end))) end++;
    if (start > 0 && /[\uDC00-\uDFFF]/.test(text.charAt(start))) start--;
    if (end < text.length && /[\uDC00-\uDFFF]/.test(text.charAt(end))) end++;
    return (start > 0 ? '…' : '') + highlight(text.slice(start, end), terms) + (end < text.length ? '…' : '');
  }

  function run(raw) {
    var q = norm(raw).toLowerCase().trim();
    if (q === lastQuery) return;
    lastQuery = q;
    try { w.history.replaceState(null, '', q ? '?q=' + encodeURIComponent(raw.trim()) : w.location.pathname); } catch (e) { /* file:// */ }
    if (q.replace(/ /g, '').length < 2) {
      results.innerHTML = '';
      setStatus(q ? 'พิมพ์อย่างน้อย 2 ตัวอักษร' : '');
      return;
    }
    load().then(function () { render(q, raw.trim()); });
  }

  function reEsc(t) { return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  function render(q, typed) {
    if (q !== lastQuery) return;
    var terms = q.split(' ').filter(Boolean);
    /* Latin/number terms score by whole words, so "gm" ranks GM above GMDSS and "segments", and "rule 19"
       ranks the Rule 19 heading first; Thai has no spaces between words, so Thai terms score as substrings */
    var words = terms.map(function (t) { return /^[a-z0-9.\-]+$/.test(t) ? new RegExp('(^|[^a-z0-9])' + reEsc(t) + '(?![a-z0-9])', 'g') : null; });
    var ascii = /^[a-z0-9 .\-]+$/.test(q);
    var phrase = terms.length > 1 && ascii ? new RegExp('(^|[^a-z0-9])' + reEsc(q) + '(?![a-z0-9])') : null;
    var lead = new RegExp('^[0-9.\\-]*\\s*' + reEsc(q) + (ascii ? '(?![a-z0-9])' : ''));   /* heading starts with the query */
    var hits = [];
    for (var i = 0; i < lc.length; i++) {
      var s = lc[i], r = data.recs[i], hl = r[2].length, ok = true, score = 0;
      for (var t = 0; t < terms.length; t++) {
        var at = s.indexOf(terms[t]);
        if (at < 0) { ok = false; break; }
        var re = words[t];
        if (re) {
          var head = s.slice(0, hl), body = s.slice(hl + 1);
          re.lastIndex = 0;
          score += re.test(head) ? 18 : (at < hl ? 3 : 0);
          var m = body.match(re);
          score += m ? Math.min(m.length, 5) : (body.indexOf(terms[t]) >= 0 ? 1 : 0);
        } else {
          if (at < hl) score += 10;
          score += count(s, terms[t], hl + 1, 5);
        }
      }
      if (!ok) continue;
      if (s.indexOf(q) >= 0) score += 5;
      var h = s.slice(0, hl);
      if (phrase && phrase.test(h)) score += 10;
      if (lead.test(h)) score += 6;
      hits.push([score, i]);
    }
    var total = hits.length;
    hits.sort(function (a, b) { return b[0] - a[0] || a[1] - b[1]; });
    hits = hits.slice(0, MAX);
    if (!total) {
      results.innerHTML = '';
      setStatus('ไม่พบ “' + typed + '” — ลองคำที่สั้นลง หรือคำภาษาอังกฤษ เช่น Rule 19');
      return;
    }
    var groups = {}, order = [];
    hits.forEach(function (h) {
      var doc = data.recs[h[1]][0];
      if (!groups[doc]) { groups[doc] = { doc: doc, best: h[0], items: [] }; order.push(groups[doc]); }
      groups[doc].items.push(h);
    });
    /* chapters: best hit first, with a small bonus for chapters that match in many places */
    order.forEach(function (g) { g.rank = g.best + Math.min(g.items.length, 10) / 2; });
    order.sort(function (a, b) { return b.rank - a.rank || a.doc - b.doc; });
    var firstTyped = typed.split(/\s+/)[0] || '';
    var directive = ('fragmentDirective' in d) && firstTyped
      ? ':~:text=' + encodeURIComponent(firstTyped).replace(/-/g, '%2D') : '';
    var html = '';
    order.forEach(function (g) {
      var doc = data.docs[g.doc];
      /* best match first, then book order */
      g.items.sort(function (a, b) { return b[0] - a[0] || a[1] - b[1]; });
      html += '<section><h2 class="sr-doc"><a href="' + esc(doc[0]) + '"><span class="sr-num">' + esc(doc[1]) + '</span> ' +
        esc(doc[2]) + '</a> <span class="sr-n">' + g.items.length + '</span></h2><ol class="sr-list">';
      g.items.forEach(function (h) {
        var r = data.recs[h[1]], id = r[1];
        var href = doc[0] + (id ? '#' + encodeURIComponent(id) : '') + (directive ? (id ? '' : '#') + directive : '');
        html += '<li><a class="sr-title" href="' + esc(href) + '">' + highlight(r[2], terms) + '</a>' +
          (r[4] === 1 ? ' <span class="sr-tag">คำถาม</span>' : '') +
          (r[3] ? '<p class="sr-snip">' + snippet(r[3], terms) + '</p>' : '') + '</li>';
      });
      html += '</ol></section>';
    });
    results.innerHTML = html;
    setStatus(total > MAX ? 'แสดง ' + MAX + ' ตำแหน่งแรกจาก ' + total + ' (ใน ' + order.length + ' บท)'
      : 'พบ ' + total + ' ตำแหน่งใน ' + order.length + ' บท');
  }

  function schedule() {
    if (composing) return;
    clearTimeout(timer);
    timer = setTimeout(function () { run(input.value); }, 120);
  }
  input.addEventListener('compositionstart', function () { composing = true; });
  input.addEventListener('compositionend', function () { composing = false; schedule(); });
  input.addEventListener('input', function (e) { if (!e.isComposing) schedule(); });
  if (form) form.addEventListener('submit', function (e) { e.preventDefault(); clearTimeout(timer); run(input.value); });

  var initial = '';
  try { initial = new URLSearchParams(w.location.search).get('q') || ''; } catch (e) { initial = ''; }
  if (initial) { input.value = initial; run(initial); }
  if (w.matchMedia && w.matchMedia('(pointer: fine)').matches) input.focus();
})();
