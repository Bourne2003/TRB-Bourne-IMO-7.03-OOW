#!/usr/bin/env python3
"""รวมทุกบทและภาคผนวกของสมุดเป็นไฟล์ PDF เล่มเดียว

ขั้นตอน: Markdown -> HTML (markdown-it-py) -> PDF (Chromium ผ่าน Playwright)
- รอบแรกพิมพ์ PDF เพื่อหาเลขหน้าของแต่ละบท แล้วรอบที่สองใส่เลขหน้าในสารบัญ
- ภาพประกอบใช้ไฟล์ SVG ใน images/ โดยตรง (คมชัดแบบเวกเตอร์)
- ฟอนต์ไทย Sarabun (SIL Open Font License) อยู่ใน tools/pdf/fonts

ต้องมี: pip install markdown-it-py mdit-py-plugins pypdf  และ Playwright (npm -g)
ใช้:   python3 tools/build_pdf.py            -> pdf/OOW-Training-Notebook-IMO-7.03-TIRAPHONG-NANTAPAN.pdf
"""
import datetime
import html
import os
import re
import subprocess
import sys
import tempfile

from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from pypdf import PdfReader, PdfWriter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDFDIR = os.path.join(ROOT, 'tools', 'pdf')
OUT = os.path.join(ROOT, 'pdf', 'OOW-Training-Notebook-IMO-7.03-TIRAPHONG-NANTAPAN.pdf')
AUTHOR = 'TIRAPHONG NANTAPAN'
TITLE = 'สมุดบันทึกการฝึกนายประจำเรือฝ่ายเดินเรือ (OOW) — IMO Model Course 7.03 / STCW A-II/1'

PARTS = [
    ('บทนำ', None, ['chapters/00-intro']),
    ('Function 1', 'Navigation at the operational level — การเดินเรือ', ['chapters/01-navigation']),
    ('Function 2', 'Cargo handling and stowage at the operational level — การจัดการสินค้า', ['chapters/02-cargo']),
    ('Function 3', 'Controlling the operation of the ship and care for persons on board at the operational level — การควบคุมการปฏิบัติการของเรือและการดูแลบุคคลบนเรือ', ['chapters/03-ship-operation']),
    ('ภาคผนวก', 'Appendices — อภิธานศัพท์ คลังคำถามสอบ เอกสารอ้างอิง และบันทึกการตรวจทาน', ['appendices']),
]


def collect():
    docs = []
    for part, sub, dirs in PARTS:
        files = []
        for d in dirs:
            files += sorted(os.path.join(d, f) for f in os.listdir(os.path.join(ROOT, d)) if f.endswith('.md'))
        docs.append((part, sub, files))
    return docs


def doc_id(rel):
    return 'd-' + re.sub(r'[^A-Za-z0-9]+', '-', os.path.splitext(os.path.basename(rel))[0]).strip('-').lower()


md = MarkdownIt('gfm-like', {'html': True, 'linkify': False, 'typographer': False}).use(tasklists_plugin)


def render_doc(rel, ids, markers=True):
    """แปลงไฟล์ markdown หนึ่งไฟล์เป็น HTML ที่ id ทุกตัวขึ้นต้นด้วย doc id เพื่อไม่ให้ชนกัน"""
    did = ids[rel]
    src = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    tokens = md.parse(src)
    heads = []
    n = 0
    for i, t in enumerate(tokens):
        if t.type == 'heading_open':
            n += 1
            hid = f'h{n}'
            t.attrSet('id', hid)
            level = int(t.tag[1])
            text = tokens[i + 1].content
            heads.append((level, hid, text))
    body = md.renderer.render(tokens, md.options, {})
    base = os.path.dirname(os.path.join(ROOT, rel))

    def fix_href(m):
        q, url = m.group(1), m.group(2)
        if url.startswith(('http://', 'https://', 'mailto:')):
            return f'href={q}{url}{q}'
        if url.startswith('#'):
            return f'href={q}#{did}-{url[1:]}{q}'
        path, _, frag = url.partition('#')
        if path.endswith('.md'):
            target = os.path.relpath(os.path.normpath(os.path.join(base, html.unescape(path))), ROOT)
            if target in ids:
                return f'href={q}#{ids[target]}-{frag}{q}' if frag else f'href={q}#{ids[target]}{q}'
            return f'href={q}#{q}'
        return f'href={q}{url}{q}'

    body = re.sub(r'href=(["\'])(.*?)\1', fix_href, body)
    body = re.sub(r'\bid=(["\'])(.*?)\1', lambda m: f'id={m.group(1)}{did}-{m.group(2)}{m.group(1)}', body)

    def fix_src(m):
        q, url = m.group(1), m.group(2)
        if url.startswith(('http://', 'https://', 'data:', 'file:')):
            return m.group(0)
        return f'src={q}file://{os.path.normpath(os.path.join(base, html.unescape(url)))}{q}'

    body = re.sub(r'src=(["\'])(.*?)\1', fix_src, body)
    # ภาพ + คำบรรยายภาพ (บรรทัดถัดไปที่ขึ้นต้นด้วย "ภาพที่") ให้อยู่หน้าเดียวกัน
    body = re.sub(r'<p>(<img [^>]+>)</p>\s*<p><em>(ภาพที่.*?)</em></p>',
                  r'<figure>\1<figcaption>\2</figcaption></figure>', body, flags=re.S)
    body = re.sub(r'<p>(<img [^>]+>)</p>', r'<figure>\1</figure>', body)
    # เครื่องหมายสำหรับหาเลขหน้า (ใส่เฉพาะรอบแรก เพื่อไม่ให้ไปปรากฏใน bookmark ของ PDF)
    if markers:
        body = re.sub(r'(<h([12]) id="' + did + r'-(h\d+)"[^>]*>)',
                      lambda m: m.group(1) + f'<span class="pgmark">@@{did}-{m.group(3)}@@</span>', body)
    return body, [(lv, f'{did}-{h}', tx) for lv, h, tx in heads]


