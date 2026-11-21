"""สคริปต์สร้างภาพประกอบ COLREG: ส่วนโค้งไฟ สถานการณ์เรือ ไฟเรือแต่ละประเภท ทุ่นวัน ฯลฯ"""
import math, os
R = math.radians
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
W_, Rd, Gn, Yl = '#ffffff', '#ef4444', '#22c55e', '#facc15'

def head(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker>'
            '<marker id="dm" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" fill="#334155"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{title}</text>\n')

def save(n, s): open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')

def sector(cx, cy, r, b1, b2, col, op=0.35):
    """bearing relative to ship's head (0 = ahead, up), clockwise"""
    a1, a2 = R(b1), R(b2)
    x1, y1 = cx + r * math.sin(a1), cy - r * math.cos(a1)
    x2, y2 = cx + r * math.sin(a2), cy - r * math.cos(a2)
    large = 1 if (b2 - b1) % 360 > 180 else 0
    return f'<path d="M {cx} {cy} L {x1:.1f} {y1:.1f} A {r} {r} 0 {large} 1 {x2:.1f} {y2:.1f} Z" fill="{col}" opacity="{op}" stroke="{col}"/>\n'

def ship_top(cx, cy, L=90, B=26, col='#334155', hd=0):
    pts = [(0, -L / 2), (B / 2, -L / 4), (B / 2, L / 2), (-B / 2, L / 2), (-B / 2, -L / 4)]
    a = R(hd)
    P = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    return '<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in P) + f'" fill="{col}" stroke="#0f172a"/>\n'

def light_arcs():
    w, h = 900, 640
    s = head(w, h, 'ส่วนโค้งของไฟเดินเรือ (Rule 21) — มองจากด้านบน')
    cx, cy, r = 340, 350, 250
    s += sector(cx, cy, r, -112.5, 112.5, '#e5e7eb', 0.9)
    s += sector(cx, cy, r * 0.82, 0, 112.5, Gn, 0.45)
    s += sector(cx, cy, r * 0.82, -112.5, 0, Rd, 0.45)
    s += sector(cx, cy, r * 0.62, 112.5, 247.5, '#94a3b8', 0.5)
    s += ship_top(cx, cy)
    for b, lab in [(0, '0° (หัวเรือ)'), (112.5, '112.5° (22.5° abaft beam)'), (-112.5, '22.5° abaft beam'), (180, '')]:
        a = R(b)
        s += f'<line x1="{cx}" y1="{cy}" x2="{cx+r*math.sin(a):.1f}" y2="{cy-r*math.cos(a):.1f}" stroke="#334155" stroke-dasharray="5 4"/>\n'
    # แนวกราบ (beam, 90°) เส้นจุด และป้าย 22.5° ระหว่างแนวกราบกับขอบไฟข้าง
    for b in (90, -90):
        a = R(b)
        s += f'<line x1="{cx}" y1="{cy}" x2="{cx+r*math.sin(a):.1f}" y2="{cy-r*math.cos(a):.1f}" stroke="#0f172a" stroke-width="1" stroke-dasharray="2 3"/>\n'
    HALO = 'stroke="#fff" stroke-width="4" paint-order="stroke"'
    s += f'<text x="{cx+r-4}" y="{cy-6}" text-anchor="end" font-size="12" fill="#0f172a" {HALO}>แนวกราบ (beam)</text>\n'
    s += f'<text x="{cx-r+4}" y="{cy-6}" font-size="12" fill="#0f172a" {HALO}>แนวกราบ (beam)</text>\n'
    for b in (101.25, -101.25):
        a = R(b)
        s += f'<text x="{cx+228*math.sin(a):.1f}" y="{cy-228*math.cos(a)+4:.1f}" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">22.5°</text>\n'
    s += f'<text x="{cx}" y="{cy-r-10}" text-anchor="middle" font-size="13">หัวเรือ (ahead)</text>\n'
    s += f'<text x="{cx+120}" y="{cy-60}" font-size="15" font-weight="bold" fill="#15803d">Starboard sidelight</text><text x="{cx+120}" y="{cy-40}" font-size="13" fill="#15803d">เขียว 112.5°</text>\n'
    s += f'<text x="{cx-280}" y="{cy-60}" font-size="15" font-weight="bold" fill="#b91c1c">Port sidelight</text><text x="{cx-280}" y="{cy-40}" font-size="13" fill="#b91c1c">แดง 112.5°</text>\n'
    s += f'<text x="{cx}" y="{cy+r*0.62+32:.0f}" text-anchor="middle" font-size="15" font-weight="bold" fill="#334155" {HALO}>Sternlight ขาว 135°</text>\n'
    s += f'<text x="{cx}" y="{cy-r+28}" text-anchor="middle" font-size="15" font-weight="bold" fill="#475569" {HALO}>Masthead light ขาว 225°</text>\n'
    s += f'<text x="{cx}" y="{cy-r+46}" text-anchor="middle" font-size="12" fill="#475569" {HALO}>(แถบสีเทารอบนอก)</text>\n'
    s += '<rect x="620" y="70" width="270" height="250" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    rows = ['Masthead 225° = 112.5° ×2', 'Sidelight 112.5° (หัว → 22.5°', '   abaft the beam)', 'Sternlight 135° (67.5° ×2', '   จากท้ายตรง)', 'Towing light เหลือง 135°', 'All-round 360°', 'Flashing ≥120 ครั้ง/นาที', '225° + 135° = 360° พอดี']
    for i, t in enumerate(rows):
        s += f'<text x="634" y="{98 + i*25}" font-size="14">{t}</text>\n'
    s += '<text x="620" y="360" font-size="13" fill="#334155">เส้น "22.5° abaft the beam" คือขอบเขต</text>\n'
    s += '<text x="620" y="380" font-size="13" fill="#334155">ระหว่าง "เห็นไฟข้าง" กับ "เห็นไฟท้าย"</text>\n'
    s += '<text x="620" y="400" font-size="13" fill="#334155">= เส้นแบ่งสถานะ overtaking (Rule 13)</text>\n'
    save('colreg-light-arcs.svg', s)

