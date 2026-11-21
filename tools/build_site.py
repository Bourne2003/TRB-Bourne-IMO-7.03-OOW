#!/usr/bin/env python3
"""สร้างเว็บไซต์ "หนังสือออนไลน์" ของสมุดบันทึกการฝึก OOW สำหรับ GitHub Pages

แปลง Markdown ทุกบทและภาคผนวกเป็นหน้า HTML แบบอ่านง่ายเหมือนหนังสือ (code name: หน้ากระดาษ)
- โครงสร้างไฟล์ใน _site/ เหมือนต้นฉบับ (chapters/…, appendices/…, images/…) ลิงก์ทุกตัวเป็น relative
  จึงใช้ได้ทั้งใต้ https://<user>.github.io/<repo>/ และเปิดจากดิสก์ (file://)
- ไม่แก้ไฟล์ต้นฉบับ ไม่พึ่ง CDN ฟอนต์ Trirong/Sarabun (SIL OFL) อยู่ในเว็บเอง
- ผลลัพธ์ deterministic: build สองครั้งได้ไฟล์เหมือนกันทุกไบต์

ต้องมี: pip install markdown-it-py==4.2.0 mdit-py-plugins==0.6.1
ใช้:   python3 tools/build_site.py [--out _site] [--no-git]
ดูผล:  python3 -m http.server -d _site   แล้วเปิด http://localhost:8000/
"""
import argparse
import hashlib
import html
import json
import math
import os
import posixpath
import re
import shutil
import string
import subprocess
import sys
import unicodedata
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_SRC = os.path.join(ROOT, 'tools', 'site')
PDF_FONTS = os.path.join(ROOT, 'tools', 'pdf', 'fonts')
AUTHOR = 'TIRAPHONG NANTAPAN'
BOOK = 'สมุดบันทึกการฝึก OOW'
COVER_TITLE = 'สมุดบันทึกการฝึกนายประจำเรือฝ่ายเดินเรือ (OOW) — TIRAPHONG NANTAPAN'
# ที่อยู่จริงของเว็บ — ใช้เฉพาะในหน้า 404 (GitHub Pages เสิร์ฟหน้านั้นที่ path ใดก็ได้ จึงใช้ลิงก์ relative ไม่ได้)
SITE_URL = 'https://bourne2003.github.io/Marnie-OOW-IMO_7.03-TRB/'

SITE_PARTS = [
    ('intro', 'บทนำ', None, 'chapters/00-intro'),
    ('f1', 'Function 1 — การเดินเรือ', 'Navigation at the operational level', 'chapters/01-navigation'),
    ('f2', 'Function 2 — การจัดการสินค้า', 'Cargo handling and stowage at the operational level', 'chapters/02-cargo'),
    ('f3', 'Function 3 — การควบคุมการปฏิบัติการของเรือและการดูแลบุคคลบนเรือ',
           'Controlling the operation of the ship and care for persons on board at the operational level', 'chapters/03-ship-operation'),
    ('app', 'ภาคผนวก', 'อภิธานศัพท์ คลังคำถามสอบ เอกสารอ้างอิง และบันทึกการตรวจทาน', 'appendices'),
]
SOURCE_DIRS = ['chapters', 'appendices', 'images', 'tools', '.git', '.github']
THAI = re.compile('[ก-๛]')
MONTHS = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
# id ที่ chrome ของหน้าใช้อยู่แล้ว — slug ของหัวข้อต้องไม่ชนกับพวกนี้ (ปกเพิ่ม preface/toc หน้า search เพิ่ม q)
CHROME_IDS = {'top', 'main', 'toc-drawer', 'toc-drawer-h', 'prefs', 'prefs-h'}
COVER_IDS = {'preface', 'toc'}
# ฟอนต์ที่ preload: ทุกหน้าใช้ Trirong ไทย 400 — หน้าบทเพิ่มชุดที่อยู่ในจอแรก (หัวบท ข้อความหัวบท เนื้อหา)
# เพื่อไม่ให้ตัวอักษรสลับฟอนต์หลังแสดงผลแล้วทำให้เนื้อหาเลื่อน (CLS) — เป็นไฟล์ที่หน้าบทโหลดอยู่แล้ว ไม่เพิ่มขนาดรวม
# รายชื่ออยู่ใน <html data-fonts> แล้ว head.js สร้าง <link rel=preload> เฉพาะเมื่อเปิดผ่าน http(s)
# (file:// ไม่ผ่าน CORS ของ preload) และข้าม Trirong เมื่อผู้อ่านเลือกแบบตัวอักษร "แบบเรียบ"
PRELOAD_BASE = ['trirong-thai-400-normal']
PRELOAD_DOC = PRELOAD_BASE + ['trirong-latin-400-normal', 'trirong-thai-600-normal', 'trirong-latin-600-normal',
                              'sarabun-thai-400-normal', 'sarabun-latin-400-normal']
PRELOAD_ITALIC = 'sarabun-latin-400-italic'   # อักษรเอียงในข้อความหัวบท (colophon)
PRELOAD_SHORT = PRELOAD_BASE + ['trirong-thai-600-normal', 'sarabun-thai-400-normal', 'sarabun-latin-400-normal']  # ปกและหน้าค้นหา

md = MarkdownIt('gfm-like', {'html': True, 'linkify': False, 'typographer': False}).use(tasklists_plugin)


# --------------------------------------------------------------------------- log

class Log:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.summary = ''

    def error(self, msg, where=None):
        self.errors.append(f'{where}: {msg}' if where else msg)

    def warn(self, msg, where=None):
        self.warnings.append(f'{where}: {msg}' if where else msg)


LOG = Log()


# --------------------------------------------------------------------------- helpers

