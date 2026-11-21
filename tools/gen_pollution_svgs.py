"""ภาพประกอบบท 3.1 การป้องกันมลพิษ (MARPOL และอนุสัญญาที่เกี่ยวข้อง)"""
import os
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


def annexes():
    w, h = 1000, 600
    s = head(w, h, 'MARPOL 73/78 ทั้ง 6 ภาคผนวก และอนุสัญญาด้านสิ่งแวดล้อมที่เกี่ยวข้อง')
    data = [('I', 'น้ำมัน (Oil)', '#1f2937', ['IOPP Certificate · SOPEP', 'Oil Record Book Part I/II', 'เครื่องแยกน้ำมัน ≤ 15 ppm', 'Special areas']),
            ('II', 'สารเหลวมีพิษเทกอง (NLS)', '#7c3aed', ['Category X / Y / Z / OS', 'NLS Certificate · P&amp;A Manual', 'Cargo Record Book', 'Prewash · SMPEP']),
            ('III', 'สารอันตรายในหีบห่อ', '#c2410c', ['Marine pollutants (IMDG)', 'ทำเครื่องหมาย ป้าย เอกสาร', 'จัดวางปลอดภัย', 'ห้ามทิ้งลงทะเล']),
            ('IV', 'น้ำเสีย (Sewage)', '#a16207', ['ISPP Certificate', 'Sewage treatment plant', 'ระยะ 3 / 12 nm', 'Baltic special area']),
            ('V', 'ขยะ (Garbage)', '#15803d', ['ห้ามทิ้งพลาสติกทุกที่', 'Garbage Management Plan', 'Garbage Record Book', 'Placards · special areas']),
            ('VI', 'มลพิษทางอากาศ (Air)', '#0369a1', ['SOx 0.50% / ECA 0.10%', 'NOx Tier I–III · ODS', 'BDN · IAPP · EIAPP', 'EEXI · CII · SEEMP · DCS'])]
    for i, (n, t, col, items) in enumerate(data):
        c, r = i % 3, i // 3
        x, y = 40 + c * 315, 60 + r * 220
        s += rect(x, y, 295, 200, '#ffffff', col, 2.5, 12)
        s += rect(x, y, 295, 50, col, col, 0, 12) + rect(x, y + 30, 295, 20, col, col, 0)
        s += txt(x + 18, y + 33, f'Annex {n}', 18, 'start', '#fff', True) + txt(x + 120, y + 32, t, 14, 'start', '#fff', True)
        for j, it in enumerate(items):
            s += txt(x + 18, y + 82 + j * 28, '• ' + it, 13)
    s += rect(40, 505, 920, 80, '#f8fafc', '#94a3b8', 1, 10)
    s += txt(56, 530, 'อนุสัญญาอื่น: BWM 2004 (น้ำอับเฉา D-1/D-2) · AFS 2001 (สีกันเพรียง — ห้าม TBT, cybutryne) · Hong Kong Convention (รีไซเคิลเรือ — มีผล 26 มิ.ย. 2025, IHM)', 12.5)
    s += txt(56, 552, 'OPRC 1990/OPRC-HNS (เตรียมรับมือมลพิษ) · London Convention/Protocol (การทิ้งของเสีย) · Biofouling Guidelines (MEPC.378(80)) · Polar Code (ส่วนสิ่งแวดล้อม)', 12.5)
    s += txt(56, 574, 'MARPOL Protocol I — การรายงานเหตุมลพิษ · ข้อกำหนดท้องถิ่น (เช่น EU, สหรัฐฯ, ท่าเรือ) อาจเข้มกว่า MARPOL', 12.5, 'start', '#b91c1c')
    save('pol-marpol-overview.svg', s)


