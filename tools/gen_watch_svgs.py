"""ภาพประกอบบทหลักการเข้ายาม: BNWAS, hours of rest, handover"""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{t}</text>\n')
def save(n, s): open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')

def bnwas():
    w, h = 1000, 400
    s = head(w, h, 'BNWAS (Res. MSC.128(75)) — ลำดับการเตือนเมื่อไม่มีการรีเซ็ต')
    stages = [('Dormant period', '3–12 นาที (ตั้งค่า)', '#e2e8f0', 220), ('ไฟเตือนบนสะพาน', '15 วินาที', '#fde68a', 150), ('1st stage: เสียงบนสะพาน', '15 วินาที', '#fdba74', 170), ('2nd stage: นายเรือ/backup', '90 วินาที*', '#f87171', 190), ('3rd stage: ลูกเรืออื่น', '', '#b91c1c', 190)]
    x = 40
    for t, d, c, wd in stages:
        s += f'<rect x="{x}" y="100" width="{wd}" height="70" fill="{c}" stroke="#0f172a"/>\n'
        s += f'<text x="{x+wd/2}" y="130" text-anchor="middle" font-size="13" font-weight="bold" fill="{"#fff" if c in ("#b91c1c",) else "#0f172a"}">{t}</text>\n'
        s += f'<text x="{x+wd/2}" y="152" text-anchor="middle" font-size="12" fill="{"#fff" if c in ("#b91c1c",) else "#0f172a"}">{d}</text>\n'
        x += wd
    s += '<line x1="40" y1="200" x2="960" y2="200" stroke="#0f172a" stroke-width="2" marker-end="url(#ar)"/><text x="900" y="222" font-size="13">เวลา</text>\n'
    s += '<text x="40" y="260" font-size="13">• รีเซ็ตได้ด้วยการกดปุ่ม reset หรือการตรวจจับการเคลื่อนไหว/การใช้งานอุปกรณ์ที่เชื่อมต่อ (ตามแบบที่ติดตั้ง)</text>\n'
    s += '<text x="40" y="282" font-size="13">• โหมด: Automatic (ทำงานเมื่อ heading/track control ทำงาน) · Manual ON · Manual OFF (ตามที่นายเรือกำหนด)</text>\n'
    s += '<text x="40" y="304" font-size="13">• ปุ่ม Emergency call (ถ้าติดตั้ง — มาตรฐานให้ "อาจจัดให้มี"): เรียกขอความช่วยเหลือไปยัง 2nd/3rd stage ทันที</text>\n'
    s += '<text x="40" y="326" font-size="13">• การกดปุ่มค้างไม่ยืด dormant period · การเลือกโหมดและค่า Td ล็อกให้นายเรือเท่านั้น</text>\n'
    s += '<text x="40" y="348" font-size="12" fill="#64748b">* ปกติ 90 วินาที เรือใหญ่ตั้งตอนติดตั้งให้นานขึ้นได้ถึง 3 นาที (ให้เวลาคนจาก 2nd stage มาถึงสะพาน)</text>\n'
    s += '<text x="40" y="370" font-size="12" fill="#64748b">เรือที่ไม่ใช่เรือโดยสาร: ตั้งให้ 2nd และ 3rd stage ดังพร้อมกันทุกจุดได้ และถ้าตั้งเช่นนั้นจะไม่มี 3rd stage แยก</text>\n'
    save('bnwas-stages.svg', s)