def esc(s):
    return html.escape(s, quote=True)


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def sha8(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha1(data).hexdigest()[:8]


def norm_ws(s):
    return re.sub(r'\s+', ' ', s).strip()


def norm_search(s):
    s = unicodedata.normalize('NFC', s)
    s = re.sub('[\u200b-\u200d\ufeff\u00ad]', '', s)
    s = s.replace('\u0e4d\u0e32', '\u0e33')
    return norm_ws(s)


def inline_text(tok):
    """ข้อความล้วนของ inline token (ไม่รวม HTML ดิบ)"""
    out = []
    for c in tok.children or []:
        if c.type in ('text', 'code_inline'):
            out.append(c.content)
        elif c.type in ('softbreak', 'hardbreak'):
            out.append(' ')
        elif c.type == 'image':
            out.append(c.content)
    return ''.join(out)


def slugify(text):
    """GitHub slug: ตัวเล็ก เก็บเฉพาะตัวอักษร/เครื่องหมายกำกับ (สระ วรรณยุกต์ไทย)/ตัวเลข _ - และช่องว่าง"""
    s = ''.join(c for c in text.lower() if unicodedata.category(c)[0] in 'LMN' or c in '_- ')
    s = s.replace(' ', '-')
    return s or 'section'


def unique(base, used, first=1):
    if base not in used:
        used.add(base)
        return base
    i = first
    while f'{base}-{i}' in used:
        i += 1
    used.add(f'{base}-{i}')
    return f'{base}-{i}'


BLOCK_TAGS = r'p|li|ul|ol|td|th|tr|thead|tbody|table|h[1-6]|figcaption|figure|blockquote|div|pre|dt|dd|dl|hr|br|header|section|nav'
BLOCK_TAG_RE = re.compile(r'</?(?:' + BLOCK_TAGS + r')\b[^>]*>', re.I)
TAG_RE = re.compile(r'<[^>]+>')
TAG_SPLIT_RE = re.compile(r'(<[^>]+>)')
H_ANCHOR_RE = re.compile(r'<a class="h-anchor"[^>]*>#</a>')


def html_to_text(h):
    h = H_ANCHOR_RE.sub('', h)
    h = BLOCK_TAG_RE.sub(' ', h)
    h = TAG_RE.sub('', h)
    return norm_ws(html.unescape(h))


def thai_date(iso, with_day=True):
    if not iso:
        return ''
    y, m, d = (int(x) for x in iso.split('-'))
    return f'{d} {MONTHS[m - 1]} {y}' if with_day else f'{MONTHS[m - 1]} {y}'


def reading_minutes(text):
    thai = sum(1 for c in text if '\u0e01' <= c <= '\u0e30' or '\u0e32' <= c <= '\u0e33'
               or '\u0e3f' <= c <= '\u0e46' or '\u0e4f' <= c <= '\u0e5b')
    latin = len(re.findall(r'[A-Za-z0-9]+', text))
    minutes = max(1, math.ceil(thai / 700 + latin / 180))
    if minutes > 10:
        minutes = int(math.ceil(minutes / 5) * 5)
    return minutes


GIT_OK = None


def git(*args):
    global GIT_OK
    if GIT_OK is False:
        return ''
    try:
        r = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        GIT_OK = False
        return ''
    if r.returncode != 0:
        return ''
    GIT_OK = True
    return r.stdout.strip()


# --------------------------------------------------------------------------- documents

class Doc:
    def __init__(self, idx, part, rel):
        self.idx = idx
        self.part = part              # tuple from SITE_PARTS
        self.rel = rel                # e.g. chapters/01-navigation/1.2.1-A-colregs.md
        self.out = rel[:-3] + '.html'
        self.page = self.out
        self.depth = rel.count('/')
        self.root = '../' * self.depth
        self.src_dir = os.path.dirname(os.path.join(ROOT, rel))
        self.stem = os.path.splitext(os.path.basename(rel))[0]
        self.is_appendix = rel.startswith('appendices/')
        self.date = None
        self.prev = self.next = None  # Doc or None (= cover)


def collect_docs():
    docs = []
    for part in SITE_PARTS:
        d = os.path.join(ROOT, part[3])
        for f in sorted(os.listdir(d)):
            if f.endswith('.md'):
                docs.append(Doc(len(docs), part, f'{part[3]}/{f}'))
    for i, doc in enumerate(docs):
        doc.prev = docs[i - 1] if i > 0 else None
        doc.next = docs[i + 1] if i + 1 < len(docs) else None
    return docs


def split_title(text, doc):
    parts = text.split(' — ')
    lead = parts[0]
    m = re.match(r'^(\d+(?:\.\d+)*)\s+(.*)$', lead)
    if m:
        num, lead_rest = m[1], m[2]
    elif re.match(r'^ภาคผนวก [ก-ฮ]$', lead) or lead == 'บทนำ':
        num, lead_rest = lead, ''
    else:
        num, lead_rest = '', lead
    if len(parts) > 1 and THAI.search(parts[-1]):
        th = parts[-1]
        en = ' — '.join([lead_rest] + parts[1:-1]).strip(' —')
    else:
        th = None
        en = ' — '.join([lead_rest] + parts[1:]).strip(' —')
    doc.h1_text = text
    doc.num = num
    doc.th = th
    doc.en = en
    doc.title = th or en
    if doc.is_appendix:
        doc.num_display = num or 'ภาคผนวก'
        doc.num_toc = num.replace('ภาคผนวก ', '') if num.startswith('ภาคผนวก ') else num
    elif doc.part[0] == 'intro':
        doc.num_display = 'บทนำ'
        doc.num_toc = ''
    else:
        letter = re.match(r'^[\d.]+-([A-E])-', doc.stem)
        doc.num_display = num + ('-' + letter[1] if letter else '')
        doc.num_toc = doc.num_display


# --------------------------------------------------------------------------- markdown -> blocks

class Block:
    def __init__(self, kind, html_='', line=None, toks=None):
        self.kind = kind          # h p table bq list hr pre raw anchor fig qa qasrc tools other
        self.html = html_
        self.line = line
        self.toks = toks or []
        self.level = 0
        self.id = ''
        self.text = ''
        self.inner = ''
        self.qa_head = False
        self.qa = None            # (label_q, q_text, label_a, a_text) for qa blocks


def split_blocks(tokens):
    blocks, i = [], 0
    while i < len(tokens):
        if tokens[i].nesting == 1:
            depth, j = 0, i
            while True:
                depth += tokens[j].nesting
                if depth == 0:
                    break
                j += 1
            blocks.append(tokens[i:j + 1])
            i = j + 1
        else:
            blocks.append(tokens[i:i + 1])
            i += 1
    return blocks


RAW_A_RE = re.compile(r'^\s*<a id="([^"]+)"></a>\s*$')
ALLOWED_RAW = re.compile(r'^</?(sub|sup|br)\b[^>]*>$|^<a id="[^"]+">$|^</a>$', re.I)
TASK_SPACE_RE = re.compile(r'(<input class="task-list-item-checkbox"[^>]*>)[ \t]+')
TASK_BOX = re.compile(r'^<input class="task-list-item-checkbox"[^>]*>$')   # generated by the tasklists plugin
KIND = {'paragraph_open': 'p', 'table_open': 'table', 'blockquote_open': 'bq', 'bullet_list_open': 'list',
        'ordered_list_open': 'list', 'hr': 'hr', 'fence': 'pre', 'code_block': 'pre', 'html_block': 'raw'}


class Ctx:
    """บริบทของหน้าที่กำลังแปลง (บทหรือปก)"""
    def __init__(self, where, src_dir, out, root, doc=None):
        self.where = where
        self.src_dir = src_dir
        self.out = out
        self.out_dir = posixpath.dirname(out)
        self.root = root
        self.doc = doc
        self.used = set(CHROME_IDS)
        self.figures = 0
        self.captions = 0
        self.tables = 0
        self.qa = 0


def check_raw_html(tokens, ctx):
    for t in tokens:
        items = [t] if t.type == 'html_block' else [c for c in (t.children or []) if c.type == 'html_inline']
        for c in items:
            for tag in re.findall(r'<[^>]+>', c.content):
                if not ALLOWED_RAW.match(tag.strip()) and not TASK_BOX.match(tag.strip()):
                    line = t.map[0] + 1 if t.map else None
                    LOG.warn(f'raw HTML tag {tag!r}', f'{ctx.where}:{line}' if line else ctx.where)


def to_blocks(tokens, ctx):
    """แปลง token เป็นรายการ block ระดับบนสุด พร้อม id ของหัวข้อ (raw anchor ย้ายไปอยู่ที่หัวข้อ)"""
    check_raw_html(tokens, ctx)
    raw = split_blocks(tokens)
    # raw ids ทั้งหมดก่อน เพื่อให้ slug ที่สร้างไม่ชนกับ id ที่ผู้เขียนกำหนด
    for bt in raw:
        if bt[0].type == 'paragraph_open':
            m = RAW_A_RE.match(bt[1].content)
            if m:
                rid = m[1]
                if rid in ctx.used:
                    LOG.error(f'duplicate id "{rid}"', f'{ctx.where}:{bt[0].map[0] + 1}')
                ctx.used.add(rid)
    blocks, pending = [], None
    env = {}
    for k, bt in enumerate(raw):
        t0 = bt[0]
        line = t0.map[0] + 1 if t0.map else None
        if t0.type == 'paragraph_open':
            m = RAW_A_RE.match(bt[1].content)
            if m:
                if k + 1 < len(raw) and raw[k + 1][0].type == 'heading_open':
                    pending = m[1]
                else:
                    blocks.append(Block('anchor', f'<a id="{esc(m[1])}" class="anchor-pt"></a>\n', line))
                continue
        if t0.type == 'heading_open':
            b = Block('h', '', line, bt)
            b.level = int(t0.tag[1])
            b.text = inline_text(bt[1])
            b.inner = md.renderer.renderInline(bt[1].children, md.options, env)
            b.id = pending if pending else unique(slugify(b.text), ctx.used)
            pending = None
            blocks.append(b)
            continue
        blocks.append(Block(KIND.get(t0.type, 'other'), md.renderer.render(bt, md.options, env), line, bt))
    return blocks


# --- figures ------------------------------------------------------------------

IMG_RE = re.compile(r'<img\s+([^>]*?)\s*/?>')
ATTR_RE = re.compile(r'([\w:-]+)="([^"]*)"')
VIEWBOX_RE = re.compile(r'viewBox\s*=\s*["\']\s*([-\d.eE]+)[\s,]+([-\d.eE]+)[\s,]+([\d.eE]+)[\s,]+([\d.eE]+)\s*["\']')
SVG_SIZE = {}


def svg_size(path, where):
    if path in SVG_SIZE:
        return SVG_SIZE[path]
    size = None
    if not os.path.isfile(path):
        LOG.error(f'image not found: {os.path.relpath(path, ROOT)}', where)
    elif path.lower().endswith('.svg'):
        with open(path, 'rb') as f:
            head = f.read(2048).decode('utf-8', 'replace')
        m = VIEWBOX_RE.search(head)
        if not m:
            LOG.error(f'SVG has no viewBox: {os.path.relpath(path, ROOT)}', where)
        else:
            size = (round(float(m[3])), round(float(m[4])))
    SVG_SIZE[path] = size
    return size


def fix_img(attr_html, ctx, where):
    attrs = ATTR_RE.findall(attr_html)
    a = dict(attrs)
    src = a.get('src', '')
    size = None
    if src and not re.match(r'^[a-z][a-z0-9+.-]*:|^/', src, re.I):
        size = svg_size(os.path.normpath(os.path.join(ctx.src_dir, unquote(html.unescape(src)))), where)
    out = [f'src="{src}"', f'alt="{a.get("alt", "")}"']
    if a.get('title'):
        out.append(f'title="{a["title"]}"')
    if size:
        out.append(f'width="{size[0]}" height="{size[1]}"')
    out.append('loading="lazy" decoding="async"')
    return '<img ' + ' '.join(out) + '>', src


IMG_ONLY_RE = re.compile(r'<p>(<img [^>]+>)</p>\s*')
# บางบทเขียนคำบรรยายภาพบรรทัดถัดจากภาพทันที (ย่อหน้าเดียวกัน)
IMG_CAP_RE = re.compile(r'<p>(<img [^>]+>)\s*(?:<br\s*/?>)?\s*<em>(ภาพที่(?:(?!</p>).)*?)</em></p>\s*', re.S)
CAPTION_RE = re.compile(r'<p><em>(ภาพที่(?:(?!</p>).)*?)</em></p>\s*', re.S)
LABEL_RE = re.compile(r'^(ภาพที่\s+(\S+?))[.:,]?\s+')


def make_figure(img_html, cap_html, ctx, where):
    m = IMG_RE.match(img_html)
    img, src = fix_img(m[1], ctx, where)
    ctx.figures += 1
    fid, cap = None, ''
    if cap_html is not None:
        ctx.captions += 1
        lm = LABEL_RE.match(cap_html)
        if lm:
            label, num, rest = lm[1], lm[2], cap_html[lm.end():]
        else:
            label, num, rest = cap_html, cap_html.replace('ภาพที่', '').strip(), ''
        fid = unique('fig-' + re.sub(r'\s+', '-', html.unescape(TAG_RE.sub('', num))).lower(), ctx.used)
        cap = f'<figcaption><span class="fig-label">{label}</span>{" " + rest if rest else ""}</figcaption>\n'
    id_attr = f' id="{esc(fid)}"' if fid else ''
    return (f'<figure class="fig"{id_attr}>\n<a class="fig-link" href="{src}">{img}</a>\n{cap}</figure>\n')


# --- Q&A ------------------------------------------------------------------------

QA_RE = re.compile(r'<p>(?P<pre>(?:(?!</p>).)*?)<strong>(?P<ql>ถาม(?: \(ไทย\))?|Q):</strong>\s*(?P<q>(?:(?!</p>).)*?)\n'
                   r'<strong>(?P<al>แนวตอบ|A(?: \(แนว\))?):</strong>\s*(?P<a>(?:(?!</p>).)*?)</p>', re.S)
SRC_Q_RE = re.compile(r'^\*\*(ถาม(?: \(ไทย\))?|Q):\*\*', re.M)
SRC_A_RE = re.compile(r'^\*\*(แนวตอบ|A(?: \(แนว\))?):\*\*', re.M)


def make_qa(m, ctx):
    pre = m['pre']
    if pre and not pre.endswith('\n'):
        return None
    out = []
    if pre:
        out.append(Block('qasrc', f'<p class="qa-src">{pre[:-1]}</p>\n'))
    qtext = html_to_text(m['q'])
    atext = html_to_text(m['a'])
    h8 = hashlib.sha1(unicodedata.normalize('NFC', qtext).encode('utf-8')).hexdigest()[:8]
    qid = unique('qa-' + h8, ctx.used, first=2)
    aid = unique(qid + '-a', ctx.used)
    lang = ' lang="en"' if m['ql'] == 'Q' else ''
    # the colon stays inside the label (text content = source "ถาม: …"); a separate hidden span would add ~40 KB to appendix B
    b = Block('qa', (f'<div class="qa" id="{qid}"{lang}>'
                     f'<p class="qa-q"><span class="qa-label">{m["ql"]}:</span> {m["q"]}</p>'
                     f'<div class="qa-a" id="{aid}"><p><span class="qa-label">{m["al"]}:</span> {m["a"]}</p></div>'
                     f'</div>\n'))
    b.id = qid
    b.qa = (m['ql'], qtext, m['al'], atext)
    ctx.qa += 1
    out.append(b)
    return out


TABLE_RE = re.compile(r'<table>.*?</table>\n?', re.S)
SLASH_RE = re.compile(r'(?<=[^\s/<])/(?=[^\s/>])')


def slash_breaks(h):
    """ในตาราง ให้ตัดบรรทัดหลัง "/" ได้ (เช่น MSC.1/Circ.1331/Rev.1) — คอลัมน์แคบบนมือถือจะได้ไม่ต้องเลื่อนข้าง
    แก้เฉพาะข้อความ ไม่แตะ tag/attribute; <wbr> ไม่มีตัวอักษร ข้อความที่คัดลอกจึงเหมือนต้นฉบับ"""
    return ''.join(part if part.startswith('<') else SLASH_RE.sub('/<wbr>', part) for part in TAG_SPLIT_RE.split(h))


def wrap_tables(h, ctx, heading):
    """ห่อทุกตาราง (รวมตารางใน blockquote) ด้วย region ที่เลื่อนแนวนอนได้และมีชื่อ"""
    def repl(m):
        t = m[0]
        ctx.tables += 1
        thead = re.search(r'<thead>(.*?)</thead>', t, re.S)
        first_row = re.search(r'<tr>(.*?)</tr>', thead[1] if thead else t, re.S)
        cols = len(re.findall(r'<th\b', first_row[1])) if first_row else 0
        cls = 'table-wrap' + (' t-wide' if cols >= 4 else '') + (' t-xwide' if cols >= 7 else '')
        label = esc('ตาราง: ' + heading)
        return f'<div class="{cls}" role="region" tabindex="0" aria-label="{label}">\n{slash_breaks(t)}</div>\n'
    return TABLE_RE.sub(repl, h)


PRE_WIDE_CHARS = 64          # บรรทัดยาวกว่านี้ล้นคอลัมน์ข้อความ (≈ 34em ที่ตัวอักษร mono .82em) → ใช้คอลัมน์กว้าง
PRE_COLS_RE = re.compile(r'\S {2,}\S')   # ช่องว่าง ≥ 2 กลางบรรทัด = จัดคอลัมน์ด้วยช่องว่าง → ห้ามตัดบรรทัดบนมือถือ


def pre_attrs(tok):
    """class ของบล็อก pre: pre-wide (บรรทัดยาว) และ pre-cols (จัดคอลัมน์ด้วยช่องว่าง ตัดบรรทัดแล้วอ่านผิด)"""
    lines = tok.content.rstrip('\n').split('\n')
    width = max((sum(1 for c in ln if unicodedata.category(c) != 'Mn') for ln in lines), default=0)
    cls = []
    if width > PRE_WIDE_CHARS:
        cls.append('pre-wide')
    if any(PRE_COLS_RE.search(ln) for ln in lines):
        cls.append('pre-cols')
    return (f' class="{" ".join(cls)}"' if cls else '') + ' tabindex="0"'


# URL เปล่าในข้อความ (ภาคผนวก ง) — GitHub แสดงเป็นลิงก์ (GFM autolink) จึงทำแบบเดียวกัน โดยไม่พึ่ง linkify-it-py
BARE_URL_RE = re.compile(r"https?://[A-Za-z0-9\-._~:/?#\[\]@!$&'()*+,;=%]+")


def _url_link(m):
    url = m[0]
    while url and url[-1] in '.,;:!?*_~\'':
        url = url[:-1]
    while url.endswith(')') and url.count(')') > url.count('('):
        url = url[:-1]
    if len(url) <= len('https://'):
        return m[0]
    return f'<a href="{url}">{url}</a>{m[0][len(url):]}'


def autolink(h):
    if 'http' not in h:
        return h
    out, skip = [], 0
    for part in TAG_SPLIT_RE.split(h):
        if part.startswith('<'):
            t = re.match(r'<(/?)(a|code|pre)\b', part, re.I)
            if t:
                skip += -1 if t[1] else 1
            out.append(part)
        elif skip or 'http' not in part:
            out.append(part)
        else:
            out.append(BARE_URL_RE.sub(_url_link, part))
    return ''.join(out)


KEY_BQ = ('จดไว้กันลืม', 'ข้อควรระวัง', 'คำเตือน', 'ระวัง', 'จุดที่ชอบถาม')
FOOTER_RE = re.compile(r'^\*(ก่อนหน้า ←|หน้าถัดไป →|ถัดไป →)')


def transform(blocks, ctx, top_level=1):
    """แปลง block: ภาพ+คำบรรยาย, ถาม/แนวตอบ, ตาราง, blockquote, แถบข้ามตัวอักษร, แถบเครื่องมือคำถาม

    top_level = ระดับหัวข้อที่อยู่เหนือ block ชุดนี้ในหน้า (1 = h1 ของบท) ใช้ไม่ให้ระดับหัวข้อกระโดด"""
    out = []
    last_heading = ctx.doc.title if ctx.doc else ''
    i = 0
    while i < len(blocks):
        b = blocks[i]
        where = f'{ctx.where}:{b.line}' if b.line else ctx.where
        if b.kind == 'h':
            last_heading = b.text
        elif b.kind == 'p':
            same = IMG_CAP_RE.fullmatch(b.html)
            if same:
                out.append(Block('fig', make_figure(same[1], same[2], ctx, where), b.line))
                i += 1
                continue
            if IMG_ONLY_RE.fullmatch(b.html):
                img = IMG_ONLY_RE.fullmatch(b.html)[1]
                cap = None
                if i + 1 < len(blocks) and blocks[i + 1].kind == 'p':
                    cm = CAPTION_RE.fullmatch(blocks[i + 1].html)
                    if cm:
                        cap = cm[1]
                        i += 1
                nb = Block('fig', make_figure(img, cap, ctx, where), b.line)
                out.append(nb)
                i += 1
                continue
            m = QA_RE.fullmatch(b.html.strip())
            if m:
                res = make_qa(m, ctx)
                if res:
                    for r in res:
                        r.line = b.line
                    out.extend(res)
                    i += 1
                    continue
            if b.html.startswith('<p><strong>ข้ามไปที่:</strong>'):
                b.html = '<p class="jumpbar">' + b.html[3:]
            b.html = IMG_RE.sub(lambda mm: fix_img(mm[1], ctx, where)[0], b.html)
        elif b.kind == 'pre' and b.toks:
            b.html = b.html.replace('<pre>', f'<pre{pre_attrs(b.toks[0])}>', 1)
        elif b.kind == 'bq':
            sm = re.search(r'<strong>(.*?)</strong>', b.html, re.S)
            if sm and html_to_text(sm[1]).startswith(KEY_BQ):
                b.html = b.html.replace('<blockquote>', '<blockquote class="bq-key">', 1)
        if b.kind in ('p', 'table', 'bq', 'list'):
            b.html = autolink(b.html)
        if b.kind in ('table', 'bq', 'list', 'other', 'raw'):
            b.html = wrap_tables(b.html, ctx, last_heading)
            b.html = IMG_RE.sub(lambda mm: fix_img(mm[1], ctx, where)[0], b.html)
        out.append(b)
        i += 1
    # แถบเครื่องมือของชุดคำถาม: ทุกหัวข้อ h2/h3 ที่มีคำถามก่อนถึงหัวข้อ h2/h3 ถัดไป — วางหลังหัวข้อ
    # หรือถ้ามีย่อหน้านำก่อนคำถามข้อแรก วางก่อนคำถามข้อแรก (และก่อนบรรทัด "จากบท …" ของข้อนั้น)
    tools_at = {}
    for i, b in enumerate(out):
        if b.kind == 'h' and b.level in (2, 3):
            n, first = 0, None
            for j in range(i + 1, len(out)):
                c = out[j]
                if c.kind == 'h' and c.level in (2, 3):
                    break
                if c.kind == 'qa':
                    n += 1
                    if first is None:
                        first = j
            if n:
                while first - 1 > i and out[first - 1].kind == 'qasrc':
                    first -= 1
                b.qa_head = True
                tools_at[first] = Block('tools', (
                    f'<div class="qa-tools"><span class="qa-count">{n} ข้อ</span>\n'
                    '<button type="button" class="qa-switch" role="switch" aria-checked="false">'
                    '<span class="qa-track" aria-hidden="true"></span>ซ่อนแนวตอบ (ทดสอบตัวเอง)</button></div>\n'), b.line)
    final = []
    for i, b in enumerate(out):
        if i in tools_at:
            final.append(tools_at[i])
        final.append(b)
    prev = top_level
    for b in final:
        if b.kind == 'h':
            inner = b.inner
            if b.level == 2:
                inner = re.sub(r'^(\d+(?:\.\d+)*\.)(?=\s)', r'<span class="sec-num">\1</span>', inner)
            # ไม่ให้ระดับหัวข้อกระโดด (เช่น #### ใต้ ## ในภาคผนวก ง) — แสดงขนาดเดิมด้วย class hl<เดิม>
            tag = min(b.level, prev + 1) if b.level > 1 else 1
            prev = tag
            classes = (['qa-head'] if b.qa_head else []) + ([f'hl{b.level}'] if tag != b.level else [])
            cls = f' class="{" ".join(classes)}"' if classes else ''
            anchor = (f'<a class="h-anchor" href="#{esc(b.id)}" aria-hidden="true" tabindex="-1">#</a>'
                      if 2 <= b.level <= 4 else '')
            b.html = f'<h{tag} id="{esc(b.id)}"{cls}>{inner}{anchor}</h{tag}>\n'
    return final


# --- links ----------------------------------------------------------------------

HREF_A_RE = re.compile(r'<a href="([^"]*)"((?:\s[^>]*)?)>(.*?)</a>', re.S)
URL_ATTR_RE = re.compile(r'\b(href|src)="([^"]*)"')


class Site:
    docs = []
    by_rel = {}
    ids = {}            # page out path -> set of ids


def resolve(attr, raw, ctx, where):
    """คืน (action, url): keep | rewrite | unwrap | error"""
    url = html.unescape(raw)
    if url.startswith('/'):
        LOG.error(f'root-absolute URL not allowed: {url}', where)
        return 'error', raw
    if re.match(r'^(https?:|mailto:)', url, re.I):
        if attr == 'src':
            LOG.error(f'external src not allowed: {url}', where)
            return 'error', raw
        return 'keep', raw
    if re.match(r'^[a-z][a-z0-9+.-]*:', url, re.I):
        if attr == 'src' and url.lower().startswith('data:'):
            return 'keep', raw
        LOG.error(f'unsupported URL scheme: {url}', where)
        return 'error', raw
    if url.startswith('#'):
        frag = unquote(url[1:])
        if frag and frag not in Site.ids.get(ctx.out, set()):
            LOG.error(f'broken fragment #{frag}', where)
            return 'error', raw
        return 'keep', raw
    path, _, frag = url.partition('#')
    target = os.path.normpath(os.path.join(ctx.src_dir, unquote(path)))
    rel = os.path.relpath(target, ROOT).replace(os.sep, '/')
    if path.endswith('.md') and (rel == 'README.md' or rel in Site.by_rel or not os.path.isfile(target)):
        if rel == 'README.md':
            out = 'index.html'
        elif rel in Site.by_rel:
            out = Site.by_rel[rel].out
        else:
            LOG.error(f'link to unknown markdown file: {path}', where)
            return 'error', raw
        new = posixpath.relpath(out, ctx.out_dir or '.')
        if frag:
            if unquote(frag) not in Site.ids.get(out, set()):
                LOG.error(f'broken link fragment: {path}#{unquote(frag)}', where)
                return 'error', raw
            new += '#' + frag
        return 'rewrite', esc(new)
    if not rel.startswith('..') and os.path.isfile(target):
        if rel.startswith('images/'):
            return 'keep', raw
        LOG.warn(f'link to non-page file {rel} unwrapped to text', where)
        return 'unwrap', raw
    LOG.error(f'broken link: {path}', where)
    return 'error', raw


def keeps_filenames(ctx):
    """ภาคผนวก ง (บันทึกการตรวจทาน) อ้างถึง "ไฟล์: x.md" โดยตั้งใจ — คงชื่อไฟล์ไว้"""
    return bool(ctx.doc and ctx.doc.is_appendix and ctx.doc.stem.startswith('D-'))


def link_label(raw, text, ctx):
    """ข้อความลิงก์ที่เป็นแค่ชื่อไฟล์ .md ของบท → เลขบทและชื่อบท (href แปลงเป็น .html แยกต่างหาก)"""
    path = unquote(html.unescape(raw)).partition('#')[0]
    if not path.endswith('.md') or html.unescape(text).strip() != posixpath.basename(path) or keeps_filenames(ctx):
        return text
    rel = os.path.relpath(os.path.normpath(os.path.join(ctx.src_dir, path)), ROOT).replace(os.sep, '/')
    d = Site.by_rel.get(rel)
    return esc(f'{d.num_display} {d.title}') if d else text


def rewrite_links(h, ctx, where):
    def a_repl(m):
        action, new = resolve('href', m[1], ctx, where)
        if action == 'unwrap':
            return m[3]
        text = link_label(m[1], m[3], ctx) if action == 'rewrite' else m[3]
        return f'<a href="{new}"{m[2]}>{text}</a>'

    h = HREF_A_RE.sub(a_repl, h)

    def src_repl(m):
        if m[1] != 'src':
            return m[0]
        action, new = resolve('src', m[2], ctx, where)
        return f'src="{new}"'

    h = URL_ATTR_RE.sub(src_repl, h)
    # ช่องว่างหลัง checkbox ของ task list ทำให้บรรทัดแรกเยื้องไม่ตรงกับบรรทัดที่ตัดขึ้นใหม่
    return TASK_SPACE_RE.sub(r'\1', h)


# --------------------------------------------------------------------------- per-doc pass 1

def process_doc(doc):
    src = read(os.path.join(ROOT, doc.rel))
    ctx = Ctx(doc.rel, doc.src_dir, doc.out, doc.root, doc)
    tokens = md.parse(src)
    blocks = to_blocks(tokens, ctx)
    h1s = [b for b in blocks if b.kind == 'h' and b.level == 1]
    if len(h1s) != 1:
        LOG.error(f'expected exactly one "# " heading, found {len(h1s)}', doc.rel)
    if not blocks or blocks[0].kind != 'h' or blocks[0].level != 1:
        LOG.error('document must start with the "# " heading', doc.rel)
        split_title(os.path.basename(doc.rel), doc)
        doc.h1_id = 'title'
        colophon = ''
    else:
        h1 = blocks.pop(0)
        split_title(h1.text, doc)
        doc.h1_id = h1.id
        colophon = ''
        if blocks and blocks[0].kind == 'bq':
            colophon = blocks.pop(0).html
        else:
            LOG.warn('no colophon blockquote after the title', doc.rel)
    doc.colophon_html = colophon.replace('<blockquote>', '<blockquote class="colophon">', 1)
    # ลิงก์ก่อนหน้า/ถัดไปท้ายบท (เป็น chrome ของสมุดต้นฉบับ — เว็บใช้ pager แทน)
    if blocks and blocks[-1].kind == 'p' and FOOTER_RE.match(blocks[-1].toks[1].content):
        foot = blocks.pop()
        if blocks and blocks[-1].kind == 'hr':
            blocks.pop()
        targets = []
        for c in foot.toks[1].children or []:
            if c.type == 'link_open':
                href = c.attrGet('href') or ''
                p = os.path.normpath(os.path.join(doc.src_dir, unquote(href.split('#')[0])))
                targets.append(os.path.relpath(p, ROOT).replace(os.sep, '/'))
        expected = [d.rel for d in (doc.prev, doc.next) if d is not None]
        if doc.part[0] == 'intro':
            expected = [doc.next.rel] if doc.next else []
        if targets != expected:
            LOG.warn(f'source footer links {targets} differ from book order {expected}', f'{doc.rel}:{foot.line}')
    doc.blocks = transform(blocks, ctx)
    doc.ctx = ctx
    # assertions against the markdown source
    nq, na = len(SRC_Q_RE.findall(src)), len(SRC_A_RE.findall(src))
    if ctx.qa != nq or ctx.qa != na:
        LOG.error(f'Q&A mismatch: rendered {ctx.qa} pairs, source has {nq} questions / {na} answers', doc.rel)
    nimg = len(re.findall(r'!\[[^\]]*\]\(', src))
    ncap = len(re.findall(r'^\*ภาพที่', src, re.M))
    if ctx.figures != nimg:
        LOG.error(f'figure mismatch: rendered {ctx.figures}, source has {nimg} images', doc.rel)
    if ctx.captions != ncap:
        LOG.error(f'caption mismatch: rendered {ctx.captions}, source has {ncap} captions', doc.rel)
    doc.src_qa, doc.src_img, doc.src_cap = nq, nimg, ncap
    body_text = ' '.join(html_to_text(b.html) for b in doc.blocks)
    doc.minutes = reading_minutes(body_text)
    doc.n_fig = ctx.figures
    doc.n_qa = ctx.qa
    doc.outline = [(b.level, b.id, norm_ws(b.text)) for b in doc.blocks if b.kind == 'h' and b.level in (2, 3)]
    ids = set(CHROME_IDS) | {doc.h1_id}
    for b in doc.blocks:
        ids.update(html.unescape(x) for x in re.findall(r'\bid="([^"]*)"', b.html))
    Site.ids[doc.out] = ids


# --------------------------------------------------------------------------- chrome

ICON_MENU = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
             'stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M4 6.5h16M4 12h16M4 17.5h11"/></svg>')
