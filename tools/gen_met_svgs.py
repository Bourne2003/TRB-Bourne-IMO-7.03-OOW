"""สคริปต์สร้างภาพประกอบบทอุตุนิยมวิทยา"""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
def head(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="a" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="context-stroke"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{title}</text>\n')
def save(n, s): open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')
def vec(x, y, brg, L, col, w=3, label=None, lx=0, ly=0):
    a = math.radians(brg); x2 = x + L * math.sin(a); y2 = y - L * math.cos(a)
    s = f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" marker-end="url(#a)"/>\n'
    if label: s += f'<text x="{(x+x2)/2+lx:.1f}" y="{(y+y2)/2+ly:.1f}" font-size="14" font-weight="bold" fill="{col}">{label}</text>\n'
    return s, x2, y2

def true_wind():
    w, h = 920, 480
    s = head(w, h, 'การหาลมจริง (True wind) จากลมสัมพัทธ์ (Apparent wind)')
    sc = 12
    O = (300, 400)
    a, ax, ay = vec(O[0], O[1], 20, 25 * sc, '#1d4ed8', 3.5, 'Apparent wind (ไปหา 020°) 25 kn', -280, 0)
    s += a
    b, bx, by = vec(ax, ay, 160, 14 * sc, '#15803d', 3.5, 'เรือ 160°×14 kn', 10, 10)
    s += b
    tx, ty = bx - O[0], -(by - O[1])
    brg = math.degrees(math.atan2(tx, ty)) % 360; spd = math.hypot(tx, ty) / sc
    s += f'<line x1="{O[0]}" y1="{O[1]}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#b91c1c" stroke-width="4" marker-end="url(#a)"/>\n'
    s += f'<text x="{(O[0]+bx)/2+14:.1f}" y="{(O[1]+by)/2+30:.1f}" font-size="14" font-weight="bold" fill="#b91c1c">True wind ไปหา {brg:03.0f}° ≈ {spd:.1f} kn → มาจาก {(brg+180)%360:03.0f}°</text>\n'
    s += '<rect x="560" y="70" width="345" height="190" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['ข้อมูล: เรือ 160°T 14 kn', 'ลมสัมพัทธ์จาก 040° กราบขวา 25 kn', '→ มาจาก 200°T (ไปหา 020°)', '', 'True = Apparent + Ship velocity', '(เวกเตอร์แบบ "ไปหา")', 'ผล: ลมจริงจาก ~232°T ~17 kn']):
        s += f'<text x="576" y="{98 + i*24}" font-size="14">{t}</text>\n'
    s += '<text x="560" y="300" font-size="13" fill="#475569">ลมจริงอยู่ "ท้ายเรือ" มากกว่าลมสัมพัทธ์เสมอ</text>\n'
    s += '<line x1="860" y1="420" x2="860" y2="350" stroke="#0f172a" stroke-width="2" marker-end="url(#a)"/><text x="853" y="340" font-size="14" font-weight="bold">N</text>\n'
    save('met-true-wind.svg', s)

def circulation():
    w, h = 980, 610
    s = head(w, h, 'การไหลเวียนของบรรยากาศทั่วโลกและแถบลมประจำ')
    cx, cy, r = 450, 320, 240
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#eff6ff" stroke="#1e3a8a" stroke-width="2"/>\n'
    bands = [(60, '#94a3b8', 'Polar front / Low ~60°'), (30, '#f59e0b', 'Subtropical High ~30°'), (0, '#ef4444', 'ITCZ / Doldrums'), (-30, '#f59e0b', ''), (-60, '#94a3b8', '')]
    for lat, col, lab in bands:
        y = cy - r * math.sin(math.radians(lat)); half = r * math.cos(math.radians(lat))
        s += f'<line x1="{cx-half:.1f}" y1="{y:.1f}" x2="{cx+half:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="3" stroke-dasharray="8 4"/>\n'
        if lab: s += f'<text x="{cx+half+10:.1f}" y="{y+5:.1f}" font-size="13" fill="{col}" font-weight="bold">{lab}</text>\n'
    def arrows(lat, brg, col):
        out = ''
        y = cy - r * math.sin(math.radians(lat)); half = r * math.cos(math.radians(lat))
        for k in (-0.55, 0, 0.55):
            x = cx + k * half
            a = math.radians(brg); L = 46
            out += f'<line x1="{x - L/2*math.sin(a):.1f}" y1="{y + L/2*math.cos(a):.1f}" x2="{x + L/2*math.sin(a):.1f}" y2="{y - L/2*math.cos(a):.1f}" stroke="{col}" stroke-width="3" marker-end="url(#a)"/>\n'
        return out
    s += arrows(75, 240, '#475569')   # polar easterlies NE->SW
    s += arrows(45, 60, '#15803d')    # westerlies SW->NE
    s += arrows(15, 240, '#1d4ed8')   # NE trades blow toward SW
    s += arrows(-15, 300, '#1d4ed8')  # SE trades toward NW
    s += arrows(-45, 120, '#15803d')  # westerlies NW->SE
    s += arrows(-75, 300, '#475569')
    labels = [(75, 'Polar easterlies'), (45, 'Westerlies'), (15, 'NE Trades'), (-15, 'SE Trades'), (-45, 'Westerlies (Roaring Forties)'), (-75, 'Polar easterlies')]
    for lat, t in labels:
        y = cy - r * math.sin(math.radians(lat))
        s += f'<text x="12" y="{y+5:.1f}" font-size="13" font-weight="bold">{t}</text>\n'
    s += '<rect x="700" y="400" width="270" height="190" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['Hadley cell: 0°–30°', 'Ferrel cell: 30°–60°', 'Polar cell: 60°–90°', '', 'แถบทั้งหมดเลื่อนตามฤดู', '(ตามดวงอาทิตย์) ราว 5°–10°', 'ITCZ ช่วง ก.ค.–ส.ค. อยู่ทางเหนือ']):
        s += f'<text x="714" y="{428 + i*24}" font-size="13">{t}</text>\n'
    save('met-global-circulation.svg', s)

def monsoon():
    w, h = 980, 520
    s = head(w, h, 'มรสุมในเอเชียตะวันออกเฉียงใต้ (แผนภาพอย่างง่าย ไม่ใช่แผนที่จริง)')
    def panel(x0, title, arrow_brg, col, notes):
        out = f'<rect x="{x0}" y="55" width="460" height="440" rx="10" fill="#f0f9ff" stroke="#94a3b8"/>\n<text x="{x0+230}" y="82" text-anchor="middle" font-size="16" font-weight="bold" fill="{col}">{title}</text>\n'
        # simplified landmasses
        out += f'<path d="M {x0+150} 100 L {x0+240} 100 L {x0+250} 180 L {x0+230} 260 L {x0+215} 330 L {x0+232} 420 L {x0+210} 430 L {x0+190} 340 L {x0+200} 250 L {x0+170} 170 Z" fill="#f5deb3" stroke="#8b6b3d"/>\n'
        out += f'<path d="M {x0+300} 100 L {x0+400} 100 L {x0+390} 200 L {x0+340} 260 L {x0+300} 230 L {x0+290} 160 Z" fill="#f5deb3" stroke="#8b6b3d"/>\n'
        out += f'<text x="{x0+175}" y="140" font-size="12">ไทย/เมียนมา</text><text x="{x0+310}" y="150" font-size="12">อินโดจีน</text><text x="{x0+225}" y="300" font-size="11">อ่าวไทย</text>\n'
        out += f'<text x="{x0+40}" y="300" font-size="12">ทะเลอันดามัน</text><text x="{x0+340}" y="350" font-size="12">ทะเลจีนใต้</text>\n'
        for (x, y) in [(x0+70, 200), (x0+90, 380), (x0+330, 300), (x0+400, 420), (x0+260, 200)]:
            a = math.radians(arrow_brg); L = 70
            out += f'<line x1="{x - L/2*math.sin(a):.1f}" y1="{y + L/2*math.cos(a):.1f}" x2="{x + L/2*math.sin(a):.1f}" y2="{y - L/2*math.cos(a):.1f}" stroke="{col}" stroke-width="5" marker-end="url(#a)"/>\n'
        for i, t in enumerate(notes):
            out += f'<text x="{x0+20}" y="{455 + i*18}" font-size="12">{t}</text>\n'
        return out
    s += panel(20, 'SW Monsoon (พ.ค. – ก.ย./ต.ค.)', 45, '#b91c1c', ['ลมจาก SW ชื้น ฝนหนักฝั่งอันดามัน', 'Sumatras ในช่องแคบมะละกา (กลางคืน)'])
    s += panel(500, 'NE Monsoon (พ.ย. – ก.พ./มี.ค.)', 225, '#1d4ed8', ['ลมจาก NE แรง (monsoon surge) ในทะเลจีนใต้', 'คลื่นลมแรงอ่าวไทยตอนล่าง ฝนภาคใต้ฝั่งอ่าวไทย'])
    save('met-monsoon-sea.svg', s)

def clouds():
    w, h = 980, 520
    s = head(w, h, 'ชนิดของเมฆ 10 ชนิด (WMO) ตามระดับความสูง')
    s += '<rect x="0" y="470" width="980" height="50" fill="#bfdbfe"/>\n'
    s += '<g font-size="12" fill="#475569"><text x="10" y="120">สูง &gt; 6 km</text><text x="10" y="270">กลาง 2–6 km</text><text x="10" y="420">ต่ำ &lt; 2 km</text></g>\n'
    s += '<line x1="0" y1="180" x2="980" y2="180" stroke="#e2e8f0" stroke-dasharray="4 4"/><line x1="0" y1="330" x2="980" y2="330" stroke="#e2e8f0" stroke-dasharray="4 4"/>\n'
    # cirrus strokes
    for i in range(5):
        s += f'<path d="M {120+i*25} {110+i*4} q 30 -20 60 -12" fill="none" stroke="#94a3b8" stroke-width="2"/>\n'
    s += '<text x="130" y="150" font-size="13" font-weight="bold">Cirrus (Ci)</text>\n'
    for i in range(12):
        s += f'<circle cx="{300+(i%6)*16}" cy="{100+(i//6)*14}" r="5" fill="#e2e8f0" stroke="#94a3b8"/>\n'
    s += '<text x="290" y="150" font-size="13" font-weight="bold">Cirrocumulus (Cc)</text>\n'
    s += '<rect x="460" y="95" width="200" height="16" rx="8" fill="#e5e7eb"/><circle cx="560" cy="80" r="16" fill="none" stroke="#facc15" stroke-width="2"/><circle cx="560" cy="80" r="34" fill="none" stroke="#fde68a" stroke-width="2"/>\n'
    s += '<text x="470" y="150" font-size="13" font-weight="bold">Cirrostratus (Cs) + halo</text>\n'
    for i in range(10):
        s += f'<ellipse cx="{130+(i%5)*26}" cy="{240+(i//5)*20}" rx="12" ry="8" fill="#e2e8f0" stroke="#94a3b8"/>\n'
    s += '<text x="120" y="300" font-size="13" font-weight="bold">Altocumulus (Ac)</text>\n'
    s += '<rect x="300" y="235" width="200" height="26" rx="10" fill="#cbd5e1"/><text x="310" y="300" font-size="13" font-weight="bold">Altostratus (As)</text>\n'
    s += '<rect x="540" y="220" width="190" height="200" rx="12" fill="#64748b"/>\n'
    for i in range(9): s += f'<line x1="{555+i*20}" y1="420" x2="{545+i*20}" y2="460" stroke="#1d4ed8" stroke-width="2"/>\n'
    s += '<text x="565" y="320" font-size="13" font-weight="bold" fill="#fff">Nimbostratus (Ns)</text>\n'
    for i in range(6):
        s += f'<ellipse cx="{130+i*30}" cy="380" rx="18" ry="11" fill="#cbd5e1" stroke="#94a3b8"/>\n'
    s += '<text x="120" y="410" font-size="13" font-weight="bold">Stratocumulus (Sc)</text>\n'
    s += '<rect x="330" y="420" width="190" height="16" fill="#d1d5db"/><text x="340" y="455" font-size="13" font-weight="bold">Stratus (St)</text>\n'
    s += '<path d="M 745 465 q -10 -40 20 -50 q 0 -30 30 -30 q 30 0 30 30 q 30 10 20 50 Z" fill="#f1f5f9" stroke="#94a3b8"/><text x="742" y="490" font-size="12" font-weight="bold">Cumulus (Cu)</text>\n'
    s += '<path d="M 850 470 L 850 300 Q 840 200 880 150 L 830 80 L 975 80 L 935 150 Q 970 220 965 300 L 965 470 Z" fill="#94a3b8" opacity="0.6" stroke="#475569"/>\n'
    s += '<text x="800" y="62" font-size="13" font-weight="bold">Cumulonimbus (Cb)</text><text x="855" y="200" font-size="11">ยอดทั่ง (anvil)</text><text x="855" y="216" font-size="11">ฟ้าคะนอง squall</text>\n'
    save('met-clouds.svg', s)

def frontal():
    w, h = 980, 600
    s = head(w, h, 'Frontal depression ในซีกโลกเหนือ (มุมมองบนแผนที่)')
    cx, cy = 400, 260
    for i, r in enumerate((50, 95, 145, 200)):
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.25}" ry="{r}" fill="none" stroke="#64748b" stroke-width="1.5"/>\n'
        s += f'<text x="{cx + r*1.25 - 30}" y="{cy - 4}" font-size="11" fill="#475569">{992 + i*4}</text>\n'
    s += f'<text x="{cx-10}" y="{cy+6}" font-size="22" font-weight="bold" fill="#b91c1c">L</text>\n'
    def along(pts, t):
        """จุดและทิศสัมผัสบน polyline ที่สัดส่วนความยาว t"""
        segs = [(pts[i], pts[i+1]) for i in range(len(pts)-1)]
        lens = [math.hypot(b[0]-a[0], b[1]-a[1]) for a, b in segs]
        target = t * sum(lens)
        for (a, b), L in zip(segs, lens):
            if target <= L:
                f = target / L
                return a[0] + f*(b[0]-a[0]), a[1] + f*(b[1]-a[1]), (b[0]-a[0])/L, (b[1]-a[1])/L
            target -= L
        a, b = segs[-1]; L = lens[-1]
        return b[0], b[1], (b[0]-a[0])/L, (b[1]-a[1])/L
    # warm front: from centre to east-southeast — สัญลักษณ์ครึ่งวงกลมอยู่ด้านที่แนวปะทะเคลื่อนไป (ด้านอากาศเย็นข้างหน้า = ทิศ NE)
    wpts = [(cx, cy), (cx+80, cy+60), (cx+170, cy+110), (cx+260, cy+140)]
    d = 'M ' + ' L '.join(f'{x} {y}' for x, y in wpts)
    s += f'<path d="{d}" fill="none" stroke="#dc2626" stroke-width="4"/>\n'
    for k in range(1, 6):
        x, y, tx, ty = along(wpts, k / 6)
        nx, ny = ty, -tx                      # ตั้งฉากชี้ไปด้านอากาศเย็นข้างหน้า (ทิศ NE)
        r = 10
        x1, y1, x2, y2 = x - r*tx, y - r*ty, x + r*tx, y + r*ty
        sweep = 0 if (tx*ny - ty*nx) > 0 else 1
        s += f'<path d="M {x1:.1f} {y1:.1f} A {r} {r} 0 0 {sweep} {x2:.1f} {y2:.1f} Z" fill="#dc2626"/>\n'
    s += f'<text x="{cx+200}" y="{cy+180}" font-size="14" font-weight="bold" fill="#dc2626">Warm front</text>\n'
    # cold front: from centre to south-southwest — สามเหลี่ยมชี้ไปทางที่แนวปะทะเคลื่อนไป (เข้าหา warm sector = ทิศ E/SE)
    cpts = [(cx, cy), (cx-30, cy+90), (cx-80, cy+180), (cx-140, cy+270)]
    d = 'M ' + ' L '.join(f'{x} {y}' for x, y in cpts)
    s += f'<path d="{d}" fill="none" stroke="#1d4ed8" stroke-width="4"/>\n'
    for k in range(1, 6):
        x, y, tx, ty = along(cpts, k / 6)
        nx, ny = ty, -tx                      # ตั้งฉากชี้ไปด้าน warm sector (ตะวันออก/ตะวันออกเฉียงใต้)
        h = 16; b = 10
        s += f'<path d="M {x - b*tx:.1f} {y - b*ty:.1f} L {x + b*tx:.1f} {y + b*ty:.1f} L {x + h*nx:.1f} {y + h*ny:.1f} Z" fill="#1d4ed8"/>\n'
    s += f'<text x="{cx-230}" y="{cy+260}" font-size="14" font-weight="bold" fill="#1d4ed8">Cold front</text>\n'
    s += f'<text x="{cx+20}" y="{cy+190}" font-size="14" font-weight="bold" fill="#b45309">Warm sector</text>\n'
    # wind arrows CCW
    for ang in range(0, 360, 45):
        if ang == 315: continue          # ตำแหน่งนี้ทับแนว warm front
        a = math.radians(ang); r = 170
        x = cx + r * 1.25 * math.cos(a); y = cy - r * math.sin(a)
        tang = math.degrees(math.atan2(-math.cos(a), -math.sin(a)))  # placeholder
        # CCW tangent direction in screen coords: derivative of (cos, -sin) wrt angle increase => (-sin, -cos)
        vx, vy = -math.sin(a), -math.cos(a)
        # add inflow 20 deg toward centre
        ix, iy = -math.cos(a), math.sin(a)
        fx, fy = vx * 0.94 + ix * 0.34, vy * 0.94 + iy * 0.34
        s += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+40*fx:.1f}" y2="{y+40*fy:.1f}" stroke="#15803d" stroke-width="3" marker-end="url(#a)"/>\n'
    s += f'<line x1="{cx+150}" y1="{cy-150}" x2="{cx+250}" y2="{cy-190}" stroke="#7c3aed" stroke-width="3" stroke-dasharray="6 4" marker-end="url(#a)"/><text x="{cx+260}" y="{cy-180}" font-size="13" fill="#7c3aed" font-weight="bold">ทิศการเคลื่อนที่ของ low</text>\n'
    s += '<rect x="700" y="330" width="265" height="210" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['ลมหมุนทวนเข็มนาฬิกา (ซีกเหนือ)', 'และเบนเข้าหาศูนย์กลาง', '', 'ก่อน warm front: ลม back,', 'ความกดลด, ฝนต่อเนื่อง', 'ผ่าน cold front: ลม veer ฉับพลัน,', 'ความกดขึ้น, ฝนหนัก/Cb', 'ตัวเลข = isobars (hPa)']):
        s += f'<text x="714" y="{356 + i*22}" font-size="13">{t}</text>\n'
    save('met-frontal-depression.svg', s)

