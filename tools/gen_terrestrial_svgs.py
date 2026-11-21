"""สคริปต์สร้างภาพประกอบบทเดินเรือชายฝั่ง (terrestrial navigation)"""
import math, os
R = math.radians
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"

def head(w, h, title=None):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
    s += ('<defs>'
          '<marker id="a1" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#0f172a"/></marker>'
          '<marker id="a1b" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#1d4ed8"/></marker>'
          '<marker id="a1r" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#b91c1c"/></marker>'
          '<marker id="a1g" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#15803d"/></marker>'
          '</defs>\n')
    if title:
        s += f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{title}</text>\n'
    return s

def save(name, s):
    open(os.path.join(OUT, name), 'w').write(s + '</svg>\n')

def bearing_vec(b):
    return math.sin(R(b)), -math.cos(R(b))

def heads(x1, y1, x2, y2, col, n, gap=9, size=12, both=False):
    """วาดหัวลูกศร n หัวที่ปลายเส้น (x2,y2) ตามธรรมเนียม BR 45:
    1 หัว = water track, 2 หัว = ground track, 3 หัว = กระแสน้ำ / หัวคู่ = transferred position line"""
    L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    out = ''
    ends = [(x2, y2, ux, uy)] + ([(x1, y1, -ux, -uy)] if both else [])
    for ex, ey, vx, vy in ends:
        for k in range(n):
            tx, ty = ex - vx * k * gap, ey - vy * k * gap
            bx, by = tx - vx * size, ty - vy * size
            out += (f'<polygon points="{tx:.1f},{ty:.1f} {bx+(-vy)*size/2:.1f},{by+vx*size/2:.1f} '
                    f'{bx-(-vy)*size/2:.1f},{by-vx*size/2:.1f}" fill="{col}"/>\n')
    return out

