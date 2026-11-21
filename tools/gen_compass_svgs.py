"""สคริปต์สร้างภาพประกอบบทเข็มทิศ"""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
def head(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="a" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="context-stroke"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{title}</text>\n')
def save(n, s): open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')
def ray(cx, cy, ang, L, col, w=3, label=None, dx=0, dy=0):
    a = math.radians(ang); x = cx + L * math.sin(a); y = cy - L * math.cos(a)
    s = f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="{w}" marker-end="url(#a)"/>\n'
    if label: s += f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" font-size="15" font-weight="bold" fill="{col}">{label}</text>\n'
    return s
def arc(cx, cy, a1, a2, r, col, label, lx=0, ly=0):
    p1 = (cx + r * math.sin(math.radians(a1)), cy - r * math.cos(math.radians(a1)))
    p2 = (cx + r * math.sin(math.radians(a2)), cy - r * math.cos(math.radians(a2)))
    sweep = 1 if a2 > a1 else 0
    s = f'<path d="M {p1[0]:.1f} {p1[1]:.1f} A {r} {r} 0 0 {sweep} {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{col}" stroke-width="2.5"/>\n'
    mid = math.radians((a1 + a2) / 2)
    s += f'<text x="{cx + (r+12)*math.sin(mid)+lx:.1f}" y="{cy - (r+12)*math.cos(mid)+ly:.1f}" font-size="13" font-weight="bold" fill="{col}">{label}</text>\n'
    return s

def tvmdc():
    w, h = 960, 520
    s = head(w, h, 'True – Magnetic – Compass North (ตัวอย่าง: Var 0.5°W, Dev 2.1°E)')
    cx, cy = 260, 430
    s += ray(cx, cy, 0, 340, '#15803d', 3.5, 'True N', -26, -10)
    s += ray(cx, cy, -8, 330, '#1d4ed8', 3, 'Magnetic N', -110, -8)
    s += ray(cx, cy, 14, 320, '#b91c1c', 3, 'Compass N', 6, -8)
    s += arc(cx, cy, -8, 0, 230, '#1d4ed8', 'Variation (W)', -120, -10)
    s += arc(cx, cy, -8, 14, 280, '#b91c1c', 'Deviation (E)', 72, 30)
    s += f'<circle cx="{cx}" cy="{cy}" r="6" fill="#0f172a"/>\n'
    s += '<text x="40" y="500" font-size="12" fill="#64748b">(มุมในภาพขยายให้เห็นชัด ไม่ได้ตามสเกล)</text>\n'
    # table panel
    s += '<rect x="520" y="70" width="420" height="420" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    lines = [('T  →  V  →  M  →  D  →  C', True), ('True Virgins Make Dull Company', False), ('', False),
             ('Compass Error = Variation + Deviation', True), ('(E = +, W = −)', False), ('', False),
             ('Compass → True : บวก E / ลบ W', False), ('True → Compass : ลบ E / บวก W', False),
             ('"Error East, Compass Least;', False), (' Error West, Compass Best"', False), ('', False),
             ('ตัวอย่าง: True 160.0°', False), ('+ Var 0.5°W → Magnetic 160.5°', False), ('− Dev 2.1°E → Compass 158.4°C', False),
             ('CE = 1.6°E → Compass = True − 1.6°', True)]
    for i, (t, b) in enumerate(lines):
        fw = ' font-weight="bold"' if b else ''
        s += f'<text x="540" y="{102 + i*25}" font-size="15"{fw}>{t}</text>\n'
    save('compass-tvmdc.svg', s)