ICON_SEARCH = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
               'stroke-linecap="round" aria-hidden="true" focusable="false"><circle cx="10.5" cy="10.5" r="6.5"/>'
               '<path d="M15.5 15.5 20 20"/></svg>')

PREFS = '''<dialog id="prefs" class="prefs" aria-labelledby="prefs-h"><form method="dialog">
<h2 id="prefs-h">การแสดงผล</h2>
<fieldset class="seg"><legend>ธีม</legend>
<label><input type="radio" name="theme" value="auto">ตามระบบ</label><label><input type="radio" name="theme" value="light">สว่าง</label>
<label><input type="radio" name="theme" value="sepia">ซีเปีย</label><label><input type="radio" name="theme" value="dark">กลางคืน</label></fieldset>
<fieldset class="size"><legend>ขนาดตัวอักษร</legend>
<button type="button" data-step="-1">ก−<span class="vh"> ลดขนาดตัวอักษร</span></button><output>100%</output>
<button type="button" data-step="1">ก+<span class="vh"> เพิ่มขนาดตัวอักษร</span></button></fieldset>
<fieldset class="seg"><legend>แบบตัวอักษร</legend>
<label><input type="radio" name="face" value="book">แบบหนังสือ</label><label><input type="radio" name="face" value="sans">แบบเรียบ</label></fieldset>
<fieldset class="seg keys"><legend>แป้นลัด</legend>
<label><input type="radio" name="keys" value="on">เปิด</label><label><input type="radio" name="keys" value="off">ปิด</label></fieldset>
<p class="hint">← → เปลี่ยนบท · / ค้นหา · t สารบัญ</p>
<button class="btn" value="close">ปิด</button>
</form></dialog>'''


