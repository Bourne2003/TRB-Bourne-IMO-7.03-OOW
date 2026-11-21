"""ภาพประกอบบท 2.2 การตรวจและรายงานความเสียหายของระวางสินค้า ฝาระวาง และถังอับเฉา"""
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


def badge(x, y, n, col='#b91c1c'):
    return f'<circle cx="{x}" cy="{y}" r="11" fill="{col}"/>' + txt(x, y + 4.5, str(n), 12, 'middle', '#fff', True)


# ---------------------------------------------------------------- bulk carrier midship section
def bulk_section():
    w, h = 1000, 640
    s = head(w, h, 'ภาคตัดกลางลำเรือ Bulk carrier (single side skin): โครงสร้างสำคัญและจุดที่มักพบความเสียหาย')
    cx = 330
    # outer hull
    s += f'<path d="M {cx-250} 120 L {cx+250} 120 L {cx+250} 520 Q {cx+250} 560 {cx+210} 560 L {cx-210} 560 Q {cx-250} 560 {cx-250} 520 Z" fill="#f8fafc" stroke="#0f172a" stroke-width="3"/>'
    # double bottom
    s += f'<path d="M {cx-250} 500 L {cx+250} 500" stroke="#0f172a" stroke-width="2.5"/>'
    s += f'<rect x="{cx-249}" y="501" width="498" height="58" fill="#bfdbfe" opacity="0.6"/>'
    for k in range(-4, 5):
        s += line(cx + k * 55, 500, cx + k * 55, 558, '#475569', 1.2)
    s += txt(cx, 540, 'Double bottom tank (ballast/น้ำมัน)', 12, 'middle', '#1e3a8a', True)
    # hopper tanks
    for sg in (-1, 1):
        x0 = cx + sg * 250
        s += f'<path d="M {x0} 400 L {cx+sg*130} 500 L {x0} 500 Z" fill="#bfdbfe" stroke="#0f172a" stroke-width="2.5" opacity="0.9"/>'
        s += f'<path d="M {x0} 120 L {cx+sg*140} 120 L {cx+sg*140} 165 L {x0} 230 Z" fill="#bfdbfe" stroke="#0f172a" stroke-width="2.5" opacity="0.9"/>'
        # side shell frames
        for k in range(5):
            y = 245 + k * 30
            s += line(x0, y, x0 - sg * 18, y, '#b45309', 3)
    s += txt(cx - 195, 175, 'Topside tank', 11.5, 'middle', '#1e3a8a', True)
    s += txt(cx - 210, 480, 'Hopper', 11.5, 'middle', '#1e3a8a', True)
    s += txt(cx - 210, 494, 'tank', 11.5, 'middle', '#1e3a8a', True)
    # hatch coaming & cover
    s += rect(cx - 150, 92, 300, 28, '#94a3b8', '#0f172a', 2)
    s += rect(cx - 160, 78, 320, 16, '#64748b', '#0f172a', 2)
    s += txt(cx, 72, 'ฝาระวาง (hatch cover) บน hatch coaming', 12, 'middle', '#0f172a', True)
    # cargo
    s += f'<path d="M {cx-130} 500 L {cx-200} 400 L {cx-160} 330 Q {cx} 270 {cx+160} 330 L {cx+200} 400 L {cx+130} 500 Z" fill="#fde68a" opacity="0.5"/>'
    s += txt(cx, 420, 'ระวางสินค้า (cargo hold)', 14, 'middle', '#78350f', True)
    # markers
    marks = [(1, cx - 230, 300), (2, cx - 160, 470), (3, cx + 40, 505), (4, cx + 150, 110), (5, cx + 210, 142),
             (6, cx - 168, 122), (7, cx + 240, 260), (8, cx + 120, 545), (9, cx + 142, 486)]
    for n, x, y in marks:
        s += badge(x, y, n)
    items = ['Side shell frames และ end brackets — grab/รถตักชน, กัดกร่อนที่ปลายล่าง (necking), แยกจากเปลือกเรือ',
             'แผ่น hopper ด้านลาด — grab กระแทก บุบ, กัดกร่อนจากกากสินค้า',
             'Tank top (inner bottom) — grab/ค้อนทุบ บุบ, น้ำหนักเกิน (local strength)',
             'Hatch coaming มุมช่องระวาง (hatch corners) — รอยร้าวจากความเค้นสูง, เครน/grab ชน',
             'ใต้ดาดฟ้าใน topside tank — แดดร้อน กัดกร่อนเร็ว coating เสื่อม',
             'Cross deck/ดาดฟ้าระหว่างช่องระวาง และฝาระวาง — คลื่นซัด เสียรูป ซีลรั่ว',
             'เปลือกเรือด้านข้าง (side shell) — ถูกเรือลากจูง/ท่าชน, กัดกร่อนบริเวณ splash zone',
             'แผ่นท้องเรือ/โครงภายใน double bottom — pitting ใต้ตะกอน, slamming ที่หัวเรือ',
             'รอยต่อ hopper กับ inner bottom และ bulkhead stools — จุดรวมความเค้น รอยร้าว']
    bx = 620
    s += rect(bx, 60, 365, 560, '#fff7ed', '#c2410c', 1.5, 10)
    s += txt(bx + 14, 84, 'จุดที่ต้องตรวจเป็นพิเศษ (ตัวอย่าง)', 14, 'start', '#7c2d12', True)
    y = 112
    for i, it in enumerate(items):
        s += badge(bx + 24, y - 4, i + 1)
        words = it
        # wrap ~34 chars
        chunks, cur = [], ''
        for part in words.split(' '):
            if len(cur) + len(part) > 34:
                chunks.append(cur); cur = part
            else:
                cur = (cur + ' ' + part).strip()
        chunks.append(cur)
        for j, c in enumerate(chunks):
            s += txt(bx + 44, y + j * 17, c, 11.5)
        y += 17 * len(chunks) + 10
    save('insp-bulk-midship-section.svg', s)