def situations():
    w, h = 960, 610
    s = head(w, h, 'สถานการณ์การพบกัน: Head-on / Crossing / Overtaking (Rules 13–15)')
    cx, cy, r = 300, 320, 220
    s += sector(cx, cy, r, -6, 6, '#f59e0b', 0.45)
    s += sector(cx, cy, r, 6, 112.5, Gn, 0.25)
    s += sector(cx, cy, r, -112.5, -6, Rd, 0.25)
    s += sector(cx, cy, r, 112.5, 247.5, '#64748b', 0.25)
    s += ship_top(cx, cy, 70, 20)
    s += f'<text x="{cx-58}" y="{cy-r-8}" font-size="14" font-weight="bold" fill="#b45309">Head-on (Rule 14)</text>\n'
    s += f'<text x="{cx+70}" y="{cy-40}" font-size="14" font-weight="bold" fill="#15803d">เรืออื่นอยู่กราบขวา:</text><text x="{cx+70}" y="{cy-20}" font-size="13" fill="#15803d">เรา = Give-way (Rule 15)</text>\n'
    s += f'<text x="{cx-230}" y="{cy-40}" font-size="14" font-weight="bold" fill="#b91c1c">เรืออื่นอยู่กราบซ้าย:</text><text x="{cx-230}" y="{cy-20}" font-size="13" fill="#b91c1c">เรา = Stand-on (Rule 17)</text>\n'
    s += f'<text x="{cx-150}" y="{cy+170}" font-size="14" font-weight="bold" fill="#334155">เรือที่ตามมาทันเราจากเขตนี้ = กำลังแซง</text><text x="{cx-150}" y="{cy+190}" font-size="13" fill="#334155">(เห็นไฟท้ายเรา) → เขาต้องหลบ (Rule 13)</text>\n'
    s += '<rect x="580" y="70" width="360" height="460" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    rows = [('Rule 13 Overtaking', True), ('เข้ามาจากทิศ > 22.5° abaft the beam', False), ('กลางคืนเห็นเฉพาะไฟท้าย ไม่เห็นไฟข้าง', False), ('ผู้แซงต้องหลบจนพ้นและผ่านไปแล้ว', False), ('สงสัย → ให้ถือว่ากำลังแซง', False), ('', False), ('Rule 14 Head-on', True), ('สวนกันตรงหรือเกือบตรง (reciprocal)', False), ('เห็นไฟเสาเรียงกัน และ/หรือ ไฟข้างทั้งสอง', False), ('ทั้งสองลำเปลี่ยนเข็มไปทางขวา', False), ('', False), ('Rule 15 Crossing', True), ('ลำที่เห็นอีกลำทางกราบขวาของตน = หลบ', False), ('หลีกเลี่ยงการตัดหน้า (avoid crossing ahead)', False), ('', False), ('Rule 16/17', True), ('Give-way: early &amp; substantial action', False), ('Stand-on: keep course &amp; speed', False), ('→ may act / shall act เมื่อจำเป็น', False)]
    for i, (t, b) in enumerate(rows):
        fw = ' font-weight="bold" fill="#1e3a8a"' if b else ''
        s += f'<text x="596" y="{96 + i*23}" font-size="13"{fw}>{t}</text>\n'
    s += '<text x="20" y="566" font-size="12" fill="#334155">หมายเหตุ: เขต head-on ±6° ในภาพเป็นแนวทางประมาณในทางปฏิบัติเท่านั้น — Rule 14 ใช้คำว่า "ahead or nearly ahead" ไม่ได้กำหนดตัวเลขมุม</text>\n'
    s += '<text x="20" y="586" font-size="12" fill="#334155">เขตกราบซ้าย/ขวาใช้กับ crossing ระหว่างเรือกลสองลำที่มองเห็นกัน (Rule 15) — ถ้าเป็นเรือต่างประเภท ให้ดู Rule 18 ก่อน</text>\n'
    save('colreg-situations.svg', s)

# ---------- light configurations (side/front glyph) ----------
def lamp(x, y, col, r=7):
    """col ขึ้นต้นด้วย 'F' = ไฟกะพริบ (flashing) เช่น 'F#facc15' — วาดรัศมีเส้นรอบดวง"""
    rays = ''
    if col.startswith('F'):
        col = col[1:]
        for k in range(8):
            a = R(k * 45)
            rays += (f'<line x1="{x + (r+4)*math.cos(a):.1f}" y1="{y + (r+4)*math.sin(a):.1f}" '
                     f'x2="{x + (r+10)*math.cos(a):.1f}" y2="{y + (r+10)*math.sin(a):.1f}" stroke="{col}" stroke-width="2"/>')
    glow = f'<circle cx="{x}" cy="{y}" r="{r+5}" fill="{col}" opacity="0.25"/>'
    return rays + glow + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" stroke="#0f172a" stroke-width="0.8"/>\n'

