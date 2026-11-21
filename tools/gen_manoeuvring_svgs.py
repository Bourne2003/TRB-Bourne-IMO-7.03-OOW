"""ภาพประกอบบท 1.9 การบังคับเรือ (Ship manoeuvring and handling)
ตัวเลขในภาพมาจากแบบจำลองอย่างง่าย (Nomoto first-order) ของเรือสมมุติ MV Andaman Pearl ยาว 172 m
ใช้เพื่อการเรียนเท่านั้น ไม่ใช่ข้อมูลทดลองเรือจริง"""
import math, os
R = math.radians
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"


def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker>'
            '<marker id="arB" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#1d4ed8"/></marker>'
            '<marker id="arR" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#b91c1c"/></marker>'
            '<marker id="arG" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#15803d"/></marker>'
            '<marker id="arO" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#c2410c"/></marker></defs>\n'
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


def ship(cx, cy, hdg, L, B, fill='#cbd5e1', stroke='#0f172a', sw=1.5, extra=''):
    """เรือมุมมองจากด้านบน: hdg 0 = ขึ้นบน (เหนือ)"""
    h = R(hdg)
    loc = [(L / 2, 0), (L / 2 - B * 1.1, B / 2), (-L / 2, B / 2), (-L / 2, -B / 2), (L / 2 - B * 1.1, -B / 2)]
    pts = []
    for f, s in loc:
        x = cx + f * math.sin(h) + s * math.cos(h)
        y = cy - f * math.cos(h) + s * math.sin(h)
        pts.append(f'{x:.1f},{y:.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>\n'


def loc2w(cx, cy, hdg, f, s):
    h = R(hdg)
    return cx + f * math.sin(h) + s * math.cos(h), cy - f * math.cos(h) + s * math.sin(h)


# ---------------------------------------------------------------- simulation
def wrap(a):
    return (a + 180) % 360 - 180


def simulate(kind, V0=7.2, Rad=280.0, T=25.0, dt=0.5):
    """kind: 'TC' turning circle, 'W' Williamson, 'S' Scharnow, 'A' Anderson. คืนค่า [(x,y,heading,t)] หน่วยเมตร x=ตะวันออก y=เหนือ"""
    K = (V0 / Rad) / 35.0
    x = y = 0.0; psi = 0.0; r = 0.0; V = V0; t = 0.0; phase = 0; turned = 0.0
    pts = [(0.0, 0.0, 0.0, 0.0)]; events = []
    while t < 900:
        hd = math.degrees(psi) % 360
        d = 35
        if kind == 'TC':
            if t < 20: d = 0  # ช่วงตรงก่อนสั่งหางเสือ (ใช้แสดงจุด wheel over)
            if turned >= 400: break
        elif kind == 'W':
            if phase == 0 and turned >= 60: phase = 1; events.append(('60', x, y))
            if phase == 1: d = -35
            if phase == 1 and turned <= -140: phase = 2; events.append(('200', x, y))
        elif kind == 'S':
            if phase == 0 and turned >= 240: phase = 1; events.append(('240', x, y))
            if phase == 1: d = -35
            if phase == 1 and turned <= 200: phase = 2; events.append(('200', x, y))
        elif kind == 'A':
            if phase == 0 and turned >= 250: phase = 2; events.append(('250', x, y))
        if phase == 2:
            if kind == 'A':
                d = 0
                V = max(0.0, V - 0.035 * dt)
                if V < 0.3: break
            else:
                err = wrap(180 - hd)
                d = max(-35, min(35, 2.0 * err - 40 * math.degrees(r)))
                if y < min(events[-1][2] - 350, -150): break
        if not (kind == 'A' and phase == 2):
            V += ((V0 * (1 - 0.35 * min(1, abs(math.degrees(r)) / 1.4))) - V) * dt / 60
        r += (K * (V / V0) * d - r) * dt / T * (V / V0)
        psi += r * dt; turned += math.degrees(r * dt)
        x += V * math.sin(psi) * dt; y += V * math.cos(psi) * dt
        t += dt
        pts.append((x, y, math.degrees(psi) % 360, t))
    return pts, events


# ---------------------------------------------------------------- 1 turning circle
def turning_circle():
    w, h = 1000, 690
    s = head(w, h, 'องค์ประกอบของวงเลี้ยว (Turning circle) — หางเสือ 35° ขวา')
    pts, _ = simulate('TC')
    sc = 0.55; ox, oy = 200, 545
    P = lambda x, y: (ox + x * sc, oy - y * sc)
    t0 = next(p for p in pts if p[3] >= 20)

    def at_turn(deg):
        acc = 0; prev = pts[0][2]
        for p in pts:
            acc += wrap(p[2] - prev); prev = p[2]
            if acc >= deg: return p
    p90, p180 = at_turn(90), at_turn(180)
    poly = ' '.join(f'{P(a, b)[0]:.1f},{P(a, b)[1]:.1f}' for a, b, _, _ in pts)
    s += f'<polyline points="{poly}" fill="none" stroke="#1d4ed8" stroke-width="3"/>\n'
    x0, y0 = P(0, -150); x1, y1 = P(0, 850)
    s += line(x0, y0, x1, y1, '#64748b', 1.5, '6 5')
    s += txt(x0 - 6, y0 - 4, 'เข็มเดิม (original course)', 12, 'end', '#475569')
    wx, wy = P(t0[0], t0[1])
    s += f'<circle cx="{wx:.1f}" cy="{wy:.1f}" r="6" fill="#b91c1c"/>' + txt(wx - 12, wy + 22, 'Wheel over', 12, 'end', '#b91c1c', True)
    s += txt(wx - 12, wy + 38, '(จุดสั่งหางเสือ)', 11, 'end', '#b91c1c')
    # advance
    ax, ay = P(p90[0], p90[1])
    s += f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="5" fill="#0f172a"/>'
    s += line(wx - 70, wy, wx - 70, ay, '#b91c1c', 2, mk='arR') + line(wx - 70, ay, wx - 70, wy, '#b91c1c', 2, mk='arR')
    s += line(wx - 78, ay, ax, ay, '#94a3b8', 1, '3 3')
    adv = p90[1] - t0[1]
    s += txt(wx - 78, (wy + ay) / 2, 'Advance', 14, 'end', '#b91c1c', True)
    s += txt(wx - 78, (wy + ay) / 2 + 18, f'{adv:.0f} m ≈ {adv/172:.1f} L', 12, 'end', '#b91c1c')
    # transfer (above the 90° point)
    yT = ay - 45
    s += line(wx, yT, ax, yT, '#15803d', 2, mk='arG') + line(ax, yT, wx, yT, '#15803d', 2, mk='arG')
    s += line(ax, ay, ax, yT - 6, '#94a3b8', 1, '3 3')
    s += txt((wx + ax) / 2, yT - 8, f'Transfer {p90[0]:.0f} m ≈ {p90[0]/172:.1f} L', 13, 'middle', '#15803d', True)
    s += txt(ax + 10, ay - 8, 'หัวเรือเปลี่ยน 90°', 12, 'start')
    # tactical diameter (below the circle)
    tx, ty = P(p180[0], p180[1])
    s += f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="5" fill="#0f172a"/>' + txt(tx + 10, ty + 4, 'หัวเรือเปลี่ยน 180°', 12)
    ymin = min(b for a, b, _, _ in pts)
    yD = P(0, ymin)[1] + 30
    s += line(wx, yD, tx, yD, '#c2410c', 2, mk='arO') + line(tx, yD, wx, yD, '#c2410c', 2, mk='arO')
    s += line(tx, ty, tx, yD + 6, '#94a3b8', 1, '3 3')
    s += txt((wx + tx) / 2, yD + 22, f'Tactical diameter {p180[0]:.0f} m ≈ {p180[0]/172:.1f} L', 13, 'middle', '#c2410c', True)
    tail = [p for p in pts if p[3] > 200]
    fd = max(a for a, b, _, _ in tail) - min(a for a, b, _, _ in tail)
    # silhouettes: early (kick) and near 90° (drift angle)
    pk = next(q for q in pts if q[3] >= 32)
    X, Y = P(pk[0], pk[1])
    s += ship(X, Y, pk[2] + 6, 172 * sc, 27 * sc, '#e2e8f0')
    sx_, sy_ = loc2w(X, Y, pk[2] + 6, -172 * sc / 2, -27 * sc / 2)
    s += line(sx_ - 4, sy_ + 2, sx_ - 22, sy_ + 8, '#7c2d12', 2, mk='ar')
    s += txt(X + 70, Y - 10, 'Kick — ช่วงแรกท้ายเรือปัดออก', 11.5, 'start', '#7c2d12', True)
    s += txt(X + 70, Y + 6, 'ไปด้านตรงข้ามกับทิศเลี้ยว', 11.5, 'start', '#7c2d12')
    s += txt(X + 70, Y + 22, '(ใช้เหวี่ยงท้ายหนีคน/สิ่งของในน้ำ)', 11.5, 'start', '#7c2d12')
    pd = next(q for q in pts if q[3] >= 70)
    X, Y = P(pd[0], pd[1])
    s += ship(X, Y, pd[2] + 12, 172 * sc, 27 * sc, '#e2e8f0')
    s += txt(X + 40, Y + 60, 'Drift angle — มุมระหว่างแนวหัวเรือ', 11.5, 'start', '#7c2d12', True)
    s += txt(X + 40, Y + 76, 'กับทิศทางเดินจริงของเรือขณะเลี้ยว', 11.5, 'start', '#7c2d12')
    s += txt(X + 40, Y + 92, '(หัวเรืออยู่ "ใน" วง ท้ายกวาดออกนอกวง)', 11.5, 'start', '#7c2d12')
    bx, by = 640, 120
    s += f'<rect x="{bx}" y="{by}" width="345" height="300" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    lines = ['เกณฑ์ IMO MSC.137(76) (เรือยาว ≥ 100 m):',
             '• Advance ไม่เกิน 4.5 L',
             '• Tactical diameter ไม่เกิน 5 L',
             '• Initial turning: หางเสือ 10° หัวเรือเปลี่ยน',
             '  10° ภายในระยะไม่เกิน 2.5 L',
             '• Stopping (full astern): track reach ไม่เกิน 15 L',
             '  (ผ่อนได้สำหรับเรือใหญ่มาก แต่ไม่เกิน 20 L)',
             'ทดลองที่: บรรทุกเต็ม · even keel · น้ำลึก',
             'ไม่จำกัด · ทะเลสงบ · test speed',
             f'Final (steady) diameter ในภาพ ≈ {fd:.0f} m',
             '',
             'ตัวเลขในภาพ: แบบจำลองอย่างง่ายของเรือสมมุติ',
             '172 m ที่ 14 kn ในน้ำลึก — ไม่ใช่ข้อมูลเรือจริง']
    for i, l in enumerate(lines):
        s += txt(bx + 14, by + 26 + i * 21, l, 12.5 if i else 13, bold=(i == 0))
    save('man-turning-circle.svg', s)
    return p90, p180, t0, fd


