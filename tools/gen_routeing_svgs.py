"""ภาพประกอบบท routeing / blind pilotage"""
import math, os
R = math.radians
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker>'
            '<marker id="arg" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#4ade80"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{t}</text>\n')
def save(n, s): open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')

def pi_radar():
    w, h = 1000, 560
    s = head(w, h, 'Parallel Indexing บนจอเรดาร์ (relative motion, north-up)')
    for k, (cx, title, off) in enumerate([(250, 'เรืออยู่บนเส้นทาง', 0.0), (720, 'เรือหลุดไปทางขวา 0.3\'', 0.3)]):
        cy, r = 300, 210
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#052e16" stroke="#334155" stroke-width="4"/>\n'
        for rr in (70, 140):
            s += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#166534" stroke-dasharray="3 4"/>\n'
        s += f'<text x="{cx}" y="70" text-anchor="middle" font-size="16" font-weight="bold">{title}</text>\n'
        trk = 45; sc = 70  # px per nm (ring 1 nm)
        ux, uy = math.sin(R(trk)), -math.cos(R(trk))
        # heading line
        s += f'<line x1="{cx}" y1="{cy}" x2="{cx+ux*r:.1f}" y2="{cy+uy*r:.1f}" stroke="#bbf7d0" stroke-width="2"/>\n'
        # PI line at 1.2 nm to starboard of track (perp right = (-uy, ux)) — but in relative motion target moves opposite to track
        px, py = -uy, ux
        cir = 1.2
        x1, y1 = cx + px * cir * sc + ux * 2.5 * sc, cy + py * cir * sc + uy * 2.5 * sc
        x2, y2 = cx + px * cir * sc - ux * 2.5 * sc, cy + py * cir * sc - uy * 2.5 * sc
        s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#facc15" stroke-width="2.5"/>\n'
        # clearing line 0.9 nm (limit before no-go area) — same as worked example in the text
        clr = 0.9
        c1x, c1y = cx + px * clr * sc + ux * 2.3 * sc, cy + py * clr * sc + uy * 2.3 * sc
        c2x, c2y = cx + px * clr * sc - ux * 2.3 * sc, cy + py * clr * sc - uy * 2.3 * sc
        s += f'<line x1="{c1x:.1f}" y1="{c1y:.1f}" x2="{c2x:.1f}" y2="{c2y:.1f}" stroke="#f87171" stroke-width="1.8" stroke-dasharray="7 5"/>\n'
        s += f'<text x="{c2x-6:.1f}" y="{c2y-6:.1f}" font-size="12" fill="#f87171" text-anchor="end">clearing 0.9\'</text>\n'
        for rr, lab in ((70, "1'"), (140, "2'")):
            s += f'<text x="{cx-rr*0.71-4:.1f}" y="{cy-rr*0.71-4:.1f}" font-size="10" fill="#4ade80" text-anchor="end">{lab}</text>\n'
        # echo track: actual passing distance = cir - off (ship set to starboard => closer)
        d = cir - off
        for i, t in enumerate([2.2, 1.5, 0.8]):
            ex, ey = cx + px * d * sc + ux * t * sc, cy + py * d * sc + uy * t * sc
            s += f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{6 if i==2 else 4}" fill="#4ade80" opacity="{0.4+0.3*i}"/>\n'
        ex0, ey0 = cx + px * d * sc + ux * 2.2 * sc, cy + py * d * sc + uy * 2.2 * sc
        ex1, ey1 = cx + px * d * sc + ux * 0.8 * sc, cy + py * d * sc + uy * 0.8 * sc
        s += f'<line x1="{ex0:.1f}" y1="{ey0:.1f}" x2="{ex1:.1f}" y2="{ey1:.1f}" stroke="#4ade80" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arg)"/>\n'
        s += f'<circle cx="{cx}" cy="{cy}" r="4" fill="#fff"/>\n'
        s += f'<text x="{x1+6:.1f}" y="{y1:.1f}" font-size="12" fill="#facc15">PI 1.2\'</text>\n'
        s += f'<text x="{cx+ux*r+6:.1f}" y="{cy+uy*r:.1f}" font-size="12" fill="#bbf7d0">HL 045°</text>\n'
    s += '<text x="40" y="535" font-size="13">เป้าถาวร (ประภาคาร) เคลื่อนบนจอขนานและสวนทางกับ ground track ของเรา · ถ้าเป้าเคลื่อนตามเส้น PI = อยู่บนเส้นทาง</text>\n'
    s += '<text x="40" y="555" font-size="13">ภาพขวา: เป้าเคลื่อนเข้ามาใกล้กว่าเส้น PI (1.2\' → 0.9\') ถึงเส้น clearing (แดง) = เรือถูกพาไปทางขวาเข้าหาเป้า → แก้เข็มไปทางซ้ายทันที แจ้งนายเรือ</text>\n'
    save('blind-pilotage-pi.svg', s)

