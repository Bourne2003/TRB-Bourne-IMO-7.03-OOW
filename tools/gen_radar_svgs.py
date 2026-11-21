"""ภาพประกอบบทเรดาร์และ ARPA"""
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
            '<marker id="arY" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#facc15"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{t}</text>\n')
def save(n, s): open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')
def box(x, y, w, h, t, sub='', c='#e0f2fe', sc='#0369a1'):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{c}" stroke="{sc}" stroke-width="2"/>\n<text x="{x+w/2}" y="{y+h/2-(6 if sub else -5)}" text-anchor="middle" font-size="14" font-weight="bold">{t}</text>\n'
    if sub: s += f'<text x="{x+w/2}" y="{y+h/2+14}" text-anchor="middle" font-size="11" fill="#334155">{sub}</text>\n'
    return s
def arrow(x1, y1, x2, y2, m='ar', c='#0f172a', w=2.5, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} marker-end="url(#{m})"/>\n'

def block():
    w, h = 1000, 470
    s = head(w, h, 'แผนผังการทำงานของเรดาร์แบบพัลส์ (Pulse radar block diagram)')
    s += box(40, 80, 170, 70, 'Timebase / Trigger', 'กำหนดจังหวะ PRF')
    s += box(260, 80, 170, 70, 'Modulator', 'สร้างพัลส์แรงสูง')
    s += box(480, 80, 170, 70, 'Transmitter', 'Magnetron / Solid-state')
    s += box(700, 80, 170, 70, 'Duplexer (T/R)', 'สลับส่ง-รับ', '#fef3c7', '#b45309')
    s += box(700, 250, 170, 70, 'Receiver', 'ขยาย + กรอง (gain, STC, FTC)')
    s += box(480, 250, 170, 70, 'Processor', 'digital, tracking, AIS')
    s += box(260, 250, 170, 70, 'Display (PPI)', 'ระยะ-ทิศ, EBL/VRM')
    s += box(40, 250, 170, 70, 'Heading / Speed', 'Gyro (THD), Log, GNSS', '#dcfce7', '#15803d')
    s += arrow(210, 115, 258, 115) + arrow(430, 115, 478, 115) + arrow(650, 115, 698, 115)
    s += arrow(785, 150, 785, 248) + arrow(700, 285, 652, 285) + arrow(480, 285, 432, 285) + arrow(210, 285, 258, 285)
    # sync: timebase triggers the display sweep at the instant of transmission (not the sensors)
    s += '<polyline points="180,150 180,200 345,200 345,246" fill="none" stroke="#0f172a" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ar)"/>\n'
    s += '<text x="190" y="194" font-size="11">sync (เริ่มเส้นกวาดพร้อมการส่งพัลส์)</text>\n'
    # antenna
    s += '<rect x="885" y="60" width="100" height="14" fill="#334155"/><line x1="935" y1="74" x2="935" y2="110" stroke="#334155" stroke-width="6"/>\n'
    s += '<text x="935" y="52" text-anchor="middle" font-size="13" font-weight="bold">Antenna (scanner)</text>\n'
    s += '<line x1="870" y1="115" x2="930" y2="115" stroke="#0f172a" stroke-width="2.5"/>\n'
    s += '<path d="M 940 130 q 15 30 0 60 M 955 125 q 20 40 0 80" fill="none" stroke="#b91c1c" stroke-width="2"/>\n'
    s += '<text x="880" y="230" font-size="12" fill="#b91c1c">พัลส์ / echo</text>\n'
    s += '<rect x="40" y="350" width="920" height="100" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['ระยะ = (c × t) / 2  — คลื่นวิทยุเดินทาง ≈ 300 m/µs (ทางเดียว) → เป้าที่ 1 nm ใช้เวลาไป-กลับประมาณ 12.36 µs',
                           'X-band 9.2–9.5 GHz (λ ≈ 3 cm): ภาพคม แยกเป้าดี ตรวจ SART/racon X · S-band 2.9–3.1 GHz (λ ≈ 10 cm): ทะลุฝน/คลื่นดีกว่า',
                           'Pulse length สั้น → แยกเป้าในระยะดี (ใช้ระยะใกล้) · ยาว → พลังงานมาก ตรวจไกล (ระยะไกล) · PRF สัมพันธ์กับ pulse length']):
        s += f'<text x="56" y="{378+i*26}" font-size="13">{t}</text>\n'
    save('radar-block-diagram.svg', s)

