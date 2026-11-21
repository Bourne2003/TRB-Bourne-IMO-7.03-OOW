"""ภาพธงประมวลสัญญาณสากล (ICS) และรหัสมอร์ส"""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"
R_, W_, B_, Y_, K_ = '#d4202a', '#ffffff', '#1f3f9a', '#f6c800', '#111111'
_cid = iter(range(1, 10000))

def flag(letter, x, y, w=72, h=48):
    """draw ICS alphabet flag at x,y"""
    c = next(_cid)
    s = f'<clipPath id="f{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#f{c})">'
    def rect(xx, yy, ww, hh, col): return f'<rect x="{xx}" y="{yy}" width="{ww}" height="{hh}" fill="{col}"/>'
    L = letter
    if L == 'A':
        s += rect(x, y, w / 2, h, W_) + f'<path d="M {x+w/2} {y} L {x+w} {y} L {x+w*0.75} {y+h/2} L {x+w} {y+h} L {x+w/2} {y+h} Z" fill="{B_}"/>'
    elif L == 'B':
        s += f'<path d="M {x} {y} L {x+w} {y} L {x+w*0.75} {y+h/2} L {x+w} {y+h} L {x} {y+h} Z" fill="{R_}"/>'
    elif L == 'C':
        cols = [B_, W_, R_, W_, B_]
        for i, cc in enumerate(cols): s += rect(x, y + i * h / 5, w, h / 5 + 0.5, cc)
    elif L == 'D':
        s += rect(x, y, w, h, Y_) + rect(x, y + h / 4, w, h / 2, B_)
    elif L == 'E':
        s += rect(x, y, w, h / 2, B_) + rect(x, y + h / 2, w, h / 2, R_)
    elif L == 'F':
        s += rect(x, y, w, h, W_) + f'<path d="M {x+w/2} {y} L {x+w} {y+h/2} L {x+w/2} {y+h} L {x} {y+h/2} Z" fill="{R_}"/>'
    elif L == 'G':
        for i in range(6): s += rect(x + i * w / 6, y, w / 6 + 0.5, h, Y_ if i % 2 == 0 else B_)
    elif L == 'H':
        s += rect(x, y, w / 2, h, W_) + rect(x + w / 2, y, w / 2, h, R_)
    elif L == 'I':
        s += rect(x, y, w, h, Y_) + f'<circle cx="{x+w/2}" cy="{y+h/2}" r="{h*0.28}" fill="{K_}"/>'
    elif L == 'J':
        s += rect(x, y, w, h, B_) + rect(x, y + h / 3, w, h / 3, W_)
    elif L == 'K':
        s += rect(x, y, w / 2, h, Y_) + rect(x + w / 2, y, w / 2, h, B_)
    elif L == 'L':
        s += rect(x, y, w / 2, h / 2, Y_) + rect(x + w / 2, y, w / 2, h / 2, K_) + rect(x, y + h / 2, w / 2, h / 2, K_) + rect(x + w / 2, y + h / 2, w / 2, h / 2, Y_)
    elif L == 'M':
        s += rect(x, y, w, h, B_) + f'<path d="M {x} {y} L {x+w} {y+h} M {x+w} {y} L {x} {y+h}" stroke="{W_}" stroke-width="{h*0.22}"/>'
    elif L == 'N':
        for i in range(4):
            for j in range(4): s += rect(x + i * w / 4, y + j * h / 4, w / 4 + 0.5, h / 4 + 0.5, B_ if (i + j) % 2 == 0 else W_)
    elif L == 'O':
        s += f'<path d="M {x} {y} L {x+w} {y} L {x+w} {y+h} Z" fill="{R_}"/><path d="M {x} {y} L {x+w} {y+h} L {x} {y+h} Z" fill="{Y_}"/>'
    elif L == 'P':
        s += rect(x, y, w, h, B_) + rect(x + w / 3, y + h / 3, w / 3, h / 3, W_)
    elif L == 'Q':
        s += rect(x, y, w, h, Y_)
    elif L == 'R':
        s += rect(x, y, w, h, R_) + rect(x + w * 0.42, y, w * 0.16, h, Y_) + rect(x, y + h * 0.38, w, h * 0.24, Y_)
    elif L == 'S':
        s += rect(x, y, w, h, W_) + rect(x + w / 3, y + h / 3, w / 3, h / 3, B_)
    elif L == 'T':
        s += rect(x, y, w / 3, h, R_) + rect(x + w / 3, y, w / 3, h, W_) + rect(x + 2 * w / 3, y, w / 3, h, B_)
    elif L == 'U':
        s += rect(x, y, w / 2, h / 2, R_) + rect(x + w / 2, y, w / 2, h / 2, W_) + rect(x, y + h / 2, w / 2, h / 2, W_) + rect(x + w / 2, y + h / 2, w / 2, h / 2, R_)
    elif L == 'V':
        s += rect(x, y, w, h, W_) + f'<path d="M {x} {y} L {x+w} {y+h} M {x+w} {y} L {x} {y+h}" stroke="{R_}" stroke-width="{h*0.22}"/>'
    elif L == 'W':
        s += rect(x, y, w, h, B_) + rect(x + w / 6, y + h / 6, w * 2 / 3, h * 2 / 3, W_) + rect(x + w / 3, y + h / 3, w / 3, h / 3, R_)
    elif L == 'X':
        s += rect(x, y, w, h, W_) + rect(x + w * 0.42, y, w * 0.16, h, B_) + rect(x, y + h * 0.38, w, h * 0.24, B_)
    elif L == 'Y':
        # ICS Y: ten diagonal bands yellow/red running from lower hoist to upper fly ("/"),
        # yellow in the upper-hoist corner, red in the lower-fly corner
        s += rect(x, y, w, h, Y_)
        bw = (w + h) / 10
        for k in range(1, 10, 2):
            c1, c2 = k * bw, (k + 1) * bw
            s += f'<path d="M {x+c1:.1f} {y} L {x+c2:.1f} {y} L {x+c2-h:.1f} {y+h} L {x+c1-h:.1f} {y+h} Z" fill="{R_}"/>'
    elif L == 'Z':
        cx, cy = x + w / 2, y + h / 2
        s += f'<path d="M {x} {y} L {x+w} {y} L {cx} {cy} Z" fill="{Y_}"/><path d="M {x+w} {y} L {x+w} {y+h} L {cx} {cy} Z" fill="{B_}"/>'
        s += f'<path d="M {x} {y+h} L {x+w} {y+h} L {cx} {cy} Z" fill="{R_}"/><path d="M {x} {y} L {x} {y+h} L {cx} {cy} Z" fill="{K_}"/>'
    s += '</g>'
    if L in 'AB':
        s += f'<path d="M {x} {y} L {x+w} {y} L {x+w*0.75} {y+h/2} L {x+w} {y+h} L {x} {y+h} Z" fill="none" stroke="#475569"/>'
    else:
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#475569"/>'
    return s + '\n'

