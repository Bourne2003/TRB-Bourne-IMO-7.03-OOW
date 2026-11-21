"""สคริปต์สร้างภาพประกอบบทน้ำขึ้นน้ำลง"""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
def head(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="m" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0f172a"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{title}</text>\n')
def save(n, s): open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')

def springs_neaps():
    w, h = 960, 440
    s = head(w, h, 'น้ำเกิด (Springs) และน้ำตาย (Neaps)')
    def panel(cx, title, moon_angles, ellipse_angle, rx, ry, note):
        out = f'<text x="{cx}" y="70" text-anchor="middle" font-size="16" font-weight="bold">{title}</text>\n'
        cy = 230
        out += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#bfdbfe" opacity="0.8" transform="rotate({ellipse_angle} {cx} {cy})"/>\n'
        out += f'<circle cx="{cx}" cy="{cy}" r="38" fill="#16a34a" stroke="#14532d" stroke-width="2"/><text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">โลก</text>\n'
        for ang, lab in moon_angles:
            a = math.radians(ang); mx = cx + 115 * math.cos(a); my = cy - 115 * math.sin(a)
            out += f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="14" fill="#e5e7eb" stroke="#374151" stroke-width="2"/><text x="{mx+20:.1f}" y="{my+5:.1f}" font-size="12">{lab}</text>\n'
        out += f'<text x="{cx}" y="400" text-anchor="middle" font-size="13" fill="#334155">{note}</text>\n'
        return out
    # sun on left
    s += '<circle cx="40" cy="220" r="30" fill="#facc15" stroke="#b45309" stroke-width="2"/><text x="40" y="270" text-anchor="middle" font-size="13" font-weight="bold">ดวงอาทิตย์</text>\n'
    s += '<line x1="75" y1="220" x2="130" y2="220" stroke="#b45309" stroke-width="2" stroke-dasharray="5 4"/>\n'
    s += panel(320, 'SPRINGS — จันทร์ดับ / จันทร์เพ็ญ', [(0, 'จันทร์เพ็ญ'), (180, 'จันทร์ดับ')], 0, 105, 58, 'แรงดวงอาทิตย์ + ดวงจันทร์เสริมกัน → range มาก')
    # viewed from above the North Pole the Moon orbits anticlockwise: with the Sun to the left,
    # first quarter (ข้างขึ้น 8 ค่ำ) is below the Earth and last quarter (ข้างแรม 8 ค่ำ) above it
    s += panel(720, 'NEAPS — จันทร์ครึ่งดวง', [(90, 'ข้างแรม 8 ค่ำ (last quarter)'), (270, 'ข้างขึ้น 8 ค่ำ (first quarter)')], 90, 82, 66, 'แรงตั้งฉากกัน หักล้างบางส่วน → range น้อย')
    s += '<text x="492" y="182" font-size="12" fill="#b45309">← ดวงอาทิตย์อยู่ทางซ้าย</text>\n'
    s += '<text x="480" y="424" text-anchor="middle" font-size="11" fill="#64748b">มองจากเหนือขั้วโลกเหนือ ดวงจันทร์โคจรทวนเข็มนาฬิกา (จันทร์ดับ → ขึ้น 8 ค่ำ → เพ็ญ → แรม 8 ค่ำ) · ภาพไม่ได้ตามมาตราส่วน</text>\n'
    s += '<line x1="480" y1="60" x2="480" y2="400" stroke="#e2e8f0" stroke-width="2"/>\n'
    save('tide-springs-neaps.svg', s)

def curve_terms():
    w, h = 960, 460
    s = head(w, h, 'เส้นโค้งน้ำขึ้นลงและนิยาม (semi-diurnal)')
    x0, x1, yCD = 80, 900, 380; sc = 70  # px per metre
    s += f'<line x1="{x0}" y1="{yCD}" x2="{x1}" y2="{yCD}" stroke="#b91c1c" stroke-width="2" stroke-dasharray="8 5"/><text x="{x1-110}" y="{yCD+20}" font-size="13" fill="#b91c1c" font-weight="bold">Chart Datum</text>\n'
    pts = []
    for i in range(0, 821, 4):
        t = i / 820 * 25  # hours
        hgt = 2.3 + 1.6 * math.cos(2 * math.pi * (t - 3) / 12.42)
        pts.append((x0 + i, yCD - hgt * sc))
    d = 'M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in pts)
    s += f'<path d="{d}" fill="none" stroke="#1d4ed8" stroke-width="3"/>\n'
    # HW at t=3 ; LW at t=9.21 ; HW at 15.42
    def xy(t):
        hgt = 2.3 + 1.6 * math.cos(2 * math.pi * (t - 3) / 12.42); return x0 + t / 25 * 820, yCD - hgt * sc
    hwx, hwy = xy(3); lwx, lwy = xy(9.21); hw2x, hw2y = xy(15.42)
    s += f'<circle cx="{hwx:.1f}" cy="{hwy:.1f}" r="5" fill="#1d4ed8"/><text x="{hwx-20:.1f}" y="{hwy-12:.1f}" font-size="14" font-weight="bold">HW</text>\n'
    s += f'<circle cx="{lwx:.1f}" cy="{lwy:.1f}" r="5" fill="#1d4ed8"/><text x="{lwx-18:.1f}" y="{lwy+22:.1f}" font-size="14" font-weight="bold">LW</text>\n'
    s += f'<circle cx="{hw2x:.1f}" cy="{hw2y:.1f}" r="5" fill="#1d4ed8"/><text x="{hw2x-20:.1f}" y="{hw2y-12:.1f}" font-size="14" font-weight="bold">HW</text>\n'
    # range arrow
    s += f'<line x1="{lwx+60:.1f}" y1="{hwy:.1f}" x2="{lwx+60:.1f}" y2="{lwy:.1f}" stroke="#0f172a" stroke-width="1.6" marker-start="url(#m)" marker-end="url(#m)"/><text x="{lwx+54:.1f}" y="{(hwy+lwy)/2:.1f}" text-anchor="end" font-size="13" font-weight="bold">Range</text>\n'
    s += f'<line x1="{hwx:.1f}" y1="{hwy:.1f}" x2="{lwx+80:.1f}" y2="{hwy:.1f}" stroke="#94a3b8" stroke-dasharray="3 3"/>\n'
    # height of tide at t=12
    tx, ty = xy(12.3)
    s += f'<line x1="{tx:.1f}" y1="{yCD}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="#15803d" stroke-width="2" marker-start="url(#m)" marker-end="url(#m)"/><text x="{tx+8:.1f}" y="{(yCD+ty)/2+20:.1f}" font-size="13" fill="#15803d" font-weight="bold">Height of tide</text>\n'
    # duration
    s += f'<line x1="{hwx:.1f}" y1="420" x2="{lwx:.1f}" y2="420" stroke="#7c3aed" stroke-width="1.6" marker-start="url(#m)" marker-end="url(#m)"/><text x="{(hwx+lwx)/2-50:.1f}" y="440" font-size="13" fill="#7c3aed" font-weight="bold">Duration of fall</text>\n'
    s += f'<line x1="{lwx:.1f}" y1="420" x2="{hw2x:.1f}" y2="420" stroke="#ea580c" stroke-width="1.6" marker-start="url(#m)" marker-end="url(#m)"/><text x="{(lwx+hw2x)/2-50:.1f}" y="440" font-size="13" fill="#ea580c" font-weight="bold">Duration of rise</text>\n'
    s += f'<text x="{hwx-40:.1f}" y="{hwy-34:.1f}" font-size="12" fill="#475569">stand</text>\n'
    s += '<text x="620" y="70" font-size="13" fill="#334155">≈ 12 ชม. 25 นาที ต่อรอบ (semi-diurnal)</text>\n'
    save('tide-curve-terms.svg', s)

def standard_curve():
    w, h = 980, 520
    s = head(w, h, 'การใช้ Standard Port Tidal Curve (ตัวอย่างจำลอง Port A)')
    # left height grid
    gx0, gx1, gy0, gy1 = 50, 330, 110, 420
    s += f'<rect x="{gx0}" y="{gy0}" width="{gx1-gx0}" height="{gy1-gy0}" fill="#f8fafc" stroke="#94a3b8"/>\n'
    s += f'<text x="{gx0}" y="{gy0-10}" font-size="13" font-weight="bold">HW heights (m)</text><text x="{gx0}" y="{gy1+22}" font-size="13" font-weight="bold">LW heights (m)</text>\n'
    def hx(hgt): return gx0 + (hgt / 5.0) * (gx1 - gx0)
    for m in range(0, 6):
        x = hx(m)
        s += f'<line x1="{x:.1f}" y1="{gy0}" x2="{x:.1f}" y2="{gy1}" stroke="#e2e8f0"/><text x="{x-4:.1f}" y="{gy0-26}" font-size="11">{m}</text><text x="{x-4:.1f}" y="{gy1+40}" font-size="11">{m}</text>\n'
    for f in range(0, 11):
        y = gy1 - f / 10 * (gy1 - gy0)
        s += f'<line x1="{gx0}" y1="{y:.1f}" x2="{gx1}" y2="{y:.1f}" stroke="#e2e8f0"/><text x="{gx1+4}" y="{y+4:.1f}" font-size="10" fill="#64748b">{f/10:.1f}</text>\n'
    HWh, LWh = 4.0, 0.8
    s += f'<line x1="{hx(HWh):.1f}" y1="{gy0}" x2="{hx(LWh):.1f}" y2="{gy1}" stroke="#b91c1c" stroke-width="2.5"/>\n'
    s += f'<text x="{hx(HWh)-30:.1f}" y="{gy0-46}" font-size="12" fill="#b91c1c" font-weight="bold">HW 4.0</text><text x="{hx(LWh)-10:.1f}" y="{gy1+58}" font-size="12" fill="#b91c1c" font-weight="bold">LW 0.8</text>\n'
    # curve panel
    cx0, cx1 = 400, 940
    s += f'<rect x="{cx0}" y="{gy0}" width="{cx1-cx0}" height="{gy1-gy0}" fill="#f8fafc" stroke="#94a3b8"/>\n'
    def tx(t): return cx0 + (t + 6) / 12 * (cx1 - cx0)
    for t in range(-6, 7):
        x = tx(t)
        s += f'<line x1="{x:.1f}" y1="{gy0}" x2="{x:.1f}" y2="{gy1}" stroke="#e2e8f0"/><text x="{x:.1f}" y="{gy1+22}" text-anchor="middle" font-size="11">{"HW" if t == 0 else ("%+d" % t)}</text>\n'
    def fac(t, T):
        return 0.5 * (1 + math.cos(math.pi * t / T))
    for T, col, lab in [(6.43, '#1d4ed8', 'Springs'), (6.0, '#0891b2', 'Neaps')]:
        pts = []
        for i in range(0, 241):
            t = -6 + i * 12 / 240
            Tt = T if t > 0 else 6.2
            f = fac(max(-Tt, min(Tt, t)), Tt)
            if col == '#0891b2': f = 0.5 + (f - 0.5) * 0.97
            pts.append((tx(t), gy1 - f * (gy1 - gy0)))
        d = 'M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in pts)
        dash = '' if lab == 'Springs' else ' stroke-dasharray="7 4"'
        s += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2.5"{dash}/>\n'
    s += f'<text x="{tx(-5.5):.1f}" y="{gy0+40}" font-size="12" fill="#1d4ed8" font-weight="bold">— Springs</text><text x="{tx(-5.5):.1f}" y="{gy0+58}" font-size="12" fill="#0891b2" font-weight="bold">- - Neaps</text>\n'
    # example at HW+3h18m
    t = 3.3; f = 0.48
    x = tx(t); y = gy1 - f * (gy1 - gy0)
    s += f'<line x1="{x:.1f}" y1="{gy1}" x2="{x:.1f}" y2="{y:.1f}" stroke="#15803d" stroke-width="2" stroke-dasharray="5 3"/>\n'
    s += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{gx1:.1f}" y2="{y:.1f}" stroke="#15803d" stroke-width="2" stroke-dasharray="5 3"/>\n'
    # intersection with HW-LW line on left
    hgt = LWh + f * (HWh - LWh)
    lx = hx(LWh) + (hx(HWh) - hx(LWh)) * f
    s += f'<line x1="{gx1}" y1="{y:.1f}" x2="{lx:.1f}" y2="{y:.1f}" stroke="#15803d" stroke-width="2" stroke-dasharray="5 3"/>\n'
    s += f'<line x1="{lx:.1f}" y1="{y:.1f}" x2="{lx:.1f}" y2="{gy0}" stroke="#15803d" stroke-width="2" stroke-dasharray="5 3"/>\n'
    s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#15803d"/><circle cx="{lx:.1f}" cy="{y:.1f}" r="5" fill="#15803d"/>\n'
    s += f'<text x="{x-200:.1f}" y="{y-10:.1f}" font-size="13" fill="#15803d" font-weight="bold">HW+3h18m → factor 0.48</text>\n'
    s += f'<text x="{lx+6:.1f}" y="{gy0+16}" font-size="13" fill="#15803d" font-weight="bold">≈ 2.3 m</text>\n'
    s += f'<text x="{cx0}" y="{gy1+48}" font-size="12" fill="#334155">เวลาเทียบกับ HW (ชั่วโมง) · factor: 1.0 = HW, 0 = LW</text>\n'
    s += f'<text x="{cx0}" y="{gy1+68}" font-size="12" fill="#334155">Height = LW + factor × range = 0.8 + 0.48 × 3.2 ≈ 2.3 m</text>\n'
    s += f'<text x="{cx0+4}" y="{gy0-10}" font-size="12" fill="#64748b">(เส้นโค้งจำลองเพื่ออธิบายวิธีใช้ ไม่ใช่ curve ของท่าจริง)</text>\n'
    save('tide-standard-curve.svg', s)

def twelfths():
    w, h = 1010, 420
    s = head(w, h, 'Rule of Twelfths — ระดับน้ำที่เปลี่ยนในแต่ละชั่วโมง')
    x0, y0, bw = 120, 360, 100; sc = 22
    parts = [1, 2, 3, 3, 2, 1]
    cum = 0
    for i, p in enumerate(parts):
        x = x0 + i * bw
        s += f'<rect x="{x+10}" y="{y0 - p*sc*3}" width="{bw-20}" height="{p*sc*3}" fill="#93c5fd" stroke="#1d4ed8"/>\n'
        s += f'<text x="{x+bw/2}" y="{y0 - p*sc*3 - 8}" text-anchor="middle" font-size="16" font-weight="bold" fill="#1e3a8a">{p}/12</text>\n'
        s += f'<text x="{x+bw/2}" y="{y0+22}" text-anchor="middle" font-size="13">ชม. {i+1}</text>\n'
        cum += p
        s += f'<text x="{x+bw/2}" y="{y0+44}" text-anchor="middle" font-size="12" fill="#475569">สะสม {cum}/12</text>\n'
    s += f'<line x1="{x0}" y1="{y0}" x2="{x0+6*bw}" y2="{y0}" stroke="#0f172a" stroke-width="2"/>\n'
    s += '<text x="740" y="120" font-size="13">ตัวอย่าง: LW 0.8 m, range 3.0 m</text><text x="740" y="142" font-size="13">หลัง LW 2 ชม. ≈ 0.8 + 3/12×3.0</text><text x="740" y="164" font-size="13">≈ 1.55 m</text>\n'
    s += '<text x="740" y="200" font-size="12" fill="#b91c1c">ใช้กับ semi-diurnal ที่สม่ำเสมอ</text><text x="740" y="218" font-size="12" fill="#b91c1c">เท่านั้น (ไม่ใช้ในอ่าวไทย</text><text x="740" y="236" font-size="12" fill="#b91c1c">ส่วนใหญ่ที่เป็น diurnal/mixed)</text>\n'
    save('tide-rule-of-twelfths.svg', s)

def ukc_window():
    """Tidal window for a shoal (simulated example, Port A, cosine-shaped curve assumed)."""
    w, h = 980, 540
    s = head(w, h, 'Tidal window สำหรับผ่านจุดตื้น (ตัวอย่างจำลอง MV Andaman Star)')
    gx0, gx1, gy0, gy1 = 70, 650, 70, 440
    t0, t1 = 2.0, 18.0
    def X(t): return gx0 + (t - t0) / (t1 - t0) * (gx1 - gx0)
    def Y(hh): return gy1 - hh / 5.0 * (gy1 - gy0)
    LW1t, HWt, LW2t = 3 + 25 / 60, 9 + 42 / 60, 16 + 8 / 60
    LW1, HW, LW2 = 0.7, 4.0, 0.8
    def height(t):
        if t <= LW1t: return LW1
        if t <= HWt:
            T = HWt - LW1t; f = 0.5 * (1 + math.cos(math.pi * (HWt - t) / T)); return LW1 + f * (HW - LW1)
        if t <= LW2t:
            T = LW2t - HWt; f = 0.5 * (1 + math.cos(math.pi * (t - HWt) / T)); return LW2 + f * (HW - LW2)
        return LW2
    req = 3.4
    # solve window
    def solve(a, b, rising):
        for _ in range(60):
            m = (a + b) / 2
            if (height(m) < req) == rising: a = m
            else: b = m
        return (a + b) / 2
    ws = solve(LW1t, HWt, True); we = solve(HWt, LW2t, False)
    def hhmm(t):
        mm = int(round(t * 60)); return f'{mm//60:02d}{mm%60:02d}'
    s += f'<rect x="{gx0}" y="{gy0}" width="{gx1-gx0}" height="{gy1-gy0}" fill="#f8fafc" stroke="#94a3b8"/>\n'
    s += f'<rect x="{X(ws):.1f}" y="{gy0}" width="{X(we)-X(ws):.1f}" height="{gy1-gy0}" fill="#bbf7d0" opacity="0.7"/>\n'
    for t in range(2, 19, 2):
        s += f'<line x1="{X(t):.1f}" y1="{gy0}" x2="{X(t):.1f}" y2="{gy1}" stroke="#e2e8f0"/><text x="{X(t):.1f}" y="{gy1+18}" text-anchor="middle" font-size="11">{t:02d}00</text>\n'
    for m in range(0, 6):
        s += f'<line x1="{gx0}" y1="{Y(m):.1f}" x2="{gx1}" y2="{Y(m):.1f}" stroke="#e2e8f0"/><text x="{gx0-8}" y="{Y(m)+4:.1f}" text-anchor="end" font-size="11">{m}</text>\n'
    s += f'<text x="22" y="{(gy0+gy1)/2}" text-anchor="middle" font-size="12" font-weight="bold" transform="rotate(-90 22 {(gy0+gy1)/2})">Height of tide เหนือ CD (m)</text>\n'
    s += f'<text x="{(gx0+gx1)/2}" y="{gy1+38}" text-anchor="middle" font-size="12" font-weight="bold">เวลา (zone time ของ Port A)</text>\n'
    pts = [(X(t0 + i * (t1 - t0) / 320), Y(height(t0 + i * (t1 - t0) / 320))) for i in range(321)]
    s += '<path d="M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in pts) + '" fill="none" stroke="#1d4ed8" stroke-width="3"/>\n'
    s += f'<line x1="{gx0}" y1="{Y(req):.1f}" x2="{gx1}" y2="{Y(req):.1f}" stroke="#b91c1c" stroke-width="2" stroke-dasharray="8 4"/>\n'
    s += f'<text x="{gx1-6}" y="{Y(req)-6:.1f}" text-anchor="end" font-size="12" fill="#b91c1c" font-weight="bold">ระดับน้ำที่ต้องการ 3.4 m</text>\n'
    for t, hh, lab, dy in [(LW1t, LW1, 'LW 0325 0.7 m', 18), (HWt, HW, 'HW 0942 4.0 m', -10), (LW2t, LW2, 'LW 1608 0.8 m', 18)]:
        s += f'<circle cx="{X(t):.1f}" cy="{Y(hh):.1f}" r="4" fill="#1d4ed8"/><text x="{X(t):.1f}" y="{Y(hh)+dy:.1f}" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e3a8a">{lab}</text>\n'
    for t in (ws, we):
        s += f'<line x1="{X(t):.1f}" y1="{Y(req):.1f}" x2="{X(t):.1f}" y2="{gy1}" stroke="#15803d" stroke-width="2"/><circle cx="{X(t):.1f}" cy="{Y(req):.1f}" r="4" fill="#15803d"/>\n'
    s += f'<text x="{(X(ws)+X(we))/2:.1f}" y="{gy1-40}" text-anchor="middle" font-size="13" fill="#166534" font-weight="bold">tidal window</text>\n'
    s += f'<text x="{(X(ws)+X(we))/2:.1f}" y="{gy1-22}" text-anchor="middle" font-size="13" fill="#166534" font-weight="bold">≈ {hhmm(ws)}–{hhmm(we)}</text>\n'
    t13 = 13.0
    s += f'<circle cx="{X(t13):.1f}" cy="{Y(height(t13)):.1f}" r="5" fill="#b91c1c"/><text x="{X(t13)+8:.1f}" y="{Y(height(t13))+4:.1f}" font-size="11" fill="#b91c1c" font-weight="bold">1300: {height(t13):.1f} m — ไม่พอ</text>\n'
    # side panel
    bx = 675
    s += f'<rect x="{bx}" y="70" width="290" height="370" rx="8" fill="#fff" stroke="#94a3b8"/>\n'
    lines = [('ข้อมูลสมมติ', True), ('charted depth จุดตื้น 8.6 m', False), ('draught 10.5 m · squat ≈ 0.5 m', False), ('UKC ขั้นต่ำตามบริษัท 1.0 m', False), ('', False),
             ('ความลึกที่ต้องการ', True), ('10.5 + 0.5 + 1.0 = 12.0 m', False), ('ระดับน้ำที่ต้องการ', True), ('12.0 − 8.6 = 3.4 m เหนือ CD', False), ('', False),
             ('factor ขาขึ้น (3.4−0.7)/3.3 = 0.82', False), ('factor ขาลง (3.4−0.8)/3.2 = 0.81', False), ('→ จาก curve ≈ HW−1h46m ถึง HW+1h50m', False),
             ('', False), ('เผื่อความกดอากาศสูง/ลมออกฝั่ง', False), ('และความคลาดของพยากรณ์ด้วย', False)]
    for i, (t, b) in enumerate(lines):
        fw = ' font-weight="bold"' if b else ''
        s += f'<text x="{bx+12}" y="{94 + i*21}" font-size="12.5"{fw}>{t}</text>\n'
    s += f'<text x="{gx0}" y="{gy1+62}" font-size="11" fill="#64748b">เส้นโค้งสมมติเป็นรูป cosine ระหว่าง LW–HW เพื่ออธิบายหลักการ บนเรือจริงใช้ tidal curve ของท่าใน ATT หรือ TotalTide</text>\n'
    save('tide-ukc-window.svg', s)

if __name__ == '__main__':
    springs_neaps(); curve_terms(); standard_curve(); twelfths(); ukc_window(); print('ok')