def oil_discharge():
    w, h = 1000, 590
    s = head(w, h, 'MARPOL Annex I: เกณฑ์การปล่อยน้ำปนน้ำมัน (หลักทั่วไป)')
    # machinery space panel
    s += rect(40, 60, 450, 510, '#f8fafc', '#1f2937', 2, 12)
    s += txt(265, 88, 'จากห้องเครื่อง (ทุกเรือ ≥ 400 GT)', 15, 'middle', '#0f172a', True)
    # diagram bilge -> holding tank -> OWS -> OCM -> overboard
    boxes = [(60, 120, 'Bilge wells'), (60, 200, 'Bilge holding tank'), (60, 280, 'Oily water separator'), (60, 360, '15 ppm alarm (OCM)')]
    for x, y, t in boxes:
        s += rect(x, y, 170, 50, '#e2e8f0', '#1f2937', 1.5, 8) + txt(x + 85, y + 30, t, 12, 'middle', '#0f172a', True)
    for y in (170, 250, 330):
        s += line(145, y, 145, y + 28, '#0f172a', 2, mk='ar')
    s += line(230, 385, 330, 385, '#15803d', 3, mk='ar') + txt(280, 375, '≤ 15 ppm', 12, 'middle', '#15803d', True)
    s += txt(340, 390, 'ลงทะเล', 12, 'start', '#15803d', True)
    s += f'<path d="M 145 410 L 145 450 L 300 450" fill="none" stroke="#b91c1c" stroke-width="2.5" marker-end="url(#arR)"/>'
    s += txt(160, 470, '&gt; 15 ppm → หยุดปล่อยอัตโนมัติ / ส่งกลับ', 12, 'start', '#b91c1c', True)
    s += txt(250, 230, 'Sludge tank → incinerator', 11.5, 'start', '#334155')
    s += txt(250, 246, 'หรือส่งท่า (reception facility)', 11.5, 'start', '#334155')
    cond = ['เงื่อนไข: เรือกำลังเดินทาง (en route) · ผ่านอุปกรณ์กรองที่รับรอง', 'ไม่เจือจาง · ไม่มาจาก cargo pump room/ปนกากสินค้าของ tanker', 'alarm + หยุดอัตโนมัติ (บังคับชัดเจนเมื่อ ≥ 10,000 GT — Reg. 14)', 'ห้ามใน Antarctic area และ Arctic (Polar Code) · บันทึก ORB Part I']
    for i, c in enumerate(cond):
        s += txt(56, 494 + i * 18, c, 11.5, 'start', '#334155')
    # cargo area panel
    s += rect(510, 60, 450, 510, '#fffbeb', '#a16207', 2, 12)
    s += txt(735, 88, 'จากส่วนสินค้าของเรือ tanker (cargo area)', 15, 'middle', '#78350f', True)
    crit = ['ไม่อยู่ใน special area', 'ห่างฝั่งที่ใกล้ที่สุดมากกว่า 50 ไมล์ทะเล', 'เรือกำลังเดินทาง (en route)',
            'อัตราปล่อยทันที ≤ 30 ลิตรต่อไมล์ทะเล', 'ปริมาณรวม ≤ 1/30,000 ของสินค้าที่บรรทุก', '(tanker ส่งมอบหลัง 31 ธ.ค. 1979)',
            'ระบบ ODMCS (oil discharge monitoring', 'and control system) ทำงาน', 'มี slop tank ตามที่กำหนด', 'บันทึก Oil Record Book Part II']
    for i, c in enumerate(crit):
        s += txt(540, 130 + i * 30, ('✔ ' if not c.startswith('(') and not c.startswith('and') else '   ') + c, 13)
    s += txt(735, 470, 'ต้องครบทุกข้อพร้อมกัน — ไม่ครบข้อใดข้อหนึ่ง = ห้ามปล่อย', 12.5, 'middle', '#b91c1c', True)
    s += txt(735, 492, 'น้ำอับเฉาสะอาด/แยก (clean/segregated ballast) มีเกณฑ์ต่างหาก', 11.5, 'middle', '#475569')
    s += txt(735, 510, 'ข้อกำหนดท้องถิ่นอาจเข้มกว่า — ตรวจก่อนเสมอ', 11.5, 'middle', '#475569')
    save('pol-oil-discharge.svg', s)


