"""ภาพประกอบบท 1.7 English และ IMO SMCP (Res. A.918(22))
- smcp-message-markers.svg : โครงสร้างการเรียก/ตอบทาง VHF + message markers 8 ตัว
- smcp-wheel-order-loop.svg : วงจรปิด (closed loop) ของคำสั่งหางเสือตาม SMCP A2/1
"""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"


def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n'
            f'<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">'
            '<path d="M0,0 L12,6 L0,12 z" fill="#334155"/></marker></defs>\n'
            f'<text x="{w/2}" y="32" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{t}</text>\n')


def save(n, s):
    open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')


def box(x, y, w, h, fill, stroke, lines, size=12, bold_first=True, anchor='start'):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>\n'
    tx = x + 10 if anchor == 'start' else x + w / 2
    for i, ln in enumerate(lines):
        fw = 'bold' if (i == 0 and bold_first) else 'normal'
        s += f'<text x="{tx}" y="{y + 20 + i * (size + 5)}" text-anchor="{anchor}" font-size="{size}" font-weight="{fw}" fill="#0f172a">{ln}</text>\n'
    return s


def message_markers():
    w, h = 1000, 730
    s = head(w, h, 'IMO SMCP: ลำดับการสื่อสารทาง VHF และ Message markers 8 ตัว')
    # ---- left: VHF exchange structure
    s += '<text x="30" y="66" font-size="15" font-weight="bold" fill="#1e3a8a">ก) โครงสร้างการเรียก–ตอบ (ITU RR + SMCP)</text>\n'
    steps = [('1. เรียก (call)', 'ชื่อสถานีที่เรียก ×(1–3) · "this is" · ชื่อเรา', '"Seaport Control, this is Andaman Pearl."', '#e0f2fe', '#0369a1'),
             ('2. ตอบรับ (answer)', 'สถานีที่ถูกเรียกตอบ · อาจให้เปลี่ยนช่อง', '"Andaman Pearl, Seaport Control. Go ahead."', '#e0f2fe', '#0369a1'),
             ('3. ข้อความ + message marker', 'พูด marker นำหน้าข้อความ · ตัวเลขทีละหลัก', '"QUESTION. What is your ETA at pilot station?"', '#fef3c7', '#b45309'),
             ('4. ตอบ / ทวนข้อความสำคัญ', 'ANSWER ห้ามมีคำถามซ้อน · ทวน (read back)', '"ANSWER. My ETA is zero six three zero local."', '#fef3c7', '#b45309'),
             ('5. ปิดการพูด', '"Over" = รอคำตอบ · "Out" = จบการติดต่อ', '"... Over."  /  "... Out."', '#dcfce7', '#15803d')]
    y = 80
    for i, (t, d, ex, f, st) in enumerate(steps):
        s += box(30, y, 440, 92, f, st, [t, d, ex], size=12.5)
        if i < len(steps) - 1:
            s += f'<line x1="250" y1="{y+92}" x2="250" y2="{y+105}" stroke="#334155" stroke-width="2" marker-end="url(#ar)"/>\n'
        y += 107
    s += ('<text x="30" y="646" font-size="12" fill="#334155">ไม่เข้าใจ/ไม่ได้ยิน → "Say again (please)." · พูดผิด → "Mistake ... correction ..." · '
          'ยังไม่มีข้อมูล → "Stand by" + เวลา</text>\n')
    s += '<text x="30" y="665" font-size="12" fill="#334155">ความชัดของสัญญาณ: "I read you bad/one ... poor/two ... fair/three ... good/four ... excellent/five"</text>\n'
    # ---- right: eight message markers
    s += '<text x="500" y="66" font-size="15" font-weight="bold" fill="#1e3a8a">ข) Message markers (SMCP General 3 · A1/6)</text>\n'
    mk = [('INSTRUCTION', 'คำสั่งจากผู้มีอำนาจ (VTS/เรือรบ) — ต้องทำตาม', 'เว้นแต่มีเหตุผลด้านความปลอดภัยและแจ้งกลับ', '#fee2e2', '#b91c1c'),
          ('ADVICE', 'คำแนะนำ — ผู้รับตัดสินใจเอง แต่ต้องพิจารณาจริงจัง', '', '#ffedd5', '#c2410c'),
          ('WARNING', 'แจ้งอันตราย — ผู้รับต้องสนใจทันที', '', '#fef9c3', '#a16207'),
          ('INFORMATION', 'ข้อเท็จจริงที่สังเกตได้ (การจราจร การเดินเรือ)', '', '#e0f2fe', '#0369a1'),
          ('QUESTION', 'คำถาม — ผู้รับต้องตอบกลับ', '', '#ede9fe', '#6d28d9'),
          ('ANSWER', 'ตอบคำถามก่อนหน้า — ห้ามมีคำถามซ้อนในคำตอบ', '', '#ede9fe', '#6d28d9'),
          ('REQUEST', 'ขอให้จัด/ให้บางสิ่ง (ลากจูง เสบียง การอนุญาต)', 'ห้ามใช้เรื่องการเดินเรือหรือเพื่อเปลี่ยน COLREG', '#dcfce7', '#15803d'),
          ('INTENTION', 'แจ้งการกระทำทางเดินเรือที่ "เรือเรา" จะทำทันที', '', '#dcfce7', '#15803d')]
    y = 80
    for name, m1, m2, f, st in mk:
        s += f'<rect x="500" y="{y}" width="470" height="62" rx="8" fill="{f}" stroke="{st}" stroke-width="1.6"/>\n'
        s += f'<text x="512" y="{y+24}" font-size="14" font-weight="bold" fill="{st}">{name}</text>\n'
        s += f'<text x="640" y="{y+24}" font-size="12">{m1}</text>\n'
        if m2:
            s += f'<text x="640" y="{y+44}" font-size="12" fill="#7f1d1d">{m2}</text>\n'
        y += 68
    s += ('<text x="30" y="684" font-size="12" fill="#334155">ใช้ marker ตามดุลยพินิจ พูดนำหน้าข้อความ (หรือส่วนของข้อความ) ที่ต้องการให้ชัดว่าเป็นอะไร</text>\n')
    s += ('<text x="30" y="703" font-size="12" fill="#334155">หลีกเลี่ยง may/might/should/could/can → ใช้ QUESTION/ANSWER/INTENTION/ADVICE/WARNING แทน (General 18)</text>\n')
    s += '<text x="30" y="722" font-size="11" fill="#64748b">ชื่อสถานีและเรือในตัวอย่างเป็นชื่อสมมติ · อ้างอิง IMO Res. A.918(22) General sections 3, 4, 6–9, 18 และ A1/6</text>\n'
    save('smcp-message-markers.svg', s)