# ---------------------------------------------------------------- 2 pivot point & wind
def pivot_wind():
    w, h = 1000, 520
    s = head(w, h, 'Pivot point และผลของลมต่อเรือที่มี headway / หยุดนิ่ง / sternway')
    cols = [(170, 'มี headway (เดินหน้า)', 'pivot point ≈ 1/4–1/3 L จากหัว', -0.28),
            (500, 'ไม่มี way (หยุดนิ่ง)', 'แรงต้านด้านข้างกระจายทั้งลำ', 0.0),
            (830, 'มี sternway (ถอยหลัง)', 'pivot point ≈ 1/4 L จากท้าย', 0.28)]
    L = 300
    for cx, t1, t2, pp in cols:
        cy = 260
        s += txt(cx, 70, t1, 15, 'middle', bold=True)
        s += txt(cx, 90, t2, 12, 'middle', '#334155')
        s += ship(cx, cy, 0, L, 50, '#e2e8f0')
        s += f'<rect x="{cx-22}" y="{cy+60}" width="44" height="50" fill="#94a3b8" stroke="#0f172a"/>'
        s += txt(cx + 30, cy + 98, 'ที่พัก', 10, 'start', '#334155')
        py = cy + pp * L if pp else cy + 10
        if pp:
            py = cy - (0.5 - (0.28 if pp < 0 else 0.72)) * L * (1)
            py = cy - L / 2 + (0.28 if pp < 0 else 0.75) * L
        s += f'<circle cx="{cx}" cy="{py:.1f}" r="9" fill="#facc15" stroke="#854d0e" stroke-width="2"/>'
        s += txt(cx - 14, py + 4, 'P', 12, 'end', '#854d0e', True)
        # centre of windage (W) ใกล้กลางลำค่อนท้ายเพราะที่พักอยู่ท้าย
        wy = cy + 25
        s += f'<circle cx="{cx}" cy="{wy}" r="6" fill="#1d4ed8"/>' + txt(cx + 10, wy + 4, 'W', 12, 'start', '#1d4ed8', True)
        # ลมจากซ้าย (beam wind from port)
        for k in (-90, 0, 90):
            s += line(cx - 140, cy + k, cx - 60, cy + k, '#1d4ed8', 2, mk='arB')
        s += txt(cx - 140, cy - 100, 'ลม', 12, 'start', '#1d4ed8', True)
        bowy, sty = cy - L / 2 + 30, cy + L / 2 - 30
        if pp < 0:
            s += line(cx + 70, cy + 40, cx + 70, cy - 40, '#0f172a', 3, mk='ar') + txt(cx + 78, cy, 'headway', 11, 'start')
            s += line(cx + 30, sty, cx + 85, sty, '#b91c1c', 3, mk='arR')
            s += line(cx - 30, bowy, cx - 75, bowy, '#b91c1c', 3, mk='arR')
            s += txt(cx, cy + 205, 'W อยู่ท้าย P ไกล → ท้ายถูกพัดไปใต้ลม', 12, 'middle', '#b91c1c')
            s += txt(cx, cy + 222, 'หัวเรือ "หันเข้าหาลม" (bow seeks the wind)', 12, 'middle', '#b91c1c', True)
        elif pp > 0:
            s += line(cx + 70, cy - 40, cx + 70, cy + 40, '#0f172a', 3, mk='ar') + txt(cx + 78, cy, 'sternway', 11, 'start')
            s += line(cx + 30, bowy, cx + 85, bowy, '#b91c1c', 3, mk='arR')
            s += line(cx - 30, sty, cx - 75, sty, '#b91c1c', 3, mk='arR')
            s += txt(cx, cy + 205, 'W อยู่หน้า P → หัวถูกพัดไปใต้ลม', 12, 'middle', '#b91c1c')
            s += txt(cx, cy + 222, 'ท้ายเรือ "หันเข้าหาลม" (stern seeks the wind)', 12, 'middle', '#b91c1c', True)
        else:
            s += line(cx + 40, cy - 60, cx + 100, cy - 60, '#b91c1c', 3, mk='arR')
            s += line(cx + 40, cy + 60, cx + 100, cy + 60, '#b91c1c', 3, mk='arR')
            s += txt(cx, cy + 205, 'ดริฟต์ไปใต้ลมทั้งลำ ส่วนใหญ่วางตัว', 12, 'middle', '#b91c1c')
            s += txt(cx, cy + 222, 'ขวางลมหรือเฉียง (ขึ้นกับรูปทรง/ที่พัก)', 12, 'middle', '#b91c1c', True)
    s += txt(500, 505, 'P = pivot point (จุดหมุนที่ปรากฏ) · W = จุดศูนย์กลางพื้นที่รับลม (centre of windage) — แนวโน้มจริงขึ้นกับรูปเรือ ระดับกินน้ำ trim และตำแหน่งที่พัก', 12, 'middle', '#334155')
    save('man-pivot-point-wind.svg', s)