def garbage():
    w, h = 1000, 600
    s = head(w, h, 'MARPOL Annex V: การทิ้งขยะลงทะเล (สรุประยะห่างจากฝั่งที่ใกล้ที่สุด)')
    # distance bands
    x0, x1, y0 = 470, 960, 70

    def DX(d):  # แกนระยะแบบไม่เชิงเส้น (ขยายช่วงใกล้ฝั่งให้อ่านง่าย) — ไม่ใช่มาตราส่วนจริง
        if d <= 3:
            return x0 + d / 3 * 50
        if d <= 12:
            return x0 + 50 + (d - 3) / 9 * 100
        return x0 + 150 + (min(d, 100) - 12) / 88 * 190
    bands = [(0, 3, '#fecaca'), (3, 12, '#fde68a')]
    for a, b, col in bands:
        s += rect(DX(a), y0, DX(b) - DX(a), 34, col, '#94a3b8', 1)
    s += rect(DX(12), y0, x1 - DX(12), 34, '#bbf7d0', '#94a3b8', 1)
    for d, lab in ((0, '0 nm'), (3, '3 nm'), (12, '12 nm'), (100, '100 nm')):
        X = DX(d)
        s += line(X, y0 + 34, X, y0 + 44, '#0f172a', 1.5) + txt(X, y0 + 58, lab, 12, 'middle', '#0f172a', True)
    s += txt(x1, y0 + 58, 'ทะเลเปิด →', 12, 'end', '#0f172a', True)
    s += txt(x0 - 10, y0 + 22, 'ระยะจากฝั่งที่ใกล้ที่สุด (ไม่ตามมาตราส่วน)', 12, 'end', '#0f172a', True)
    rows = [('พลาสติกทุกชนิด (รวมเชือก อวน ถุง ขี้เถ้าพลาสติก)', None, None, '#b91c1c', 'ห้ามทุกที่'),
            ('เศษอาหาร บดหรือย่อย ≤ 25 mm', 3, None, '#15803d', '&gt; 3 nm (special area &gt; 12 nm)'),
            ('เศษอาหาร ไม่บด', 12, None, '#15803d', '&gt; 12 nm (ห้ามใน special area)'),
            ('กากสินค้า (ไม่ใช่ HME) ที่เก็บด้วยวิธีปกติไม่ได้', 12, None, '#15803d', '&gt; 12 nm (special area เงื่อนไขเข้มกว่า)'),
            ('สารทำความสะอาดในน้ำล้างระวาง (ไม่เป็น HME)', 12, None, '#15803d', 'ตามเงื่อนไขกากสินค้าในน้ำล้าง (น้ำล้างดาดฟ้า: ได้)'),
            ('ซากสัตว์ (animal carcasses)', 100, None, '#a16207', '&gt; 100 nm ในน้ำลึกที่สุด (ห้ามใน special area)'),
            ('ขยะครัวเรือน ขี้เถ้าเตาเผา น้ำมันทำอาหาร ขยะปฏิบัติการ', None, None, '#b91c1c', 'ห้ามทิ้ง → ส่งท่า/เผา (ตามข้อกำหนด)'),
            ('ขยะอิเล็กทรอนิกส์ (E-waste), เครื่องมือประมง', None, None, '#b91c1c', 'ห้ามทิ้ง (เว้นกรณีฉุกเฉิน/ข้อยกเว้นที่กำหนด)')]
    for i, (t, d, _, col, note) in enumerate(rows):
        y = 130 + i * 44
        s += txt(40, y + 20, t, 12.5, 'start', '#0f172a', True)
        if d is None:
            s += rect(x0, y + 4, x1 - x0, 24, '#fee2e2', '#b91c1c', 1, 6)
        else:
            X = DX(d)
            s += rect(X, y + 4, x1 - X, 24, '#dcfce7' if col == '#15803d' else '#fef3c7', col, 1, 6)
        if d == 100:  # แถบสั้น — วางคำอธิบายไว้หน้าแถบ
            s += txt(DX(d) - 8, y + 21, note, 11.5, 'end', col, True)
        else:
            s += txt(x1 - 8, y + 21, note, 11.5, 'end', col, True)
    s += rect(40, 490, 920, 95, '#f8fafc', '#94a3b8', 1, 10)
    notes = ['Special areas (Annex V): Mediterranean, Baltic, Black Sea, Red Sea, Gulfs area, North Sea, Antarctic area, Wider Caribbean region',
             'ข้อยกเว้น: ความปลอดภัยของเรือ/ชีวิต, ความเสียหายของเรือ/อุปกรณ์ (มีมาตรการป้องกันแล้ว), การสูญหายของเครื่องมือประมงโดยอุบัติเหตุ',
             'แถบสีในภาพแสดงบริเวณที่อนุญาต (เมื่อเรือกำลังเดินทาง) — รายละเอียดเงื่อนไขดู MARPOL Annex V และ 2017 Guidelines (MEPC.295(71))',
             'ทุกการทิ้ง/ส่งท่า/เผา ต้องบันทึกใน Garbage Record Book: วันที่ เวลา ตำแหน่ง ประเภท (A–K) ปริมาณ (m³) วิธี']
    for i, n in enumerate(notes):
        s += txt(56, 514 + i * 20, n, 11.8)
    save('pol-garbage-discharge.svg', s)


