"""ภาพประกอบบท 2.1 (การขนถ่าย จัดวาง ยึดสินค้า) และ 2.2 (การตรวจระวาง ฝาระวาง ถังอับเฉา)"""
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


# ---------------------------------------------------------------- heavy lift
def heavy_lift():
    w, h = 1000, 560
    s = head(w, h, 'การยกของหนัก (Heavy lift) ด้วยปั้นจั่นของเรือ: ผลต่อ KG, GM และมุมเอียง')
    cx, wl, keel = 330, 330, 430
    # hull section (listed slightly to stbd = right)
    ang = 5.1
    s += f'<g transform="rotate({ang} {cx} {wl})">'
    s += f'<path d="M {cx-150} 200 L {cx+150} 200 L {cx+150} {keel-30} Q {cx+150} {keel} {cx+120} {keel} L {cx-120} {keel} Q {cx-150} {keel} {cx-150} {keel-30} Z" fill="#e2e8f0" stroke="#0f172a" stroke-width="2"/>'
    s += rect(cx - 150, keel - 60, 50, 60, '#bfdbfe', '#1d4ed8', 1.2)
    s += txt(cx - 125, keel - 26, 'WB', 11, 'middle', '#1d4ed8', True)
    s += line(cx, 200, cx, 80, '#334155', 6)  # crane pedestal/jib start
    s += line(cx, 90, cx + 230, 60, '#334155', 5)  # jib
    s += f'<circle cx="{cx+230}" cy="60" r="6" fill="#0f172a"/>'
    s += line(cx + 230, 60, cx + 230, 170, '#0f172a', 1.5)
    s += rect(cx + 205, 170, 50, 34, '#fde68a', '#92400e', 1.5)
    s += txt(cx + 230, 192, '120 t', 11, 'middle', '#78350f', True)
    s += f'<circle cx="{cx}" cy="{keel-85}" r="6" fill="#b91c1c"/>' + txt(cx - 12, keel - 81, 'G₀', 13, 'end', '#b91c1c', True)
    s += f'<circle cx="{cx+24}" cy="{keel-122}" r="6" fill="#c2410c"/>' + txt(cx + 36, keel - 118, 'G₁ (ขณะยก)', 12, 'start', '#c2410c', True)
    s += f'<circle cx="{cx}" cy="{keel-165}" r="5" fill="#15803d"/>' + txt(cx - 12, keel - 161, 'M', 13, 'end', '#15803d', True)
    s += line(cx, keel - 85, cx + 22, keel - 119, '#c2410c', 1.5, '4 3')
    s += '</g>'
    s += f'<rect x="20" y="{wl}" width="640" height="{h-wl-20}" fill="#e0f2fe" opacity="0.55"/>'
    s += line(20, wl, 660, wl, '#0284c7', 2)
    s += txt(30, wl - 6, 'ผิวน้ำ', 11, 'start', '#0284c7')
    s += txt(40, 100, 'เมื่อของพ้นพื้น (ท่า/เรือลำเลียง) น้ำหนักทั้งหมด', 12, 'start', '#334155', True)
    s += txt(40, 118, '"กระทำที่หัวปั้นจั่น (jib head)" ทันที', 12, 'start', '#334155', True)
    s += txt(cx - 140, 230, 'เรือเอียงไปด้านที่ยก', 12, 'start', '#b91c1c', True)
    s += txt(cx - 140, 246, '(ในภาพ ≈ 5° หลังเติม ballast ถ่วงไว้)', 11, 'start', '#b91c1c')
    s += txt(cx - 150, keel + 60, 'WB = ถังอับเฉาด้านตรงข้าม (counter ballast)', 11.5, 'start', '#1d4ed8')
    # calc box
    bx, by = 680, 60
    s += rect(bx, by, 300, 470, '#f8fafc', '#94a3b8', 1, 10)
    L = ['ตัวอย่างจำลอง (เรือ MPP สมมุติ)', 'Δ 12,000 t · KG 7.50 m · KM 8.50 m', 'GM 1.00 m (แก้ FSE แล้ว)',
         'ยก 120 t · หัวปั้นจั่นสูง 30 m จาก keel', 'ระยะยื่น (outreach) 15 m จากแนวกลางลำ', '',
         '1) ของพ้นพื้น: KG₁ = (12,000×7.5 + 120×30)', '    ÷ 12,120 = 7.72 m → GM₁ = 0.78 m', '2) มุมเอียง: tan θ = (120×15)', '    ÷ (12,120×0.78) → θ ≈ 10.8°',
         '3) เติม ballast 90 t ถังกราบตรงข้าม', '    (แขน 10 m): ก่อนยกเอียงตรงข้าม ≈ 4.1°', '    ขณะยกที่ระยะยื่นสูงสุด ≈ 5.1°', '',
         '4) วางบนดาดฟ้ากลางลำ (Kg 12 m) แล้ว', '    สูบ ballast ออก → GM ≈ 0.95 m', '', 'สูตรจำ: GG₁ = w × d ÷ Δ (d = ระยะจากจุด',
         'เดิมของของถึงหัวปั้นจั่น) · tan θ = w × y ÷ (Δ × GM)']
    for i, l in enumerate(L):
        s += txt(bx + 12, by + 24 + i * 22, l, 12, 'start', '#0f172a', i in (0, 17))
    save('cargo-heavy-lift.svg', s)