def earth_field():
    """สนามแม่เหล็กโลกแบบ dipole: ขั้วแม่เหล็ก เส้นศูนย์สูตรแม่เหล็ก และองค์ประกอบ T, H, Z, dip"""
    w, h = 960, 560
    s = head(w, h, 'สนามแม่เหล็กโลก (Terrestrial magnetism) — องค์ประกอบ H, Z และมุม dip')
    cx, cy, R = 290, 300, 115
    tilt = math.radians(-11)                      # แกนแม่เหล็กเอียงจากแกนหมุนโลก (โดยประมาณ)
    ax, ay = math.sin(tilt), -math.cos(tilt)      # ทิศไปยังขั้วแม่เหล็กเหนือ
    px, py = math.cos(tilt), math.sin(tilt)       # ตั้งฉาก (ไปทางขวา)
    # field lines (r = L sin^2 theta) ทั้งสองข้าง
    for L in (1.45, 1.9, 2.45):
        th0 = math.asin(math.sqrt(1 / L))
        for side in (1, -1):
            pts = []
            n = 60
            for i in range(n + 1):
                th = th0 + (math.pi - 2 * th0) * i / n
                r = L * R * math.sin(th) ** 2
                x = cx + r * (math.cos(th) * ax + side * math.sin(th) * px)
                y = cy + r * (math.cos(th) * ay + side * math.sin(th) * py)
                pts.append((x, y))
            s += '<path d="M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in pts) + '" fill="none" stroke="#a78bfa" stroke-width="1.6"/>\n'
            # หัวลูกศรที่ยอดเส้น (ชี้จากใต้ไปเหนือ ภายนอกโลก)
            r = L * R
            mx = cx + r * side * px; my = cy + r * side * py
            s += f'<line x1="{mx - 8*ax:.1f}" y1="{my - 8*ay:.1f}" x2="{mx + 8*ax:.1f}" y2="{my + 8*ay:.1f}" stroke="#7c3aed" stroke-width="2" marker-end="url(#a)"/>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#e0f2fe" stroke="#1e3a8a" stroke-width="2"/>\n'
    # แกนหมุนโลกและแกนแม่เหล็ก
    s += f'<line x1="{cx}" y1="{cy-R-30}" x2="{cx}" y2="{cy+R+30}" stroke="#334155" stroke-width="1.5" stroke-dasharray="6 4"/>\n'
    s += f'<text x="{cx+6}" y="{cy-R-34}" font-size="12" fill="#334155">ขั้วโลกเหนือ (ภูมิศาสตร์) / แกนหมุนโลก</text>\n'
    s += f'<line x1="{cx - (R+22)*ax:.1f}" y1="{cy - (R+22)*ay:.1f}" x2="{cx + (R+22)*ax:.1f}" y2="{cy + (R+22)*ay:.1f}" stroke="#b91c1c" stroke-width="1.5"/>\n'
    nmx, nmy = cx + R * ax, cy + R * ay
    s += f'<circle cx="{nmx:.1f}" cy="{nmy:.1f}" r="5" fill="#b91c1c"/>\n'
    s += f'<text x="{nmx-255:.1f}" y="{nmy-52:.1f}" font-size="12" fill="#b91c1c">ขั้วแม่เหล็กเหนือ (ทางฟิสิกส์เป็นขั้ว S)</text>\n'
    s += f'<line x1="{nmx-55:.1f}" y1="{nmy-48:.1f}" x2="{nmx-3:.1f}" y2="{nmy-6:.1f}" stroke="#b91c1c"/>\n'
    s += f'<text x="{cx - R*ax - 60:.1f}" y="{cy - R*ay + 22:.1f}" font-size="12" fill="#b91c1c">ขั้วแม่เหล็กใต้</text>\n'
    # magnetic equator
    s += f'<line x1="{cx - R*px:.1f}" y1="{cy - R*py:.1f}" x2="{cx + R*px:.1f}" y2="{cy + R*py:.1f}" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="7 4"/>\n'
    s += f'<text x="{cx - R*px + 8:.1f}" y="{cy - R*py + 18:.1f}" font-size="12" fill="#b45309" font-weight="bold">magnetic equator (dip = 0°)</text>\n'
    # เวกเตอร์สนามที่ผิวโลก 3 จุด (ฝั่งขวา) — tan(dip) = 2 tan(lat แม่เหล็ก)
    for lam_deg, lab in ((0, 'A'), (45, 'B'), (75, 'C')):
        lam = math.radians(lam_deg)
        ux, uy = math.sin(lam) * ax + math.cos(lam) * px, math.sin(lam) * ay + math.cos(lam) * py
        nx, ny = math.cos(lam) * ax - math.sin(lam) * px, math.cos(lam) * ay - math.sin(lam) * py
        dip = math.atan(2 * math.tan(lam))
        vx, vy = math.cos(dip) * nx - math.sin(dip) * ux, math.cos(dip) * ny - math.sin(dip) * uy
        sx, sy = cx + R * ux, cy + R * uy
        s += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4" fill="#0f172a"/>\n'
        s += f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{sx + 48*vx:.1f}" y2="{sy + 48*vy:.1f}" stroke="#15803d" stroke-width="3" marker-end="url(#a)"/>\n'
        s += f'<text x="{sx + 12*ux + 6:.1f}" y="{sy + 12*uy + 4:.1f}" font-size="14" font-weight="bold" fill="#0f172a">{lab}</text>\n'
    s += f'<text x="40" y="520" font-size="12" fill="#334155">ลูกศรเขียว = ทิศของสนามที่ผิวโลก: A ศูนย์สูตรแม่เหล็ก (แนวราบ), B ละติจูดแม่เหล็ก ~45° (dip ~63°), C ใกล้ขั้ว (dip ~82°)</text>\n'
    s += f'<text x="40" y="540" font-size="12" fill="#334155">ซีกโลกเหนือปลายเหนือของเข็มถูกดึงลง (dip ลง) · ซีกโลกใต้ดึงขึ้น · แกนแม่เหล็กเอียงจากแกนหมุนโลก ~10° (ภาพไม่ตามสเกล)</text>\n'
    # แผนภาพเวกเตอร์ T, H, Z
    ox, oy = 640, 150
    dip = math.radians(50); T = 235
    hx, zy = ox + T * math.cos(dip), oy + T * math.sin(dip)
    s += f'<line x1="{ox}" y1="{oy}" x2="{hx:.1f}" y2="{oy}" stroke="#1d4ed8" stroke-width="3.5" marker-end="url(#a)"/>\n'
    s += f'<line x1="{hx:.1f}" y1="{oy}" x2="{hx:.1f}" y2="{zy:.1f}" stroke="#b91c1c" stroke-width="3.5" marker-end="url(#a)"/>\n'
    s += f'<line x1="{ox}" y1="{oy}" x2="{hx:.1f}" y2="{zy:.1f}" stroke="#15803d" stroke-width="4" marker-end="url(#a)"/>\n'
    s += f'<path d="M {ox+70} {oy} A 70 70 0 0 1 {ox + 70*math.cos(dip):.1f} {oy + 70*math.sin(dip):.1f}" fill="none" stroke="#0f172a" stroke-width="1.5"/>\n'
    s += f'<text x="{ox+76}" y="{oy+38}" font-size="14" font-weight="bold">θ (dip)</text>\n'
    s += f'<text x="{ox+20}" y="{oy-12}" font-size="14" font-weight="bold" fill="#1d4ed8">H — แรงแนวราบ (ชี้ magnetic north)</text>\n'
    s += f'<text x="{hx+10:.1f}" y="{(oy+zy)/2:.1f}" font-size="14" font-weight="bold" fill="#b91c1c">Z — แรงแนวดิ่ง</text>\n'
    s += f'<text x="{ox+20}" y="{(oy+zy)/2+60:.1f}" font-size="14" font-weight="bold" fill="#15803d">T — total force</text>\n'
    s += '<rect x="560" y="410" width="385" height="96" rx="8" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['H = T cos θ · Z = T sin θ · tan θ = Z / H',
                           'H มากสุดใกล้ magnetic equator → เข็มทิศเสถียรสุด',
                           'ใกล้ขั้วแม่เหล็ก H → 0 → เข็มทิศแม่เหล็กใช้ไม่ได้ดี',
                           'Z เปลี่ยนตามละติจูด → Flinders bar/heeling magnet']):
        s += f'<text x="574" y="{434 + i*21}" font-size="13">{t}</text>\n'
    save('compass-earth-field.svg', s)

