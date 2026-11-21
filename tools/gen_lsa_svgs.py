"""ภาพประกอบบท 3.4 อุปกรณ์ช่วยชีวิต (Life-saving appliances)"""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"


def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker>'
            '<marker id="arR" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#b91c1c"/></marker>'
            '<marker id="arB" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#1d4ed8"/></marker></defs>\n'
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


def arrangement():
    w, h = 1000, 560
    s = head(w, h, 'การจัดอุปกรณ์ช่วยชีวิตบนเรือสินค้า (ตัวอย่างมองจากด้านบน — ภาพแนวคิด)')
    s += '<path d="M 80 160 L 820 160 Q 930 160 960 260 Q 930 360 820 360 L 80 360 Q 50 360 50 330 L 50 190 Q 50 160 80 160 Z" fill="#f1f5f9" stroke="#0f172a" stroke-width="2.5"/>'
    s += rect(70, 200, 150, 120, '#e2e8f0', '#0f172a', 2) + txt(145, 265, 'ที่พัก/สะพาน', 12, 'middle', '#334155', True)
    # lifeboats both sides
    for y in (150, 350):
        s += f'<ellipse cx="160" cy="{y}" rx="55" ry="14" fill="#f97316" stroke="#7c2d12" stroke-width="2"/>'
    s += txt(160, 128, 'เรือชูชีพปิดมิดชิด 100% (กราบซ้าย)', 11.5, 'middle', '#7c2d12', True)
    s += txt(160, 384, 'เรือชูชีพปิดมิดชิด 100% (กราบขวา)', 11.5, 'middle', '#7c2d12', True)
    # liferafts
    for x, y in ((280, 168), (280, 352), (900, 220)):
        s += f'<ellipse cx="{x}" cy="{y}" rx="18" ry="10" fill="#fde68a" stroke="#92400e" stroke-width="2"/>'
    s += txt(310, 128, 'แพชูชีพ (รวม 100% ย้ายข้างได้', 11.5, 'start', '#92400e', True) + txt(310, 143, 'หรือ 100% ทั้งสองข้าง)', 11.5, 'start', '#92400e', True)
    s += line(900, 208, 900, 150, '#92400e', 1.2)
    s += txt(900, 128, 'แพหัวเรือ (forward liferaft)', 11, 'middle', '#92400e', True) + txt(900, 143, 'ถ้า survival craft ห่างหัวเรือ > 100 m', 9.5, 'middle', '#92400e')
    # rescue boat
    s += f'<ellipse cx="320" cy="352" rx="28" ry="9" fill="#ef4444" stroke="#7f1d1d" stroke-width="2"/>' + txt(330, 384, 'Rescue boat', 11.5, 'start', '#7f1d1d', True)
    # lifebuoys
    for x, y in ((240, 165), (240, 355), (500, 165), (500, 355), (760, 165), (760, 355), (60, 175), (60, 345)):
        s += f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="#dc2626" stroke-width="4"/>'
    # EPIRB, SART on bridge wing
    s += rect(200, 196, 18, 18, '#22c55e', '#14532d', 1.5) + txt(209, 209, 'E', 10, 'middle', '#fff', True)
    s += rect(200, 300, 18, 18, '#3b82f6', '#1e3a8a', 1.5) + txt(209, 313, 'S', 10, 'middle', '#fff', True)
    s += txt(500, 260, 'ระวางสินค้า', 14, 'middle', '#94a3b8', True)
    rows = [('#f97316', 'Lifeboats — ปิดมิดชิด แต่ละกราบจุ 100% (หรือ free-fall ท้ายเรือ 100%)'),
            ('#fde68a', 'Liferafts — จุรวม 100% ย้ายข้างได้ง่าย (หรือ 100% แต่ละข้าง) + แพหัวเรือเมื่อ survival craft ห่างหัว/ท้ายเกิน 100 m'),
            ('#ef4444', 'Rescue boat อย่างน้อย 1 ลำ (เรือชูชีพอาจใช้แทนได้ถ้าเป็นไปตามข้อกำหนด)'),
            ('#22c55e', 'E = EPIRB 406 MHz แบบลอยปล่อยอิสระ (float-free) · S = SART/AIS-SART อย่างน้อย 1 ต่อกราบ (≥ 500 GT; SOLAS IV/7 ตั้งแต่ 2024)'),
            ('#fecaca', 'วงกลมแดง = ห่วงชูชีพ (lifebuoys) กระจายสองกราบ — บางลูกมีไฟ ควัน หรือเชือก (ตามจำนวนที่กำหนดตามความยาวเรือ)'),
            ('#ffffff', 'Immersion suit สำหรับทุกคน · lifejacket ทุกคน + สำรอง · VHF พกพา (≥ 3 เครื่อง) · line-throwing appliance · พลุ 12 นัดบนสะพาน')]
    for i, (c, t) in enumerate(rows):
        y = 414 + i * 25
        s += rect(40, y - 14, 18, 18, c, '#0f172a', 1) + txt(68, y, t, 12)
    save('lsa-cargo-ship-arrangement.svg', s)


