"""ภาพประกอบบท 3.6 ข้อกำหนดทางกฎหมาย (Legislative requirements)"""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"


def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker></defs>\n'
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


def zones():
    w, h = 1000, 520
    s = head(w, h, 'เขตทางทะเลตาม UNCLOS 1982 (Maritime zones)')
    s += '<path d="M 40 80 L 160 80 L 160 300 L 40 300 Z" fill="#d6d3d1" stroke="#57534e"/>'
    s += txt(100, 190, 'แผ่นดิน', 14, 'middle', '#44403c', True)
    bands = [(160, 250, '#bae6fd', 'น่านน้ำภายใน', '(internal)'), (250, 390, '#93c5fd', 'ทะเลอาณาเขต', '12 nm'),
             (390, 500, '#bfdbfe', 'เขตต่อเนื่อง', '24 nm'), (500, 820, '#dbeafe', 'เขตเศรษฐกิจจำเพาะ (EEZ)', '200 nm'), (820, 960, '#f1f5f9', 'ทะเลหลวง', '(high seas)')]
    for x0, x1, col, t1, t2 in bands:
        s += rect(x0, 80, x1 - x0, 220, col, '#64748b', 1)
        s += txt((x0 + x1) / 2, 180, t1, 12.5, 'middle', '#0f172a', True) + txt((x0 + x1) / 2, 200, t2, 11.5, 'middle', '#334155')
    s += line(250, 70, 250, 310, '#b91c1c', 2.5) + txt(250, 64, 'เส้นฐาน (baseline)', 11.5, 'middle', '#b91c1c', True)
    s += f'<path d="M 160 300 L 160 330 Q 500 350 820 360 L 900 450 L 960 460" fill="none" stroke="#78350f" stroke-width="3"/>'
    s += txt(560, 375, 'ไหล่ทวีป (continental shelf) — สิทธิ์ทรัพยากรใต้ท้องทะเล', 11.5, 'middle', '#78350f', True)
    s += rect(40, 395, 920, 115, '#f8fafc', '#94a3b8', 1, 10)
    L = ['ทะเลอาณาเขต: อำนาจอธิปไตยของรัฐชายฝั่ง — เรือต่างชาติมีสิทธิ์ผ่านโดยสุจริต (innocent passage) แต่ต้องเคารพกฎของรัฐ (TSS, รายงาน)',
         'เขตต่อเนื่อง: รัฐควบคุมเพื่อป้องกัน/ลงโทษการละเมิดกฎศุลกากร การคลัง เข้าเมือง สุขอนามัย · EEZ: สิทธิ์ทรัพยากร และเขตอำนาจด้านสิ่งแวดล้อมบางประการ',
         'ช่องแคบที่ใช้เดินเรือระหว่างประเทศ: transit passage · รัฐหมู่เกาะ: archipelagic sea lanes passage · ทะเลหลวง: เสรีภาพการเดินเรือ อยู่ใต้อำนาจรัฐเจ้าของธง',
         'ระยะทั้งหมดวัดจากเส้นฐาน — รัฐเจ้าของธงต้องดูแลเรือของตน (Art. 94) · รัฐเจ้าท่ามีอำนาจตรวจเรือในท่า (port State control)']
    for i, l in enumerate(L):
        s += txt(56, 420 + i * 25, l, 11.8)
    save('legal-maritime-zones.svg', s)