def binnacle():
    w, h = 900, 560
    s = head(w, h, 'Binnacle และตัวแก้ Deviation')
    cx = 400
    s += f'<rect x="{cx-70}" y="200" width="140" height="300" rx="12" fill="#e2e8f0" stroke="#475569" stroke-width="2"/>\n'
    s += f'<ellipse cx="{cx}" cy="150" rx="95" ry="30" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>\n'
    s += f'<path d="M {cx-95} 150 L {cx-80} 205 L {cx+80} 205 L {cx+95} 150" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>\n'
    s += f'<ellipse cx="{cx}" cy="140" rx="70" ry="20" fill="#fef3c7" stroke="#92400e"/>\n'
    s += f'<text x="{cx}" y="145" text-anchor="middle" font-size="12" fill="#92400e">compass bowl</text>\n'
    s += f'<rect x="{cx-12}" y="60" width="24" height="60" fill="#94a3b8"/><text x="{cx+20}" y="80" font-size="12">azimuth circle / hood</text>\n'
    # quadrantal spheres
    for x in (cx - 150, cx + 150):
        s += f'<circle cx="{x}" cy="160" r="34" fill="#64748b" stroke="#1e293b" stroke-width="2"/>\n'
        s += f'<line x1="{x + (34 if x < cx else -34)}" y1="160" x2="{cx + (-95 if x < cx else 95)}" y2="155" stroke="#475569" stroke-width="6"/>\n'
    s += f'<text x="{cx-230}" y="215" font-size="13" font-weight="bold">Quadrantal spheres</text><text x="{cx-230}" y="233" font-size="12">(soft iron) → แก้ D, E</text>\n'
    # flinders bar
    s += f'<rect x="{cx-30}" y="230" width="60" height="150" fill="#94a3b8" opacity="0.5" stroke="#475569" stroke-dasharray="4 3"/>\n'
    s += f'<rect x="{cx+90}" y="230" width="26" height="170" rx="6" fill="#0f172a"/><text x="{cx+125}" y="300" font-size="13" font-weight="bold">Flinders bar</text><text x="{cx+125}" y="318" font-size="12">(vertical soft iron) → แก้ B ส่วน induced</text>\n'
    # magnets trays
    for i, y in enumerate((300, 330, 360)):
        s += f'<rect x="{cx-60}" y="{y}" width="50" height="8" fill="#dc2626"/><rect x="{cx+10}" y="{y}" width="50" height="8" fill="#2563eb"/>\n'
    s += f'<text x="{cx-330}" y="320" font-size="13" font-weight="bold">Fore-and-aft magnets → แก้ B</text><text x="{cx-330}" y="340" font-size="13" font-weight="bold">Athwartship magnets → แก้ C</text>\n'
    s += f'<line x1="{cx-110}" y1="330" x2="{cx-62}" y2="330" stroke="#334155"/>\n'
    s += f'<rect x="{cx-6}" y="215" width="12" height="70" fill="#7c3aed"/><text x="{cx-330}" y="260" font-size="13" font-weight="bold">Heeling error magnet (bucket)</text><text x="{cx-330}" y="278" font-size="12">แนวดิ่งใต้เข็มทิศ → แก้ heeling error</text>\n'
    s += f'<line x1="{cx-110}" y1="262" x2="{cx-8}" y2="250" stroke="#334155"/>\n'
    s += f'<text x="{cx}" y="530" text-anchor="middle" font-size="13" fill="#334155">Coefficient A → แก้ด้วยการวางแนว lubber line/เข็มทิศให้ตรงแนวหัวเรือ (ไม่ใช้แม่เหล็ก)</text>\n'
    save('compass-binnacle.svg', s)