MEANINGS = {
 'A': 'I have a diver down; keep well clear at slow speed', 'B': 'I am taking in, discharging or carrying dangerous goods',
 'C': 'Affirmative (YES)', 'D': 'Keep clear of me; I am manoeuvring with difficulty', 'E': 'I am altering my course to starboard',
 'F': 'I am disabled; communicate with me', 'G': 'I require a pilot (fishing vsl: I am hauling nets)', 'H': 'I have a pilot on board',
 'I': 'I am altering my course to port', 'J': 'I am on fire and have dangerous cargo on board: keep well clear of me (or: leaking dangerous cargo)',
 'K': 'I wish to communicate with you', 'L': 'You should stop your vessel instantly', 'M': 'My vessel is stopped and making no way through the water',
 'N': 'Negative (NO)', 'O': 'Man overboard', 'P': 'In harbour: all persons should report on board as the vessel is about to proceed to sea (at sea, fishing vsl: my nets have come fast upon an obstruction)',
 'Q': 'My vessel is "healthy" and I request free pratique', 'R': '(ไม่มีความหมายเป็นสัญญาณอักษรเดียว — ใช้เป็น procedure signal "Received")',
 'S': 'I am operating astern propulsion', 'T': 'Keep clear of me; I am engaged in pair trawling', 'U': 'You are running into danger',
 'V': 'I require assistance', 'W': 'I require medical assistance', 'X': 'Stop carrying out your intentions and watch for my signals',
 'Y': 'I am dragging my anchor', 'Z': 'I require a tug (fishing vsl: I am shooting nets)'}

def short(t, n=40):
    words, lines, cur = t.split(), [], ''
    for wd in words:
        if len(cur) + len(wd) + 1 > n: lines.append(cur); cur = wd
        else: cur = (cur + ' ' + wd).strip()
    lines.append(cur)
    return lines