def lat_long():
    w, h = 900, 560
    s = head(w, h, 'ละติจูด ลองจิจูด และ departure')
    cx, cy, r = 280, 300, 220
    tilt = R(20)
    def proj(lat, lon, lon0=-30):
        la, lo = R(lat), R(lon - lon0)
        x = math.cos(la) * math.sin(lo)
        y = math.sin(la) * math.cos(tilt) - math.cos(la) * math.cos(lo) * math.sin(tilt)
        z = math.cos(la) * math.cos(lo) * math.cos(tilt) + math.sin(la) * math.sin(tilt)
        return cx + r * x, cy - r * y, z
    def path(pts, col, wd=1.5, dash=False):
        out = ''; seg = []; fr = None
        for p in pts:
            x, y, z = proj(*p); f = z >= 0
            if fr is None: fr = f
            if f != fr:
                if len(seg) > 1:
                    d = 'M ' + ' L '.join(f'{a:.1f} {b:.1f}' for a, b in seg)
                    out += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wd}"' + ('' if fr else ' stroke-dasharray="4 4" opacity="0.35"') + '/>\n'
                seg = [seg[-1]] if seg else []; fr = f
            seg.append((x, y))
        if len(seg) > 1:
            d = 'M ' + ' L '.join(f'{a:.1f} {b:.1f}' for a, b in seg)
            out += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{wd}"' + ('' if fr else ' stroke-dasharray="4 4" opacity="0.35"') + '/>\n'
        return out
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#eff6ff" stroke="#1e3a8a" stroke-width="2"/>\n'
    for la in range(-60, 61, 30):
        s += path([(la, lo) for lo in range(-180, 181, 3)], '#93c5fd', 1.2)
    for lo in range(-180, 180, 30):
        s += path([(la, lo) for la in range(-90, 91, 3)], '#93c5fd', 1.2)
    s += path([(0, lo) for lo in range(-180, 181, 2)], '#1d4ed8', 2.5)
    s += path([(la, 0) for la in range(-90, 91, 2)], '#15803d', 2.5)
    # point P at lat 40N lon 40W; Q at 40N lon 0
    P = (40, -60); Q = (40, 0)
    s += path([(0, P[1])] + [(la, P[1]) for la in range(0, 41)], '#b91c1c', 3)
    s += path([(40, lo) for lo in range(-60, 1)], '#7c3aed', 3.5)
    s += path([(0, lo) for lo in range(-60, 1)], '#ea580c', 4)
    # great circle A-B (สั้นกว่าเส้นขนาน นูนขึ้นไปทางขั้ว)
    def gcp(a, b, n=60):
        def v(p):
            la, lo = R(p[0]), R(p[1]); return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))
        va, vb = v(a), v(b); om = math.acos(sum(i * j for i, j in zip(va, vb)))
        out = []
        for k in range(n + 1):
            t = k / n; f1 = math.sin((1 - t) * om) / math.sin(om); f2 = math.sin(t * om) / math.sin(om)
            q = [f1 * i + f2 * j for i, j in zip(va, vb)]
            out.append((math.degrees(math.asin(q[2])), math.degrees(math.atan2(q[1], q[0]))))
        return out
    GCAB = gcp(P, Q)
    s += path(GCAB, '#0f766e', 2.5).replace('stroke-width="2.5"', 'stroke-width="2.5" stroke-dasharray="7 4"')
    vx_, vy_, _ = proj(*GCAB[len(GCAB) // 2])
    s += f'<text x="{vx_-62:.1f}" y="{vy_-8:.1f}" font-size="12" fill="#0f766e" font-weight="bold">great circle (≈ 2,703 ไมล์)</text>\n'
    px, py, _ = proj(*P); qx, qy, _ = proj(*Q)
    s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#b91c1c"/><text x="{px-24:.1f}" y="{py-10:.1f}" font-size="15" font-weight="bold">A</text>\n'
    s += f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="6" fill="#7c3aed"/><text x="{qx+8:.1f}" y="{qy-8:.1f}" font-size="15" font-weight="bold">B</text>\n'
    nx, ny, _ = proj(90, 0)
    s += f'<text x="{nx-8:.1f}" y="{ny-8:.1f}" font-size="15" font-weight="bold">Pn</text>\n'
    ex, ey, _ = proj(0, 60)
    s += f'<text x="{ex-70:.1f}" y="{ey+20:.1f}" font-size="13" fill="#1d4ed8" font-weight="bold">Equator</text>\n'
    gx, gy, _ = proj(-40, 0)
    s += f'<text x="{gx+6:.1f}" y="{gy:.1f}" font-size="13" fill="#15803d" font-weight="bold">Greenwich 0°</text>\n'
    mx, my, _ = proj(20, -60)
    s += f'<text x="{mx-80:.1f}" y="{my:.1f}" font-size="13" fill="#b91c1c" font-weight="bold">Lat 40°N</text>\n'
    dx_, dy_, _ = proj(40, -30)
    s += f'<text x="{dx_-40:.1f}" y="{dy_+20:.1f}" font-size="13" fill="#7c3aed" font-weight="bold">departure</text>\n'
    lx, ly, _ = proj(0, -30)
    s += f'<text x="{lx-40:.1f}" y="{ly+22:.1f}" font-size="13" fill="#ea580c" font-weight="bold">d.long 60°</text>\n'
    s += '<rect x="560" y="80" width="320" height="324" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    lines = ['A และ B อยู่ที่ละติจูด 40°N เท่ากัน', 'd.long (A→B) = 60° = 3,600\'', '', 'departure = d.long × cos Lat', '              = 3,600 × cos 40°', '              ≈ 2,758 ไมล์', '', 'ระยะตามเส้นขนาน (rhumb line 090°)', '= 2,758 ไมล์', 'ระยะตาม great circle ≈ 2,703 ไมล์', '(สั้นกว่า ~55 ไมล์ · เส้นประเขียวอมฟ้า)', 'จุดสูงสุด (vertex) ≈ 46°06\'N ที่ 30°W']
    for i, t in enumerate(lines):
        s += f'<text x="576" y="{108 + i*24}" font-size="14">{t}</text>\n'
    s += '<text x="560" y="436" font-size="13" fill="#334155">• 1\' ละติจูด ≈ 1 ไมล์ทะเล (ตามเมอริเดียน)</text>\n'
    s += '<text x="560" y="460" font-size="13" fill="#334155">• 1\' ลองจิจูด = cos Lat ไมล์ (ตามเส้นขนาน)</text>\n'
    s += '<text x="560" y="484" font-size="13" fill="#334155">• เส้นศูนย์สูตรและเมอริเดียน = great circle</text>\n'
    s += '<text x="560" y="508" font-size="13" fill="#334155">• เส้นขนานอื่น ๆ = small circle</text>\n'
    save('ter-lat-long.svg', s)

def projections():
    w, h = 980, 520
    s = head(w, h, 'Mercator กับ Gnomonic: rhumb line และ great circle')
    # Mercator panel
    x0, y0, W, H = 40, 70, 430, 380
    s += f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" fill="#f0f9ff" stroke="#0369a1"/>\n'
    def mp(lat): return math.log(math.tan(math.pi / 4 + R(lat) / 2))
    lat_min, lat_max, lon_min, lon_max = 20, 60, -80, 10
    def mxy(lat, lon):
        x = x0 + (lon - lon_min) / (lon_max - lon_min) * W
        y = y0 + H - (mp(lat) - mp(lat_min)) / (mp(lat_max) - mp(lat_min)) * H
        return x, y
    for la in range(20, 61, 10):
        x1, y1 = mxy(la, lon_min); x2, y2 = mxy(la, lon_max)
        s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#bae6fd"/><text x="{x1+4:.1f}" y="{y1-3:.1f}" font-size="11" fill="#0369a1">{la}°N</text>\n'
    for lo in range(-80, 11, 15):
        x1, y1 = mxy(lat_min, lo); x2, y2 = mxy(lat_max, lo)
        s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#bae6fd"/>\n'
    A = (40.5, -74); B = (50.0, -5)
    # great circle points
    def gc_points(A, B, n=60):
        def v(p):
            la, lo = R(p[0]), R(p[1]); return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))
        a, b = v(A), v(B); om = math.acos(sum(i * j for i, j in zip(a, b)))
        pts = []
        for k in range(n + 1):
            t = k / n; f1 = math.sin((1 - t) * om) / math.sin(om); f2 = math.sin(t * om) / math.sin(om)
            q = [f1 * i + f2 * j for i, j in zip(a, b)]
            pts.append((math.degrees(math.asin(q[2])), math.degrees(math.atan2(q[1], q[0]))))
        return pts
    G = gc_points(A, B)
    d = 'M ' + ' L '.join('%.1f %.1f' % mxy(*p) for p in G)
    s += f'<path d="{d}" fill="none" stroke="#b91c1c" stroke-width="3"/>\n'
    ax, ay = mxy(*A); bx, by = mxy(*B)
    s += f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="#1d4ed8" stroke-width="3" stroke-dasharray="8 5"/>\n'
    s += f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="5" fill="#0f172a"/><circle cx="{bx:.1f}" cy="{by:.1f}" r="5" fill="#0f172a"/>\n'
    s += f'<text x="{ax-10:.1f}" y="{ay+20:.1f}" font-size="13" font-weight="bold">New York</text><text x="{bx-60:.1f}" y="{by+22:.1f}" font-size="13" font-weight="bold">English Channel</text>\n'
    s += f'<text x="{x0+W/2}" y="{y0-10}" text-anchor="middle" font-size="16" font-weight="bold" fill="#0369a1">Mercator</text>\n'
    s += f'<text x="{x0+10}" y="{y0+H+26}" font-size="13"><tspan fill="#1d4ed8" font-weight="bold">- - rhumb line = เส้นตรง</tspan>   <tspan fill="#b91c1c" font-weight="bold">— great circle = เส้นโค้งนูนไปทางขั้ว</tspan></text>\n'
    # Gnomonic panel centered at 45N -40
    x0g = 510; c_lat, c_lon = R(45), R(-40); scale = 330
    s += f'<defs><clipPath id="gclip"><rect x="{x0g}" y="{y0}" width="{W}" height="{H}"/></clipPath></defs>\n'
    s += f'<rect x="{x0g}" y="{y0}" width="{W}" height="{H}" fill="#fefce8" stroke="#a16207"/>\n<g clip-path="url(#gclip)">\n'
    def gxy(lat, lon):
        la, lo = R(lat), R(lon)
        cosc = math.sin(c_lat) * math.sin(la) + math.cos(c_lat) * math.cos(la) * math.cos(lo - c_lon)
        X = math.cos(la) * math.sin(lo - c_lon) / cosc
        Y = (math.cos(c_lat) * math.sin(la) - math.sin(c_lat) * math.cos(la) * math.cos(lo - c_lon)) / cosc
        return x0g + W / 2 + X * scale, y0 + H / 2 + 20 - Y * scale
    for la in range(20, 71, 10):
        pts = [gxy(la, lo) for lo in range(-85, 6, 2)]
        d = 'M ' + ' L '.join('%.1f %.1f' % p for p in pts)
        s += f'<path d="{d}" fill="none" stroke="#fde68a"/>\n'
        tx, ty = gxy(la, -85)
        if x0g < tx < x0g + W and y0 < ty < y0 + H: s += f'<text x="{tx+3:.1f}" y="{ty-3:.1f}" font-size="11" fill="#a16207">{la}°N</text>\n'
    for lo in range(-80, 11, 15):
        pts = [gxy(la, lo) for la in range(15, 80, 2)]
        d = 'M ' + ' L '.join('%.1f %.1f' % p for p in pts)
        s += f'<path d="{d}" fill="none" stroke="#fde68a"/>\n'
    s += '</g>\n'
    gpts = [gxy(*p) for p in G]
    d = 'M ' + ' L '.join('%.1f %.1f' % p for p in gpts)
    s += f'<path d="{d}" fill="none" stroke="#b91c1c" stroke-width="3"/>\n'
    # rhumb line on gnomonic: points along constant course (Mercator straight line)
    rpts = []
    for k in range(61):
        t = k / 60
        my_ = mp(A[0]) + t * (mp(B[0]) - mp(A[0])); lat = math.degrees(2 * math.atan(math.exp(my_)) - math.pi / 2)
        lon = A[1] + t * (B[1] - A[1]); rpts.append(gxy(lat, lon))
    d = 'M ' + ' L '.join('%.1f %.1f' % p for p in rpts)
    s += f'<path d="{d}" fill="none" stroke="#1d4ed8" stroke-width="3" stroke-dasharray="8 5"/>\n'
    ax, ay = gxy(*A); bx, by = gxy(*B)
    s += f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="5" fill="#0f172a"/><circle cx="{bx:.1f}" cy="{by:.1f}" r="5" fill="#0f172a"/>\n'
    s += f'<text x="{x0g+W/2}" y="{y0-10}" text-anchor="middle" font-size="16" font-weight="bold" fill="#a16207">Gnomonic</text>\n'
    s += f'<text x="{x0g+10}" y="{y0+H+26}" font-size="13"><tspan fill="#b91c1c" font-weight="bold">— great circle = เส้นตรง</tspan>   <tspan fill="#1d4ed8" font-weight="bold">- - rhumb line = เส้นโค้ง</tspan></text>\n'
    s += f'<text x="{w/2}" y="{h-12}" text-anchor="middle" font-size="13" fill="#334155">วางแผน GC บน gnomonic → อ่านพิกัด waypoints → ถ่ายลง Mercator แล้วแล่น rhumb line ระหว่าง waypoints</text>\n'
    save('ter-projections.svg', s)