def imo():
    w, h = 1000, 540
    s = head(w, h, 'โครงสร้าง IMO และการเกิดผลบังคับของอนุสัญญา')
    s += rect(400, 55, 200, 50, '#1d4ed8', '#1d4ed8', 0, 10) + txt(500, 86, 'Assembly (สมัชชา)', 14, 'middle', '#fff', True)
    s += rect(400, 125, 200, 45, '#3b82f6', '#3b82f6', 0, 10) + txt(500, 153, 'Council (คณะมนตรี)', 13, 'middle', '#fff', True)
    s += line(500, 105, 500, 125, '#0f172a', 2)
    comms = [('MSC', 'ความปลอดภัย'), ('MEPC', 'สิ่งแวดล้อม'), ('LEG', 'กฎหมาย'), ('TCC', 'ความร่วมมือทางวิชาการ'), ('FAL', 'อำนวยความสะดวก')]
    for i, (c, t) in enumerate(comms):
        x = 70 + i * 180
        s += rect(x, 200, 160, 54, '#eff6ff', '#1d4ed8', 1.5, 10) + txt(x + 80, 222, c, 14, 'middle', '#1e3a8a', True) + txt(x + 80, 242, t, 11, 'middle')
        s += line(500, 170, x + 80, 200, '#94a3b8', 1.5)
    s += txt(500, 280, 'Sub-committees (เช่น NCSR, SDC, SSE, PPR, HTW, III, CCC) — งานวิชาการรายละเอียด · Secretariat (Secretary-General)', 12, 'middle', '#334155')
    steps = ['เสนอ/ร่าง|ในคณะกรรมการ', 'รับรอง|(adoption)', 'ให้สัตยาบัน/|ภาคยานุวัติ', 'มีผลบังคับ|(entry into force)', 'รัฐออก|กฎหมายภายใน', 'บังคับใช้: Flag|Port · Coastal State']
    for i, t in enumerate(steps):
        x = 30 + i * 160
        s += rect(x, 320, 145, 60, '#f0fdf4', '#15803d', 1.5, 10)
        for j, part in enumerate(t.split('|')):
            s += txt(x + 72, 345 + j * 18, part, 11, 'middle', '#14532d', j == 0)
        if i < 5:
            s += line(x + 146, 350, x + 158, 350, '#0f172a', 2, mk='ar')
    s += rect(30, 400, 940, 125, '#f8fafc', '#94a3b8', 1, 10)
    L = ['Tacit acceptance — การแก้ไขภาคผนวก/บททางเทคนิคมีผลตามวันที่กำหนด เว้นแต่รัฐคัดค้านถึงเกณฑ์ (ทำให้ SOLAS/MARPOL ทันสมัยเร็ว)',
         'ตราสาร: อนุสัญญา (convention) · พิธีสาร (protocol) · ประมวล (code — บังคับเมื่ออ้างในอนุสัญญา เช่น ISM, ISPS, IMDG, FSS, LSA)',
         'ข้อมติ (resolution — A. ของ Assembly, MSC., MEPC.) · หนังสือเวียน (circular — MSC.1/Circ., MEPC.1/Circ.) มักเป็นแนวทาง (guidelines)',
         'ILO รับผิดชอบมาตรฐานแรงงาน (MLC 2006) · IMO Member State Audit Scheme (บังคับ) ตรวจการปฏิบัติตามของรัฐภาคี (III Code)']
    for i, l in enumerate(L):
        s += txt(46, 426 + i * 26, l, 12)
    save('legal-imo-structure.svg', s)


def solas():
    w, h = 1000, 520
    s = head(w, h, 'SOLAS 1974 (as amended) — บทต่าง ๆ')
    ch = [('I', 'บททั่วไป การสำรวจและใบรับรอง'), ('II-1', 'โครงสร้าง การแบ่งช่อง เสถียรภาพ เครื่องจักร ไฟฟ้า'), ('II-2', 'การป้องกัน ตรวจจับ ดับไฟ'),
          ('III', 'อุปกรณ์และการจัดการช่วยชีวิต'), ('IV', 'การสื่อสารทางวิทยุ (GMDSS)'), ('V', 'ความปลอดภัยในการเดินเรือ'), ('VI', 'การบรรทุกสินค้าและน้ำมันเชื้อเพลิง'),
          ('VII', 'การบรรทุกสินค้าอันตราย'), ('VIII', 'เรือนิวเคลียร์'), ('IX', 'การจัดการเพื่อความปลอดภัย (ISM Code)'), ('X', 'เรือความเร็วสูง (HSC Code)'),
          ('XI-1', 'มาตรการพิเศษ: RO, ESP, IMO number, CSR, PSC'), ('XI-2', 'มาตรการพิเศษด้านการรักษาความปลอดภัย (ISPS)'), ('XII', 'มาตรการเพิ่มเติมสำหรับ bulk carrier'),
          ('XIII', 'การตรวจสอบการปฏิบัติตาม (IMSAS)'), ('XIV', 'เรือในน่านน้ำขั้วโลก (Polar Code)'), ('XV', 'การขนส่งบุคลากรอุตสาหกรรม (IP Code)')]
    for i, (c, t) in enumerate(ch):
        col, row = i % 2, i // 2
        x, y = 40 + col * 470, 55 + row * 49
        s += rect(x, y, 70, 40, '#1d4ed8', '#1d4ed8', 0, 8) + txt(x + 35, y + 26, c, 14, 'middle', '#fff', True)
        s += rect(x + 76, y, 374, 40, '#eff6ff', '#bfdbfe', 1, 8) + txt(x + 88, y + 25, t, 12.5)
    s += txt(500, 510, 'เรือต้องมีใบรับรองตาม SOLAS บทที่ I และอยู่ใต้การตรวจของรัฐเจ้าของธง/RO และรัฐเจ้าท่า — ติดตามการแก้ไขที่มีผลบังคับล่าสุดเสมอ', 12, 'middle', '#334155')
    save('legal-solas-chapters.svg', s)