def esc(s):
    return html.escape(re.sub(r'[*_`]', '', s))


def build_html(docs, pages, markers=True):
    mk = (lambda k: f'<span class="pgmark">@@{k}@@</span>') if markers else (lambda k: '')
    ids = {rel: doc_id(rel) for _, _, files in docs for rel in files}
    css = open(os.path.join(PDFDIR, 'style.css'), encoding='utf-8').read().replace('FONTDIR', 'file://' + os.path.join(PDFDIR, 'fonts'))
    today = datetime.date.today()
    thai_months = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
    date_th = f'{thai_months[today.month - 1]} {today.year + 543} ({today.isoformat()})'
    out = [f'<!doctype html><html lang="th"><head><meta charset="utf-8"><title>{html.escape(TITLE)}</title>',
           f'<meta name="author" content="{AUTHOR}"><style>{css}</style></head><body>']
    out.append(f'''<section class="cover">
<div class="cover-top">IMO Model Course 7.03 · STCW Code Section A-II/1</div>
<h1 class="cover-title">สมุดบันทึกการฝึก<br>นายประจำเรือฝ่ายเดินเรือ</h1>
<div class="cover-sub">Officer in Charge of a Navigational Watch (OOW)<br>ships of 500 gross tonnage or more</div>
<div class="cover-functions">Function 1 Navigation · Function 2 Cargo handling and stowage ·<br>Function 3 Controlling the operation of the ship and care for persons on board</div>
<div class="cover-author">บันทึกและเรียบเรียงโดย<br><b>{AUTHOR}</b></div>
<div class="cover-date">ฉบับรวมเล่ม PDF · {date_th}</div>
<div class="cover-note">บันทึกเพื่อการศึกษา ไม่ใช่สิ่งพิมพ์ทางการ — การทำงานจริงต้องใช้อนุสัญญา ประมวลข้อบังคับ แผนที่และสิ่งพิมพ์ฉบับปัจจุบัน SMS ของบริษัท และข้อกำหนดของรัฐเจ้าของธงเสมอ</div>
</section>''')
    bodies, toc = [], ['<section class="toc"><h1 class="toc-title">สารบัญ</h1>']
    all_heads = {}
    for pi, (part, sub, files) in enumerate(docs):
        pid = f'part-{pi}'
        if sub:
            bodies.append(f'<section class="part" id="{pid}"><h1 class="part-title">{mk(pid)}{esc(part)}</h1><div class="part-sub">{esc(sub)}</div></section>')
            toc.append(f'<div class="toc-part"><a href="#{pid}">{esc(part)} — {esc(sub)}</a><span class="pg">{pages.get(pid, "")}</span></div>')
        for rel in files:
            body, heads = render_doc(rel, ids, markers)
            all_heads[rel] = heads
            did = ids[rel]
            bodies.append(f'<section class="chapter" id="{did}">{mk(did)}{body}</section>')
            title = heads[0][2] if heads else os.path.basename(rel)
            toc.append(f'<div class="toc-ch"><a href="#{did}">{esc(title)}</a><span class="pg">{pages.get(did, "")}</span></div>')
            for lv, hid, tx in heads[1:]:
                if lv == 2 and not tx.startswith('คำถามสอบ'):
                    toc.append(f'<div class="toc-sec"><a href="#{hid}">{esc(tx)}</a><span class="pg">{pages.get(hid, "")}</span></div>')
    toc.append('</section>')
    out += toc + bodies + ['</body></html>']
    return '\n'.join(out)


def render_pdf(html_text, pdf_path):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8', dir=os.path.join(ROOT, 'pdf')) as f:
        f.write(html_text)
        tmp = f.name
    env = dict(os.environ)
    env.setdefault('PWPATH', subprocess.check_output(['npm', 'root', '-g'], text=True).strip() + '/playwright')
    try:
        subprocess.run(['node', os.path.join(PDFDIR, 'render_pdf.js'), tmp, pdf_path], check=True, env=env)
    finally:
        os.unlink(tmp)


def find_pages(pdf_path):
    pages = {}
    for i, p in enumerate(PdfReader(pdf_path).pages, start=1):
        # ตัวอักษรขนาดเล็กมากถูกแยกด้วยช่องว่างตอนดึงข้อความ จึงตัด whitespace ทิ้งก่อนค้นหา
        for m in re.finditer(r'@@([A-Za-z0-9\-]+?)@@', re.sub(r'\s+', '', p.extract_text() or '')):
            pages.setdefault(m.group(1), i)
    return pages


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    docs = collect()
    first = OUT + '.pass1.pdf'
    render_pdf(build_html(docs, {}), first)
    pages = find_pages(first)
    os.unlink(first)
    print('page markers found:', len(pages))
    render_pdf(build_html(docs, pages, markers=False), OUT)
    r = PdfReader(OUT)
    w = PdfWriter(clone_from=r)
    w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
    w.add_metadata({'/Title': TITLE, '/Author': AUTHOR, '/Subject': 'OOW training notebook following IMO Model Course 7.03 and STCW Code A-II/1',
                    '/Keywords': 'STCW, IMO 7.03, OOW, SOLAS, COLREG, MARPOL'})
    with open(OUT, 'wb') as f:
        w.write(f)
    print(f'wrote {OUT}: {len(r.pages)} pages, {os.path.getsize(OUT) / 1e6:.1f} MB')


if __name__ == '__main__':
    sys.exit(main())