def rest_hours():
    w, h = 1000, 474
    s = head(w, h, 'ชั่วโมงพักผ่อน (STCW A-VIII/1, MLC 2006) — ตัวอย่างตารางยาม 4-on/8-off')
    x0, x1 = 300, 980; sc = (x1 - x0) / 24
    for t in range(0, 25, 2):
        s += f'<line x1="{x0+t*sc}" y1="60" x2="{x0+t*sc}" y2="320" stroke="#e2e8f0"/><text x="{x0+t*sc}" y="335" text-anchor="middle" font-size="11">{t:02d}:00</text>\n'
    rows = [
        ('2/O (0000–0400, 1200–1600)', [(0, 4, 'W'), (12, 16, 'W')]),
        ('3/O (0800–1200, 2000–2400)', [(8, 12, 'W'), (20, 24, 'W')]),
        ('C/O (0400–0800, 1600–2000)', [(4, 8, 'W'), (16, 20, 'W')]),
        ('ตัวอย่างผิด: 3/O วันเข้าท่า', [(3, 6, 'X'), (8, 12, 'W'), (13, 17, 'X'), (18, 19, 'X'), (20, 24, 'W')]),
    ]
    for i, (lab, segs) in enumerate(rows):
        y = 70 + i * 62
        s += f'<text x="10" y="{y+26}" font-size="12" font-weight="bold">{lab}</text>\n'
        s += f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="40" fill="#dcfce7" stroke="#86efac"/>\n'
        for a, b, k in segs:
            col = '#1e3a8a' if k == 'W' else '#b91c1c'
            s += f'<rect x="{x0+a*sc:.1f}" y="{y}" width="{(b-a)*sc:.1f}" height="40" fill="{col}"/>\n'
    s += '<rect x="300" y="350" width="16" height="12" fill="#1e3a8a"/><text x="322" y="361" font-size="12">ยาม/ทำงาน</text>\n'
    s += '<rect x="420" y="350" width="16" height="12" fill="#b91c1c"/><text x="442" y="361" font-size="12">งานเพิ่ม (เข้าท่า ซ้อม ขนถ่ายสินค้า)</text>\n'
    s += '<rect x="700" y="350" width="16" height="12" fill="#dcfce7" stroke="#86efac"/><text x="722" y="361" font-size="12">พักผ่อน</text>\n'
    s += '<text x="10" y="392" font-size="13">เกณฑ์: พัก ≥ 10 ชม./24 ชม. และ ≥ 77 ชม./7 วัน · แบ่งได้ไม่เกิน 2 ช่วง โดยช่วงหนึ่ง ≥ 6 ชม. · ระหว่างช่วงพักห่างกันไม่เกิน 14 ชม.</text>\n'
    s += '<text x="10" y="414" font-size="13">MLC A2.3 ให้ใช้อีกแบบได้: ทำงานไม่เกิน 14 ชม./24 ชม. และ 72 ชม./7 วัน · ข้อยกเว้นตาม STCW A-VIII/1 วรรค 9: ≥ 70 ชม./7 วัน แบ่งได้ 3 ช่วง</text>\n'
    s += '<text x="10" y="440" font-size="13" fill="#b91c1c">แถวสุดท้าย (stand-by เข้าท่า 0300–0600, ยามสินค้า 1300–1700, ซ้อม 1800–1900): พักรวมเพียง 8 ชม. แบ่ง 5 ช่วง</text>\n'
    s += '<text x="10" y="462" font-size="13" fill="#b91c1c">ไม่มีช่วงใดถึง 6 ชม. → ผิดเกณฑ์ทั้ง 10 ชม./24 ชม. และการแบ่งช่วง (งานเข้าท่า/สินค้าไม่ใช่เหตุฉุกเฉินตาม A-VIII/1)</text>\n'
    save('hours-of-rest.svg', s)

def handover():
    w, h = 1000, 520
    s = head(w, h, 'การรับ-ส่งยาม (STCW A-VIII/2 Part 4-1 วรรค 19–23) — สิ่งที่ผู้รับยามต้องรู้ก่อนรับ')
    boxes = [
        ('คำสั่งและข้อจำกัด', ['Master\'s standing orders', 'Night orders / คำสั่งพิเศษ', 'สถานะ passage plan']),
        ('ตำแหน่งและการเคลื่อนที่', ['ตำแหน่ง เข็ม ความเร็ว', 'draught, UKC (squat, heel, trim)', 'set &amp; drift ล่าสุด']),
        ('สภาพแวดล้อม', ['น้ำขึ้นลง กระแสน้ำ', 'อากาศ ทัศนวิสัย (ปัจจุบัน/พยากรณ์)', 'อันตรายที่จะเจอในยาม']),
        ('การจราจร', ['เรือที่มองเห็นหรือรู้ว่าอยู่ใกล้', 'CPA/TCPA เป้าสำคัญ', 'การตกลงกับเรืออื่น/VTS']),
        ('อุปกรณ์', ['สภาพเครื่องมือเดินเรือ/ความปลอดภัย', 'gyro/magnetic compass error', 'โหมดถือท้าย, ไฟเดินเรือ']),
        ('เครื่องจักรและอื่น ๆ', ['ขั้นตอนใช้เครื่องจักรบังคับเรือ', 'งานบนดาดฟ้า/คนทำงานข้างนอก', 'GMDSS, NAVTEX ใหม่']),
    ]
    for i, (t, items) in enumerate(boxes):
        c, r = i % 3, i // 3
        x, y = 30 + c * 320, 60 + r * 200
        s += f'<rect x="{x}" y="{y}" width="300" height="180" rx="10" fill="#f8fafc" stroke="#1e3a8a"/>\n'
        s += f'<rect x="{x}" y="{y}" width="300" height="36" rx="10" fill="#1e3a8a"/><text x="{x+150}" y="{y+24}" text-anchor="middle" font-size="15" font-weight="bold" fill="#fff">{t}</text>\n'
        for j, it in enumerate(items):
            s += f'<text x="{x+16}" y="{y+70+j*34}" font-size="14">☐ {it}</text>\n'
    s += '<text x="30" y="490" font-size="13" fill="#b91c1c" font-weight="bold">ห้ามส่งยามระหว่างกำลังบังคับเรือหลบหลีก · ผู้รับยามต้องปรับสายตาให้ชินความมืดก่อน · ถ้าผู้รับยามไม่พร้อม (ป่วย เมา) ห้ามส่ง แจ้งนายเรือ</text>\n'
    save('watch-handover.svg', s)

if __name__ == '__main__':
    bnwas(); rest_hours(); handover(); print('ok')
