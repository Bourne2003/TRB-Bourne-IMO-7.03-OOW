"""ภาพประกอบบทเหตุฉุกเฉินและ SAR"""
import math, os
R = math.radians
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker>'
            '<marker id="arB" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#1d4ed8"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{t}</text>\n')
def save(n, s): open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')

def flow():
    w, h = 1000, 710
    s = head(w, h, 'การกระทำเบื้องต้นของ OOW หลังโดนกันหรือเกยตื้น (ลำดับทั่วไป)')
    steps = [('1. ส่งสัญญาณเตือนภัยทั่วไป (General alarm)', 'เรียกนายเรือ · แจ้งห้องเครื่อง · ประกาศ PA'),
             ('2. ควบคุมเรือ', 'หยุด/ลดเครื่องตามสถานการณ์ · หางเสือ · อย่าถอยออกทันทีถ้าหัวเรือเสียบอีกลำ'),
             ('3. ปิดประตูผนึกน้ำ (WT doors) และช่องเปิด', 'รักษา watertight integrity'),
             ('4. ไฟ/ทุ่นวัน/สัญญาณ', 'NUC หรือ aground · สัญญาณเสียง · VDR save'),
             ('5. ตำแหน่งและการสื่อสาร', 'fix ตำแหน่ง · VHF/DSC (ตามคำสั่งนายเรือ) · แลกข้อมูลกับอีกลำ'),
             ('6. ประเมินความเสียหาย', 'วัดถัง/ท้องเรือ (soundings) · ตรวจรอบลำ · น้ำเข้า? ไฟไหม้? รั่วไหล? คนบาดเจ็บ?'),
             ('7. ควบคุมความเสียหาย', 'สูบน้ำ · อุด/ค้ำยัน · stability &amp; stress · ป้องกันมลพิษ (SOPEP)'),
             ('8. เตรียมพร้อม', 'LSA · นับคน · แจ้งบริษัท (DPA) · รัฐชายฝั่ง · บันทึกเหตุการณ์')]
    for i, (t, d) in enumerate(steps):
        c, r = i % 2, i // 2
        x, y = 40 + c * 480, 55 + r * 157
        s += f'<rect x="{x}" y="{y}" width="440" height="145" rx="12" fill="{"#fee2e2" if i < 4 else "#e0f2fe"}" stroke="{"#b91c1c" if i < 4 else "#0369a1"}" stroke-width="2"/>\n'
        s += f'<text x="{x+16}" y="{y+36}" font-size="15" font-weight="bold">{t}</text>\n'
        words = d.split(' · ')
        for j, wd in enumerate(words):
            s += f'<text x="{x+16}" y="{y+62+j*18}" font-size="12" fill="#334155">• {wd}</text>\n'
    s += '<text x="40" y="698" font-size="13" fill="#334155">ลำดับจริงขึ้นกับสถานการณ์และ emergency checklist ใน SMS — หลายข้อทำพร้อมกันโดยทีม · OOW ต้องไม่ลังเลทำการเพื่อความปลอดภัยทันที</text>\n'
    save('emergency-initial-actions.svg', s)