def oarrow(x, y, dx, L=70, W=14, col='#a21caf', dash=False):
    """outlined arrow (chart symbol) from (x,y) horizontally, dx=+1 east / -1 west"""
    hl, sw = 22, W / 2
    pts = [(0, -sw / 2), (L - hl, -sw / 2), (L - hl, -sw), (L, 0), (L - hl, sw), (L - hl, sw / 2), (0, sw / 2)]
    d = ' '.join(f'{x + dx * a:.1f},{y + b:.1f}' for a, b in pts)
    da = ' stroke-dasharray="5 3"' if dash else ''
    return f'<polygon points="{d}" fill="#fff" stroke="{col}" stroke-width="2"{da}/>'

def tdash(pts, col='#a21caf', inward=None):
    """limit of restricted area: T-shaped dashes, stems pointing into the area (centre = inward)"""
    out = ''
    n = len(pts)
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        Lg = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / Lg, (y2 - y1) / Lg
        nx, ny = -uy, ux
        if inward and ((inward[0] - x1) * nx + (inward[1] - y1) * ny) < 0: nx, ny = -nx, -ny
        t = 4
        while t < Lg - 10:
            ax, ay, bx, by = x1 + ux * t, y1 + uy * t, x1 + ux * (t + 12), y1 + uy * (t + 12)
            mx, my = x1 + ux * (t + 6), y1 + uy * (t + 6)
            out += f'<path d="M {ax:.1f} {ay:.1f} L {bx:.1f} {by:.1f} M {mx:.1f} {my:.1f} L {mx + nx * 7:.1f} {my + ny * 7:.1f}" stroke="{col}" stroke-width="2" fill="none"/>'
            t += 20
    return out + '\n'