def lights_gallery():
    items = [
        ('Power-driven &lt; 50 m (มองจากหัว)', [(0, -60, W_), (-22, -22, Rd), (22, -22, Gn)], 'masthead + sidelights'),
        ('Power-driven ≥ 50 m (เห็นกราบขวา)', [(30, -50, W_), (-30, -72, W_), (10, -22, Gn)], 'หัวไปขวา: masthead หน้าต่ำ-หลังสูง + เขียว'),
        ('Towing ≤ 200 m (มองจากท้าย)', [(0, -20, W_), (0, -42, Yl)], 'sternlight + towing light เหลือง'),
        ('Towing > 200 m (มองจากหัว)', [(0, -40, W_), (0, -62, W_), (0, -84, W_), (-22, -22, Rd), (22, -22, Gn)], 'masthead 3 ดวงแนวตั้ง'),
        ('NUC – making way (หัว)', [(0, -60, Rd), (0, -82, Rd), (-22, -22, Rd), (22, -22, Gn)], '2 แดง all-round + ไฟข้าง'),
        ('RAM – making way (หัว)', [(0, -50, Rd), (0, -72, W_), (0, -94, Rd), (16, -110, W_), (-22, -22, Rd), (22, -22, Gn)], 'แดง-ขาว-แดง + masthead'),
        ('Constrained by draught (หัว)', [(0, -50, Rd), (0, -72, Rd), (0, -94, Rd), (16, -112, W_), (-22, -22, Rd), (22, -22, Gn)], '3 แดง all-round (option)'),
        ('Trawling – making way (หัว)', [(0, -60, Gn), (0, -82, W_), (14, -104, W_), (-22, -22, Rd), (22, -22, Gn)], 'เขียวบนขาว (+masthead หลัง)'),
        ('Fishing (not trawling) – ไม่มี way', [(0, -82, Rd), (0, -60, W_), (30, -40, W_)], 'แดงบนขาว (+ขาวทิศเครื่องมือ)'),
        ('Pilot vessel on duty (หัว)', [(0, -60, Rd), (0, -82, W_), (-22, -22, Rd), (22, -22, Gn)], 'ขาวบนแดง ("White Hat Red Nose")'),
        ('At anchor ≥ 50 m (หัวเรือไปทางซ้าย)', [(-34, -60, W_), (34, -36, W_)], 'ขาวหัวสูงกว่าขาวท้าย'),
        ('Aground (หัวเรือไปทางซ้าย)', [(-34, -60, W_), (34, -36, W_), (0, -70, Rd), (0, -92, Rd)], 'anchor lights + 2 แดง'),
        ('Sailing vessel (หัว)', [(-22, -22, Rd), (22, -22, Gn), (0, -80, Rd), (0, -102, Gn)], 'ไฟข้าง (+ แดงบนเขียว option)'),
        ('Dredger RAM – obstruction', [(0, -66, Rd), (0, -88, W_), (0, -110, Rd), (-44, -30, Rd), (-44, -52, Rd), (44, -30, Gn), (44, -52, Gn)], 'แดงคู่ = ด้านกีดขวาง เขียวคู่ = ผ่านได้'),
        ('Mine clearance (หัว)', [(0, -104, Gn), (-34, -78, Gn), (34, -78, Gn), (0, -50, W_), (-22, -22, Rd), (22, -22, Gn)], '3 เขียว + ไฟเรือกล — อันตรายภายใน 1000 m'),
        ('Air-cushion (non-displacement)', [(0, -60, W_), (0, -90, 'F' + Yl), (-22, -22, Rd), (22, -22, Gn)], '+ เหลืองกะพริบ all-round'),
        ('Towing ≤ 200 m (มองจากหัว)', [(0, -60, W_), (0, -82, W_), (-22, -22, Rd), (22, -22, Gn)], 'masthead 2 ดวงแนวตั้ง + ไฟข้าง'),
        ('NUC – ไม่มี way (ทุกมุมมอง)', [(0, -60, Rd), (0, -82, Rd)], '2 แดง all-round เท่านั้น ไม่มีไฟข้าง'),
        ('RAM ทอดสมอ (หัวเรือไปทางซ้าย)', [(-50, -56, W_), (50, -32, W_), (0, -60, Rd), (0, -82, W_), (0, -104, Rd)], 'แดง-ขาว-แดง + ไฟทอดสมอ'),
        ('WIG craft ขึ้น/ลง/บินใกล้ผิวน้ำ', [(0, -60, W_), (0, -92, 'F' + Rd), (-22, -22, Rd), (22, -22, Gn)], '+ แดงกะพริบความเข้มสูง all-round'),
    ]
    cols = 4; cw, ch = 240, 210
    rows = math.ceil(len(items) / cols)
    w, h = cols * cw + 20, rows * ch + 120
    s = head(w, h, 'ไฟของเรือประเภทต่าง ๆ ในเวลากลางคืน (Part C) — ภาพสรุปสำหรับท่องจำ')
    for i, (title, lamps, note) in enumerate(items):
        c, r_ = i % cols, i // cols
        x0, y0 = 10 + c * cw, 50 + r_ * ch
        s += f'<rect x="{x0+4}" y="{y0+4}" width="{cw-8}" height="{ch-8}" rx="8" fill="#0b1220"/>\n'
        s += f'<text x="{x0+cw/2}" y="{y0+24}" text-anchor="middle" font-size="12" font-weight="bold" fill="#e2e8f0">{title}</text>\n'
        bx, by = x0 + cw / 2, y0 + 165
        s += f'<path d="M {bx-60} {by} L {bx+60} {by} L {bx+48} {by+14} L {bx-48} {by+14} Z" fill="#1e293b" stroke="#475569"/>\n'
        for dx, dy, col in lamps:
            s += lamp(bx + dx, by + dy, col)
        s += f'<text x="{x0+cw/2}" y="{y0+196}" text-anchor="middle" font-size="11" fill="#cbd5e1">{note}</text>\n'
    yb = 50 + rows * ch + 22
    s += f'<text x="20" y="{yb}" font-size="12" fill="#334155">ภาพเป็นแผนผัง ไม่ตามมาตราส่วน · ดวงที่มีรัศมีเส้นรอบ = ไฟกะพริบ (flashing) · ไฟ all-round ที่วางแนวตั้งห่างกัน ≥ 2 m (เรือ ≥ 20 m) ตาม Annex I §2(i)</text>\n'
    s += f'<text x="20" y="{yb+20}" font-size="12" fill="#334155">เรือขุดลอก: ไฟคู่ด้านข้างต้องไม่สูงกว่าดวงล่างสุดของแดง-ขาว-แดง และห่างออกไปทางข้าง ≥ 2 m (Annex I §4(b))</text>\n'
    s += f'<text x="20" y="{yb+40}" font-size="12" fill="#334155">เรือประมงที่ไม่ใช่อวนลาก: ไฟขาวบอกทิศเครื่องมือห่างจากไฟแดง/ขาว 2–6 m ไม่สูงกว่าไฟขาว all-round และไม่ต่ำกว่าไฟข้าง (Annex I §4(a))</text>\n'
    save('colreg-lights-gallery.svg', s)