def certificates():
    w, h = 1000, 680
    s = head(w, h, 'ใบรับรองและเอกสารสำคัญของเรือสินค้า (ตัวอย่าง — ตรวจรายการเต็มตาม FAL/รัฐเจ้าของธง)')
    rows = [('Certificate of Registry', 'ทะเบียนเรือ/สัญชาติ', 'ตามรัฐเจ้าของธง'),
            ('International Tonnage Certificate (1969)', 'GT/NT', 'ไม่มีวันหมดอายุ (เว้นดัดแปลง)'),
            ('International Load Line Certificate', 'Load Line Convention', '5 ปี + annual survey'),
            ('Cargo Ship Safety Construction / Equipment / Radio', 'SOLAS', '5 ปี (Radio มี periodical)'),
            ('IOPP · ISPP · IAPP · IEE', 'MARPOL I, IV, VI', '5 ปี (IEE ตลอดอายุเรือ)'),
            ('International BWM Certificate', 'BWM Convention', '5 ปี'),
            ('International Anti-fouling System Certificate', 'AFS', 'ตามการเปลี่ยนระบบสี'),
            ('Safety Management Certificate (SMC) + copy of DOC', 'ISM Code', '5 ปี (intermediate audit)'),
            ('International Ship Security Certificate (ISSC)', 'ISPS Code', '5 ปี (intermediate verification)'),
            ('Maritime Labour Certificate + DMLC I/II', 'MLC 2006', '5 ปี (intermediate inspection)'),
            ('Minimum Safe Manning Document', 'SOLAS V/14', 'ตามรัฐเจ้าของธง'),
            ('Continuous Synopsis Record (CSR)', 'SOLAS XI-1/5', 'บันทึกประวัติต่อเนื่อง'),
            ('ประกันภัยตามอนุสัญญา (CLC · Bunkers · Wreck Removal)', 'ความรับผิดทางแพ่ง', 'ตามระยะประกัน'),
            ('DOC for Dangerous Goods · Certificate of Fitness · Grain', 'SOLAS II-2/19 · IBC/IGC · Grain', 'ตามชนิดเรือ'),
            ('ใบประกาศนียบัตรลูกเรือ (CoC, CoP, endorsement, medical)', 'STCW · MLC', 'ตามใบแต่ละใบ'),
            ('International Certificate on Inventory of Hazardous Materials (IHM)', 'Hong Kong Conv. (26 มิ.ย. 2025)', '≤ 5 ปี (เรือ ≥ 500 GT)')]
    s += rect(30, 50, 940, 30, '#1e3a8a', '#1e3a8a', 0, 6)
    s += txt(46, 70, 'ใบรับรอง/เอกสาร', 12.5, 'start', '#fff', True) + txt(560, 70, 'ตามกฎ', 12.5, 'start', '#fff', True) + txt(770, 70, 'อายุ/การตรวจ (ทั่วไป)', 12.5, 'start', '#fff', True)
    for i, (a, b, c) in enumerate(rows):
        y = 84 + i * 34
        s += rect(30, y, 940, 32, '#f8fafc' if i % 2 else '#eef2ff', '#e2e8f0', 1, 4)
        s += txt(46, y + 21, a, 12) + txt(560, y + 21, b, 11.5, 'start', '#334155') + txt(770, y + 21, c, 11.5, 'start', '#334155')
    s += txt(500, 650, 'บันทึก (logs): Official log, deck/engine log, ORB, GRB, BWRB, Cargo Record Book, GMDSS log, hours of rest — เป็นเอกสารทางกฎหมาย', 12, 'middle', '#b91c1c')
    s += txt(500, 670, 'ใช้ระบบการสำรวจและออกใบรับรองที่ประสานกัน (HSSC) — annual window ± 3 เดือนจากวันครบรอบ', 11.5, 'middle', '#475569')
    save('legal-certificates.svg', s)