# ---------------------------------------------------------------- 3 transverse thrust
def transverse_thrust():
    w, h = 1000, 470
    s = head(w, h, 'แรงผลักด้านข้างของใบจักร (Transverse thrust / paddle-wheel effect)')
    # panel 1: RH propeller viewed from astern
    cx, cy = 170, 220
    s += f'<circle cx="{cx}" cy="{cy}" r="85" fill="#f1f5f9" stroke="#0f172a" stroke-width="2"/>'
    for a in (0, 120, 240):
        x2, y2 = cx + 75 * math.sin(R(a)), cy - 75 * math.cos(R(a))
        s += f'<ellipse cx="{(cx+x2)/2:.1f}" cy="{(cy+y2)/2:.1f}" rx="14" ry="38" transform="rotate({a} {(cx+x2)/2:.1f} {(cy+y2)/2:.1f})" fill="#94a3b8" stroke="#0f172a"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="12" fill="#0f172a"/>'
    s += f'<path d="M {cx+100} {cy-40} A 108 108 0 0 1 {cx+100} {cy+40}" fill="none" stroke="#15803d" stroke-width="3" marker-end="url(#arG)"/>'
    s += txt(cx + 112, cy, 'ahead', 12, 'start', '#15803d', True)
    # astern = ทวนเข็มนาฬิกา (มองจากท้าย): ด้านซ้ายของวงหมุนจากบนลงล่าง
    s += f'<path d="M {cx-100} {cy-40} A 108 108 0 0 0 {cx-100} {cy+40}" fill="none" stroke="#b91c1c" stroke-width="3" marker-end="url(#arR)"/>'
    s += txt(cx - 112, cy, 'astern', 12, 'end', '#b91c1c', True)
    s += txt(cx, 85, 'ใบจักรเวียนขวา (RH FPP) มองจากท้าย', 14, 'middle', bold=True)
    s += txt(cx, 335, 'เดินหน้า: หมุนตามเข็มนาฬิกา', 12, 'middle', '#15803d')
    s += txt(cx, 353, 'ถอยหลัง: หมุนทวนเข็มนาฬิกา', 12, 'middle', '#b91c1c')
    s += txt(cx, 380, 'กราบซ้าย ← · → กราบขวา', 11, 'middle', '#475569')
    # panel 2: effect astern
    cx2, cy2 = 500, 255
    s += txt(cx2, 85, 'สั่งถอยหลัง (astern) ขณะหยุด/ช้า', 14, 'middle', bold=True)
    s += ship(cx2, cy2, 0, 240, 44, '#e2e8f0')
    s += line(cx2 + 10, cy2 + 105, cx2 - 70, cy2 + 105, '#b91c1c', 4, mk='arR')
    s += txt(cx2, cy2 + 140, 'ท้ายปัดไปซ้าย (stern cants to port)', 12.5, 'middle', '#b91c1c', True)
    s += line(cx2 - 10, cy2 - 100, cx2 + 70, cy2 - 100, '#15803d', 3, mk='arG')
    s += txt(cx2 + 78, cy2 - 96, 'หัวหันขวา', 12, 'start', '#15803d', True)
    s += txt(cx2, 418, 'ผลชัดมากเมื่อถอยหลังและความเร็วต่ำ · เดินหน้าก็มี', 12, 'middle')
    s += txt(cx2, 434, 'แต่เล็กกว่ามากและหางเสือแก้ได้', 12, 'middle')
    # panel 3: port side to berthing
    cx3, cy3 = 820, 245
    s += txt(cx3, 85, 'ใช้ประโยชน์: เข้าเทียบกราบซ้าย', 14, 'middle', bold=True)
    s += f'<rect x="{cx3-150}" y="105" width="40" height="300" fill="#a8a29e" stroke="#57534e"/>'
    s += txt(cx3 - 130, 420, 'ท่า', 12, 'middle', '#57534e', True)
    s += ship(cx3 - 45, cy3, -12, 250, 42, '#e2e8f0')
    s += f'<path d="M {cx3-15} {cy3+120} q -30 15 -55 10" fill="none" stroke="#b91c1c" stroke-width="3" marker-end="url(#arR)"/>'
    s += f'<path d="M {cx3-75} {cy3-120} q 30 -10 50 0" fill="none" stroke="#15803d" stroke-width="3" marker-end="url(#arG)"/>'
    for i, t_ in enumerate(['เข้าทำมุมเล็ก', 'สั่งถอยเพื่อหยุด', '→ ท้ายเข้าหาท่า', '→ หัวออก', '= ลำขนานท่า']):
        s += txt(cx3 + 45, cy3 - 40 + i * 18, t_, 12, 'start', '#15803d' if i == 4 else '#0f172a', i == 4)
    s += txt(500, 455, 'CPP: เพลาหมุนทิศเดียวตลอด ทิศ transverse thrust ตอนถอยขึ้นกับทิศหมุนของเพลา — ดูจาก pilot card/wheelhouse poster และลองสังเกตในที่ปลอดภัย', 12, 'middle', '#334155')
    save('man-transverse-thrust.svg', s)