def shapes():
    w, h = 1000, 720
    s = head(w, h, 'ทุ่นวัน / รูปทรงสัญญาณกลางวัน (Day shapes) — สีดำ')
    def ball(x, y, r=14): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#111827"/>\n'
    def cone(x, y, up=True, s_=28):
        return (f'<path d="M {x-s_/2} {y+s_/2} L {x+s_/2} {y+s_/2} L {x} {y-s_/2} Z" fill="#111827"/>\n' if up else
                f'<path d="M {x-s_/2} {y-s_/2} L {x+s_/2} {y-s_/2} L {x} {y+s_/2} Z" fill="#111827"/>\n')
    def diamond(x, y, s_=28): return f'<path d="M {x} {y-s_} L {x+s_/2} {y} L {x} {y+s_} L {x-s_/2} {y} Z" fill="#111827"/>\n'
    def cyl(x, y): return f'<rect x="{x-12}" y="{y-24}" width="24" height="48" fill="#111827"/>\n'
    def flag_a(x, y):
        # ธง A ของ ICS: ครึ่งด้านเสา (hoist) สีขาว ครึ่งปลาย (fly) สีน้ำเงิน ปลายเป็นหางแฉก (swallowtail)
        return (f'<line x1="{x-34}" y1="{y-40}" x2="{x-34}" y2="{y+46}" stroke="#334155" stroke-width="3"/>'
                f'<rect x="{x-32}" y="{y-36}" width="32" height="50" fill="#ffffff" stroke="#0f172a"/>'
                f'<path d="M {x} {y-36} L {x+40} {y-36} L {x+24} {y-11} L {x+40} {y+14} L {x} {y+14} Z" fill="#1d4ed8" stroke="#0f172a"/>\n')
    def dredger(x, y):
        # กลม-ข้าวหลามตัด-กลม ตรงกลาง; ลูกกลม 2 = ด้านกีดขวาง, ข้าวหลามตัด 2 = ด้านผ่านได้ (ไม่สูงกว่าทุ่นล่างสุดของชุดกลาง)
        return (ball(x, y - 54, 10) + diamond(x, y - 22, 16) + ball(x, y + 8, 10) +
                ball(x - 58, y + 8, 10) + ball(x - 58, y + 36, 10) +
                diamond(x + 58, y + 8, 12) + diamond(x + 58, y + 36, 12))
    items = [
        ('At anchor', [lambda x, y: ball(x, y)], 'ลูกกลม 1 ลูก (ส่วนหน้าเรือ)'),
        ('NUC', [lambda x, y: ball(x, y - 22), lambda x, y: ball(x, y + 22)], 'ลูกกลม 2 ลูก'),
        ('Aground', [lambda x, y: ball(x, y - 44), lambda x, y: ball(x, y), lambda x, y: ball(x, y + 44)], 'ลูกกลม 3 ลูก'),
        ('RAM', [lambda x, y: ball(x, y - 50), lambda x, y: diamond(x, y), lambda x, y: ball(x, y + 50)], 'กลม-ข้าวหลามตัด-กลม'),
        ('Constrained by draught', [lambda x, y: cyl(x, y)], 'ทรงกระบอก'),
        ('Fishing (any)', [lambda x, y: cone(x, y - 15, False), lambda x, y: cone(x, y + 15, True)], 'กรวย 2 อันยอดชนกัน'),
        ('Fishing gear > 150 m', [lambda x, y: cone(x, y, True)], 'กรวยยอดชี้ขึ้น (ทิศเครื่องมือ)'),
        ('Towing, tow > 200 m', [lambda x, y: diamond(x, y)], 'ข้าวหลามตัด (ทั้งเรือลากและถูกลาก)'),
        ('Motor-sailing', [lambda x, y: cone(x, y, False)], 'กรวยยอดชี้ลง'),
        ('Mine clearance', [lambda x, y: ball(x, y - 36), lambda x, y: ball(x - 46, y + 10), lambda x, y: ball(x + 46, y + 10)], 'ลูกกลม 3 ลูก (ยอด+ปลายพรวน)'),
        ('Dredging มีสิ่งกีดขวาง', [dredger], 'ลูกกลมคู่ = ด้านห้ามผ่าน|ข้าวหลามตัดคู่ = ด้านผ่านได้'),
        ('Diving (เรือเล็ก) 27(e)', [flag_a], 'ธง A แบบแข็ง สูง ≥ 1 m (ไม่ใช่สีดำ)'),
        ('RAM ทอดสมอ 27(b)(iv)', [lambda x, y: ball(x - 50, y - 36), lambda x, y: ball(x + 20, y - 50), lambda x, y: diamond(x + 20, y), lambda x, y: ball(x + 20, y + 50)], 'RAM + ลูกกลมทอดสมอ'),
        ('Towing RAM 27(c)', [lambda x, y: ball(x - 30, y - 50), lambda x, y: diamond(x - 30, y), lambda x, y: ball(x - 30, y + 50), lambda x, y: diamond(x + 40, y)], 'RAM + ข้าวหลามตัด (ถ้าลาก > 200 m)'),
    ]
    cw = 196
    for i, (t, fs, note) in enumerate(items):
        c, r_ = i % 5, i // 5
        x0, y0 = 12 + c * cw, 60 + r_ * 200
        s += f'<rect x="{x0}" y="{y0}" width="{cw-10}" height="186" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>\n'
        s += f'<text x="{x0+(cw-10)/2}" y="{y0+22}" text-anchor="middle" font-size="13" font-weight="bold">{t}</text>\n'
        for f in fs:
            s += f(x0 + (cw - 10) / 2, y0 + 100)
        if '|' in note:
            n1, n2 = note.split('|')
            s += f'<text x="{x0+(cw-10)/2}" y="{y0+164}" text-anchor="middle" font-size="11" fill="#334155">{n1}</text><text x="{x0+(cw-10)/2}" y="{y0+179}" text-anchor="middle" font-size="11" fill="#334155">{n2}</text>\n'
        else:
            s += f'<text x="{x0+(cw-10)/2}" y="{y0+176}" text-anchor="middle" font-size="11" fill="#334155">{note}</text>\n'
    s += '<rect x="796" y="460" width="186" height="186" rx="8" fill="#fff" stroke="#94a3b8" stroke-dasharray="4 3"/>\n'
    s += '<text x="889" y="484" text-anchor="middle" font-size="13" font-weight="bold" fill="#0f172a">ขนาดจริง (Annex I §6)</text>\n'
    for k, t in enumerate(['ลูกกลม Ø ≥ 0.6 m', 'กรวย ฐาน ≥ 0.6 m สูง = ฐาน', 'ทรงกระบอก Ø ≥ 0.6 m สูง 2Ø', 'ข้าวหลามตัด = กรวยคู่ฐานชนกัน', 'ระยะห่างแนวตั้ง ≥ 1.5 m', 'เรือ &lt; 20 m ย่อขนาดได้ตามสัดส่วน']):
        s += f'<text x="804" y="{512 + k*22}" font-size="11" fill="#334155">• {t}</text>\n'
    s += '<text x="20" y="700" font-size="12" fill="#334155">ภาพไม่ตามมาตราส่วน (ระยะห่างจริงระหว่างทุ่นวัน ≥ 1.5 m ห่างกว่าในภาพมาก) · ทุ่นวันทุกแบบเป็นสีดำ ยกเว้นธง A ของงานดำน้ำ</text>\n'
    save('colreg-day-shapes.svg', s)