def hssc():
    w, h = 1000, 360
    s = head(w, h, 'รอบการสำรวจแบบประสาน (HSSC) ของใบรับรองอายุ 5 ปี — ตัวอย่างแนวคิด')
    x0, x1, y = 80, 920, 170
    s += line(x0, y, x1, y, '#0f172a', 3)
    for k in range(6):
        X = x0 + k * (x1 - x0) / 5
        s += line(X, y - 12, X, y + 12, '#0f172a', 2) + txt(X, y + 34, f'ปีที่ {k}', 12, 'middle', '#0f172a', True)
        if 0 < k < 5:
            s += rect(X - 28, y - 48, 56, 22, '#bfdbfe', '#1d4ed8', 1, 4) + txt(X, y - 33, '±3 ด.', 10.5, 'middle', '#1e3a8a', True)
            lab = 'Annual' if k not in (2, 3) else 'Annual หรือ Intermediate'
            s += txt(X, y - 58, lab, 11, 'middle', '#1e3a8a')
    s += rect(x0 - 30, y - 50, 60, 24, '#bbf7d0', '#15803d', 1, 4) + txt(x0, y - 34, 'Initial', 11, 'middle', '#14532d', True)
    s += rect(x1 - 70, y - 50, 70, 24, '#fecaca', '#b91c1c', 1, 4) + txt(x1 - 35, y - 34, 'Renewal', 11, 'middle', '#7f1d1d', True)
    s += txt(500, 250, 'Intermediate survey: ภายใน ±3 เดือนของวันครบรอบปีที่ 2 หรือ 3 (แทน annual ครั้งนั้น) · Renewal: ภายใน 3 เดือนก่อนหมดอายุ (ใบใหม่นับต่อจากวันหมดอายุเดิม)', 11.8, 'middle')
    s += txt(500, 274, 'ISM/ISPS/MLC ใช้รอบ audit/inspection คล้ายกัน (intermediate ระหว่างปีที่ 2–3) · Bottom inspection 2 ครั้งในรอบ 5 ปี', 11.8, 'middle')
    s += txt(500, 310, 'การสำรวจแต่ละครั้งต้องสลักหลัง (endorse) ในใบรับรอง — OOW ช่วยเตรียมอุปกรณ์/สาธิตการทำงานให้ surveyor', 11.8, 'middle', '#475569')
    save('legal-hssc-survey-cycle.svg', s)


def ism():
    w, h = 1000, 545
    s = head(w, h, 'ISM Code — ระบบการจัดการความปลอดภัย (SMS)')
    import math
    cx, cy, r = 265, 300, 185
    els = ['นโยบาย|ความปลอดภัย|สิ่งแวดล้อม', 'บริษัท:|ความรับผิดชอบ|และอำนาจ', 'DPA', 'นายเรือ:|อำนาจ|และหน้าที่', 'ทรัพยากร|และบุคลากร',
           'แผนปฏิบัติ|งานบนเรือ', 'เตรียมพร้อม|เหตุฉุกเฉิน', 'รายงาน|ความไม่สอดคล้อง|อุบัติเหตุ', 'บำรุงรักษา|เรือและ|อุปกรณ์', 'เอกสาร', 'ตรวจสอบ|ทบทวน|ประเมินผล']
    for i, t in enumerate(els):
        a = -90 + i * 360 / len(els)
        x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="49" fill="#eff6ff" stroke="#1d4ed8" stroke-width="2"/>'
        parts = t.split('|')
        for j, p in enumerate(parts):
            s += txt(x, y + 4 + (j - (len(parts) - 1) / 2) * 14, p, 9.8, 'middle', '#1e3a8a', True)
    s += f'<circle cx="{cx}" cy="{cy}" r="70" fill="#1d4ed8"/>' + txt(cx, cy - 4, 'SMS', 20, 'middle', '#fff', True) + txt(cx, cy + 18, 'ของบริษัทและเรือ', 11, 'middle', '#fff')
    bx = 520
    s += rect(bx, 60, 450, 440, '#f8fafc', '#94a3b8', 1, 10)
    L = ['วัตถุประสงค์', '• ความปลอดภัยในทะเล ป้องกันการบาดเจ็บ/สูญเสียชีวิต', '• หลีกเลี่ยงความเสียหายต่อสิ่งแวดล้อมและทรัพย์สิน', '',
         'ใบรับรอง', '• DOC (Document of Compliance) — บริษัท, สำเนาบนเรือ', '• SMC (Safety Management Certificate) — เรือ 5 ปี', '• ตรวจภายใน (internal audit) ทุกปี · ตรวจภายนอก',
         '  โดยรัฐเจ้าของธง/RO (initial, annual DOC, intermediate SMC,', '  renewal)', '', 'สิ่งที่ OOW ทำในชีวิตประจำวัน', '• ปฏิบัติตามขั้นตอน/checklist ใน SMS', '• รายงาน non-conformity, near miss, อุบัติเหตุ',
         '• รู้จัก DPA — ช่องทางตรงจากเรือถึงผู้บริหารระดับสูง', '• ฝึกซ้อมตามแผน · บันทึกถูกต้อง', '• เสนอปรับปรุงขั้นตอนที่ไม่เหมาะสม (ไม่ข้ามเอง)']
    for i, l in enumerate(L):
        s += txt(bx + 14, 84 + i * 24.5, l, 12, 'start', '#1d4ed8' if l in ('วัตถุประสงค์', 'ใบรับรอง', 'สิ่งที่ OOW ทำในชีวิตประจำวัน') else '#0f172a', l in ('วัตถุประสงค์', 'ใบรับรอง', 'สิ่งที่ OOW ทำในชีวิตประจำวัน'))
    save('legal-ism-sms.svg', s)