def header_html(root, runhead, search_current=False):
    cur = ' aria-current="page"' if search_current else ''
    return (f'<header class="site-header">\n<div class="h-left">\n'
            f'<a class="hbtn toc-btn" href="{root}index.html#toc" aria-controls="toc-drawer">{ICON_MENU}<span class="lbl">สารบัญ</span></a>\n'
            f'<a class="booktitle" href="{root}index.html">{BOOK}</a>\n</div>\n'
            f'<div class="runhead" aria-hidden="true">{esc(runhead)}</div>\n'
            f'<div class="h-right">\n'
            f'<a class="hbtn" href="{root}search.html"{cur}>{ICON_SEARCH}<span class="lbl">ค้นหา</span></a>\n'
            f'<button class="hbtn aa-btn" type="button" aria-haspopup="dialog" aria-controls="prefs">Aa<span class="vh"> ตั้งค่าการอ่าน</span></button>\n'
            f'</div>\n</header>')


def outline_list(doc):
    if not doc.outline:
        return ''
    out, open_h2 = ['<ol class="ol-list">'], False
    in_sub = False
    for level, hid, text in doc.outline:
        if level == 2:
            if in_sub:
                out.append('</ol>')
                in_sub = False
            if open_h2:
                out.append('</li>')
            out.append(f'<li><a href="#{esc(hid)}">{esc(text)}</a>')
            open_h2 = True
        else:
            if not open_h2:
                out.append('<li class="ol-orphan">')
                open_h2 = True
            if not in_sub:
                out.append('<ol>')
                in_sub = True
            out.append(f'<li><a href="#{esc(hid)}">{esc(text)}</a></li>')
    if in_sub:
        out.append('</ol>')
    if open_h2:
        out.append('</li>')
    out.append('</ol>')
    return ''.join(out)