def liferaft_hru():
    w, h = 1000, 520
    s = head(w, h, 'แพชูชีพแบบโยน (Throw-over liferaft): HRU, weak link และการปล่อยอัตโนมัติเมื่อเรือจม')
    # stowage panel
    s += txt(180, 66, 'ตำแหน่งเก็บบนแท่น (cradle)', 14, 'middle', bold=True)
    s += rect(80, 120, 200, 70, '#f8fafc', '#0f172a', 2, 30) + txt(180, 160, 'ถังแพชูชีพ (canister)', 12, 'middle', '#0f172a', True)
    s += rect(60, 190, 240, 14, '#94a3b8', '#0f172a', 1.5) + txt(180, 225, 'cradle บนดาดฟ้า', 11, 'middle', '#334155')
    s += line(180, 120, 180, 95, '#0f172a', 2) + line(180, 95, 310, 95, '#0f172a', 2)
    s += rect(310, 85, 50, 22, '#22c55e', '#14532d', 1.5) + txt(335, 100, 'HRU', 11, 'middle', '#fff', True)
    s += line(360, 96, 380, 96, '#0f172a', 2) + line(380, 96, 380, 190, '#0f172a', 2) + txt(386, 182, 'ยึดกับเรือ', 11, 'start')
    s += f'<path d="M 280 160 q 40 10 60 -20" fill="none" stroke="#c2410c" stroke-width="2.5"/>'
    s += f'<circle cx="345" cy="135" r="6" fill="none" stroke="#c2410c" stroke-width="2.5"/>' + txt(300, 122, 'weak link', 11, 'end', '#c2410c', True)
    s += line(351, 135, 380, 135, '#c2410c', 2)
    s += txt(180, 260, 'Painter (เชือกผูกแพ) ต่อกับ weak link ที่ยึดกับจุดแข็งแรงของเรือ', 11.5, 'middle', '#c2410c', True)
    s += txt(180, 278, '(หรือ weak link ที่ติดกับส่วนที่ยึดตายของ HRU ตามแบบ)', 11, 'middle', '#c2410c')
    s += txt(180, 296, 'ห้ามผูกกับสายรัด/ส่วนที่ถูกปลด และห้ามผูกตรงกับเรือโดยข้าม weak link', 11, 'middle', '#7f1d1d', True)
    # sinking sequence
    s += txt(700, 66, 'เมื่อเรือจม (float-free)', 14, 'middle', bold=True)
    s += f'<rect x="440" y="90" width="520" height="240" fill="#bae6fd" opacity="0.5"/>' + line(440, 90, 960, 90, '#0284c7', 2)
    steps = [(540, 235, '1. ที่ความลึกไม่เกิน 4 m', 'HRU ตัดสายยึด canister'),
             (650, 170, '2. canister ลอยขึ้น', 'painter ถูกดึงออกจนสุด'),
             (790, 100, '3. แรงดึง painter', 'เปิดวาล์วก๊าซ → แพพองตัว'),
             (900, 140, '4. แรงลอยตัวของแพ', 'ดึง weak link ขาด → แพเป็นอิสระ')]
    s += f'<path d="M 450 330 L 520 250 L 555 268 L 495 330 Z" fill="#475569" opacity="0.8"/>'
    s += f'<path d="M 540 235 Q 610 215 650 170 Q 720 120 790 100" fill="none" stroke="#c2410c" stroke-width="2" stroke-dasharray="5 4"/>'
    for k, (x, y, t1, t2) in enumerate(steps):
        s += f'<circle cx="{x}" cy="{y}" r="14" fill="#fde68a" stroke="#92400e" stroke-width="2"/>'
        if k == 0:
            s += txt(x + 22, y + 22, t1, 11, 'start', '#0f172a', True) + txt(x + 22, y + 37, t2, 10.5, 'start', '#334155')
        else:
            s += txt(x, y + 32, t1, 11, 'middle', '#0f172a', True) + txt(x, y + 47, t2, 10.5, 'middle', '#334155')
    s += rect(40, 360, 920, 145, '#f8fafc', '#94a3b8', 1, 10)
    L = ['การโยนแพด้วยมือ (ขณะเรือยังลอย): ตรวจ painter ยึดกับจุดแข็งแรงของเรือ → ตรวจด้านข้างเรือโล่ง (ไม่มีคน/สิ่งกีดขวาง) → ปลดสายรัด',
         '→ ยก/โยนลงน้ำ → ดึง painter ออกให้สุด (ยาวพอสำหรับระยะถึงน้ำเมื่อเรือเบาที่สุด) แล้วกระตุกแรง ๆ → แพพอง → ดึงเข้าข้างเรือ',
         '→ ลงแพทางบันได/ตาข่ายหรือลงน้ำแล้วขึ้นแพ (หลีกเลี่ยงการกระโดดใส่หลังคาแพ) → ตัด painter ด้วยมีด (อยู่ใกล้ทางเข้า) → พายออกห่างเรือ',
         'HRU: แบบใช้แล้วทิ้งมีอายุตามที่ผู้ผลิตกำหนด (ทั่วไป 2 ปี) — แบบบำรุงรักษาได้ต้องตรวจทุก 12 เดือน · แพต้องส่งสถานีบริการที่ได้รับอนุมัติ',
         'ทุก 12 เดือน (ขยายได้ถึง 17 เดือนตามเงื่อนไข) · ตรวจทุกสัปดาห์/เดือน: สายรัด HRU วันหมดอายุ ตำแหน่ง painter ป้ายวิธีใช้']
    for i, l in enumerate(L):
        s += txt(56, 384 + i * 25, l, 11.8)
    save('lsa-liferaft-hru.svg', s)


