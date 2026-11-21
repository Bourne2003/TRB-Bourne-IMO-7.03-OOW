"""สคริปต์สร้างภาพทุ่นระบบ IALA และลักษณะไฟ"""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
_ids = iter(range(1, 100000))
RED, GREEN, YEL, BLK, WHT, BLU = '#dc2626', '#16a34a', '#facc15', '#111827', '#ffffff', '#1d4ed8'

def head(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{title}</text>\n')

def water(x, y, w=120):
    return f'<path d="M {x-w/2} {y} q 10 -6 20 0 t 20 0 t 20 0 t 20 0 t 20 0 t 20 0" fill="none" stroke="#0284c7" stroke-width="2"/>\n'

def body(x, y, bands, shape='pillar', w=46, h=110):
    """bands: list of (color, fraction) from top to bottom; returns svg and top y"""
    s = ''
    top = y - h
    if shape == 'pillar':
        # trapezoid body
        tw = w * 0.55
        clip = f'M {x-tw/2} {top} L {x+tw/2} {top} L {x+w/2} {y} L {x-w/2} {y} Z'
    elif shape == 'can':
        clip = f'M {x-w/2} {y-h*0.62} L {x+w/2} {y-h*0.62} L {x+w/2} {y} L {x-w/2} {y} Z'; top = y - h * 0.62
    elif shape == 'cone':
        clip = f'M {x} {y-h*0.75} L {x+w/2} {y} L {x-w/2} {y} Z'; top = y - h * 0.75
    elif shape == 'sphere':
        clip = None; top = y - w
    cid = f'c{next(_ids)}'
    if clip:
        s += f'<clipPath id="{cid}"><path d="{clip}"/></clipPath>\n'
        yy = top; total = y - top
        for col, frac in bands:
            hh = total * frac
            s += f'<rect x="{x-w/2-2}" y="{yy:.1f}" width="{w+4}" height="{hh+0.6:.1f}" fill="{col}" clip-path="url(#{cid})"/>\n'
            yy += hh
        s += f'<path d="{clip}" fill="none" stroke="#111827" stroke-width="1.5"/>\n'
    else:
        r = w / 2
        s += f'<clipPath id="{cid}"><circle cx="{x}" cy="{y-r}" r="{r}"/></clipPath>\n'
        # vertical stripes for safe water
        n = len(bands)
        for i, (col, frac) in enumerate(bands):
            s += f'<rect x="{x-r+i*w/n:.1f}" y="{y-w}" width="{w/n+0.6:.1f}" height="{w}" fill="{col}" clip-path="url(#{cid})"/>\n'
        s += f'<circle cx="{x}" cy="{y-r}" r="{r}" fill="none" stroke="#111827" stroke-width="1.5"/>\n'
    return s, top

def vstripes(x, y, cols, w=46, h=110):
    tw = w * 0.55; top = y - h
    cid = f'v{next(_ids)}'
    s = f'<clipPath id="{cid}"><path d="M {x-tw/2} {top} L {x+tw/2} {top} L {x+w/2} {y} L {x-w/2} {y} Z"/></clipPath>\n'
    n = len(cols)
    for i, c in enumerate(cols):
        s += f'<rect x="{x-w/2+i*w/n:.1f}" y="{top}" width="{w/n+0.6:.1f}" height="{h}" fill="{c}" clip-path="url(#{cid})"/>\n'
    s += f'<path d="M {x-tw/2} {top} L {x+tw/2} {top} L {x+w/2} {y} L {x-w/2} {y} Z" fill="none" stroke="#111827" stroke-width="1.5"/>\n'
    return s, top

def mast(x, top, L=26):
    return f'<line x1="{x}" y1="{top}" x2="{x}" y2="{top-L}" stroke="#111827" stroke-width="3"/>\n', top - L

def cone(x, yb, up=True, col=BLK, size=16):
    if up:
        return f'<path d="M {x-size/2} {yb} L {x+size/2} {yb} L {x} {yb-size} Z" fill="{col}" stroke="#111827"/>\n'
    return f'<path d="M {x-size/2} {yb-size} L {x+size/2} {yb-size} L {x} {yb} Z" fill="{col}" stroke="#111827"/>\n'

def topmark(kind, x, y):
    s = ''
    if kind == 'N': s += cone(x, y - 20, True) + cone(x, y, True)
    elif kind == 'S': s += cone(x, y - 20, False) + cone(x, y, False)
    elif kind == 'E': s += cone(x, y - 18, True) + cone(x, y, False)
    elif kind == 'W': s += cone(x, y - 20, False) + cone(x, y - 2, True)
    elif kind == 'can_r': s += f'<rect x="{x-8}" y="{y-16}" width="16" height="16" fill="{RED}" stroke="#111827"/>\n'
    elif kind == 'can_g': s += f'<rect x="{x-8}" y="{y-16}" width="16" height="16" fill="{GREEN}" stroke="#111827"/>\n'
    elif kind == 'cone_g': s += cone(x, y, True, GREEN)
    elif kind == 'cone_r': s += cone(x, y, True, RED)
    elif kind == '2sph': s += f'<circle cx="{x}" cy="{y-8}" r="8" fill="{BLK}"/><circle cx="{x}" cy="{y-26}" r="8" fill="{BLK}"/>\n'
    elif kind == 'sph_r': s += f'<circle cx="{x}" cy="{y-9}" r="9" fill="{RED}" stroke="#111827"/>\n'
    elif kind == 'X': s += f'<path d="M {x-9} {y-18} L {x+9} {y} M {x+9} {y-18} L {x-9} {y}" stroke="{YEL}" stroke-width="5"/><path d="M {x-9} {y-18} L {x+9} {y} M {x+9} {y-18} L {x-9} {y}" stroke="#111827" stroke-width="1" fill="none"/>\n'
    elif kind == 'cross': s += f'<path d="M {x} {y-22} L {x} {y} M {x-10} {y-11} L {x+10} {y-11}" stroke="{YEL}" stroke-width="5"/>\n'
    return s

def label(x, y, lines, col='#0f172a', size=13, bold_first=True):
    s = ''
    for i, t in enumerate(lines):
        fw = ' font-weight="bold"' if (i == 0 and bold_first) else ''
        s += f'<text x="{x}" y="{y + i*17}" text-anchor="middle" font-size="{size if i else size+1}" fill="{col}"{fw}>{t}</text>\n'
    return s

def lateral():
    w, h = 1000, 640
    s = head(w, h, 'IALA Lateral Marks — Region A และ Region B')
    s += '<text x="250" y="66" text-anchor="middle" font-size="17" font-weight="bold" fill="#b91c1c">REGION A (รวมประเทศไทย)</text>\n'
    s += '<text x="750" y="66" text-anchor="middle" font-size="17" font-weight="bold" fill="#15803d">REGION B (อเมริกา ญี่ปุ่น เกาหลี ฟิลิปปินส์)</text>\n'
    s += '<line x1="500" y1="50" x2="500" y2="620" stroke="#cbd5e1" stroke-width="2"/>\n'
    def mark(x, y, cols, shape, tm, lines):
        out = water(x, y + 4)
        b, top = body(x, y, cols, shape)
        out += b
        m, mt = mast(x, top, 22)
        out += m + topmark(tm, x, mt)
        out += label(x, y + 30, lines)
        return out
    # Region A
    s += mark(120, 270, [(RED, 1)], 'can', 'can_r', ['Port hand', 'สีแดง ทรงกระบอก (can)', 'ไฟแดง (ยกเว้น Fl(2+1))'])
    s += mark(370, 270, [(GREEN, 1)], 'cone', 'cone_g', ['Starboard hand', 'สีเขียว ทรงกรวย (cone)', 'ไฟเขียว (ยกเว้น Fl(2+1))'])
    s += mark(120, 520, [(RED, .35), (GREEN, .3), (RED, .35)], 'can', 'can_r', ['Preferred channel', 'to STARBOARD', 'Fl(2+1)R'])
    s += mark(370, 520, [(GREEN, .35), (RED, .3), (GREEN, .35)], 'cone', 'cone_g', ['Preferred channel', 'to PORT', 'Fl(2+1)G'])
    # Region B
    s += mark(620, 270, [(GREEN, 1)], 'can', 'can_g', ['Port hand', 'สีเขียว ทรงกระบอก', 'ไฟเขียว'])
    s += mark(870, 270, [(RED, 1)], 'cone', 'cone_r', ['Starboard hand', 'สีแดง ทรงกรวย', 'ไฟแดง'])
    s += mark(620, 520, [(GREEN, .35), (RED, .3), (GREEN, .35)], 'can', 'can_g', ['Preferred channel', 'to STARBOARD', 'Fl(2+1)G'])
    s += mark(870, 520, [(RED, .35), (GREEN, .3), (RED, .35)], 'cone', 'cone_r', ['Preferred channel', 'to PORT', 'Fl(2+1)R'])
    s += '<text x="500" y="632" text-anchor="middle" font-size="13" fill="#334155">ด้านซ้าย/ขวา นับตาม "ทิศทางของทุ่น" (conventional direction of buoyage) — ขาเข้าจากทะเลสู่ท่าเรือ หรือตามเข็มนาฬิการอบทวีป ดูลูกศรบนแผนที่</text>\n'
    open(os.path.join(OUT, 'iala-lateral.svg'), 'w').write(s + '</svg>\n')

def cardinal():
    w, h = 1000, 780
    s = head(w, h, 'IALA Cardinal Marks — บอกว่าน้ำปลอดภัยอยู่ด้านไหนของอันตราย')
    cx, cy = 500, 390
    s += f'<circle cx="{cx}" cy="{cy}" r="62" fill="#fde68a" stroke="#b45309" stroke-width="2" stroke-dasharray="6 4"/>\n'
    s += f'<text x="{cx}" y="{cy+6}" text-anchor="middle" font-size="16" font-weight="bold" fill="#92400e">อันตราย</text>\n'
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        s += f'<line x1="{cx+70*math.sin(a):.1f}" y1="{cy-70*math.cos(a):.1f}" x2="{cx+320*math.sin(a):.1f}" y2="{cy-320*math.cos(a):.1f}" stroke="#94a3b8" stroke-dasharray="6 5"/>\n'
    def mk(x, y, bands, tm, lines):
        out = water(x, y + 4)
        b, top = body(x, y, bands, 'pillar')
        out += b
        m, mt = mast(x, top, 22)
        out += m + topmark(tm, x, mt)
        out += label(x, y + 28, lines)
        return out
    s += mk(cx, 210, [(BLK, .5), (YEL, .5)], 'N', ['NORTH', 'ดำบน เหลืองล่าง · กรวยชี้ขึ้นทั้งคู่', 'VQ หรือ Q (ต่อเนื่อง)'])
    s += mk(cx + 330, cy + 60, [(BLK, .33), (YEL, .34), (BLK, .33)], 'E', ['EAST', 'ดำ-เหลือง-ดำ · ฐานชนฐาน', 'VQ(3) 5s / Q(3) 10s'])
    s += mk(cx, 650, [(YEL, .5), (BLK, .5)], 'S', ['SOUTH', 'เหลืองบน ดำล่าง · กรวยชี้ลงทั้งคู่', 'VQ(6)+LFl 10s / Q(6)+LFl 15s'])
    s += mk(cx - 330, cy + 60, [(YEL, .33), (BLK, .34), (YEL, .33)], 'W', ['WEST', 'เหลือง-ดำ-เหลือง · ยอดชนยอด', 'VQ(9) 10s / Q(9) 15s'])
    s += '<rect x="20" y="60" width="300" height="120" rx="8" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['ช่วยจำ: ไฟแวบตามหน้าปัดนาฬิกา', 'E = 3 นาฬิกา → 3 แวบ', 'S = 6 นาฬิกา → 6 แวบ + LFl', 'W = 9 นาฬิกา → 9 แวบ', 'N = ต่อเนื่อง (ไม่มีกลุ่ม)']):
        fw = ' font-weight="bold"' if i == 0 else ''
        s += f'<text x="34" y="{86 + i*21}" font-size="14"{fw}>{t}</text>\n'
    s += '<rect x="680" y="60" width="300" height="120" rx="8" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['ช่วยจำ topmark:', 'N ชี้ขึ้น (เหนือ) · S ชี้ลง (ใต้)', 'W ยอดชนกัน = รูปแก้วไวน์', 'E ฐานชนกัน = รูปไข่ (Egg)', 'สีดำอยู่ด้านที่กรวยชี้']):
        fw = ' font-weight="bold"' if i == 0 else ''
        s += f'<text x="694" y="{86 + i*21}" font-size="14"{fw}>{t}</text>\n'
    s += f'<text x="{cx}" y="{cy-95}" text-anchor="middle" font-size="13" fill="#0369a1">ผ่านทางเหนือของทุ่น N</text>\n'
    open(os.path.join(OUT, 'iala-cardinal.svg'), 'w').write(s + '</svg>\n')

def other_marks():
    w, h = 1000, 420
    s = head(w, h, 'IALA — Isolated Danger, Safe Water, Special และ Emergency Wreck Marking')
    xs = [125, 375, 625, 875]
    # isolated danger
    x = xs[0]; y = 260
    s += water(x, y + 4)
    b, top = body(x, y, [(BLK, .35), (RED, .3), (BLK, .35)], 'pillar'); s += b
    m, mt = mast(x, top, 22); s += m + topmark('2sph', x, mt)
    s += label(x, y + 30, ['Isolated Danger', 'ดำ มีแถบแดง · ลูกกลมดำ 2 ลูก', 'ไฟขาว Fl(2)', 'วางบนอันตรายที่มีน้ำปลอดภัยรอบ'])
    # safe water
    x = xs[1]
    s += water(x, y + 4)
    # R1001: red and white vertical stripes (draw several stripes, not half/half)
    b, top = body(x, y, [(RED, .2), (WHT, .2), (RED, .2), (WHT, .2), (RED, .2)], 'sphere', w=70); s += b
    m, mt = mast(x, top, 30); s += m + topmark('sph_r', x, mt)
    s += label(x, y + 30, ['Safe Water', 'แถบแดง-ขาวแนวตั้ง · ลูกกลมแดง', 'ไฟขาว Iso / Oc / LFl 10s / Mo(A)', 'กลางร่องน้ำ / จุดเข้าฝั่ง (landfall)'])
    # special
    x = xs[2]
    s += water(x, y + 4)
    b, top = body(x, y, [(YEL, 1)], 'pillar'); s += b
    m, mt = mast(x, top, 22); s += m + topmark('X', x, mt)
    s += label(x, y + 30, ['Special Mark', 'สีเหลือง · topmark รูป X สีเหลือง', 'ไฟเหลือง (จังหวะไม่ซ้ำไฟขาว)', 'เขตพิเศษ ท่อ เคเบิล ODAS'])
    # emergency wreck
    x = xs[3]
    s += water(x, y + 4)
    b, top = vstripes(x, y, [BLU, YEL, BLU, YEL, BLU, YEL]); s += b
    m, mt = mast(x, top, 22); s += m + topmark('cross', x, mt)
    s += label(x, y + 30, ['Emergency Wreck', 'แถบน้ำเงิน-เหลืองแนวตั้ง 4–8 แถบ', 'ไฟ Al.Bu.Y (1s+0.5s+1s+0.5s)', 'กากบาท (+) เหลือง · Racon "D" · AIS'])
    open(os.path.join(OUT, 'iala-other-marks.svg'), 'w').write(s + '</svg>\n')

def light_chars():
    rows = [
        ('F', 'Fixed – ไฟนิ่ง', [(0, 24, 1)]),
        ('Oc 6s', 'Occulting – สว่างนานกว่ามืด', [(0, 4.5, 1), (4.5, 6, 0), (6, 10.5, 1), (10.5, 12, 0), (12, 16.5, 1), (16.5, 18, 0), (18, 22.5, 1), (22.5, 24, 0)]),
        ('Oc(2) 10s', 'Group occulting', [(0, 1, 0), (1, 2, 1), (2, 3, 0), (3, 10, 1), (10, 11, 0), (11, 12, 1), (12, 13, 0), (13, 20, 1), (20, 21, 0), (21, 22, 1), (22, 23, 0), (23, 24, 1)]),
        ('Iso 4s', 'Isophase – สว่างเท่ามืด', [(0, 2, 1), (2, 4, 0), (4, 6, 1), (6, 8, 0), (8, 10, 1), (10, 12, 0), (12, 14, 1), (14, 16, 0), (16, 18, 1), (18, 20, 0), (20, 22, 1), (22, 24, 0)]),
        ('Fl 5s', 'Flashing – สว่างสั้นกว่ามืด', [(0, 0.6, 1), (5, 5.6, 1), (10, 10.6, 1), (15, 15.6, 1), (20, 20.6, 1)]),
        ('LFl 10s', 'Long flash (≥ 2 s)', [(0, 2, 1), (10, 12, 1), (20, 22, 1)]),
        ('Fl(3) 10s', 'Group flashing', [(0, .5, 1), (1.5, 2, 1), (3, 3.5, 1), (10, 10.5, 1), (11.5, 12, 1), (13, 13.5, 1), (20, 20.5, 1), (21.5, 22, 1), (23, 23.5, 1)]),
        ('Fl(2+1) 12s', 'Composite group flashing', [(0, .5, 1), (1.5, 2, 1), (4.5, 5, 1), (12, 12.5, 1), (13.5, 14, 1), (16.5, 17, 1)]),
        ('Q', 'Quick 50–79/นาที (ปกติ 60)', [(i, i + .4, 1) for i in range(0, 24)]),
        ('VQ', 'Very quick 80–159/นาที (ปกติ 120)', [(i / 2, i / 2 + .2, 1) for i in range(0, 48)]),
        ('IQ', 'Interrupted quick', [(i, i + .4, 1) for i in list(range(0, 8)) + list(range(12, 20))]),
        ('Q(3) 10s', 'Group quick (East cardinal)', [(t, t + .4, 1) for b in (0, 10, 20) for t in (b, b + 1, b + 2) if t < 24]),
        ('Q(6)+LFl 15s', 'South cardinal', [(t, t + .4, 1) for t in range(0, 6)] + [(6, 8, 1)] + [(15 + t, 15.4 + t, 1) for t in range(0, 6)] + [(21, 23, 1)]),
        ('Mo(A) 8s', 'Morse code A (·−) safe water', [(0, .5, 1), (1, 2.5, 1), (8, 8.5, 1), (9, 10.5, 1), (16, 16.5, 1), (17, 18.5, 1)]),
        ('Al.WR 4s', 'Alternating – สลับสี', [(0, 2, 'W'), (2, 4, 'R'), (4, 6, 'W'), (6, 8, 'R'), (8, 10, 'W'), (10, 12, 'R'), (12, 14, 'W'), (14, 16, 'R'), (16, 18, 'W'), (18, 20, 'R'), (20, 22, 'W'), (22, 24, 'R')]),
    ]
    w = 1000; rh = 36; h = 90 + rh * len(rows) + 40
    s = head(w, h, 'ลักษณะไฟ (Light Characters) — แถบดำ = ไฟสว่าง (สเกลเวลา 24 วินาที)')
    x0, x1 = 400, 960; sc = (x1 - x0) / 24
    for i, (abbr, desc, segs) in enumerate(rows):
        y = 70 + i * rh
        s += f'<rect x="10" y="{y-2}" width="{w-20}" height="{rh-4}" fill="{"#f8fafc" if i % 2 else "#fff"}"/>\n'
        s += f'<text x="20" y="{y+20}" font-size="15" font-weight="bold" fill="#1e3a8a">{abbr}</text>\n'
        s += f'<text x="150" y="{y+20}" font-size="13">{desc}</text>\n'
        s += f'<line x1="{x0}" y1="{y+15}" x2="{x1}" y2="{y+15}" stroke="#cbd5e1"/>\n'
        for a, b, on in segs:
            col = '#111827'
            if on == 'R': col = RED
            if on == 'W': col = '#111827'
            if on:
                s += f'<rect x="{x0+a*sc:.1f}" y="{y+6}" width="{(b-a)*sc:.1f}" height="18" fill="{col}"/>\n'
    yb = 70 + len(rows) * rh + 10
    for t in range(0, 25, 2):
        s += f'<line x1="{x0+t*sc:.1f}" y1="{yb}" x2="{x0+t*sc:.1f}" y2="{yb+6}" stroke="#334155"/><text x="{x0+t*sc:.1f}" y="{yb+20}" text-anchor="middle" font-size="11">{t}s</text>\n'
    open(os.path.join(OUT, 'light-characters.svg'), 'w').write(s + '</svg>\n')

def light_range():
    w, h = 960, 520
    s = head(w, h, 'Geographical range ของไฟ — ความโค้งของโลกบังแสง')
    # earth arc (curvature exaggerated so that d1 ~ sqrt(H) and d2 ~ sqrt(h) both fit on the page)
    cx, cy, R = 480, 1063, 733
    s += f'<path d="M 0 {cy-math.sqrt(R*R-480*480):.1f} A {R} {R} 0 0 1 960 {cy-math.sqrt(R*R-480*480):.1f} L 960 {h} L 0 {h} Z" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="2"/>\n'
    def surf(x): return cy - math.sqrt(R * R - (x - cx) ** 2)
    xl, xo = 120, 860
    Hpx = 120
    # compute the true tangent from the light to the earth arc, then put the eye on that line
    Lx, Ly = xl, surf(xl) - Hpx
    dx, dy = Lx - cx, Ly - cy
    dist = math.hypot(dx, dy)
    base = math.atan2(dy, dx)
    off = math.acos(R / dist)
    cands = [(cx + R * math.cos(base + sg * off), cy + R * math.sin(base + sg * off)) for sg in (1, -1)]
    xt, yt = max(cands, key=lambda p: p[0])  # tangent point on the observer's side
    ye = Ly + (yt - Ly) * (xo - Lx) / (xt - Lx)
    hpx = surf(xo) - ye
    s += f'<rect x="{xl-10}" y="{surf(xl)-Hpx:.1f}" width="20" height="{Hpx}" fill="#f8fafc" stroke="#111827"/><circle cx="{xl}" cy="{surf(xl)-Hpx:.1f}" r="8" fill="#facc15" stroke="#111827"/>\n'
    s += f'<text x="{xl-60}" y="{surf(xl)-Hpx-16:.1f}" font-size="14" font-weight="bold">ไฟ (H เหนือระดับน้ำ)</text>\n'
    s += f'<line x1="{xo}" y1="{surf(xo):.1f}" x2="{xo}" y2="{ye:.1f}" stroke="#111827" stroke-width="4"/><circle cx="{xo}" cy="{ye:.1f}" r="7" fill="#0f172a"/>\n'
    s += f'<text x="{xo+10}" y="{ye-14:.1f}" text-anchor="end" font-size="14" font-weight="bold">ตาผู้สังเกต (h)</text>\n'
    s += f'<line x1="{xl}" y1="{surf(xl)-Hpx:.1f}" x2="{xo}" y2="{ye:.1f}" stroke="#d97706" stroke-width="2" stroke-dasharray="7 5"/>\n'
    s += f'<text x="{xo-60}" y="{ye-48:.1f}" text-anchor="end" font-size="12" fill="#92400e">เส้นแสงเฉียดขอบฟ้า (ภาพขยายความโค้ง ไม่แสดงการหักเหของแสง)</text>\n'
    s += f'<circle cx="{xt:.1f}" cy="{yt:.1f}" r="5" fill="#b91c1c"/><text x="{xt-60:.1f}" y="{yt+28:.1f}" font-size="13" fill="#b91c1c" font-weight="bold">จุดสัมผัสขอบฟ้า</text>\n'
    s += f'<text x="{(xl+xt)/2-60:.1f}" y="{surf((xl+xt)/2)+50:.1f}" font-size="14" fill="#0f172a">d₁ ≈ 2.08 √H</text>\n'
    s += f'<text x="{(xt+xo)/2-40:.1f}" y="{surf((xt+xo)/2)+50:.1f}" font-size="14" fill="#0f172a">d₂ ≈ 2.08 √h</text>\n'
    s += '<rect x="20" y="50" width="450" height="134" rx="8" fill="#fff" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['Geographical range (nm) ≈ 2.08 (√H + √h)  [H, h เป็นเมตร]', 'ตัวอย่าง: H = 45 m, h = 16 m → 2.08 (6.71 + 4.00) ≈ 22.3 nm', 'ตาราง Geographical Range ใน List of Lights (IHO S-12) ใช้ 2.03 → ≈ 21.7 nm', 'Visible range = ค่าที่น้อยกว่าระหว่าง', 'luminous range กับ geographical range']):
        s += f'<text x="34" y="{76 + i*24}" font-size="13">{t}</text>\n'
    open(os.path.join(OUT, 'light-range.svg'), 'w').write(s + '</svg>\n')

def sector_light():
    w, h = 900, 620
    s = head(w, h, 'Sector light ที่ทางเข้าร่องน้ำ (ตัวอย่างจำลอง)')
    L = (450, 120)
    s += '<path d="M 0 50 L 900 50 L 900 110 Q 700 120 560 100 L 450 120 L 340 100 Q 200 120 0 110 Z" fill="#f5deb3" stroke="#8b6b3d" stroke-width="2"/>\n'
    def wedge(b1, b2, col, r=420):
        # bearings FROM seaward TO the light: sector defined by bearings from sea; draw from light outward at reciprocal
        a1, a2 = math.radians(b1 + 180), math.radians(b2 + 180)
        x1, y1 = L[0] + r * math.sin(a1), L[1] - r * math.cos(a1)
        x2, y2 = L[0] + r * math.sin(a2), L[1] - r * math.cos(a2)
        return f'<path d="M {L[0]} {L[1]} L {x1:.1f} {y1:.1f} A {r} {r} 0 0 1 {x2:.1f} {y2:.1f} Z" fill="{col}" opacity="0.35"/>\n'
    s += wedge(320, 357, '#16a34a')
    s += wedge(357, 3, '#ffffff')
    s += wedge(3, 40, '#dc2626')
    for b in (320, 357, 3, 40):
        a = math.radians(b + 180)
        s += f'<line x1="{L[0]}" y1="{L[1]}" x2="{L[0]+420*math.sin(a):.1f}" y2="{L[1]-420*math.cos(a):.1f}" stroke="#334155" stroke-dasharray="4 4"/>\n'
    s += f'<circle cx="{L[0]}" cy="{L[1]}" r="9" fill="#facc15" stroke="#111827" stroke-width="2"/>\n'
    s += f'<text x="{L[0]+14}" y="{L[1]-6}" font-size="14" font-weight="bold">Dir.Lt / Fl.WRG.4s</text>\n'
    s += '<text x="250" y="420" font-size="15" font-weight="bold" fill="#b91c1c">R 003°–040°</text>\n'
    s += '<text x="450" y="584" text-anchor="middle" font-size="15" font-weight="bold" fill="#334155">W 357°–003° (แนวร่องน้ำ — ไฟขาวแคบตรงกลาง)</text>\n'
    s += '<text x="560" y="420" font-size="15" font-weight="bold" fill="#15803d">G 320°–357°</text>\n'
    s += '<path d="M 450 560 L 450 170" stroke="#1e3a8a" stroke-width="3"/><path d="M 442 182 L 450 165 L 458 182 Z" fill="#1e3a8a"/>\n'
    s += '<text x="450" y="606" text-anchor="middle" font-size="12" fill="#1e3a8a">เรือขาเข้า ถือเข็ม 000° ตามแนวไฟขาว · เห็นแดง = หลุดไปทางซ้ายของแนว เห็นเขียว = หลุดไปทางขวา (ตาม Region A)</text>\n'
    s += '<rect x="620" y="140" width="270" height="120" rx="8" fill="#fff" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['แบริ่งของ sector วัด "จากทะเล', 'มองเข้าหาไฟ" (from seaward)', 'อยู่ใน W = อยู่บนแนวร่องน้ำ', 'เห็น R/G = หลุดไปด้านข้าง', 'ขอบ sector ไม่คมชัด อย่าเชื่อ 100%']):
        s += f'<text x="632" y="{164 + i*21}" font-size="13">{t}</text>\n'
    open(os.path.join(OUT, 'light-sectors.svg'), 'w').write(s + '</svg>\n')

def luminous_range():
    """Luminous range diagram computed from Allard's law with IALA constants
    (threshold illuminance 0.2 microlux at night; nominal range = luminous range at
    meteorological visibility 10 M, i.e. atmospheric transmissivity 0.05 over 10 M)."""
    Et, NM = 2e-7, 1852.0
    def intensity(rn):
        return Et * (rn * NM) ** 2 / (0.05 ** (rn / 10.0))
    def lum(I, V):
        lo, hi = 0.001, 300.0
        for _ in range(80):
            m = (lo + hi) / 2
            if I * 0.05 ** (m / V) / (m * NM) ** 2 > Et: lo = m
            else: hi = m
        return lo
    w, h = 960, 600
    s = head(w, h, 'Luminous range diagram — ความสัมพันธ์ nominal range กับทัศนวิสัย')
    gx0, gx1, gy0, gy1 = 90, 640, 70, 520
    xmax, ymax = 30.0, 45.0
    def X(v): return gx0 + v / xmax * (gx1 - gx0)
    def Y(v): return gy1 - v / ymax * (gy1 - gy0)
    s += f'<rect x="{gx0}" y="{gy0}" width="{gx1-gx0}" height="{gy1-gy0}" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for v in range(0, 31, 5):
        s += f'<line x1="{X(v):.1f}" y1="{gy0}" x2="{X(v):.1f}" y2="{gy1}" stroke="#e2e8f0"/><text x="{X(v):.1f}" y="{gy1+18}" text-anchor="middle" font-size="12">{v}</text>\n'
    for v in range(0, 46, 5):
        s += f'<line x1="{gx0}" y1="{Y(v):.1f}" x2="{gx1}" y2="{Y(v):.1f}" stroke="#e2e8f0"/><text x="{gx0-8}" y="{Y(v)+4:.1f}" text-anchor="end" font-size="12">{v}</text>\n'
    s += f'<text x="{(gx0+gx1)/2}" y="{gy1+42}" text-anchor="middle" font-size="13" font-weight="bold">Nominal range (M) — ค่าที่พิมพ์ในแผนที่/ALL</text>\n'
    s += f'<text x="30" y="{(gy0+gy1)/2}" text-anchor="middle" font-size="13" font-weight="bold" transform="rotate(-90 30 {(gy0+gy1)/2})">Luminous range (M)</text>\n'
    cols = {1: '#7f1d1d', 2: '#b91c1c', 5: '#ea580c', 10: '#0f172a', 20: '#1d4ed8', 50: '#0891b2'}
    for V, col in cols.items():
        pts = []
        for i in range(1, 301):
            rn = i * xmax / 300
            L = lum(intensity(rn), V)
            if L > ymax: break
            pts.append((X(rn), Y(L)))
        d = 'M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in pts)
        sw = 3 if V == 10 else 2
        s += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}"/>\n'
        lx, ly = pts[-1]
        lab = f'V = {V} M' + (' (= nominal)' if V == 10 else '')
        if ly < gy0 + 14:
            s += f'<text x="{lx-4:.1f}" y="{gy0+16}" text-anchor="end" font-size="12" font-weight="bold" fill="{col}">{lab}</text>\n'
        else:
            s += f'<text x="{min(lx+6, gx1-4):.1f}" y="{ly-7:.1f}" font-size="12" font-weight="bold" fill="{col}" text-anchor="{"end" if lx > gx1-90 else "start"}">{lab}</text>\n'
    # worked example: nominal 20 M, visibility 5 M
    ex = lum(intensity(20), 5)
    s += f'<line x1="{X(20):.1f}" y1="{gy1}" x2="{X(20):.1f}" y2="{Y(ex):.1f}" stroke="#15803d" stroke-width="2" stroke-dasharray="5 3"/>\n'
    s += f'<line x1="{X(20):.1f}" y1="{Y(ex):.1f}" x2="{gx0}" y2="{Y(ex):.1f}" stroke="#15803d" stroke-width="2" stroke-dasharray="5 3"/>\n'
    s += f'<circle cx="{X(20):.1f}" cy="{Y(ex):.1f}" r="5" fill="#15803d"/>\n'
    s += f'<text x="{X(20)+8:.1f}" y="{Y(ex)+18:.1f}" font-size="12" fill="#15803d" font-weight="bold">20 M ที่ V 5 M → ≈ {ex:.0f} M</text>\n'
    # info box
    bx = 665
    s += f'<rect x="{bx}" y="70" width="280" height="300" rx="8" fill="#fff" stroke="#94a3b8"/>\n'
    lines = ['วิธีอ่าน (เหมือน diagram ใน ALL)', '1. เข้าแกนนอนด้วย nominal range', '2. ขึ้นไปถึงเส้นทัศนวิสัย (V) ที่คาด', '3. อ่าน luminous range ที่แกนตั้ง',
             '', 'ตัวอย่างจำลอง (คำนวณ):', f'• nominal 20 M, V 5 M → ≈ {lum(intensity(20),5):.1f} M', f'• nominal 24 M, V 5 M → ≈ {lum(intensity(24),5):.1f} M',
             f'• nominal 10 M, V 7 M → ≈ {lum(intensity(10),7):.1f} M', '', 'เส้น V = 10 M คือเส้นที่ luminous = nominal', '(นิยามของ nominal range)']
    for i, t in enumerate(lines):
        fw = ' font-weight="bold"' if i in (0, 5) else ''
        s += f'<text x="{bx+12}" y="{94 + i*22}" font-size="12.5"{fw}>{t}</text>\n'
    s += f'<text x="{bx}" y="400" font-size="11" fill="#475569">คำนวณด้วย Allard\'s law: E = I·T^d / d²</text>\n'
    s += f'<text x="{bx}" y="418" font-size="11" fill="#475569">E ขีดเริ่มเห็นกลางคืน 0.2 µlux (IALA)</text>\n'
    s += f'<text x="{bx}" y="436" font-size="11" fill="#475569">T = 0.05 ต่อระยะเท่ากับทัศนวิสัย V</text>\n'
    s += f'<text x="{bx}" y="462" font-size="11" fill="#b91c1c">ใช้ประกอบการเรียน บนเรือให้อ่าน diagram</text>\n'
    s += f'<text x="{bx}" y="480" font-size="11" fill="#b91c1c">ในเล่ม List of Lights ที่ใช้จริง</text>\n'
    s += f'<text x="{bx}" y="506" font-size="11" fill="#475569">ระยะที่เห็นจริง = ค่าน้อยกว่าระหว่าง</text>\n'
    s += f'<text x="{bx}" y="522" font-size="11" fill="#475569">luminous range กับ geographical range</text>\n'
    open(os.path.join(OUT, 'light-luminous-range.svg'), 'w').write(s + '</svg>\n')

if __name__ == '__main__':
    lateral(); cardinal(); other_marks(); light_chars(); light_range(); sector_light(); luminous_range()
    print('ok')