def drawer_html(root, current=None):
    parts = []
    for part in SITE_PARTS:
        docs = [d for d in Site.docs if d.part is part]
        is_open = ' open' if current is not None and current.part is part else ''
        rows = []
        for d in docs:
            cur = ' aria-current="page"' if d is current else ''
            rows.append(f'<li><a href="{root}{d.out}"{cur}><span class="toc-num">{esc(d.num_toc)}</span>'
                        f'<span class="toc-title">{esc(d.title)}</span></a></li>')
        parts.append(f'<details class="toc-part"{is_open}><summary>{esc(part[1])}</summary>\n<ol>{"".join(rows)}</ol>\n</details>')
    here = ''
    if current is not None and current.outline:
        here = f'<details class="toc-here" open><summary>ในบทนี้</summary>{outline_list(current)}</details>\n'
    return (f'<dialog id="toc-drawer" class="drawer" aria-labelledby="toc-drawer-h">\n<div class="drawer-in">\n'
            f'<div class="drawer-top"><h2 id="toc-drawer-h">สารบัญ</h2><button type="button" class="hbtn drawer-close">ปิด</button></div>\n'
            f'{here}<nav class="toc toc-compact" aria-label="สารบัญทั้งเล่ม">\n' + '\n'.join(parts) + '\n</nav>\n'
            f'<p class="drawer-foot"><a href="{root}index.html">หน้าแรก</a> · <a href="{root}search.html">ค้นหา</a></p>\n'
            f'</div>\n</dialog>')


def footer_html(root, build):
    b = f'\n<p class="f-build">{build}</p>' if build else ''
    return (f'<footer class="site-footer">\n'
            f'<p>{BOOK} · บันทึกและเรียบเรียงโดย <b>{AUTHOR}</b></p>\n'
            f'<p class="disclaimer">บันทึกเพื่อการศึกษา ไม่ใช่สิ่งพิมพ์ทางการ — การทำงานจริงต้องใช้อนุสัญญา ประมวลข้อบังคับ แผนที่และสิ่งพิมพ์ฉบับปัจจุบัน SMS ของบริษัท และข้อกำหนดของรัฐเจ้าของธงเสมอ</p>\n'
            f'<p class="f-links"><a href="#top">กลับขึ้นด้านบน</a> · <a href="{root}index.html#toc">สารบัญ</a> · <a href="{root}search.html">ค้นหา</a></p>\n'
            f'<p class="f-credits">© {AUTHOR} · ฟอนต์ <a href="{root}assets/fonts/OFL-Trirong.txt">Trirong</a> และ '
            f'<a href="{root}assets/fonts/OFL-Sarabun.txt">Sarabun</a> (SIL Open Font License 1.1)</p>{b}\n'
            f'</footer>')


def compact_css(css):
    """ตัด comment และช่องว่างที่ไม่จำเป็น (ไม่แตะค่าใน calc() ที่ต้องมีช่องว่างรอบ + -) — ไม่ใช่ minifier เต็มรูป"""
    head, _, rest = css.partition('\n')
    head = head if head.startswith('/*') else ''
    rest = css if not head else rest
    rest = re.sub(r'/\*.*?\*/', '', rest, flags=re.S)
    rest = re.sub(r'\s+', ' ', rest)
    rest = re.sub(r'\s*([{};,])\s*', r'\1', rest)
    rest = re.sub(r'(^|[{}])([^{}@]+)(?=\{)', lambda m: m[1] + re.sub(r'\s*([>+~])\s*', r'\1', m[2]), rest)
    rest = rest.replace(';}', '}').strip()
    return (head + '\n' if head else '') + rest + '\n'