def sulphur():
    w, h = 1000, 500
    s = head(w, h, 'MARPOL Annex VI: ขีดจำกัดกำมะถันในน้ำมันเชื้อเพลิง และ NOx Tier')
    gx, gy, gw, gh = 90, 80, 520, 300
    years = list(range(2008, 2029))
    def X(yr): return gx + (yr - 2008) / 20 * gw
    def Y(v): return gy + gh - v / 5.0 * gh
    s += line(gx, gy + gh, gx + gw, gy + gh, '#0f172a', 1.5) + line(gx, gy, gx, gy + gh, '#0f172a', 1.5)
    for v in (0, 1, 2, 3, 4, 5):
        s += line(gx - 5, Y(v), gx, Y(v), '#0f172a', 1) + txt(gx - 8, Y(v) + 4, f'{v:.1f}', 11, 'end') + line(gx, Y(v), gx + gw, Y(v), '#f1f5f9', 1)
    for yr in (2008, 2012, 2015, 2020, 2025, 2028):
        s += line(X(yr), gy + gh, X(yr), gy + gh + 5, '#0f172a', 1) + txt(X(yr), gy + gh + 20, str(yr), 11, 'middle')
    s += f'<text x="{gx-48}" y="{gy+gh/2}" font-size="12" text-anchor="middle" transform="rotate(-90 {gx-48} {gy+gh/2})">กำมะถัน % m/m</text>'
    glob = [(2008, 4.5), (2012, 4.5), (2012, 3.5), (2020, 3.5), (2020, 0.5), (2028, 0.5)]
    eca = [(2008, 1.5), (2010.5, 1.5), (2010.5, 1.0), (2015, 1.0), (2015, 0.1), (2028, 0.1)]
    s += '<polyline points="' + ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in glob) + '" fill="none" stroke="#b91c1c" stroke-width="3.5"/>'
    s += '<polyline points="' + ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in eca) + '" fill="none" stroke="#1d4ed8" stroke-width="3.5"/>'
    s += txt(X(2009), Y(4.5) - 8, 'ทั่วโลก 4.50%', 12, 'start', '#b91c1c', True)
    s += txt(X(2013), Y(3.5) - 8, '3.50% (2012)', 12, 'start', '#b91c1c', True)
    s += txt(X(2020) + 6, Y(0.5) - 10, '0.50% (1 ม.ค. 2020)', 12, 'start', '#b91c1c', True)
    s += txt(X(2009), Y(1.5) - 8, 'ECA 1.50 → 1.00%', 12, 'start', '#1d4ed8', True)
    s += txt(X(2015) + 6, Y(0.1) - 8, 'ECA 0.10% (1 ม.ค. 2015)', 12, 'start', '#1d4ed8', True)
    bx = 640
    s += rect(bx, 60, 330, 420, '#f8fafc', '#94a3b8', 1, 10)
    L = ['SOx ECA (0.10% m/m) — วันที่ใช้ขีดจำกัด', '• Baltic · North Sea (2015) · North American', '  · US Caribbean (2015)', '• Mediterranean (1 พ.ค. 2025)',
         '• Canadian Arctic · Norwegian Sea (1 มี.ค. 2027)', '• North-East Atlantic (1 ก.ย. 2028) — รับรองแล้ว', '  ตรวจรายการ/เส้นเขตล่าสุดก่อนเดินทาง', '',
         'NOx (Reg. 13) — เครื่องดีเซล &gt; 130 kW', '• Tier I (2000) · Tier II (2011) ทั่วโลก', '• Tier III ใน NOx ECA ตามวันสร้างเรือ:',
         '  N. American/US Caribbean 2016 · Baltic/', '  North Sea 2021 · Canadian Arctic 2025 ·', '  Norwegian Sea 2026 · NE Atlantic 2027', '',
         'ห้ามบรรทุกเชื้อเพลิง &gt; 0.50% เพื่อใช้ (ไม่มี', 'EGCS/scrubber) ตั้งแต่ 1 มี.ค. 2020 · เปลี่ยนน้ำมัน', 'ก่อนเข้า ECA: บันทึกเวลา ตำแหน่ง ปริมาณ']
    for i, l in enumerate(L):
        s += txt(bx + 12, 82 + i * 21.5, l, 11.8, 'start', '#0f172a', l in (L[0], L[8]))
    save('pol-sulphur-nox.svg', s)