# ---------------------------------------------------------------- hatch cover sealing
def hatch_cover():
    w, h = 1000, 560
    s = head(w, h, 'ฝาระวาง (Hatch cover): ส่วนประกอบระบบผนึกกันน้ำ และข้อบกพร่องที่พบบ่อย')
    # coaming
    x0, y0 = 120, 200
    s += rect(x0, y0 + 60, 26, 220, '#94a3b8', '#0f172a', 2)  # coaming plate
    s += rect(x0 - 10, y0 + 50, 70, 14, '#64748b', '#0f172a', 2)  # coaming top bar
    s += txt(x0 - 4, y0 + 300, 'Hatch coaming', 12, 'start', '#0f172a', True)
    # compression bar
    s += rect(x0 + 18, y0 + 30, 10, 20, '#475569', '#0f172a', 1.5)
    # panel
    s += f'<path d="M {x0-30} {y0-20} L {x0+420} {y0-20} L {x0+420} {y0+30} L {x0-30} {y0+30} Z" fill="#cbd5e1" stroke="#0f172a" stroke-width="2"/>'
    s += txt(x0 + 200, y0 + 10, 'แผ่นฝาระวาง (hatch cover panel)', 13, 'middle', '#0f172a', True)
    # rubber packing in channel
    s += rect(x0 + 6, y0 + 30, 34, 14, '#111827', '#0f172a', 1)
    s += f'<rect x="{x0+12}" y="{y0+38}" width="22" height="10" rx="3" fill="#1f2937"/>'
    # cleat
    s += f'<path d="M {x0-30} {y0+60} L {x0-6} {y0+60} L {x0-6} {y0+30} " fill="none" stroke="#b45309" stroke-width="5"/>'
    # drain channel
    s += f'<path d="M {x0+60} {y0+50} L {x0+60} {y0+70} L {x0+110} {y0+70} L {x0+110} {y0+50}" fill="none" stroke="#0369a1" stroke-width="3"/>'
    s += line(x0 + 85, y0 + 70, x0 + 85, y0 + 120, '#0369a1', 3)
    s += f'<circle cx="{x0+85}" cy="{y0+128}" r="7" fill="#e0f2fe" stroke="#0369a1" stroke-width="2"/>'
    # steel to steel pad
    s += rect(x0 + 160, y0 + 30, 30, 20, '#f59e0b', '#92400e', 1.5)
    s += rect(x0 + 160, y0 + 50, 30, 14, '#64748b', '#0f172a', 1.5)
    labels = [(1, x0 + 50, y0 + 36, 'ยางผนึก (packing/gasket) ในราง'), (2, x0 + 44, y0 + 64, 'Compression bar บนขอบ coaming'),
              (3, x0 - 30, y0 + 75, 'Cleat/ตัวล็อก (quick-acting cleat)'), (4, x0 + 85, y0 + 145, 'รางระบายน้ำ + non-return valve'),
              (5, x0 + 175, y0 + 75, 'Bearing pad (steel-to-steel contact)')]
    for n, x, y, t in labels:
        s += f'<circle cx="{x}" cy="{y}" r="10" fill="#b91c1c" opacity="0.9"/>' + txt(x, y + 4, str(n), 11, 'middle', '#fff', True)
    for i, (n, x, y, t) in enumerate(labels):
        s += f'<circle cx="{x0+260}" cy="{y0+92+i*28}" r="10" fill="#b91c1c"/>' + txt(x0 + 260, y0 + 96 + i * 28, str(n), 11, 'middle', '#fff', True)
        s += txt(x0 + 278, y0 + 96 + i * 28, t, 12.5)
    s += txt(x0 + 100, y0 - 50, 'ภาพตัดขอบฝาระวางกับขอบ coaming (แนวคิด)', 13, 'middle', '#334155', True)
    # defects box
    bx = 640
    s += rect(bx, 60, 345, 470, '#fef2f2', '#b91c1c', 1.5, 10)
    D = ['ข้อบกพร่องที่พบบ่อย', '• ยางแข็ง แตก ขาด หลุดจากราง', '  หรือมีรอยกดถาวร (permanent set)', '  ลึกเกินเกณฑ์ผู้ผลิต',
         '• Compression bar คด บิ่น เป็นสนิม', '• Cleat หลวม หาย ยางรอง (washer)', '  เสื่อม ปรับระยะไม่ถูก',
         '• รางระบายน้ำตัน non-return valve', '  ติด/หาย → น้ำล้นเข้าระวาง', '• Bearing pad สึก → ยางรับแรงเกิน',
         '• ขอบ coaming/ฝาเป็นสนิม รอยร้าวที่มุม', '• แผ่นฝาบุบ/เสียรูปจากเครน หรือคลื่น', '• ล้อ ราง โซ่ ไฮดรอลิก รั่ว/เสียหาย',
         '', 'การทดสอบความผนึกน้ำ', '• Hose test (ฉีดน้ำตามแนวรอยต่อ)', '• Ultrasonic test (ทำได้แม้มีสินค้า)', '• Chalk test (ดูรอยสัมผัสยาง)',
         '• Light test (ดูแสงลอดจากในระวาง)']
    for i, d in enumerate(D):
        s += txt(bx + 14, 86 + i * 22.5, d, 12.3, 'start', '#7f1d1d' if i in (0, 14) else '#0f172a', i in (0, 14))
    save('insp-hatch-cover.svg', s)