def sound_signals():
    # S = short (~1 s), L = prolonged (4–6 s), B = รัวระฆัง ~5 s, G = รัวฆ้อง ~5 s, b = ตีระฆัง 1 ครั้ง
    rows = [
        ('1 short', 'S', 'กำลังเปลี่ยนเข็มไปทางขวา (เห็นกัน)', 'Rule 34(a)'),
        ('2 short', 'SS', 'กำลังเปลี่ยนเข็มไปทางซ้าย (เห็นกัน)', 'Rule 34(a)'),
        ('3 short', 'SSS', 'กำลังใช้เครื่องถอยหลัง', 'Rule 34(a)'),
        ('5 short (อย่างน้อย)', 'SSSSS', 'สงสัยเจตนา/การกระทำของอีกลำ', 'Rule 34(d)'),
        ('2 long + 1 short', 'LLS', 'จะแซงทางกราบขวาของท่าน (ร่องน้ำแคบ)', 'Rule 34(c)'),
        ('2 long + 2 short', 'LLSS', 'จะแซงทางกราบซ้ายของท่าน', 'Rule 34(c)'),
        ('L S L S', 'LSLS', 'ตกลงให้แซง (เรือที่ถูกแซง)', 'Rule 34(c)'),
        ('1 long', 'L', 'เข้าใกล้โค้ง/บริเวณที่บังสายตา (ฝ่ายที่ได้ยินตอบ 1 long)', 'Rule 34(e)'),
        ('1 long ≤ 2 นาที', 'L', 'Power-driven making way (ทัศนวิสัยจำกัด)', 'Rule 35(a)'),
        ('2 long ≤ 2 นาที', 'LL', 'Power-driven underway not making way (ห่าง ~2 วินาที)', 'Rule 35(b)'),
        ('1 long + 2 short', 'LSS', 'NUC, RAM, CBD, sailing, fishing, towing/pushing', 'Rule 35(c)'),
        ('1 long + 2 short', 'LSS', 'เรือประมงทอดสมอ / RAM ทอดสมอทำงาน (แทนระฆัง)', 'Rule 35(d)'),
        ('1 long + 3 short', 'LSSS', 'เรือที่ถูกลาก (ลำท้ายสุดที่มีคน)', 'Rule 35(e)'),
        ('4 short', 'SSSS', 'Pilot vessel identity (เพิ่มเติม)', 'Rule 35(k)'),
        ('ทอดสมอ ≤ 1 นาที', 'B', 'รัวระฆังส่วนหน้าเรือ ~5 วินาที', 'Rule 35(g)'),
        ('ทอดสมอ ≥ 100 m', 'BG', 'รัวระฆังหัวเรือ แล้วรัวฆ้องท้ายเรือทันที ~5 วินาที', 'Rule 35(g)'),
        ('S L S (option)', 'SLS', 'เรือทอดสมอเตือนเรือที่เข้าใกล้', 'Rule 35(g)'),
        ('เกยตื้น ≤ 1 นาที', 'bbbBbbb', 'ตีระฆัง 3 ครั้ง + รัวระฆัง + ตีระฆัง 3 ครั้ง (+ฆ้องถ้า ≥100 m)', 'Rule 35(h)'),
    ]
    COL = {'S': '#111827', 'L': '#111827', 'B': '#b45309', 'G': '#7c3aed', 'b': '#b45309'}
    WID = {'S': 14, 'L': 56, 'B': 56, 'G': 56, 'b': 8}
    w = 1000; rh = 34; h = 80 + rh * len(rows) + 90
    s = head(w, h, 'สัญญาณเสียง (Rules 34–35) — short ≈ 1 วินาที, prolonged 4–6 วินาที')
    for i, (name, code, meaning, rule) in enumerate(rows):
        y = 60 + i * rh
        s += f'<rect x="10" y="{y}" width="{w-20}" height="{rh-4}" fill="{"#f8fafc" if i % 2 else "#fff"}"/>\n'
        s += f'<text x="20" y="{y+21}" font-size="14" font-weight="bold" fill="#1e3a8a">{name}</text>\n'
        x = 220
        for ch_ in code:
            ww = WID[ch_]
            if ch_ == 'b':
                s += f'<circle cx="{x+4}" cy="{y+15}" r="5" fill="{COL[ch_]}"/>\n'
            elif ch_ in 'BG':
                s += f'<rect x="{x}" y="{y+8}" width="{ww}" height="14" rx="3" fill="{COL[ch_]}"/>\n'
                for k in range(1, 7):
                    s += f'<line x1="{x+k*8}" y1="{y+9}" x2="{x+k*8}" y2="{y+21}" stroke="#fff" stroke-width="1.5"/>'
                s += f'<text x="{x+ww/2}" y="{y+6}" text-anchor="middle" font-size="9" fill="{COL[ch_]}">{"ระฆัง" if ch_ == "B" else "ฆ้อง"}</text>\n'
            else:
                s += f'<rect x="{x}" y="{y+8}" width="{ww}" height="14" rx="3" fill="{COL[ch_]}"/>\n'
            x += ww + 8
        s += f'<text x="470" y="{y+21}" font-size="13">{meaning}</text><text x="900" y="{y+21}" font-size="12" fill="#64748b">{rule}</text>\n'
    yb = 60 + len(rows) * rh + 20
    s += f'<rect x="20" y="{yb-10}" width="14" height="10" rx="2" fill="#111827"/><text x="40" y="{yb}" font-size="12" fill="#334155">หวูด (whistle)</text>'
    s += f'<rect x="150" y="{yb-10}" width="24" height="10" rx="2" fill="#b45309"/><text x="180" y="{yb}" font-size="12" fill="#334155">รัวระฆัง (bell)</text>'
    s += f'<circle cx="300" cy="{yb-5}" r="5" fill="#b45309"/><text x="310" y="{yb}" font-size="12" fill="#334155">ตีระฆัง 1 ครั้ง (stroke)</text>'
    s += f'<rect x="450" y="{yb-10}" width="24" height="10" rx="2" fill="#7c3aed"/><text x="480" y="{yb}" font-size="12" fill="#334155">รัวฆ้อง (gong)</text>\n'
    s += f'<text x="20" y="{yb+22}" font-size="12" fill="#334155">Rule 34(a)–(c) ใช้เฉพาะเมื่อมองเห็นกัน · Rule 35 ใช้ในหรือใกล้บริเวณทัศนวิสัยจำกัด ทั้งกลางวันและกลางคืน · เรือ 12–&lt;20 m และ &lt;12 m ใช้เสียงอื่นที่มีประสิทธิภาพแทนได้ (35(i),(j))</text>\n'
    s += f'<text x="20" y="{yb+42}" font-size="12" fill="#334155">ไฟประกอบ Rule 34(b): ไฟขาว all-round เห็นได้ ≥ 5 ไมล์ แวบละ ~1 วินาที เว้น ~1 วินาที และระหว่างชุดสัญญาณ ≥ 10 วินาที · ความยาวแถบในภาพเป็นสัดส่วนโดยประมาณ</text>\n'
    save('colreg-sound-signals.svg', s)

def rule19():
    w, h = 900, 600
    s = head(w, h, 'Rule 19(d) — การหลบเมื่อทัศนวิสัยจำกัด (ตรวจพบด้วยเรดาร์อย่างเดียว)')
    cx, cy, r = 330, 330, 240
    s += sector(cx, cy, r, -90, 0, Rd, 0.30)
    s += sector(cx, cy, r, 0, 90, '#f59e0b', 0.30)
    s += sector(cx, cy, r, 90, 270, '#3b82f6', 0.22)
    s += ship_top(cx, cy, 70, 20)
    s += f'<text x="{cx-220}" y="{cy-120}" font-size="14" font-weight="bold" fill="#b91c1c">เป้าอยู่หน้าแนวกราบ (ซ้าย)</text><text x="{cx-220}" y="{cy-100}" font-size="13" fill="#b91c1c">หลีกเลี่ยงการเปลี่ยนเข็มไปทางซ้าย</text><text x="{cx-220}" y="{cy-82}" font-size="13" fill="#b91c1c">→ เปลี่ยนไปทางขวา</text>\n'
    s += f'<text x="{cx+40}" y="{cy-120}" font-size="14" font-weight="bold" fill="#b45309">เป้าอยู่หน้าแนวกราบ (ขวา)</text><text x="{cx+40}" y="{cy-100}" font-size="13" fill="#b45309">หลีกเลี่ยงการเปลี่ยนเข็มไปทางซ้าย</text><text x="{cx+40}" y="{cy-82}" font-size="13" fill="#b45309">→ เปลี่ยนไปทางขวา (หรือลดความเร็ว)</text>\n'
    s += f'<text x="{cx-200}" y="{cy+140}" font-size="14" font-weight="bold" fill="#1d4ed8">เป้าอยู่ตรงกราบหรือหลังแนวกราบ</text><text x="{cx-200}" y="{cy+160}" font-size="13" fill="#1d4ed8">หลีกเลี่ยงการเปลี่ยนเข็ม "เข้าหา" เป้า</text><text x="{cx-200}" y="{cy+178}" font-size="13" fill="#1d4ed8">(เป้ากราบขวา → อย่าหันขวา, เป้ากราบซ้าย → อย่าหันซ้าย)</text>\n'
    s += '<rect x="610" y="70" width="280" height="366" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    rows = ['ข้อยกเว้นข้อ (i): ถ้าเป้าข้างหน้า', 'กำลังถูกเราแซง ไม่บังคับข้อนี้', '', 'Rule 19(e): ได้ยินสัญญาณหมอก', 'ทางหน้าแนวกราบ หรือหลีกเลี่ยง', 'close-quarters ไม่ได้', '→ ลดความเร็วต่ำสุดที่ยังถือท้ายได้', '→ ถ้าจำเป็นหยุดเรือ (take all way off)', '→ เดินเรือด้วยความระมัดระวังสูงสุด', '', 'ไม่มี stand-on / give-way ใน Rule 19', 'ทุกลำต้องหลบ', '', 'กฎใช้คำว่า "shall be avoided"', '(ให้หลีกเลี่ยงเท่าที่ทำได้)']
    for i, t in enumerate(rows):
        s += f'<text x="624" y="{96 + i*23}" font-size="13">{t}</text>\n'
    save('colreg-rule19.svg', s)