def bunkering():
    w, h = 1000, 560
    s = head(w, h, 'การป้องกันมลพิษระหว่างรับน้ำมันเชื้อเพลิง (Bunkering)')
    # ship deck sketch
    s += rect(40, 250, 560, 160, '#e2e8f0', '#0f172a', 2, 10)
    s += txt(420, 400, 'ดาดฟ้าเรือ (main deck)', 12, 'middle', '#334155')
    s += rect(120, 310, 80, 50, '#fef3c7', '#a16207', 1.5, 6) + txt(160, 340, 'Manifold', 11.5, 'middle', '#78350f', True)
    s += rect(100, 360, 120, 18, '#fde68a', '#a16207', 1) + txt(160, 373, 'save-all / drip tray', 10, 'middle', '#78350f')
    s += f'<path d="M 240 470 Q 250 380 201 335" fill="none" stroke="#1f2937" stroke-width="6"/>'
    for xs in (60, 300, 560):
        s += f'<circle cx="{xs}" cy="402" r="8" fill="#0f172a"/>'
    s += txt(440, 435, '● = scupper plugs ปิดทุกจุด', 12, 'middle', '#0f172a', True)
    s += rect(400, 280, 150, 80, '#f1f5f9', '#0f172a', 1.5, 6) + txt(475, 312, 'SOPEP locker', 12, 'middle', '#0f172a', True) + txt(475, 330, 'sorbents · ปั๊มมือ', 10.5, 'middle') + txt(475, 345, 'ถังเปล่า · ทราย/ขี้เลื่อย', 10.5, 'middle')
    # barge
    s += f'<path d="M 40 470 L 600 470 L 580 520 L 60 520 Z" fill="#cbd5e1" stroke="#0f172a" stroke-width="2"/>'
    s += txt(320, 502, 'เรือส่งน้ำมัน (bunker barge)', 12, 'middle', '#0f172a', True)
    s += txt(256, 450, 'สายส่ง (bunker hose)', 11, 'start')
    # tank & vent
    s += rect(250, 120, 160, 110, '#fff', '#0f172a', 2, 4)
    s += rect(252, 150, 156, 78, '#1f2937', '#1f2937', 0)
    s += txt(290, 112, 'ถังน้ำมัน', 12, 'middle', '#0f172a', True)
    s += line(250, 138, 410, 138, '#b91c1c', 1.5, '6 4') + txt(415, 142, 'สูงสุด ≈ 85–90%', 11, 'start', '#b91c1c', True)
    s += line(330, 120, 330, 80, '#0f172a', 3) + f'<path d="M 318 80 L 342 80 L 330 64 Z" fill="#0f172a"/>' + txt(350, 78, 'ท่อระบาย (vent) + save-all', 11, 'start')
    s += f'<path d="M 160 310 L 160 250 L 250 200" fill="none" stroke="#1f2937" stroke-width="3" marker-end="url(#ar)"/>'
    # checklist
    bx = 620
    s += rect(bx, 60, 350, 480, '#f8fafc', '#94a3b8', 1, 10)
    C = ['ก่อนเริ่ม', '• ประชุม/checklist กับ barge — ชนิด ปริมาณ', '  อัตรา ความดัน ลำดับถัง สัญญาณหยุด', '• วัด sounding/ullage ทุกถังก่อนเริ่ม',
         '• ปิด scupper plugs, save-all ว่าง', '• SOPEP พร้อม, ไฟ/ป้ายห้ามสูบบุหรี่ ธง B/ไฟแดง', '• วาล์วถูกต้อง ท่อที่ไม่ใช้ปิด blank',
         '• สื่อสารทดสอบแล้ว (วิทยุ/โทรศัพท์)', '', 'ระหว่าง', '• เริ่มช้า ตรวจว่าน้ำมันเข้าถังที่ถูก', '• มีคนเฝ้า manifold และวัดถังตลอด',
         '• ลดอัตราเมื่อใกล้เต็ม (topping off)', '• ตรวจรั่ว สายส่ง หน้าแปลน รอบ ๆ เรือ', '', 'หลังเสร็จ',
         '• Drain สาย ปิดวาล์ว วัดถัง เทียบ BDN', '• เก็บตัวอย่าง MARPOL sample', '• บันทึก ORB Part I และ logbook', '• ถ้าต่าง/มีปัญหา → Letter of Protest']
    for i, c in enumerate(C):
        s += txt(bx + 14, 84 + i * 22.5, c, 12, 'start', '#1d4ed8' if c in ('ก่อนเริ่ม', 'ระหว่าง', 'หลังเสร็จ') else '#0f172a', c in ('ก่อนเริ่ม', 'ระหว่าง', 'หลังเสร็จ'))
    save('pol-bunkering.svg', s)