def measures():
    w, h = 1000, 560
    s = head(w, h, 'มาตรการจัดเส้นทางเดินเรือ (Routeing measures) — สัญลักษณ์บนแผนที่โดยสรุป')
    items = [
        ('Traffic lane + separation zone', 'tss'), ('Roundabout', 'round'), ('Inshore traffic zone', 'itz'), ('Two-way route', 'two'),
        ('Recommended track / route', 'rec'), ('Deep-water route (DW)', 'dw'), ('Precautionary area', 'prec'), ('Area to be avoided (ATBA)', 'atba'),
    ]
    for i, (t, k) in enumerate(items):
        c, r = i % 4, i // 4
        x, y = 20 + c * 245, 60 + r * 245
        s += f'<rect x="{x}" y="{y}" width="230" height="230" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>\n'
        s += f'<text x="{x+115}" y="{y+24}" text-anchor="middle" font-size="13" font-weight="bold">{t}</text>\n'
        cx, cy = x + 115, y + 130
        M = '#a21caf'
        if k == 'tss':
            s += f'<rect x="{x+20}" y="{cy-12}" width="190" height="24" fill="{M}" opacity="0.3"/>'
            s += f'<path d="M {x+20} {cy-70} L {x+210} {cy-70} M {x+20} {cy+70} L {x+210} {cy+70}" stroke="{M}" stroke-dasharray="8 5" stroke-width="1.5"/>'
            s += oarrow(x + 150, cy - 40, -1) + oarrow(x + 80, cy + 40, +1)
            s += f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="10">separation zone</text>'
            s += f'<text x="{cx}" y="{cy+88}" text-anchor="middle" font-size="11">ลูกศรโปร่ง = ทิศการจราจรที่กำหนด</text>'
            s += f'<text x="{cx}" y="{cy+103}" text-anchor="middle" font-size="11">เดินชิดขวา (zone อยู่ทางซ้ายเรา)</text>\n'
        elif k == 'round':
            s += f'<circle cx="{cx}" cy="{cy}" r="22" fill="{M}" opacity="0.3"/><circle cx="{cx}" cy="{cy}" r="60" fill="none" stroke="{M}" stroke-dasharray="6 4"/>'
            s += f'<path d="M {cx+60} {cy} A 60 60 0 0 0 {cx} {cy-60}" fill="none" stroke="{M}" stroke-width="3" marker-end="url(#ar)"/>\n'
            s += f'<text x="{cx}" y="{cy+90}" text-anchor="middle" font-size="11">วนทวนเข็มนาฬิการอบจุดกลาง</text>\n'
        elif k == 'itz':
            s += f'<rect x="{x+20}" y="{cy-70}" width="190" height="50" fill="#fef9c3" stroke="#ca8a04" stroke-dasharray="5 3"/><rect x="{x+20}" y="{cy-20}" width="190" height="40" fill="#e0f2fe"/>'
            s += f'<text x="{cx}" y="{cy-40}" text-anchor="middle" font-size="11">ITZ (ระหว่าง lane กับฝั่ง)</text><rect x="{x+20}" y="{cy-100}" width="190" height="30" fill="#f5deb3"/>\n'
            s += f'<text x="{cx}" y="{cy-81}" text-anchor="middle" font-size="11">ฝั่ง (coast)</text>'
            s += f'<rect x="{x+20}" y="{cy-22}" width="190" height="5" fill="{M}" opacity="0.45"/>'
            s += oarrow(x + 145, cy + 5, -1, L=60, W=12)
            s += f'<text x="{cx}" y="{cy+40}" text-anchor="middle" font-size="11">traffic lane ของ TSS</text>'
            s += f'<text x="{cx}" y="{cy+88}" text-anchor="middle" font-size="11">ใช้ตาม COLREG Rule 10(d)</text>\n'
        elif k == 'two':
            s += f'<path d="M {x+30} {cy-25} L {x+200} {cy-25} M {x+30} {cy+25} L {x+200} {cy+25}" stroke="{M}" stroke-dasharray="8 5" stroke-width="2"/>'
            s += oarrow(x + 175, cy - 11, -1, L=60, W=11, dash=True) + oarrow(x + 55, cy + 11, +1, L=60, W=11, dash=True)
            s += f'<text x="{cx}" y="{cy+70}" text-anchor="middle" font-size="11">สองทาง — ให้ชิดขวา (GPSR 8.7)</text>\n'
        elif k == 'rec':
            s += f'<path d="M {x+30} {cy+40} L {x+200} {cy-40}" stroke="#111827" stroke-width="2"/><path d="M {x+60} {cy+26} L {x+100} {cy+7}" stroke="#111827" stroke-width="2" marker-end="url(#ar)"/>'
            s += f'<text x="{cx}" y="{cy+80}" text-anchor="middle" font-size="11">เส้นเดี่ยว/เส้นประ ตามที่แผนที่กำหนด</text>\n'
        elif k == 'dw':
            s += f'<path d="M {x+30} {cy-20} L {x+200} {cy-20} M {x+30} {cy+20} L {x+200} {cy+20}" stroke="{M}" stroke-dasharray="10 5" stroke-width="2"/><text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="16" font-weight="bold" fill="{M}">DW 22m</text>'
            s += f'<text x="{cx}" y="{cy+80}" text-anchor="middle" font-size="11">สำหรับเรือกินน้ำลึก (สำรวจแล้ว)</text>\n'
        elif k == 'prec':
            s += f'<rect x="{x+40}" y="{cy-60}" width="150" height="120" fill="none" stroke="{M}" stroke-dasharray="6 4" stroke-width="2"/><path d="M {cx} {cy-26} L {cx+24} {cy+16} L {cx-24} {cy+16} Z" fill="none" stroke="{M}" stroke-width="2.5"/><text x="{cx}" y="{cy+11}" text-anchor="middle" font-size="22" font-weight="bold" fill="{M}">!</text>'
            s += f'<text x="{cx}" y="{cy+85}" text-anchor="middle" font-size="11">ระวังเป็นพิเศษ (อาจมีทิศแนะนำ)</text>\n'
        elif k == 'atba':
            s += tdash([(x+40, cy-50), (x+190, cy-58), (x+198, cy+42), (x+50, cy+50)], M, inward=(cx, cy))
            s += f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="13" fill="{M}" font-weight="bold">ATBA</text>'
            s += f'<text x="{cx}" y="{cy+80}" text-anchor="middle" font-size="11">หลีกเลี่ยงทั้งหมดหรือบางประเภทเรือ</text>'
            s += f'<text x="{cx}" y="{cy+94}" text-anchor="middle" font-size="10">ขอบเป็น T-dash ก้านชี้เข้าพื้นที่</text>\n'
    save('routeing-measures.svg', s)