# ---------------------------------------------------------------- 4 stopping
def stopping():
    w, h = 1000, 480
    s = head(w, h, 'ระยะหยุดเรือ (Stopping) — crash stop เทียบ inertia stop (เรือสมมุติ บรรทุกเต็ม น้ำลึก)')
    ox, sc = 70, 0.12  # 1 m = 0.12 px ตามยาว
    # crash stop จาก 19 kn: เส้นทางโค้งไปทางกราบขวา (ลงล่างในภาพเมื่อเรือมุ่งไปทางขวา) — ขยายสเกลด้านข้าง
    y0 = 110
    s += txt(ox, y0 - 18, 'Crash stop (Full ahead → Full astern) จาก 19 kn', 13, 'start', '#b91c1c', True)
    pts = [(ox + 1708 * f * sc, y0 + 70 * f ** 2.4) for f in [i / 100 for i in range(101)]]
    s += '<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts) + '" fill="none" stroke="#b91c1c" stroke-width="5"/>\n'
    ex, ey = pts[-1]
    s += ship(ex + 6, ey + 4, 125, 34, 9, '#fecaca')
    s += txt(ex + 30, ey - 4, '≈ 1,700 m (≈ 10 L, 0.9 nm) · ≈ 6 นาที', 12.5, 'start', '#b91c1c', True)
    s += txt(ex + 30, ey + 14, 'หัวเรือมักปัดไปทางขวา (RH FPP) → เส้นทางเบนไปทางกราบขวา', 12, 'start', '#b91c1c')
    s += txt(ex + 30, ey + 32, '(ระยะด้านข้างในภาพขยายสเกลให้เห็นชัด)', 11, 'start', '#7f1d1d')
    # crash stop 14 kn
    y1 = 250
    s += line(ox, y1, ox + 1207 * sc, y1, '#c2410c', 5)
    s += txt(ox, y1 - 14, 'Crash stop จาก 14 kn (full ahead manoeuvring)', 13, 'start', '#c2410c', True)
    s += txt(ox + 1207 * sc + 10, y1 + 5, '≈ 1,200 m (≈ 7 L, 0.65 nm) · ≈ 5.5 นาที', 12.5, 'start', '#c2410c', True)
    # inertia
    y2 = 320
    s += line(ox, y2, ox + 7133 * sc, y2, '#64748b', 6)
    s += txt(ox, y2 - 14, 'Inertia stop (Stop engine ปล่อยไหลไปเอง) จาก 19 kn จนเหลือ 2 kn ≈ 7,100 m (3.9 nm) · ≈ 46 นาที', 13, 'start', '#334155', True)
    ys = 352
    s += line(ox, ys, ox + 7000 * sc, ys, '#0f172a', 1)
    for k in range(0, 8):
        X = ox + k * 1000 * sc
        s += line(X, ys - 5, X, ys + 5, '#0f172a', 1) + txt(X, ys + 20, f'{k} km', 11, 'middle')
    notes = ['คำศัพท์: Head reach = ระยะตามแนวเข็มเดิมจนหยุด · Track reach = ระยะตามทางเดินจริง · Lateral deviation = ระยะเบนออกด้านข้าง',
             'ระยะหยุดขึ้นกับมวล (displacement + added mass) และความเร็วยกกำลังสอง — บรรทุกเต็มหยุดยากกว่าเรือเปล่ามาก; น้ำไหลตามทำให้ไปไกลขึ้นเมื่อเทียบพื้น',
             'ตัวเลขจากแบบจำลองอย่างง่าย (มวล 31,000 t, แรงถอย 700 kN, หน่วงกลับเครื่อง 45 s) — ใช้ค่าจาก manoeuvring booklet ของเรือจริงเสมอ']
    for i, n in enumerate(notes):
        s += txt(40, 410 + i * 20, n, 12, 'start', '#334155')
    save('man-stopping-distances.svg', s)


# ---------------------------------------------------------------- 5 squat
def squat():
    w, h = 1000, 640
    s = head(w, h, 'Squat และ blockage factor (สูตร Barrass)')
    # cross section
    cx, top = 230, 90
    s += txt(cx, 70 + 5, 'ภาคตัดขวางร่องน้ำ', 14, 'middle', bold=True)
    s += f'<path d="M 40 110 L 90 110 L 130 270 L 330 270 L 370 110 L 420 110" fill="#fef3c7" stroke="#92400e" stroke-width="2"/>'
    s += f'<rect x="60" y="110" width="340" height="0" />'
    s += line(40, 140, 420, 140, '#0284c7', 2)
    s += f'<rect x="190" y="125" width="80" height="70" fill="#cbd5e1" stroke="#0f172a" stroke-width="2"/>'
    s += txt(230, 165, 'b × T', 12, 'middle', bold=True)
    s += line(110, 300, 350, 300, '#c2410c', 1.5, mk='arO') + line(350, 300, 110, 300, '#c2410c', 1.5, mk='arO')
    s += txt(230, 318, 'B = ความกว้างร่อง (ร่องคางหมูใช้พื้นที่หน้าตัดจริงแทน B × h)', 11, 'middle', '#c2410c')
    s += line(430, 140, 430, 270, '#c2410c', 1.5, mk='arO') + line(430, 270, 430, 140, '#c2410c', 1.5, mk='arO')
    s += txt(438, 210, 'h', 13, 'start', '#c2410c', True)
    s += txt(230, 350, 'Blockage factor  S = (b × T) / (B × h)', 13, 'middle', bold=True)
    s += txt(230, 370, 'น้ำเปิด S &lt; ~0.10 · ร่องจำกัด S ≈ 0.10–0.27', 12, 'middle', '#334155')
    # profile bow/stern
    px, py = 520, 70
    s += txt(745, py + 5, 'ลักษณะการจม (โปรไฟล์)', 14, 'middle', bold=True)
    s += line(520, 130, 970, 130, '#0284c7', 1.5, '6 4')
    s += f'<polygon points="540,105 940,105 960,120 940,160 560,160 540,145" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.5" transform="rotate(2.5 750 130)"/>'
    s += txt(745, 190, 'Cb &gt; 0.7 (เรือป้อม เช่น tanker/bulk) → หัวจมมากกว่า (trim by head)', 12, 'middle', '#b91c1c')
    s += f'<polygon points="540,105 940,105 960,120 940,160 560,160 540,145" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.5" transform="translate(0 110) rotate(-2.5 750 130)"/>'
    s += line(520, 240, 970, 240, '#0284c7', 1.5, '6 4')
    s += txt(745, 300, 'Cb &lt; 0.7 (เรือเพรียว เช่น container) → ท้ายจมมากกว่า (trim by stern)', 12, 'middle', '#1d4ed8')
    s += txt(745, 318, 'Cb ≈ 0.7 → จมเกือบเท่ากันทั้งหัวท้าย · มี static trim อยู่แล้ว squat มากที่ปลายด้านที่จมกว่า', 11, 'middle', '#334155')
    # graph
    gx, gy, gw, gh = 90, 420, 400, 180
    s += line(gx, gy + gh, gx + gw, gy + gh, '#0f172a', 1.5) + line(gx, gy + gh, gx, gy, '#0f172a', 1.5)
    s += txt(gx + gw / 2, gy + gh + 34, 'ความเร็วผ่านน้ำ V (kn)', 12, 'middle')
    s += f'<text x="{gx-44}" y="{gy+gh/2}" font-size="12" text-anchor="middle" transform="rotate(-90 {gx-44} {gy+gh/2})">squat สูงสุด (m)</text>'
    Cb = 0.65
    for v in range(0, 15, 2):
        X = gx + v / 14 * gw
        s += line(X, gy + gh, X, gy + gh + 5, '#0f172a', 1) + txt(X, gy + gh + 18, str(v), 11, 'middle')
    for m_ in (0, 0.5, 1.0, 1.5, 2.0, 2.5):
        Y = gy + gh - m_ / 2.6 * gh
        s += line(gx - 5, Y, gx, Y, '#0f172a', 1) + txt(gx - 8, Y + 4, f'{m_:.1f}', 11, 'end')
        s += line(gx, Y, gx + gw, Y, '#e2e8f0', 1)
    for div, col, lab in ((100, '#15803d', 'น้ำเปิด  Cb·V²/100'), (50, '#b91c1c', 'ร่องจำกัด  Cb·V²/50')):
        pts = [(gx + v / 14 * gw, gy + gh - (Cb * v * v / div) / 2.6 * gh) for v in [i * 0.25 for i in range(57)]]
        s += '<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts) + f'" fill="none" stroke="{col}" stroke-width="3"/>'
        s += txt(pts[-1][0] + 6, pts[-1][1] + 4, lab, 12, 'start', col, True)
    s += txt(gx + 10, gy - 10, 'ตัวอย่าง Cb = 0.65 (V เป็นนอต ผลเป็นเมตร)', 12, 'start', '#334155')
    # notes
    bx, by = 600, 380
    s += f'<rect x="{bx}" y="{by}" width="380" height="240" rx="10" fill="#f8fafc" stroke="#94a3b8"/>'
    notes = ['สัญญาณเตือนว่ากำลังเกิด squat/น้ำตื้น:', '• ความเร็วลดลงเองที่รอบเครื่องเท่าเดิม', '• รอบเครื่องตก ตัวเรือสั่น (vibration)',
             '• คลื่นหัว/ท้ายสูงขึ้น ร่องคลื่นท้ายเปลี่ยน', '• หางเสือตอบสนองช้า เรือ sheer', '• น้ำขุ่นโคลนขึ้นในร่องน้ำท้ายเรือ',
             '• echo sounder แสดง UKC ลดลง', '', 'แก้ไขที่ได้ผลที่สุด: ลดความเร็ว', '(squat แปรผันประมาณ V² — ลดเร็วครึ่ง', 'squat เหลือประมาณ 1/4)']
    for i, n in enumerate(notes):
        s += txt(bx + 14, by + 26 + i * 19, n, 12.5, 'start', '#0f172a', i in (0, 8))
    save('man-squat.svg', s)