def tss():
    w, h = 960, 520
    s = head(w, h, 'Traffic Separation Scheme (Rule 10) — แผนผังจำลอง')
    s += '<rect x="40" y="120" width="880" height="80" fill="#e0f2fe" stroke="#0284c7"/>\n'
    s += '<rect x="40" y="200" width="880" height="40" fill="#f9a8d4" opacity="0.6" stroke="#be185d"/>\n'
    s += '<rect x="40" y="240" width="880" height="80" fill="#e0f2fe" stroke="#0284c7"/>\n'
    s += '<rect x="40" y="60" width="880" height="60" fill="#fef9c3" stroke="#ca8a04" stroke-dasharray="6 4"/>\n'
    s += '<text x="60" y="95" font-size="14" font-weight="bold" fill="#854d0e">Inshore Traffic Zone (ITZ) — เรือ &lt;20 m, เรือใบ, เรือประมง, เรือเข้า-ออกท่าในเขตนี้</text>\n'
    # ทิศเหนืออยู่ด้านบน: lane เหนือไปทางตะวันตก lane ใต้ไปทางตะวันออก (เรือแล่นชิดขวาของ scheme, separation zone อยู่ทางซ้ายของเรือ)
    for x in range(120, 900, 160):
        s += f'<path d="M {x+60} 160 L {x} 160" stroke="#0369a1" stroke-width="4" marker-end="url(#ar)"/>\n'
        s += f'<path d="M {x} 280 L {x+60} 280" stroke="#0369a1" stroke-width="4" marker-end="url(#ar)"/>\n'
    s += '<text x="60" y="140" font-size="13" fill="#0369a1" font-weight="bold">Traffic lane (มุ่งตะวันตก ←)</text>\n'
    s += '<text x="60" y="310" font-size="13" fill="#0369a1" font-weight="bold">Traffic lane (มุ่งตะวันออก →)</text>\n'
    s += '<text x="480" y="226" text-anchor="middle" font-size="13" fill="#831843" font-weight="bold">Separation zone — โดยปกติห้ามเข้า ยกเว้นตาม Rule 10(e)</text>\n'
    s += '<path d="M 905 48 L 905 22" stroke="#0f172a" stroke-width="2" marker-end="url(#ar)"/><text x="918" y="44" font-size="13" font-weight="bold">N</text>\n'
    # crossing vessel
    s += '<path d="M 720 470 L 720 52" stroke="#16a34a" stroke-width="3" stroke-dasharray="8 5" marker-end="url(#ar)"/>\n'
    s += '<text x="710" y="400" text-anchor="end" font-size="13" fill="#15803d" font-weight="bold">ข้าม TSS: หัวเรือตั้งฉากกับทิศจราจร</text><text x="710" y="418" text-anchor="end" font-size="13" fill="#15803d">(heading at right angles) 10(c)</text>\n'
    # joining at small angle (เข้าทางด้านข้างด้วยมุมเล็ก ไปในทิศเดียวกับ lane)
    s += '<path d="M 80 380 Q 200 330 300 285" stroke="#7c3aed" stroke-width="3" fill="none" marker-end="url(#ar)"/>\n'
    s += '<text x="60" y="400" font-size="13" fill="#6d28d9" font-weight="bold">เข้า/ออก lane ที่ปลาย หรือทางด้านข้าง</text><text x="60" y="418" font-size="13" fill="#6d28d9" font-weight="bold">ด้วยมุมเล็กที่สุด 10(b)(iii)</text>\n'
    s += '<rect x="40" y="430" width="560" height="70" rx="8" fill="#f8fafc" stroke="#94a3b8"/>\n'
    s += '<text x="52" y="452" font-size="12">• ไปตามทิศจราจรทั่วไปของ lane · อยู่ห่างเส้น/เขตแบ่ง · หลีกเลี่ยงการทอดสมอใน TSS/ปลาย TSS</text>\n'
    s += '<text x="52" y="472" font-size="12">• เรือ &lt;20 m, เรือใบ, เรือประมง ต้องไม่ขัดขวาง (not impede) เรือที่ใช้ lane</text>\n'
    s += '<text x="52" y="492" font-size="12">• TSS ไม่ได้ยกเลิกกฎอื่น — Rule 13–17 ยังใช้ระหว่างเรือใน lane</text>\n'
    save('colreg-tss.svg', s)

