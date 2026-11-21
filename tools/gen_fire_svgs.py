"""ภาพประกอบบท 3.3 การป้องกันและดับเพลิง"""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"


def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker>'
            '<marker id="arR" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#b91c1c"/></marker></defs>\n'
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


def tetra():
    w, h = 1000, 500
    s = head(w, h, 'องค์ประกอบของไฟ (Fire triangle / tetrahedron) และหลักการดับไฟ')
    cx, cy = 260, 270
    pts = [(cx, cy - 170), (cx - 180, cy + 130), (cx + 180, cy + 130)]
    s += f'<polygon points="{" ".join(f"{a},{b}" for a, b in pts)}" fill="#fff7ed" stroke="#c2410c" stroke-width="4"/>'
    s += txt(cx - 110, cy - 30, 'เชื้อเพลิง', 15, 'end', '#7c2d12', True) + txt(cx - 110, cy - 12, '(Fuel)', 12, 'end', '#7c2d12')
    s += txt(cx + 110, cy - 30, 'ออกซิเจน', 15, 'start', '#1d4ed8', True) + txt(cx + 110, cy - 12, '(Oxygen ≥ ~16%)', 12, 'start', '#1d4ed8')
    s += txt(cx, cy + 160, 'ความร้อน (Heat)', 15, 'middle', '#b91c1c', True)
    s += f'<circle cx="{cx}" cy="{cy+20}" r="52" fill="#fecaca" stroke="#b91c1c" stroke-width="2"/>'
    s += txt(cx, cy + 14, 'ปฏิกิริยาลูกโซ่', 13, 'middle', '#7f1d1d', True) + txt(cx, cy + 32, '(chain reaction)', 11, 'middle', '#7f1d1d')
    bx = 520
    rows = [('Cooling (ลดความร้อน)', 'น้ำ — ดูดความร้อนสูงมาก (จุดเด่นของน้ำ)', '#b91c1c'),
            ('Smothering (ตัดออกซิเจน)', 'โฟม CO₂ ผ้าห่มดับไฟ ปิดช่องเปิด/ระบายอากาศ', '#1d4ed8'),
            ('Starving (ตัดเชื้อเพลิง)', 'ปิดวาล์วน้ำมัน (quick-closing) ย้ายของไหม้ได้ออก', '#7c2d12'),
            ('Breaking chain reaction', 'ผงเคมีแห้ง (dry powder) สารดับเพลิงบางชนิด', '#7c3aed')]
    s += txt(bx, 80, 'หลักการดับไฟ = เอาองค์ประกอบใดองค์ประกอบหนึ่งออก', 14, 'start', '#0f172a', True)
    for i, (t, d, col) in enumerate(rows):
        y = 110 + i * 70
        s += rect(bx, y, 450, 58, '#fff', col, 2, 10)
        s += txt(bx + 16, y + 24, t, 14, 'start', col, True) + txt(bx + 16, y + 45, d, 12)
    s += rect(bx, 400, 450, 80, '#f8fafc', '#94a3b8', 1, 10)
    for i, t in enumerate(['Flash point — อุณหภูมิต่ำสุดที่ไอติดไฟวาบเมื่อมีประกายไฟ', 'Fire point — ไอเกิดพอให้ลุกไหม้ต่อเนื่อง',
                           'Auto-ignition temp. — ติดไฟเองโดยไม่ต้องมีประกายไฟ']):
        s += txt(bx + 14, 424 + i * 20, t, 12)
    save('fire-tetrahedron.svg', s)