def dev_curve():
    w, h = 900, 440
    s = head(w, h, 'Deviation Curve (ตัวอย่างจำลอง)')
    x0, x1, y0, ymid = 80, 860, 70, 220; sc = 35
    s += f'<line x1="{x0}" y1="{ymid}" x2="{x1}" y2="{ymid}" stroke="#0f172a" stroke-width="1.5"/>\n'
    for d in range(-4, 5):
        y = ymid - d * sc
        s += f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#e2e8f0"/><text x="{x0-40}" y="{y+4}" font-size="12">{abs(d)}°{"E" if d>0 else ("W" if d<0 else "")}</text>\n'
    for hd in range(0, 361, 30):
        x = x0 + hd / 360 * (x1 - x0)
        s += f'<line x1="{x:.1f}" y1="{ymid-150}" x2="{x:.1f}" y2="{ymid+150}" stroke="#f1f5f9"/><text x="{x-12:.1f}" y="{ymid+175}" font-size="12">{hd:03d}</text>\n'
    A, B, C, D, E = 0.2, 2.5, -1.5, 0.8, 0.2
    pts = []
    for i in range(0, 361, 3):
        t = math.radians(i); dv = A + B*math.sin(t) + C*math.cos(t) + D*math.sin(2*t) + E*math.cos(2*t)
        pts.append((x0 + i / 360 * (x1 - x0), ymid - dv * sc))
    s += '<path d="M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in pts) + '" fill="none" stroke="#b91c1c" stroke-width="3"/>\n'
    for i in range(0, 360, 30):
        t = math.radians(i); dv = A + B*math.sin(t) + C*math.cos(t) + D*math.sin(2*t) + E*math.cos(2*t)
        s += f'<circle cx="{x0 + i/360*(x1-x0):.1f}" cy="{ymid - dv*sc:.1f}" r="4" fill="#b91c1c"/>\n'
    hx = x0 + 158 / 360 * (x1 - x0)
    s += f'<line x1="{hx:.1f}" y1="{ymid+150}" x2="{hx:.1f}" y2="{ymid-2.1*sc:.1f}" stroke="#1d4ed8" stroke-dasharray="5 4" stroke-width="2"/><text x="{hx+6:.1f}" y="{ymid-2.1*sc-10:.1f}" font-size="13" fill="#1d4ed8" font-weight="bold">หัวเรือ 158°C → Dev ≈ 2.1°E</text>\n'
    s += f'<text x="{(x0+x1)/2}" y="{ymid+200}" text-anchor="middle" font-size="13">Ship\'s head (compass) — Dev = A + B sinθ + C cosθ + D sin2θ + E cos2θ</text>\n'
    save('compass-deviation-curve.svg', s)