# ---------------------------------------------------------------- corrosion
def corrosion():
    w, h = 1000, 600
    s = head(w, h, 'การกัดกร่อน (Corrosion): กลไก ชนิด และการป้องกัน')
    # electrochemical cell
    s += txt(250, 66, 'กลไกไฟฟ้าเคมี (electrochemical cell)', 14, 'middle', bold=True)
    s += rect(60, 90, 380, 150, '#e0f2fe', '#0369a1', 1.5)
    s += txt(250, 112, 'อิเล็กโทรไลต์ (น้ำทะเล/ความชื้น/ตะกอน)', 12, 'middle', '#075985', True)
    s += rect(80, 180, 140, 40, '#94a3b8', '#0f172a', 1.5) + txt(150, 205, 'Anode (ผุกร่อน)', 12, 'middle', '#7f1d1d', True)
    s += rect(280, 180, 140, 40, '#cbd5e1', '#0f172a', 1.5) + txt(350, 205, 'Cathode', 12, 'middle', '#0f172a', True)
    s += f'<path d="M 150 180 Q 250 130 350 180" fill="none" stroke="#b91c1c" stroke-width="2" marker-end="url(#arR)"/>'
    s += txt(250, 146, 'อิออนโลหะละลายจาก anode', 11, 'middle', '#b91c1c')
    s += line(150, 230, 350, 230, '#0f172a', 2, mk='ar') + txt(250, 250, 'อิเล็กตรอนไหลในเนื้อโลหะ', 11, 'middle')
    s += txt(250, 275, 'ต้องมีครบ 4 อย่าง: anode, cathode, อิเล็กโทรไลต์, ทางไฟฟ้า', 12, 'middle', '#0f172a', True)
    s += txt(250, 293, 'ตัดได้ข้อใดข้อหนึ่ง (coating, anode เสียสละ, ทำให้แห้ง) = หยุดการกัดกร่อน', 11.5, 'middle', '#15803d')
    # types
    s += txt(735, 66, 'ชนิดของการกัดกร่อนที่พบในเรือ', 14, 'middle', bold=True)
    types = [('General (uniform)', 'บางลงทั่วทั้งแผ่น สนิมเกล็ด (scale)', 'g'),
             ('Pitting', 'หลุมเฉพาะจุด ลึก — พื้นถัง/ท้องระวางใต้ตะกอน', 'p'),
             ('Grooving', 'ร่องตามแนวเชื่อม/ขอบ — ร้ายเพราะเฉพาะจุด', 'r'),
             ('Galvanic', 'โลหะต่างชนิดสัมผัสกันในน้ำทะเล', 'v'),
             ('Erosion-corrosion / MIC', 'การไหลแรง (ท่อ ปากดูด) / แบคทีเรีย (SRB)', 'm')]
    for i, (t, d, k) in enumerate(types):
        y = 92 + i * 52
        s += rect(560, y, 90, 36, '#e2e8f0', '#475569', 1)
        if k == 'g':
            s += rect(560, y + 22, 90, 14, '#b45309', '#b45309', 0)
        elif k == 'p':
            for j in range(4):
                s += f'<path d="M {572+j*20} {y} q 5 14 10 0" fill="#b45309"/>'
        elif k == 'r':
            s += f'<path d="M 560 {y} L 650 {y} L 650 {y+4} L 610 {y+4} L 606 {y+16} L 602 {y+4} L 560 {y+4} Z" fill="#b45309"/>'
            s += line(606, y + 4, 606, y + 36, '#0f172a', 1, '2 2')
        elif k == 'v':
            s += rect(560, y, 45, 36, '#fcd34d', '#475569', 1) + txt(582, y + 22, 'Cu', 11, 'middle', '#78350f', True) + txt(628, y + 22, 'Fe', 11, 'middle', '#0f172a', True)
        else:
            for j in range(5):
                s += f'<circle cx="{570+j*18}" cy="{y+28}" r="5" fill="#b45309"/>'
        s += txt(660, y + 14, t, 12.5, 'start', '#0f172a', True) + txt(660, y + 31, d, 11.5, 'start', '#334155')
    # causes & prevention
    s += rect(40, 340, 450, 240, '#fff7ed', '#c2410c', 1.5, 10)
    C = ['สาเหตุ/ปัจจัยเร่งในระวางและถังอับเฉา', '• น้ำทะเลและความชื้น วงจรเปียก-แห้ง', '• Coating เสื่อม/เสียหาย (grab, การเชื่อม, ขอบคม)',
         '• อุณหภูมิสูง (ใต้ดาดฟ้าที่ถูกแดด, ข้างถังน้ำมันอุ่น)', '• ตะกอนค้างในถัง (ใต้ตะกอนเกิด pitting)', '• กากสินค้ากัดกร่อน (ถ่านหิน กำมะถัน เกลือ ปุ๋ย)',
         '• Anode หมด/ไม่จมน้ำ (anode ทำงานเมื่อจมเท่านั้น)', '• ความเค้นและการสั่น (stress corrosion/fatigue)', '• แบคทีเรียลดซัลเฟต (SRB) ในน้ำนิ่ง']
    for i, c in enumerate(C):
        s += txt(56, 366 + i * 24, c, 12.3, 'start', '#7c2d12' if i == 0 else '#0f172a', i == 0)
    s += rect(510, 340, 450, 240, '#f0fdf4', '#15803d', 1.5, 10)
    P = ['การป้องกันและควบคุม', '• Coating ที่ดี (ถังอับเฉาเรือใหม่ตาม PSPC — SOLAS II-1/3-2)', '• ซ่อม coating จุดเสียหายเร็ว (touch-up) ตาม MSC.1/Circ.1330',
         '• Sacrificial anodes (สังกะสี/อะลูมิเนียม) และ impressed current', '• ล้างตะกอน ล้างกากสินค้ากัดกร่อนด้วยน้ำ (และน้ำจืดถ้าทำได้)', '• ป้องกันความเสียหายทางกลระหว่างขนถ่าย',
         '• ตรวจตามแผน วัดความหนา (UTM) เทียบค่าที่ยอมให้', '• ระบายอากาศ/ทำให้แห้ง (ระวาง void)', '• บันทึกและติดตามแนวโน้ม (trend)']
    for i, p in enumerate(P):
        s += txt(526, 366 + i * 24, p, 12.3, 'start', '#14532d' if i == 0 else '#0f172a', i == 0)
    save('insp-corrosion.svg', s)