def wt_profile():
    w, h = 1000, 420
    s = head(w, h, 'Damage control plan (ภาพย่อ): ช่องผนึกน้ำ ประตู และระบบสูบน้ำ')
    s += '<path d="M 60 260 L 120 120 L 880 120 L 940 160 L 940 260 Q 900 300 860 300 L 120 300 Q 80 290 60 260 Z" fill="#e2e8f0" stroke="#0f172a" stroke-width="2"/>\n'
    s += '<line x1="40" y1="230" x2="960" y2="230" stroke="#0284c7" stroke-width="2" stroke-dasharray="8 5"/><text x="62" y="224" text-anchor="end" font-size="12" fill="#0284c7">waterline</text>\n'
    xs = [170, 300, 430, 560, 690, 800]
    labels = ['Fore peak', 'Hold 1', 'Hold 2', 'Hold 3', 'Hold 4', 'E/R', 'Aft peak']
    prev = 90
    for i, x in enumerate(xs):
        s += f'<line x1="{x}" y1="120" x2="{x}" y2="300" stroke="#b91c1c" stroke-width="4"/>\n'
    pts = [90] + xs + [910]
    for i in range(len(pts) - 1):
        cx = (pts[i] + pts[i + 1]) / 2
        s += f'<text x="{cx}" y="200" text-anchor="middle" font-size="13" font-weight="bold">{labels[i]}</text>\n'
    s += '<rect x="120" y="280" width="760" height="20" fill="#94a3b8" opacity="0.6"/><text x="500" y="295" text-anchor="middle" font-size="11">double bottom tanks</text>\n'
    s += '<rect x="783" y="250" width="14" height="30" fill="#facc15" stroke="#854d0e"/><text x="740" y="330" font-size="12" fill="#854d0e">WT door (ห้องเครื่อง–shaft/ห้องอื่น)</text>\n'
    # bilge main with a suction in each hold and the bilge/ballast pump in the E/R
    s += '<line x1="190" y1="268" x2="750" y2="268" stroke="#15803d" stroke-width="3"/>\n'
    for x in (235, 365, 495, 625):
        s += f'<line x1="{x}" y1="268" x2="{x}" y2="276" stroke="#15803d" stroke-width="3"/><circle cx="{x}" cy="276" r="4" fill="#fff" stroke="#15803d" stroke-width="2"/>\n'
    s += '<circle cx="750" cy="262" r="11" fill="#dcfce7" stroke="#15803d" stroke-width="2.5"/><text x="750" y="266" text-anchor="middle" font-size="11" font-weight="bold" fill="#15803d">P</text>\n'
    s += '<rect x="306" y="245" width="248" height="17" rx="3" fill="#fff" opacity="0.9"/><text x="312" y="258" font-size="11" fill="#15803d">bilge main + suction ทุกช่อง (ปั๊ม P ในห้องเครื่อง)</text>\n'
    s += '<text x="905" y="112" text-anchor="end" font-size="11" fill="#334155">แผนจริงแสดงทุกชั้นดาดฟ้า + ตำแหน่งวาล์ว/สวิตช์ควบคุม</text>\n'
    s += '<text x="170" y="112" text-anchor="middle" font-size="11" fill="#b91c1c">collision bulkhead</text>\n'
    s += '<rect x="40" y="345" width="920" height="65" rx="8" fill="#f8fafc" stroke="#94a3b8"/>\n'
    s += '<text x="54" y="368" font-size="13">SOLAS II-1/19: แผนควบคุมความเสียหายติดถาวรบนสะพาน แสดงขอบเขตช่องผนึกน้ำแต่ละชั้น ช่องเปิดและวิธีปิด ตำแหน่งควบคุม</text>\n'
    s += '<text x="54" y="392" font-size="13">ระบบ cross-flooding ฯลฯ และมีคู่มือ (damage control booklet) — เส้นสีแดง = ผนังกั้นน้ำ · เส้นเขียว = ระบบสูบน้ำท้องเรือ (bilge)</text>\n'
    save('damage-control-plan.svg', s)

def _arrowhead(x, y, ang, col, size=9):
    """small filled arrowhead at (x, y) pointing along ang (radians, SVG coords)"""
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    return (f'<path d="M {x:.1f} {y:.1f} L {x + size*math.cos(a1):.1f} {y + size*math.sin(a1):.1f} '
            f'L {x + size*math.cos(a2):.1f} {y + size*math.sin(a2):.1f} Z" fill="{col}"/>')

def _leg_arrows(pts, col):
    """arrowhead at 60% of every leg of a polyline"""
    out = ''
    for (a, b), (c, d) in zip(pts[:-1], pts[1:]):
        out += _arrowhead(a + 0.6 * (c - a), b + 0.6 * (d - b), math.atan2(d - b, c - a), col)
    return out

def _panel(x0, y0, title, lines, col):
    s = f'<rect x="{x0}" y="{y0}" width="310" height="392" rx="10" fill="#f8fafc" stroke="#cbd5e1"/>\n'
    s += f'<text x="{x0+155}" y="{y0+316}" text-anchor="middle" font-size="14" font-weight="bold" fill="{col}">{title}</text>\n'
    for i, ln in enumerate(lines):
        s += f'<text x="{x0+155}" y="{y0+338+i*17}" text-anchor="middle" font-size="11" fill="#334155">{ln}</text>\n'
    return s

