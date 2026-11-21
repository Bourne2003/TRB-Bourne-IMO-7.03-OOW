"""ภาพประกอบบท ECDIS"""
import math, os
R = math.radians
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker></defs>\n'
            f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{t}</text>\n')
def save(n, s): open(os.path.join(OUT, n), 'w').write(s + '</svg>\n')
def box(x, y, w, h, t, sub='', c='#e0f2fe', sc='#0369a1'):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{c}" stroke="{sc}" stroke-width="2"/>\n<text x="{x+w/2}" y="{y+h/2-(6 if sub else -5)}" text-anchor="middle" font-size="14" font-weight="bold">{t}</text>\n'
    if sub: s += f'<text x="{x+w/2}" y="{y+h/2+14}" text-anchor="middle" font-size="11" fill="#334155">{sub}</text>\n'
    return s

def safety_contour():
    w, h = 1000, 560
    s = head(w, h, 'ECDIS safety settings — ตัวอย่าง draught 9.6 m (ข้อมูลจำลอง)')
    # four-shade depth areas as horizontal bands (cross section on left as plan)
    bands = [('#c9a66b', 'บก (land)', 0, 70), ('#9fd5a5', 'แห้งเมื่อน้ำลง (drying)', 70, 120), ('#61a5e8', 'ตื้นกว่า shallow contour (&lt; 10 m)', 120, 190), ('#a8d4f7', 'ระหว่าง shallow – safety contour (10–15 m)', 190, 300), ('#dbeefe', 'ระหว่าง safety – deep contour (15–20 m)', 300, 420), ('#ffffff', 'ลึกกว่า deep contour (> 20 m)', 420, 520)]
    x0, x1 = 40, 640
    for c, t, a, b in bands:
        s += f'<rect x="{x0}" y="{40+a}" width="{x1-x0}" height="{b-a}" fill="{c}" stroke="#94a3b8" stroke-width="0.5"/><text x="{x0+12}" y="{40+(a+b)/2+5}" font-size="13">{t}</text>\n'
    s += f'<line x1="{x0}" y1="{40+300}" x2="{x1}" y2="{40+300}" stroke="#111827" stroke-width="4"/>\n'
    s += f'<text x="{x1-250}" y="{40+294}" font-size="14" font-weight="bold">SAFETY CONTOUR 15 m (หนา)</text>\n'
    # isolated danger in safe water
    s += f'<g transform="translate(560,{40+470})"><circle r="11" fill="none" stroke="#c026d3" stroke-width="2.5"/><path d="M -7 -7 L 7 7 M 7 -7 L -7 7" stroke="#c026d3" stroke-width="2.5"/></g>\n'
    s += f'<text x="400" y="{40+500}" font-size="12" fill="#a21caf">isolated danger (≤ safety contour) ในน้ำลึก</text>\n'
    # spot soundings
    for (xx, yy, v, bold) in [(300, 360, '18', False), (380, 205, '7', True), (420, 470, '34', False), (220, 262, '11', True), (520, 305, '13', False)]:
        fw = ' font-weight="bold"' if bold else ''
        col = '#111827' if bold else '#64748b'
        s += f'<text x="{xx}" y="{yy}" font-size="15"{fw} fill="{col}">{v}</text>\n'
    s += '<text x="250" y="262" font-size="11" fill="#111827">← ตัวเลขดำหนา = ≤ safety depth (12 m) · ตัวเลขเทา = ลึกกว่า</text>\n'
    # settings box
    s += '<rect x="670" y="60" width="315" height="470" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    rows = [('การคำนวณ (MV Andaman Pearl — สมมติ)', True), ('Draught สูงสุด              9.60 m', False), ('Squat (open water 10 kn)    0.65 m', False), ('UKC policy (≈10% draught)   1.00 m', False), ('เผื่อ CATZOC B/คลื่น          0.50 m', False), ('รวม (ไม่นับระดับน้ำ)       11.75 m', False), ('', False), ('ตั้งค่าใน ECDIS', True), ('Safety depth = 12 m', False), ('Safety contour = 12 m', False), ('→ ENC มี contour 10/15/20 m', False), ('→ ECDIS ใช้ 15 m (ถัดไปที่ลึกกว่า)', False), ('Shallow contour = 10 m', False), ('Deep contour = 20 m (≈ 2 × draught)', False), ('Look-ahead = 6 นาที (10 kn → 1.0 nm)', False), ('XTL = 0.2 nm (TSS)', False), ('', False), ('Four-shade ON, shallow pattern ON', False)]
    for i, (t, b) in enumerate(rows):
        fw = ' font-weight="bold" fill="#1e3a8a"' if b else ''
        s += f'<text x="684" y="{88+i*24}" font-size="13"{fw}>{t}</text>\n'
    save('ecdis-safety-contour.svg', s)