def spill():
    w, h = 1000, 540
    s = head(w, h, 'การรับมือเมื่อน้ำมันรั่วไหลบนเรือ (ตาม SOPEP — ลำดับทั่วไป)')
    steps = [('1. หยุดต้นเหตุ', 'หยุดปั๊ม/การถ่ายเท ปิดวาล์ว\nกด emergency stop แจ้ง barge/ท่า', '#b91c1c'),
             ('2. แจ้งเตือน', 'สัญญาณ/ประกาศ แจ้ง OOW → นายเรือ\nต้นเรือ ต้นกล', '#b91c1c'),
             ('3. ความปลอดภัย', 'ห้ามสูบบุหรี่/ประกายไฟ ระบายอากาศ\nป้องกันไฟไหม้ PPE', '#c2410c'),
             ('4. กักเก็บบนเรือ', 'scupper plugs, sorbents, ทราย\nสูบเข้าถังว่าง/ถัง slop', '#c2410c'),
             ('5. รายงาน', 'รัฐชายฝั่ง/ท่า ตาม SOPEP (Protocol I)\nบริษัท (DPA) P&amp;I ตัวแทน', '#1d4ed8'),
             ('6. ถ้าหลุดลงทะเล', 'ประสานหน่วยงานรับมือฝั่ง\nห้ามใช้สารกระจายคราบน้ำมันเอง\nถ้าไม่ได้รับอนุญาต', '#1d4ed8'),
             ('7. บันทึก', 'เวลา ตำแหน่ง ปริมาณ การกระทำ\nORB, logbook, ภาพถ่าย', '#15803d'),
             ('8. ทบทวน', 'สอบสวนสาเหตุ แก้ไข SMS\nเติมอุปกรณ์ SOPEP', '#15803d')]
    for i, (t, d, col) in enumerate(steps):
        c, r = i % 4, i // 4
        x, y = 30 + c * 240, 70 + r * 210
        s += rect(x, y, 220, 170, '#fff', col, 2.5, 12)
        s += rect(x, y, 220, 40, col, col, 0, 12) + rect(x, y + 25, 220, 15, col, col, 0)
        s += txt(x + 110, y + 27, t, 15, 'middle', '#fff', True)
        for j, part in enumerate(d.split('\n')):
            s += txt(x + 110, y + 75 + j * 24, part, 12, 'middle')
        if c < 3:
            s += line(x + 222, y + 85, x + 238, y + 85, '#0f172a', 2, mk='ar')
    s += txt(500, 515, 'หลายขั้นทำพร้อมกันโดยทีม — ปฏิบัติตาม SOPEP/SMPEP ของเรือ ซึ่งมีรายชื่อผู้ติดต่อของรัฐชายฝั่ง (Appendix) และแผนผังระบบน้ำมัน', 12, 'middle', '#334155')
    save('pol-spill-response.svg', s)