def gyro_principles():
    w, h = 960, 480
    s = head(w, h, 'ไจโรสโคป: Rigidity in space และ Precession')
    cx, cy = 240, 260
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="170" ry="170" fill="none" stroke="#94a3b8" stroke-width="6"/>\n'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="60" ry="150" fill="none" stroke="#64748b" stroke-width="6"/>\n'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="150" ry="42" fill="none" stroke="#475569" stroke-width="5"/>\n'
    # rotor = จานหมุนในระนาบตั้งฉากกับ spin axis (มองเกือบด้านข้างจึงเห็นเป็นวงรีแคบ)
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="26" ry="95" fill="#1e3a8a" stroke="#0f172a" stroke-width="2"/>\n'
    s += f'<path d="M {cx-30} {cy-70} q -22 70 0 140" fill="none" stroke="#f59e0b" stroke-width="2.5" marker-end="url(#a)"/>\n'
    s += f'<line x1="{cx-170}" y1="{cy}" x2="{cx+170}" y2="{cy}" stroke="#b91c1c" stroke-width="3"/>\n'
    s += f'<text x="{cx+175}" y="{cy+5}" font-size="13" fill="#b91c1c" font-weight="bold">spin axis</text>\n'
    s += f'<line x1="{cx}" y1="{cy-200}" x2="{cx}" y2="{cy+200}" stroke="#15803d" stroke-width="2" stroke-dasharray="5 4"/><text x="{cx+6}" y="{cy-205}" font-size="12" fill="#15803d">vertical axis</text>\n'
    s += f'<line x1="{cx+178}" y1="{cy-62}" x2="{cx+22}" y2="{cy-45}" stroke="#1e3a8a" stroke-width="1"/>\n'
    s += f'<text x="{cx+180}" y="{cy-64}" font-size="12" fill="#1e3a8a" font-weight="bold">rotor (หมุนเร็วมาก)</text>\n'
    s += f'<text x="{cx+180}" y="{cy-48}" font-size="11" fill="#475569">จานตั้งฉากกับ spin axis</text>\n'
    s += f'<text x="{cx-150}" y="{cy+215}" font-size="13">gimbals ให้อิสระ 3 แกน (free gyroscope)</text>\n'
    # precession panel
    px, py = 700, 250
    s += f'<ellipse cx="{px}" cy="{py}" rx="120" ry="45" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>\n'
    s += f'<path d="M {px+80} {py-38} q 30 5 40 25" fill="none" stroke="#1d4ed8" stroke-width="2" marker-end="url(#a)"/><text x="{px+95}" y="{py-48}" font-size="12" fill="#1d4ed8">ทิศการหมุน</text>\n'
    s += f'<line x1="{px}" y1="{py+45}" x2="{px}" y2="{py+120}" stroke="#b91c1c" stroke-width="4" marker-end="url(#a)"/><text x="{px+10}" y="{py+110}" font-size="13" fill="#b91c1c" font-weight="bold">แรงที่กระทำ (torque)</text>\n'
    s += f'<line x1="{px}" y1="{py}" x2="{px}" y2="{py-80}" stroke="#0f172a" stroke-width="2.5" stroke-dasharray="5 3"/><text x="{px+6}" y="{py-70}" font-size="11" fill="#0f172a">spin axis</text>\n'
    s += f'<line x1="{px-120}" y1="{py}" x2="{px-120}" y2="{py+75}" stroke="#15803d" stroke-width="4" marker-end="url(#a)"/><text x="{px-300}" y="{py+100}" font-size="13" fill="#15803d" font-weight="bold">ผลจริงเกิดที่จุดนี้ (ห่าง 90°)</text><text x="{px-300}" y="{py+118}" font-size="12" fill="#15803d">→ ขอบซ้ายกดลง แกนหมุนเอียง (precession)</text>\n'
    s += f'<text x="{px-160}" y="{py-90}" font-size="14" font-weight="bold">Precession: เคลื่อน 90° ตามทิศการหมุน</text>\n'
    s += f'<text x="{px-160}" y="{py+170}" font-size="13">อัตรา precession ∝ แรงบิด / โมเมนตัมเชิงมุม</text>\n'
    s += f'<text x="{px-160}" y="{py+192}" font-size="13">Free gyro บนโลก: drift = 15° sin L /ชม., tilt = 15° cos L /ชม.</text>\n'
    save('gyro-principles.svg', s)