# ---------------------------------------------------------------- ballast tank hotspots
def ballast_hotspots():
    w, h = 1000, 600
    s = head(w, h, 'ถังอับเฉา (Ballast tank) ตัวอย่างโครงสร้างภายในและจุดที่ต้องตรวจ')
    x0, y0, W, H = 60, 70, 560, 470
    s += rect(x0, y0, W, H, '#eff6ff', '#0f172a', 3)
    # web frame with lightening holes
    s += rect(x0 + 200, y0, 40, H, '#cbd5e1', '#475569', 1.5)
    for yy in (150, 300, 430):
        s += f'<ellipse cx="{x0+220}" cy="{y0+yy}" rx="12" ry="30" fill="#eff6ff" stroke="#475569"/>'
    # longitudinals
    for k in range(9):
        y = y0 + 30 + k * 50
        s += line(x0, y, x0 + W, y, '#64748b', 4)
    # brackets
    for (bx, by, sx) in ((x0 + 200, y0 + 30, -1), (x0 + 240, y0 + 30, 1), (x0 + 200, y0 + H - 20, -1), (x0 + 240, y0 + H - 20, 1)):
        s += f'<path d="M {bx} {by} L {bx+sx*50} {by} L {bx} {by+ (40 if by < y0+100 else -40)} Z" fill="#cbd5e1" stroke="#475569" stroke-width="1.5"/>'
    # sediment
    s += f'<path d="M {x0+3} {y0+H-3} L {x0+W-3} {y0+H-3} L {x0+W-3} {y0+H-30} Q {x0+W/2} {y0+H-10} {x0+3} {y0+H-35} Z" fill="#a16207" opacity="0.55"/>'
    # anode
    for ax in (x0 + 110, x0 + 380):
        s += rect(ax, y0 + 395, 50, 12, '#d1d5db', '#374151', 1.5)
    # bellmouth
    s += f'<path d="M {x0+470} {y0+380} L {x0+470} {y0+430} L {x0+455} {y0+450} L {x0+505} {y0+450} L {x0+490} {y0+430} L {x0+490} {y0+380}" fill="#94a3b8" stroke="#0f172a" stroke-width="1.5"/>'
    # ladder & manhole
    s += rect(x0 + 300, y0 + 4, 60, 34, '#fff', '#0f172a', 2, 14)
    for k in range(8):
        s += line(x0 + 315, y0 + 50 + k * 22, x0 + 345, y0 + 50 + k * 22, '#334155', 2)
    s += line(x0 + 315, y0 + 40, x0 + 315, y0 + 230, '#334155', 2) + line(x0 + 345, y0 + 40, x0 + 345, y0 + 230, '#334155', 2)
    marks = [(1, x0 + 165, y0 + 52), (2, x0 + 275, y0 + 52), (3, x0 + 80, y0 + 18), (4, x0 + 260, y0 + H - 30), (5, x0 + 135, y0 + 388),
             (6, x0 + 480, y0 + 460), (7, x0 + 330, y0 + 22), (8, x0 + 330, y0 + 150), (9, x0 + 220, y0 + 215)]
    for n, x, y in marks:
        s += badge(x, y, n)
    bx = 640
    s += rect(bx, 70, 345, 470, '#fff7ed', '#c2410c', 1.5, 10)
    items = ['ปลายแขน bracket (bracket toes) — รอยร้าวล้า (fatigue)', 'รอยต่อ longitudinal กับ web frame — รอยร้าว, coating แตกตามแนวเชื่อม',
             'ใต้ดาดฟ้า (under-deck) — ร้อน กัดกร่อนเร็วที่สุด', 'พื้นถังใต้ตะกอน — pitting', 'Sacrificial anode — สึกไปกี่ % ยึดแน่นหรือไม่',
             'Bellmouth/ปากดูด — erosion, pitting, strum/กระจัง', 'ขอบ manhole — รอยร้าว ขอบบาง', 'บันได แท่นพัก ราว — กัดกร่อน (ความปลอดภัยของผู้ตรวจ)',
             'ขอบ lightening holes/cut-outs และ coating ตามขอบคม']
    y = 100
    for i, it in enumerate(items):
        s += badge(bx + 24, y - 4, i + 1)
        chunks, cur = [], ''
        for part in it.split(' '):
            if len(cur) + len(part) > 33:
                chunks.append(cur); cur = part
            else:
                cur = (cur + ' ' + part).strip()
        chunks.append(cur)
        for j, c in enumerate(chunks):
            s += txt(bx + 44, y + j * 17, c, 11.5)
        y += 17 * len(chunks) + 9
    s += txt(340, 565, 'ภาพแนวคิดของถังข้าง/ถังท้องเรือ — ตำแหน่งจริงดูจากแบบโครงสร้างและ Ship Structure Access Manual ของเรือ', 11.5, 'middle', '#475569')
    save('insp-ballast-tank-hotspots.svg', s)