# ---------------------------------------------------------------- 6 shallow water
def shallow():
    w, h = 1000, 470
    s = head(w, h, 'ผลของน้ำตื้น (Shallow-water effects) ตามอัตราส่วน h/T')
    x0, x1, y = 80, 920, 110
    s += f'<defs><linearGradient id="gS" x1="0" x2="1"><stop offset="0" stop-color="#fecaca"/><stop offset="0.5" stop-color="#fde68a"/><stop offset="1" stop-color="#bbf7d0"/></linearGradient></defs>'
    s += f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="34" fill="url(#gS)" stroke="#0f172a"/>'
    for v, lab in ((1.0, '1.0'), (1.2, '1.2'), (1.5, '1.5'), (2.0, '2.0'), (3.0, '3.0'), (4.0, '4.0')):
        X = x0 + (v - 1.0) / 3.0 * (x1 - x0)
        s += line(X, y + 34, X, y + 44, '#0f172a', 1.5) + txt(X, y + 60, lab, 12, 'middle', bold=True)
    s += txt(x0, y - 10, 'h/T (ความลึกน้ำ ÷ กินน้ำลึก)', 13, 'start', bold=True)
    s += txt(x0 + 10, y + 22, 'ผลรุนแรงมาก', 12, 'start', '#7f1d1d', True)
    s += txt((x0 + x1) / 2 - 140, y + 22, 'เริ่มเห็นผลชัด (≈ &lt; 1.5–2)', 12, 'middle', '#78350f', True)
    s += txt(x1 - 10, y + 22, 'น้ำลึก (ผลน้อย)', 12, 'end', '#14532d', True)
    # turning circles deep vs shallow
    cx, cy = 230, 310
    s += f'<circle cx="{cx}" cy="{cy}" r="55" fill="none" stroke="#15803d" stroke-width="3"/>'
    s += f'<circle cx="{cx+50}" cy="{cy}" r="105" fill="none" stroke="#b91c1c" stroke-width="3" stroke-dasharray="8 5"/>'
    s += txt(cx - 20, cy + 4, 'น้ำลึก', 12, 'middle', '#15803d', True)
    s += txt(cx + 50, cy + 128, 'น้ำตื้น h/T ≈ 1.2: tactical diameter', 12, 'middle', '#b91c1c', True)
    s += txt(cx + 50, cy + 145, 'อาจโตขึ้นเกือบ 2 เท่า', 12, 'middle', '#b91c1c', True)
    # effects list
    bx = 470
    items = ['• Squat เพิ่ม (จมและเปลี่ยน trim) — UKC ลดลง',
             '• ความต้านทานเพิ่ม → ความเร็วลดที่รอบเท่าเดิม รอบเครื่องตก',
             '• วงเลี้ยวโตขึ้น หางเสือตอบสนองช้า ต้องใช้มุมหางเสือมากขึ้น',
             '• ทรงทิศ (directional stability) เปลี่ยน — บางลำ "ตรง" ขึ้น บางลำ sheer',
             '• มวลน้ำติดเรือ (added mass) เพิ่ม → เร่ง/หยุด/หันช้าลง',
             '• Transverse thrust และการตอบสนองต่อการถอยผิดคาดได้',
             '• คลื่นหัว/ท้ายใหญ่ขึ้น กระทบเรือเล็กและเรือที่จอด',
             '• แรงจากกระแสน้ำ/ลมด้านข้างต่อใต้ท้องเรือเพิ่มมาก (UKC น้อย)',
             '• ใบจักรดูดตะกอน/ทำลายท้องร่องน้ำ เครื่องร้อน (cooling intake)']
    for i, it in enumerate(items):
        s += txt(bx, 200 + i * 26, it, 13)
    save('man-shallow-water.svg', s)