# ---------------------------------------------------------------- bay-row-tier
def bay_row_tier():
    w, h = 1000, 560
    s = head(w, h, 'ระบบตำแหน่งตู้สินค้า Bay – Row – Tier (ISO 9711 / ระบบที่ใช้กันทั่วไป)')
    # side view bays
    s += txt(250, 66, 'มองด้านข้าง: Bay', 14, 'middle', bold=True)
    x0, y0 = 40, 110
    labels = ['01', '03', '05', '07', '09', '11']
    for i, b in enumerate(labels):
        x = 440 - i * 66
        s += rect(x - 60, y0 + 40, 60, 40, '#dbeafe', '#1d4ed8')
        s += txt(x - 30, y0 + 66, b, 12, 'middle', '#1d4ed8', True)
    # ตู้ 40 ฟุตคร่อม bay 07 (x 182–242) และ 05 (x 248–308) → bay 06
    s += rect(440 - 3 * 66 - 60, y0, 126, 38, '#fde68a', '#92400e')
    s += txt(440 - 3 * 66 + 3, y0 + 24, '40 ฟุต = Bay 06', 12, 'middle', '#78350f', True)
    s += txt(250, y0 + 108, '← ท้ายเรือ                     หัวเรือ →', 12, 'middle', '#475569')
    s += txt(250, y0 + 128, 'ตู้ 20 ฟุตใช้เลขคี่ · ตู้ 40 ฟุตที่คร่อมสอง bay ใช้เลขคู่ระหว่างกลาง', 12, 'middle')
    s += txt(250, y0 + 146, '(เช่น ตู้ 40 ฟุตคร่อม bay 05 และ 07 = bay 06) — นับจากหัวไปท้าย', 12, 'middle')
    # cross section rows & tiers
    s += txt(730, 66, 'มองหน้าตัด (จากท้ายไปหัว): Row และ Tier', 14, 'middle', bold=True)
    cx, base = 730, 470
    rows = ['08', '06', '04', '02', '01', '03', '05', '07']
    cw = 44
    # hull
    s += f'<path d="M {cx-200} 300 L {cx+200} 300 L {cx+200} {base} L {cx-200} {base} Z" fill="none" stroke="#0f172a" stroke-width="2.5"/>'
    s += rect(cx - 205, 292, 410, 10, '#94a3b8', '#0f172a', 1)
    s += txt(cx + 210, 300, 'ฝาระวาง', 11, 'start', '#334155')
    for i, r in enumerate(rows):
        x = cx - 4 * cw + i * cw
        for t in range(3):  # hold tiers 02 04 06
            y = base - (t + 1) * 52
            s += rect(x + 1, y + 1, cw - 2, 50, '#e2e8f0', '#64748b', 1)
            if i == 0: s += txt(cx - 4 * cw - 8, y + 30, f'{(t+1)*2:02d}', 11, 'end', '#b91c1c', True)
        for t in range(3):  # deck tiers 82 84 86
            y = 292 - (t + 1) * 52
            s += rect(x + 1, y + 1, cw - 2, 50, '#dcfce7', '#15803d', 1)
            if i == 0: s += txt(cx - 4 * cw - 8, y + 30, f'{82+t*2}', 11, 'end', '#15803d', True)
        s += txt(x + cw / 2, base + 18, r, 12, 'middle', '#1d4ed8', True)
    s += line(cx, 120, cx, base + 6, '#b91c1c', 1.2, '5 4')
    s += txt(cx, 116, 'แนวกลางลำ', 11, 'middle', '#b91c1c')
    s += txt(cx - 100, base + 40, '← กราบซ้าย: เลขคู่', 12, 'middle', '#1d4ed8', True)
    s += txt(cx + 100, base + 40, 'กราบขวา: เลขคี่ →', 12, 'middle', '#1d4ed8', True)
    s += txt(cx, base + 60, '(ถ้าจำนวน row เป็นเลขคี่ row กลางลำ = 00)', 11, 'middle', '#475569')
    # hi-light one container
    x = cx - 4 * cw + 5 * cw; y = 292 - 2 * 52
    s += rect(x + 1, y + 1, cw - 2, 50, '#fca5a5', '#b91c1c', 2.5)
    # example box
    s += rect(40, 300, 420, 230, '#f8fafc', '#94a3b8', 1, 10)
    E = ['ตัวอย่างตำแหน่ง: 06 03 84', '• Bay 06 = ตู้ 40 ฟุต คร่อม bay 05/07', '• Row 03 = แถวที่สองกราบขวานับจากกลางลำ',
         '• Tier 84 = ชั้นที่สองบนดาดฟ้า', '(ตู้สีแดงในหน้าตัด)', '', 'Tier ในระวาง: 02, 04, 06 … จากล่างขึ้นบน',
         'Tier บนดาดฟ้า: 82 (หรือ 80), 84, 86 …', 'ใช้ใน bay plan / BAPLIE และระบบ loading computer', 'ตรวจกับ stowage plan ของเรือเสมอ — บางสายเรือใช้ระบบต่างไปเล็กน้อย']
    for i, e in enumerate(E):
        s += txt(56, 326 + i * 20, e, 12.5 if i else 14, 'start', '#0f172a', i == 0)
    save('cargo-bay-row-tier.svg', s)