def search_patterns():
    w, h = 1000, 900
    s = head(w, h, 'รูปแบบการค้นหาตาม IAMSAR (Search patterns) — S = ระยะห่างแนวค้นหา (track spacing)')
    X = [20, 345, 670]; Y = [48, 452]
    # ---- 1. expanding square (SS): CSP = datum, first leg into the wind, legs S,S,2S,2S,3S,3S ...
    x0, y0 = X[0], Y[0]
    s += _panel(x0, y0, 'Expanding square (SS)', ['CSP = datum เสมอ · ขาแรกหันเข้าหาลม', 'ความยาวขา S, S, 2S, 2S, 3S, 3S … เลี้ยว 90°',
                                                  'เป้าอยู่ใกล้ datum · ห้ามใช้หลายลำในพื้นที่เดียว'], '#1d4ed8')
    d = 27; cx, cy = x0 + 142, y0 + 162
    pts = [(cx, cy)]; x, y = cx, cy; dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]; leg = 1
    for k in range(10):
        dx, dy = dirs[k % 4]
        x += dx * leg * d; y += dy * leg * d
        pts.append((x, y))
        if k % 2 == 1: leg += 1
    s += '<polyline points="' + ' '.join(f'{a},{b}' for a, b in pts) + '" fill="none" stroke="#1d4ed8" stroke-width="2.4"/>\n'
    s += _leg_arrows(pts, '#1d4ed8') + '\n'
    labels = ['S', 'S', '2S', '2S', '3S', '3S', '4S', '4S', '5S', '5S']
    mcx, mcy = cx + 0.5 * d, cy - 0.5 * d
    for i, ((a, b), (c, e)) in enumerate(zip(pts[:-1], pts[1:])):
        if i not in (0, 1, 2, 3, 4, 8): continue
        mx, my = (a + c) / 2, (b + e) / 2
        if a == c: ox, oy = (11 if mx > mcx else -11), 4
        else: ox, oy = 0, (-6 if my < mcy else 15)
        s += f'<text x="{mx+ox:.0f}" y="{my+oy:.0f}" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e3a8a">{labels[i]}</text>'
    s += f'\n<circle cx="{cx}" cy="{cy}" r="5.5" fill="#b91c1c"/><circle cx="{x0+92}" cy="{y0+286}" r="5" fill="#b91c1c"/><text x="{x0+102}" y="{y0+290}" font-size="10.5" fill="#b91c1c">= datum = CSP (จุดเริ่มค้นหา)</text>\n'
    s += f'<line x1="{x0+40}" y1="{y0+22}" x2="{x0+40}" y2="{y0+62}" stroke="#0f172a" stroke-width="2" marker-end="url(#ar)"/><text x="{x0+48}" y="{y0+36}" font-size="11">ลม</text>\n'
    # ---- 2. sector search (VS): radius R, turns 120 deg to starboard
    x0, y0 = X[1], Y[0]
    s += _panel(x0, y0, 'Sector search (VS)', ['ตำแหน่งเป้าค่อนข้างแน่ชัด · พื้นที่วงกลมเล็ก', 'เรือ: รัศมี R มักใช้ 2–5 nm · เลี้ยวขวา 120°',
                                              'เวลาต่อขา t = R/V · ไม่พบ → รอบ 2 หมุน 30°'], '#15803d')
    cx, cy, r = x0 + 155, y0 + 150, 112
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#cbd5e1" stroke-dasharray="4 4"/>\n'
    def P(b): return (cx + r * math.sin(R(b)), cy - r * math.cos(R(b)))
    path = [(cx, cy), P(0), P(60), (cx, cy), P(240), P(300), (cx, cy), P(120), P(180), (cx, cy)]
    s += '<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in path) + '" fill="none" stroke="#15803d" stroke-width="2.2"/>\n'
    s += _leg_arrows(path, '#15803d') + '\n'
    for n, ((a, b), (c, e)) in enumerate(zip(path[:-1], path[1:])):
        mx, my = a + 0.38 * (c - a), b + 0.38 * (e - b)
        s += f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="8" fill="#fff" stroke="#15803d"/><text x="{mx:.1f}" y="{my+3.5:.1f}" text-anchor="middle" font-size="10" font-weight="bold" fill="#15803d">{n+1}</text>'
    s += f'\n<circle cx="{cx}" cy="{cy}" r="5.5" fill="#b91c1c"/><circle cx="{x0+62}" cy="{y0+290}" r="5" fill="#b91c1c"/><text x="{x0+72}" y="{y0+294}" font-size="10.5" fill="#b91c1c">= datum (ทิ้ง smoke float/ทุ่น) · เลข = ลำดับขา</text>\n'
    s += f'<text x="{cx+6}" y="{cy-r+46}" font-size="11" font-weight="bold" fill="#14532d">R</text>\n'
    # ---- 3. track line search (TSR / TSN)
    x0, y0 = X[2], Y[0]
    s += _panel(x0, y0, 'Track line search (TSR / TSN)', ['เป้าหายระหว่างเส้นทางที่รู้ (เช่นเรือไม่ถึงปลายทาง)', 'TSR: ค้นห่างเส้นทาง ½S ข้างหนึ่งแล้วย้อนกลับอีกข้าง',
                                                         'TSN: ค้นตามเส้นทางครั้งเดียวแล้วไปต่อ (ไม่ย้อน)'], '#b45309')
    ly = y0 + 112
    s += f'<line x1="{x0+30}" y1="{ly}" x2="{x0+285}" y2="{ly}" stroke="#64748b" stroke-width="2" stroke-dasharray="7 5"/>'
    s += f'<text x="{x0+30}" y="{ly-36}" font-size="10.5" fill="#475569">เส้นทางที่ตั้งใจของเป้า (intended track)</text>\n'
    tsr = [(x0 + 30, ly - 22), (x0 + 270, ly - 22), (x0 + 270, ly + 22), (x0 + 40, ly + 22)]
    s += '<polyline points="' + ' '.join(f'{a},{b}' for a, b in tsr) + '" fill="none" stroke="#b45309" stroke-width="2.2" marker-end="url(#ar)"/>' + _leg_arrows(tsr[:2], '#b45309') + '\n'
    s += f'<text x="{x0+292}" y="{ly-6}" font-size="10" fill="#92400e">½S</text><text x="{x0+292}" y="{ly+16}" font-size="10" fill="#92400e">½S</text><text x="{x0+150}" y="{ly+46}" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e">TSR (return)</text>\n'
    ly2 = y0 + 228
    s += f'<line x1="{x0+30}" y1="{ly2}" x2="{x0+285}" y2="{ly2}" stroke="#64748b" stroke-width="2" stroke-dasharray="7 5"/>'
    tsn = [(x0 + 30, ly2 - 26), (x0 + 110, ly2 - 26), (x0 + 110, ly2 + 26), (x0 + 190, ly2 + 26), (x0 + 190, ly2), (x0 + 280, ly2)]
    s += '<polyline points="' + ' '.join(f'{a},{b}' for a, b in tsn) + '" fill="none" stroke="#b45309" stroke-width="2.2" marker-end="url(#ar)"/>\n'
    s += f'<text x="{x0+150}" y="{ly2+48}" text-anchor="middle" font-size="11" font-weight="bold" fill="#92400e">TSN (non-return) — ค้นห่าง S ทั้งสองข้าง แล้วไปต่อ</text>\n'
    # ---- 4. parallel track (PS): CSP in a corner, half S inside both sides, legs parallel to long side
    x0, y0 = X[0], Y[1]
    s += _panel(x0, y0, 'Parallel track / sweep (PS)', ['พื้นที่ใหญ่ ตำแหน่งไม่แน่ชัด · แบ่ง sub-area ให้หลายหน่วย', 'CSP ที่มุมพื้นที่ ห่างจากขอบสองด้าน ½S',
                                                       'ขาค้นหาขนานด้านยาว · ระยะห่างแนว S'], '#7c3aed')
    ax, ay, aw, ah, S = x0 + 30, y0 + 40, 250, 200, 40
    s += f'<rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" fill="#ede9fe" fill-opacity="0.5" stroke="#7c3aed" stroke-dasharray="6 4"/>\n'
    pts = []
    for i in range(5):
        yy = ay + S / 2 + i * S
        pts += [(ax + S / 2, yy), (ax + aw - S / 2, yy)] if i % 2 == 0 else [(ax + aw - S / 2, yy), (ax + S / 2, yy)]
    s += '<polyline points="' + ' '.join(f'{a},{b}' for a, b in pts) + '" fill="none" stroke="#7c3aed" stroke-width="2.2" marker-end="url(#ar)"/>' + _leg_arrows(pts[:2], '#7c3aed') + '\n'
    s += f'<circle cx="{ax+S/2}" cy="{ay+S/2}" r="5" fill="#b91c1c"/><text x="{ax+S/2}" y="{ay-6}" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#b91c1c">CSP</text>\n'
    s += f'<line x1="{ax+aw+10}" y1="{ay+S/2}" x2="{ax+aw+10}" y2="{ay+S*1.5}" stroke="#334155"/><text x="{ax+aw+13}" y="{ay+S+4}" font-size="11" font-weight="bold">S</text>'
    s += f'<text x="{ax-4}" y="{ay+S/2+4}" text-anchor="end" font-size="10">½S</text>\n'
    s += f'<line x1="{ax+aw/2}" y1="{ay+ah+8}" x2="{ax+aw/2}" y2="{ay+ah+30}" stroke="#334155" stroke-width="1.5" marker-end="url(#ar)"/><text x="{ax+aw/2+8}" y="{ay+ah+24}" font-size="10.5">direction of creep</text>\n'
    # ---- 5. creeping line (CS): legs parallel to the short side, creep along the long (major) axis
    x0, y0 = X[1], Y[1]
    s += _panel(x0, y0, 'Creeping line (CS)', ['ขาค้นหาขนานด้านสั้น เคลื่อนไปตามแกนยาว', 'ใช้เมื่อพื้นที่ยาวแคบ/เป้าน่าจะอยู่ปลายด้านหนึ่ง',
                                              'ส่วนใหญ่เป็นงานอากาศยาน (รายละเอียดใน Vol II)'], '#0f766e')
    ax, ay, aw, ah, S = x0 + 25, y0 + 70, 262, 150, 37
    s += f'<rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" fill="#ccfbf1" fill-opacity="0.5" stroke="#0f766e" stroke-dasharray="6 4"/>\n'
    pts = []
    for i in range(7):
        xx = ax + S / 2 + i * S
        pts += [(xx, ay + S / 2), (xx, ay + ah - S / 2)] if i % 2 == 0 else [(xx, ay + ah - S / 2), (xx, ay + S / 2)]
    s += '<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts) + '" fill="none" stroke="#0f766e" stroke-width="2.2" marker-end="url(#ar)"/>' + _leg_arrows(pts[:2], '#0f766e') + '\n'
    s += f'<text x="{ax+S/2}" y="{ay-8}" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#b91c1c">CSP</text><circle cx="{ax+S/2}" cy="{ay+S/2}" r="5" fill="#b91c1c"/>\n'
    s += f'<line x1="{ax}" y1="{ay+ah+16}" x2="{ax+aw}" y2="{ay+ah+16}" stroke="#334155" stroke-width="1.5" marker-end="url(#ar)"/><text x="{ax+aw/2}" y="{ay+ah+32}" text-anchor="middle" font-size="10.5">แกนยาว (major axis) = ทิศที่ค้นคืบหน้า</text>\n'
    s += f'<line x1="{ax+S/2}" y1="{ay-22}" x2="{ax+S*1.5}" y2="{ay-22}" stroke="#334155"/><text x="{ax+S}" y="{ay-27}" text-anchor="middle" font-size="11" font-weight="bold">S</text>\n'
    # ---- 6. co-ordinated vessel-aircraft (CSC)
    x0, y0 = X[2], Y[1]
    s += _panel(x0, y0, 'Vessel–aircraft co-ordinated (CSC)', ['อากาศยานบิน creeping line ตัดเรือไปมา', 'เรือแล่นตามแกนกลางเป็นจุดอ้างอิงตามที่ OSC สั่ง',
                                                               'ความเร็วเรือ Vs = S × Va ÷ (L + S)'], '#be123c')
    ax, ay, aw, ah, S = x0 + 25, y0 + 60, 262, 170, 37
    pts = []
    for i in range(7):
        xx = ax + S / 2 + i * S
        pts += [(xx, ay), (xx, ay + ah)] if i % 2 == 0 else [(xx, ay + ah), (xx, ay)]
    s += '<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts) + '" fill="none" stroke="#be123c" stroke-width="2" stroke-dasharray="7 4"/>\n'
    my = ay + ah / 2
    s += f'<line x1="{ax}" y1="{my}" x2="{ax+aw}" y2="{my}" stroke="#0f172a" stroke-width="3" marker-end="url(#ar)"/>'
    s += f'<path d="M {ax+150} {my-7} L {ax+174} {my-7} L {ax+184} {my} L {ax+174} {my+7} L {ax+150} {my+7} Z" fill="#334155"/>\n'
    s += f'<rect x="{ax+143}" y="{my+12}" width="50" height="16" rx="3" fill="#fff"/><text x="{ax+168}" y="{my+24}" text-anchor="middle" font-size="10.5" font-weight="bold">เรือ (Vs)</text><text x="{ax+aw-2}" y="{ay-8}" text-anchor="end" font-size="10.5" font-weight="bold" fill="#be123c">อากาศยาน (Va) — ขายาว L</text>\n'
    s += f'<line x1="{ax+S/2}" y1="{ay+ah+14}" x2="{ax+S*1.5}" y2="{ay+ah+14}" stroke="#334155"/><text x="{ax+S}" y="{ay+ah+28}" text-anchor="middle" font-size="11" font-weight="bold">S</text>\n'
    s += ('<text x="500" y="872" text-anchor="middle" font-size="12" fill="#334155">ค้นหาคนในน้ำด้วย SS/VS: เดินเรือแบบ DR หรืออ้างอิง smoke float/ทุ่นที่ทิ้งไว้ที่ datum '
          'เพื่อให้รูปแบบเคลื่อนไปกับกระแสน้ำเหมือนเป้า (IAMSAR Vol III Section 3)</text>\n')
    save('sar-search-patterns.svg', s)

