"""ภาพประกอบบท 3.7 ภาวะผู้นำและการทำงานเป็นทีม"""
import math, os
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


def box(x, y, w, h, t1, t2, col):
    return rect(x - w / 2, y - h / 2, w, h, '#fff', col, 2, 10) + txt(x, y - 3, t1, 12.5, 'middle', col, True) + (txt(x, y + 14, t2, 10.5, 'middle', '#334155') if t2 else '')


def organisation():
    w, h = 1000, 560
    s = head(w, h, 'โครงสร้างองค์กรบนเรือสินค้า (ตัวอย่างทั่วไป) และการเชื่อมกับฝั่ง')
    s += box(500, 85, 180, 50, 'นายเรือ (Master)', 'อำนาจเหนือสุด (ISM 5)', '#1e3a8a')
    s += box(860, 85, 200, 50, 'บริษัท · DPA · CSO', 'ฝั่ง (shore management)', '#7c3aed')
    s += line(590, 85, 760, 85, '#7c3aed', 2, '6 4')
    depts = [(180, 'ฝ่ายเดินเรือ (Deck)', '#1d4ed8', [('ต้นเรือ (C/O)', 'สินค้า เสถียรภาพ ดาดฟ้า'), ('ผู้ช่วยต้นเรือ 2/O', 'การเดินเรือ/แผนที่'), ('ผู้ช่วยต้นเรือ 3/O', 'LSA/FFA ตามมอบหมาย'), ('Bosun · AB · OS', 'งานดาดฟ้า ยาม'), ('Deck cadet', 'ฝึกตาม TRB')]),
             (500, 'ฝ่ายช่างกล (Engine)', '#c2410c', [('ต้นกล (C/E)', 'เครื่องจักรทั้งหมด'), ('รองต้นกล 2/E', 'บำรุงรักษาหลัก'), ('3/E · 4/E', 'เครื่องไฟ ปั๊ม หม้อน้ำ'), ('ETO', 'ไฟฟ้า อิเล็กทรอนิกส์'), ('Fitter · Oiler · Wiper', 'งานห้องเครื่อง')]),
             (820, 'ฝ่ายบริการ (Catering)', '#15803d', [('Chief cook', 'อาหาร สุขอนามัย'), ('Messman/Steward', 'ที่พัก ห้องอาหาร')])]
    for x, t, col, members in depts:
        s += line(500, 110, x, 150, '#94a3b8', 2)
        s += rect(x - 140, 150, 280, 40, col, col, 0, 10) + txt(x, 176, t, 14, 'middle', '#fff', True)
        for i, (a, b) in enumerate(members):
            y = 220 + i * 56
            s += box(x, y, 250, 46, a, b, col)
            s += line(x, 190 + (i > 0) * (y - 56 - 190 + 23), x, y - 23, '#cbd5e1', 1.5) if i == 0 else line(x, y - 33, x, y - 23, '#cbd5e1', 1.5)
    s += rect(30, 500, 940, 50, '#f8fafc', '#94a3b8', 1, 8)
    s += txt(500, 522, 'จำนวนและตำแหน่งตาม Minimum Safe Manning Document และนโยบายบริษัท · หน้าที่ฉุกเฉินตาม muster list · OOW ต้องรู้สายบังคับบัญชา', 12, 'middle')
    s += txt(500, 540, 'และช่องทางสื่อสารข้ามฝ่าย (ห้องเครื่อง–สะพานเดินเรือ–ดาดฟ้า) — ลูกเรือหลายสัญชาติ: ภาษาทำงานร่วม (มักเป็นอังกฤษ) และความเข้าใจวัฒนธรรม', 12, 'middle', '#334155')
    save('lead-shipboard-organisation.svg', s)