def flags_chart():
    cols, cw, ch = 3, 330, 108
    rows = 9
    w, h = cols * cw + 20, rows * ch + 70
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
         f'<text x="{w/2}" y="32" text-anchor="middle" font-size="20" font-weight="bold">ธงอักษร ICS และความหมายของสัญญาณอักษรเดียว (Single-letter signals)</text>\n')
    for i, L in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        c, r = i % cols, i // cols
        x, y = 15 + c * cw, 52 + r * ch
        s += f'<rect x="{x}" y="{y}" width="{cw-10}" height="{ch-8}" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>\n'
        s += flag(L, x + 10, y + 12)
        s += f'<text x="{x+46}" y="{y+82}" text-anchor="middle" font-size="15" font-weight="bold">{L}</text>\n'
        lines = short(MEANINGS[L].replace('&', 'and').replace('<', '&lt;'))
        for j, ln in enumerate(lines[:5]):
            s += f'<text x="{x+92}" y="{y+26+j*17}" font-size="11.5">{ln}</text>\n'
    # code pennant
    x, y = 15 + 2 * cw, 52 + 8 * ch
    s += f'<rect x="{x}" y="{y}" width="{cw-10}" height="{ch-8}" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>\n'
    s += pennant('ANS', x + 10, y + 18, 90, 44)
    s += f'<text x="{x+110}" y="{y+30}" font-size="11.5">Code / Answering pennant</text><text x="{x+110}" y="{y+47}" font-size="11.5">ตอบรับ · แสดงว่าใช้ ICS</text><text x="{x+110}" y="{y+64}" font-size="11.5">ใช้เป็นจุดทศนิยมกับตัวเลข</text>\n'
    open(os.path.join(OUT, 'ics-flags.svg'), 'w').write(s + '</svg>\n')

def pennant(kind, x, y, w=120, h=56):
    """ICS numeral pennant (kind '0'-'9'), answering pennant ('ANS') or substitute ('S1','S2','S3')"""
    c = next(_cid)
    if kind.startswith('S'):
        shape = f'M {x} {y} L {x+w} {y+h/2} L {x} {y+h} Z'          # substitutes are triangular
    else:
        shape = f'M {x} {y} L {x+w} {y+h/4} L {x+w} {y+3*h/4} L {x} {y+h} Z'   # tapered, blunt fly
    def rect(xx, yy, ww, hh, col): return f'<rect x="{xx:.1f}" y="{yy:.1f}" width="{ww:.1f}" height="{hh:.1f}" fill="{col}"/>'
    s = f'<clipPath id="p{c}"><path d="{shape}"/></clipPath><g clip-path="url(#p{c})">'
    if kind == '1':
        s += rect(x, y, w, h, W_) + f'<circle cx="{x+0.3*w:.1f}" cy="{y+h/2:.1f}" r="{0.3*h:.1f}" fill="{R_}"/>'
    elif kind == '2':
        s += rect(x, y, w, h, B_) + f'<circle cx="{x+0.3*w:.1f}" cy="{y+h/2:.1f}" r="{0.3*h:.1f}" fill="{W_}"/>'
    elif kind == '3':
        s += rect(x, y, w / 3, h, R_) + rect(x + w / 3, y, w / 3, h, W_) + rect(x + 2 * w / 3, y, w / 3 + 1, h, B_)
    elif kind in '48':
        bg, fg = (R_, W_) if kind == '4' else (W_, R_)
        s += rect(x, y, w, h, bg) + rect(x, y + 3 * h / 8, w, h / 4, fg) + rect(x + 0.21 * w, y, 0.14 * w, h, fg)
    elif kind == '5':
        s += rect(x, y, w / 2, h, Y_) + rect(x + w / 2, y, w / 2 + 1, h, B_)
    elif kind == '6':
        s += rect(x, y, w, h / 2, K_) + rect(x, y + h / 2, w, h / 2, W_)
    elif kind == '7':
        s += rect(x, y, w, h / 2, Y_) + rect(x, y + h / 2, w, h / 2, R_)
    elif kind == '9':
        s += rect(x, y, w / 2, h / 2, W_) + rect(x + w / 2, y, w / 2 + 1, h / 2, K_) + rect(x, y + h / 2, w / 2, h / 2, R_) + rect(x + w / 2, y + h / 2, w / 2 + 1, h / 2, Y_)
    elif kind == '0':
        s += rect(x, y, w, h, Y_) + rect(x + w / 3, y, w / 3, h, R_)
    elif kind == 'ANS':
        for k in range(5): s += rect(x + k * w / 5, y, w / 5 + 0.5, h, R_ if k % 2 == 0 else W_)
    elif kind == 'S1':
        s += f'<path d="{shape}" fill="{B_}"/><path d="M {x} {y+0.17*h:.1f} L {x+0.64*w:.1f} {y+h/2:.1f} L {x} {y+0.83*h:.1f} Z" fill="{Y_}"/>'
    elif kind == 'S2':
        s += rect(x, y, w / 2, h, B_) + rect(x + w / 2, y, w / 2, h, W_)
    elif kind == 'S3':
        s += rect(x, y, w, h, W_) + rect(x, y + h / 3, w, h / 3, K_)
    s += '</g>'
    return s + f'<path d="{shape}" fill="none" stroke="#475569"/>\n'

