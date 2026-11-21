"""ภาพประกอบบท BRM / Human factors"""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker>'
            '<marker id="arr" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" refX="12" refY="7" orient="auto"><path d="M0,0 L14,7 L0,14 z" fill="#b91c1c"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{t}</text>\n')
def save(n, s): open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')

def swiss():
    w, h = 1000, 470
    s = head(w, h, 'Swiss Cheese Model (James Reason) — อุบัติเหตุเกิดเมื่อ "รู" ของทุกชั้นเรียงตรงกัน')
    layers = [('องค์กร/บริษัท', 'นโยบาย กำลังคน การฝึก', '#fde68a'), ('การกำกับดูแล', 'SMS ตรวจสอบ checklist', '#fcd34d'), ('เงื่อนไขก่อนเกิด', 'ความเหนื่อยล้า การสื่อสาร', '#fbbf24'), ('การกระทำที่ไม่ปลอดภัย', 'ไม่ cross-check ปิด alarm', '#f59e0b')]
    for i, (t, d, c) in enumerate(layers):
        x = 140 + i * 190
        s += f'<path d="M {x} 110 L {x+60} 80 L {x+60} 330 L {x} 360 Z" fill="{c}" stroke="#92400e"/>\n'
        yl = 200 + 40 * (x + 30 - 100) / 830   # y of the hazard trajectory at this slice — one hole sits on it (holes line up)
        for (dx, dy, r) in [(30, 145 + i * 4, 10), (30, yl, 13), (30, 300 - i * 6, 7)]:
            s += f'<ellipse cx="{x+dx}" cy="{dy}" rx="{r*0.6}" ry="{r}" fill="#fff" stroke="#92400e"/>\n'
        s += f'<text x="{x+30}" y="390" text-anchor="middle" font-size="13" font-weight="bold">{t}</text><text x="{x+30}" y="408" text-anchor="middle" font-size="11" fill="#475569">{d}</text>\n'
    s += '<text x="40" y="200" font-size="14" font-weight="bold" fill="#b91c1c">อันตราย</text><text x="40" y="218" font-size="12" fill="#b91c1c">(hazard)</text>\n'
    s += '<path d="M 100 200 L 930 240" stroke="#b91c1c" stroke-width="3" stroke-dasharray="10 5" marker-end="url(#arr)"/>\n'
    s += '<text x="860" y="280" font-size="14" font-weight="bold" fill="#b91c1c">อุบัติเหตุ</text><text x="860" y="298" font-size="12" fill="#b91c1c">(เกยตื้น/โดนกัน)</text>\n'
    s += '<text x="40" y="440" font-size="13" fill="#334155">BRM ทำหน้าที่ "อุดรู" — การ cross-check, challenge &amp; response, briefing ทำให้ห่วงโซ่ความผิดพลาด (error chain) ขาดก่อนถึงอุบัติเหตุ</text>\n'
    s += '<text x="40" y="458" font-size="12" fill="#64748b">รูในชั้นซ้าย 3 ชั้น = latent conditions (แฝงอยู่นาน) · รูในชั้นขวาสุด = active failure (เกิดหน้างาน) · เส้นประผ่านรูที่เรียงตรงกันทุกชั้น</text>\n'
    save('brm-swiss-cheese.svg', s)

def sa_levels():
    w, h = 1000, 400
    s = head(w, h, 'Situational Awareness 3 ระดับ (Endsley) ในบริบทสะพานเดินเรือ')
    items = [('ระดับ 1 Perception', 'รับรู้: เห็นไฟแดงทางขวา ระยะ 3\'', 'เรดาร์ CPA 0.2\' · ลมแรงขึ้น', '#bfdbfe'),
             ('ระดับ 2 Comprehension', 'เข้าใจ: เรือกลตัดหน้า', 'เราเป็น give-way · ความเสี่ยงสูง', '#93c5fd'),
             ('ระดับ 3 Projection', 'คาดการณ์: 10 นาทีข้างหน้า', 'ถ้าหันขวา 40° จะใกล้เรือประมง?', '#60a5fa')]
    for i, (t, a, b, c) in enumerate(items):
        x = 40 + i * 320
        s += f'<rect x="{x}" y="90" width="280" height="160" rx="12" fill="{c}" stroke="#1e3a8a"/>\n'
        s += f'<text x="{x+140}" y="125" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">{t}</text>\n'
        s += f'<text x="{x+140}" y="170" text-anchor="middle" font-size="13">{a}</text><text x="{x+140}" y="196" text-anchor="middle" font-size="13">{b}</text>\n'
        if i < 2:
            s += f'<path d="M {x+282} 170 L {x+318} 170" stroke="#0f172a" stroke-width="3" marker-end="url(#ar)"/>\n'
    s += '<path d="M 880 255 Q 520 330 180 255" fill="none" stroke="#15803d" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#ar)"/>\n'
    s += '<text x="400" y="320" font-size="13" fill="#15803d" font-weight="bold">ตัดสินใจ → ทำ → ตรวจผล → รับรู้ใหม่ (วงจรต่อเนื่อง)</text>\n'
    s += '<text x="40" y="365" font-size="13" fill="#b91c1c">สัญญาณ SA หลุด: ความคลุมเครือ จดจ่อสิ่งเดียว สับสน ไม่ทำตามแผน/ขั้นตอน ข้อมูลขัดแย้งไม่ได้แก้ ไม่มีใครขับเรือ (no one conning) สื่อสารไม่ชัด</text>\n'
    save('brm-sa-levels.svg', s)