def davit():
    w, h = 1000, 520
    s = head(w, h, 'การปล่อยเรือชูชีพด้วย gravity davit (ลำดับทั่วไป — ปฏิบัติตามคู่มือของเรือ)')
    steps = ['ตรวจ: ปลั๊กท่อระบายน้ำ (drain plug) ปิด, painter ต่อไปข้างหน้า, ทางลงน้ำโล่ง, เรือหยุด/ช้ามาก',
             'ปลดตัวยึด: harbour pins/safety pins, gripes (สายรัด) — เรือพร้อมเคลื่อน',
             'ลดเรือถึงดาดฟ้าขึ้นเรือ (embarkation deck) ดึงเข้าข้าง (tricing/bowsing) ให้คนขึ้น',
             'คนขึ้นเรือ นั่ง คาดเข็มขัด สวม lifejacket — ปลดสาย bowsing/tricing',
             'ผู้ควบคุมในเรือดึงสาย remote control ยกเบรก → เรือลดลงด้วยน้ำหนักตัวเอง (ควบคุมความเร็ว)',
             'สตาร์ทเครื่องก่อนถึงน้ำ · เมื่อเรือลอยน้ำจริง (hydrostatic interlock) ปลด on-load release hooks',
             'ปลด painter เมื่อพร้อม · ขับออกห่างจากเรือ (ระวังใบจักรของเรือใหญ่และข้างเรือ)']
    for i, t in enumerate(steps):
        y = 70 + i * 52
        s += f'<circle cx="60" cy="{y+18}" r="16" fill="#f97316"/>' + txt(60, y + 24, str(i + 1), 14, 'middle', '#fff', True)
        s += rect(90, y, 520, 38, '#fff7ed', '#c2410c', 1.2, 8) + txt(102, y + 24, t, 11.6)
    # davit sketch
    x0 = 700
    s += line(x0, 420, x0, 120, '#0f172a', 5) + line(x0, 120, x0 + 120, 100, '#0f172a', 6)
    s += line(x0 + 120, 100, x0 + 120, 250, '#475569', 2) + line(x0 + 60, 112, x0 + 60, 250, '#475569', 2)
    s += f'<path d="M {x0+30} 250 L {x0+150} 250 Q {x0+165} 270 {x0+150} 290 L {x0+30} 290 Q {x0+15} 270 {x0+30} 250 Z" fill="#f97316" stroke="#7c2d12" stroke-width="2"/>'
    s += txt(x0 + 90, 276, 'Lifeboat', 12, 'middle', '#fff', True)
    s += txt(x0 + 125, 92, 'davit arm', 11, 'start', '#0f172a', True) + txt(x0 + 125, 200, 'falls', 11, 'start', '#334155')
    s += rect(x0 - 40, 360, 40, 30, '#94a3b8', '#0f172a', 1.5) + txt(x0 - 20, 405, 'winch', 10.5, 'middle')
    s += line(x0 - 20, 360, x0 + 60, 250, '#c2410c', 1.5, '4 3') + txt(x0 - 30, 330, 'สาย remote', 10.5, 'end', '#c2410c')
    s += txt(x0 - 30, 344, 'control (ยกเบรก)', 10.5, 'end', '#c2410c')
    s += line(640, 420, 980, 420, '#0284c7', 2) + txt(810, 440, 'ผิวน้ำ', 11, 'middle', '#0284c7')
    s += rect(40, 450, 920, 60, '#fef2f2', '#b91c1c', 1.5, 10)
    s += txt(56, 474, 'ความปลอดภัย: อุบัติเหตุเรือชูชีพในการฝึกเคยทำให้คนเสียชีวิตจาก hook ปลดก่อนเวลา/ประกอบผิด — ตรวจตัวชี้ hook reset ก่อนยกเรือขึ้นทุกครั้ง', 12, 'start', '#7f1d1d', True)
    s += txt(56, 494, 'คนในเรือขณะยกขึ้นให้น้อยที่สุด ปฏิบัติตาม MSC.1/Circ.1206/Rev.1 และการบำรุงรักษาตาม MSC.402(96) (ตรวจละเอียดรายปี, ทดสอบ 5 ปี โดยผู้ให้บริการที่ได้รับอนุญาต)', 12, 'start', '#7f1d1d')
    save('lsa-davit-launch.svg', s)