def discrimination():
    w, h = 1000, 440
    s = head(w, h, 'การแยกเป้า (Discrimination) — Bearing ขึ้นกับ beam width, Range ขึ้นกับ pulse length')
    # left: beam width
    cx, cy = 230, 380
    a1, a2 = R(-6), R(6)
    L = 300
    s += f'<path d="M {cx} {cy} L {cx+L*math.sin(a1):.1f} {cy-L*math.cos(a1):.1f} A {L} {L} 0 0 1 {cx+L*math.sin(a2):.1f} {cy-L*math.cos(a2):.1f} Z" fill="#fde68a" opacity="0.6" stroke="#b45309"/>\n'
    s += f'<circle cx="{cx-12}" cy="{cy-250}" r="7" fill="#0f172a"/><circle cx="{cx+12}" cy="{cy-250}" r="7" fill="#0f172a"/>\n'
    s += f'<text x="{cx+40}" y="{cy-246}" font-size="12">เป้า 2 ลำระยะเท่ากัน</text>\n'
    s += f'<path d="M {cx-45} {cy-280} Q {cx} {cy-292} {cx+45} {cy-280}" stroke="#16a34a" stroke-width="10" fill="none" opacity="0.8"/>\n'
    s += f'<text x="{cx}" y="{cy-305}" text-anchor="middle" font-size="12" fill="#15803d">บนจอเห็นเป็น echo เดียวยาว</text>\n'
    s += f'<text x="{cx}" y="{cy+30}" text-anchor="middle" font-size="14" font-weight="bold">Horizontal beam width (X ≈ 1°–2°)</text>\n'
    # right: pulse length
    x0 = 560
    s += f'<line x1="{x0}" y1="200" x2="{x0+400}" y2="200" stroke="#94a3b8"/>\n'
    s += f'<rect x="{x0+40}" y="180" width="160" height="40" fill="#fecaca" stroke="#b91c1c"/><text x="{x0+120}" y="172" text-anchor="middle" font-size="12" fill="#b91c1c">ความยาวพัลส์ในอวกาศ (c × τ)</text>\n'
    s += f'<circle cx="{x0+250}" cy="200" r="7" fill="#0f172a"/><circle cx="{x0+300}" cy="200" r="7" fill="#0f172a"/>\n'
    s += f'<text x="{x0+275}" y="240" text-anchor="middle" font-size="12">เป้าห่างกันน้อยกว่า ½ ความยาวพัลส์</text>\n'
    s += f'<text x="{x0+275}" y="258" text-anchor="middle" font-size="12">→ echo ซ้อนเป็นอันเดียว</text>\n'
    s += f'<text x="{x0+200}" y="320" text-anchor="middle" font-size="14" font-weight="bold">Range discrimination ≈ ½ × c × τ</text>\n'
    s += f'<text x="{x0+200}" y="345" text-anchor="middle" font-size="12">τ = 0.05 µs → ≈ 7.5 m · τ = 1.0 µs → ≈ 150 m</text>\n'
    s += f'<text x="{x0+200}" y="370" text-anchor="middle" font-size="12">MSC.192(79): แยก 40 m ในระยะ, 2.5° ในแบริ่ง (range scale ≤ 1.5 nm)</text>\n'
    save('radar-discrimination.svg', s)