class Page:
    template = None
    assets = {}
    page_css = {}
    head_js = ''
    build = ''

    @classmethod
    def render(cls, **kw):
        root = kw['root']
        fonts = ' '.join(kw.get('preloads', PRELOAD_BASE))
        values = dict(
            root=root, page=kw['page'], html_attrs=f' data-fonts="{fonts}"' + kw.get('html_attrs', ''),
            title=esc(kw['title']), description=esc(kw['description']), head_js=cls.head_js,
            css_v=cls.assets['style.css'], ico_v=cls.assets['favicon.svg'], js_v=cls.assets['app.js'],
            rel_links=kw.get('rel_links', ''), extra_head=kw.get('extra_head', ''), body_class=kw['body_class'],
            progress=kw.get('progress', ''), header=kw['header'], drawer=kw['drawer'], main_class=kw.get('main_class', ''),
            main_attrs=kw.get('main_attrs', ''), main=kw['main'], outline=kw.get('outline', ''),
            footer=footer_html(root, cls.build), prefs_dialog=PREFS)
        return cls.template.substitute(values)


def pager_link(cls, rel, key, target, root):
    if target is None:
        n, t, href = '', 'หน้าแรก · สารบัญ', f'{root}index.html'
    else:
        n, t, href = target.num_display, target.title, root + target.out
    return (f'<a class="{cls}" rel="{rel}" href="{href}"><span class="pager-k">{key}</span>'
            f'<span class="pager-n">{esc(n)}</span><span class="pager-t">{esc(t)}</span></a>')


def doc_page(doc):
    root = doc.root
    meta = [f'≈ {doc.minutes} นาที']
    if doc.n_fig:
        meta.append(f'ภาพ {doc.n_fig}')
    if doc.n_qa:
        meta.append(f'คำถาม {doc.n_qa} ข้อ')
    if doc.date:
        meta.append(f'ปรับปรุงล่าสุด {thai_date(doc.date)}')
    if doc.th:
        chk = doc.num + (' ' + doc.en if doc.en else '')
        sep = ' — '
    else:
        chk = doc.num
        sep = ' '
    if not chk:
        h1 = f'<h1 id="{esc(doc.h1_id)}"><span class="ch-t">{esc(doc.title)}</span></h1>'
    else:
        h1 = (f'<h1 id="{esc(doc.h1_id)}"><span class="ch-k">{esc(chk)}</span><span class="vh">{sep}</span>'
              f'<span class="ch-t">{esc(doc.title)}</span></h1>')
    kicker = doc.part[1].replace(' — ', ' · ')
    if kicker == doc.num_display:          # บทนำ: ไม่ซ้ำคำเดียวกันสองบรรทัด
        kicker = 'IMO Model Course 7.03 · STCW A-II/1'
    if doc.is_appendix:                    # "ภาคผนวก ข" อยู่ในหัวเรื่องแล้ว
        kicker = ''
    kicker_html = f'<p class="kicker">{esc(kicker)}</p>\n' if kicker else ''
    opener = (f'<header class="opener">\n{kicker_html}{h1}\n'
              f'{doc.colophon_html}<p class="meta">{" · ".join(meta)}</p>\n</header>\n')
    body = ''.join(b.html for b in doc.blocks)
    pager = ('<nav class="pager" aria-label="เปลี่ยนบท">\n'
             + pager_link('pager-prev', 'prev', '← ก่อนหน้า', doc.prev, root) + '\n'
             + pager_link('pager-next', 'next', 'ถัดไป →', doc.next, root) + '\n</nav>\n')
    main = opener + body + '<p class="endmark" aria-hidden="true">๛</p>\n' + pager
    prev_href = root + doc.prev.out if doc.prev else f'{root}index.html'
    next_href = root + doc.next.out if doc.next else f'{root}index.html'
    outline = ''
    if doc.outline:
        outline = f'<aside class="outline" aria-label="ในบทนี้"><p class="outline-h">ในบทนี้</p>{outline_list(doc)}</aside>'
    preloads = PRELOAD_DOC + ([PRELOAD_ITALIC] if '<em>' in doc.colophon_html else [])
    return Page.render(
        root=root, page=doc.page, preloads=preloads,
        title=f'{doc.num_display} {doc.title} · {BOOK}',
        description=f'{doc.title} — {BOOK} (IMO Model Course 7.03 / STCW A-II/1) โดย {AUTHOR}',
        rel_links=f'<link rel="prev" href="{prev_href}">\n<link rel="next" href="{next_href}">',
        body_class='page-doc',
        progress='<div class="progress" aria-hidden="true"><span></span></div>',
        header=header_html(root, f'{doc.num_display} {doc.title}'),
        drawer=drawer_html(root, doc),
        main_class=' has-outline' if outline else '',
        main_attrs=f' data-num="{esc(doc.num_display)}" data-title="{esc(doc.title)}"',
        main=main, outline=outline)


# --------------------------------------------------------------------------- cover

def readme_sections():
    """คำนำ (หลังเส้นคั่นแรกจนถึงเส้นคั่น/หัวข้อถัดไป) และหัวข้อ 'วิธีอ่าน' จาก README"""
    ctx = Ctx('README.md', ROOT, 'index.html', '')
    ctx.used.update(COVER_IDS)
    blocks = to_blocks(md.parse(read(os.path.join(ROOT, 'README.md'))), ctx)
    preface, howto = [], []
    k = next((i for i, b in enumerate(blocks) if b.kind == 'hr'), None)
    if k is None:
        LOG.warn('README has no "---" before the preface', 'README.md')
    else:
        for b in blocks[k + 1:]:
            if b.kind == 'hr' or (b.kind == 'h' and b.level <= 2):
                break
            preface.append(b)
    start = next((i for i, b in enumerate(blocks) if b.kind == 'h' and b.level == 2 and b.text.strip() == 'วิธีอ่าน'), None)
    if start is None:
        LOG.warn('README has no "## วิธีอ่าน" section', 'README.md')
    else:
        howto.append(blocks[start])
        for b in blocks[start + 1:]:
            if b.kind == 'hr' or (b.kind == 'h' and b.level <= 2):
                break
            howto.append(b)
    preface = transform(preface, ctx, top_level=2)
    howto = transform(howto, ctx)
    return ctx, preface, howto


def cover_ids(preface, howto):
    ids = set(CHROME_IDS) | COVER_IDS
    for b in preface + howto:
        ids.update(html.unescape(x) for x in re.findall(r'\bid="([^"]*)"', b.html))
    Site.ids['index.html'] = ids


def cover_page(preface, howto, stats):
    tparts = []
    for part in SITE_PARTS:
        docs = [d for d in Site.docs if d.part is part]
        rows = []
        for d in docs:
            en = f'<span class="toc-en">{esc(d.en)}</span>' if d.th and d.en else ''
            mins = '' if d.is_appendix else f'≈ {d.minutes} นาที'
            rows.append(f'<li><a class="toc-row" href="{d.out}">\n<span class="toc-num">{esc(d.num_toc)}</span>\n'
                        f'<span class="toc-title">{esc(d.title)}{en}</span>\n'
                        f'<span class="toc-lead" aria-hidden="true"></span><span class="toc-min">{mins}</span></a></li>')
        sub = f'<p class="toc-part-sub">{esc(part[2])}</p>' if part[2] else ''
        tparts.append(f'<div class="toc-part"><h3 class="toc-part-h">{esc(part[1])}</h3>{sub}\n'
                      f'<ol class="toc-list">\n' + '\n'.join(rows) + '\n</ol></div>')
    st = [f'{stats["chapters"]} บท', f'{stats["appendices"]} ภาคผนวก', f'ภาพประกอบ {stats["images"]} ภาพ',
          f'คำถามท้ายบท {stats["qa_chapters"]} ข้อ']
    if stats['date']:
        st.append(f'ปรับปรุงล่าสุด {thai_date(stats["date"], with_day=False)}')
    titlepage = (
        '<header class="titlepage">\n'
        '<div class="tp-monogram" aria-hidden="true"><span>OOW</span></div>\n'
        '<p class="tp-kicker">IMO MODEL COURSE 7.03 · STCW A-II/1</p>\n'
        '<h1 class="tp-title">สมุดบันทึกการฝึกนายประจำเรือฝ่ายเดินเรือ</h1>\n'
        '<p class="tp-sub">OOW Training Notebook</p>\n'
        '<span class="tp-rule" aria-hidden="true"></span>\n'
        '<p class="tp-desc">Officer in Charge of a Navigational Watch (ships of 500 GT or more)</p>\n'
        f'<p class="tp-by"><span>บันทึกและเรียบเรียงโดย</span><b>{AUTHOR}</b></p>\n'
        f'<p class="tp-actions"><a class="btn" href="{Site.docs[0].out}">เริ่มอ่าน</a><a href="#toc">สารบัญ ↓</a></p>\n'
        '<aside class="tp-panel" aria-label="ภาพรวมสมุด"><p class="tp-panel-kicker">NAVIGATIONAL STUDIES</p>'
        '<div class="tp-panel-mark" aria-hidden="true"><span>7.03</span></div>'
        f'<dl><div><dt>บทและภาคผนวก</dt><dd>{stats["chapters"]} + {stats["appendices"]}</dd></div>'
        f'<div><dt>ภาพประกอบ</dt><dd>{stats["images"]}</dd></div>'
        f'<div><dt>คำถามท้ายบท</dt><dd>{stats["qa_chapters"]}</dd></div></dl></aside>\n'
        '<a class="continue" href="#"><span class="c-k">อ่านต่อจากครั้งก่อน</span><span class="c-t"></span>'
        '<span class="c-s"><span class="c-sec"></span><span class="c-pct"></span></span><span class="c-bar"><i></i></span></a>\n'
        f'<p class="tp-stats">{" · ".join(st)}</p>\n'
        '</header>\n')
    main = (titlepage + '<h2 id="preface">คำนำ</h2>\n' + ''.join(b.html for b in preface)
            + '<h2 id="toc">สารบัญ</h2>\n<nav class="toc" aria-labelledby="toc">\n' + '\n'.join(tparts) + '\n</nav>\n'
            + ''.join(b.html for b in howto))
    return Page.render(
        root='', page='index.html', title=COVER_TITLE, preloads=PRELOAD_SHORT,
        description=f'{COVER_TITLE.split(" — ")[0]} — {BOOK} (IMO Model Course 7.03 / STCW A-II/1) โดย {AUTHOR}',
        rel_links=f'<link rel="next" href="{Site.docs[0].out}">',
        extra_head=f'<style>{Page.page_css["cover"].strip()}</style>',
        body_class='page-cover', header=header_html('', ''), drawer=drawer_html(''),
        main_class=' cover', main=main)