def workload():
    w, h = 1000, 520
    s = head(w, h, 'การจัดการงานและภาระงาน (Task and workload management)')
    x0, y0, cw, ch = 60, 80, 220, 160
    quad = [('ด่วน + สำคัญ', 'ทำทันที', 'เหตุฉุกเฉิน ความปลอดภัย|เรือกำลังเข้าใกล้อันตราย', '#b91c1c'), ('ไม่ด่วน + สำคัญ', 'วางแผน/กำหนดเวลา', 'บำรุงรักษาตาม PMS การฝึก|วางแผนเดินทาง เตรียมท่า', '#1d4ed8'),
            ('ด่วน + ไม่สำคัญ', 'มอบหมาย/จัดการสั้น ๆ', 'คำขอเอกสารบางอย่าง|งานธุรการที่รอได้ไม่นาน', '#ca8a04'), ('ไม่ด่วน + ไม่สำคัญ', 'ตัดออก/เลื่อน', 'งานที่ไม่เพิ่มความปลอดภัย|หรือคุณค่า', '#64748b')]
    for i, (t, a, d, col) in enumerate(quad):
        c, r = i % 2, i // 2
        x, y = x0 + c * (cw + 10), y0 + r * (ch + 10)
        s += rect(x, y, cw, ch, '#fff', col, 2.5, 12)
        s += txt(x + cw / 2, y + 30, t, 14, 'middle', col, True) + txt(x + cw / 2, y + 56, '→ ' + a, 13, 'middle', '#0f172a', True)
        for j, p in enumerate(d.split('|')):
            s += txt(x + cw / 2, y + 90 + j * 20, p, 11.5, 'middle', '#334155')
    s += txt(x0 + cw + 5, y0 - 12, 'การจัดลำดับความสำคัญ (prioritization)', 13, 'middle', '#0f172a', True)
    bx = 540
    steps = [('1. วางแผนและประสาน', 'กำหนดงาน เป้าหมาย ลำดับ จุดเชื่อมกับฝ่ายอื่น (ห้องเครื่อง ท่า)'), ('2. มอบหมายบุคลากร', 'ตามความสามารถ ประสบการณ์ ใบประกาศ และสภาพความเหนื่อยล้า'),
             ('3. ข้อจำกัดเวลาและทรัพยากร', 'ชั่วโมงพัก อุปกรณ์ สภาพอากาศ เวลาในท่า งบประมาณ'), ('4. จัดลำดับความสำคัญ', 'ความปลอดภัยและงานวิกฤตก่อน — ปรับเมื่อสถานการณ์เปลี่ยน'),
             ('5. ติดตามและทบทวน', 'ตรวจความคืบหน้า สื่อสาร ปรับแผน debrief')]
    for i, (t, d) in enumerate(steps):
        y = 70 + i * 74
        s += rect(bx, y, 430, 62, '#f0f9ff', '#0369a1', 1.5, 10)
        s += txt(bx + 14, y + 24, t, 13, 'start', '#075985', True) + txt(bx + 14, y + 46, d, 11.3)
    s += rect(60, 440, 450, 60, '#fff7ed', '#c2410c', 1.2, 10)
    s += txt(76, 464, 'ภาระงานสูงเกิน → ผิดพลาด ความเหนื่อยล้า; ต่ำเกิน → เบื่อ ขาดสมาธิ', 12, 'start', '#7c2d12', True)
    s += txt(76, 486, 'ผู้นำต้องคาดการณ์ช่วงงานหนัก (เข้าท่า ขนถ่าย) และเตรียมคนล่วงหน้า', 12, 'start', '#7c2d12')
    save('lead-workload.svg', s)