def false_echoes():
    w, h = 1000, 800
    s = head(w, h, 'ภาพลวงบนจอเรดาร์ (False echoes) — 4 แบบที่ต้องแยกให้ออก')
    def ppi(cx, cy, r=130):
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#052e16" stroke="#334155" stroke-width="3"/><line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-r}" stroke="#bbf7d0"/><circle cx="{cx}" cy="{cy}" r="3" fill="#fff"/>\n'
    G = '#4ade80'
    # 1 indirect — false echo at the SAME range as the true target, on the bearing of the obstruction
    cx, cy = 250, 190; s += ppi(cx, cy)
    rr = 80
    tb, fb = R(50), R(200)
    s += f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#fde68a" stroke-width="1" stroke-dasharray="3 4" opacity="0.7"/>\n'
    # shadow sector of the funnel/mast (bearing ~190-210)
    a1, a2 = R(190), R(210)
    s += f'<path d="M {cx} {cy} L {cx+130*math.sin(a1):.1f} {cy-130*math.cos(a1):.1f} A 130 130 0 0 1 {cx+130*math.sin(a2):.1f} {cy-130*math.cos(a2):.1f} Z" fill="#334155" opacity="0.55"/>\n'
    s += f'<rect x="{cx+14*math.sin(fb)-5:.1f}" y="{cy-14*math.cos(fb)-4:.1f}" width="10" height="8" fill="#94a3b8"/>\n'
    s += f'<rect x="{cx+rr*math.sin(tb)-8:.1f}" y="{cy-rr*math.cos(tb)-5:.1f}" width="16" height="10" fill="{G}"/><text x="{cx+rr*math.sin(tb)+12:.1f}" y="{cy-rr*math.cos(tb)-8:.1f}" font-size="11" fill="#bbf7d0">เป้าจริง</text>\n'
    s += f'<rect x="{cx+rr*math.sin(fb)-7:.1f}" y="{cy-rr*math.cos(fb)-5:.1f}" width="14" height="10" fill="{G}" opacity="0.6"/>\n'
    s += f'<text x="{cx+rr*math.sin(fb)+14:.1f}" y="{cy-rr*math.cos(fb)+20:.1f}" font-size="11" fill="#fde68a">ภาพลวง</text><text x="{cx+rr*math.sin(fb)+14:.1f}" y="{cy-rr*math.cos(fb)+34:.1f}" font-size="11" fill="#fde68a">(ระยะเท่ากัน)</text>\n'
    s += f'<text x="{cx-118}" y="{cy+8}" font-size="11" fill="#e2e8f0">shadow sector</text><text x="{cx-118}" y="{cy+22}" font-size="11" fill="#e2e8f0">ทิศเสา/ปล่องควัน</text>\n'
    s += f'<text x="{cx}" y="{cy+160}" text-anchor="middle" font-size="14" font-weight="bold">1) Indirect (reflected) echo</text><text x="{cx}" y="{cy+178}" text-anchor="middle" font-size="11">ระยะเท่าเป้าจริง แต่ปรากฏในแบริ่งของสิ่งกีดขวางบนเรือ (มักใน shadow sector)</text>\n'
    # 2 multiple
    cx = 750; s += ppi(cx, cy)
    for k in (1, 2, 3):
        s += f'<rect x="{cx+30*k-6}" y="{cy-6}" width="12" height="12" fill="{G}" opacity="{1.1-0.3*k}"/>\n'
    s += f'<text x="{cx+20}" y="{cy-16}" font-size="11" fill="#bbf7d0">ใหญ่ ใกล้ ตรงกราบ</text>\n'
    s += f'<text x="{cx}" y="{cy+160}" text-anchor="middle" font-size="14" font-weight="bold">2) Multiple echoes</text><text x="{cx}" y="{cy+178}" text-anchor="middle" font-size="11">แบริ่งเดียวกัน ระยะเป็นทวีคูณของระยะจริง (2×, 3×) — สะท้อนไป-มาระหว่างเรือกับเป้า</text>\n'
    # 3 side lobe
    cx, cy = 250, 575; s += ppi(cx, cy)
    s += f'<rect x="{cx-6}" y="{cy-56}" width="12" height="10" fill="{G}"/>\n'
    s += f'<path d="M {cx-38} {cy-40} A 52 52 0 0 1 {cx+38} {cy-40}" stroke="{G}" stroke-width="3" fill="none" opacity="0.6"/>\n'
    s += f'<text x="{cx}" y="{cy+160}" text-anchor="middle" font-size="14" font-weight="bold">3) Side-lobe echoes</text><text x="{cx}" y="{cy+178}" text-anchor="middle" font-size="11">เป็นส่วนโค้งระยะเดียวกับเป้าจริงที่อยู่ใกล้ — ลด gain/ใช้ STC</text>\n'
    # 4 second trace — echo shown too close, on the true bearing of the distant target
    cx = 750; s += ppi(cx, cy)
    b4 = R(35)
    ex, ey = cx + 75 * math.sin(b4), cy - 75 * math.cos(b4)
    s += f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{cx+128*math.sin(b4):.1f}" y2="{cy-128*math.cos(b4):.1f}" stroke="#fde68a" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#arY)"/>\n'
    s += f'<rect x="{ex-7:.1f}" y="{ey-5:.1f}" width="14" height="10" fill="{G}"/><text x="{ex-14:.1f}" y="{ey+4:.1f}" text-anchor="end" font-size="11" fill="#bbf7d0">ปรากฏใกล้ (ระยะผิด)</text>\n'
    s += f'<text x="{cx}" y="{cy+50}" text-anchor="middle" font-size="11" fill="#fde68a">เป้าจริงอยู่ไกลเกิน max range</text><text x="{cx}" y="{cy+65}" text-anchor="middle" font-size="11" fill="#fde68a">ในแบริ่งเดียวกัน (super-refraction / ducting)</text>\n'
    s += f'<text x="{cx}" y="{cy+160}" text-anchor="middle" font-size="14" font-weight="bold">4) Second-trace echoes</text><text x="{cx}" y="{cy+178}" text-anchor="middle" font-size="11">echo จากพัลส์ก่อนหน้ากลับมาหลังพัลส์ใหม่ → ระยะผิด — เปลี่ยน PRF/range scale แล้ว echo จะกระโดด</text>\n'
    save('radar-false-echoes.svg', s)