def sart():
    w, h = 1000, 470
    s = head(w, h, 'การแสดงผลของ SART บนจอเรดาร์ (X-band 9 GHz) และ AIS-SART')
    titles = ['ระยะไกล (> ~1 nm)', 'ใกล้เข้ามา (~1 nm)', 'ใกล้มาก']
    for k, t in enumerate(titles):
        cx, cy, r = 150 + k * 260, 230, 110
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0f172a" stroke="#334155" stroke-width="2"/>'
        s += f'<circle cx="{cx}" cy="{cy}" r="3" fill="#22c55e"/>'
        s += txt(cx, 98, t, 13, 'middle', '#0f172a', True)
        ang = math.radians(40)
        if k == 0:
            for i in range(12):
                d = 45 + i * 5
                x, y = cx + d * math.sin(ang), cy - d * math.cos(ang)
                s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#facc15"/>'
            s += txt(cx, cy + 135, 'เส้นจุด 12 จุด ห่างกันประมาณ 0.6 nm', 11, 'middle')
            s += txt(cx, cy + 151, 'SART อยู่ที่จุดแรก (ใกล้เรือที่สุด)', 11, 'middle', '#b91c1c', True)
        elif k == 1:
            for i in range(12):
                d = 18 + i * 7
                s += f'<path d="M {cx + d*math.sin(ang-0.35):.1f} {cy - d*math.cos(ang-0.35):.1f} A {d} {d} 0 0 1 {cx + d*math.sin(ang+0.35):.1f} {cy - d*math.cos(ang+0.35):.1f}" fill="none" stroke="#facc15" stroke-width="2.2"/>'
            s += txt(cx, cy + 135, 'จุดกลายเป็นส่วนโค้ง (arcs)', 11, 'middle')
            s += txt(cx, cy + 151, '(side lobes ของเรดาร์)', 11, 'middle')
        else:
            for i in range(10):
                s += f'<circle cx="{cx}" cy="{cy}" r="{12+i*9}" fill="none" stroke="#facc15" stroke-width="1.8"/>'
            s += txt(cx, cy + 135, 'กลายเป็นวงกลมซ้อน', 11, 'middle')
            s += txt(cx, cy + 151, '— SART อยู่ใกล้มาก', 11, 'middle')
    bx = 820
    s += rect(bx - 20, 120, 190, 230, '#f8fafc', '#94a3b8', 1, 10)
    s += txt(bx + 75, 146, 'AIS-SART', 14, 'middle', '#0f172a', True)
    s += f'<circle cx="{bx+75}" cy="200" r="22" fill="none" stroke="#b91c1c" stroke-width="3"/>' + line(bx + 59, 184, bx + 91, 216, '#b91c1c', 3) + line(bx + 91, 184, bx + 59, 216, '#b91c1c', 3)
    for i, t in enumerate(['สัญลักษณ์บน ECDIS/', 'เรดาร์/AIS display', 'MMSI ขึ้นต้น 970', 'ข้อความ "SART ACTIVE"', 'ส่งตำแหน่ง GNSS']):
        s += txt(bx + 75, 250 + i * 18, t, 11, 'middle')
    s += txt(500, 440, 'ติดตั้ง SART ให้สูงจากน้ำอย่างน้อย 1 m (เสาในเรือชูชีพ/แพ) — ระยะตรวจพบจากเรือ (เสาอากาศสูง ~15 m) ประมาณ 5 nm, จากอากาศยานไกลกว่ามาก', 12, 'middle', '#334155')
    save('lsa-sart-display.svg', s)