def styles():
    w, h = 1000, 520
    s = head(w, h, 'รูปแบบภาวะผู้นำตามสถานการณ์ และแรงจูงใจ')
    x0, y0, cw, ch = 50, 80, 210, 150
    q = [('S3 Participating (ร่วมคิด)', 'ทีมมีความสามารถ|แต่ขาดความมั่นใจ/แรงจูงใจ', '#15803d'), ('S2 Selling/Coaching (แนะนำ)', 'ทีมเริ่มเรียนรู้|ต้องอธิบายเหตุผล', '#ca8a04'),
         ('S4 Delegating (มอบหมาย)', 'ทีมชำนาญและมั่นใจ|ให้อิสระ ติดตามผล', '#1d4ed8'), ('S1 Telling/Directing (สั่งการ)', 'มือใหม่ หรือเหตุฉุกเฉิน|สั่งชัด ควบคุมใกล้ชิด', '#b91c1c')]
    for i, (t, d, col) in enumerate(q):
        c, r = i % 2, i // 2
        x, y = x0 + c * (cw + 10), y0 + r * (ch + 10)
        s += rect(x, y, cw, ch, '#fff', col, 2.5, 12)
        s += txt(x + cw / 2, y + 32, t, 12.5, 'middle', col, True)
        for j, p in enumerate(d.split('|')):
            s += txt(x + cw / 2, y + 72 + j * 22, p, 11.8, 'middle')
    s += txt(x0 + cw + 5, y0 - 12, 'เลือกรูปแบบให้เหมาะกับคนและสถานการณ์', 13, 'middle', '#0f172a', True)
    # axes of the situational-leadership grid (Hersey-Blanchard): directive behaviour to the right, supportive behaviour upward
    gx1, gy1 = x0 + 2 * cw + 10, y0 + 2 * ch + 10
    s += line(x0, gy1 + 14, gx1, gy1 + 14, '#475569', 1.5, mk='ar')
    s += txt(x0 + cw + 5, gy1 + 30, 'พฤติกรรมสั่งการ (directive) มากขึ้น →', 11, 'middle', '#475569')
    s += line(x0 - 14, gy1, x0 - 14, y0, '#475569', 1.5, mk='ar')
    s += f'<text x="{x0-22}" y="{y0+ch+5}" font-size="11" fill="#475569" text-anchor="middle" transform="rotate(-90 {x0-22} {y0+ch+5})">พฤติกรรมสนับสนุน (supportive) มากขึ้น →</text>'
    s += txt(x0 + cw + 5, gy1 + 52, 'ภาวะฉุกเฉิน → ชัดเจนเด็ดขาด · งานปกติกับทีมชำนาญ → มีส่วนร่วม/มอบหมาย', 11.5, 'middle', '#334155')
    s += txt(x0 + cw + 5, gy1 + 70, '(Situational Leadership — Hersey &amp; Blanchard)', 10.5, 'middle', '#64748b')
    # Maslow pyramid
    cx, base, top = 748, 430, 90
    levels = [('การบรรลุศักยภาพ', '#7c3aed'), ('การยอมรับ ความภาคภูมิ', '#1d4ed8'), ('การเป็นส่วนหนึ่งของทีม', '#0891b2'), ('ความปลอดภัย มั่นคง', '#15803d'), ('ปัจจัยพื้นฐาน อาหาร พักผ่อน', '#ca8a04')]
    n = len(levels)
    for i, (t, col) in enumerate(levels):
        yt = top + i * (base - top) / n
        yb = top + (i + 1) * (base - top) / n
        wt = 20 + i * 45
        wb = 20 + (i + 1) * 45
        s += f'<polygon points="{cx-wt},{yt:.1f} {cx+wt},{yt:.1f} {cx+wb},{yb:.1f} {cx-wb},{yb:.1f}" fill="{col}" stroke="#fff" stroke-width="2"/>'
        s += txt(cx, (yt + yb) / 2 + 5, t, 11.5 if i else 10, 'middle', '#fff', True)
    s += txt(cx, 70, 'ลำดับความต้องการ (Maslow) — แนวคิดแรงจูงใจ', 13, 'middle', '#0f172a', True)
    s += txt(cx, 460, 'บนเรือ: อาหารดี ที่พักดี พักพอ ปลอดภัย → ทีม ยอมรับ', 11.5, 'middle', '#334155')
    s += txt(cx, 478, 'ความก้าวหน้า — ชมเชยงานดีต่อหน้า ติเพื่อก่อในที่ส่วนตัว', 11.5, 'middle', '#334155')
    save('lead-leadership-styles.svg', s)