def classes():
    w, h = 1000, 520
    s = head(w, h, 'ประเภทของไฟ (ISO 3941 — ใช้ในแนวทาง IMO) และสารดับเพลิงที่เหมาะสม')
    cls = [('A', 'ของแข็ง (ไม้ ผ้า กระดาษ พลาสติก)', '#15803d'), ('B', 'ของเหลวไวไฟ (น้ำมัน สี ตัวทำละลาย)', '#b91c1c'),
           ('C', 'ก๊าซไวไฟ (LPG อะเซทิลีน มีเทน)', '#ca8a04'), ('D', 'โลหะ (Mg, ผง Al, Na, Li)', '#475569'),
           ('F', 'น้ำมันทำอาหาร (ในครัว)', '#7c3aed'), ('ไฟฟ้า', 'อุปกรณ์ที่มีไฟ (ไม่ใช่ class ใน ISO)', '#0369a1')]
    agents = ['น้ำ (jet)', 'น้ำ (spray/mist)', 'โฟม', 'ผง ABC', 'CO₂', 'Wet chemical', 'ผงพิเศษ (D)']
    table = [  # A B C D F E
        ['✔', '✘', '✘', '✘', '✘', '✘'],
        ['✔', '△', '✘', '✘', '✘', '△'],
        ['✔', '✔', '✘', '✘', '△', '✘'],
        ['✔', '✔', '△', '✘', '✘', '✔'],
        ['△', '✔', '✘', '✘', '✘', '✔'],
        ['✔', '✘', '✘', '✘', '✔', '✘'],
        ['✘', '✘', '✘', '✔', '✘', '✘']]
    x0, y0, cw, rh = 230, 70, 120, 46
    for j, (c, d, col) in enumerate(cls):
        x = x0 + j * cw
        s += rect(x, y0, cw - 6, 70, col, col, 0, 8) + txt(x + (cw - 6) / 2, y0 + 30, c, 22, 'middle', '#fff', True)
        parts = d.split(' (')
        s += txt(x + (cw - 6) / 2, y0 + 52, parts[0], 11, 'middle', '#fff', True)
        if len(parts) > 1:
            s += txt(x + (cw - 6) / 2, y0 + 66, '(' + parts[1], 9, 'middle', '#fff')
    for i, a in enumerate(agents):
        y = y0 + 80 + i * rh
        s += rect(40, y, 180, rh - 6, '#f1f5f9', '#cbd5e1', 1, 6) + txt(52, y + 26, a, 13, 'start', '#0f172a', True)
        for j in range(6):
            v = table[i][j]
            col = {'✔': '#15803d', '✘': '#b91c1c', '△': '#ca8a04'}[v]
            bg = {'✔': '#dcfce7', '✘': '#fee2e2', '△': '#fef9c3'}[v]
            s += rect(x0 + j * cw, y, cw - 6, rh - 6, bg, '#e2e8f0', 1, 6) + txt(x0 + j * cw + (cw - 6) / 2, y + 27, v, 18, 'middle', col, True)
    s += txt(40, 488, '✔ เหมาะสม · △ ใช้ได้จำกัด/มีเงื่อนไข (เช่น CO₂ กับไฟ A ดับผิวแต่ไม่เย็นลึก; ไฟก๊าซต้องปิดต้นทางก่อน; spray น้ำกับไฟฟ้าแรงต่ำตามคู่มือ) · ✘ ไม่เหมาะ/อันตราย', 12)
    s += txt(40, 508, 'ระบบสหรัฐฯ (NFPA): A, B, C = ไฟฟ้า, D, K = น้ำมันทำอาหาร — ดูป้ายบนถังดับเพลิงของเรือเสมอ', 12, 'start', '#475569')
    save('fire-classes.svg', s)