def sar_org():
    w, h = 1000, 420
    s = head(w, h, 'โครงสร้างการค้นหาและช่วยเหลือ (SAR system) ตาม IAMSAR')
    def b(x, y, t, sub, c='#e0f2fe', sc='#0369a1', ww=220):
        return (f'<rect x="{x}" y="{y}" width="{ww}" height="70" rx="10" fill="{c}" stroke="{sc}" stroke-width="2"/>'
                f'<text x="{x+ww/2}" y="{y+30}" text-anchor="middle" font-size="14" font-weight="bold">{t}</text>'
                f'<text x="{x+ww/2}" y="{y+52}" text-anchor="middle" font-size="11" fill="#334155">{sub}</text>\n')
    s += b(390, 55, 'SAR Coordinator (SC)', 'รัฐ/หน่วยงานรับผิดชอบระบบ SAR', '#ede9fe', '#6d28d9')
    s += b(390, 160, 'RCC / MRCC → SMC', 'SAR Mission Coordinator', '#dbeafe', '#1d4ed8')
    s += b(120, 270, 'OSC (On-Scene Coordinator)', 'มักเป็นเรือ/หน่วยแรกที่ถึง', '#dcfce7', '#15803d')
    s += b(390, 270, 'SRU / เรือพาณิชย์', 'หน่วยค้นหา (ships, boats)', '#fef3c7', '#b45309')
    s += b(660, 270, 'ACO / อากาศยาน', 'Aircraft coordinator', '#fee2e2', '#b91c1c')
    for (x1, y1, x2, y2) in [(500, 125, 500, 158), (500, 230, 230, 268), (500, 230, 500, 268), (500, 230, 770, 268)]:
        s += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#334155" stroke-width="2" marker-end="url(#ar)"/>\n'
    s += '<line x1="342" y1="305" x2="388" y2="305" stroke="#334155" stroke-width="2" stroke-dasharray="5 4"/><line x1="612" y1="305" x2="658" y2="305" stroke="#334155" stroke-width="2" stroke-dasharray="5 4"/>\n'
    s += '<text x="40" y="380" font-size="13">ระยะของเหตุ: Uncertainty (INCERFA) → Alert (ALERFA) → Distress (DETRESFA)</text>\n'
    s += '<text x="40" y="402" font-size="13">เรือพาณิชย์ที่ได้รับสัญญาณ: ตอบรับ · plot · แจ้ง RCC · ไปที่เกิดเหตุ (SOLAS V/33) · ทำหน้าที่ OSC ถ้าได้รับมอบหมาย</text>\n'
    save('sar-organization.svg', s)

if __name__ == '__main__':
    flow(); wt_profile(); search_patterns(); sar_org(); print('ok')