def page_404():
    """หน้า 404 ไม่มีไฟล์ภายนอกเลย (CSS/JS inline) เพราะ GitHub Pages เสิร์ฟที่ path ใดก็ได้ — สคริปต์ในหน้าหาฐานของเว็บ
    จาก path ของ repo ใน SITE_URL แล้วตั้งลิงก์และฟอนต์เอง ไม่มี JS ลิงก์ชี้ไปที่ SITE_URL"""
    base_path = urlsplit(SITE_URL).path
    page = read(os.path.join(SITE_SRC, 'templates', '404.html'))
    for k, v in (('{{SITE_URL}}', SITE_URL), ('{{BASE_PATH}}', base_path)):
        if k not in page:
            LOG.error(f'placeholder {k} missing', 'tools/site/templates/404.html')
        page = page.replace(k, v)
    return page


def search_page(index_v):
    main = ('<h1 class="search-h">ค้นหาในสมุด</h1>\n'
            '<form class="search-form" role="search" action="search.html" method="get">\n'
            '<label for="q" class="vh">คำค้น</label>\n'
            '<input id="q" name="q" type="search" placeholder="ค้นหาในสมุด… เช่น Rule 19, ไฟเรือ" autocomplete="off" '
            'enterkeyhint="search" spellcheck="false">\n</form>\n'
            '<p class="search-status" role="status" aria-live="polite"></p>\n'
            '<div class="search-results"></div>\n'
            '<noscript><p>การค้นหาต้องใช้ JavaScript — ใช้ Ctrl+F ในหน้าบท หรือดู <a href="index.html#toc">สารบัญ</a></p></noscript>\n')
    return Page.render(
        root='', page='search.html', html_attrs=f' data-index-v="{index_v}"', preloads=PRELOAD_SHORT,
        title=f'ค้นหา · {BOOK}', description=f'ค้นหา — {BOOK} (IMO Model Course 7.03 / STCW A-II/1) โดย {AUTHOR}',
        extra_head=(f'<script src="assets/search.js?v={Page.assets["search.js"]}" defer></script>\n'
                    f'<style>{Page.page_css["search"].strip()}</style>'),
        body_class='page-search', header=header_html('', '', search_current=True), drawer=drawer_html(''),
        main_class=' search', main=main)


# --------------------------------------------------------------------------- search index

def search_index():
    recs = []
    for doc in Site.docs:
        if doc.stem.startswith('D-') and doc.is_appendix:
            continue
        is_b = doc.is_appendix and doc.stem.startswith('B-')
        sec = ['', doc.h1_text, []]          # anchor, heading, text parts
        sections = [sec]
        qas = []
        skip = False
        colophon = html_to_text(doc.colophon_html)
        boiler = f'{BOOK} · {AUTHOR}'
        if colophon.startswith(boiler):
            colophon = colophon[len(boiler):]
        sec[2].append(colophon)
        for b in doc.blocks:
            if b.kind == 'h' and b.level <= 3:
                skip = is_b and b.level == 3 and b.id.startswith('q-')
                sec = [b.id, norm_ws(b.text), []]
                sections.append(sec)
                qas.append(('sec', sec))
                continue
            if b.kind == 'qa':
                if not skip:
                    qas.append(('qa', b, sec))
                continue
            if b.kind == 'tools' or skip:
                continue
            sec[2].append(html_to_text(b.html))
        # interleave in book order: lead section, then for each heading its section followed by its Q&A
        recs.append([doc.idx, '', norm_search(doc.h1_text), norm_search(' '.join(sections[0][2])), 0])
        for item in qas:
            if item[0] == 'sec':
                s = item[1]
                recs.append([doc.idx, s[0], norm_search(s[1]), norm_search(' '.join(s[2])), 0])
            else:
                b, s = item[1], item[2]
                ql, q, al, a = b.qa
                recs.append([doc.idx, b.id, norm_search(s[1]), norm_search(f'{ql}: {q} {al}: {a}'), 1])
    for r in recs:
        for s in (r[2], r[3]):
            if len(s.lower()) != len(s):
                LOG.error(f'search text changes length when lower-cased: {s[:40]!r}', Site.docs[r[0]].rel)
    data = {'v': 1, 'docs': [[d.out, d.num_display, d.title] for d in Site.docs], 'recs': recs}
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')), len(recs)


# --------------------------------------------------------------------------- validation of _site

CSS_URL_RE = re.compile(r'url\(\s*["\']?([^"\')]*)')


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.urls = []      # (tag, attr, value, line)
        self.fonts = []     # names from <html data-fonts>
        self.h1 = 0
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        for k, v in attrs:
            if k == 'id' and v is not None:
                self.ids.append(v)
            elif k in ('href', 'src', 'action') and v is not None:
                self.urls.append((tag, k, v, line))
            elif k in ('srcset', 'imagesrcset') and v:
                for cand in v.split(','):
                    if cand.strip():
                        self.urls.append((tag, 'src', cand.split()[0], line))
            elif k == 'style' and v and 'url(' in v:
                for u in CSS_URL_RE.findall(v):
                    self.urls.append((tag, 'url()', u, line))
            elif k == 'data-fonts' and v:
                self.fonts.extend(v.split())
        if tag == 'h1':
            self.h1 += 1
        if tag == 'style':
            self.in_style = True

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.in_style = False

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False

    def handle_data(self, data):
        if self.in_style and 'url(' in data:
            line = self.getpos()[0]
            for u in CSS_URL_RE.findall(data):
                self.urls.append(('style', 'url()', u, line))


def validate_site(out):
    pages = {}
    for dp, dns, fns in os.walk(out):
        dns.sort()
        for fn in sorted(fns):
            if fn.endswith('.html'):
                path = os.path.join(dp, fn)
                p = PageParser()
                p.feed(read(path))
                rel = os.path.relpath(path, out).replace(os.sep, '/')
                pages[rel] = p
    for rel, p in sorted(pages.items()):
        seen = set()
        for i in p.ids:
            if i in seen:
                LOG.error(f'duplicate id "{i}"', f'_site/{rel}')
            seen.add(i)
        if p.h1 != 1:
            LOG.error(f'page has {p.h1} <h1> elements (expected 1)', f'_site/{rel}')
    for rel, p in sorted(pages.items()):
        base = posixpath.dirname(rel)
        for f in p.fonts:
            if not os.path.isfile(os.path.join(out, 'assets', 'fonts', f + '.woff2')):
                LOG.error(f'data-fonts names a missing font: {f}', f'_site/{rel}')
        for tag, attr, v, line in p.urls:
            where = f'_site/{rel}:{line}'
            if v.startswith('/'):
                LOG.error(f'root-absolute URL {v!r}', where)
                continue
            if re.match(r'^https?:', v, re.I):
                if attr in ('src', 'url()') or tag == 'link':
                    LOG.error(f'external resource {v!r}', where)
                continue
            if re.match(r'^[a-z][a-z0-9+.-]*:', v, re.I):
                if v.startswith(('mailto:', 'data:')):
                    continue
                LOG.error(f'unsupported URL {v!r}', where)
                continue
            path, _, frag = v.partition('#')
            path = path.split('?')[0]
            if path.endswith('.md'):
                LOG.error(f'.md link left in output: {v}', where)
                continue
            target = rel if not path else posixpath.normpath(posixpath.join(base, unquote(path)))
            if target.startswith('..') or not os.path.isfile(os.path.join(out, target)):
                LOG.error(f'broken link {v!r}', where)
                continue
            frag = unquote(frag)
            if frag and target.endswith('.html'):
                tp = pages.get(target)
                if tp is None or frag not in tp.ids:
                    LOG.error(f'missing fragment #{frag} in {target}', where)
    css = read(os.path.join(out, 'assets', 'style.css'))
    for u in re.findall(r'url\(\s*["\']?([^"\')]*)', css):
        if u.startswith('/') or re.match(r'^https?:', u, re.I):
            LOG.error(f'CSS url() not allowed: {u}', '_site/assets/style.css')
        elif not u.startswith('data:') and not os.path.isfile(os.path.join(out, 'assets', u)):
            LOG.error(f'CSS url() target missing: {u}', '_site/assets/style.css')
    return pages