def trs():
    w, h = 1000, 590
    s = head(w, h, 'Tropical Revolving Storm — Dangerous / Navigable semicircle')
    def panel(cx, title, hemi):
        cy = 310
        out = f'<text x="{cx}" y="62" text-anchor="middle" font-size="16" font-weight="bold">{title}</text>\n'
        right = 1 if hemi == 'N' else -1
        # semicircles: storm moving north (up) for clarity
        out += f'<path d="M {cx} {cy-180} A 180 180 0 0 {1 if right>0 else 0} {cx} {cy+180} Z" fill="#fecaca" opacity="0.7"/>\n'
        out += f'<path d="M {cx} {cy-180} A 180 180 0 0 {0 if right>0 else 1} {cx} {cy+180} Z" fill="#bbf7d0" opacity="0.7"/>\n'
        # advance quadrant darker
        out += f'<path d="M {cx} {cy} L {cx} {cy-180} A 180 180 0 0 {1 if right>0 else 0} {cx + right*180} {cy} Z" fill="#ef4444" opacity="0.45"/>\n'
        out += f'<circle cx="{cx}" cy="{cy}" r="14" fill="#fff" stroke="#0f172a" stroke-width="2"/><text x="{cx-12}" y="{cy+34}" font-size="12">eye</text>\n'
        out += f'<line x1="{cx}" y1="{cy+170}" x2="{cx}" y2="{cy-205}" stroke="#0f172a" stroke-width="2.5" stroke-dasharray="8 5" marker-end="url(#a)"/>\n'
        out += f'<text x="{cx+10}" y="{cy-196}" font-size="12" font-weight="bold">ทิศการเคลื่อนที่</text>\n'
        # circulation arrows
        for ang in range(0, 360, 60):
            a = math.radians(ang); r = 110
            x = cx + r * math.cos(a); y = cy - r * math.sin(a)
            if hemi == 'N': vx, vy = -math.sin(a), -math.cos(a)
            else: vx, vy = math.sin(a), math.cos(a)
            out += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+34*vx:.1f}" y2="{y+34*vy:.1f}" stroke="#1e3a8a" stroke-width="3" marker-end="url(#a)"/>\n'
        dx = cx + right * 95; nx = cx - right * 95
        out += f'<text x="{dx}" y="{cy-60}" text-anchor="middle" font-size="14" font-weight="bold" fill="#991b1b">DANGEROUS</text>\n'
        out += f'<text x="{dx}" y="{cy-42}" text-anchor="middle" font-size="12" fill="#991b1b">(advance quadrant อันตรายสุด)</text>\n'
        out += f'<text x="{nx}" y="{cy+70}" text-anchor="middle" font-size="14" font-weight="bold" fill="#166534">NAVIGABLE</text>\n'
        if hemi == 'N':
            notes = ['ลม veer → dangerous: ลมกราบขวาหัวเรือ 10°–45°', 'ลม back → navigable: ลมกราบขวาท้ายเรือ', 'บนเส้นทางข้างหน้า: ลมกราบขวาท้ายเรือ']
        else:
            notes = ['ลม back → dangerous: ลมกราบซ้ายหัวเรือ 10°–45°', 'ลม veer → navigable: ลมกราบซ้ายท้ายเรือ', 'บนเส้นทางข้างหน้า: ลมกราบซ้ายท้ายเรือ']
        for i, t in enumerate(notes):
            out += f'<text x="{cx-230}" y="{cy+210 + i*18}" font-size="12">{t}</text>\n'
        return out
    s += panel(260, 'ซีกโลกเหนือ (ลมหมุนทวนเข็มนาฬิกา)', 'N')
    s += panel(740, 'ซีกโลกใต้ (ลมหมุนตามเข็มนาฬิกา)', 'S')
    s += '<line x1="500" y1="60" x2="500" y2="550" stroke="#e2e8f0" stroke-width="2"/>\n'
    save('met-trs-semicircles.svg', s)