# ---------------------------------------------------------------- 7 bank & interaction
def interaction():
    w, h = 1000, 585
    s = head(w, h, 'Bank effect และ interaction ระหว่างเรือ (pressure fields)')
    # bank effect panel
    s += txt(250, 70, 'Bank effect (ตลิ่งอยู่กราบซ้าย เรือมุ่งไปทางขวา)', 15, 'middle', bold=True)
    s += '<path d="M 40 110 L 460 110 L 460 90 L 40 90 Z" fill="#d6d3d1" stroke="#57534e"/>'
    s += txt(250, 104, 'ตลิ่ง / ขอบร่องน้ำ (bank)', 12, 'middle', '#44403c', True)
    s += ship(250, 190, 90, 300, 50, '#e2e8f0')
    s += line(400, 160, 400, 140, '#15803d', 3, mk='arG') if False else ''
    s += line(380, 165, 380, 210, '#15803d', 3, mk='arG')
    s += txt(388, 240, 'Bank cushion: หัวถูกดันออก', 12, 'middle', '#15803d', True)
    s += line(120, 160, 120, 125, '#b91c1c', 3, mk='arR')
    s += txt(120, 240, 'Bank suction: ท้ายถูกดูดเข้า', 12, 'middle', '#b91c1c', True)
    s += txt(250, 270, 'ผลรวม: เรือ sheer หันหัวหนีตลิ่ง (ไปกลางร่อง)', 12, 'middle', bold=True)
    s += txt(250, 288, 'แก้: หางเสือหันเข้าหาตลิ่ง ลดความเร็ว รักษาระยะ', 12, 'middle', '#334155')
    s += txt(250, 306, 'ความเร็วสูง + ใกล้ตลิ่ง + UKC น้อย = ผลแรงที่สุด', 12, 'middle', '#334155')
    # pressure field
    s += txt(750, 70, 'Pressure field รอบตัวเรือที่แล่น', 15, 'middle', bold=True)
    cx, cy = 750, 190
    s += f'<ellipse cx="{cx+140}" cy="{cy}" rx="70" ry="60" fill="#fecaca" opacity="0.8"/>'
    s += f'<ellipse cx="{cx-140}" cy="{cy}" rx="60" ry="50" fill="#fecaca" opacity="0.8"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="110" ry="70" fill="#bfdbfe" opacity="0.8"/>'
    s += ship(cx, cy, 90, 300, 50, '#e2e8f0')
    s += txt(cx + 150, cy - 64, '+ ความดันสูง (หัว)', 12, 'middle', '#b91c1c', True)
    s += txt(cx - 150, cy - 56, '+ (ท้าย)', 12, 'middle', '#b91c1c', True)
    s += txt(cx, cy + 92, '− ความดันต่ำ (กลางลำ) = แรงดูด', 12, 'middle', '#1d4ed8', True)
    s += line(cx + 40, cy + 115, cx + 110, cy + 115, '#0f172a', 2, mk='ar') + txt(cx + 34, cy + 119, 'ทิศเดินเรือ', 11, 'end')
    # overtaking stages
    s += txt(500, 330, 'การแซงในร่องน้ำแคบ (overtaking) — ช่วงอันตราย', 15, 'middle', bold=True)
    stages = [('1. หัวเรือแซงถึงท้ายเรือถูกแซง', ['+ ชน + → ผลักกัน: ท้ายเรือถูกแซงถูกดันออก', 'หัวเรือถูกแซงจึงหันเข้าหาทางเรือแซง'], -110),
              ('2. ขนานกันกลางลำ', ['− กับ − → แรงดูดดึงเข้าหากัน', 'ทั้งสองลำ (ยิ่งใกล้ยิ่งแรง)'], 0),
              ('3. หัวเรือถูกแซงอยู่ช่วงท้ายเรือแซง', ['หัวเรือถูกแซงถูกดูดเข้าหา อาจ sheer', 'ตัดท้ายเรือแซง — ช่วงอันตรายมาก'], 95)]
    for i, (t1, t2, off) in enumerate(stages):
        X = 190 + i * 310
        s += ship(X, 395, 90, 120, 22, '#e2e8f0')
        s += ship(X + off, 430, 90, 130, 24, '#bfdbfe')
        s += txt(X, 470, t1, 12.5, 'middle', bold=True)
        for j, l2 in enumerate(t2):
            s += txt(X, 488 + j * 16, l2, 11.5, 'middle', '#334155')
    s += txt(60, 375, 'เทา = เรือถูกแซง (ช้า) · ฟ้า = เรือแซง', 11, 'start', '#475569')
    s += txt(500, 548, 'ข้อปฏิบัติ: ตกลงกันทาง VHF/สัญญาณเสียง (Rule 9(e)) · ลดความเร็วของเรือที่ถูกแซง (แต่คงหางเสือ) · ระยะด้านข้างให้มากที่สุด', 12, 'middle')
    s += txt(500, 568, 'เรือเล็ก/เรือลากจูงใกล้หัวเรือใหญ่อาจถูกดูดเข้าหาหรือหมุนตัดหน้า — ระวังเป็นพิเศษ', 12, 'middle', '#b91c1c')
    save('man-bank-interaction.svg', s)


# ---------------------------------------------------------------- 8 MOB turns
def mob_turns():
    w, h = 1000, 680
    s = head(w, h, 'การหันเรือกลับเพื่อช่วยคนตกน้ำ (IAMSAR Vol III) — คนตกกราบขวา')
    panels = [('W', 'Williamson turn', 170, ['หางเสือ hard over (ไปกราบที่คนตก)', 'เบนจากเข็มเดิม 60° → hard over อีกข้าง',
                                              'หัวเรือห่างเข็มกลับ 20° → midships', 'กลับมาบนแนวเส้นทางเดิม (ทิศตรงข้าม)',
                                              'ดีเมื่อกลางคืน/ทัศนวิสัยจำกัด/delayed action', 'ข้อเสีย: ช้า พาเรือห่างจุดเกิดเหตุ']),
              ('A', 'Anderson (single turn)', 500, ['หางเสือ hard over (ไปกราบที่คนตก)', 'เบนจากเข็มเดิม ~250° → midships',
                                                     'แล้วเริ่มหยุดเรือ (stopping manoeuvre)', 'เร็วที่สุด เหมาะ immediate action',
                                                     'เรือเลี้ยวแคบ/กำลังเครื่องสูงทำได้ดี', 'ข้อเสีย: เรือใบจักรเดียวเข้าหาคนยาก']),
              ('S', 'Scharnow turn', 830, ['หางเสือ hard over', 'เบนจากเข็มเดิม 240° → hard over อีกข้าง',
                                            'หัวเรือห่างเข็มกลับ 20° → midships', 'กลับเข้าร่องท้ายเรือ (wake) ระยะสั้นกว่า',
                                            'ไม่เหมาะ immediate action (ในภาพ', 'จะกลับมาที่แนวเส้นทางเลยจุดคนตกไปแล้ว)'])]
    sc = 0.2
    for kind, title, cx, notes in panels:
        pts, ev = simulate(kind)
        oy = 360
        P = lambda x, y: (cx - 60 + x * sc, oy - y * sc)
        s += txt(cx, 68, title, 15, 'middle', bold=True)
        a0, b0 = P(0, -800); a1, b1 = P(0, 1150)
        s += line(a0, b0, a1, b1, '#94a3b8', 1.2, '5 4')
        poly = ' '.join(f'{P(x, y)[0]:.1f},{P(x, y)[1]:.1f}' for x, y, _, _ in pts)
        s += f'<polyline points="{poly}" fill="none" stroke="#1d4ed8" stroke-width="2.6"/>'
        lx, ly = P(pts[-1][0], pts[-1][1])
        px, py = P(pts[-8][0], pts[-8][1])
        s += line(px, py, lx, ly, '#1d4ed8', 2.6, mk='arB')
        mx, my = P(0, 0)
        s += f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="7" fill="#f97316" stroke="#7c2d12" stroke-width="2"/>'
        s += txt(mx - 10, my + 4, 'MOB', 11, 'end', '#7c2d12', True)
        for lab, x, y in ev:
            X, Y = P(x, y)
            s += f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="4.5" fill="#b91c1c"/>'
            show = {'60': '60°', '240': '240°', '250': '250° → midships', '200': 'หัว 200° → midships'}[lab]
            s += txt(X + 8, Y - 6, show, 11, 'start', '#b91c1c', True)
        for i, n in enumerate(notes):
            s += txt(cx, 548 + i * 18, n, 11.5, 'middle', '#0f172a', i == 3)
        if kind != 'W':
            s += line(cx - 165, 80, cx - 165, 650, '#e2e8f0', 1)
    s += txt(500, 670, 'แบบจำลองอย่างง่าย เรือ 172 m ที่ 14 kn (เส้นประ = เส้นทางเดิม เรือเริ่มเดินขึ้นเหนือ ณ จุด MOB) — ระยะจริงขึ้นกับเรือแต่ละลำ', 11, 'middle', '#475569')
    save('man-mob-turns.svg', s)