def sart_racon():
    w, h = 1000, 780
    s = head(w, h, 'SART (9 GHz) และ Racon บนจอเรดาร์ X-band')
    def ppi(cx, cy, r=170):
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#052e16" stroke="#334155" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="3" fill="#fff"/>\n'
    G = '#4ade80'
    cx, cy = 260, 250; s += ppi(cx, cy)
    # SART 12 dots outward along bearing 060
    b = R(60)
    sx, sy = cx + 40 * math.sin(b), cy - 40 * math.cos(b)
    for k in range(12):
        d = 40 + k * 10
        s += f'<circle cx="{cx+d*math.sin(b):.1f}" cy="{cy-d*math.cos(b):.1f}" r="3.2" fill="{G}"/>\n'
    s += f'<text x="{cx-160}" y="{cy+200}" font-size="13" font-weight="bold">SART ระยะไกล: จุด 12 จุดเรียงออกไปด้านไกล</text>\n'
    s += f'<text x="{cx-160}" y="{cy+218}" font-size="12">ตำแหน่ง SART = จุดแรกที่ใกล้เรือที่สุด · ยาวประมาณ 8 nm</text>\n'
    s += f'<text x="{cx-160}" y="{cy+236}" font-size="12">ใกล้ &lt; ~1 nm: จุดกลายเป็นส่วนโค้ง → วงกลมรอบศูนย์กลาง</text>\n'
    s += f'<text x="{cx+20}" y="{cy-60}" font-size="11" fill="#bbf7d0">SART</text>\n'
    s += f'<text x="{cx}" y="{cy+150}" text-anchor="middle" font-size="11" fill="#bbf7d0">range scale 12 nm</text>\n'
    cx = 740; s += ppi(cx, cy)
    b = R(300)
    d0 = 60
    s += f'<rect x="{cx+d0*math.sin(b)-5:.1f}" y="{cy-d0*math.cos(b)-5:.1f}" width="10" height="10" fill="{G}"/>\n'
    # morse K -.- along bearing outward
    segs = [(0, 22), (30, 36), (44, 66)]
    for a, c in segs:
        x1, y1 = cx + (d0 + 10 + a) * math.sin(b), cy - (d0 + 10 + a) * math.cos(b)
        x2, y2 = cx + (d0 + 10 + c) * math.sin(b), cy - (d0 + 10 + c) * math.cos(b)
        s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{G}" stroke-width="6"/>\n'
    s += f'<text x="{cx-60}" y="{cy-130}" font-size="11" fill="#bbf7d0">Racon "K" (−·−)</text>\n'
    s += f'<text x="{cx-160}" y="{cy+200}" font-size="13" font-weight="bold">Racon: รหัสมอร์สเริ่มด้านหลังเป้า ยื่นออกไปตามรัศมี</text>\n'
    s += f'<text x="{cx-160}" y="{cy+218}" font-size="12">ใช้ระบุทุ่น/ประภาคาร/แท่น · ระยะวัดที่จุดเริ่มต้นของรหัส</text>\n'
    s += f'<text x="{cx-160}" y="{cy+236}" font-size="12">interference rejection อาจลบ racon/SART ออก</text>\n'
    # SART appearance as the rescuing ship closes (three stages)
    s += '<line x1="40" y1="510" x2="960" y2="510" stroke="#cbd5e1"/>\n'
    s += '<text x="500" y="536" text-anchor="middle" font-size="15" font-weight="bold">ภาพ SART เปลี่ยนไปเมื่อเรือเราเข้าใกล้ (ใช้ระบุระยะคร่าว ๆ)</text>\n'
    def mini(cx, cy, r=80):
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#052e16" stroke="#334155" stroke-width="3"/><circle cx="{cx}" cy="{cy}" r="2.5" fill="#fff"/>\n'
    cy2 = 640
    # stage 1: dots
    cx2 = 180; s += mini(cx2, cy2); b1 = R(30)
    for k in range(12):
        d = 18 + k * 5
        s += f'<circle cx="{cx2+d*math.sin(b1):.1f}" cy="{cy2-d*math.cos(b1):.1f}" r="2" fill="{G}"/>\n'
    s += f'<text x="{cx2}" y="{cy2+102}" text-anchor="middle" font-size="12" font-weight="bold">ไกลกว่า ~1 nm: 12 จุดเรียงตามรัศมี</text>\n'
    # stage 2: arcs
    cx2 = 500; s += mini(cx2, cy2)
    for k in range(8):
        d = 14 + k * 8
        a1, a2 = R(30 - 12 - k * 2), R(30 + 12 + k * 2)
        s += f'<path d="M {cx2+d*math.sin(a1):.1f} {cy2-d*math.cos(a1):.1f} A {d} {d} 0 0 1 {cx2+d*math.sin(a2):.1f} {cy2-d*math.cos(a2):.1f}" fill="none" stroke="{G}" stroke-width="2"/>\n'
    s += f'<text x="{cx2}" y="{cy2+102}" text-anchor="middle" font-size="12" font-weight="bold">~1 nm: จุดกลายเป็นส่วนโค้ง (side lobes)</text>\n'
    # stage 3: circles
    cx2 = 820; s += mini(cx2, cy2)
    for k in range(8):
        d = 10 + k * 8
        s += f'<circle cx="{cx2}" cy="{cy2}" r="{d}" fill="none" stroke="{G}" stroke-width="1.8" opacity="0.9"/>\n'
    s += f'<text x="{cx2}" y="{cy2+102}" text-anchor="middle" font-size="12" font-weight="bold">ใกล้มาก: วงกลมซ้อนรอบเรือเรา</text>\n'
    s += '<text x="500" y="770" text-anchor="middle" font-size="12" fill="#334155">ใกล้ SART แล้วลด gain/ปรับ clutter เพื่อหาทิศ — ค้นหาด้วยสายตา/ไฟส่องควบคู่ (MSC.510(105): ตรวจพบได้ ≥ 5 nm จากเสาอากาศ 15 m)</text>\n'
    save('radar-sart-racon.svg', s)