def development():
    w, h = 1000, 510
    s = head(w, h, 'การถ่ายเทความร้อนและพัฒนาการของไฟในห้อง (Fire development)')
    # heat transfer
    s += txt(230, 66, 'การถ่ายเทความร้อน 3 แบบ', 14, 'middle', bold=True)
    items = [('Conduction', 'ผ่านเนื้อโลหะ — ผนังเหล็ก/ท่อ ทำให้ไฟลาม|ไปห้องข้างเคียง (ต้อง boundary cooling)'),
             ('Convection', 'อากาศร้อน/ควันลอยขึ้น — ผ่านช่องบันได|ท่อระบายอากาศ ลามขึ้นชั้นบน'),
             ('Radiation', 'รังสีความร้อนแผ่ไปทุกทิศ — จุดไฟวัตถุ|ที่อยู่ใกล้โดยไม่ต้องสัมผัส')]
    for i, (t, d) in enumerate(items):
        y = 90 + i * 80
        s += rect(40, y, 380, 68, '#fff7ed', '#c2410c', 1.5, 10)
        s += txt(56, y + 24, t, 14, 'start', '#9a3412', True)
        for j, c in enumerate(d.split('|')):
            s += txt(56, y + 44 + j * 16, c, 11.5)
    # development curve
    gx, gy, gw, gh = 500, 90, 450, 260
    s += line(gx, gy + gh, gx + gw, gy + gh, '#0f172a', 1.5) + line(gx, gy, gx, gy + gh, '#0f172a', 1.5)
    s += txt(gx + gw / 2, gy + gh + 30, 'เวลา', 12, 'middle')
    s += f'<text x="{gx-20}" y="{gy+gh/2}" font-size="12" text-anchor="middle" transform="rotate(-90 {gx-20} {gy+gh/2})">อุณหภูมิในห้อง</text>'
    pts = []
    for i in range(0, 101):
        t = i / 100
        if t < 0.15: v = 0.05 + t * 0.3
        elif t < 0.45: v = 0.095 + (t - 0.15) ** 2 * 3.5
        elif t < 0.5: v = 0.41 + (t - 0.45) * 9
        elif t < 0.75: v = 0.86 + 0.04 * math.sin((t - 0.5) * 12)
        else: v = 0.86 - (t - 0.75) * 2.6
        pts.append((gx + t * gw, gy + gh - v * gh))
    s += '<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts) + '" fill="none" stroke="#b91c1c" stroke-width="3.5"/>'
    for t, lab in ((0.07, 'เริ่มต้น'), (0.3, 'ลุกลาม'), (0.47, 'Flashover'), (0.62, 'เต็มห้อง'), (0.88, 'มอด')):
        s += txt(gx + t * gw, gy + gh + 16, lab, 11, 'middle', '#7f1d1d', True)
    s += line(gx + 0.47 * gw, gy + 10, gx + 0.47 * gw, gy + gh, '#7f1d1d', 1, '4 3')
    s += rect(40, 400, 920, 95, '#f8fafc', '#94a3b8', 1, 10)
    for i, t in enumerate(['Flashover — ทุกอย่างในห้องติดไฟพร้อมกันจากความร้อนสะสม (ไม่มีใครรอดในห้องได้) → ต้องดับ/จำกัดไฟก่อนถึงจุดนี้',
                           'Backdraught — ห้องปิดที่ไฟขาดออกซิเจน มีก๊าซร้อนสะสม เมื่อเปิดประตูอากาศเข้า → ระเบิดเป็นลูกไฟ: ตรวจความร้อนประตู เปิดอย่างระมัดระวัง',
                           'ควันและก๊าซพิษ (CO, HCN ฯลฯ) ฆ่าคนมากกว่าเปลวไฟ — ใช้ SCBA, หมอบต่ำ, ปิดประตูกันควันลาม, EEBD สำหรับหนีออก']):
        s += txt(56, 424 + i * 24, t, 12)
    save('fire-development.svg', s)