# ---------------------------------------------------------------- 9 anchoring
def anchoring():
    w, h = 1000, 600
    s = head(w, h, 'การทอดสมอ: โซ่สมอรูปโค้ง catenary และวงแกว่ง (swinging circle)')
    # profile
    sea, bed = 150, 330
    s += f'<rect x="30" y="{sea}" width="600" height="{bed-sea}" fill="#e0f2fe"/>'
    s += f'<rect x="30" y="{bed}" width="600" height="30" fill="#d6d3d1"/>'
    s += txt(40, bed + 22, 'พื้นทะเล (holding ground)', 12, 'start', '#44403c', True)
    # ship hull at right
    hx = 520
    s += f'<path d="M {hx-10} {sea-40} L {hx+100} {sea-40} L {hx+100} {sea+30} L {hx+20} {sea+30} Z" fill="#cbd5e1" stroke="#0f172a" stroke-width="2"/>'
    hawse = (hx, sea - 30)
    # catenary: a = 170 m, y = 35 m (hawse to bed); scale 3 px/m vertical, 2.2 px/m horizontal
    a = 170.0; yv = 35.0
    xt = a * math.acosh(yv / a + 1)
    sx, sy = 2.6, 5.1
    pts = []
    for i in range(0, 61):
        xx = xt * i / 60
        yy = a * (math.cosh(xx / a) - 1)
        pts.append((hawse[0] - (xt - xx) * sx, bed - yy * sy))
    # chain on seabed
    pts = [(hawse[0] - (xt + 45) * sx, bed)] + pts
    s += '<polyline points="' + ' '.join(f'{p[0]:.1f},{p[1]:.1f}' for p in pts) + '" fill="none" stroke="#0f172a" stroke-width="3"/>'
    ax_ = pts[0][0]
    s += f'<path d="M {ax_-4} {bed-14} l -14 14 l 30 0 z" fill="#0f172a"/>'
    s += txt(ax_ - 5, bed - 22, 'สมอ (anchor)', 12, 'middle', bold=True)
    s += txt(230, bed + 22, 'โซ่ส่วนที่นอนพื้น → แรงที่สมอเป็นแนวนอน (สมอกินดิน)', 11.5, 'start', '#1c1917')
    s += line(hx + 100, sea - 30, hx + 100, bed, '#c2410c', 1.5, mk='arO') + line(hx + 100, bed, hx + 100, sea - 30, '#c2410c', 1.5, mk='arO')
    s += txt(hx + 92, 245, 'y ≈ 35 m', 12.5, 'end', '#c2410c', True)
    s += txt(hx + 92, 263, '(ความลึก + ความสูง', 11.5, 'end', '#c2410c')
    s += txt(hx + 92, 279, 'ช่องโซ่เหนือน้ำ)', 11.5, 'end', '#c2410c')
    s += line(30, sea, 630, sea, '#0284c7', 2)
    s += line(hx - 90, sea - 60, hx - 20, sea - 60, '#1d4ed8', 2.5, mk='arB')
    s += txt(hx - 96, sea - 56, 'ลม/กระแสดันเรือ → แรง H', 12, 'end', '#1d4ed8', True)
    # formula box
    bx, by = 30, 385
    s += f'<rect x="{bx}" y="{by}" width="600" height="195" rx="10" fill="#f8fafc" stroke="#94a3b8"/>'
    fl = ['ความยาวโซ่ส่วนโค้งที่ทำให้แรงที่สมอเป็นแนวนอนพอดี:',
          's = √( y² + 2·a·y )   โดย a = H ÷ w',
          'H = แรงดึงแนวนอนจากลม กระแส คลื่น · w = น้ำหนักโซ่ในน้ำต่อเมตร',
          'ตัวอย่าง: โซ่ 68 mm (≈ 88 kg/m ในน้ำ), y = 35 m',
          '  H = 15 t → a ≈ 170 m → s ≈ 115 m (≈ 4.2 shackles) + ส่วนนอนพื้น',
          '  H = 30 t → a ≈ 341 m → s ≈ 158 m (≈ 5.8 shackles) + ส่วนนอนพื้น',
          '1 shackle = 15 fathoms = 27.5 m · กฎหัวแม่มือ ≈ 1.5√(ความลึก m) shackles',
          'เผื่อเสมอ: โซ่นอนพื้นอีกช่วงหนึ่ง และเพิ่มเมื่อสภาพอากาศแย่ลง']
    for i, f in enumerate(fl):
        s += txt(bx + 14, by + 24 + i * 21, f, 12.5, 'start', '#0f172a', i in (0, 1))
    # swing circle plan
    cx, cy = 820, 330
    s += txt(cx, 70, 'วงแกว่ง (มุมมองจากด้านบน)', 14, 'middle', bold=True)
    s += f'<circle cx="{cx}" cy="{cy}" r="150" fill="#f0f9ff" stroke="#0369a1" stroke-width="2" stroke-dasharray="7 4"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="5" fill="#0f172a"/>' + txt(cx + 8, cy + 16, 'สมอ', 11, 'start', bold=True)
    s += line(cx, cy, cx + 80, cy - 40, '#0f172a', 2)
    s += ship(cx + 80 + 40 * math.sin(R(63.4)), cy - 40 - 40 * math.cos(R(63.4)), 243.4, 80, 14, '#cbd5e1')
    s += line(cx, cy, cx - 150, cy, '#b91c1c', 1.5, mk='arR')
    s += txt(cx - 75, cy - 8, 'รัศมี', 12, 'middle', '#b91c1c', True)
    s += txt(cx, cy + 175, 'รัศมีวงแกว่ง ≈ ความยาวโซ่ (ระยะราบ)', 12, 'middle', '#b91c1c', True)
    s += txt(cx, cy + 193, '+ ความยาวเรือ (LOA) — ใช้ตั้ง anchor watch', 12, 'middle', '#b91c1c', True)
    s += txt(cx, cy + 211, 'circle/guard zone บน ECDIS และเรดาร์', 12, 'middle', '#b91c1c')
    s += txt(cx, cy + 236, 'ระวังระยะกับเรือข้างเคียงที่วงแกว่งต่างกัน', 12, 'middle', '#334155')
    save('man-anchor-catenary.svg', s)