def synoptic():
    w, h = 980, 420
    s = head(w, h, 'สัญลักษณ์แผนที่อากาศ — แนวปะทะ และ Wind barbs')
    y = 90
    def front(y, col, kind, label):
        out = f'<line x1="40" y1="{y}" x2="360" y2="{y}" stroke="{col}" stroke-width="4"/>\n'
        for k in range(5):
            x = 70 + k * 60
            if kind == 'warm': out += f'<path d="M {x-12} {y} A 12 12 0 0 1 {x+12} {y} Z" fill="{col}"/>\n'
            elif kind == 'cold': out += f'<path d="M {x-12} {y} L {x+12} {y} L {x} {y-18} Z" fill="{col}"/>\n'
            elif kind == 'occl':
                if k % 2: out += f'<path d="M {x-12} {y} A 12 12 0 0 1 {x+12} {y} Z" fill="{col}"/>\n'
                else: out += f'<path d="M {x-12} {y} L {x+12} {y} L {x} {y-18} Z" fill="{col}"/>\n'
            elif kind == 'stat':
                if k % 2: out += f'<path d="M {x-12} {y} A 12 12 0 0 0 {x+12} {y} Z" fill="#dc2626"/>\n'
                else: out += f'<path d="M {x-12} {y} L {x+12} {y} L {x} {y-18} Z" fill="#1d4ed8"/>\n'
        out += f'<text x="380" y="{y+5}" font-size="14" font-weight="bold" fill="{col if kind != "stat" else "#0f172a"}">{label}</text>\n'
        return out
    s += front(90, '#dc2626', 'warm', 'Warm front')
    s += front(160, '#1d4ed8', 'cold', 'Cold front')
    s += front(230, '#7c3aed', 'occl', 'Occluded front')
    s += front(300, '#0f172a', 'stat', 'Stationary front')
    # wind barbs
    def barb(x, y, frm, kn, label):
        a = math.radians(frm); L = 70
        x2, y2 = x + L * math.sin(a), y - L * math.cos(a)
        out = f'<circle cx="{x}" cy="{y}" r="6" fill="none" stroke="#0f172a" stroke-width="2"/><line x1="{x}" y1="{y}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#0f172a" stroke-width="2.5"/>\n'
        # barbs on the clockwise side (NH convention)
        px, py = math.cos(a), math.sin(a)
        rem = kn; pos = 0
        while rem >= 50:
            bx, by = x2 - pos * math.sin(a), y2 + pos * math.cos(a)
            bx2, by2 = bx - 10 * math.sin(a), by + 10 * math.cos(a)
            out += f'<path d="M {bx:.1f} {by:.1f} L {bx + 22*px:.1f} {by + 22*py:.1f} L {bx2:.1f} {by2:.1f} Z" fill="#0f172a"/>\n'
            rem -= 50; pos += 14
        while rem >= 10:
            bx, by = x2 - pos * math.sin(a), y2 + pos * math.cos(a)
            out += f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx + 22*px:.1f}" y2="{by + 22*py:.1f}" stroke="#0f172a" stroke-width="2.5"/>\n'
            rem -= 10; pos += 9
        if rem >= 5:
            bx, by = x2 - pos * math.sin(a), y2 + pos * math.cos(a)
            out += f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx + 11*px:.1f}" y2="{by + 11*py:.1f}" stroke="#0f172a" stroke-width="2.5"/>\n'
        out += f'<text x="{x-40}" y="{y+40}" font-size="13">{label}</text>\n'
        return out
    s += barb(600, 140, 45, 15, 'NE 15 kn')
    s += barb(760, 140, 270, 25, 'W 25 kn')
    s += barb(900, 140, 0, 55, 'N 55 kn')
    s += '<text x="560" y="250" font-size="14">ก้านชี้ไปทิศที่ลม "มาจาก"</text><text x="560" y="274" font-size="14">ขีดสั้น 5 kn · ขีดยาว 10 kn · ธง 50 kn</text>\n'
    s += '<text x="560" y="310" font-size="14">Isobars ทุก 4 hPa · ชิดกัน = ลมแรง</text><text x="560" y="334" font-size="14">H = ความกดสูง · L = ความกดต่ำ</text>\n'
    save('met-synoptic-symbols.svg', s)

if __name__ == '__main__':
    true_wind(); circulation(); monsoon(); clouds(); frontal(); trs(); synoptic(); print('ok')