def authority():
    w, h = 1000, 380
    s = head(w, h, 'Authority Gradient — ความชันของลำดับอำนาจบนสะพานเดินเรือ')
    cfgs = [('ชันเกินไป (Too steep)', 'ลูกน้องไม่กล้าทัก', 190, '#b91c1c'), ('เหมาะสม (Optimal)', 'ผู้นำชัด + ทีมกล้าพูด', 90, '#15803d'), ('แบนเกินไป (Too flat)', 'ไม่มีใครตัดสินใจ', 12, '#b45309')]
    for i, (t, d, rise, c) in enumerate(cfgs):
        x = 60 + i * 320; y = 280
        x2 = x + 220; y2 = y - rise
        s += f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2:.1f}" stroke="{c}" stroke-width="6"/>\n'
        s += f'<circle cx="{x}" cy="{y}" r="14" fill="#64748b"/><text x="{x}" y="{y+36}" text-anchor="middle" font-size="12">OOW/ลูกเรือ</text>\n'
        s += f'<circle cx="{x2}" cy="{y2:.1f}" r="16" fill="#1e3a8a"/><text x="{x2}" y="{y2-24:.1f}" text-anchor="middle" font-size="12">นายเรือ</text>\n'
        s += f'<text x="{x+120}" y="330" text-anchor="middle" font-size="15" font-weight="bold" fill="{c}">{t}</text><text x="{x+120}" y="352" text-anchor="middle" font-size="13">{d}</text>\n'
    save('brm-authority-gradient.svg', s)

def closed_loop():
    w, h = 1000, 330
    s = head(w, h, 'Closed-loop communication — สั่ง → ทวน → ยืนยัน → รายงานผล')
    steps = [('ผู้ส่ง (Pilot/Master/OOW)', '"Starboard ten."'), ('ผู้รับทวน (Helmsman)', '"Starboard ten."'), ('ผู้ส่งยืนยัน', '"Correct."'), ('ผู้รับรายงานผล', '"Wheel is starboard ten."')]
    for i, (t, q) in enumerate(steps):
        x = 30 + i * 245
        s += f'<rect x="{x}" y="90" width="215" height="110" rx="12" fill="#eff6ff" stroke="#1e3a8a"/>\n'
        s += f'<text x="{x+107}" y="125" text-anchor="middle" font-size="14" font-weight="bold">{t}</text><text x="{x+107}" y="160" text-anchor="middle" font-size="14" fill="#1d4ed8">{q}</text>\n'
        if i < 3:
            s += f'<path d="M {x+217} 145 L {x+243} 145" stroke="#0f172a" stroke-width="3" marker-end="url(#ar)"/>\n'
    s += '<text x="30" y="245" font-size="13">ใช้กับคำสั่งหางเสือ เครื่องจักร การรายงานตำแหน่ง/เป้า และการสื่อสารภายนอก (VTS, เรืออื่น) — ช่วยตัด "การได้ยินผิด" ซึ่งเป็นสาเหตุอุบัติเหตุจำนวนมาก</text>\n'
    s += '<text x="30" y="270" font-size="13">ภาษาเดียวกัน (มักเป็นอังกฤษ + SMCP) · คำสั่งสั้น ชัด · เรียกชื่อผู้รับ · ไม่ใช้คำกำกวม เช่น "OK" แทนการทวนคำสั่ง</text>\n'
    s += '<text x="30" y="295" font-size="13">ปิดวง: เมื่อได้รับรายงานผล ผู้ส่งตรวจที่ rudder angle indicator แล้วรับทราบ ("Thank you") — บางเรือพูดยืนยันหลังรายงานผลแทน หลักคือห้ามจบวงโดยไม่ตรวจ</text>\n'
    save('brm-closed-loop.svg', s)

if __name__ == '__main__':
    swiss(); sa_levels(); authority(); closed_loop(); print('ok')