# ---------------------------------------------------------------- 10 mooring
def mooring():
    w, h = 1000, 560
    s = head(w, h, 'การผูกเรือเข้าเทียบท่า: ชื่อและหน้าที่ของเชือก (ตัวอย่างเทียบกราบขวา)')
    s += '<rect x="40" y="380" width="920" height="60" fill="#a8a29e" stroke="#57534e"/>'
    s += txt(500, 418, 'หน้าท่า (quay / berth)', 14, 'middle', '#1c1917', True)
    for x in range(80, 960, 110):
        s += f'<rect x="{x}" y="372" width="16" height="12" rx="3" fill="#57534e"/>'
    # ship
    s += '<path d="M 200 360 L 760 360 Q 860 360 900 300 Q 860 240 760 240 L 200 240 Q 180 240 180 260 L 180 340 Q 180 360 200 360 Z" fill="#e2e8f0" stroke="#0f172a" stroke-width="2"/>'
    s += txt(540, 305, 'MV Andaman Pearl (หัวเรือไปทางขวา)', 14, 'middle', '#334155', True)
    lines_ = [  # (ship x, ship y, quay x, label, colour, label pos)
        (880, 316, 960, 'Head line', '#b91c1c', (950, 470)),
        (840, 345, 860, 'Fwd breast', '#c2410c', (845, 470)),
        (800, 355, 650, 'Fwd spring', '#1d4ed8', (690, 470)),
        (260, 355, 410, 'Aft spring', '#1d4ed8', (390, 470)),
        (220, 350, 205, 'Aft breast', '#c2410c', (210, 470)),
        (190, 330, 60, 'Stern line', '#b91c1c', (90, 470))]
    for sx_, sy_, qx, lab, col, (lx, ly) in lines_:
        s += line(sx_, sy_, qx, 378, col, 2.6)
        s += txt(lx, ly, lab, 12.5, 'middle', col, True)
    s += txt(500, 500, 'Head/Stern lines + Springs = ต้านการเคลื่อนตามยาว (surge) · Breast lines = ต้านการเคลื่อนออกจากท่า (sway)', 12.5, 'middle')
    s += txt(500, 520, 'Springs ยิ่งขนานกับเรือยิ่งดี · Breast ยิ่งตั้งฉากกับเรือยิ่งดี · มุมก้ม/เงย (vertical angle) ไม่ควรเกินประมาณ 25–30°', 12.5, 'middle')
    s += txt(500, 540, 'เชือกที่ทำหน้าที่เดียวกันควรเป็นวัสดุ ขนาด และความยาวใกล้เคียงกัน — ไม่ปนเชือก wire กับ fibre ในทิศเดียวกัน', 12.5, 'middle', '#b91c1c')
    # snap-back sketch
    s += '<rect x="40" y="60" width="920" height="160" rx="10" fill="#fff7ed" stroke="#c2410c"/>'
    s += txt(60, 86, 'Snap-back: เชือกที่ขาดจะดีดกลับด้วยพลังงานสูงมาก ในทิศและระยะที่ทำนายยาก', 14, 'start', '#9a3412', True)
    s += f'<circle cx="160" cy="160" r="12" fill="#57534e"/>' + txt(160, 200, 'bitt', 11, 'middle')
    s += f'<rect x="300" y="146" width="40" height="28" fill="#94a3b8" stroke="#0f172a"/>' + txt(320, 200, 'fairlead', 11, 'middle')
    s += line(172, 160, 300, 160, '#0f172a', 3) + line(340, 160, 470, 160, '#0f172a', 3, '10 6')
    s += '<path d="M 300 160 q -80 -40 -150 -55" fill="none" stroke="#c2410c" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#arO)"/>'
    s += '<path d="M 300 160 q -80 40 -170 40" fill="none" stroke="#c2410c" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#arO)"/>'
    for i, t in enumerate(['• ถือว่าพื้นที่ทั้งหมดบนดาดฟ้าผูกเรือเป็นพื้นที่เสี่ยง', '  (แนวทางล่าสุดของ UK MCA COSWP — สีที่ทาพื้นอาจให้ความรู้สึกปลอดภัยผิด ๆ)',
                           '• ยืนให้ห่างแนวเชือกที่ตึง โดยเฉพาะด้านในมุมที่เชือกหักเลี้ยวผ่าน fairlead/pedestal',
                           '• สื่อสารชัด ใช้คนน้อยที่สุดในพื้นที่ · ตรวจสภาพเชือก/tail ตามแผน (SOLAS II-1/3-8)']):
        s += txt(500, 120 + i * 22, t, 12, 'start', '#7c2d12')
    save('man-mooring-lines.svg', s)


# ---------------------------------------------------------------- 11 berthing / unberthing
def berthing():
    w, h = 1000, 430
    s = head(w, h, 'การออกจากท่าโดยใช้ spring (Springing off) — เทียบกราบซ้าย ใบจักรเวียนขวา')
    s += '<rect x="40" y="340" width="920" height="50" fill="#a8a29e" stroke="#57534e"/>'
    s += txt(500, 372, 'หน้าท่า (อยู่กราบซ้ายของเรือ — หัวเรือหันไปทางซ้ายของภาพ)', 13, 'middle', '#1c1917', True)
    steps = [(180, 0, '1. Single up เหลือ fwd spring', 'มีกันชน (fender) ที่หัวเรือ'),
             (500, 14, '2. Slow ahead + หางเสือ hard to port', 'หัวถูก spring ยึด → ท้ายเหวี่ยงออก'),
             (820, 26, '3. ท้ายออกพอ → stop, let go spring', 'ถอยหลังออก (ท้ายปัดซ้ายเล็กน้อย)')]
    for cx, ang, t1, t2 in steps:
        bowx, bowy = cx - 115, 318
        hdg = 270 - ang
        ccx = bowx - 115 * math.sin(R(hdg)); ccy = bowy + 115 * math.cos(R(hdg))
        s += ship(ccx, ccy, hdg, 230, 36, '#e2e8f0')
        s += line(bowx + 8, bowy + 8, bowx + 80, 340, '#1d4ed8', 2.5)
        s += f'<circle cx="{bowx+2}" cy="{bowy+14}" r="6" fill="#facc15" stroke="#854d0e"/>'
        s += txt(cx, 90, t1, 13, 'middle', bold=True)
        s += txt(cx, 110, t2, 12, 'middle', '#334155')
    s += '<path d="M 600 255 q 10 -40 -10 -75" fill="none" stroke="#b91c1c" stroke-width="3" marker-end="url(#arR)"/>'
    s += txt(180, 140, 'เส้นสีน้ำเงิน = forward spring (นำไปทางท้าย)', 11.5, 'middle', '#1d4ed8')
    s += txt(820, 128, 'ข้อควรระวัง: ถอยหลังแล้วท้ายปัดซ้าย = กลับเข้าหาท่า', 11.5, 'middle', '#b91c1c', True)
    s += txt(820, 144, 'จึงต้องให้ท้ายออกได้มุมพอก่อนสั่งถอย', 11.5, 'middle', '#b91c1c')
    s += txt(500, 415, 'ภาพจำลองแนวคิด — ถ้ามีลมพัดเข้าท่า กระแสแรง หรือเรือใหญ่ ใช้ tug/bow thruster ตามแผนของนายเรือและนำร่อง', 12, 'middle', '#334155')
    save('man-springing-off.svg', s)


if __name__ == '__main__':
    r = turning_circle()
    print('advance', round(r[0][1] - r[2][1]), 'transfer', round(r[0][0]), 'TD', round(r[1][0]), 'FD', round(r[3]), 't90', r[0][3] - r[2][3], 't180', r[1][3] - r[2][3])
    pivot_wind(); transverse_thrust(); stopping(); squat(); shallow(); interaction(); mob_turns(); anchoring(); mooring(); berthing()