# ---------------------------------------------------------------- container lashing
def lashing():
    w, h = 1000, 560
    s = head(w, h, 'อุปกรณ์ยึดตู้สินค้าบนดาดฟ้า (Container lashing) และแรงที่กระทำ')
    base = 430
    s += rect(60, base, 520, 22, '#94a3b8', '#0f172a', 1.5)
    s += txt(320, base + 16, 'ฝาระวาง (hatch cover)', 12, 'middle', '#0f172a', True)
    # lashing bridge
    s += rect(30, base - 210, 26, 232, '#cbd5e1', '#0f172a', 1.2)
    s += txt(43, base + 42, 'lashing bridge', 11, 'middle', '#334155')
    for col in range(3):
        x = 70 + col * 170
        for t in range(4):
            y = base - (t + 1) * 78
            s += rect(x, y, 160, 76, '#dbeafe' if t % 2 == 0 else '#e0e7ff', '#1d4ed8', 1.4)
            # corner fittings
            for cxp in (x + 4, x + 146):
                for cyp in (y + 4, y + 62):
                    s += rect(cxp, cyp, 10, 10, '#334155', '#0f172a', 0.5)
        for t in range(4):
            y = base - t * 78
            for cxp in (x + 6, x + 148):
                s += rect(cxp - 2, y - 4, 10, 6, '#f59e0b', '#92400e', 0.8)
    # lashing rods from lashing bridge/hatch to corner castings (cross lashing)
    for x in (70, 240):
        s += line(x + 2, base, x + 150, base - 152, '#b91c1c', 2.5)
        s += line(x + 158, base, x + 10, base - 152, '#b91c1c', 2.5)
        s += rect(x + 20, base - 30, 10, 26, '#f97316', '#9a3412', 1) + rect(x + 130, base - 30, 10, 26, '#f97316', '#9a3412', 1)
    s += txt(600, 110, 'ส่วนประกอบหลัก', 15, 'start', bold=True)
    items = [('#f59e0b', 'Twistlock (SATL/FAT) และ stacking cone — ยึดมุมตู้ระหว่างชั้น'),
             ('#b91c1c', 'Lashing rod — ยึดแนวทแยงจากฝาระวาง/lashing bridge'),
             ('#f97316', 'Turnbuckle (bottle screw) — ปรับความตึง lashing rod'),
             ('#334155', 'Corner casting — จุดยึดมุมตู้ 8 มุม (ISO)'),
             ('#cbd5e1', 'Lashing bridge — ให้ lash ได้สูงขึ้น ลดแรงต่อชั้นบน'),
             ('#94a3b8', 'Bridge fitting / buttress — ยึดระหว่างแถวบนสุด (บางเรือ)')]
    for i, (c, t) in enumerate(items):
        y = 140 + i * 30
        s += rect(600, y - 12, 16, 16, c, '#0f172a', 0.8) + txt(626, y + 1, t, 12)
    s += txt(600, 340, 'แรงที่กระทำต่อตู้ในทะเล', 15, 'start', bold=True)
    forces = ['• แรงขวาง (transverse) จากการโคลง — มากที่สุดที่ชั้นบนและหัว/ท้ายเรือ',
              '• แรงตามยาว (longitudinal) จากการโต้ (pitch)', '• แรงตั้ง (vertical) จากการ heave/pitch — ตู้ยกตัว (racking/tipping)',
              '• ลมบนตู้ชั้นบนและคลื่นกระแทก (green sea)', '• ขีดจำกัด: น้ำหนักกองตู้ (stack weight), ความสูงกอง, GM สูงเกิน',
              '  → โคลงเร็ว แรงเร่งสูง (ตรวจด้วย lashing computer)', '• Parametric rolling ทำให้ lashing ล้มเหลวทั้งกองได้']
    for i, f in enumerate(forces):
        s += txt(600, 366 + i * 22, f, 12)
    s += txt(320, 70, 'ตัวอย่างการยึดแบบ cross lashing (มองจากหัว/ท้าย)', 13, 'middle', '#334155', True)
    s += txt(320, 520, 'การจัดยึดจริงต้องเป็นไปตาม Cargo Securing Manual (CSM) ของเรือ และผลคำนวณ lashing software', 12, 'middle', '#b91c1c')
    save('cargo-container-lashing.svg', s)