def wheel_loop():
    w, h = 1000, 600
    s = head(w, h, 'คำสั่งหางเสือแบบวงจรปิด (closed loop) — SMCP A2/1 Standard wheel orders')
    # four boxes around a loop
    B = [(70, 70, 'OOW / นำร่อง สั่ง', ['"Starboard twenty."', 'พูดชัด ทิศก่อน แล้วมุม'], '#dbeafe', '#1d4ed8'),
         (560, 70, 'นายท้ายทวนคำสั่งทันที', ['"Starboard twenty."', '(ทวนก่อนลงมือ)'], '#fef3c7', '#b45309'),
         (560, 300, 'นายท้ายหมุนพวงมาลัย + รายงาน', ['"Wheel starboard twenty."', 'เมื่อหางเสือถึงมุมที่สั่ง'], '#fef3c7', '#b45309'),
         (70, 300, 'OOW ตรวจและรับทราบ', ['ดู rudder angle indicator', 'และการหันของหัวเรือ (ROT)'], '#dbeafe', '#1d4ed8')]
    for x, y, t, ls, f, st in B:
        s += f'<rect x="{x}" y="{y}" width="370" height="120" rx="12" fill="{f}" stroke="{st}" stroke-width="2"/>\n'
        s += f'<text x="{x+185}" y="{y+34}" text-anchor="middle" font-size="16" font-weight="bold" fill="{st}">{t}</text>\n'
        for i, ln in enumerate(ls):
            s += f'<text x="{x+185}" y="{y+66+i*24}" text-anchor="middle" font-size="{15 if i == 0 else 13}" font-weight="{"bold" if i == 0 else "normal"}">{ln}</text>\n'
    arrows = [(440, 130, 556, 130), (745, 190, 745, 296), (560, 360, 444, 360), (255, 300, 255, 194)]
    for x1, y1, x2, y2 in arrows:
        s += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#334155" stroke-width="2.5" marker-end="url(#ar)"/>\n'
    s += '<text x="500" y="250" text-anchor="middle" font-size="13" fill="#b91c1c" font-weight="bold">ทวนผิด / หางเสือไม่ไปตามสั่ง</text>'
    s += '<text x="500" y="268" text-anchor="middle" font-size="13" fill="#b91c1c">→ OOW แก้คำสั่งทันที (ตรวจได้ก่อนเรือหันผิด)</text>\n'
    # course-to-steer example and rules
    s += '<rect x="40" y="446" width="920" height="138" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    s += '<text x="56" y="472" font-size="14" font-weight="bold" fill="#0f172a">สั่งเข็มเป็นตัวเลข: บอกทิศที่จะหมุนก่อน แล้วพูดเลขทีละหลัก (รวมศูนย์)</text>\n'
    ex = ['OOW: "Port, steer one eight two."  →  นายท้าย: "Port, steer one eight two."  →  เมื่อนิ่งบนเข็ม: "Steady on one eight two."  →  OOW รับทราบ',
          'มุมหางเสือพูดเป็นจำนวน (fifteen, twenty) ส่วนเข็ม/แบริ่งพูดทีละหลัก · คำสั่งค้างไว้จนกว่าจะมีคำสั่งใหม่ (held until countermanded)',
          'นายท้ายต้องรายงานทันทีถ้าเรือไม่ตอบสนองหางเสือ · ถ้าสงสัยว่านายท้ายเหม่อ ให้ถาม "What is your heading?" → "My heading is ... degrees."',
          'Steady = ลดการหันให้เร็วที่สุด · Meet her = ต้านการหันของหัวเรือ · Steady as she goes = ถือเข็มที่หัวเรือชี้ขณะสั่ง (นายท้ายขานเข็ม)']
    for i, ln in enumerate(ex):
        s += f'<text x="56" y="{498+i*22}" font-size="12">{ln}</text>\n'
    save('smcp-wheel-order-loop.svg', s)


if __name__ == '__main__':
    message_markers(); wheel_loop(); print('ok')
