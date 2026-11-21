"""ภาพประกอบบท 3.2.1 เสถียรภาพของเรือ — ค่าตัวอย่างเป็นของเรือสมมุติ MV Andaman Pearl"""
import math, os
R = math.radians
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"


def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker>'
            '<marker id="arB" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#1d4ed8"/></marker>'
            '<marker id="arR" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#b91c1c"/></marker>'
            '<marker id="arG" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#15803d"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{t}</text>\n')


def save(n, s):
    open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')


def txt(x, y, t, size=12, anchor='start', fill='#0f172a', bold=False):
    b = ' font-weight="bold"' if bold else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{fill}"{b}>{t}</text>\n'


def line(x1, y1, x2, y2, col='#0f172a', w=2, dash=None, mk=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    m = f' marker-end="url(#{mk})"' if mk else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{d}{m}/>\n'


def rect(x, y, w, h, fill='#e2e8f0', stroke='#0f172a', sw=1.5, rx=0):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def dot(x, y, lab, col, side='end', dx=-10):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{col}"/>' + txt(x + dx, y + 4, lab, 13, side, col, True)


# ข้อมูลตัวอย่าง (สอดคล้องกับเนื้อหาในบท)
KG, FSC, KM = 10.14, 0.071, 11.90
KGF = KG + FSC
KN = {0: 0, 10: 2.10, 20: 4.20, 30: 6.15, 40: 7.70, 50: 8.80, 60: 9.45, 70: 9.70, 80: 9.55}
GZ = {a: KN[a] - KGF * math.sin(R(a)) for a in KN}


def gz(t):
    i = min(int(t // 10), 7)
    return GZ[i * 10] + (GZ[i * 10 + 10] - GZ[i * 10]) * (t - i * 10) / 10


# ---------------------------------------------------------------- B G M
def bgm():
    w, h = 1000, 520
    s = head(w, h, 'จุดสำคัญของเสถียรภาพตามขวาง: K, B, G, M และแขนตั้งตรง GZ')
    for k, (cx, ang, title) in enumerate(((250, 0, 'เรือตั้งตรง (upright)'), (720, 20, 'เรือเอียงด้วยแรงภายนอก θ'))):
        wl, keel = 250, 400
        Gy, My, By = 220, 140, 325
        s += txt(cx, 70, title, 15, 'middle', bold=True)
        s += f'<g transform="rotate({ang} {cx} {wl})">'
        s += f'<path d="M {cx-150} 120 L {cx+150} 120 L {cx+150} {keel-30} Q {cx+150} {keel} {cx+120} {keel} L {cx-120} {keel} Q {cx-150} {keel} {cx-150} {keel-30} Z" fill="#e2e8f0" stroke="#0f172a" stroke-width="2.5"/>'
        s += line(cx, 100, cx, keel + 10, '#94a3b8', 1, '4 3')
        s += dot(cx, keel, 'K', '#0f172a') + dot(cx, Gy, 'G', '#b91c1c')
        s += '</g>'
        s += f'<rect x="{cx-200}" y="{wl}" width="400" height="{h-wl-60}" fill="#bae6fd" opacity="0.45"/>'
        s += line(cx - 200, wl, cx + 200, wl, '#0284c7', 2)
        if ang == 0:
            s += dot(cx, By, 'B', '#1d4ed8')
            s += dot(cx, My, 'M', '#15803d')
            s += line(cx + 40, My, cx + 40, Gy, '#15803d', 1.5) + txt(cx + 46, (My + Gy) / 2 + 4, 'GM', 12, 'start', '#15803d', True)
            s += line(cx + 90, keel, cx + 90, By, '#1d4ed8', 1.2, mk='arB') + txt(cx + 96, 365, 'KB', 12, 'start', '#1d4ed8', True)
            s += line(cx + 120, keel, cx + 120, Gy, '#b91c1c', 1.2, mk='arR') + txt(cx + 126, 300, 'KG', 12, 'start', '#b91c1c', True)
            s += line(cx - 100, keel, cx - 100, My, '#15803d', 1.2, mk='arG') + txt(cx - 106, 280, 'KM', 12, 'end', '#15803d', True)
            s += line(cx, Gy, cx, Gy + 40, '#b91c1c', 3, mk='arR') + line(cx, By, cx, By - 40, '#1d4ed8', 3, mk='arB')
        else:
            sa, ca = math.sin(R(ang)), math.cos(R(ang))
            gx, gy = cx + (wl - Gy) * sa, wl - (wl - Gy) * ca
            mx, my = cx + (wl - My) * sa, wl - (wl - My) * ca
            b1x, b1y = mx, 335
            s += dot(mx, my, 'M', '#15803d', 'start', 10)
            s += dot(b1x, b1y, 'B₁', '#1d4ed8', 'start', 10)
            s += line(b1x, b1y, mx, my, '#1d4ed8', 1.3, '5 3')
            s += line(gx, gy, b1x, gy, '#b91c1c', 3) + dot(b1x, gy, 'Z', '#b91c1c', 'start', 10)
            s += txt((gx + b1x) / 2, gy - 12, 'GZ', 13, 'middle', '#b91c1c', True)
            s += line(gx, gy, gx, gy + 50, '#b91c1c', 3, mk='arR') + txt(gx - 8, gy + 66, 'น้ำหนัก (Δ) ลงที่ G', 11, 'end', '#b91c1c')
            s += line(b1x, b1y, b1x, b1y - 45, '#1d4ed8', 3, mk='arB') + txt(b1x + 12, b1y - 22, 'แรงลอยตัวขึ้นที่ B₁', 11, 'start', '#1d4ed8')
            s += txt(cx, 480, 'Righting moment = Δ × GZ   ·   มุมเล็ก: GZ ≈ GM × sin θ', 13, 'middle', '#0f172a', True)
    s += txt(250, 480, 'GM = KM − KG   ·   KM = KB + BM   ·   BM = I ÷ V', 13, 'middle', '#0f172a', True)
    s += txt(500, 505, 'M อยู่เหนือ G → เสถียร (stable) · M ตรงกับ G → เป็นกลาง (neutral) · M ต่ำกว่า G → ไม่เสถียร (unstable)', 12, 'middle', '#334155')
    save('stab-bgm.svg', s)


# ---------------------------------------------------------------- GZ curve
def gz_curve():
    w, h = 1000, 560
    s = head(w, h, 'กราฟแขนตั้งตรง (GZ curve) กับเกณฑ์ IMO Intact Stability Code 2008 (ตัวอย่าง)')
    gx, gy, gw, gh = 90, 80, 560, 380
    X = lambda a: gx + a / 80 * gw
    Y = lambda v: gy + gh - (v + 0.6) / 2.6 * gh
    # area shading 0-30, 30-40
    pts = [(X(0), Y(0))] + [(X(a / 2), Y(gz(a / 2))) for a in range(0, 61)] + [(X(30), Y(0))]
    s += '<polygon points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts) + '" fill="#bfdbfe" opacity="0.8"/>'
    pts = [(X(30), Y(0))] + [(X(30 + a / 2), Y(gz(30 + a / 2))) for a in range(0, 21)] + [(X(40), Y(0))]
    s += '<polygon points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts) + '" fill="#bbf7d0" opacity="0.9"/>'
    # axes
    s += line(gx, Y(0), gx + gw, Y(0), '#0f172a', 1.5) + line(gx, gy, gx, gy + gh, '#0f172a', 1.5)
    for a in range(0, 81, 10):
        s += line(X(a), Y(0), X(a), Y(0) + 5, '#0f172a', 1) + txt(X(a), Y(0) + 20, f'{a}°', 11, 'middle')
    for v in (-0.5, 0, 0.5, 1.0, 1.5, 2.0):
        s += line(gx - 5, Y(v), gx, Y(v), '#0f172a', 1) + txt(gx - 8, Y(v) + 4, f'{v:.1f}', 11, 'end')
    s += f'<text x="{gx-50}" y="{gy+gh/2}" font-size="12" text-anchor="middle" transform="rotate(-90 {gx-50} {gy+gh/2})">GZ (m)</text>'
    s += txt(gx + gw / 2, gy + gh + 40, 'มุมเอียง θ', 12, 'middle')
    curve = [(X(a / 2), Y(gz(a / 2))) for a in range(0, 161)]
    s += '<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in curve) + '" fill="none" stroke="#b91c1c" stroke-width="3.5"/>'
    # GM tangent at 57.3 deg
    gm = KM - KGF
    s += line(X(0), Y(0), X(57.3), Y(gm), '#475569', 1.5, '6 4')
    s += line(X(57.3), Y(0), X(57.3), Y(gm), '#475569', 1.2, '3 3')
    s += txt(X(57.3) + 6, Y(gm) + 4, f'GM = {gm:.2f} m ที่ 57.3° (1 rad)', 11.5, 'start', '#334155', True)
    # max GZ
    mx = max(range(0, 161), key=lambda a: gz(a / 2)) / 2
    s += f'<circle cx="{X(mx):.1f}" cy="{Y(gz(mx)):.1f}" r="5" fill="#b91c1c"/>' + txt(X(mx), Y(gz(mx)) - 12, f'GZ สูงสุด ≈ {gz(mx):.2f} m ที่ ≈ {mx:.0f}°', 12, 'middle', '#b91c1c', True)
    # vanishing angle
    avs = next(a / 2 for a in range(100, 161) if gz(a / 2) <= 0)
    s += f'<circle cx="{X(avs):.1f}" cy="{Y(0):.1f}" r="5" fill="#0f172a"/>' + txt(X(avs) + 6, Y(0) + 38, f'↑ มุมหมดเสถียรภาพ (AVS) ≈ {avs:.0f}°', 11.5, 'end', '#0f172a', True)
    s += txt(X(15), Y(0.12), 'A₀₋₃₀', 12, 'middle', '#1e3a8a', True) + txt(X(35), Y(0.4), 'A₃₀₋₄₀', 12, 'middle', '#14532d', True)
    # criteria box
    def area(a0, a1):
        n = 200; hh = (a1 - a0) / n; acc = gz(a0) + gz(a1)
        for i in range(1, n):
            acc += (4 if i % 2 else 2) * gz(a0 + i * hh)
        return acc * hh / 3 * math.pi / 180
    rows = [('พื้นที่ 0–30°', '≥ 0.055 m·rad', f'{area(0,30):.3f}'), ('พื้นที่ 0–40° (หรือ θf)', '≥ 0.090 m·rad', f'{area(0,40):.3f}'),
            ('พื้นที่ 30–40° (หรือ θf)', '≥ 0.030 m·rad', f'{area(30,40):.3f}'), ('GZ ที่มุม ≥ 30°', '≥ 0.20 m', f'{gz(30):.2f}'),
            ('มุมที่ GZ สูงสุด', '≥ 25°', f'{mx:.0f}°'), ('GM₀ (แก้ FSE แล้ว)', '≥ 0.15 m', f'{gm:.2f}')]
    bx = 680
    s += rect(bx, 70, 300, 300, '#f8fafc', '#94a3b8', 1, 10)
    s += txt(bx + 14, 94, 'เกณฑ์ทั่วไป (IS Code Part A 2.2)', 13, 'start', '#0f172a', True)
    s += txt(bx + 14, 114, 'เกณฑ์', 11.5, 'start', '#475569', True) + txt(bx + 170, 114, 'ต้องได้', 11.5, 'start', '#475569', True) + txt(bx + 250, 114, 'ตัวอย่าง', 11.5, 'start', '#475569', True)
    for i, (a, b, c) in enumerate(rows):
        y = 140 + i * 36
        s += txt(bx + 14, y, a, 12) + txt(bx + 170, y, b, 11.5) + txt(bx + 250, y, c + ' ✔', 12, 'start', '#15803d', True)
    s += rect(bx, 385, 300, 145, '#fff7ed', '#c2410c', 1, 10)
    for i, t in enumerate(['นอกจากนี้ต้องผ่าน weather criterion', '(ลมแรงด้านข้างร่วมกับการโคลง) และเกณฑ์', 'เฉพาะประเภท (grain, timber, container',
                           'ฯลฯ) — ข้อมูลในภาพคือสภาพสมมุติ', 'Δ 31,000 t, KG (fluid) 10.21 m', 'ไม่ใช่ข้อมูลเรือจริง']):
        s += txt(bx + 14, 408 + i * 20, t, 12, 'start', '#7c2d12')
    save('stab-gz-curve.svg', s)


# ---------------------------------------------------------------- free surface
def free_surface():
    w, h = 1000, 470
    s = head(w, h, 'ผลของผิวน้ำอิสระ (Free surface effect) และการแบ่งถังตามยาว')
    for k, (cx, sub, title) in enumerate(((200, 1, 'ถังไม่แบ่ง: ของเหลวไหลไปด้านต่ำ'), (520, 2, 'แบ่งกลาง 2 ช่อง: FSE เหลือ 1/4'))):
        s += txt(cx, 70, title, 14, 'middle', bold=True)
        s += rect(cx - 130, 100, 260, 140, '#fff', '#0f172a', 2.5)
        if sub == 1:
            s += f'<polygon points="{cx-128},{150+30} {cx+128},{150-30} {cx+128},238 {cx-128},238" fill="#38bdf8" opacity="0.7"/>'
            s += line(cx - 60, 205, cx + 60, 190, '#0f172a', 2, mk='ar')
        else:
            s += line(cx, 100, cx, 240, '#0f172a', 3)
            for off in (-65, 65):
                s += f'<polygon points="{cx+off-63},{150+15} {cx+off+63},{150-15} {cx+off+63},238 {cx+off-63},238" fill="#38bdf8" opacity="0.7"/>'
        s += txt(cx, 262, 'มุมเอียงเล็กน้อย → ผิวน้ำยังขนานพื้นโลก', 11, 'middle', '#334155')
    # G Gv diagram
    cx = 830
    s += txt(cx, 70, 'ผลต่อ G', 14, 'middle', bold=True)
    s += line(cx, 90, cx, 260, '#94a3b8', 1, '4 3')
    s += dot(cx, 120, 'M', '#15803d', 'start', 12) + dot(cx, 200, 'G (solid)', '#b91c1c', 'start', 12) + dot(cx, 165, 'Gv (virtual)', '#c2410c', 'start', 12)
    s += line(cx - 30, 200, cx - 30, 165, '#c2410c', 2, mk='ar') + txt(cx - 36, 186, 'FSC', 12, 'end', '#c2410c', True)
    s += txt(cx, 285, 'GM (fluid) = GM (solid) − FSC', 12, 'middle', '#0f172a', True)
    s += rect(40, 310, 920, 140, '#f8fafc', '#94a3b8', 1, 10)
    L = ['FSM (t·m) = i × ρ  โดย i = l × b³ ÷ 12 (ถังสี่เหลี่ยม: l ความยาวถัง, b ความกว้างถัง, ρ ความหนาแน่นของเหลวในถัง)  ·  FSC = ΣFSM ÷ Δ',
         'ตัวอย่าง: ถัง 20 × 12 m น้ำทะเล → i = 2,880 m⁴, FSM ≈ 2,952 t·m, Δ 31,000 t → FSC ≈ 0.095 m  ·  แบ่งกลางเป็น 2 ช่อง → FSM ≈ 738 t·m (1/4)',
         'แบ่ง n ช่องเท่ากันตามยาว → FSE ลดเหลือ 1/n² · FSE ไม่ขึ้นกับปริมาณของเหลว (ถ้ายังมีผิวอิสระ) และไม่ขึ้นกับตำแหน่งถังในเรือ',
         'ลดผล: ถังเต็ม (pressed up) หรือว่างจริง · หลีกเลี่ยงถังหย่อนหลายถังพร้อมกัน · ระวังน้ำดับเพลิง/น้ำเข้าเรือที่สะสมบนดาดฟ้า']
    for i, l in enumerate(L):
        s += txt(56, 338 + i * 28, l, 12.3, 'start', '#0f172a', i == 0)
    save('stab-free-surface.svg', s)


# ---------------------------------------------------------------- list vs loll
def list_loll():
    w, h = 1000, 590
    s = head(w, h, 'เรือเอียงเพราะ G ไม่อยู่กลางลำ (List) กับ เรือเอียงเพราะ GM ติดลบ (Loll)')
    for k, (cx, title, col) in enumerate(((250, 'LIST — G เยื้องไปด้านหนึ่ง, GM เป็นบวก', '#1d4ed8'), (750, 'LOLL — GM ติดลบเมื่อตั้งตรง', '#b91c1c'))):
        wl, keel = 260, 400
        ang = 6 if k == 0 else 10
        s += txt(cx, 66, title, 14.5, 'middle', col, True)
        s += f'<g transform="rotate({ang} {cx} {wl})">'
        s += f'<path d="M {cx-140} 140 L {cx+140} 140 L {cx+140} {keel-30} Q {cx+140} {keel} {cx+110} {keel} L {cx-110} {keel} Q {cx-140} {keel} {cx-140} {keel-30} Z" fill="#e2e8f0" stroke="#0f172a" stroke-width="2.5"/>'
        s += line(cx, 120, cx, keel, '#94a3b8', 1, '4 3')
        if k == 0:
            s += dot(cx + 22, 235, 'G₁', '#b91c1c', 'start', 10) + dot(cx, 190, 'M', '#15803d', 'start', 10)
        else:
            s += dot(cx, 215, 'G', '#b91c1c', 'start', 10) + dot(cx, 238, 'M', '#15803d', 'start', 10)
        s += '</g>'
        s += f'<rect x="{cx-190}" y="{wl}" width="380" height="170" fill="#bae6fd" opacity="0.45"/>' + line(cx - 190, wl, cx + 190, wl, '#0284c7', 2)
    A = ['สาเหตุ: น้ำหนักไม่สมดุลซ้าย-ขวา (สินค้า ถังน้ำ/น้ำมัน)', 'เอียงไปด้านเดียวคงที่ ตั้งตรงได้ถ้าย้ายน้ำหนักกลับ', 'tan θ = GG₁ ÷ GM',
         'แก้: ถ่ายน้ำหนัก/ballast ไปด้านที่สูง']
    B = ['สาเหตุ: G สูงเกิน M (ของบนดาดฟ้า ใช้น้ำมันถังล่าง', 'FSE มาก น้ำแข็งเกาะ) — ตั้งตรงไม่ได้ เอียงไปข้างใด', 'ข้างหนึ่งแล้วอาจ "พลิก" ไปอีกข้าง (flop) · โคลงช้า เฉื่อย',
         'tan θ = √(2 × |GM| ÷ BM) (ผนังตรง) · GM ที่มุม loll ≈ 2|GM| ÷ cos θ', 'แก้: ลด G — เติมถังล่างที่ "ด้านต่ำก่อน" แบบถังแบ่ง', 'หรือถังกลางลำ ลด FSE ยกของหนักบนลง',
         'ห้าม: เติม ballast ด้านที่สูงเพื่อ "แก้เอียง" — อาจพลิกแรง']
    for i, a in enumerate(A):
        s += txt(60, 470 + i * 24, a, 12.5, 'start', '#1e3a8a', i == 3)
    for i, b in enumerate(B):
        s += txt(520, 456 + i * 19, b, 12, 'start', '#7f1d1d', i in (4, 6))
    save('stab-list-loll.svg', s)


# ---------------------------------------------------------------- trim
def trim():
    w, h = 1000, 470
    s = head(w, h, 'การคำนวณ trim เมื่อบรรทุกน้ำหนักเพิ่ม (ตัวอย่างจำลอง)')
    x0, x1, wl = 80, 900, 230
    s += f'<path d="M {x0} 150 L {x1} 150 L {x1+40} 200 L {x1} 300 L {x0+30} 300 Q {x0} 290 {x0} 250 Z" fill="#e2e8f0" stroke="#0f172a" stroke-width="2"/>'
    s += line(x0 - 20, wl, x1 + 60, wl, '#0284c7', 2) + txt(x0 - 16, wl - 6, 'WL เดิม', 11, 'start', '#0284c7')
    # new waterline (trim by head)
    s += line(x0 - 20, wl + 10, x1 + 60, wl - 16, '#b91c1c', 2, '8 4') + txt(x0 - 16, wl + 26, 'WL ใหม่ (trim by head)', 11, 'start', '#b91c1c', True)
    mid = (x0 + x1) / 2
    lcf = mid - 15
    s += line(mid, 140, mid, 310, '#94a3b8', 1, '4 3') + txt(mid, 132, '⊗ กลางลำ', 11, 'middle', '#475569')
    s += f'<circle cx="{lcf}" cy="{wl}" r="6" fill="#15803d"/>' + txt(lcf - 8, wl + 22, 'LCF (3.0 m ท้ายกลางลำ)', 11.5, 'end', '#15803d', True)
    lx = mid + 50 / 81 * (x1 - mid)
    s += rect(lx - 25, 115, 50, 35, '#fde68a', '#92400e', 1.5) + txt(lx, 137, '400 t', 12, 'middle', '#78350f', True)
    s += line(lcf, 330, lx, 330, '#b91c1c', 1.5, mk='arR') + txt((lcf + lx) / 2, 348, 'ระยะจาก LCF = 53 m', 12, 'middle', '#b91c1c', True)
    s += txt(x0, 320, 'AP', 12, 'middle', '#0f172a', True) + txt(x1, 320, 'FP', 12, 'middle', '#0f172a', True)
    s += rect(40, 365, 920, 95, '#f8fafc', '#94a3b8', 1, 10)
    L = ['ข้อมูล: LBP 162 m · TPC 42 t/cm · MCTC 380 t·m/cm · draught เดิม F 9.40 m A 9.80 m · บรรทุก 400 t ที่ 50 m หน้ากลางลำ',
         '1) Sinkage = 400 ÷ 42 = 9.5 cm  ·  2) Change of trim = 400 × 53 ÷ 380 = 55.8 cm (by head)',
         '3) แบ่งตามระยะ LCF: ท้าย = 55.8 × 78 ÷ 162 = 26.9 cm (ลด) · หัว = 55.8 − 26.9 = 28.9 cm (เพิ่ม)',
         '4) Draught ใหม่: F = 9.40 + 0.095 + 0.289 = 9.78 m · A = 9.80 + 0.095 − 0.269 = 9.63 m']
    for i, l in enumerate(L):
        s += txt(56, 388 + i * 21, l, 12.3, 'start', '#0f172a', i == 3)
    save('stab-trim.svg', s)


# ---------------------------------------------------------------- bilging
def bilging():
    w, h = 1000, 470
    s = head(w, h, 'การสูญเสียแรงลอยตัวบางส่วน (Bilging) — วิธี lost buoyancy (เรือรูปกล่องตัวอย่าง)')
    x0, x1, top, bot = 80, 600, 120, 300
    wl0, wl1 = 200, 200 - 27
    s += rect(x0, top, x1 - x0, bot - top, '#e2e8f0', '#0f172a', 2.5)
    cx0, cx1 = 304, 376
    s += rect(cx0, top, cx1 - cx0, bot - top, '#38bdf8', '#0f172a', 2.5)
    s += txt((cx0 + cx1) / 2, top - 8, 'ช่องที่น้ำเข้า l = 12 m', 12, 'middle', '#075985', True)
    s += line(x0 - 30, wl0, x1 + 30, wl0, '#0284c7', 2) + txt(x1 + 34, wl0 + 4, 'WL เดิม 6.00 m', 11.5, 'start', '#0284c7')
    s += line(x0 - 30, wl1, x1 + 30, wl1, '#b91c1c', 2, '8 4') + txt(x1 + 34, wl1 + 4, 'WL ใหม่ 6.82 m', 11.5, 'start', '#b91c1c', True)
    s += line(x0 - 15, wl0, x0 - 15, wl1, '#b91c1c', 2, mk='arR') + txt(x0 - 20, (wl0 + wl1) / 2 + 4, 'sinkage', 11, 'end', '#b91c1c', True)
    s += f'<path d="M 340 306 l 12 22 l -24 0 z" fill="#b91c1c"/>' + txt(358, 324, 'รูรั่ว', 11, 'start', '#b91c1c')
    s += txt((x0 + x1) / 2, bot + 56, 'เรือรูปกล่อง L 100 m × B 15 m × T 6 m', 12, 'middle', '#334155')
    s += rect(40, 380, 920, 80, '#f8fafc', '#94a3b8', 1, 10)
    L = ['Sinkage = ปริมาตรแรงลอยตัวที่เสีย ÷ พื้นที่ระนาบน้ำที่เหลือ = (μ × l × B × T) ÷ (L × B − μ × l × B)',
         'ช่องว่าง μ = 1.0 → 1,080 ÷ 1,320 = 0.82 m (draught 6.82 m)  ·  ช่องมีสินค้า μ = 0.6 → 648 ÷ 1,392 = 0.47 m',
         'μ (permeability) = สัดส่วนปริมาตรที่น้ำเข้าได้ — ห้องว่าง/ที่พัก ~0.95, ห้องเครื่อง ~0.85, เก็บของ ~0.60 (ค่าตาม SOLAS ใช้ในการคำนวณออกแบบ)']
    for i, l in enumerate(L):
        s += txt(56, 404 + i * 22, l, 12.3, 'start', '#0f172a', i == 0)
    # side effect box
    bx = 745
    s += rect(bx, 60, 230, 300, '#fef2f2', '#b91c1c', 1.5, 10)
    E = ['ผลที่ตามมา', '• จม (sinkage) — freeboard ลด', '• Trim ถ้าช่องไม่อยู่กลางลำ', '• List ถ้าน้ำเข้าไม่สมมาตร',
         '• GM เปลี่ยน (เพิ่มหรือลดได้)', '• Free surface ของน้ำที่เข้า', '  (ช่องไม่เต็มหรือไม่เปิดถึงทะเล)', '• ช่องเปิดจมน้ำ → น้ำลาม',
         '  (progressive flooding)', '• ความแข็งแรงตามยาวเปลี่ยน']
    for i, e in enumerate(E):
        s += txt(bx + 14, 86 + i * 27, e, 12.3, 'start', '#7f1d1d', i == 0)
    save('stab-bilging.svg', s)


# ---------------------------------------------------------------- load line
def load_line():
    # วาดตามมาตราส่วนจริงของ LL 1966 Reg. 4–7 (k px ต่อ mm) ยกเว้นระยะ summer freeboard ซึ่งตัดช่วง (ไม่ตามมาตราส่วน)
    w, h = 1100, 560
    s = head(w, h, 'เครื่องหมายแนวน้ำบรรทุก (Load line mark) และ Deck line — ขนาดตาม Load Line Convention')
    k = 0.45
    lw = 25 * k                      # ความกว้างเส้น 25 mm
    cx, cy = 250, 330                # ศูนย์กลางวงกลม (ขอบบนเส้น S อยู่ที่ระดับนี้)
    ink = '#0f172a'
    grey = '#475569'
    # deck line 300 x 25 mm (กลางลำ เหนือศูนย์กลางวงกลม)
    yd = 92
    s += rect(cx - 150 * k, yd, 300 * k, lw, ink, ink, 0)
    s += txt(cx, yd - 8, 'Deck line 300 × 25 mm', 12, 'middle', ink, True)
    # summer freeboard (ตัดช่วง)
    s += line(cx, yd + lw + 2, cx, 150, grey, 1, '3 3') + line(cx, 175, cx, cy - 6, grey, 1, '3 3')
    s += f'<path d="M {cx-12} 152 l 24 -6 M {cx-12} 172 l 24 -6" stroke="{grey}" stroke-width="1.5" fill="none"/>'
    s += txt(cx - 18, 140, 'Summer freeboard ที่กำหนด', 11, 'end', grey)
    s += txt(cx - 18, 156, '(ขอบบน deck line ถึงขอบบน', 11, 'end', grey)
    s += txt(cx - 18, 172, 'เส้นผ่ากลางวงกลม — ไม่ตามมาตราส่วน)', 11, 'end', grey)
    # ring OD 300 mm, width 25 mm + horizontal line 450 x 25 mm (ขอบบนผ่านศูนย์กลาง)
    ro = 150 * k
    s += f'<circle cx="{cx}" cy="{cy}" r="{ro - lw / 2:.2f}" fill="none" stroke="{ink}" stroke-width="{lw:.2f}"/>'
    s += rect(cx - 225 * k, cy, 450 * k, lw, ink, ink, 0)
    # อักษรย่อหน่วยงาน ~115 x 75 mm วางสองข้างวงกลมเหนือเส้น
    for sx in (-1, 1):
        s += txt(cx + sx * (150 + 37.5) * k, cy - 4, 'X', 44, 'middle', ink, True)
    # vertical line 25 mm wide, 540 mm forward of ring centre (หัวเรืออยู่ทางขวาของภาพ)
    vx = cx + 540 * k
    T48 = 200      # 1/48 ของ summer draught 9.60 m = 200 mm (ตัวอย่าง)
    FWA = 185      # Δ 31,000 t ÷ (4 × 42) ≈ 185 mm (ตัวอย่าง)
    marks = [('S', 0, 1, ''), ('T', T48, 1, 'S+1/48'), ('W', -T48, 1, 'S−1/48'),
             ('WNA', -T48 - 50, 1, 'W−50 mm'), ('F', FWA, -1, 'S + FWA'), ('TF', T48 + FWA, -1, 'T + FWA')]
    top = cy - (T48 + FWA) * k
    bot = cy + (T48 + 50) * k + lw
    s += rect(vx - lw / 2, top, lw, bot - top, ink, ink, 0)
    for lab, up, side, note in marks:
        y = cy - up * k
        col = '#b91c1c' if lab in ('F', 'TF') else ink
        if side == 1:
            x2 = vx + lw / 2 + 230 * k
            s += rect(vx + lw / 2, y, 230 * k, lw, col, col, 0) + txt(x2 + 8, y + 11, lab, 15, 'start', col, True)
            s += txt(x2 + (50 if lab == 'WNA' else 30), y + 10, note, 10.5, 'start', grey)
        else:
            x2 = vx - lw / 2 - 230 * k
            s += rect(x2, y, 230 * k, lw, col, col, 0) + txt(x2 - 8, y + 11, lab, 15, 'end', col, True)
            s += txt(x2 - 36, y + 10, note, 10.5, 'end', grey)
    # dimension notes
    s += line(cx - 225 * k, cy + 86, cx + 225 * k, cy + 86, '#64748b', 1) + txt(cx, cy + 102, 'เส้นผ่าวงกลม 450 mm · วงกลม Ø นอก 300 mm', 10.5, 'middle', grey)
    s += line(cx, cy + 118, vx, cy + 118, '#64748b', 1, mk='ar') + txt((cx + vx) / 2, cy + 134, '540 mm (ศูนย์กลางวงกลม → เส้นตั้ง)', 10.5, 'middle', grey)
    s += txt(vx + lw / 2 + 115 * k, cy + 160, '← เส้นแนวน้ำยาว 230 mm →', 10.5, 'middle', grey)
    s += txt(330, h - 20, '← ท้ายเรือ · หัวเรือ →   (ภาพด้านขวาของเรือ · มาตราส่วน 0.45 px ต่อ mm)', 10.5, 'middle', grey)
    # คำอธิบาย
    bx = 712
    s += rect(bx, 54, 376, 490, '#f8fafc', '#94a3b8', 1, 10)
    L = ['ความหมาย (LL 1966/1988 Reg. 4–8, 40)', 'S — Summer: ขอบบนเสมอขอบบนเส้นผ่าวงกลม', 'T — Tropical: สูงกว่า S = 1/48 summer draught',
         'W — Winter: ต่ำกว่า S = 1/48 summer draught', 'WNA — ต่ำกว่า W 50 mm (เรือยาว ≤ 100 m)', 'F — Fresh: สูงกว่า S = FWA (อยู่ท้ายเส้นตั้ง)',
         'TF — Tropical fresh: สูงกว่า T = FWA', 'FWA (mm) = Δ ÷ (4 × TPC)', 'DWA = FWA × (1025 − ρ) ÷ 25', '',
         'ขนาด (ทุกเส้นกว้าง 25 mm)', '• Deck line ยาว 300 mm ที่กลางลำ', '• วงกลม Ø นอก 300 mm, เส้นผ่ากลางยาว 450 mm', '• เส้นแนวน้ำยาว 230 mm ออกจากเส้นตั้งที่อยู่',
         '  ห่างศูนย์กลางวงกลม 540 mm ไปทางหัวเรือ', '• อักษรย่อหน่วยงานที่กำหนด freeboard ~115×75 mm', '• ขาว/เหลืองบนพื้นเข้ม หรือดำบนพื้นสว่าง + ทำถาวร', '',
         'ตัวอย่าง (สมมุติ): summer draught 9.60 m', '→ 1/48 = 200 mm · Δ 31,000 t, TPC 42 → FWA ≈ 185 mm']
    for i, l in enumerate(L):
        s += txt(bx + 14, 78 + i * 23.3, l, 12, 'start', '#0f172a', i in (0, 10, 18))
    save('stab-load-line.svg', s)


# ---------------------------------------------------------------- watertight integrity
def watertight():
    w, h = 1000, 520
    s = head(w, h, 'ความผนึกน้ำ (Watertight integrity): ผนังกั้นน้ำ ช่องเปิด และจุดที่น้ำอาจไหลเข้า')
    s += '<path d="M 60 300 L 120 360 L 860 360 L 930 290 L 940 200 L 120 200 L 60 230 Z" fill="#e2e8f0" stroke="#0f172a" stroke-width="2.5"/>'
    s += line(20, 300, 980, 300, '#0284c7', 1.8, '8 5') + txt(24, 294, 'แนวน้ำ', 11, 'start', '#0284c7')
    s += rect(80, 120, 110, 80, '#cbd5e1', '#0f172a', 2)
    for x, lab in ((150, 'Aft peak bhd'), (250, 'E/R bhd'), (420, ''), (590, ''), (760, ''), (860, 'Collision bhd')):
        s += line(x, 200, x, 360, '#b91c1c', 4)
        if lab:
            s += txt(x, 380, lab, 11, 'middle', '#b91c1c', True)
    s += rect(243, 320, 14, 30, '#facc15', '#854d0e', 1.5) + txt(250, 400, 'ประตูกันน้ำ (WT door)', 11, 'middle', '#854d0e', True)
    for x in (300, 470, 640):
        s += rect(x, 185, 110, 15, '#94a3b8', '#0f172a', 1.5)
    s += txt(525, 175, 'ฝาระวาง (weathertight)', 11.5, 'middle', '#0f172a', True)
    for x in (880, 905):
        s += line(x, 200, x, 170, '#0f172a', 3) + f'<circle cx="{x}" cy="166" r="5" fill="#0f172a"/>'
    s += txt(895, 150, 'ท่ออากาศ/ช่องระบาย', 11, 'middle', '#0f172a', True)
    s += rect(170, 140, 16, 20, '#fff', '#0f172a', 1.5) + txt(200, 112, 'ประตูภายนอก/ช่องหน้าต่าง (weathertight)', 11, 'start', '#0f172a')
    for x in (330, 520, 700):
        s += f'<circle cx="{x}" cy="345" r="5" fill="#0369a1"/>'
    s += txt(520, 395, '● sea valves / overboard discharges — ต้องปิดได้จริง เปิดเฉพาะเมื่อใช้', 11, 'middle', '#0369a1', True)
    s += rect(40, 420, 920, 90, '#f8fafc', '#94a3b8', 1, 10)
    L = ['Watertight = กันน้ำได้ทั้งสองทิศภายใต้แรงดันน้ำที่ออกแบบ (ผนังกั้นน้ำ ประตูกันน้ำ) · Weathertight = กันน้ำเข้าไม่ได้ในสภาพทะเลใด ๆ (ฝาระวาง ประตูภายนอก)',
         'Downflooding point = ช่องเปิดที่ปิดกันน้ำไม่ได้ซึ่งเมื่อจมน้ำแล้วน้ำจะไหลเข้า (กำหนดมุม θf ใน GZ curve)',
         'ก่อนออกเรือและในทะเล: ประตูกันน้ำปิด (ตามที่อนุญาตให้เปิด), ฝาระวาง/manhole/ประตูภายนอกปิดล็อก, ฝา sounding/air pipe อยู่ในสภาพดี, ระบบสัญญาณและไฟแสดงทำงาน',
         'ผนังกั้นที่มีสายไฟ/ท่อผ่านต้องรักษาความผนึกน้ำของจุดผ่าน (transits) — การเจาะ/เดินสายใหม่ต้องได้รับอนุมัติ']
    for i, l in enumerate(L):
        s += txt(56, 442 + i * 20, l, 11.6)
    save('stab-watertight.svg', s)


if __name__ == '__main__':
    bgm(); gz_curve(); free_surface(); list_loll(); trim(); bilging(); load_line(); watertight()