def display_categories():
    w, h = 1000, 470
    s = head(w, h, 'ประเภทการแสดงผลของ ECDIS (IHO S-52 / MSC.232(82))')
    for k, (t, c, sc) in enumerate([('Display Base', '#dbeafe', '#1d4ed8'), ('Standard Display', '#dcfce7', '#15803d'), ('All Other Information', '#fef9c3', '#a16207')]):
        x = 60 + k * 305
        s += f'<rect x="{x}" y="70" width="270" height="350" rx="10" fill="{c}" stroke="{sc}" stroke-width="2"/>\n'
        s += f'<text x="{x+135}" y="98" text-anchor="middle" font-size="16" font-weight="bold" fill="{sc}">{t}</text>\n'
    cols = [['ลบออกจากจอไม่ได้', '• แนวชายฝั่ง (high water)', '• Own safety contour', '• Isolated dangers ในน้ำปลอดภัย', '  (ตื้นกว่า safety contour)', '• Isolated dangers ในน้ำปลอดภัย', '  เช่น สะพาน สายไฟ ทุ่น/หลักแสดง', '• ระบบจัดเส้นทาง (TSS)', '• Scale, range, orientation,', '  display mode', '• หน่วยความลึกและความสูง'],
            ['แสดงเมื่อเปิดเครื่อง (default)', '• Display Base +', '• Drying line', '• ทุ่น หลักแสดง เครื่องหมาย', '• ขอบร่องน้ำ ช่องทาง', '• วัตถุเด่นทางตาและเรดาร์', '• เขตห้าม/จำกัด', '• ขอบเขตมาตราส่วนแผนที่', '• Cautionary notes', '• ทางเรือข้ามฟาก', '• Archipelagic sea lanes'],
            ['เลือกแสดงทีละรายการ', '• Spot soundings', '• เคเบิล/ท่อใต้น้ำ', '• รายละเอียดอันตราย/ไฟ', '• Magnetic variation', '• Graticule', '• ชื่อสถานที่', '• ลักษณะพื้นทะเล', '• รายละเอียดอื่นทั้งหมด', '', '"All" ≠ ทุกอย่างจำเป็น', 'ระวังจอรก (clutter)']]
    for k, lines in enumerate(cols):
        x = 76 + k * 305
        for i, t in enumerate(lines):
            fw = ' font-weight="bold"' if i == 0 else ''
            s += f'<text x="{x}" y="{140 + i*25}" font-size="13"{fw}>{t}</text>\n'
    s += '<text x="500" y="452" text-anchor="middle" font-size="13" fill="#b91c1c">ข้อควรจำ: "Standard" ไม่แสดง spot soundings — วางแผน/ตรวจเส้นทางต้องดูแบบ "All/Other" ที่ scale เหมาะสมด้วย</text>\n'
    save('ecdis-display-categories.svg', s)