# ---------------------------------------------------------------- IMDG classes
def imdg():
    w, h = 1000, 640
    s = head(w, h, 'IMDG Code: ประเภทสินค้าอันตราย 9 ประเภท และคำศัพท์การแยกเก็บ (Segregation)')
    classes = [('1', 'วัตถุระเบิด', 'Explosives (1.1–1.6)', '#f97316', '#0f172a'),
               ('2', 'ก๊าซ', '2.1 ไวไฟ (แดง) · 2.2 ไม่ไวไฟ|ไม่เป็นพิษ (เขียว) · 2.3 พิษ (ขาว)', '#15803d', '#fff'),
               ('3', 'ของเหลวไวไฟ', 'Flammable liquids', '#dc2626', '#fff'),
               ('4', 'ของแข็งไวไฟ ฯลฯ', '4.1 ของแข็งไวไฟ · 4.2 ลุกไหม้เอง|4.3 ถูกน้ำแล้วเกิดก๊าซไวไฟ', '#ef4444', '#fff'),
               ('5', 'ออกซิไดซ์/เปอร์ออกไซด์', '5.1 Oxidizing · 5.2 Organic peroxides', '#facc15', '#0f172a'),
               ('6', 'พิษ/ติดเชื้อ', '6.1 Toxic · 6.2 Infectious', '#f8fafc', '#0f172a'),
               ('7', 'กัมมันตรังสี', 'Radioactive (I, II, III, fissile)', '#fde047', '#0f172a'),
               ('8', 'กัดกร่อน', 'Corrosive', '#1f2937', '#fff'),
               ('9', 'อันตรายอื่น ๆ', 'Miscellaneous (เช่น lithium batteries)', '#f1f5f9', '#0f172a')]
    for i, (n, th, en, col, tc) in enumerate(classes):
        c, r = i % 3, i // 3
        x, y = 110 + c * 310, 110 + r * 120
        sz = 44
        s += f'<polygon points="{x},{y-sz} {x+sz},{y} {x},{y+sz} {x-sz},{y}" fill="{col}" stroke="#0f172a" stroke-width="2"/>'
        if n == '4':
            s += f'<polygon points="{x},{y-sz} {x+sz},{y} {x},{y+sz} {x-sz},{y}" fill="url(#stripes)" stroke="#0f172a" stroke-width="2"/>'
        if n == '7':
            s += f'<polygon points="{x-sz},{y} {x},{y+sz} {x+sz},{y}" fill="#fff"/>'
            s += f'<polygon points="{x},{y-sz} {x+sz},{y} {x},{y+sz} {x-sz},{y}" fill="none" stroke="#0f172a" stroke-width="2"/>'
        if n == '8':
            s += f'<polygon points="{x},{y-sz} {x+sz},{y} {x-sz},{y}" fill="#fff"/>'
            s += f'<polygon points="{x},{y-sz} {x+sz},{y} {x},{y+sz} {x-sz},{y}" fill="none" stroke="#0f172a" stroke-width="2"/>'
        if n == '9':
            # ป้าย class 9: แถบดำแนวตั้ง 7 แถบในครึ่งบน
            for k in range(7):
                s += line(x - 21 + k * 7, y - 30, x - 21 + k * 7, y - 6, '#0f172a', 3)
        s += txt(x, y + 34, n, 16, 'middle', '#fff' if n == '8' else '#0f172a', True)
        s += txt(x + 56, y - 6, f'Class {n}: {th}', 14, 'start', '#0f172a', True)
        for k, part in enumerate(en.split('|')):
            s += txt(x + 56, y + 14 + k * 15, part, 11, 'start', '#334155')
    s = s.replace('<defs>', '<defs><pattern id="stripes" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="6" height="12" fill="#dc2626"/><rect x="6" width="6" height="12" fill="#fff"/></pattern>', 1)
    # segregation table
    y0 = 470
    s += txt(40, y0 - 10, 'คำศัพท์การแยกเก็บ (IMDG Code ส่วนที่ 7) — จากหลวมไปเข้มงวด', 14, 'start', bold=True)
    seg = [('1', 'Away from', 'แยกห่างพอไม่ให้ทำปฏิกิริยากันถ้าเกิดอุบัติเหตุ (อยู่ช่องเดียวกันได้)'),
           ('2', 'Separated from', 'ต่างช่อง/ต่างระวาง (หรือบนดาดฟ้าตามระยะที่กำหนด)'),
           ('3', 'Separated by a complete compartment or hold from', 'มีระวาง/ช่องเต็มหนึ่งช่องคั่นกลาง'),
           ('4', 'Separated longitudinally by an intervening complete compartment or hold from', 'คั่นด้วยระวางเต็มตามแนวยาวเรือ')]
    for i, (n, en, th) in enumerate(seg):
        y = y0 + 12 + i * 36
        s += rect(40, y, 30, 28, '#1d4ed8', '#1d4ed8', 0, 4) + txt(55, y + 19, n, 14, 'middle', '#fff', True)
        s += txt(80, y + 13, en, 12.5, 'start', '#0f172a', True)
        s += txt(80, y + 27, th, 11.5, 'start', '#334155')
    s += txt(620, y0 + 30, 'ใช้ร่วมกับ Dangerous Goods List (คอลัมน์', 12, 'start')
    s += txt(620, y0 + 48, 'stowage &amp; segregation, SG codes), ตาราง', 12, 'start')
    s += txt(620, y0 + 66, 'segregation 7.2.4 และตารางเฉพาะเรือ container', 12, 'start')
    s += txt(620, y0 + 84, '"X" ในตาราง = ดู DGL เป็นรายสาร', 12, 'start')
    s += txt(620, y0 + 112, 'ป้ายในภาพเป็นแบบย่อเพื่อจำสี — รูปสัญลักษณ์', 11, 'start', '#b91c1c')
    s += txt(620, y0 + 128, 'จริงดูจาก IMDG Code 5.2', 11, 'start', '#b91c1c')
    save('cargo-imdg-classes.svg', s)