def hierarchy():
    w, h = 820, 580
    s = head(w, h, 'Rule 18 — ลำดับความรับผิดชอบระหว่างเรือ (ขณะเห็นกัน)')
    levels = [('NUC  |  RAM — ระดับเดียวกัน (กฎไม่ได้กำหนดให้ลำใดหลีกลำใด)', '#991b1b'),
              ('CBD — ทุกลำยกเว้น NUC/RAM ต้องไม่ขัดขวาง (18(d))', '#c2410c'),
              ('Fishing vessel (engaged in fishing)', '#ca8a04'),
              ('Sailing vessel', '#15803d'),
              ('Power-driven vessel (รวม WIG ที่แล่นบนผิวน้ำ)', '#1d4ed8'),
              ('Seaplane บนน้ำ / WIG ขณะขึ้น-ลง-บินใกล้ผิวน้ำ', '#475569')]
    for i, (t, c) in enumerate(levels):
        wid = 440 + i * 54
        x = (w - wid) / 2; y = 60 + i * 66
        s += f'<rect x="{x}" y="{y}" width="{wid}" height="52" rx="8" fill="{c}"/>\n'
        s += f'<text x="{w/2}" y="{y+32}" text-anchor="middle" font-size="15" font-weight="bold" fill="#fff">{t}</text>\n'
    s += '<path d="M 26 440 L 26 70" stroke="#0f172a" stroke-width="3" marker-end="url(#ar)"/>\n'
    s += '<text x="20" y="480" font-size="12">เรือล่างหลีกทาง (keep out of the way) เรือที่อยู่สูงกว่า · CBD: เรืออื่นต้อง "ไม่ขัดขวาง" (not impede) และ CBD เองต้องเดินเรือด้วยความระมัดระวังเป็นพิเศษ</text>\n'
    s += '<text x="20" y="500" font-size="12">Seaplane บนน้ำต้องหลีกห่างทุกลำ (18(e)) · WIG ขณะขึ้น-ลง-บินใกล้ผิวน้ำต้องหลีกห่างทุกลำ แต่ถ้าแล่นบนผิวน้ำถือเป็นเรือกล (18(f))</text>\n'
    s += '<text x="20" y="520" font-size="12" font-weight="bold" fill="#b91c1c">ข้อยกเว้น: ลำดับนี้ใช้ "ยกเว้นที่ Rule 9, 10 และ 13 กำหนดไว้เป็นอย่างอื่น" — เช่น เรือที่กำลังแซงต้องหลบเสมอ ไม่ว่าเป็นเรือประเภทใด</text>\n'
    s += '<text x="20" y="540" font-size="12">เรือประมง/เรือใบ/เรือ &lt; 20 m ต้องไม่ขัดขวางเรือที่แล่นได้เฉพาะในร่องน้ำแคบหรือเรือใน traffic lane (9(b)(c), 10(i)(j))</text>\n'
    save('colreg-hierarchy.svg', s)

def annex1_positioning():
    """Annex I §2–3: ตำแหน่งไฟของเรือกล ≥ 50 m (ภาพด้านข้าง หัวเรือไปทางขวา เห็นกราบขวา) — มาตราส่วนแนวตั้งโดยประมาณ 1 m ≈ 12 px"""
    w, h = 980, 600
    s = head(w, h, 'Annex I — ตำแหน่งไฟของเรือกล ≥ 50 m (มองด้านข้าง หัวเรือไปทางขวา)')
    HALO = 'stroke="#fff" stroke-width="4" paint-order="stroke"'
    deck, wl = 360, 400
    stern, stem = 80, 820
    # ทะเลและตัวเรือ
    s += f'<rect x="20" y="{wl}" width="{w-40}" height="40" fill="#dbeafe"/>\n'
    s += f'<path d="M {stern} {deck} L {stem-40} {deck} L {stem+20} {deck-14} L {stem-30} {wl+20} L {stern+20} {wl+20} L {stern} {deck} Z" fill="#475569" stroke="#0f172a"/>\n'
    # สะพานเดินเรือ (ส่วนกลางค่อนหน้า) และเสา
    s += f'<rect x="520" y="{deck-104}" width="80" height="104" fill="#94a3b8" stroke="#0f172a"/>\n'
    fx, ax = 700, 320          # เสาหน้า / เสาหลัง
    fh, ah = deck - 144, deck - 204   # masthead หน้า 12 m, หลัง 17 m เหนือ hull
    s += f'<line x1="{fx}" y1="{deck}" x2="{fx}" y2="{fh-8}" stroke="#0f172a" stroke-width="4"/>\n'
    s += f'<line x1="{ax}" y1="{deck}" x2="{ax}" y2="{ah-8}" stroke="#0f172a" stroke-width="4"/>\n'
    s += f'<line x1="{stem}" y1="{deck-14}" x2="{stem}" y2="{deck-86}" stroke="#0f172a" stroke-width="3"/>\n'
    s += f'<line x1="{stern+16}" y1="{deck}" x2="{stern+16}" y2="{deck-30}" stroke="#0f172a" stroke-width="3"/>\n'
    def lt(x, y, col):
        return f'<circle cx="{x}" cy="{y}" r="8" fill="{col}" stroke="#0f172a" stroke-width="1.5"/>\n'
    s += lt(fx, fh, '#ffffff') + lt(ax, ah, '#ffffff')
    s += lt(600, deck - 96, Gn)                      # sidelight กราบขวา ที่ปีกสะพาน (8 m)
    s += lt(stem, deck - 86, '#f1f5f9') + lt(stern + 16, deck - 30, '#f1f5f9')   # anchor lights (แสดงเพื่อบอกตำแหน่ง)
    s += lt(stern + 4, deck - 6, '#ffffff')          # sternlight
    # มิติ
    def vdim(x, y1, y2, txt, anchor='start', dx=8):
        return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#b91c1c" stroke-width="1.5" marker-end="url(#dm)" marker-start="url(#dm)"/>'
                f'<text x="{x+dx}" y="{(y1+y2)/2+4}" text-anchor="{anchor}" font-size="12" fill="#b91c1c" {HALO}>{txt}</text>\n')
    s += vdim(fx + 22, deck, fh + 9, 'h₁ ≥ 6 m และ ≥ B (ไม่ต้องเกิน 12 m)')
    s += f'<line x1="{ax}" y1="{fh}" x2="{fx}" y2="{fh}" stroke="#94a3b8" stroke-dasharray="4 3"/>\n'
    s += vdim(ax - 22, fh, ah + 9, 'ดวงหลังสูงกว่า ≥ 4.5 m', 'end', -8)
    s += vdim(614, deck, deck - 87, 'sidelight ≤ ¾ h₁')
    s += f'<line x1="{ax}" y1="{wl+44}" x2="{fx}" y2="{wl+44}" stroke="#1d4ed8" stroke-width="1.5" marker-end="url(#dm)" marker-start="url(#dm)"/><text x="{(ax+fx)/2}" y="{wl+62}" text-anchor="middle" font-size="12" fill="#1d4ed8">ระยะแนวนอน ≥ L/2 (ไม่ต้องเกิน 100 m)</text>\n'
    s += f'<line x1="{fx}" y1="{wl+80}" x2="{stem+20}" y2="{wl+80}" stroke="#1d4ed8" stroke-width="1.5" marker-end="url(#dm)" marker-start="url(#dm)"/><text x="{(fx+stem)/2+10}" y="{wl+98}" text-anchor="middle" font-size="12" fill="#1d4ed8">≤ L/4 จาก stem</text>\n'
    for x in (ax, fx):
        s += f'<line x1="{x}" y1="{deck}" x2="{x}" y2="{wl+86}" stroke="#94a3b8" stroke-dasharray="3 3"/>\n'
    s += f'<line x1="{stem+20}" y1="{deck-14}" x2="{stem+20}" y2="{wl+86}" stroke="#94a3b8" stroke-dasharray="3 3"/>\n'
    # ป้ายไฟ
    s += f'<text x="{fx+12}" y="{fh-12}" font-size="12" font-weight="bold" {HALO}>masthead หน้า</text>\n'
    s += f'<text x="{ax+12}" y="{ah-6}" font-size="12" font-weight="bold" {HALO}>masthead หลัง</text>\n'
    s += f'<text x="612" y="{deck-112}" font-size="12" font-weight="bold" fill="#15803d" {HALO}>sidelight (ไม่อยู่หน้า masthead หน้า)</text>\n'
    s += f'<text x="{stem-6}" y="{deck-100}" text-anchor="middle" font-size="12" {HALO}>anchor หน้า ≥ 6 m</text>\n'
    s += f'<text x="{stern+4}" y="{deck-44}" font-size="12" {HALO}>anchor ท้าย (ต่ำกว่าหน้า ≥ 4.5 m)</text>\n'
    s += f'<text x="{stern-2}" y="{deck+22}" text-anchor="end" font-size="11" fill="#0f172a">sternlight</text>\n'
    s += f'<text x="{stern+140}" y="{deck+26}" font-size="12" fill="#f8fafc">ดาดฟ้าต่อเนื่องบนสุด (uppermost continuous deck) = ระดับ "hull" ที่ใช้วัดความสูงไฟ (§1)</text>\n'
    # กล่องสรุป
    bx = 640
    s += f'<rect x="20" y="520" width="{w-40}" height="70" rx="8" fill="#f8fafc" stroke="#94a3b8"/>\n'
    notes = ['• แยกแนวตั้งของ masthead ให้มากพอที่เมื่อมองจากระดับน้ำทะเลห่าง 1,000 m หน้าหัวเรือ จะเห็นดวงหลังอยู่เหนือและแยกจากดวงหน้าทุกสภาพ trim ปกติ (§2(b))',
             '• ไฟ all-round หลายดวงแนวตั้ง: เรือ ≥ 20 m ห่าง ≥ 2 m ดวงล่าง ≥ 4 m เหนือ hull · เรือ &lt; 20 m ห่าง ≥ 1 m ดวงล่าง ≥ 2 m เหนือ gunwale · 3 ดวงเว้นระยะเท่ากัน (§2(i))',
             '• ภาพเป็นแผนผัง: ตัวเลขในภาพคือค่าขั้นต่ำ/สูงสุดของ Annex I — ไฟทอดสมอกับไฟเดินเรือแสดงพร้อมกันเพื่อบอกตำแหน่งเท่านั้น (ของจริงไม่เปิดพร้อมกัน)']
    for i, t in enumerate(notes):
        s += f'<text x="32" y="{540 + i*20}" font-size="11.5" fill="#334155">{t}</text>\n'
    save('colreg-annex1-positioning.svg', s)