def pi_wheel_over():
    """ตัวอย่างจำลอง 2 ในบท 1.2.1-C: คำนวณ CIR และขีด wheel-over บนเส้น PI"""
    w, h = 1000, 560
    s = head(w, h, 'วางแผน PI และจุด wheel-over (ตัวอย่างจำลอง: ขา 045° → 090°)')
    # --- chart view (east/north in nm, B = origin) ---
    sc, ox, oy = 110, 330, 150
    P = lambda e, n: (ox + sc * e, oy - sc * n)
    u1 = (math.sin(R(45)), math.cos(R(45)))
    L = (2.0 * math.sin(R(160)), 2.0 * math.cos(R(160)))
    a1 = L[0] * u1[0] + L[1] * u1[1]           # along-track of L on leg 1 (negative = before B)
    c1 = L[0] * u1[1] - L[1] * u1[0]           # cross-track (starboard +)
    A1 = (a1 * u1[0], a1 * u1[1]); A2 = (L[0], 0.0)
    WOP = (-0.5 * u1[0], -0.5 * u1[1])
    s += '<rect x="20" y="50" width="590" height="420" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>\n'
    s += '<text x="315" y="72" text-anchor="middle" font-size="14" font-weight="bold">บนแผนที่/ECDIS (ทิศเหนือขึ้น)</text>\n'
    x0, y0 = P(-2.1, -2.1); xb, yb = P(0, 0); x2, y2 = P(2.3, 0)
    s += f'<path d="M {x0:.1f} {y0:.1f} L {xb:.1f} {yb:.1f} L {x2:.1f} {y2:.1f}" fill="none" stroke="#0f172a" stroke-width="2.5"/>\n'
    s += f'<text x="{P(-1.32,-1.2)[0]:.1f}" y="{P(-1.32,-1.2)[1]:.1f}" font-size="13" font-weight="bold" text-anchor="end">045°T</text><text x="{P(1.6,0.12)[0]:.1f}" y="{P(1.6,0.12)[1]:.1f}" font-size="13" font-weight="bold">090°T</text>\n'
    s += f'<circle cx="{xb:.1f}" cy="{yb:.1f}" r="4" fill="#0f172a"/><text x="{xb-8:.1f}" y="{yb-10:.1f}" font-size="13" text-anchor="end" font-weight="bold">WP B</text>\n'
    xl, yl = P(*L)
    s += f'<path d="M {xl:.1f} {yl-12:.1f} L {xl+8:.1f} {yl+6:.1f} L {xl-8:.1f} {yl+6:.1f} Z" fill="#f59e0b" stroke="#0f172a"/><text x="{xl+12:.1f}" y="{yl+18:.1f}" font-size="13" font-weight="bold">ประภาคาร L</text>\n'
    s += f'<text x="{xl+12:.1f}" y="{yl+34:.1f}" font-size="11">160°T 2.0\' จาก B</text>\n'
    for (ax, ay), lab, col in ((A1, f"CIR {c1:.2f}'", '#b45309'), (A2, "CIR 1.88'", '#0369a1')):
        xa, ya = P(ax, ay)
        s += f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xl:.1f}" y2="{yl:.1f}" stroke="{col}" stroke-width="1.8" stroke-dasharray="6 4"/>\n'
        mx, my = (xa + xl) / 2, (ya + yl) / 2
        s += f'<text x="{mx+(-8 if col=="#b45309" else 8):.1f}" y="{my:.1f}" font-size="12" fill="{col}" font-weight="bold" text-anchor="{"end" if col=="#b45309" else "start"}">{lab}</text>\n'
    xw, yw = P(*WOP); xa1, ya1 = P(*A1)
    s += f'<circle cx="{xw:.1f}" cy="{yw:.1f}" r="6" fill="#dc2626"/><text x="{xw-10:.1f}" y="{yw-6:.1f}" font-size="12" fill="#dc2626" font-weight="bold" text-anchor="end">WOP (0.5\' ก่อน B)</text>\n'
    s += f'<circle cx="{xa1:.1f}" cy="{ya1:.1f}" r="4" fill="#b45309"/><text x="{xa1-10:.1f}" y="{ya1+4:.1f}" font-size="11" fill="#b45309" text-anchor="end">L ตรงกราบ (0.85\' ก่อน B)</text>\n'
    s += '<text x="36" y="440" font-size="12">ระหว่างจุดตรงกราบกับ WOP = 0.85 − 0.50 = 0.35\' → ที่ WOP เป้าอยู่ท้ายแนวกราบ 0.35\'</text>\n'
    s += '<text x="36" y="458" font-size="12">มาตราส่วนในภาพ: 1 ไมล์ ≈ 110 px (ภาพประกอบ ไม่ใช่แผนที่จริง)</text>\n'
    # --- radar view at WOP (relative motion, north-up) ---
    cx, cy, r, rs = 805, 290, 175, 60
    s += f'<text x="{cx}" y="72" text-anchor="middle" font-size="14" font-weight="bold">จอเรดาร์ขณะถึง WOP (RM, north-up)</text>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#052e16" stroke="#334155" stroke-width="4"/>\n'
    for rr in (rs, 2 * rs):
        s += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#166534" stroke-dasharray="3 4"/>\n'
    ux, uy = math.sin(R(45)), -math.cos(R(45)); px, py = -uy, ux
    s += f'<line x1="{cx}" y1="{cy}" x2="{cx+ux*r:.1f}" y2="{cy+uy*r:.1f}" stroke="#bbf7d0" stroke-width="2"/>\n'
    bx, by = cx + px * c1 * rs, cy + py * c1 * rs
    s += f'<line x1="{bx+ux*1.6*rs:.1f}" y1="{by+uy*1.6*rs:.1f}" x2="{bx-ux*1.0*rs:.1f}" y2="{by-uy*1.0*rs:.1f}" stroke="#facc15" stroke-width="2.5"/>\n'
    s += f'<text x="{bx+ux*1.6*rs-8:.1f}" y="{by+uy*1.6*rs+4:.1f}" font-size="12" fill="#facc15" text-anchor="end">PI {c1:.2f}\'</text>\n'
    s += f'<line x1="{cx}" y1="{cy}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#94a3b8" stroke-dasharray="3 3"/>\n'
    wx, wy = bx - ux * 0.35 * rs, by - uy * 0.35 * rs
    s += f'<line x1="{wx-px*10:.1f}" y1="{wy-py*10:.1f}" x2="{wx+px*10:.1f}" y2="{wy+py*10:.1f}" stroke="#f87171" stroke-width="3"/>\n'
    s += f'<circle cx="{wx:.1f}" cy="{wy:.1f}" r="6" fill="#4ade80"/>\n'
    s += f'<text x="{wx-16:.1f}" y="{wy+4:.1f}" font-size="12" fill="#f87171" text-anchor="end">WO (ท้ายกราบ 0.35\')</text>\n'
    yn = cy + 1.88 * rs
    half = math.sqrt(max(r * r - (1.88 * rs) ** 2, 0)) - 6
    s += f'<line x1="{cx-half:.1f}" y1="{yn:.1f}" x2="{cx+half:.1f}" y2="{yn:.1f}" stroke="#fde68a" stroke-width="1.8" stroke-dasharray="8 5"/>\n'
    s += f'<text x="{cx-half+10:.1f}" y="{yn+16:.1f}" font-size="11" fill="#fde68a">PI ขาใหม่ 090° = 1.88\'</text>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="4" fill="#fff"/>\n'
    s += f'<text x="{cx}" y="{cy+r+22}" text-anchor="middle" font-size="12">เช็คซ้ำ: เป้าระยะ 1.85\' แบริ่ง 146°T (VRM + EBL)</text>\n'
    s += '<text x="20" y="500" font-size="13">CIR = 2.0 × sin(160° − 045°) = 1.81\' · จุดตรงกราบ = 2.0 × |cos 115°| = 0.85\' ก่อน B · CIR ขาใหม่ = 2.0 × sin(160° − 090°) = 1.88\'</text>\n'
    s += '<text x="20" y="522" font-size="13">เมื่อเป้าเลื่อนตามเส้น PI มาถึงขีด WO ให้สั่งหางเสือ แล้วย้ายไปดูเส้น PI ขาใหม่ (เป้าควรเข้ามาอยู่บนเส้น 1.88\' หลังเลี้ยวเสร็จ)</text>\n'
    s += '<text x="20" y="544" font-size="12" fill="#64748b">วงระยะบนจอ 1\' และ 2\' · เส้นสีเทา = แนวกราบขวา (beam)</text>\n'
    save('blind-pilotage-wheel-over.svg', s)

if __name__ == '__main__':
    pi_radar(); measures(); pi_wheel_over(); print('ok')