def epirb():
    w, h = 1000, 590
    s = head(w, h, 'ระบบ COSPAS-SARSAT และ EPIRB 406 MHz')
    nodes = [(110, 370, 'EPIRB', '406 MHz + 121.5 MHz homing', '#22c55e'), (330, 120, 'ดาวเทียม', 'LEO · MEO (MEOSAR) · GEO', '#1d4ed8'),
             (560, 370, 'LUT', 'สถานีภาคพื้นรับสัญญาณ', '#7c3aed'), (760, 370, 'MCC', 'ศูนย์ควบคุมภารกิจ', '#7c3aed'),
             (880, 200, 'RCC/MRCC', 'ประสานการค้นหาช่วยเหลือ', '#b91c1c')]
    for x, y, t, d, col in nodes:
        s += rect(x - 85, y - 32, 170, 64, '#fff', col, 2.5, 12) + txt(x, y - 6, t, 14, 'middle', col, True) + txt(x, y + 16, d, 10.5, 'middle')
    s += line(150, 336, 290, 156, '#0f172a', 2, mk='ar') + line(370, 156, 530, 336, '#0f172a', 2, mk='ar')
    s += line(645, 370, 672, 370, '#0f172a', 2, mk='ar') + line(820, 338, 860, 236, '#0f172a', 2, mk='ar')
    s += f'<path d="M 720 338 Q 640 200 420 128" fill="none" stroke="#15803d" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#ar)"/>'
    s += f'<path d="M 250 156 Q 150 210 100 336" fill="none" stroke="#15803d" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#ar)"/>'
    s += txt(640, 70, 'Return Link Service (RLS ผ่าน Galileo): MCC → ดาวเทียม → beacon', 11, 'middle', '#15803d', True)
    s += txt(640, 86, 'แจ้งผู้ประสบภัยว่าระบบได้รับสัญญาณแล้ว (เฉพาะรุ่นที่รองรับ RLS)', 10.5, 'middle', '#15803d')
    s += txt(140, 250, 'RLS', 10.5, 'end', '#15803d', True)
    L = ['ลอยปล่อยอิสระ (float-free) ด้วย HRU เมื่อจมประมาณ 1.5–4 m และเปิดทำงานเองเมื่อสัมผัสน้ำ · หรือเปิดด้วยมือ',
         'ข้อมูลที่ส่ง: รหัสประจำเครื่อง (15 hex ID; beacon รุ่นที่สอง SGB ใช้ 23 hex) ที่ลงทะเบียนกับเรือ + ตำแหน่ง GNSS',
         'EPIRB ที่ติดตั้งตั้งแต่ 1 ก.ค. 2022 ต้องมีเครื่องรับ GNSS ในตัวและส่ง AIS locating signal (MSC.471(101))',
         'ทดสอบตัวเอง (self-test) ทุกเดือน · ตรวจวันหมดอายุแบตเตอรี่/HRU · ทดสอบประจำปี · บำรุงรักษาที่ฝั่งไม่เกินทุก 5 ปี',
         'ถ้าเปิดโดยไม่ตั้งใจ → อย่าปิดเงียบ ๆ: แจ้ง RCC/MRCC ที่ใกล้ที่สุดเพื่อยกเลิกการแจ้งเหตุ']
    L.append('MEOSAR (ดาวเทียมวงโคจรระดับกลาง) ทำให้ตรวจจับและหาตำแหน่งได้เร็วกว่าระบบ LEO/GEO เดิมมาก')
    s += rect(40, 425, 920, 150, '#f0fdf4', '#15803d', 1, 10)
    for i, l in enumerate(L):
        s += txt(56, 448 + i * 23, '• ' + l, 11.8, 'start', '#14532d')
    save('lsa-epirb.svg', s)