def catzoc():
    rows = [('A1', 6, '± 5 m + 5% ความลึก', '0.50 + 1% d', 'สำรวจเต็มพื้นที่ (full area search) พบสิ่งที่มีนัยสำคัญทั้งหมด'),
            ('A2', 5, '± 20 m', '1.00 + 2% d', 'สำรวจเต็มพื้นที่'),
            ('B', 4, '± 50 m', '1.00 + 2% d', 'ไม่เต็มพื้นที่ — ไม่คาดว่ามีอันตรายนอกแผนที่ แต่อาจมี'),
            ('C', 3, '± 500 m', '2.00 + 5% d', 'ไม่ได้สำรวจเต็มพื้นที่ คาดว่ามีความลึกผิดปกติ'),
            ('D', 2, 'แย่กว่า C', 'แย่กว่า C', 'ไม่ได้สำรวจเต็มพื้นที่ คาดว่ามีความลึกผิดปกติมาก'),
            ('U', 0, 'ยังไม่ประเมิน', '–', 'ข้อมูลคุณภาพยังไม่ได้ประเมิน')]
    w, h = 1000, 440
    s = head(w, h, 'Zones of Confidence (CATZOC) — ความน่าเชื่อถือของข้อมูลใน ENC')
    hdr = ['ZOC', 'สัญลักษณ์', 'ความแม่นยำตำแหน่ง', 'ความแม่นยำความลึก (m)', 'Seafloor coverage']
    xs = [30, 110, 260, 460, 640]
    for x, t in zip(xs, hdr):
        s += f'<text x="{x}" y="70" font-size="14" font-weight="bold">{t}</text>\n'
    for i, (z, n, p, d, c) in enumerate(rows):
        y = 100 + i * 50
        s += f'<rect x="20" y="{y-24}" width="960" height="44" fill="{"#f8fafc" if i % 2 else "#fff"}"/>\n'
        s += f'<text x="{xs[0]}" y="{y+4}" font-size="16" font-weight="bold">{z}</text>\n'
        if n:
            for k in range(n):
                a = 2 * math.pi * k / n - math.pi / 2
                s += f'<text x="{xs[1]+40+16*math.cos(a):.1f}" y="{y+6+14*math.sin(a):.1f}" font-size="12" text-anchor="middle" fill="#a16207">★</text>\n'
        else:
            s += f'<text x="{xs[1]+40}" y="{y+6}" font-size="15" text-anchor="middle" fill="#a16207">U</text>\n'
        s += f'<text x="{xs[2]}" y="{y+4}" font-size="13">{p}</text><text x="{xs[3]}" y="{y+4}" font-size="13">{d}</text><text x="{xs[4]}" y="{y+4}" font-size="12">{c}</text>\n'
    s += '<text x="30" y="405" font-size="12" fill="#334155">แสดงใน ECDIS เป็นรูปดาวในสามเหลี่ยม/วงรี (data quality indicator) เมื่อเปิดแสดง — ใช้เพิ่ม safety margin ในพื้นที่ ZOC ต่ำ (ค่าในตารางสรุปจาก IHO S-57 / S-67)</text>\n'
    s += '<text x="30" y="428" font-size="12" fill="#334155">S-101: CATZOC (M_QUAL) ถูกแทนด้วย Quality of Bathymetric Data ที่แยกความแม่นยำตำแหน่ง ความลึก และ seafloor coverage — การแสดงผลแบบดาวกำลังถูกทบทวน</text>\n'
    save('ecdis-catzoc.svg', s)

def system():
    w, h = 1000, 470
    s = head(w, h, 'ECDIS กับเซนเซอร์และระบบที่เชื่อมต่อ')
    s += box(390, 180, 220, 110, 'ECDIS', 'SENC + presentation + alarms', '#1e3a8a', '#1e3a8a').replace('font-weight="bold">ECDIS', 'font-weight="bold" fill="#fff">ECDIS').replace('fill="#334155">SENC', 'fill="#dbeafe">SENC')
    items = [(40, 60, 'GNSS 1/2', 'ตำแหน่ง SOG COG'), (40, 180, 'Gyro (THD)', 'heading'), (40, 300, 'Speed log', 'STW (และ/หรือ SOG)'), (390, 60, 'ENC + updates', 'AVCS / S-63 permits'), (740, 60, 'Radar / ARPA', 'overlay + tracked targets'), (740, 180, 'AIS', 'เป้า AIS, AtoN'), (740, 300, 'Echo sounder', 'ความลึก (บางระบบ)'), (390, 360, 'Back-up ECDIS', 'แหล่งไฟแยก + route เดียวกัน')]
    ends = {(40, 60): (390, 205), (40, 180): (390, 235), (40, 300): (390, 265),
            (740, 60): (610, 205), (740, 180): (610, 235), (740, 300): (610, 265),
            (390, 60): (500, 178)}
    for x, y, t, sub in items:
        s += box(x, y, 220, 80, t, sub)
        if (x, y) == (390, 360):
            # primary ECDIS keeps the back-up loaded with the same route/ENCs
            s += '<line x1="500" y1="292" x2="500" y2="358" stroke="#334155" stroke-width="2" marker-end="url(#ar)"/>\n'
            s += '<text x="492" y="330" text-anchor="end" font-size="11" fill="#334155">route + ENC เดียวกัน (พร้อมรับช่วง)</text>\n'
            continue
        ex, ey = ends[(x, y)]
        if (x, y) == (390, 60):
            sx, sy = 500, 140
        else:
            sx, sy = (x + 220, y + 40) if x < 390 else (x, y + 40)
        s += f'<line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}" stroke="#334155" stroke-width="2" marker-end="url(#ar)"/>\n'
    s += '<text x="500" y="460" text-anchor="middle" font-size="12" fill="#b91c1c">ถ้าเซนเซอร์ตัวเดียวผิด (เช่น GNSS) ทุกจอที่ใช้ข้อมูลนั้นผิดพร้อมกัน → ต้องยืนยันตำแหน่งด้วยวิธีอิสระเสมอ</text>\n'
    save('ecdis-system.svg', s)