def plot_triangle():
    w, h = 1000, 640
    s = head(w, h, 'Radar plot (ตัวอย่างจำลอง): สามเหลี่ยม O–A–W, CPA/TCPA และการเปลี่ยนเข็ม')
    cx, cy, sc = 380, 470, 38  # px per nm
    def P(b, r): return cx + r * sc * math.sin(R(b)), cy - r * sc * math.cos(R(b))
    for rr in (2, 4, 6, 8, 10):
        s += f'<circle cx="{cx}" cy="{cy}" r="{rr*sc}" fill="none" stroke="#e2e8f0"/>\n'
    s += f'<text x="{cx+4}" y="{cy-10*sc-4}" font-size="11" fill="#94a3b8">10 nm</text>\n'
    obs = [(40.0, 10.0, '1000'), (39.8, 7.93, '1006'), (39.4, 5.87, '1012')]
    pts = [P(b, r) for b, r, _ in obs]
    (Ox, Oy), (Ax, Ay) = pts[0], pts[2]
    # W: O minus own ship 12 min run (own 000, 12 kn -> 2.4 nm north): W = O - own vector => O shifted south 2.4
    Wx, Wy = Ox, Oy + 2.4 * sc
    # O': new own-ship vector (060 deg, 12 kn, same 12 min = 2.4 nm) laid off from W
    Opx, Opy = Wx + 2.4 * sc * math.sin(R(60)), Wy - 2.4 * sc * math.cos(R(60))
    s += f'<line x1="{Wx:.1f}" y1="{Wy:.1f}" x2="{Ox:.1f}" y2="{Oy:.1f}" stroke="#1d4ed8" stroke-width="3" marker-end="url(#arB)"/>\n'
    s += f'<line x1="{Wx:.1f}" y1="{Wy:.1f}" x2="{Opx:.1f}" y2="{Opy:.1f}" stroke="#1d4ed8" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#arB)"/>\n'
    s += f'<line x1="{Opx:.1f}" y1="{Opy:.1f}" x2="{Ax:.1f}" y2="{Ay:.1f}" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="4 4"/>\n'
    s += f'<line x1="{Wx:.1f}" y1="{Wy:.1f}" x2="{Ax:.1f}" y2="{Ay:.1f}" stroke="#15803d" stroke-width="3" marker-end="url(#arG)"/>\n'
    s += f'<line x1="{Ox:.1f}" y1="{Oy:.1f}" x2="{Ax:.1f}" y2="{Ay:.1f}" stroke="#b91c1c" stroke-width="3" marker-end="url(#arR)"/>\n'
    for (x, y), (_, _, t) in zip(pts, obs):
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#0f172a"/>\n'
    s += f'<text x="{pts[0][0]+10:.1f}" y="{pts[0][1]+4:.1f}" font-size="12">1000</text><text x="{pts[1][0]-40:.1f}" y="{pts[1][1]-4:.1f}" font-size="12">1006</text><text x="{Ax-44:.1f}" y="{Ay-8:.1f}" font-size="12">1012</text>\n'
    s += f'<text x="{Wx+8:.1f}" y="{Wy+16:.1f}" font-size="14" font-weight="bold">W</text><text x="{Ox-20:.1f}" y="{Oy-6:.1f}" font-size="14" font-weight="bold">O</text><text x="{Ax-14:.1f}" y="{Ay+22:.1f}" font-size="14" font-weight="bold">A</text>\n'
    s += f'<text x="{Opx+8:.1f}" y="{Opy-4:.1f}" font-size="14" font-weight="bold" fill="#c2410c">O\'</text>\n'
    # extend relative motion line
    dx, dy = Ax - Ox, Ay - Oy; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    ex, ey = Ax + ux * 7 * sc, Ay + uy * 7 * sc
    s += f'<line x1="{Ax:.1f}" y1="{Ay:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#b91c1c" stroke-width="1.5" stroke-dasharray="6 4"/>\n'
    # CPA point
    t = -((Ax - cx) * ux + (Ay - cy) * uy)
    Cx, Cy = Ax + ux * t, Ay + uy * t
    s += f'<line x1="{cx}" y1="{cy}" x2="{Cx:.1f}" y2="{Cy:.1f}" stroke="#7c3aed" stroke-width="2"/><circle cx="{Cx:.1f}" cy="{Cy:.1f}" r="4" fill="#7c3aed"/>\n'
    s += f'<text x="{cx+14}" y="{cy+30}" font-size="13" fill="#7c3aed" font-weight="bold">CPA 0.15\' TCPA ≈ 1029 (ถ้าไม่ทำอะไร)</text>\n'
    # own ship
    s += f'<path d="M {cx} {cy-14} L {cx+7} {cy+10} L {cx-7} {cy+10} Z" fill="#334155"/>\n'
    s += f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-2.4*sc}" stroke="#1d4ed8" stroke-width="2" stroke-dasharray="3 3"/>\n'
    # new relative track after altering to 060 at 1012: parallel to O'A through A (point of execution)
    rdx, rdy = Ax - Opx, Ay - Opy; rL = math.hypot(rdx, rdy); rux, ruy = rdx / rL, rdy / rL
    nx, ny = Ax + rux * 8 * sc, Ay + ruy * 8 * sc
    s += f'<line x1="{Ax:.1f}" y1="{Ay:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#ea580c" stroke-width="2.5" stroke-dasharray="10 5" marker-end="url(#ar)"/>\n'
    s += f'<text x="{nx+60:.1f}" y="{ny+24:.1f}" text-anchor="end" font-size="12" fill="#c2410c" font-weight="bold">RML ใหม่ (ขนานกับ O\'A)</text>\n'
    t2 = -((Ax - cx) * rux + (Ay - cy) * ruy)
    C2x, C2y = Ax + rux * t2, Ay + ruy * t2
    s += f'<line x1="{cx}" y1="{cy}" x2="{C2x:.1f}" y2="{C2y:.1f}" stroke="#c2410c" stroke-width="1.5" stroke-dasharray="3 3"/><circle cx="{C2x:.1f}" cy="{C2y:.1f}" r="4" fill="#c2410c"/>\n'
    s += f'<text x="{C2x-8:.1f}" y="{C2y-12:.1f}" text-anchor="end" font-size="12" fill="#c2410c" font-weight="bold">CPA ใหม่ ≈ 2.8\'</text>\n'
    s += '<rect x="640" y="370" width="350" height="262" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    rows = ['เรือเรา 000° 12 kn (WO = 12 นาที = 2.4\')', '1000 040.0° 10.00\'  (O)', '1006 039.8°  7.93\'', '1012 039.4°  5.87\'  (A)', 'OA = relative motion 221° 20.7 kn', 'WA = target true 255° 14.0 kn', 'CPA 0.15\' (ผ่านหน้าเรา) TCPA 17 นาที', 'Aspect ≈ Red 36°', 'แบริ่งเกือบคงที่ ระยะลดเร็ว = เสี่ยงมาก', 'หันเป็น 060° ที่ 1012: WO\' = 060° 2.4\'', 'O\'A → RML ใหม่ 248° · CPA 2.82\' · TCPA 12 นาที']
    for i, t in enumerate(rows):
        col = ' fill="#c2410c"' if i >= 9 else ''
        s += f'<text x="652" y="{392+i*22.5}" font-size="12.5"{col}>{t}</text>\n'
    save('plot-triangle.svg', s)