def systems():
    w, h = 1000, 560
    s = head(w, h, 'ระบบและอุปกรณ์ดับเพลิงบนเรือสินค้า (ภาพรวม)')
    s += '<path d="M 60 300 L 120 360 L 860 360 L 930 290 L 940 200 L 120 200 L 60 230 Z" fill="#f1f5f9" stroke="#0f172a" stroke-width="2.5"/>'
    s += rect(80, 100, 120, 100, '#e2e8f0', '#0f172a', 2)
    s += line(20, 300, 980, 300, '#0284c7', 1.5, '8 5')
    # fire main
    s += line(130, 215, 900, 215, '#b91c1c', 5)
    for x in (260, 400, 540, 680, 820):
        s += f'<circle cx="{x}" cy="215" r="7" fill="#fff" stroke="#b91c1c" stroke-width="3"/>'
    s += txt(540, 238, 'Fire main + hydrants (ดาดฟ้าและภายใน)', 12, 'middle', '#b91c1c', True)
    s += rect(150, 300, 70, 40, '#fecaca', '#b91c1c', 2) + txt(185, 325, 'Fire pumps', 10.5, 'middle', '#7f1d1d', True)
    s += rect(760, 300, 70, 40, '#fecaca', '#b91c1c', 2) + txt(795, 318, 'Emergency', 10, 'middle', '#7f1d1d', True) + txt(795, 331, 'fire pump', 10, 'middle', '#7f1d1d', True)
    s += line(185, 300, 185, 220, '#b91c1c', 3) + line(795, 300, 795, 220, '#b91c1c', 3)
    s += rect(210, 150, 60, 45, '#e0f2fe', '#0369a1', 2) + txt(240, 170, 'CO₂', 11, 'middle', '#075985', True) + txt(240, 185, 'room', 10, 'middle', '#075985')
    s += f'<path d="M 270 172 L 330 172 L 330 260 L 600 260" fill="none" stroke="#0369a1" stroke-width="2.5" stroke-dasharray="6 3"/>'
    s += txt(470, 276, 'ท่อ CO₂ ไปห้องเครื่อง/ระวาง (total flooding)', 11, 'middle', '#075985')
    s += rect(85, 110, 24, 24, '#fde68a', '#92400e', 1.5) + txt(97, 127, 'FCP', 8, 'middle', '#78350f', True)
    s += rect(150, 140, 24, 24, '#bbf7d0', '#15803d', 1.5) + txt(162, 157, 'FO', 9, 'middle', '#14532d', True)
    s += f'<circle cx="440" cy="190" r="6" fill="#7c3aed"/>' + f'<circle cx="610" cy="190" r="6" fill="#7c3aed"/>'
    s += rect(900, 185, 30, 18, '#94a3b8', '#0f172a', 1.5) + txt(915, 175, 'ISC', 10, 'middle', '#0f172a', True)
    legend = [('#fde68a', 'FCP — Fire control plan (ติดถาวร + สำเนาในกล่องกันน้ำนอกที่พักให้หน่วยดับเพลิงฝั่ง)'),
              ('#bbf7d0', 'FO — Fire-fighter\'s outfits (เรือสินค้าอย่างน้อย 2 ชุด, tanker เพิ่ม) + SCBA ≥ 1,200 L อากาศ'),
              ('#7c3aed', 'Detectors และ manual call points → แผงระบบตรวจจับ/สัญญาณบนสะพานเดินเรือ'),
              ('#fecaca', 'Fire pumps: เรือ ≥ 1,000 GT อย่างน้อย 2 เครื่องแยกกัน + emergency fire pump ตามข้อกำหนด'),
              ('#94a3b8', 'ISC — International shore connection: ต่อน้ำจากฝั่ง/เรืออื่นเข้า fire main (ขนาดหน้าแปลนมาตรฐาน)'),
              ('#e0f2fe', 'ระบบคงที่ (fixed): CO₂, โฟม, water mist/local application, sprinkler, ผงเคมี, inert gas (tanker)')]
    for i, (c, t) in enumerate(legend):
        y = 390 + i * 26
        s += rect(40, y - 14, 18, 18, c, '#0f172a', 1) + txt(68, y, t, 12)
    s += txt(500, 552, 'ถังดับเพลิงแบบหิ้ว (portable) และแบบล้อ (semi-portable) ติดตั้งตามแผน fire control plan · EEBD สำหรับหนีออกจากพื้นที่อันตราย (อย่างน้อย 10 นาที)', 11.5, 'middle', '#475569')
    save('fire-systems-overview.svg', s)