def liferaft_actions():
    w, h = 1000, 520
    s = head(w, h, 'การกระทำทันทีเมื่อขึ้นแพชูชีพ และหลักการรอดชีวิต')
    imm = ['ตัด painter (มีดอยู่ใกล้ทางเข้า) พายออกห่างเรือที่จม', 'มองหาและช่วยผู้รอดชีวิตอื่น ขว้างห่วงช่วยชีวิต (rescue quoit)',
           'ปล่อย sea anchor (drogue) ลดการลอยและการพลิก', 'ปิดทางเข้า (อากาศเย็น) ระบายน้ำ (bail) เป่าพื้นแพ (insulated floor)',
           'เปิด SART ติดตั้งให้สูง · EPIRB (ถ้านำมา) · VHF พกพา', 'แจกยาแก้เมาคลื่นทันที (ก่อนเมา) · ปฐมพยาบาล',
           'ตรวจแพ: รั่ว แรงดันลม (เติมด้วยที่สูบ) · ผูกแพหลายลำเข้าด้วยกัน', 'แบ่งหน้าที่ ผู้เฝ้าระวัง (lookout) หมุนเวียน · บันทึก']
    s += txt(250, 66, 'การกระทำทันที (Immediate actions)', 15, 'middle', '#b91c1c', True)
    for i, t in enumerate(imm):
        y = 82 + i * 46
        s += f'<circle cx="52" cy="{y+18}" r="14" fill="#b91c1c"/>' + txt(52, y + 23, str(i + 1), 12, 'middle', '#fff', True)
        s += rect(74, y, 410, 36, '#fef2f2', '#fecaca', 1, 8) + txt(86, y + 23, t, 11.6)
    s += txt(745, 66, 'ลำดับความสำคัญในการรอดชีวิต', 15, 'middle', '#1d4ed8', True)
    pr = [('1. Protection (ป้องกันตัว)', 'จากความเย็น/ร้อน ลม ฝน — ชุด immersion suit, TPA,|ใส่เสื้อผ้าแห้ง อยู่รวมกัน ปิดหลังคา'),
          ('2. Location (ให้ถูกพบ)', 'EPIRB, SART, VHF, พลุ (ใช้เมื่อเห็นเรือ/เครื่องบิน),|กระจกสะท้อนแสง ไฟฉาย นกหวีด'),
          ('3. Water (น้ำ)', 'งดดื่มน้ำ 24 ชม.แรก (ยกเว้นผู้บาดเจ็บ) แล้วแบ่ง|ประมาณ 0.5 ลิตร/คน/วัน · ห้ามดื่มน้ำทะเล/ปัสสาวะ · เก็บน้ำฝน'),
          ('4. Food (อาหาร)', 'สำคัญน้อยกว่าน้ำ — กินเมื่อมีน้ำพอ|(อาหารใช้น้ำในการย่อย)')]
    for i, (t, d) in enumerate(pr):
        y = 82 + i * 90
        s += rect(510, y, 460, 78, '#eff6ff', '#1d4ed8', 1.5, 10)
        s += txt(526, y + 24, t, 13.5, 'start', '#1e3a8a', True)
        for j, part in enumerate(d.split('|')):
            s += txt(526, y + 46 + j * 17, part, 11.3)
    s += rect(510, 450, 460, 60, '#fff7ed', '#c2410c', 1.5, 10)
    s += txt(526, 474, 'ขวัญกำลังใจ (morale) และความเป็นผู้นำ: กำหนดกิจวัตร แบ่งงาน', 12, 'start', '#7c2d12', True)
    s += txt(526, 494, 'รักษาความหวัง — คนที่ยอมแพ้มีโอกาสรอดน้อยลงมาก', 12, 'start', '#7c2d12')
    save('lsa-liferaft-actions.svg', s)