def arpa_vectors():
    w, h = 1000, 480
    s = head(w, h, 'ARPA: True vectors กับ Relative vectors (vector time 12 นาที)')
    for k, (title, mode) in enumerate([('True vectors (sea-stabilised)', 'T'), ('Relative vectors', 'R')]):
        cx, cy, r = 250 + k * 500, 250, 170
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#052e16" stroke="#334155" stroke-width="3"/>\n'
        s += f'<text x="{cx}" y="62" text-anchor="middle" font-size="16" font-weight="bold">{title}</text>\n'
        sc = 13
        own = (0, 12)
        tgts = [((40, 5.9), (255, 14)), ((300, 6), (90, 10)), ((150, 4), (330, 15))]
        ox, oy = own[1] * 0.2 * math.sin(R(own[0])), own[1] * 0.2 * math.cos(R(own[0]))
        if mode == 'T':
            # own-ship vector drawn at the SAME scale as target vectors (2*sc px per nm, 12 min)
            s += f'<line x1="{cx}" y1="{cy}" x2="{cx+ox*sc*2:.1f}" y2="{cy-oy*sc*2:.1f}" stroke="#facc15" stroke-width="2.5" marker-end="url(#arY)"/>\n'
            s += f'<text x="{cx+8}" y="{cy-30}" font-size="11" fill="#fde68a">own ship 000° 12 kn</text>\n'
        else:
            s += f'<text x="{cx+8}" y="{cy+16}" font-size="11" fill="#fde68a">own ship (นิ่งบนจอ RM)</text>\n'
        for (b, rr), (c, v) in tgts:
            tx, ty = cx + rr * sc * math.sin(R(b)) * 2.0, cy - rr * sc * math.cos(R(b)) * 2.0
            vx, vy = v * 0.2 * math.sin(R(c)), v * 0.2 * math.cos(R(c))
            if mode == 'R': vx, vy = vx - ox, vy - oy
            s += f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="7" fill="none" stroke="#4ade80" stroke-width="2"/>\n'
            s += f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{tx+vx*sc*2:.1f}" y2="{ty-vy*sc*2:.1f}" stroke="#4ade80" stroke-width="2.5" marker-end="url(#arG)"/>\n'
            lab = {40: 'A', 300: 'B', 150: 'C'}[b]
            lx = tx - 26 if b == 40 else tx + 10
            s += f'<text x="{lx:.1f}" y="{ty-10:.1f}" font-size="13" font-weight="bold" fill="#bbf7d0">{lab}</text>\n'
        s += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#fff"/>\n'
    s += '<text x="500" y="466" text-anchor="middle" font-size="12" fill="#334155">A = เป้าในตัวอย่าง 2.3 (255° 14 kn) · B = 090° 10 kn · C = 330° 15 kn · เรือเรา 000° 12 kn · vector 12 นาที (สเกลเดียวกันทุกเส้น)</text>\n'
    s += '<text x="40" y="440" font-size="13">True vectors บอก "เรือลำนั้นกำลังไปทางไหน" (aspect, ประเภทสถานการณ์ COLREG) · Relative vectors บอก "จะเข้าใกล้เราแค่ไหน" (ชี้ผ่านเรา = เสี่ยงชน)</text>\n'
    save('arpa-vectors.svg', s)

if __name__ == '__main__':
    block(); discrimination(); false_echoes(); sart_racon(); plot_triangle(); arpa_vectors(); print('ok')