def ballast_water():
    w, h = 1000, 480
    s = head(w, h, 'Ballast Water Management (BWM Convention): D-1 exchange กับ D-2 standard')
    # D-1 diagram coast distances
    s += rect(40, 60, 450, 380, '#f0f9ff', '#0369a1', 2, 12)
    s += txt(265, 88, 'D-1 Ballast water exchange (เดิม)', 15, 'middle', '#075985', True)
    s += f'<path d="M 60 120 L 60 400 L 100 400 Q 90 260 100 120 Z" fill="#d6d3d1" stroke="#57534e"/>'
    s += txt(80, 115, 'ฝั่ง', 11, 'middle', '#44403c', True)
    for xx, lab, col in ((210, '50 nm', '#ca8a04'), (380, '200 nm', '#15803d')):
        s += line(xx, 120, xx, 400, col, 2, '6 4') + txt(xx, 418, lab, 12, 'middle', col, True)
    s += rect(385, 200, 95, 90, '#dcfce7', '#15803d', 1.5, 8) + txt(432, 230, 'ดีที่สุด', 12, 'middle', '#14532d', True) + txt(432, 248, '≥ 200 nm', 11, 'middle') + txt(432, 264, 'ลึก ≥ 200 m', 11, 'middle')
    s += rect(215, 200, 160, 90, '#fef9c3', '#ca8a04', 1.5, 8) + txt(295, 230, 'ถ้าทำไม่ได้', 12, 'middle', '#713f12', True) + txt(295, 248, '≥ 50 nm และ', 11, 'middle') + txt(295, 264, 'ลึก ≥ 200 m', 11, 'middle')
    s += rect(112, 305, 368, 66, '#ffffff', '#bae6fd', 1, 6)
    s += txt(296, 323, 'ประสิทธิภาพ ≥ 95% ปริมาตร (sequential)', 12, 'middle')
    s += txt(296, 341, 'หรือสูบผ่าน 3 เท่าของปริมาตรถัง (flow-through)', 12, 'middle')
    s += txt(296, 361, 'ไม่ต้องเบี่ยงเส้นทาง/ไม่ทำเมื่อไม่ปลอดภัย (B-4)', 11.5, 'middle', '#475569')
    # D-2
    s += rect(510, 60, 450, 380, '#f0fdf4', '#15803d', 2, 12)
    s += txt(735, 88, 'D-2 Performance standard (ปัจจุบัน)', 15, 'middle', '#14532d', True)
    L = ['เรือทุกลำต้องเป็นไปตาม D-2 แล้ว (ช่วงเปลี่ยนผ่าน', 'สิ้นสุด 8 ก.ย. 2024) → ใช้ Ballast Water', 'Management System (BWMS) ที่ได้รับการรับรอง',
         '', 'น้ำที่ปล่อยต้องมีสิ่งมีชีวิตไม่เกินเกณฑ์:', '• ขนาด ≥ 50 µm: &lt; 10 ตัวต่อ m³', '• ขนาด 10–50 µm: &lt; 10 ตัวต่อ mL',
         '• แบคทีเรียตัวชี้วัด (V. cholerae &lt; 1 cfu/100 mL,', '  E. coli &lt; 250, enterococci &lt; 100 cfu/100 mL)', '', 'เอกสาร: BWM Plan · BWRB (แบบใหม่ 1 ก.พ. 2025)',
         '· International BWM Certificate', 'OOW: ตำแหน่ง/เวลา/ปริมาณ ทุกการรับ-ปล่อย', 'และติดตามข้อกำหนดท้องถิ่น (เช่น สหรัฐฯ)']
    for i, l in enumerate(L):
        s += txt(530, 118 + i * 22, l, 12.3, 'start', '#0f172a', l.startswith('เอกสาร'))
    s += txt(500, 465, 'ภาพแสดงหลักการ — รายละเอียดและข้อยกเว้นดู BWM Convention, Guidelines G1–G14 และข้อกำหนดของรัฐเจ้าท่า', 11.5, 'middle', '#475569')
    save('pol-ballast-water.svg', s)


if __name__ == '__main__':
    annexes(); oil_discharge(); garbage(); sulphur(); bunkering(); spill(); ballast_water()