# ---------------------------------------------------------------- ventilation
def ventilation():
    w, h = 1000, 480
    s = head(w, h, 'การระบายอากาศในระวาง: Ship\'s sweat กับ Cargo sweat และกฎ dew point')
    for i, (title, sub, col, items) in enumerate([
        ("Ship's sweat (เหงื่อตัวเรือ)", 'เรือเดินจากที่อุ่นไปที่เย็น', '#1d4ed8',
         ['อากาศในระวางอุ่นและชื้น', 'แต่ผนัง/ดาดฟ้าเย็นลงตามทะเล', 'ผิวโลหะเย็นกว่า dew point', 'ของอากาศในระวาง',
          '→ ไอน้ำกลั่นตัวใต้ดาดฟ้า หยดลงสินค้า', 'แก้: ระบายอากาศถ้าอากาศภายนอก', 'มี dew point ต่ำกว่าในระวาง']),
        ('Cargo sweat (เหงื่อสินค้า)', 'เรือเดินจากที่เย็นไปที่อุ่น', '#b91c1c',
         ['สินค้ายังเย็นจากต้นทาง', 'อากาศภายนอกอุ่นชื้นเข้ามา', 'สัมผัสผิวสินค้าที่เย็น', '→ ไอน้ำกลั่นตัวบนสินค้าโดยตรง',
          'แก้: งด/ลดระบายอากาศ ถ้า dew point', 'อากาศภายนอกสูงกว่า', 'อุณหภูมิสินค้า'])]):
        x = 40 + i * 480
        s += rect(x, 60, 440, 250, '#f8fafc', col, 2, 12)
        s += txt(x + 220, 88, title, 16, 'middle', col, True)
        s += txt(x + 220, 108, sub, 12.5, 'middle', '#334155')
        # little hold drawing
        s += f'<path d="M {x+30} 140 L {x+170} 140 L {x+170} 280 L {x+30} 280 Z" fill="#fff" stroke="#0f172a" stroke-width="2"/>'
        s += rect(x + 50, 220, 100, 60, '#fde68a', '#92400e', 1)
        s += txt(x + 100, 255, 'สินค้า', 12, 'middle', '#78350f', True)
        if i == 0:
            for k in range(6):
                s += f'<circle cx="{x+45+k*22}" cy="{148+ (k%2)*6}" r="3.5" fill="#1d4ed8"/>'
                s += line(x + 45 + k * 22, 156, x + 45 + k * 22, 196, '#1d4ed8', 1.2, '3 3')
        else:
            for k in range(5):
                s += f'<circle cx="{x+60+k*20}" cy="216" r="3.5" fill="#b91c1c"/>'
            s += line(x + 30, 160, x + 60, 190, '#b91c1c', 2, mk='arR')
            s += txt(x + 34, 154, 'อากาศอุ่นชื้นเข้า', 10.5, 'start', '#b91c1c')
        for j, it in enumerate(items):
            s += txt(x + 190, 142 + j * 23, it, 11.5)
    s += rect(40, 330, 920, 130, '#f0fdf4', '#15803d', 1.5, 12)
    rules = ['กฎ dew point (ใช้กับสินค้าส่วนใหญ่): ระบายอากาศเมื่อ dew point ของอากาศภายนอก ต่ำกว่า dew point ของอากาศในระวาง — ถ้าสูงกว่า งดระบาย',
             'กฎ 3 องศา (สินค้าดูดความชื้น เช่น เมล็ดพืช ข้าว กาแฟ โกโก้ — เมื่อวัด dew point ในระวางไม่ได้): ระบายอากาศเมื่ออุณหภูมิอากาศภายนอก',
             'ต่ำกว่าอุณหภูมิสินค้า (วัดตอนบรรทุก) อย่างน้อย 3°C · อ่าน dry/wet bulb ทั้งภายในและภายนอก และบันทึกใน ventilation log ทุกยาม',
             'ไม่ระบายอากาศเมื่อคลื่นซัดน้ำเข้าช่องระบาย สินค้าที่ห้ามระบาย (เช่นบางชนิดใน IMSBC) หรือมีการรมยาในระวาง — ทำตามคำแนะนำผู้ส่ง/IMSBC/คู่มือเรือ']
    for i, r in enumerate(rules):
        s += txt(56, 358 + i * 26, r, 12, 'start', '#14532d', i == 0)
    save('cargo-ventilation.svg', s)