def drills():
    w, h = 1000, 500
    s = head(w, h, 'การฝึกสละเรือและการตรวจอุปกรณ์ช่วยชีวิต (SOLAS III/19–20) — สรุปความถี่')
    rows = [('ทุกสัปดาห์', ['ตรวจด้วยตา: survival craft, rescue boats, อุปกรณ์ปล่อย — รวมสภาพ hook และ on-load release ที่ reset ครบ', 'เดินเครื่องเรือชูชีพ/เรือกู้ภัยรวมอย่างน้อย 3 นาที (ตรวจการเข้าเกียร์เดินหน้า-ถอยหลัง)', 'ทดสอบ general emergency alarm · เรือสินค้า: เลื่อนเรือชูชีพ (ไม่ใช่ free-fall) ออกจากที่เก็บเท่าที่จำเป็น · บันทึก log'], '#15803d'),
            ('ทุกเดือน', ['Abandon ship drill และ fire drill — ลูกเรือทุกคนอย่างน้อยเดือนละครั้ง', 'ตรวจอุปกรณ์ช่วยชีวิตทั้งหมดตาม checklist (อุปกรณ์ในเรือครบ ใช้ได้) บันทึก log', 'Turn out เรือชูชีพ (ไม่ใช่ free-fall) จากที่เก็บโดยไม่มีคน · EPIRB self-test · ปล่อยเรือกู้ภัยเท่าที่ทำได้'], '#1d4ed8'),
            ('ทุก 3 เดือน', ['ปล่อยเรือชูชีพ (davit) ลงน้ำพร้อมลูกเรือประจำเรือและบังคับในน้ำ', 'Free-fall: ลูกเรือขึ้นนั่งคาดเข็มขัด เริ่มขั้นตอนถึงก่อนปล่อยจริง แล้วปล่อย/ลดด้วยวิธีรอง', 'เรือกู้ภัย: ปล่อยและบังคับในน้ำอย่างน้อยทุก 3 เดือน'], '#7c3aed'),
            ('6 เดือน – 5 ปี', ['Free-fall: ปล่อยจริง (เฉพาะลูกเรือประจำ) หรือ simulated launching ไม่เกินทุก 6 เดือน', 'แพชูชีพ/HRU บำรุง: ทุก 12 เดือน (แพ ขยายได้ถึง 17 เดือน) · ตรวจละเอียดรายปีตาม MSC.402(96) · ทดสอบ EPIRB รายปี', 'Falls: กลับปลาย ≤ 30 เดือน เปลี่ยนเมื่อเสื่อมหรือ ≤ 5 ปี · ทดสอบ 5 ปีของอุปกรณ์ปล่อย'], '#b91c1c')]
    for i, (t, items, col) in enumerate(rows):
        y = 60 + i * 105
        s += rect(30, y, 160, 92, col, col, 0, 12) + txt(110, y + 52, t, 15, 'middle', '#fff', True)
        s += rect(200, y, 770, 92, '#f8fafc', col, 1.5, 12)
        for j, it in enumerate(items):
            s += txt(216, y + 26 + j * 26, '• ' + it, 12)
    s += txt(500, 488, 'ถ้าลูกเรือเกิน 25% ไม่ได้ร่วมฝึกในเดือนก่อน: ฝึกภายใน 24 ชม. หลังออกเรือ · ลูกเรือใหม่ต้องได้รับการฝึกใช้อุปกรณ์ภายในเวลาที่กำหนด — ตรวจตามฉบับแก้ไขล่าสุดของ SOLAS/Flag', 11.5, 'middle', '#334155')
    save('lsa-drills-inspections.svg', s)