def isps():
    w, h = 1000, 520
    s = head(w, h, 'ISPS Code — ระดับการรักษาความปลอดภัยและผู้รับผิดชอบ')
    lv = [('ระดับ 1', 'ปกติ (normal)', 'มาตรการพื้นฐานตลอดเวลา: ควบคุมการเข้าออก ตรวจบุคคล/สัมภาระ|เขตหวงห้าม ตรวจตราดาดฟ้าและบริเวณเรือ การขนถ่ายเสบียง', '#15803d'),
          ('ระดับ 2', 'เพิ่มขึ้น (heightened)', 'มาตรการเพิ่มเติมช่วงเวลาที่ความเสี่ยงสูงขึ้น: เพิ่มยาม|จำกัดทางเข้า ตรวจละเอียดขึ้น', '#ca8a04'),
          ('ระดับ 3', 'พิเศษ (exceptional)', 'ช่วงเวลาจำกัดที่เหตุใกล้จะเกิด/เกิดขึ้น: ปฏิบัติตามคำสั่ง|หน่วยงานรัฐ อาจหยุดการทำงาน อพยพ', '#b91c1c')]
    for i, (t, d1, d2, col) in enumerate(lv):
        y = 60 + i * 90
        s += rect(30, y, 150, 76, col, col, 0, 10) + txt(105, y + 34, t, 18, 'middle', '#fff', True) + txt(105, y + 56, d1, 11.5, 'middle', '#fff')
        s += rect(190, y, 380, 76, '#fff', col, 1.5, 10)
        for j, p in enumerate(d2.split('|')):
            s += txt(204, y + 30 + j * 20, p, 11.5)
    bx = 600
    s += rect(bx, 60, 370, 256, '#f8fafc', '#94a3b8', 1, 10)
    R = ['ผู้รับผิดชอบ', '• SSO — Ship Security Officer (บนเรือ)', '• CSO — Company Security Officer', '• PFSO — Port Facility Security Officer', '• Contracting Government/รัฐ กำหนดระดับ',
         '', 'เอกสาร/ระบบ', '• Ship Security Plan (SSP) — ลับ', '• ISSC 5 ปี · บันทึกกิจกรรมความปลอดภัย', '• Declaration of Security (DoS) เมื่อจำเป็น']
    for i, r in enumerate(R):
        s += txt(bx + 14, 84 + i * 23, r, 12, 'start', '#1d4ed8' if r in ('ผู้รับผิดชอบ', 'เอกสาร/ระบบ') else '#0f172a', r in ('ผู้รับผิดชอบ', 'เอกสาร/ระบบ'))
    s += rect(30, 340, 940, 165, '#fef2f2', '#b91c1c', 1.5, 10)
    L = ['Ship Security Alert System (SSAS — SOLAS XI-2/6): ส่งสัญญาณเตือนแบบเงียบ (covert) จากเรือไปยังบริษัท/รัฐ — ไม่มีสัญญาณบนเรือ ไม่ส่งไปเรืออื่น',
         'อย่างน้อยสองจุดเปิด (สะพานเดินเรือ + อีกจุด) · ทดสอบตามแผน (แจ้งผู้รับก่อน) · ห้ามบอกตำแหน่งสวิตช์ให้คนที่ไม่เกี่ยวข้อง',
         'OOW: ควบคุมทางขึ้นเรือ (gangway) ตามระดับ บันทึกผู้มาเยือน ตรวจบัตร เฝ้าระวังเรือเล็กเข้าใกล้ รายงานสิ่งผิดปกติต่อ SSO/นายเรือ',
         'การฝึก: security drills อย่างน้อยทุก 3 เดือน (และเมื่อเปลี่ยนลูกเรือมากกว่า 25%) · exercises อย่างน้อยปีละครั้ง',
         'โจรสลัด/ปล้นเรือ: ปฏิบัติตาม SSP, แนวทางอุตสาหกรรม (BMP ฉบับปัจจุบัน), รายงานศูนย์ข้อมูลภูมิภาค (เช่น ReCAAP ISC ในเอเชีย, UKMTO)']
    for i, l in enumerate(L):
        s += txt(46, 366 + i * 30, l, 11.8)
    save('legal-isps-levels.svg', s)


