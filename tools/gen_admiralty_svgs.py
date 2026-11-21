"""สคริปต์สร้างภาพประกอบบท 1.1.2-E (ADMIRALTY publications)

ภาพ admiralty-np-passage-planning.svg — สิ่งพิมพ์ ADMIRALTY ชุด NP แต่ละกลุ่มใช้ในขั้นใดของ
passage planning (Appraisal / Planning / Execution / Monitoring ตาม IMO Res. A.893(21))
และแต่ละกลุ่มได้รับการแก้ไขจาก Section ใดของ ADMIRALTY Weekly Notices to Mariners
"""
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def head(w, h, title, sub=None):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n'
         f'<rect width="{w}" height="{h}" fill="#fff"/>\n'
         '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">'
         '<path d="M0,0 L10,5 L0,10 z" fill="#334155"/></marker></defs>\n'
         f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{esc(title)}</text>\n')
    if sub:
        s += f'<text x="{w/2}" y="52" text-anchor="middle" font-size="13" fill="#475569">{esc(sub)}</text>\n'
    return s


def passage_planning():
    w, h = 1000, 690
    s = head(w, h, 'ADMIRALTY publications ชุด NP — ใช้ในขั้นไหนของ passage planning',
             'ขั้นตอนตาม IMO Res. A.893(21) Guidelines for Voyage Planning · ตัวเลขในวงเล็บคือ Section ของ Weekly NMs ที่ใช้แก้ไข')
    stages = [
        ('1. APPRAISAL', 'รวบรวม/ประเมินข้อมูล', '#1e3a8a', '#eff6ff', [
            ('NP131 Catalogue', 'เลือกแผนที่/ENC ที่ต้องใช้'),
            ('NP1–NP72 Sailing Directions (IV)', 'ชายฝั่ง ท่า กฎท้องถิ่น'),
            ('NP136(1)/(2) Ocean Passages (VII)', 'เส้นทางเดินสมุทรตามฤดู'),
            ('Routeing Charts 5124–5128', 'ลม กระแสน้ำ load line'),
            ('NP100 Mariner\'s Handbook (VII)', 'ความน่าเชื่อถือของข้อมูล'),
            ('NP350 Distance Tables', 'ระยะทางระหว่างท่า'),
            ('NP247 / NAVAREA in force (III)', 'T&P และคำเตือนที่มีผล'),
            ('Q-series Security Charts', 'พื้นที่เสี่ยง การรายงาน'),
        ]),
        ('2. PLANNING', 'ลากเส้นทาง/ทำ plan', '#166534', '#f0fdf4', [
            ('แผนที่กระดาษ / ENC-AVCS (II, VIII)', 'แผนที่ทางการ เป็นปัจจุบัน'),
            ('NP5011 / NP5012', 'อ่านสัญลักษณ์กระดาษ/ENC'),
            ('NP74–NP88 List of Lights (V)', 'ไฟ landfall, sector, clearing'),
            ('NP282 ALRS Vol 2 (VI)', 'Racon, AIS AtoN, legal time'),
            ('NP286 ALRS Vol 6 (VI)', 'จุดรายงาน VTS นำร่อง ท่า'),
            ('NP201–NP208 ATT / TotalTide', 'UKC, tidal window, air draught'),
            ('Tidal Stream Atlases', 'กระแสน้ำรายชั่วโมง'),
            ('Ships\' Routeing (IMO)', 'TSS, ATBA, ระบบรายงาน'),
        ]),
        ('3. EXECUTION', 'เดินเรือตาม plan', '#9a3412', '#fff7ed', [
            ('NP74–NP88 List of Lights', 'ระบุไฟด้วยคาบ/จังหวะ'),
            ('NP283 ALRS Vol 3', 'ตาราง NAVTEX, SafetyNET, อากาศ'),
            ('NP281 ALRS Vol 1', 'สถานีวิทยุ TMAS'),
            ('NP285 ALRS Vol 5', 'ขั้นตอน GMDSS'),
            ('NP286 ALRS Vol 6', 'ช่อง VHF VTS/นำร่อง'),
            ('NP314 Nautical Almanac', 'GHA/Dec ดาราศาสตร์'),
            ('NP401 / NP303 Sight Reduction', 'คำนวณ intercept'),
            ('Sailing Directions', 'directions เข้าท่า'),
        ]),
        ('4. MONITORING', 'ติดตาม/ปรับแผน', '#6b21a8', '#faf5ff', [
            ('Weekly NMs (I–VIII)', 'แก้ไขทุกสัปดาห์'),
            ('NP234A/B Cumulative List', 'ตรวจว่าแผนที่แก้ครบ'),
            ('NP247(1)/(2) Annual Summary', 'Annual NMs, T&P ต้นปี'),
            ('NAVTEX / SafetyNET / SafetyCast', 'คำเตือนใหม่ระหว่างทาง'),
            ('NP133A / NP133C (VII)', 'บันทึกการแก้ไข'),
            ('NP294', 'วิธีแก้ไขผลิตภัณฑ์ ADMIRALTY'),
            ('e-NP / ADSD / ADP', 'ฉบับดิจิทัล อัปเดตอัตโนมัติ'),
            ('H102 (รายงานกลับ UKHO)', 'แจ้งอันตราย/ข้อมูลผิด'),
        ]),
    ]
    cw, gap, x0, y0 = 232, 12, 18, 74
    row_h = 52
    for i, (title, sub, col, bg, items) in enumerate(stages):
        x = x0 + i * (cw + gap)
        bh = 58 + row_h * len(items) + 6
        s += f'<rect x="{x}" y="{y0}" width="{cw}" height="{bh}" rx="10" fill="{bg}" stroke="{col}" stroke-width="2"/>\n'
        s += f'<rect x="{x}" y="{y0}" width="{cw}" height="46" rx="10" fill="{col}"/>\n'
        s += f'<rect x="{x}" y="{y0+30}" width="{cw}" height="16" fill="{col}"/>\n'
        s += f'<text x="{x+cw/2}" y="{y0+21}" text-anchor="middle" font-size="15" font-weight="bold" fill="#fff">{esc(title)}</text>\n'
        s += f'<text x="{x+cw/2}" y="{y0+39}" text-anchor="middle" font-size="12" fill="#e2e8f0">{esc(sub)}</text>\n'
        for j, (name, use) in enumerate(items):
            yy = y0 + 58 + j * row_h
            s += f'<rect x="{x+8}" y="{yy}" width="{cw-16}" height="{row_h-8}" rx="6" fill="#fff" stroke="#cbd5e1"/>\n'
            s += f'<text x="{x+16}" y="{yy+18}" font-size="12" font-weight="bold" fill="{col}">{esc(name)}</text>\n'
            s += f'<text x="{x+16}" y="{yy+35}" font-size="11.5" fill="#334155">{esc(use)}</text>\n'
        if i < 3:
            ax = x + cw + 1
            s += f'<line x1="{ax}" y1="{y0+23}" x2="{ax+gap-1}" y2="{y0+23}" stroke="#334155" stroke-width="2" marker-end="url(#ar)"/>\n'
    # loop back arrow monitoring -> appraisal (plan is revised when new information arrives)
    yb = y0 + 58 + row_h * 8 + 6 + 14
    s += f'<path d="M {x0 + 3*(cw+gap) + cw/2} {yb-14} L {x0 + 3*(cw+gap) + cw/2} {yb} L {x0 + cw/2} {yb} L {x0 + cw/2} {yb-12}" fill="none" stroke="#64748b" stroke-width="1.6" stroke-dasharray="6 4" marker-end="url(#ar)"/>\n'
    s += f'<text x="{w/2}" y="{yb+17}" text-anchor="middle" font-size="12" fill="#475569">ข้อมูลใหม่ (NMs, คำเตือน, สภาพอากาศ) → ทบทวนและแก้ plan ได้ตลอด แต่ต้องแจ้งนายเรือและบันทึก</text>\n'
    # weekly NM sections bar
    yS = yb + 46
    s += f'<text x="{x0}" y="{yS}" font-size="13" font-weight="bold" fill="#0f172a">ADMIRALTY Weekly NMs — Section ไหนแก้อะไร</text>\n'
    secs = [('I', 'ดัชนี · New Editions'), ('II', 'แผนที่กระดาษ (รวม T&amp;P)'), ('III', 'NAVAREA I warnings'),
            ('IV', 'Sailing Directions'), ('V', 'List of Lights'), ('VI', 'List of Radio Signals'),
            ('VII', 'สิ่งพิมพ์อื่น เช่น NP100'), ('VIII', 'บริการดิจิทัล')]
    bw = (w - 2 * x0 - 7 * 6) / 8
    for k, (num, txt) in enumerate(secs):
        bx = x0 + k * (bw + 6)
        s += f'<rect x="{bx:.1f}" y="{yS+8}" width="{bw:.1f}" height="44" rx="6" fill="#f1f5f9" stroke="#94a3b8"/>\n'
        s += f'<text x="{bx+bw/2:.1f}" y="{yS+25}" text-anchor="middle" font-size="12" font-weight="bold" fill="#0f172a">Section {num}</text>\n'
        s += f'<text x="{bx+bw/2:.1f}" y="{yS+42}" text-anchor="middle" font-size="9.5" fill="#334155">{txt}</text>\n'
    open(os.path.join(OUT, 'admiralty-np-passage-planning.svg'), 'w').write(s + '</svg>\n')


if __name__ == '__main__':
    passage_planning()
    print('ok')