def suits():
    w, h = 1000, 470
    s = head(w, h, 'Lifejacket · Immersion suit · Thermal protective aid (TPA) — ต่างกันอย่างไร')
    cols = [('Lifejacket', '#f97316', ['ลอยตัว พลิกคนหมดสติให้หน้าหงาย', 'ไฟ (light) นกหวีด แถบสะท้อนแสง', 'สวมได้ถูกต้องภายใน 1 นาที', 'กระโดดจากสูง ≥ 4.5 m ได้ไม่บาดเจ็บ', 'ทุกคน + สำรองที่สถานีเฝ้ายาม']),
            ('Immersion suit', '#dc2626', ['ป้องกันความเย็นในน้ำ ลดการเสียความร้อน', 'สวมได้เองภายใน 2 นาที', 'แบบมีฉนวน: อุณหภูมิแกนกลางลดไม่เกิน 2°C', 'หลัง 6 ชม. ในน้ำ 0–2°C (ตามมาตรฐาน)', 'เรือสินค้า: มีให้ทุกคน (SOLAS III/32)']),
            ('Thermal protective aid', '#ca8a04', ['ถุง/ชุดวัสดุนำความร้อนต่ำ ใช้ในเรือ/แพ', 'ลดการเสียความร้อนของผู้รอดชีวิต', 'ใช้กับคนที่เปียก/ตัวเย็น', 'ถอดออกได้ภายใน 2 นาทีถ้าขัดการว่ายน้ำ', 'มีในเรือชูชีพ 10% ของความจุ หรืออย่างน้อย 2'])]
    for i, (t, col, items) in enumerate(cols):
        x = 40 + i * 315
        s += rect(x, 60, 295, 380, '#fff', col, 2.5, 14)
        s += rect(x, 60, 295, 46, col, col, 0, 14) + rect(x, 90, 295, 16, col, col, 0)
        s += txt(x + 147, 90, t, 16, 'middle', '#fff', True)
        # icon
        cx = x + 147
        if i == 0:
            s += f'<path d="M {cx-40} 130 L {cx-15} 130 L {cx-10} 200 L {cx-45} 200 Z" fill="{col}"/><path d="M {cx+40} 130 L {cx+15} 130 L {cx+10} 200 L {cx+45} 200 Z" fill="{col}"/>'
            s += f'<circle cx="{cx-28}" cy="145" r="4" fill="#facc15"/>'
        elif i == 1:
            s += f'<circle cx="{cx}" cy="128" r="16" fill="{col}"/>' + rect(cx - 30, 145, 60, 70, col, col, 0, 10) + rect(cx - 30, 210, 24, 30, col, col, 0, 6) + rect(cx + 6, 210, 24, 30, col, col, 0, 6)
        else:
            s += f'<path d="M {cx-40} 130 Q {cx} 115 {cx+40} 130 L {cx+45} 230 L {cx-45} 230 Z" fill="#fde68a" stroke="{col}" stroke-width="2"/>'
        for j, it in enumerate(items):
            s += txt(x + 18, 270 + j * 30, '• ' + it, 12)
    s += txt(500, 460, 'Immersion suit แบบไม่มีฉนวนต้องสวมทับเสื้อผ้าอุ่น — ตรวจซิป ขนาด ทดสอบแรงดันอากาศ ≤ 3 ปี (ถี่ขึ้นเมื่ออายุ > 10 ปี — MSC/Circ.1114)', 11.5, 'middle', '#334155')
    save('lsa-suits-tpa.svg', s)


if __name__ == '__main__':
    arrangement(); liferaft_hru(); davit(); sart(); epirb(); liferaft_actions(); drills(); suits()