def look_ahead():
    w, h = 1000, 470
    s = head(w, h, 'Anti-grounding: look-ahead area และ alarm "crossing safety contour"')
    s += '<rect x="0" y="40" width="1000" height="430" fill="#dbeefe"/>\n'
    s += '<path d="M 560 40 Q 640 160 600 260 Q 570 330 640 470 L 1000 470 L 1000 40 Z" fill="#a8d4f7"/>\n'
    s += '<path d="M 560 40 Q 640 160 600 260 Q 570 330 640 470" fill="none" stroke="#111827" stroke-width="4"/>\n'
    s += '<path d="M 760 40 Q 820 200 790 300 Q 770 380 800 470 L 1000 470 L 1000 40 Z" fill="#c9a66b"/>\n'
    s += '<text x="616" y="232" font-size="14" font-weight="bold">Safety contour</text><text x="840" y="250" font-size="14">บก</text>\n'
    # ship
    sx, sy = 260, 300; hdg = 65
    ux, uy = math.sin(R(hdg)), -math.cos(R(hdg))
    px, py = -uy, ux
    L = 380; half = 45
    poly = [(sx + px * 20, sy + py * 20), (sx + ux * L + px * half, sy + uy * L + py * half), (sx + ux * L - px * half, sy + uy * L - py * half), (sx - px * 20, sy - py * 20)]
    s += '<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in poly) + '" fill="#fca5a5" opacity="0.55" stroke="#b91c1c" stroke-dasharray="6 4"/>\n'
    s += f'<g transform="translate({sx},{sy}) rotate({hdg})"><path d="M 0 -18 L 8 10 L -8 10 Z" fill="#111827"/></g>\n'
    s += f'<line x1="{sx}" y1="{sy}" x2="{sx+ux*120:.1f}" y2="{sy+uy*120:.1f}" stroke="#111827" stroke-width="2" marker-end="url(#ar)"/>\n'
    s += '<text x="120" y="360" font-size="14" font-weight="bold">Own ship + vector</text>\n'
    s += '<text x="110" y="150" font-size="14" font-weight="bold" fill="#b91c1c">Look-ahead area</text><text x="110" y="170" font-size="12" fill="#b91c1c">(เช่น 6 นาที × SOG และความกว้างที่ตั้ง)</text>\n'
    s += '<circle cx="618" cy="170" r="14" fill="none" stroke="#dc2626" stroke-width="3"/><text x="640" y="112" font-size="14" font-weight="bold" fill="#dc2626">ALARM: crossing safety contour</text><line x1="640" y1="118" x2="624" y2="158" stroke="#dc2626" stroke-width="2"/>\n'
    s += '<rect x="20" y="380" width="520" height="80" rx="8" fill="#fff" stroke="#94a3b8"/>\n'
    s += '<text x="34" y="404" font-size="13">ถ้าพื้นที่ look-ahead แตะ safety contour หรือ area พิเศษ → ALARM</text>\n'
    s += '<text x="34" y="426" font-size="13">สั้นเกินไป → เตือนช้า · ยาวเกินไป → alarm ตลอด (alarm fatigue)</text>\n'
    s += '<text x="34" y="448" font-size="13">ห้ามปิดเสียง alarm แบบถาวร — ปรับค่าให้เหมาะกับสถานการณ์แทน</text>\n'
    save('ecdis-look-ahead.svg', s)

if __name__ == '__main__':
    safety_contour(); display_categories(); catzoc(); system(); look_ahead(); print('ok')
