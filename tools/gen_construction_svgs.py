"""ภาพประกอบบท 3.2.2 โครงสร้างเรือ (Ship construction)"""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"


def head(w, h, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
            '<defs><marker id="ar" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker>'
            '<marker id="arR" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#b91c1c"/></marker>'
            '<marker id="arB" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#1d4ed8"/></marker></defs>\n'
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


def callout(x, y, tx, ty, t, anchor='start', col='#1e3a8a'):
    return line(x, y, tx, ty, '#64748b', 1) + f'<circle cx="{x}" cy="{y}" r="3" fill="#0f172a"/>' + txt(tx + (4 if anchor == 'start' else -4), ty + 4, t, 11.5, anchor, col, True)


# ---------------------------------------------------------------- profile
def profile():
    w, h = 1000, 560
    s = head(w, h, 'ภาพด้านข้างเรือสินค้าทั่วไป (General cargo ship profile) และชื่อส่วนต่าง ๆ')
    keel, deck = 380, 220
    hull = f'M 110 {keel} L 840 {keel} Q 880 {keel} 900 {keel-40} L 930 {deck-30} L 880 {deck-30} L 880 {deck} L 150 {deck-10} L 150 {deck-40} L 90 {deck-40} L 80 {deck} Q 75 {keel-50} 110 {keel} Z'
    s += f'<path d="{hull}" fill="#f1f5f9" stroke="#0f172a" stroke-width="2.5"/>'
    # bulbous bow
    s += f'<path d="M 870 {keel} Q 925 {keel-5} 915 {keel-40} Q 905 {keel-55} 890 {keel-50}" fill="#f1f5f9" stroke="#0f172a" stroke-width="2"/>'
    # double bottom
    s += line(110, keel - 25, 860, keel - 25, '#475569', 1.5)
    # bulkheads
    for x in (150, 300, 440, 580, 720, 830):
        s += line(x, deck - 8, x, keel, '#b91c1c', 2.5)
    # engine, holds labels
    s += txt(232, 318, 'ห้องเครื่อง (E/R)', 12, 'middle', '#0f172a', True)
    for i, x in enumerate((370, 510, 650, 775)):
        s += txt(x, 320, f'ระวาง {4-i}' if False else f'Hold No.{4-i}', 12, 'middle', '#0f172a', True)
    s += txt(865, 320, 'Fore', 10.5, 'middle') + txt(865, 333, 'peak', 10.5, 'middle')
    s += txt(132, 278, 'Aft', 10.5, 'middle') + txt(132, 291, 'peak', 10.5, 'middle')
    # superstructure
    s += rect(150, deck - 120, 100, 110, '#e2e8f0', '#0f172a', 2) + rect(160, deck - 150, 80, 30, '#cbd5e1', '#0f172a', 2)
    s += rect(180, deck - 172, 14, 22, '#475569', '#0f172a', 1)
    # hatch coamings
    for x in (320, 460, 600, 740):
        s += rect(x, deck - 22, 90, 14, '#94a3b8', '#0f172a', 1.5)
    # rudder & propeller
    s += f'<path d="M 95 {keel-80} L 70 {keel-80} L 65 {keel-10} L 95 {keel-10} Z" fill="#cbd5e1" stroke="#0f172a" stroke-width="2"/>'
    s += f'<ellipse cx="110" cy="{keel-45}" rx="6" ry="30" fill="#94a3b8" stroke="#0f172a"/>'
    s += line(110, keel - 45, 225, keel - 45, '#475569', 3)
    s += txt(160, keel - 52, 'shaft', 10, 'middle', '#334155')
    # waterline
    s += line(40, 300, 960, 300, '#0284c7', 1.5, '8 5')
    labels = [(880, deck - 30, 990, 80, 'Forecastle (หัวเรือยก)', 'end'), (930, deck - 30, 990, 112, 'Stem (หัวเรือ)', 'end'),
              (905, keel - 30, 990, 440, 'Bulbous bow', 'end'), (830, keel - 60, 820, 450, 'Collision bulkhead', 'end'),
              (120, deck - 40, 20, 92, 'Poop (ท้ายเรือยก)', 'start'), (200, deck - 150, 300, 90, 'Navigation bridge / ที่พัก', 'start'),
              (365, deck - 15, 380, 140, 'Hatch coaming / hatchway', 'start'), (500, keel - 12, 520, 470, 'Double bottom tanks', 'start'),
              (70, keel - 50, 20, 440, 'Rudder', 'start'), (110, keel - 20, 70, 500, 'Propeller', 'start'), (300, keel - 100, 300, 500, 'Watertight bulkheads', 'start'),
              (700, 300, 700, 520, 'แนวน้ำ (waterline)', 'start')]
    for x, y, tx, ty, t, an in labels:
        s += callout(x, y, tx, ty, t, an)
    save('cons-ship-profile.svg', s)


# ---------------------------------------------------------------- midship section
def midship():
    w, h = 1000, 640
    s = head(w, h, 'ภาคตัดกลางลำ (Midship section) เรือสินค้าทั่วไปแบบโครงตามขวาง — ชื่อโครงสร้าง')
    cx, top, keel, B = 480, 120, 520, 260
    L, Rr = cx - B, cx + B
    # shell
    s += f'<path d="M {L} {top} L {L} {keel-60} Q {L} {keel} {L+60} {keel} L {Rr-60} {keel} Q {Rr} {keel} {Rr} {keel-60} L {Rr} {top}" fill="none" stroke="#0f172a" stroke-width="5"/>'
    # deck with camber
    s += f'<path d="M {L} {top} Q {cx} {top-18} {Rr} {top}" fill="none" stroke="#0f172a" stroke-width="4"/>'
    # bulwark
    s += line(L, top, L, top - 40, '#0f172a', 3) + line(Rr, top, Rr, top - 40, '#0f172a', 3)
    # hatch coaming
    s += line(cx - 120, top - 14, cx - 120, top - 60, '#0f172a', 4) + line(cx + 120, top - 14, cx + 120, top - 60, '#0f172a', 4)
    # tank top
    db = keel - 70
    s += line(L + 40, db, Rr - 40, db, '#0f172a', 4)
    s += f'<path d="M {L+40} {db} L {L} {db+30}" stroke="#0f172a" stroke-width="4"/>' + f'<path d="M {Rr-40} {db} L {Rr} {db+30}" stroke="#0f172a" stroke-width="4"/>'
    # centre girder and side girders, floor
    s += line(cx, db, cx, keel, '#0f172a', 4)
    for gx in (cx - 150, cx + 150):
        s += line(gx, db, gx, keel, '#475569', 2.5)
    s += f'<rect x="{L+50}" y="{db+3}" width="{2*B-100}" height="{keel-db-6}" fill="#bfdbfe" opacity="0.35"/>'
    # frames
    for sx in (L + 14, Rr - 14):
        s += line(sx, top + 30, sx, db - 10, '#b45309', 6)
    # beam brackets & bilge brackets
    s += f'<path d="M {L} {top+5} L {L+60} {top+5} L {L} {top+60} Z" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.5"/>'
    s += f'<path d="M {Rr} {top+5} L {Rr-60} {top+5} L {Rr} {top+60} Z" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.5"/>'
    s += f'<path d="M {L} {db-50} L {L+40} {db} L {L} {db} Z" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.5"/>'
    s += f'<path d="M {Rr} {db-50} L {Rr-40} {db} L {Rr} {db} Z" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.5"/>'
    # beam
    s += line(L + 20, top + 8, cx - 125, top - 2, '#b45309', 6) + line(cx + 125, top - 2, Rr - 20, top + 8, '#b45309', 6)
    # pillar
    s += line(cx - 160, top + 4, cx - 160, db, '#475569', 5)
    # bilge keel
    s += f'<path d="M {L+20} {keel-25} L {L-10} {keel+5}" stroke="#0f172a" stroke-width="6"/>'
    # stringer plate highlight & sheer strake
    s += line(L, top, L + 70, top - 5, '#15803d', 7) + line(L, top, L, top + 60, '#7c3aed', 8)
    s += line(L + 60, keel, L + 160, keel, '#c2410c', 8) + line(cx - 30, keel, cx + 30, keel, '#1d4ed8', 9)
    labels = [(cx, keel, cx + 40, 600, 'Flat plate keel (กระดูกงูแผ่นเรียบ)', 'start'),
              (L + 110, keel, 8, 620, 'Garboard strake (แผ่นข้างกระดูกงู)', 'start'),
              (L + 25, keel - 25, 8, 575, 'Bilge strake + Bilge keel', 'start'),
              (cx + 150, keel - 30, 760, 590, 'Side girder', 'start'),
              (cx + 2, db + 30, 760, 560, 'Centre girder', 'start'),
              (cx + 200, db + 40, 760, 530, 'Plate floor (ในถังท้องเรือ)', 'start'),
              (cx + 230, db, 760, 495, 'Tank top / inner bottom', 'start'),
              (Rr - 20, db + 15, 760, 465, 'Margin plate', 'start'),
              (Rr - 14, 300, 760, 300, 'Frame (โครงข้าง)', 'start'),
              (Rr - 10, db - 20, 760, 425, 'Bilge (tank side) bracket', 'start'),
              (L, top + 40, 8, 210, 'Sheer strake', 'start'),
              (L + 40, top - 3, 8, 170, 'Stringer plate', 'start'),
              (Rr - 40, top + 15, 760, 150, 'Beam knee (bracket)', 'start'),
              (cx + 180, top + 4, 760, 115, 'Deck beam', 'start'),
              (cx + 60, top - 16, 760, 80, 'Deck plating (มี camber)', 'start'),
              (cx + 120, top - 40, 640, 56, 'Hatch coaming', 'start'),
              (Rr, top - 30, 760, 190, 'Bulwark', 'start'),
              (cx - 160, 300, 8, 330, 'Pillar (เสาค้ำ)', 'start'),
              (L, 400, 8, 400, 'Side shell plating', 'start'),
              (cx - 80, keel, 330, 630, 'Bottom shell plating', 'start')]
    for x, y, tx, ty, t, a in labels:
        s += callout(x, y, tx, ty, t, a)
    save('cons-midship-section.svg', s)


# ---------------------------------------------------------------- framing systems
def framing():
    w, h = 1000, 480
    s = head(w, h, 'ระบบโครงเรือ: โครงตามขวาง (Transverse) กับ โครงตามยาว (Longitudinal)')
    for k, (x0, title, col) in enumerate(((40, 'Transverse framing', '#b45309'), (520, 'Longitudinal framing (Isherwood)', '#1d4ed8'))):
        s += txt(x0 + 220, 66, title, 15, 'middle', col, True)
        s += f'<path d="M {x0} 100 L {x0+440} 100 L {x0+440} 320 L {x0} 320 Z" fill="#f8fafc" stroke="#0f172a" stroke-width="2"/>'
        if k == 0:
            for i in range(12):
                x = x0 + 20 + i * 36
                s += line(x, 100, x, 320, col, 4)
            s += line(x0, 210, x0 + 440, 210, '#475569', 6) + rect(x0 + 170, 191, 100, 17, '#ffffff', '#cbd5e1', 1, 4) + txt(x0 + 220, 204, 'stringer (บางเรือ)', 10.5, 'middle', '#334155')
        else:
            for j in range(8):
                y = 115 + j * 27
                s += line(x0, y, x0 + 440, y, col, 4)
            for x in (x0 + 110, x0 + 330):
                s += rect(x - 8, 100, 16, 220, '#94a3b8', '#0f172a', 1.5)
            s += txt(x0 + 110, 340, 'web frame / transverse', 10.5, 'middle', '#334155') + txt(x0 + 330, 340, 'ระยะห่างมาก', 10.5, 'middle', '#334155')
        s += txt(x0 + 220, 360 if k == 0 else 360, '← หัว/ท้ายเรือ →', 11, 'middle', '#475569')
    A = ['โครงตามขวางระยะถี่ (frame spacing ~0.6–0.9 m)', 'แข็งแรงต่อแรงด้านข้าง/แรงกดน้ำ, ง่ายต่อการสร้าง', 'ช่องระวางโล่ง เหมาะสินค้าทั่วไป เรือเล็ก-กลาง',
         'ความแข็งแรงตามยาวต่ำกว่า สำหรับเรือยาวต้องแผ่นหนา']
    B = ['longitudinals วิ่งตามยาวระยะถี่ มี web frames ห่าง ๆ', 'แข็งแรงตามยาวสูง (ต้าน hogging/sagging) น้ำหนักเหล็กน้อย', 'เหมาะเรือยาว: tanker, bulk carrier, container',
         'ระบบผสม (combined): ท้อง/ดาดฟ้าตามยาว ด้านข้างตามขวาง']
    for i, a in enumerate(A):
        s += txt(60, 395 + i * 21, '• ' + a, 12)
    for i, b in enumerate(B):
        s += txt(540, 395 + i * 21, '• ' + b, 12)
    save('cons-framing-systems.svg', s)


# ---------------------------------------------------------------- stresses
def stresses():
    w, h = 1000, 520
    s = head(w, h, 'แรงและความเค้นที่กระทำต่อตัวเรือ (Stresses on the hull)')
    cells = [('Hogging', 'ยอดคลื่นกลางลำ|น้ำหนักมากที่หัว-ท้าย', 'hog'), ('Sagging', 'ท้องคลื่นกลางลำ|น้ำหนักมากกลางลำ', 'sag'),
             ('Racking', 'การโคลงทำให้ภาคตัด|บิดเป็นสี่เหลี่ยมด้านขนาน', 'rack'), ('Panting', 'แรงดันน้ำเปลี่ยนเป็นจังหวะที่หัว/ท้าย|แผ่นเปลือกขยับเข้าออก', 'pant'),
             ('Pounding / Slamming', 'ท้องหัวเรือกระแทกน้ำ|เมื่อโต้คลื่น', 'pound'), ('Torsion', 'ตัวเรือบิดตามยาว|(คลื่นเฉียง, ช่องเปิดกว้าง)', 'tors'),
             ('Local stresses', 'น้ำหนักเฉพาะจุด สินค้าหนัก|ปั้นจั่น เข้าอู่ (docking)', 'local'), ('Vibration / fatigue', 'เครื่องยนต์ ใบจักร คลื่น|รอยร้าวจากความล้า', 'vib')]
    for i, (t, d, k) in enumerate(cells):
        c, r = i % 4, i // 4
        x, y = 30 + c * 240, 60 + r * 220
        s += rect(x, y, 220, 200, '#f8fafc', '#94a3b8', 1, 10)
        s += txt(x + 110, y + 24, t, 14, 'middle', '#0f172a', True)
        cx, cy = x + 110, y + 100
        if k == 'hog':
            s += f'<path d="M {x+20} {cy+20} Q {cx} {cy-30} {x+200} {cy+20}" fill="none" stroke="#b91c1c" stroke-width="12" stroke-linecap="round"/>'
        elif k == 'sag':
            s += f'<path d="M {x+20} {cy-20} Q {cx} {cy+30} {x+200} {cy-20}" fill="none" stroke="#1d4ed8" stroke-width="12" stroke-linecap="round"/>'
        elif k == 'rack':
            s += f'<polygon points="{cx-50},{cy-40} {cx+40},{cy-40} {cx+60},{cy+40} {cx-30},{cy+40}" fill="#e2e8f0" stroke="#0f172a" stroke-width="2"/>'
            s += f'<rect x="{cx-50}" y="{cy-40}" width="90" height="80" fill="none" stroke="#94a3b8" stroke-dasharray="4 3"/>'
        elif k == 'pant':
            s += f'<path d="M {x+30} {cy-30} L {x+150} {cy-30} Q {x+200} {cy} {x+150} {cy+30} L {x+30} {cy+30}" fill="#e2e8f0" stroke="#0f172a" stroke-width="2"/>'
            for dy in (-18, 18):
                s += line(x + 205, cy + dy, x + 180, cy + dy * 0.6, '#b91c1c', 2, mk='arR')
        elif k == 'pound':
            s += f'<path d="M {x+30} {cy+10} L {x+180} {cy-30}" stroke="#0f172a" stroke-width="10"/>'
            s += f'<path d="M {x+20} {cy+40} Q {x+100} {cy+20} {x+200} {cy+40}" fill="none" stroke="#0369a1" stroke-width="3"/>'
            s += line(x + 160, cy + 30, x + 160, cy - 10, '#b91c1c', 3, mk='arR')
        elif k == 'tors':
            s += f'<polygon points="{x+30},{cy-25} {x+190},{cy-40} {x+190},{cy+10} {x+30},{cy+25}" fill="#e2e8f0" stroke="#0f172a" stroke-width="2"/>'
            s += f'<path d="M {x+40} {cy+45} q -20 -10 0 -20" fill="none" stroke="#b91c1c" stroke-width="2" marker-end="url(#arR)"/>'
        elif k == 'local':
            s += rect(x + 30, cy, 160, 30, '#e2e8f0', '#0f172a', 2) + rect(x + 90, cy - 40, 40, 40, '#fde68a', '#92400e', 2)
            s += line(x + 110, cy - 60, x + 110, cy - 42, '#b91c1c', 3, mk='arR')
        else:
            for j in range(6):
                s += f'<path d="M {x+30+j*27} {cy} q 7 -20 14 0 q 7 20 13 0" fill="none" stroke="#7c3aed" stroke-width="2.5"/>'
        for j, part in enumerate(d.split('|')):
            s += txt(x + 110, y + 166 + j * 16, part, 11, 'middle', '#334155')
    save('cons-stresses.svg', s)


# ---------------------------------------------------------------- dimensions
def dimensions():
    w, h = 1000, 580
    s = head(w, h, 'ขนาดหลักของเรือ (Principal dimensions)')
    keel, deck, wl = 300, 170, 240
    s += f'<path d="M 120 {keel} L 760 {keel} Q 800 {keel} 820 {keel-40} L 860 {deck} L 120 {deck+5} L 100 {deck} Q 90 {keel-60} 120 {keel} Z" fill="#f1f5f9" stroke="#0f172a" stroke-width="2.5"/>'
    s += line(60, wl, 900, wl, '#0284c7', 1.8, '8 5')
    s += line(100, 120, 860, 120, '#b91c1c', 1.5, mk='arR') + line(860, 120, 100, 120, '#b91c1c', 1.5, mk='arR') + txt(480, 112, 'LOA — ความยาวตลอดลำ', 12, 'middle', '#b91c1c', True)
    s += line(120, 350, 822, 350, '#1d4ed8', 1.5, mk='arB') + line(822, 350, 120, 350, '#1d4ed8', 1.5, mk='arB') + txt(470, 368, 'LBP — ระหว่าง AP (แกนหางเสือ) ถึง FP (หัวเรือที่แนวน้ำบรรทุกฤดูร้อน)', 12, 'middle', '#1d4ed8', True)
    for x, lab in ((120, 'AP'), (822, 'FP')):
        s += line(x, 130, x, 345, '#1d4ed8', 1, '4 3') + txt(x, 390, lab, 12, 'middle', '#1d4ed8', True)
    mid = (120 + 822) / 2                      # กลางลำ (amidships) = กึ่งกลาง LBP
    dk = deck + 5 - (mid - 120) / (860 - 120) * 5   # ระดับดาดฟ้าที่ข้างเรือกลางลำ
    s += line(mid, deck - 6, mid, keel + 20, '#64748b', 1, '2 4') + txt(mid, keel + 34, '⊗ กลางลำ (amidships)', 11, 'middle', '#475569')
    s += line(mid + 30, dk, mid + 30, wl, '#15803d', 1.5, mk='ar') + txt(mid + 36, (dk + wl) / 2 + 4, 'Freeboard (กลางลำ)', 11.5, 'start', '#15803d', True)
    s += line(mid + 30, wl, mid + 30, keel, '#7c3aed', 1.5, mk='ar') + txt(mid + 36, (wl + keel) / 2 + 6, 'Draught', 11.5, 'start', '#7c3aed', True)
    s += line(mid - 30, dk, mid - 30, keel, '#0f172a', 1.5, mk='ar') + txt(mid - 36, (dk + keel) / 2, 'Depth (moulded)', 11.5, 'end', '#0f172a', True)
    s += txt(700, 160, 'Sheer — ดาดฟ้าโค้งขึ้นที่หัว/ท้าย', 11.5, 'middle', '#334155')
    # cross section inset
    cx, cy = 680, 470
    s += f'<path d="M {cx-120} {cy-40} L {cx-110} {cy+40} Q {cx-105} {cy+60} {cx-80} {cy+62} L {cx+80} {cy+62} Q {cx+105} {cy+60} {cx+110} {cy+40} L {cx+120} {cy-40}" fill="#f1f5f9" stroke="#0f172a" stroke-width="2"/>'
    s += f'<path d="M {cx-120} {cy-40} Q {cx} {cy-58} {cx+120} {cy-40}" fill="none" stroke="#0f172a" stroke-width="2"/>'
    s += txt(cx, cy - 62, 'Camber', 11, 'middle', '#334155', True)
    s += line(cx - 120, cy + 76, cx + 120, cy + 76, '#c2410c', 1.5, mk='ar') + txt(cx, cy + 96, 'Breadth (moulded/extreme)', 11.5, 'middle', '#c2410c', True)
    s += txt(cx - 130, cy, 'Flare/tumblehome', 11, 'end', '#334155')
    s += rect(40, 420, 330, 110, '#f8fafc', '#94a3b8', 1, 10)
    for i, t in enumerate(['Moulded = วัดถึงด้านในของแผ่นเปลือก', 'Extreme = วัดถึงด้านนอกสุด', 'GT/NT — ตาม Tonnage Convention 1969', '(ปริมาตร ไม่ใช่น้ำหนัก)', 'DWT/Δ — น้ำหนัก (ตัน)']):
        s += txt(54, 444 + i * 19, t, 12)
    save('cons-dimensions.svg', s)


# ---------------------------------------------------------------- bow and stern
def bow_stern():
    w, h = 1000, 520
    s = head(w, h, 'โครงสร้างส่วนหัว (Bow) และส่วนท้าย (Stern) — ชื่อที่ควรรู้')
    # bow
    s += txt(250, 66, 'ส่วนหัวเรือ', 15, 'middle', bold=True)
    s += f'<path d="M 60 120 L 380 120 L 440 110 L 410 300 Q 440 330 400 360 Q 360 370 330 350 L 60 350 Z" fill="#f1f5f9" stroke="#0f172a" stroke-width="2.5"/>'
    s += line(200, 120, 200, 350, '#b91c1c', 3) + txt(200, 380, 'Collision bulkhead', 11.5, 'middle', '#b91c1c', True)
    for y in (170, 220, 270):
        s += line(200, y, 405, y, '#475569', 3)
    s += txt(300, 196, 'Panting stringers / breasthooks', 11, 'middle', '#334155')
    s += rect(240, 125, 60, 40, '#e2e8f0', '#0f172a', 1.5) + txt(270, 150, 'chain locker', 9.5, 'middle')
    s += line(380, 135, 425, 175, '#0f172a', 4) + txt(440, 168, 'Hawse pipe', 11, 'start', '#0f172a', True)
    s += txt(300, 320, 'Fore peak tank', 12, 'middle', '#1e3a8a', True)
    s += txt(420, 380, 'Bulbous bow', 11.5, 'middle', '#0f172a', True)
    s += txt(450, 120, 'Stem', 11.5, 'start', '#0f172a', True)
    # stern
    s += txt(750, 66, 'ส่วนท้ายเรือ', 15, 'middle', bold=True)
    s += f'<path d="M 940 120 L 600 120 L 560 160 L 580 260 L 640 300 L 940 350 Z" fill="#f1f5f9" stroke="#0f172a" stroke-width="2.5"/>'
    s += line(800, 120, 800, 350, '#b91c1c', 3) + txt(800, 380, 'Aft peak bulkhead', 11.5, 'middle', '#b91c1c', True)
    s += f'<path d="M 640 300 L 640 360 L 600 360" fill="none" stroke="#0f172a" stroke-width="5"/>'
    s += txt(655, 395, 'Stern frame / sole piece', 11, 'start', '#0f172a', True)
    s += f'<path d="M 625 255 L 590 255 L 585 345 L 625 345 Z" fill="#cbd5e1" stroke="#0f172a" stroke-width="2"/>' + txt(580, 300, 'Rudder', 11.5, 'end', '#0f172a', True)
    s += line(605, 150, 605, 255, '#0f172a', 5) + txt(598, 205, 'Rudder stock', 11, 'end', '#0f172a', True)
    s += f'<ellipse cx="655" cy="320" rx="7" ry="28" fill="#94a3b8" stroke="#0f172a"/>' + txt(668, 340, 'Propeller', 11, 'start', '#0f172a', True)
    s += line(662, 320, 790, 300, '#475569', 4) + txt(720, 300, 'Stern tube / shaft', 10.5, 'middle', '#334155')
    s += txt(700, 200, 'Aft peak tank', 12, 'middle', '#1e3a8a', True)
    s += txt(700, 150, 'Steering gear room', 11.5, 'middle', '#0f172a', True)
    s += rect(40, 420, 920, 90, '#f8fafc', '#94a3b8', 1, 10)
    for i, t in enumerate(['ส่วนหัวรับแรง panting และ pounding → เสริมด้วย panting beams/stringers, breasthooks, โครงถี่ขึ้น, แผ่นหนาขึ้น (และพื้นหัวเรือรับ slamming)',
                           'ส่วนท้ายรับแรงจากใบจักร/หางเสือและการสั่น → stern frame แข็งแรง, rudder stock + carrier + bearings, stern tube + seals (ป้องกันน้ำมันรั่ว)',
                           'Collision bulkhead และ aft peak bulkhead คือผนังกั้นน้ำที่ต้องมีทุกเรือ — ช่องว่างหน้า/ท้ายสุดมักเป็นถังอับเฉาปรับ trim']):
        s += txt(56, 446 + i * 24, t, 12)
    save('cons-bow-stern.svg', s)


# ---------------------------------------------------------------- rudder types
def rudders():
    w, h = 1000, 420
    s = head(w, h, 'ชนิดของหางเสือ (Rudder types)')
    for i, (t, d, off) in enumerate((('Unbalanced', 'แกนอยู่ขอบหน้า แรงบิดสูง', 0.0), ('Semi-balanced (horn type)', 'บางส่วนอยู่หน้าแกน มี horn', 0.2), ('Balanced / spade', 'ประมาณ 20–30% อยู่หน้าแกน', 0.25))):
        x = 100 + i * 300
        s += txt(x + 80, 70, t, 14, 'middle', '#0f172a', True)
        rx = x + 40
        wid = 120
        ax = rx + wid * off
        s += rect(rx, 120, wid, 200, '#cbd5e1', '#0f172a', 2, 6)
        if i == 1:
            s += rect(rx - 4, 100, wid * off + 8, 110, '#94a3b8', '#0f172a', 2)
            s += txt(rx - 8, 160, 'horn', 11, 'end', '#334155')
        s += line(ax, 80, ax, 330, '#b91c1c', 3, '6 4')
        s += txt(ax + 4, 95, 'แกนหมุน', 10.5, 'start', '#b91c1c', True)
        if i == 0:
            for y in (150, 230, 300):
                s += f'<circle cx="{ax}" cy="{y}" r="6" fill="#0f172a"/>'
            s += txt(rx + wid + 6, 236, 'pintles/gudgeons', 10.5, 'start', '#334155')
        s += txt(x + 80, 360, d, 12, 'middle', '#334155')
        s += txt(x + 80, 342, '← หัวเรือ', 10.5, 'middle', '#475569')
    s += txt(500, 400, 'ส่วนประกอบ: rudder stock, rudder carrier (รับน้ำหนัก), bearings, pintles/gudgeons, stopper (จำกัดมุม), steering gear (ดู 1.1.6)', 12, 'middle')
    save('cons-rudder-types.svg', s)


if __name__ == '__main__':
    profile(); midship(); framing(); stresses(); dimensions(); bow_stern(); rudders()