def decision():
    w, h = 1000, 580
    s = head(w, h, 'การตัดสินใจ: DODAR และการประเมินความเสี่ยง (risk matrix)')
    cx, cy, r = 250, 290, 150
    steps = [('D', 'Diagnose', 'ประเมินสถานการณ์|เกิดอะไรขึ้น'), ('O', 'Options', 'สร้างทางเลือก|ข้อดี-ข้อเสีย'), ('D', 'Decide', 'เลือกแนวทาง|(และแผนสำรอง)'),
             ('A', 'Assign', 'มอบหมายงาน|สื่อสารชัด'), ('R', 'Review', 'ประเมินผล|ปรับเมื่อจำเป็น')]
    for i, (k, t, d) in enumerate(steps):
        a = -90 + i * 72
        x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="55" fill="#eff6ff" stroke="#1d4ed8" stroke-width="2.5"/>'
        s += txt(x, y - 18, k + ' — ' + t, 12.5, 'middle', '#1e3a8a', True)
        for j, p in enumerate(d.split('|')):
            s += txt(x, y + 4 + j * 16, p, 10.5, 'middle')
    for i in range(5):
        a1, a2 = -90 + i * 72 + 24, -90 + i * 72 + 48
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        x2, y2 = cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2))
        s += f'<path d="M {x1:.1f} {y1:.1f} A {r} {r} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="#1d4ed8" stroke-width="2" marker-end="url(#ar)"/>'
    s += txt(cx, cy + 5, 'วนซ้ำ', 14, 'middle', '#1d4ed8', True)
    # risk matrix
    mx, my, cs = 560, 90, 72
    def band(v):  # same bands as the legend: 1-2 / 3-6 / 8-12 / 15-25
        return '#bbf7d0' if v <= 2 else '#fde68a' if v <= 6 else '#fecaca' if v <= 12 else '#f87171'
    for r_ in range(5):
        for c in range(5):
            s += rect(mx + c * cs, my + (4 - r_) * cs * 0.75, cs, cs * 0.75, band((r_ + 1) * (c + 1)), '#fff', 2)
            s += txt(mx + c * cs + cs / 2, my + (4 - r_) * cs * 0.75 + cs * 0.45, str((r_ + 1) * (c + 1)), 13, 'middle', '#0f172a', True)
    s += txt(mx + 2.5 * cs, my + 5 * cs * 0.75 + 22, 'ความรุนแรงของผลที่ตามมา (severity) →', 12, 'middle')
    s += f'<text x="{mx-16}" y="{my+2.5*cs*0.75}" font-size="12" text-anchor="middle" transform="rotate(-90 {mx-16} {my+2.5*cs*0.75})">โอกาสเกิด (likelihood) →</text>'
    s += txt(mx + 2.5 * cs, my - 14, 'Risk = Likelihood × Severity (ตัวอย่าง 5×5)', 13, 'middle', '#0f172a', True)
    s += rect(560, 405, 410, 160, '#f8fafc', '#94a3b8', 1, 10)
    L = [('#bbf7d0', 'ต่ำ (1–2): ยอมรับได้ ควบคุมตามปกติ'), ('#fde68a', 'ต่ำ–กลาง (3–6): ลดให้ต่ำที่สุดเท่าที่ทำได้ (ALARP)'),
         ('#fecaca', 'กลาง–สูง (8–12): ต้องมีมาตรการเพิ่มก่อนเริ่มงาน'), ('#f87171', 'สูง (15–25): ห้ามทำจนกว่าจะลดความเสี่ยง/อนุมัติระดับสูง')]
    for i, (c, l) in enumerate(L):
        s += rect(576, 418 + i * 22, 14, 14, c, '#94a3b8', 1, 2) + txt(598, 430 + i * 22, l, 11.6)
    s += txt(576, 528, 'ลำดับการควบคุม: ขจัด → ทดแทน → วิศวกรรม → บริหาร/ขั้นตอน → PPE', 11.6)
    s += txt(576, 550, 'แถบสีเป็นตัวอย่าง — ใช้ risk matrix ของบริษัท (SMS) เสมอ', 11, 'start', '#64748b')
    save('lead-decision-making.svg', s)


if __name__ == '__main__':
    organisation(); workload(); styles(); decision()