# --------------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description='Build the online-book site (GitHub Pages) into _site/')
    ap.add_argument('--out', default=os.path.join(ROOT, '_site'))
    ap.add_argument('--no-git', action='store_true', help='skip "last updated" dates and the build stamp')
    args = ap.parse_args(argv)
    out = os.path.realpath(os.path.abspath(args.out))
    root_real = os.path.realpath(ROOT)
    forbidden = [root_real] + [os.path.join(root_real, d) for d in SOURCE_DIRS]
    if out in forbidden or root_real.startswith(out + os.sep) or out == os.sep or \
            any(out.startswith(f + os.sep) for f in forbidden[1:]):
        print(f'refusing to build into {out}: it is the repository root, a source directory or one of their parents',
              file=sys.stderr)
        return 1
    if os.path.lexists(out) and not os.path.isdir(out):
        print(f'refusing to build into {out}: it exists and is not a directory', file=sys.stderr)
        return 1
    if os.path.isdir(out) and os.listdir(out) and not looks_like_build(out):
        print(f'refusing to replace {out}: it is not empty and does not look like a previous build '
              f'(no {", ".join(BUILD_MARKERS)}) — choose an empty or new directory', file=sys.stderr)
        return 1

    docs = collect_docs()
    if not docs:
        print('error: no documents found', file=sys.stderr)
        return 1
    Site.docs = docs
    Site.by_rel = {d.rel: d for d in docs}
    use_git = not args.no_git
    if use_git:
        for d in docs:
            d.date = git('log', '-1', '--format=%cs', '--', d.rel) or None
        head = git('log', '-1', '--format=%h %cs')
        if head:
            sha, day = head.split()
            Page.build = f'ฉบับวันที่ {thai_date(day)} · <span class="f-sha">{esc(sha)}</span>'

    # pass 1: render every document, collect ids
    for d in docs:
        process_doc(d)

    # assets (needed for page shells)
    def asset(name, sub):
        return read(os.path.join(SITE_SRC, sub, name))
    Page.page_css = {k: compact_css(asset(k + '.css', 'css')) for k in ('cover', 'search')}
    assets_txt = {'style.css': compact_css(asset('style.css', 'css')), 'app.js': asset('app.js', 'js'),
                  'search.js': asset('search.js', 'js'), 'favicon.svg': read(os.path.join(SITE_SRC, 'favicon.svg'))}
    Page.assets = {k: sha8(v) for k, v in assets_txt.items()}
    Page.head_js = read(os.path.join(SITE_SRC, 'js', 'head.js')).strip()
    Page.template = string.Template(read(os.path.join(SITE_SRC, 'templates', 'page.html')))

    images = sorted(f for f in os.listdir(os.path.join(ROOT, 'images')) if not f.startswith('.'))
    stats = {'chapters': sum(1 for d in docs if d.rel.startswith('chapters/')),
             'appendices': sum(1 for d in docs if d.is_appendix),
             'images': len(images),
             'qa_chapters': sum(d.n_qa for d in docs if d.rel.startswith('chapters/')),
             'date': max((d.date for d in docs if d.date), default=None)}
    # README blocks for the cover; their ids are needed before pass 2 (README.md#… resolves to index.html)
    cover_ctx, preface, howto = readme_sections()
    cover_ids(preface, howto)

    # pass 2: rewrite links now that every page's ids are known
    for d in docs:
        for b in d.blocks:
            b.html = rewrite_links(b.html, d.ctx, f'{d.rel}:{b.line}' if b.line else d.rel)
        d.colophon_html = rewrite_links(d.colophon_html, d.ctx, d.rel)
    for b in preface + howto:
        b.html = rewrite_links(b.html, cover_ctx, f'README.md:{b.line}' if b.line else 'README.md')
    cover_html = cover_page(preface, howto, stats)

    index_json, n_recs = search_index()
    index_v = sha8(index_json)

    if LOG.errors:
        return report(1, None)

    # write into a fresh sibling directory, validate it there, then swap it into place: a failed build leaves the
    # previous output untouched, and builds running at the same time cannot delete each other's files mid-check
    final_out = out
    out = f'{final_out}.tmp-{os.getpid()}'
    if os.path.lexists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    try:
        code = write_site(out, final_out, assets_txt, docs, cover_html, index_v, index_json, images, n_recs)
        if code == 0 and not swap_into_place(out, final_out):
            LOG.error(f'could not move the build into {final_out} (another build kept replacing it)')
            code = report(1, None)
        elif code == 0:
            code = report(0, LOG.summary)
        return code
    finally:
        if os.path.lexists(out):
            shutil.rmtree(out, ignore_errors=True)


BUILD_MARKERS = ('index.html', '404.html', 'assets/style.css')


def looks_like_build(path):
    return all(os.path.isfile(os.path.join(path, m)) for m in BUILD_MARKERS)


def swap_into_place(tmp, out):
    """แทนที่ out ด้วย tmp — rename ภายในโฟลเดอร์แม่เดียวกัน (เกือบ atomic)"""
    for _ in range(5):
        old = None
        if os.path.lexists(out):
            old = f'{out}.old-{os.getpid()}'
            try:
                os.rename(out, old)
            except FileNotFoundError:
                old = None
        try:
            os.rename(tmp, out)
        except OSError:
            if old:
                shutil.rmtree(old, ignore_errors=True)
            continue
        if old:
            shutil.rmtree(old, ignore_errors=True)
        return True
    return False


def write_site(out, final_out, assets_txt, docs, cover_html, index_v, index_json, images, n_recs):
    write(os.path.join(out, 'index.html'), cover_html)
    write(os.path.join(out, 'search.html'), search_page(index_v))
    write(os.path.join(out, '404.html'), page_404())
    for d in docs:
        write(os.path.join(out, d.out), doc_page(d))
    adir = os.path.join(out, 'assets')
    for name, txt in assets_txt.items():
        write(os.path.join(adir, name), txt)
    write(os.path.join(adir, 'search-index.json'), index_json)
    write(os.path.join(adir, 'search-index.js'),
          'window.OOW_SEARCH=' + index_json.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029') + ';\n')
    fdir = os.path.join(adir, 'fonts')
    os.makedirs(fdir)
    for src_dir, pat in ((PDF_FONTS, r'^sarabun-.*\.woff2$|^OFL-Sarabun\.txt$'),
                         (os.path.join(SITE_SRC, 'fonts'), r'^trirong-.*\.woff2$|^OFL-Trirong\.txt$')):
        for f in sorted(os.listdir(src_dir)):
            if re.match(pat, f):
                shutil.copyfile(os.path.join(src_dir, f), os.path.join(fdir, f))
    idir = os.path.join(out, 'images')
    os.makedirs(idir)
    for f in images:
        shutil.copyfile(os.path.join(ROOT, 'images', f), os.path.join(idir, f))

    pages = validate_site(out)
    total_fig = sum(d.n_fig for d in docs)
    total_cap = sum(d.ctx.captions for d in docs)
    total_qa = sum(d.n_qa for d in docs)
    if total_fig != sum(d.src_img for d in docs) or total_cap != sum(d.src_cap for d in docs) \
            or total_qa != sum(d.src_qa for d in docs):
        LOG.error('figure/caption/Q&A totals do not match the sources')
    if LOG.errors:
        return report(1, None)
    size = 0
    largest = ('', 0)
    for dp, dns, fns in os.walk(out):
        for fn in fns:
            s = os.path.getsize(os.path.join(dp, fn))
            size += s
            if fn.endswith('.html') and s > largest[1]:
                largest = (os.path.relpath(os.path.join(dp, fn), out), s)
    summary = (f'built {final_out}: {len(docs)} docs, {len(pages)} pages, {len(images)} images copied, '
               f'{total_fig} figures, {total_cap} captions, {total_qa} Q&A, '
               f'{sum(d.ctx.tables for d in docs)} tables, {n_recs} search records, 0 broken links, '
               f'{size / 1e6:.1f} MB total, largest page {largest[0]} ({largest[1] / 1e3:.0f} KB)')
    LOG.summary = summary
    return 0


def report(code, summary):
    for w in LOG.warnings:
        print('warning: ' + w, file=sys.stderr)
    for e in LOG.errors:
        print('error: ' + e, file=sys.stderr)
    if code == 0:
        print(summary)
    else:
        print(f'build failed: {len(LOG.errors)} error(s)', file=sys.stderr)
    return code


if __name__ == '__main__':
    sys.exit(main())