# ---------------------------------------------------------------- securing forces & rule of thumb
def securing():
    w, h = 1000, 470
    s = head(w, h, 'หลักการยึดสินค้า (CSS Code): แรง มุม lashing และ Maximum Securing Load (MSL)')
    # cargo unit
    x, y = 160, 170
    s += rect(x, y, 200, 140, '#fde68a', '#92400e', 2)
    s += txt(x + 100, y + 76, 'สินค้า W ตัน', 14, 'middle', '#78350f', True)
    s += rect(60, y + 140, 400, 16, '#94a3b8', '#0f172a', 1)
    s += line(x, y + 30, x - 80, y + 140, '#b91c1c', 3) + line(x + 200, y + 30, x + 280, y + 140, '#b91c1c', 3)
    s += f'<path d="M {x-80+30} {y+140} A 30 30 0 0 0 {x-80+18} {y+117}" fill="none" stroke="#0f172a"/>'
    s += txt(x - 40, y + 128, 'α', 13, 'start', '#0f172a', True)
    s += line(x + 100, y - 24, x + 220, y - 24, '#1d4ed8', 3, mk='arB') + txt(x + 100, y - 32, 'แรงขวาง (โคลง)', 12, 'start', '#1d4ed8', True)
    s += line(x + 100, y + 150, x + 100, y + 210, '#15803d', 3, mk='arG') + txt(x + 110, y + 205, 'แรงเสียดทาน/น้ำหนัก', 12, 'start', '#15803d', True)
    s += txt(x + 100, 70, 'มุม lashing (α) ต่ำ → ต้านการเลื่อนได้ดี', 12, 'middle')
    s += txt(x + 100, 88, 'มุมสูงขึ้น → ต้านการยกตัว/ล้มได้ดีขึ้น — ใช้ตามที่ CSM กำหนด', 12, 'middle', '#334155')
    # table MSL
    bx = 520
    s += txt(bx, 70, 'MSL เป็น % ของแรงขาดต่ำสุด (MBL) — CSS Code Annex 13', 13, 'start', bold=True)
    rows = [('Shackles, rings, deck eyes, turnbuckles (เหล็กกล้าอ่อน)', '50%'), ('Fibre rope', '33%'), ('Web lashing', '50%'),
            ('Wire rope (ใช้ครั้งเดียว)', '80%'), ('Wire rope (ใช้ซ้ำ)', '30%'), ('Steel band (ใช้ครั้งเดียว)', '70%'), ('Chains', '50%')]
    for i, (a, b) in enumerate(rows):
        yy = 90 + i * 28
        s += rect(bx, yy, 360, 26, '#f8fafc' if i % 2 else '#eef2ff', '#cbd5e1', 1)
        s += rect(bx + 360, yy, 80, 26, '#f8fafc' if i % 2 else '#eef2ff', '#cbd5e1', 1)
        s += txt(bx + 8, yy + 18, a, 12) + txt(bx + 400, yy + 18, b, 12.5, 'middle', '#1d4ed8', True)
    s += rect(bx, 300, 440, 140, '#fff7ed', '#c2410c', 1.5, 10)
    rl = ['กฎหัวแม่มือ (rule-of-thumb) ของ CSS Code:', 'ผลรวม MSL ของอุปกรณ์ยึดแต่ละข้าง (ซ้ายและขวา)',
          'ของสินค้าหนึ่งหน่วย ควรเท่ากับน้ำหนักของสินค้า', 'เช่น สินค้า 30 ตัน → ข้างละ ≥ 30 t MSL',
          'ใช้เมื่อไม่มีวิธีคำนวณละเอียด (Advanced calculation', 'method ใน CSM) — แรงเร่งจริงขึ้นกับตำแหน่ง/GM']
    for i, r in enumerate(rl):
        s += txt(bx + 14, 324 + i * 20, r, 12, 'start', '#7c2d12', i == 0)
    save('cargo-securing-principles.svg', s)