def organisation():
    w, h = 1000, 480
    s = head(w, h, 'การจัดทีมเหตุฉุกเฉินไฟไหม้ตาม Muster list (ตัวอย่างโครงสร้างทั่วไป)')
    nodes = [(500, 90, 'Command (สะพานเดินเรือ)', 'นายเรือ + OOW: สั่งการ เดินเรือ สื่อสาร บันทึก', '#1d4ed8'),
             (170, 230, 'Emergency team 1', 'ต้นเรือ — ทีมดับเพลิงหลัก (2 SCBA)', '#b91c1c'),
             (500, 230, 'Engine room team', 'ต้นกล — เครื่อง ปั๊ม ระบบดับเพลิงคงที่', '#c2410c'),
             (830, 230, 'Emergency team 2 / Support', 'ทีมสำรอง ทดแทน ขนอุปกรณ์ boundary cooling', '#7c3aed'),
             (330, 370, 'First aid team', 'ปฐมพยาบาล เปลหาม', '#15803d'), (670, 370, 'LSA preparation', 'เตรียมเรือชูชีพ/แพ (ถ้าต้องสละเรือ)', '#0369a1')]
    # วาดเส้นเชื่อมก่อน แล้วจึงวาดกล่อง (พื้นขาว) ทับ เพื่อไม่ให้เส้นผ่านตัวอักษร
    for x, y in ((170, 194), (500, 194), (830, 194)):
        s += line(500, 126, x, y, '#94a3b8', 2)
    for x in (330, 670):
        s += line(500, 126, x, 334, '#cbd5e1', 1.5, '5 4')
    for x, y, t, d, col in nodes:
        s += rect(x - 150, y - 36, 300, 72, '#fff', col, 2.5, 12)
        s += txt(x, y - 8, t, 14, 'middle', col, True) + txt(x, y + 16, d, 11.5, 'middle')
    s += txt(500, 452, 'ใช้ชื่อตำแหน่ง/หน้าที่ตาม muster list ของเรือจริง (SOLAS III/8, III/37) — การสื่อสารด้วยวิทยุพกพาชนิดป้องกันการระเบิด อย่างน้อย 2 เครื่องต่อทีมดับเพลิง', 12, 'middle', '#334155')
    save('fire-organisation.svg', s)


def oil_fire():
    w, h = 1000, 560
    s = head(w, h, 'ไฟไหม้จากระบบน้ำมันในห้องเครื่อง — ลำดับการกระทำทั่วไป')
    steps = [('ตรวจพบ / สัญญาณ', 'alarm, กดสัญญาณไฟไหม้\nแจ้งสะพานเดินเรือ', '#b91c1c'),
             ('ตัดเชื้อเพลิง', 'หยุดปั๊มน้ำมัน/purifiers (emergency stop)\nปิด quick-closing valves จากระยะไกล', '#b91c1c'),
             ('ตัดอากาศ', 'หยุดพัดลม ปิด fire dampers\nปิดประตู skylight ช่องเปิด', '#c2410c'),
             ('ดับในขั้นต้น', 'ถังโฟม/ผง, water mist/local application\nห้ามใช้น้ำแบบลำ (jet) กับน้ำมัน', '#c2410c'),
             ('ถ้าควบคุมไม่ได้', 'อพยพ นับคนให้ครบ ปิดห้อง\nนายเรือสั่งปล่อย CO₂ ตามขั้นตอน', '#1d4ed8'),
             ('Boundary cooling', 'ฉีดน้ำหล่อเย็นผนัง/ดาดฟ้ารอบห้อง\nเฝ้าทุกด้าน (6 ด้าน)', '#1d4ed8'),
             ('เดินเรือและสื่อสาร', 'ไฟ NUC, แจ้ง MRCC/เรือใกล้เคียง\nบริษัท, เตรียม LSA', '#15803d'),
             ('หลังดับ', 'รอให้เย็น (ห้ามเปิดเร็ว — ติดใหม่)\nวัดก๊าซก่อนเข้า เฝ้าระวัง บันทึก', '#15803d')]
    for i, (t, d, col) in enumerate(steps):
        c, r = i % 4, i // 4
        x, y = 30 + c * 240, 70 + r * 220
        s += rect(x, y, 220, 180, '#fff', col, 2.5, 12)
        s += rect(x, y, 220, 40, col, col, 0, 12) + rect(x, y + 25, 220, 15, col, col, 0)
        s += txt(x + 110, y + 27, f'{i+1}. {t}', 14, 'middle', '#fff', True)
        for j, part in enumerate(d.split('\n')):
            s += txt(x + 110, y + 80 + j * 24, part, 11.5, 'middle')
        if c < 3:
            s += line(x + 222, y + 90, x + 238, y + 90, '#0f172a', 2, mk='ar')
    s += txt(500, 530, 'สาเหตุที่พบบ่อย: น้ำมันพ่น/รั่วจากท่อแรงดันสูง ข้อต่อ ตัวกรอง ลงบนพื้นผิวร้อน (ท่อไอเสีย turbocharger) — SOLAS II-2/4 กำหนดฉนวนพื้นผิวร้อนและท่อน้ำมันแรงดันสูงแบบมีปลอก', 11.5, 'middle', '#334155')
    s += txt(500, 550, 'ขั้นตอนจริงตาม SMS และ fire safety operational booklet ของเรือ — การปล่อย CO₂ เป็นการตัดสินใจของนายเรือ', 11.5, 'middle', '#b91c1c')
    save('fire-oil-system-actions.svg', s)