def current_triangle():
    w, h = 860, 560
    s = head(w, h, 'สามเหลี่ยมกระแสน้ำ — หา Course to Steer (CTS)')
    sc = 30  # px per knot
    A = (280, 110)
    track, stw, set_, rate = 160, 13.5, 225, 1.5
    cts, sog = 154.2, 14.06
    ux, uy = bearing_vec(track)
    # intended track line
    s += f'<line x1="{A[0]}" y1="{A[1]}" x2="{A[0]+ux*sc*16.5:.1f}" y2="{A[1]+uy*sc*16.5:.1f}" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="6 5"/>\n'
    cx_, cy_ = bearing_vec(set_)
    B = (A[0] + cx_ * rate * sc, A[1] + cy_ * rate * sc)
    C = (A[0] + ux * sog * sc, A[1] + uy * sog * sc)
    s += f'<line x1="{A[0]}" y1="{A[1]}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke="#15803d" stroke-width="3.5"/>\n'
    s += heads(A[0], A[1], B[0], B[1], '#15803d', 3, gap=8, size=10)
    s += f'<line x1="{B[0]:.1f}" y1="{B[1]:.1f}" x2="{C[0]:.1f}" y2="{C[1]:.1f}" stroke="#1d4ed8" stroke-width="3.5"/>\n'
    s += heads(B[0], B[1], C[0], C[1], '#1d4ed8', 1)
    s += f'<line x1="{A[0]}" y1="{A[1]}" x2="{C[0]:.1f}" y2="{C[1]:.1f}" stroke="#b91c1c" stroke-width="3.5"/>\n'
    s += heads(A[0], A[1], C[0], C[1], '#b91c1c', 2)
    # arc of radius stw from B
    a1 = math.degrees(math.atan2(C[1] - B[1], C[0] - B[0]))
    r = stw * sc
    pts = []
    for dd in range(-12, 13):
        t = R(a1 + dd)
        pts.append((B[0] + r * math.cos(t), B[1] + r * math.sin(t)))
    d = 'M ' + ' L '.join('%.1f %.1f' % p for p in pts)
    s += f'<path d="{d}" fill="none" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3 3"/>\n'
    s += f'<circle cx="{A[0]}" cy="{A[1]}" r="6" fill="#0f172a"/><text x="{A[0]-60}" y="{A[1]-8}" font-size="15" font-weight="bold">A (ตำแหน่งเรือ)</text>\n'
    s += f'<text x="{B[0]-8:.1f}" y="{B[1]+6:.1f}" text-anchor="end" font-size="14" fill="#15803d" font-weight="bold">B: กระแสน้ำ set 225° × 1.5 kn</text>\n'
    s += f'<text x="{C[0]+10:.1f}" y="{C[1]+6:.1f}" font-size="15" font-weight="bold">C</text>\n'
    mx, my = (B[0] + C[0]) / 2, (B[1] + C[1]) / 2
    s += f'<text x="{mx-210:.1f}" y="{my:.1f}" font-size="14" fill="#1d4ed8" font-weight="bold">BC = CTS 154° × STW 13.5 kn</text>\n'
    mx, my = (A[0] + C[0]) / 2, (A[1] + C[1]) / 2
    s += f'<text x="{mx+16:.1f}" y="{my:.1f}" font-size="14" fill="#b91c1c" font-weight="bold">AC = Track 160° · SOG ≈ 14.1 kn</text>\n'
    s += '<rect x="500" y="90" width="340" height="190" rx="10" fill="#f8fafc" stroke="#94a3b8"/>\n'
    lines = [('#15803d', 'ลูกศร 3 หัว: กระแสน้ำ AB (set × rate)'), ('#1d4ed8', 'ลูกศร 1 หัว: water track BC (CTS × STW)'), ('#b91c1c', 'ลูกศร 2 หัว: ground track AC (COG × SOG)'), ('#334155', 'วงเวียนรัศมี STW จาก B ตัดเส้นทางที่ C'), ('#334155', 'Water + Current = Ground')]
    for i, (c, t) in enumerate(lines):
        s += f'<text x="514" y="{120 + i*32}" font-size="14" fill="{c}">{t}</text>\n'
    s += '<line x1="800" y1="400" x2="800" y2="330" stroke="#0f172a" stroke-width="2" marker-end="url(#a1)"/><text x="793" y="320" font-size="15" font-weight="bold">N</text>\n'
    save('ter-current-triangle.svg', s)