PENNANTS = [('1', 'ขาว · วงกลมแดง'), ('2', 'น้ำเงิน · วงกลมขาว'), ('3', 'แดง–ขาว–น้ำเงิน (แนวตั้ง)'), ('4', 'แดง · กากบาทขาว'),
            ('5', 'เหลือง (ด้านเสา) | น้ำเงิน'), ('6', 'ดำ (บน) / ขาว (ล่าง)'), ('7', 'เหลือง (บน) / แดง (ล่าง)'), ('8', 'ขาว · กากบาทแดง'),
            ('9', 'สี่ส่วน: ขาว ดำ / แดง เหลือง'), ('0', 'เหลือง–แดง–เหลือง (แนวตั้ง)')]

def pennants_chart():
    w, h = 1000, 870
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
         f'<text x="{w/2}" y="32" text-anchor="middle" font-size="20" font-weight="bold">ธงตัวเลข (numeral pennants) ธงแทน (substitutes) และธงตอบรับ — ICS</text>\n'
         '<text x="500" y="54" text-anchor="middle" font-size="12.5" fill="#334155">ชุดธงสัญญาณ 1 ชุด = ธงอักษร 26 + ธงตัวเลข 10 + ธงแทน 3 + answering pennant 1 (ICS Chapter 1)</text>\n')
    s += '<text x="24" y="86" font-size="15" font-weight="bold" fill="#1e3a8a">1) Numeral pennants — ธงชายรูปเรียว ปลายตัด (ด้านซ้าย = ด้านเสา/hoist)</text>\n'
    for i, (k, desc) in enumerate(PENNANTS):
        c, r = i % 5, i // 5
        x, y = 24 + c * 194, 100 + r * 118
        s += f'<rect x="{x}" y="{y}" width="184" height="108" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>\n'
        s += pennant(k, x + 14, y + 12)
        s += f'<text x="{x+158}" y="{y+48}" font-size="24" font-weight="bold" fill="#0f172a">{k}</text>\n'
        s += f'<text x="{x+92}" y="{y+94}" text-anchor="middle" font-size="11.5">{desc}</text>\n'
    y0 = 352
    s += f'<text x="24" y="{y0}" font-size="15" font-weight="bold" fill="#1e3a8a">2) Substitutes (ธงแทน รูปสามเหลี่ยม) และ Code / Answering pennant</text>\n'
    subs = [('S1', '1st substitute', 'น้ำเงิน ขอบรอบสามเหลี่ยมเหลือง'), ('S2', '2nd substitute', 'น้ำเงิน (ด้านเสา) | ขาว'),
            ('S3', '3rd substitute', 'ขาว · แถบดำแนวนอนกลาง'), ('ANS', 'Code / Answering', 'แดง–ขาว 5 แถบแนวตั้ง')]
    for i, (k, name, desc) in enumerate(subs):
        x, y = 24 + i * 242, y0 + 14
        s += f'<rect x="{x}" y="{y}" width="232" height="112" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>\n'
        s += pennant(k, x + 12, y + 14, 96, 56)
        s += f'<text x="{x+116}" y="{y+40}" font-size="12.5" font-weight="bold">{name}</text>\n'
        s += f'<text x="{x+116}" y="{y+98}" text-anchor="middle" font-size="11.5">{desc}</text>\n'
    y0 = 512
    s += f'<text x="24" y="{y0}" font-size="15" font-weight="bold" fill="#1e3a8a">3) ตัวอย่างการใช้ธงแทน (อ่านจากบนลงล่าง)</text>\n'
    examples = [('"VV"', [('F', 'V'), ('S', 'S1')], 'ธงแทนที่ 1 ซ้ำธงบนสุด'),
                ('"1100"', [('P', '1'), ('S', 'S1'), ('P', '0'), ('S', 'S3')], 'S1 ซ้ำ 1 · S3 ซ้ำผืนที่ 3 (เลข 0)'),
                ('"L 2330"', [('F', 'L'), ('P', '2'), ('P', '3'), ('S', 'S2'), ('P', '0')], 'S2 ตามหลังธงตัวเลข → ซ้ำเลขตัวที่ 2 (3)')]
    for i, (title, items, note) in enumerate(examples):
        x = 40 + i * 320
        s += f'<text x="{x}" y="{y0+30}" font-size="14" font-weight="bold">{title}</text>\n'
        s += f'<line x1="{x+6}" y1="{y0+40}" x2="{x+6}" y2="{y0+52+len(items)*42}" stroke="#334155" stroke-width="2"/>\n'
        for j, (t, k) in enumerate(items):
            yy = y0 + 46 + j * 42
            if t == 'F':
                s += flag(k, x + 8, yy, 54, 36)
                lab = k
            else:
                s += pennant(k, x + 8, yy, 70, 36)
                lab = {'S1': '1st sub', 'S2': '2nd sub', 'S3': '3rd sub'}.get(k, k)
            s += f'<text x="{x+92}" y="{yy+23}" font-size="12">{lab}</text>\n'
        s += f'<text x="{x}" y="{y0+290}" font-size="11.5" fill="#334155">{note}</text>\n'
    s += '<text x="24" y="850" font-size="12" fill="#334155">ธงแทนใช้ซ้ำธง "ประเภทเดียวกัน" (อักษรหรือตัวเลข) ที่อยู่ติดเหนือมัน · ในกลุ่มเดียวใช้ธงแทนแต่ละผืนได้ครั้งเดียว · answering pennant ที่ใช้เป็นจุดทศนิยมไม่นับ</text>\n'
    open(os.path.join(OUT, 'ics-pennants-substitutes.svg'), 'w').write(s + '</svg>\n')