# ---------------------------------------------------------------- coating rating
def coating_rating():
    w, h = 1000, 400
    s = head(w, h, 'การประเมินสภาพ coating ตาม ESP Code: GOOD · FAIR · POOR')
    import random
    rnd = random.Random(7)
    panels = [('GOOD', '#15803d', 'มีสนิมเป็นจุดเล็กน้อยเท่านั้น', 'minor spot rusting', 0.02, 0),
              ('FAIR', '#ca8a04', 'coating เสื่อมเฉพาะที่ขอบ stiffener และแนวเชื่อม', 'และ/หรือสนิมบาง ๆ ≥ 20% ของพื้นที่ (แต่ยังไม่ถึง POOR)', 0.12, 1),
              ('POOR', '#b91c1c', 'coating เสื่อมทั่วไป ≥ 20% ของพื้นที่', 'หรือสนิมเกล็ดแข็ง (hard scale) ≥ 10% ของพื้นที่', 0.35, 2)]
    for i, (t, col, d1, d2, frac, lvl) in enumerate(panels):
        x = 40 + i * 320
        s += rect(x, 60, 290, 190, '#e5e7eb', col, 3, 8)
        # stiffeners
        for k in range(3):
            s += rect(x + 40 + k * 90, 60, 14, 190, '#d1d5db', '#6b7280', 1)
            if lvl >= 1:
                s += rect(x + 38 + k * 90, 60, 3, 190, '#b45309', '#b45309', 0)
                s += rect(x + 53 + k * 90, 60, 3, 190, '#b45309', '#b45309', 0)
        n = int(frac * 400)
        for _ in range(n):
            px, py = x + 6 + rnd.random() * 278, 66 + rnd.random() * 178
            r = 1.5 + rnd.random() * (2 if lvl < 2 else 7)
            s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="#b45309" opacity="0.8"/>'
        s += txt(x + 145, 280, t, 20, 'middle', col, True)
        s += txt(x + 145, 304, d1, 11.5, 'middle')
        s += txt(x + 145, 322, d2, 11.5, 'middle', '#334155')
    s += txt(500, 356, 'ESP (แก้ไขโดย MSC.525(106) มีผล 1 ก.ค. 2024): ถังอับเฉา (ยกเว้น double bottom) ที่ coating ต่ำกว่า GOOD และไม่ซ่อมใหม่', 11.5, 'middle', '#475569')
    s += txt(500, 374, 'หรือเป็น soft/semi-hard coating/ไม่มี hard coating ต้องตรวจภายในทุกปี (เดิมเกณฑ์คือ POOR) — ภาพเป็นแนวคิดเพื่อการจำ', 11.5, 'middle', '#475569')
    save('insp-coating-rating.svg', s)