def cross_bearings():
    w, h = 880, 600
    s = head(w, h, 'Fix ด้วยแบริ่ง 3 เส้น (Cross bearings)')
    s += '<path d="M 0 60 L 880 60 L 880 150 Q 760 200 640 170 Q 560 150 480 210 Q 400 260 300 220 Q 200 180 120 230 Q 60 260 0 250 Z" fill="#f5deb3" stroke="#8b6b3d" stroke-width="2"/>\n'
    objs = [('Lt A', (150, 226)), ('Tower B (conspic)', (440, 228)), ('Pt C', (760, 182))]
    ship = (470, 470)
    brgs = []
    for name, (x, y) in objs:
        b = math.degrees(math.atan2(x - ship[0], -(y - ship[1]))) % 360
        brgs.append(b)
    offs = [0.9, -0.7, 0.6]  # ความคลาดเคลื่อนเล็กน้อยของแต่ละแบริ่ง (องศา) ทำให้เกิด cocked hat
    for (name, (x, y)), b, o in zip(objs, brgs, offs):
        bb = b + o
        ux, uy = bearing_vec(bb)
        # line from object back toward ship extended
        dist = math.hypot(ship[0]-x, ship[1]-y)
        x2, y2 = x - ux * (dist + 50), y - uy * (dist + 50)
        s += f'<line x1="{x}" y1="{y}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1d4ed8" stroke-width="2"/>\n'
        s += f'<circle cx="{x}" cy="{y}" r="7" fill="#a21caf"/><text x="{x-30}" y="{y-14}" font-size="14" font-weight="bold" fill="#701a75">{name}</text>\n'
        lx, ly = x - ux * dist * 0.45, y - uy * dist * 0.45
        s += f'<text x="{lx+8:.1f}" y="{ly:.1f}" font-size="13" fill="#1d4ed8" font-weight="bold">{bb:05.1f}°T</text>\n'
    # cocked hat = จุดตัดจริงของเส้นแบริ่งที่วาด
    lines_ = []
    for (name, (x, y)), b, o in zip(objs, brgs, offs):
        ux, uy = bearing_vec(b + o); lines_.append(((x, y), (ux, uy)))
    pts = []
    for i in range(3):
        (p1, u1), (p2, u2) = lines_[i], lines_[(i + 1) % 3]
        det = u1[0] * (-u2[1]) - u1[1] * (-u2[0]); dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        t = (dx * (-u2[1]) - dy * (-u2[0])) / det
        pts.append((p1[0] + t * u1[0], p1[1] + t * u1[1]))
    gx = sum(p[0] for p in pts) / 3; gy = sum(p[1] for p in pts) / 3
    rr = max(math.hypot(p[0] - gx, p[1] - gy) for p in pts) + 8
    s += '<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + '" fill="#fecaca" stroke="#b91c1c" stroke-width="1.5"/>\n'
    s += f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{rr:.1f}" fill="none" stroke="#0f172a" stroke-width="2"/><circle cx="{gx:.1f}" cy="{gy:.1f}" r="2" fill="#0f172a"/>\n'
    s += f'<text x="{gx+rr+10:.1f}" y="{gy+6:.1f}" font-size="14" font-weight="bold">Fix 0815 (cocked hat เล็ก ใช้จุดกลาง)</text>\n'
    s += '<rect x="20" y="490" width="400" height="98" rx="8" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['• มุมตัดดี: 3 เส้นห่างกันประมาณ 60°/120°', '• วัดวัตถุใกล้หัว/ท้ายก่อน ใกล้แนวกราบหลังสุด', '• สามเหลี่ยมใหญ่ → ตรวจ ID วัตถุ / compass error', '• ทุ่นลอยไม่ควรใช้เป็นวัตถุหลัก']):
        s += f'<text x="34" y="{514 + i*22}" font-size="13">{t}</text>\n'
    save('ter-fix-cross-bearings.svg', s)