def drill_cycle():
    w, h = 1000, 500
    s = head(w, h, 'การจัดการฝึกซ้อมดับเพลิง (Organizing fire drills)')
    cx, cy, r = 260, 270, 160
    steps = ['วางแผน|สถานการณ์', 'ประเมินความเสี่ยง|ของการฝึก', 'บรีฟทีม', 'ปฏิบัติเหมือน|เหตุจริง', 'ประเมินผล', 'Debrief|บทเรียน', 'บันทึก|ปรับปรุง']
    for i, t in enumerate(steps):
        a = -90 + i * 360 / len(steps)
        x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="52" fill="#fff7ed" stroke="#c2410c" stroke-width="2.5"/>'
        parts = t.split('|')
        for j, p_ in enumerate(parts):
            s += txt(x, y + 4 + (j - (len(parts) - 1) / 2) * 16, p_, 11, 'middle', '#7c2d12', True)
    s += f'<circle cx="{cx}" cy="{cy}" r="70" fill="#fef2f2" stroke="#b91c1c" stroke-width="2" stroke-dasharray="6 4"/>'
    s += txt(cx, cy - 4, 'ทุกเดือน', 14, 'middle', '#b91c1c', True) + txt(cx, cy + 16, '(SOLAS III/19)', 11, 'middle', '#b91c1c')
    bx = 500
    s += rect(bx, 60, 470, 420, '#f8fafc', '#94a3b8', 1, 10)
    L = ['สิ่งที่ fire drill ต้องมี (SOLAS III/19.3.4)', '• รายงานตัวที่สถานีและเตรียมปฏิบัติหน้าที่ตาม muster list', '• เดินเครื่องสูบดับเพลิง ใช้หัวฉีดน้ำอย่างน้อย 2 ชุด',
         '  แสดงว่าระบบทำงานได้', '• ตรวจชุดนักดับเพลิงและอุปกรณ์ช่วยชีวิตส่วนบุคคล', '• ตรวจอุปกรณ์สื่อสารที่เกี่ยวข้อง',
         '• ตรวจการทำงานของประตูกันน้ำ ประตูกันไฟ fire dampers', '  และช่องลมเข้า-ออกหลักของระบบระบายอากาศในพื้นที่ฝึก',
         '• ตรวจการเตรียมการสำหรับการสละเรือที่อาจตามมา', '', 'ข้อกำหนดเวลา', '• ลูกเรือทุกคนฝึก fire drill และ abandon ship drill',
         '  อย่างน้อยเดือนละครั้ง', '• ภายใน 24 ชม. หลังออกจากท่า ถ้าลูกเรือเกิน 25%', '  ไม่ได้ร่วมฝึกบนเรือลำนั้นในเดือนก่อน',
         '• บันทึกใน logbook (วันที่ รายละเอียด อุปกรณ์ที่ใช้)', '', 'เคล็ดลับ: เปลี่ยนสถานที่และชนิดไฟทุกครั้ง (ห้องเครื่อง ครัว',
         'ห้องพัก ระวาง/ตู้ DG ห้องสี ไฟฟ้า) ใส่คนบาดเจ็บ/ควัน']
    for i, l in enumerate(L):
        s += txt(bx + 14, 84 + i * 21, l, 12.2, 'start', '#0f172a', l in (L[0], 'ข้อกำหนดเวลา'))
    save('fire-drill-cycle.svg', s)