# ---------------------------------------------------------------- heavy weather damage
def weather_damage():
    w, h = 1000, 470
    s = head(w, h, 'ความเสียหายจากสภาพอากาศเลว (Severe weather) — ตำแหน่งที่ต้องตรวจหลังผ่านพายุ')
    # profile of bulk carrier
    s += '<path d="M 60 260 L 120 300 L 860 300 L 930 230 L 940 170 L 120 170 L 60 200 Z" fill="#e2e8f0" stroke="#0f172a" stroke-width="2.5"/>'
    s += '<rect x="80" y="110" width="90" height="60" fill="#cbd5e1" stroke="#0f172a" stroke-width="2"/>'
    for k in range(5):
        x = 260 + k * 125
        s += f'<rect x="{x}" y="155" width="100" height="15" fill="#94a3b8" stroke="#0f172a" stroke-width="1.5"/>'
    s += line(20, 250, 980, 250, '#0284c7', 1.5, '8 5')
    # sea
    s += '<path d="M 700 150 Q 800 90 900 150" fill="none" stroke="#0369a1" stroke-width="4"/>'
    s += txt(800, 90, 'คลื่นซัดหัวเรือ (green seas)', 12, 'middle', '#0369a1', True)
    marks = [(1, 900, 185), (2, 820, 160), (3, 905, 270), (4, 520, 150), (5, 622, 152), (6, 330, 160), (7, 120, 235), (8, 860, 200)]
    for n, x, y in marks:
        s += badge(x, y, n)
    items = ['ดาดฟ้าหัวเรือ: ท่ออากาศ ช่องระบาย ฝาช่องเปิด กว้าน',
             'ฝาระวางหมายเลข 1: เสียรูป cleat ขาด ซีลรั่ว',
             'ท้องเรือส่วนหัว: slamming แผ่นบุบ โครงในโก่ง',
             'มุมช่องระวาง/ดาดฟ้ากลางลำ: รอยร้าว (hog/sag, ล้า)',
             'Bulwark ราวกันตก บันได: คลื่นซัดพัง',
             'ฝาระวางช่องอื่น: ตัวเรือบิดตัว ซีลรั่ว',
             'สินค้าเลื่อน: ผนังระวาง จุดยึด lashing เสียหาย',
             'Fore peak/chain locker: น้ำเข้า (ตรวจ sounding/alarm)']
    for i, it in enumerate(items):
        y = 340 + (i // 2) * 30
        x = 40 + (i % 2) * 480
        s += badge(x + 10, y - 4, i + 1)
        s += txt(x + 28, y, it, 12.5)
    save('insp-weather-damage.svg', s)


# ---------------------------------------------------------------- inspection schedule
def schedule():
    w, h = 1000, 520
    s = head(w, h, 'ตัวอย่างแผนหมุนเวียนการตรวจ (Inspection rotation) ให้ครอบคลุมทุกพื้นที่ภายใน 12 เดือน')
    months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
    rows = [('ระวาง 1–5 (หลังขนลงทุกครั้ง)', [1] * 12, '#f59e0b'),
            ('ฝาระวาง (ตรวจด้วยตา/ทุกเที่ยว)', [1] * 12, '#64748b'),
            ('ฝาระวาง (ทดสอบผนึกน้ำ)', [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0], '#475569'),
            ('Topside tanks 1P/S–2P/S', [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], '#1d4ed8'),
            ('Topside tanks 3P/S–5P/S', [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], '#1d4ed8'),
            ('Hopper/DB tanks 1–2', [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0], '#0369a1'),
            ('Hopper/DB tanks 3–5', [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0], '#0369a1'),
            ('Fore peak / Aft peak', [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0], '#7c3aed'),
            ('Void spaces, pipe duct, chain locker', [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], '#be185d')]
    x0, y0, cw, rh = 300, 70, 54, 36
    for j, m in enumerate(months):
        s += txt(x0 + j * cw + cw / 2, y0 + 16, m, 12, 'middle', '#0f172a', True)
    for i, (name, flags, col) in enumerate(rows):
        y = y0 + 28 + i * rh
        s += rect(30, y, 260, rh - 6, '#f8fafc', '#cbd5e1', 1)
        s += txt(38, y + 20, name, 12)
        for j, f in enumerate(flags):
            s += rect(x0 + j * cw + 2, y, cw - 4, rh - 6, col if f else '#f1f5f9', '#e2e8f0', 1, 4)
    s += txt(500, y0 + 28 + len(rows) * rh + 24, 'แต่ละถังถูกตรวจ 2 ครั้งต่อปีในตัวอย่างนี้ — ปรับตามอายุเรือ สภาพ coating ประวัติความเสียหาย ข้อกำหนดบริษัท/สมาคมจัดชั้น และโอกาสที่ถังว่าง', 12, 'middle')
    s += txt(500, y0 + 28 + len(rows) * rh + 44, 'ตารางสมมุติสำหรับเรือ bulk 5 ระวาง — การตรวจของลูกเรือไม่แทนที่การ survey ของสมาคมจัดชั้น แต่เป็นเอกสารสนับสนุนใน ESP', 12, 'middle', '#475569')
    save('insp-schedule.svg', s)


if __name__ == '__main__':
    bulk_section(); hatch_cover(); corrosion(); ballast_hotspots(); coating_rating(); weather_damage(); schedule()