def running_fix():
    w, h = 860, 560
    s = head(w, h, 'Running Fix — เลื่อนเส้นตำแหน่ง (Transferred position line)')
    s += '<path d="M 520 60 L 860 60 L 860 330 Q 760 300 700 250 Q 640 200 600 140 Q 560 100 520 60 Z" fill="#f5deb3" stroke="#8b6b3d" stroke-width="2"/>\n'
    L = (600, 140)
    s += f'<circle cx="{L[0]}" cy="{L[1]}" r="8" fill="#a21caf"/><text x="{L[0]+10}" y="{L[1]-10}" font-size="14" font-weight="bold" fill="#701a75">Lt (ประภาคาร)</text>\n'
    co = 75; spd_px = 400
    ux, uy = bearing_vec(co)
    P1 = (150, 480); P2 = (P1[0] + ux * spd_px, P1[1] + uy * spd_px)
    s += f'<line x1="{P1[0]-ux*80:.1f}" y1="{P1[1]-uy*80:.1f}" x2="{P2[0]+ux*120:.1f}" y2="{P2[1]+uy*120:.1f}" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="6 5"/>\n'
    b1 = math.degrees(math.atan2(L[0] - P1[0], -(L[1] - P1[1]))) % 360
    b2 = math.degrees(math.atan2(L[0] - P2[0], -(L[1] - P2[1]))) % 360
    for (P, b, col, lab, ll, lox, loy) in [(P1, b1, '#1d4ed8', '1st brg 0900', 520, -150, 18), (P2, b2, '#b91c1c', '2nd brg 0930', 330, 10, 0)]:
        vx, vy = bearing_vec(b)
        s += f'<line x1="{L[0]}" y1="{L[1]}" x2="{L[0]-vx*ll:.1f}" y2="{L[1]-vy*ll:.1f}" stroke="{col}" stroke-width="2.5"/>\n'
        s += f'<text x="{L[0]-vx*ll+lox:.1f}" y="{L[1]-vy*ll+loy:.1f}" font-size="13" fill="{col}" font-weight="bold">{lab} ({b:05.1f}°)</text>\n'
    # pick a point on first LOP (DR at 0900 on LOP): use P1 itself shifted
    Q = (P1[0] + 40 * bearing_vec(b1)[0], P1[1] + 40 * bearing_vec(b1)[1])
    Q2 = (Q[0] + ux * spd_px, Q[1] + uy * spd_px)
    s += f'<line x1="{Q[0]:.1f}" y1="{Q[1]:.1f}" x2="{Q2[0]:.1f}" y2="{Q2[1]:.1f}" stroke="#0f172a" stroke-width="2.5" marker-end="url(#a1)"/>\n'
    s += f'<text x="{Q2[0]-198:.1f}" y="{Q2[1]-28:.1f}" font-size="13" font-weight="bold">เข็ม 075° × ระยะที่แล่น 30 นาที</text>\n'
    vx, vy = bearing_vec(b1)
    s += f'<line x1="{Q2[0]+vx*200:.1f}" y1="{Q2[1]+vy*200:.1f}" x2="{Q2[0]-vx*170:.1f}" y2="{Q2[1]-vy*170:.1f}" stroke="#1d4ed8" stroke-width="2.5" stroke-dasharray="10 4"/>\n'
    s += heads(Q2[0]-vx*170, Q2[1]-vy*170, Q2[0]+vx*200, Q2[1]+vy*200, '#1d4ed8', 2, gap=8, size=11, both=True)
    s += f'<text x="{Q2[0]+vx*200+8:.1f}" y="{Q2[1]+vy*200-8:.1f}" font-size="13" fill="#1d4ed8" font-weight="bold">transferred 1st LOP</text>\n'
    s += f'<circle cx="{P2[0]:.1f}" cy="{P2[1]:.1f}" r="12" fill="none" stroke="#0f172a" stroke-width="2.5"/><circle cx="{P2[0]:.1f}" cy="{P2[1]:.1f}" r="3" fill="#0f172a"/>\n'
    s += f'<text x="{P2[0]+18:.1f}" y="{P2[1]+30:.1f}" font-size="14" font-weight="bold">Running fix 0930</text>\n'
    s += '<text x="300" y="545" font-size="13" fill="#334155">เส้นทึบ = position line · เส้นประหัวลูกศรคู่ = เส้นที่เลื่อนมา · ใช้ ground track ถ้ารู้กระแสน้ำ</text>\n'
    save('ter-running-fix.svg', s)