def gyro_settling():
    w, h = 900, 460
    s = head(w, h, 'การเคลื่อนที่ของปลายเหนือของแกนไจโร (มองไปทางทิศเหนือ)')
    def panel(cx, title, damp):
        out = f'<text x="{cx}" y="70" text-anchor="middle" font-size="15" font-weight="bold">{title}</text>\n'
        cy = 250
        out += f'<line x1="{cx-180}" y1="{cy}" x2="{cx+180}" y2="{cy}" stroke="#94a3b8"/><text x="{cx+150}" y="{cy-6}" font-size="11">horizon</text>\n'
        out += f'<line x1="{cx}" y1="{cy-150}" x2="{cx}" y2="{cy+150}" stroke="#15803d" stroke-dasharray="5 4"/><text x="{cx+4}" y="{cy-155}" font-size="12" fill="#15803d">meridian (N)</text>\n'
        pts = []
        for i in range(0, 1200):
            t = i / 100
            amp = math.exp(-0.18 * t) if damp else 1
            x = cx + 150 * amp * math.cos(t)
            y = cy - 60 * amp * math.sin(t) - (8 if damp else 0) * (1 - amp)
            pts.append((x, y))
            if not damp and t > 6.4: break
        out += '<path d="M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in pts) + f'" fill="none" stroke="{"#1d4ed8" if damp else "#b91c1c"}" stroke-width="2.5"/>\n'
        out += f'<text x="{cx-170}" y="{cy+110}" font-size="12">W ←</text><text x="{cx+140}" y="{cy+110}" font-size="12">→ E</text>\n'
        return out
    s += panel(220, 'ไม่มี damping: แกว่งเป็นวงรีไม่หยุด', False)
    s += panel(670, 'มี damping: เกลียวเข้าหาจุดตั้ง (settle)', True)
    s += '<text x="450" y="420" text-anchor="middle" font-size="13" fill="#334155">คาบการแกว่งออกแบบ ≈ 84.4 นาที (Schuler period) · gyro กลไกต้องเปิดล่วงหน้าหลายชั่วโมงก่อนออกเรือ</text>\n'
    save('gyro-settling.svg', s)

if __name__ == '__main__':
    earth_field(); tvmdc(); binnacle(); dev_curve(); gyro_principles(); gyro_settling(); print('ok')