def shore_connection():
    w, h = 1000, 445
    s = head(w, h, 'International shore connection (FSS Code บทที่ 2) — มาตรฐานหน้าแปลน')
    cx, cy = 260, 230
    s += f'<circle cx="{cx}" cy="{cy}" r="140" fill="#e2e8f0" stroke="#0f172a" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="50" fill="#fff" stroke="#0f172a" stroke-width="3"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="104" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5 4"/>'
    for a in (45, 135, 225, 315):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        x, y = cx + 104 * ca, cy + 104 * sa
        # ร่อง (slot) จากรูออกไปถึงขอบหน้าแปลนตาม FSS Code
        s += line(x, y, cx + 143 * ca, cy + 143 * sa, '#ffffff', 28)
        for side in (-1, 1):
            px, py = -sa * 14 * side, ca * 14 * side
            s += line(x + px, y + py, cx + 139.5 * ca + px, cy + 139.5 * sa + py, '#0f172a', 2)
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="#fff" stroke="#0f172a" stroke-width="2"/>'
        s += line(x - sa * 13, y + ca * 13, x + sa * 13, y - ca * 13, '#ffffff', 4)
    s += line(cx - 140, cy + 165, cx + 140, cy + 165, '#b91c1c', 1.5, mk='arR') + line(cx + 140, cy + 165, cx - 140, cy + 165, '#b91c1c', 1.5, mk='arR')
    s += txt(cx, cy + 185, 'เส้นผ่านศูนย์กลางนอก 178 mm', 12, 'middle', '#b91c1c', True)
    bx = 480
    s += rect(bx, 60, 490, 320, '#f8fafc', '#94a3b8', 1, 10)
    L = ['ขนาดมาตรฐาน (FSS Code บทที่ 2)', '• เส้นผ่านศูนย์กลางนอก 178 mm', '• เส้นผ่านศูนย์กลางใน 64 mm', '• วงกลมรูน็อต (bolt circle) 132 mm',
         '• รู 4 รู Ø 19 mm เว้นระยะเท่ากัน มีร่องเปิดถึงขอบหน้าแปลน', '• ความหนาหน้าแปลนอย่างน้อย 14.5 mm หน้าเรียบ (flat face)', '• น็อต 4 ชุด Ø 16 mm ยาว 50 mm และแหวน 8 ตัว',
         '• วัสดุรับแรงดันใช้งาน 1.0 N/mm²', '', 'เรือ ≥ 500 GT ต้องมีอย่างน้อย 1 ชุด (SOLAS II-2/10.2.1.7)', 'ใช้ต่อระบบน้ำดับเพลิงระหว่างเรือกับฝั่ง/เรือลำอื่น',
         'เก็บพร้อมปะเก็นและอุปกรณ์ ใช้ได้ทั้งสองกราบ', 'ตำแหน่งระบุใน fire control plan']
    for i, l in enumerate(L):
        s += txt(bx + 14, 86 + i * 22.5, l, 12.3, 'start', '#0f172a', i == 0)
    save('fire-shore-connection.svg', s)


if __name__ == '__main__':
    tetra(); classes(); development(); systems(); organisation(); oil_fire(); drill_cycle(); shore_connection()