def doubling():
    w, h = 860, 520
    s = head(w, h, 'Doubling the angle on the bow และ Four-point bearing')
    A = (110, 420); hd = 0
    L = (560, 150)
    s += f'<circle cx="{L[0]}" cy="{L[1]}" r="9" fill="#a21caf"/><text x="{L[0]+12}" y="{L[1]-8}" font-size="14" font-weight="bold" fill="#701a75">Lt</text>\n'
    # ship track horizontal heading 090 from A
    y = 420
    # find point where relative bearing 30 and 60 (relative to heading 090)
    def x_at(rel):
        # angle between track (east) and line to L = rel
        dy = y - L[1]
        return L[0] - dy / math.tan(R(rel))
    x30, x60, x90 = x_at(30), x_at(60), L[0]
    s += f'<line x1="60" y1="{y}" x2="800" y2="{y}" stroke="#0f172a" stroke-width="3" marker-end="url(#a1)"/>\n'
    s += f'<text x="700" y="{y+30}" font-size="13" font-weight="bold">เข็ม 090°</text>\n'
    for x, lab, col in [(x30, '30° on bow (2000)', '#1d4ed8'), (x60, '60° on bow (2024)', '#b91c1c'), (x90, 'Abeam', '#15803d')]:
        s += f'<line x1="{x:.1f}" y1="{y}" x2="{L[0]}" y2="{L[1]}" stroke="{col}" stroke-width="2"/>\n'
        s += f'<circle cx="{x:.1f}" cy="{y}" r="5" fill="{col}"/><text x="{x-50:.1f}" y="{y+24}" font-size="12" fill="{col}" font-weight="bold">{lab}</text>\n'
    s += f'<text x="{(x30+x60)/2-60:.1f}" y="{y-12}" font-size="14" font-weight="bold" fill="#0f172a">d = ระยะที่แล่น</text>\n'
    mx, my = (x60 + L[0]) / 2, (y + L[1]) / 2
    s += f'<text x="{mx-160:.1f}" y="{my:.1f}" font-size="14" font-weight="bold" fill="#b91c1c">ระยะถึง Lt = d</text>\n'
    s += f'<text x="{L[0]+10}" y="{(y+L[1])/2:.1f}" font-size="13" fill="#15803d" font-weight="bold">ระยะผ่านตรงกราบ = d·sin60°</text>\n'
    s += '<rect x="40" y="50" width="285" height="96" rx="8" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['θ → 2θ : สามเหลี่ยมหน้าจั่ว', '45° → 90° : run = distance abeam', '26½° → 45° : run = distance abeam', '(ทำนายระยะผ่านได้ล่วงหน้า)']):
        s += f'<text x="52" y="{72 + i*22}" font-size="13">{t}</text>\n'
    save('ter-doubling-angle.svg', s)

if __name__ == '__main__':
    lat_long(); projections(); current_triangle(); cross_bearings(); running_fix(); doubling()
    print('ok')