def annex2_fishing():
    """Annex II — สัญญาณเพิ่มเติมของเรือประมงที่ทำการประมงใกล้กัน"""
    w, h = 1000, 420
    s = head(w, h, 'Annex II — สัญญาณเพิ่มเติมของเรือประมงที่ทำการประมงใกล้กัน')
    panels = [
        ('อวนลาก: ปล่อยอวน', 'shooting nets', [(Gn, W_), (W_, W_)], 'ขาวบนขาว'),
        ('อวนลาก: กู้อวน', 'hauling nets', [(Gn, W_), (W_, Rd)], 'ขาวบนแดง'),
        ('อวนลาก: อวนติดสิ่งกีดขวาง', 'net fast on obstruction', [(Gn, W_), (Rd, Rd)], 'แดงบนแดง'),
        ('อวนล้อม (purse seine)', 'hampered by gear', [(Rd, W_), ('F' + Yl, '#713f12')], 'เหลือง 2 ดวงกะพริบสลับ'),
    ]
    cw = 240
    for i, (t, t2, pairs, note) in enumerate(panels):
        x0, y0 = 24 + i * cw, 50
        s += f'<rect x="{x0}" y="{y0}" width="{cw-8}" height="290" rx="8" fill="#0b1220"/>\n'
        s += f'<text x="{x0+(cw-8)/2}" y="{y0+24}" text-anchor="middle" font-size="13" font-weight="bold" fill="#e2e8f0">{t}</text>\n'
        s += f'<text x="{x0+(cw-8)/2}" y="{y0+42}" text-anchor="middle" font-size="11" fill="#94a3b8">({t2})</text>\n'
        cx = x0 + (cw - 8) / 2 - 20
        (u1, l1), (u2, l2) = pairs
        s += lamp(cx, y0 + 80, u1) + lamp(cx, y0 + 110, l1)
        s += lamp(cx, y0 + 170, u2) + lamp(cx, y0 + 196, l2)
        s += f'<path d="M {cx+26} {y0+72} L {cx+32} {y0+72} L {cx+32} {y0+118} L {cx+26} {y0+118}" fill="none" stroke="#cbd5e1"/><text x="{cx+38}" y="{y0+99}" font-size="11" fill="#cbd5e1">Rule 26</text>\n'
        s += f'<path d="M {cx+26} {y0+162} L {cx+32} {y0+162} L {cx+32} {y0+204} L {cx+26} {y0+204}" fill="none" stroke="#facc15"/><text x="{cx+38}" y="{y0+187}" font-size="11" fill="#facc15">Annex II</text>\n'
        s += f'<path d="M {x0+(cw-8)/2-60} {y0+236} L {x0+(cw-8)/2+60} {y0+236} L {x0+(cw-8)/2+48} {y0+250} L {x0+(cw-8)/2-48} {y0+250} Z" fill="#1e293b" stroke="#475569"/>\n'
        s += f'<text x="{x0+(cw-8)/2}" y="{y0+276}" text-anchor="middle" font-size="12" fill="#e2e8f0">{note}</text>\n'
    s += '<text x="24" y="362" font-size="12" fill="#334155">ไฟ Annex II อยู่ต่ำกว่าไฟ Rule 26(b)(i)/(c)(i) ห่างกัน ≥ 0.9 m มองเห็นรอบตัว ≥ 1 ไมล์ แต่ระยะน้อยกว่าไฟเรือประมงตามกฎหลัก</text>\n'
    s += '<text x="24" y="382" font-size="12" fill="#334155">อวนลาก (ทั้ง demersal และ pelagic) ยาว ≥ 20 m ต้องแสดง · &lt; 20 m อาจแสดง · อวนล้อมอาจแสดง (may) เฉพาะเมื่อถูกเครื่องมือประมงขัดขวาง · เหลืองดวงทึบในภาพ = จังหวะที่ดับ</text>\n'
    s += '<text x="24" y="402" font-size="12" fill="#334155">ลากคู่ (pair trawling): กลางคืนแต่ละลำส่องไฟฉายไปข้างหน้าและไปทางอีกลำของคู่ และเมื่อปล่อย/กู้อวน/อวนติด ให้แสดงไฟตามสามกรอบแรกด้วย</text>\n'
    save('colreg-annex2-fishing.svg', s)

if __name__ == '__main__':
    light_arcs(); situations(); lights_gallery(); shapes(); sound_signals(); rule19(); tss(); hierarchy()
    annex1_positioning(); annex2_fishing()
    print('ok')