# ---------------------------------------------------------------- longitudinal strength
def strength():
    w, h = 1000, 540
    s = head(w, h, 'ความแข็งแรงตามยาว: Hogging, Sagging, Shear force และ Bending moment')
    # hogging and sagging sketches
    for i, (t, d, col, desc) in enumerate([('Hogging (กลางลำโก่งขึ้น)', 'M 60 150 Q 230 95 400 150', '#b91c1c', 'น้ำหนักมากที่หัว-ท้าย / ยอดคลื่นกลางลำ → ดาดฟ้ารับแรงดึง ท้องเรือรับแรงอัด'),
                                           ('Sagging (กลางลำแอ่นลง)', 'M 560 110 Q 730 165 900 110', '#1d4ed8', 'น้ำหนักมากกลางลำ / ท้องคลื่นกลางลำ → ดาดฟ้ารับแรงอัด ท้องเรือรับแรงดึง')]):
        x0 = 60 + i * 500
        s += txt(x0 + 170, 72, t, 15, 'middle', col, True)
        s += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="16" stroke-linecap="round" opacity="0.85"/>'
        s += txt(x0 + 170, 200, desc, 11.5, 'middle', '#334155')
    # SF & BM curves
    gx, gy, gw = 90, 330, 820
    s += line(gx, gy, gx + gw, gy, '#0f172a', 1.5)
    s += txt(gx - 10, gy + 4, '0', 11, 'end')
    s += txt(gx - 14, gy + 20, 'ท้าย (AP)', 11, 'end', '#475569') + txt(gx + gw + 6, gy + 4, 'หัว (FP)', 11, 'start', '#475569')
    sf, bm = [], []
    for i in range(101):
        xx = i / 100
        v = math.sin(2 * math.pi * xx) * 80 * (1 - 0.2 * xx)
        sf.append((gx + xx * gw, gy - v))
        b = (1 - math.cos(2 * math.pi * xx)) / 2 * 95
        bm.append((gx + xx * gw, gy + 0 - b))
    s += '<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in sf) + '" fill="none" stroke="#15803d" stroke-width="3"/>'
    s += '<polyline points="' + ' '.join(f'{a:.1f},{b:.1f}' for a, b in bm) + '" fill="none" stroke="#b91c1c" stroke-width="3"/>'
    s += txt(gx + 0.25 * gw, gy - 90, 'Shear force (SF) — สูงสุดประมาณ 1/4 จากปลาย', 12, 'middle', '#15803d', True)
    s += txt(gx + 0.62 * gw, gy - 100, 'Bending moment (BM) — สูงสุดใกล้กลางลำ', 12, 'start', '#b91c1c', True)
    s += txt(500, gy + 112, 'ค่าจริงต้องคำนวณด้วย loading instrument/loading computer ที่รับรอง เทียบกับค่าที่ยอมให้ (permissible) ทั้งในท่าและในทะเล', 12, 'middle')
    s += txt(500, gy + 132, 'ทุกขั้นตอนของการขนถ่าย (ไม่ใช่แค่สภาพสุดท้าย) — โดยเฉพาะเรือ bulk ที่บรรทุกเร็ว (SOLAS XII, BLU Code)', 12, 'middle')
    s += txt(500, gy + 152, 'นอกจากนี้ต้องดู local strength: น้ำหนักต่อพื้นที่ tank top (t/m²), น้ำหนักกองตู้, น้ำหนักบนฝาระวาง/ดาดฟ้า', 12, 'middle', '#b91c1c')
    s += txt(500, gy + 180, 'กราฟเป็นรูปแบบตัวอย่างเพื่อแสดงแนวคิดเท่านั้น', 11, 'middle', '#475569')
    save('cargo-longitudinal-strength.svg', s)