MORSE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--',
         'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
         '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----'}

def morse_chart():
    keys = list(MORSE.keys())
    cols, cw, ch = 4, 245, 42
    rows = (len(keys) + cols - 1) // cols
    w, h = cols * cw + 20, rows * ch + 170
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
         f'<text x="{w/2}" y="32" text-anchor="middle" font-size="20" font-weight="bold">รหัสมอร์ส (Morse code) — จุด = 1 หน่วย, ขีด = 3 หน่วย</text>\n')
    for i, k in enumerate(keys):
        c, r = i // rows, i % rows
        x, y = 20 + c * cw, 60 + r * ch
        s += f'<text x="{x}" y="{y+22}" font-size="18" font-weight="bold" fill="#1e3a8a">{k}</text>\n'
        xx = x + 36
        for sym in MORSE[k]:
            if sym == '.':
                s += f'<circle cx="{xx+5}" cy="{y+16}" r="5" fill="#111"/>'; xx += 18
            else:
                s += f'<rect x="{xx}" y="{y+11}" width="30" height="10" rx="3" fill="#111"/>'; xx += 40
        s += '\n'
    yb = 60 + rows * ch + 20
    s += f'<rect x="20" y="{yb}" width="{w-40}" height="92" rx="8" fill="#fef2f2" stroke="#b91c1c"/>\n'
    s += f'<text x="36" y="{yb+28}" font-size="16" font-weight="bold" fill="#b91c1c">SOS (···−−−···) — ส่งต่อเนื่องเป็นสัญญาณเดียว ไม่เว้นช่องระหว่างตัวอักษร (COLREG Annex IV / ICS)</text>\n'
    xx = 40
    for sym in '...---...':
        if sym == '.':
            s += f'<circle cx="{xx+6}" cy="{yb+58}" r="6" fill="#b91c1c"/>'; xx += 22
        else:
            s += f'<rect x="{xx}" y="{yb+52}" width="36" height="12" rx="3" fill="#b91c1c"/>'; xx += 46
    s += f'\n<text x="{xx+20}" y="{yb+64}" font-size="13">ช่วงห่าง: ภายในตัวอักษร 1 หน่วย · ระหว่างตัวอักษร 3 หน่วย · ระหว่างคำ 7 หน่วย</text>\n'
    open(os.path.join(OUT, 'morse-code.svg'), 'w').write(s + '</svg>\n')

if __name__ == '__main__':
    flags_chart(); pennants_chart(); morse_chart(); print('ok')