def psc():
    w, h = 1000, 480
    s = head(w, h, 'การตรวจเรือโดยรัฐเจ้าท่า (Port State Control) — ลำดับทั่วไป')
    steps = [('เลือกเรือ', 'ตามระบบความเสี่ยงของ MOU|(ประวัติ อายุ ธง RO บริษัท)', '#1d4ed8'), ('Initial inspection', 'ตรวจใบรับรอง/เอกสาร|ความประทับใจทั่วไป สภาพเรือ', '#1d4ed8'),
             ('Clear grounds?', 'ใบรับรองไม่ถูกต้อง ข้อบกพร่องชัด|ลูกเรือไม่คุ้นเคยขั้นตอนสำคัญ', '#ca8a04'), ('More detailed inspection', 'ตรวจละเอียด ทดสอบอุปกรณ์|สั่งฝึกซ้อม (fire/abandon ship)', '#ca8a04'),
             ('ผลการตรวจ', 'ไม่มีข้อบกพร่อง / ข้อบกพร่องต้องแก้|ภายในเวลา / ก่อนออก', '#c2410c'), ('Detention', 'ข้อบกพร่องร้ายแรงที่ทำให้เรือไม่ปลอดภัย|กักเรือจนแก้ไข — เผยแพร่ข้อมูล', '#b91c1c')]
    for i, (t, d, col) in enumerate(steps):
        c, r = i % 3, i // 3
        x, y = 40 + c * 315, 60 + r * 160
        s += rect(x, y, 295, 130, '#fff', col, 2.5, 12)
        s += rect(x, y, 295, 40, col, col, 0, 12) + rect(x, y + 25, 295, 15, col, col, 0)
        s += txt(x + 147, y + 27, t, 14, 'middle', '#fff', True)
        for j, p in enumerate(d.split('|')):
            s += txt(x + 147, y + 74 + j * 22, p, 11.8, 'middle')
        if c < 2:
            s += line(x + 296, y + 65, x + 313, y + 65, '#0f172a', 2, mk='ar')
    s += rect(40, 385, 920, 85, '#f8fafc', '#94a3b8', 1, 10)
    L = ['MOU ภูมิภาค เช่น Paris MOU, Tokyo MOU (เอเชีย-แปซิฟิก), Indian Ocean MOU · USCG ใช้ระบบของสหรัฐฯ เอง (ไม่ใช่ MOU) — มี CIC หัวข้อเฉพาะทุกปี',
         'OOW ช่วยได้มาก: รู้หน้าที่ฉุกเฉินของตน สาธิตอุปกรณ์ที่รับผิดชอบได้ (ECDIS, GMDSS, LSA, ไฟฉุกเฉิน) บันทึกตรงกัน (log, ชั่วโมงพัก)',
         'ตอบคำถามตามจริง สุภาพ แจ้งนายเรือ — ข้อบกพร่องเล็ก ๆ ที่แก้ได้ทันที ควรแก้ก่อนเรือเข้าท่า (เตรียม PSC checklist ล่วงหน้า)']
    for i, l in enumerate(L):
        s += txt(56, 410 + i * 24, l, 11.8)
    save('legal-psc-process.svg', s)


if __name__ == '__main__':
    zones(); imo(); solas(); certificates(); hssc(); ism(); isps(); psc()