# ---------------------------------------------------------------- ship–shore communication
def communication():
    w, h = 1000, 520
    s = head(w, h, 'การสื่อสารระหว่างการขนถ่ายสินค้า (Ship–shore communication)')
    nodes = {'M': (170, 120, 'นายเรือ', 'Master'), 'C': (500, 120, 'ต้นเรือ / Chief Officer', 'ผู้รับผิดชอบงานสินค้า'),
             'T': (830, 120, 'Terminal / Stevedore', 'Shore supervisor, foreman'), 'O': (500, 270, 'OOW (นายยามสินค้า)', 'Cargo watch'),
             'E': (170, 270, 'ห้องเครื่อง', 'ballast / power / pumps'), 'K': (830, 270, 'ผู้ควบคุมเครน/ปั๊มฝั่ง', 'Crane / loading arm'),
             'A': (500, 400, 'ลูกเรือยาม / AB', 'gangway, mooring, deck rounds')}
    for a, b in ('MC', 'CT', 'CO', 'OE', 'OK', 'OA', 'TK', 'OT', 'MO'):
        x1, y1 = nodes[a][:2]; x2, y2 = nodes[b][:2]
        s += line(x1, y1, x2, y2, '#94a3b8', 2.5)
    for x, y, t1, t2 in nodes.values():
        s += rect(x - 140, y - 34, 280, 68, '#eff6ff', '#1d4ed8', 1.8, 12)
        s += txt(x, y - 6, t1, 14, 'middle', '#0f172a', True) + txt(x, y + 16, t2, 11.5, 'middle', '#334155')
    s += rect(40, 460 - 10, 920, 60, '#fef2f2', '#b91c1c', 1.5, 10)
    s += txt(56, 474, 'ตกลงก่อนเริ่ม: แผนขนถ่าย/อัตรา, ช่องวิทยุและภาษา, ผู้ติดต่อ, สัญญาณ "STOP" ฉุกเฉิน (วิทยุ/แตร/ไฟ), Emergency stop ของปั๊ม/เครน,', 12, 'start', '#7f1d1d', True)
    s += txt(56, 494, 'ขีดจำกัด (draught, list, stress, air draught ใต้เครน), การแจ้งเตือนล่วงหน้าก่อนเปลี่ยนอัตรา/จบงาน (topping off) — ทวนคำสั่งทุกครั้ง', 12, 'start', '#7f1d1d')
    save('cargo-ship-shore-communication.svg', s)


# ---------------------------------------------------------------- tanker ullage
def ullage():
    w, h = 1000, 480
    s = head(w, h, 'การวัดสินค้าเหลวในถัง: Ullage, Sounding และการคำนวณปริมาณ')
    x, top, bot = 120, 90, 420
    s += rect(x, top, 260, bot - top, '#f8fafc', '#0f172a', 2.5)
    liq = 200
    s += rect(x + 2, liq, 256, bot - liq - 2, '#fde68a', '#92400e', 0)
    s += rect(x + 2, bot - 22, 256, 20, '#bae6fd', '#0369a1', 0)
    s += txt(x + 130, bot - 8, 'น้ำก้นถัง (free water)', 11, 'middle', '#075985', True)
    s += txt(x + 130, 320, 'สินค้า (น้ำมัน)', 14, 'middle', '#78350f', True)
    s += rect(x + 200, top - 20, 30, 20, '#94a3b8', '#0f172a', 1)
    s += txt(x + 215, top - 26, 'reference point', 11, 'middle')
    s += line(x + 215, top, x + 215, liq, '#b91c1c', 2, mk='arR') + line(x + 215, liq, x + 215, top, '#b91c1c', 2, mk='arR')
    s += txt(x + 270, (top + liq) / 2 + 4, 'Ullage', 13, 'start', '#b91c1c', True)
    s += line(x + 40, liq, x + 40, bot, '#1d4ed8', 2, mk='arB') + line(x + 40, bot, x + 40, liq, '#1d4ed8', 2, mk='arB')
    s += txt(x + 46, (liq + bot) / 2 - 30, 'Sounding', 13, 'start', '#1d4ed8', True)
    s += txt(x + 130, bot + 30, 'Ullage + Sounding = ความสูงอ้างอิง (reference height)', 12, 'middle')
    bx = 450
    s += rect(bx, 70, 520, 380, '#f8fafc', '#94a3b8', 1, 10)
    L = ['ลำดับคำนวณปริมาณสินค้าเหลว (หลักการทั่วไป)', '1) วัด ullage/ความลึกน้ำก้นถัง/อุณหภูมิ ทุกถัง (ระบบปิด — closed gauging)',
         '2) แก้ trim/list (ตาราง correction ของถัง) → อ่าน TOV จาก tank table', '3) TOV − free water = GOV (Gross Observed Volume)',
         '4) GOV × VCF (Volume Correction Factor จาก ASTM/API', '    Table 54 ตามอุณหภูมิและความหนาแน่น) = GSV ที่ 15°C', '5) GSV − น้ำ/ตะกอนที่ผสม (S&amp;W) = NSV',
         '6) NSV × WCF (density in air) = น้ำหนัก (metric tons in air)', '', 'เทียบตัวเลขเรือกับฝั่ง (ship/shore difference) ด้วย VEF',
         'ถ้าต่างเกินเกณฑ์ → แจ้งนายเรือ ออก Letter of Protest', '', 'ความปลอดภัย: ระวัง static electricity, H₂S, benzene,',
         'อัตราบรรทุกเริ่มต้นช้า, ระดับ alarm ล้น (high/overfill),', 'ระบบ inert gas (O₂ ในถัง ≤ 8%) — ตาม ISGOTT']
    for i, l in enumerate(L):
        s += txt(bx + 14, 96 + i * 23, l, 12.3, 'start', '#0f172a', i == 0)
    save('cargo-ullage-calculation.svg', s)


if __name__ == '__main__':
    heavy_lift(); bay_row_tier(); lashing(); imdg(); ventilation(); securing(); strength(); communication(); ullage()
