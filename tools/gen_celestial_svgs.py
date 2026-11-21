"""สคริปต์สร้างภาพประกอบบทดาราศาสตร์ (celestial sphere, PZX, star fix, intercept)"""
import math, os
R = math.radians
OUT = os.path.join(os.path.dirname(__file__), '..', 'images')
FONT = "Tahoma, 'Noto Sans Thai', 'Leelawadee UI', Sarabun, sans-serif"

def head(w, h, title=None):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#fff"/>\n'
    s += ('<defs><marker id="ah" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">'
          '<path d="M0,0 L12,6 L0,12 z" fill="context-stroke"/></marker></defs>\n')
    if title:
        s += f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#0f172a">{title}</text>\n'
    return s

class Sphere:
    def __init__(self, cx, cy, r, tilt, a0):
        self.cx, self.cy, self.r, self.e, self.a0 = cx, cy, r, R(tilt), a0
    def proj(self, a, d):
        a = R(a - self.a0); d = R(d)
        x = math.cos(d) * math.sin(a)
        y = math.sin(d) * math.cos(self.e) - math.cos(d) * math.cos(a) * math.sin(self.e)
        z = math.cos(d) * math.cos(a) * math.cos(self.e) + math.sin(d) * math.sin(self.e)
        return self.cx + self.r * x, self.cy - self.r * y, z
    def curve(self, pts, color, width=2, dash_back=True, extra=''):
        """pts list of (a,d); split into front/back segments"""
        out = ''
        seg = []; front = None
        P = [self.proj(a, d) for a, d in pts]
        for x, y, z in P:
            f = z >= 0
            if front is None: front = f
            if f != front:
                out += self._seg(seg, front, color, width, dash_back, extra)
                seg = [seg[-1]] if seg else []
                front = f
            seg.append((x, y))
        out += self._seg(seg, front, color, width, dash_back, extra)
        return out
    def _seg(self, seg, front, color, width, dash_back, extra):
        if len(seg) < 2: return ''
        d = 'M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in seg)
        dash = '' if front or not dash_back else ' stroke-dasharray="5 5" opacity="0.55"'
        return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{dash} {extra}/>\n'

def celestial_sphere():
    w, h = 900, 640
    s = head(w, h, 'ทรงกลมท้องฟ้า (Celestial Sphere) — Equinoctial System')
    S = Sphere(380, 340, 250, 18, -10)
    s += f'<circle cx="{S.cx}" cy="{S.cy}" r="{S.r}" fill="#f8fafc" stroke="#334155" stroke-width="2"/>\n'
    eq = [(a, 0) for a in range(0, 361, 2)]
    s += S.curve(eq, '#1d4ed8', 2.5)
    # ecliptic
    eps = 23.44
    ecl = []
    for L in range(0, 361, 2):
        l = R(L)
        a = math.degrees(math.atan2(math.sin(l) * math.cos(R(eps)), math.cos(l))) % 360
        d = math.degrees(math.asin(math.sin(R(eps)) * math.sin(l)))
        ecl.append((a, d))
    s += S.curve(ecl, '#d97706', 2.2)
    # Greenwich meridian (RA = 40) and star hour circle (RA = -65)
    G = 40; X = -65; dX = 35
    s += S.curve([(G, d) for d in range(-90, 91, 2)], '#15803d', 2)
    s += S.curve([(X, d) for d in range(-90, 91, 2)], '#7c3aed', 2)
    # axis
    pnx, pny, _ = S.proj(0, 90); psx, psy, _ = S.proj(0, -90)
    s += f'<line x1="{pnx:.1f}" y1="{pny-40:.1f}" x2="{psx:.1f}" y2="{psy+40:.1f}" stroke="#64748b" stroke-dasharray="3 4"/>\n'
    s += f'<circle cx="{pnx:.1f}" cy="{pny:.1f}" r="5" fill="#0f172a"/><text x="{pnx+10:.1f}" y="{pny-8:.1f}" font-size="16" font-weight="bold">Pn</text>\n'
    s += f'<circle cx="{psx:.1f}" cy="{psy:.1f}" r="5" fill="#0f172a"/><text x="{psx+10:.1f}" y="{psy+20:.1f}" font-size="16" font-weight="bold">Ps</text>\n'
    # arcs along equator: GHA Aries (G->0), SHA (0->X), GHA X (G->X)
    def arc(a1, a2, d, color, label, lx_off=0, ly_off=0, step=1):
        rng = range(int(a1), int(a2) - 1, -step) if a1 > a2 else range(int(a1), int(a2) + 1, step)
        pts = [(a, d) for a in rng]
        out = S.curve(pts, color, 3.5, extra='marker-end="url(#ah)"')
        mx, my, _ = S.proj((a1 + a2) / 2, d)
        out += f'<text x="{mx+lx_off:.1f}" y="{my+ly_off:.1f}" font-size="14" font-weight="bold" fill="{color}" text-anchor="middle">{label}</text>\n'
        return out
    s += arc(G, 0, -6, '#15803d', 'GHA ♈', 0, 24)
    s += arc(0, X, -6, '#b91c1c', 'SHA ✶', 0, 24)
    s += arc(G, X, -20, '#0f766e', 'GHA ✶ = GHA ♈ + SHA', 0, 26)
    # Dec arc
    pts = [(X, d) for d in range(0, dX + 1)]
    s += S.curve(pts, '#7c3aed', 3.5, extra='marker-end="url(#ah)"')
    xx, xy, _ = S.proj(X, dX)
    s += f'<circle cx="{xx:.1f}" cy="{xy:.1f}" r="7" fill="#facc15" stroke="#854d0e" stroke-width="2"/><text x="{xx-34:.1f}" y="{xy-12:.1f}" font-size="16" font-weight="bold" fill="#854d0e">X (ดาว)</text>\n'
    mx, my, _ = S.proj(X, dX / 2)
    s += f'<text x="{mx-48:.1f}" y="{my:.1f}" font-size="14" font-weight="bold" fill="#7c3aed">Dec</text>\n'
    ax, ay, _ = S.proj(0, 0)
    s += f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="6" fill="#b91c1c"/><text x="{ax+6:.1f}" y="{ay-10:.1f}" font-size="15" font-weight="bold" fill="#b91c1c">♈ First Point of Aries</text>\n'
    gx, gy, _ = S.proj(G, 50)
    s += f'<text x="{gx+8:.1f}" y="{gy:.1f}" font-size="13" fill="#15803d" font-weight="bold">Greenwich meridian</text>\n'
    ex, ey, _ = S.proj(120, 0)
    s += f'<text x="{ex+6:.1f}" y="{ey+18:.1f}" font-size="13" fill="#1d4ed8" font-weight="bold">Equinoctial</text>\n'
    lx, ly, _ = S.proj(150, 12)
    s += f'<text x="{lx-60:.1f}" y="{ly+24:.1f}" font-size="13" fill="#b45309" font-weight="bold">Ecliptic (เอียง 23°26\')</text>\n'
    # legend
    s += '<rect x="660" y="80" width="225" height="190" rx="8" fill="#fff" stroke="#94a3b8"/>\n'
    items = [('#1d4ed8', 'เส้นศูนย์สูตรฟ้า'), ('#d97706', 'สุริยวิถี'), ('#15803d', 'เมอริเดียนกรีนิช'), ('#7c3aed', 'Hour circle ของดาว'), ('#b91c1c', 'SHA วัดไปทางตะวันตก'), ('#0f766e', 'GHA ของดาว')]
    for i, (c, t) in enumerate(items):
        y = 106 + i * 27
        s += f'<line x1="672" y1="{y}" x2="702" y2="{y}" stroke="{c}" stroke-width="3"/><text x="710" y="{y+5}" font-size="13">{t}</text>\n'
    s += '<text x="660" y="300" font-size="13" fill="#334155">LHA = GHA + Long E</text>\n'
    s += '<text x="660" y="320" font-size="13" fill="#334155">LHA = GHA − Long W</text>\n'
    s += '<text x="660" y="345" font-size="13" fill="#334155">SHA = 360° − RA</text>\n'
    s += '<text x="660" y="370" font-size="12" fill="#64748b">(เส้นประ = ด้านหลังทรงกลม)</text>\n'
    s += '</svg>\n'
    open(os.path.join(OUT, 'cel-celestial-sphere.svg'), 'w').write(s)

def pzx():
    w, h = 900, 620
    s = head(w, h, 'สามเหลี่ยมดาราศาสตร์ PZX')
    # horizon system: use Sphere where 'a' = azimuth measured, 'd' = altitude; view from SW elevated
    S = Sphere(360, 360, 250, 15, 50)
    s += f'<circle cx="{S.cx}" cy="{S.cy}" r="{S.r}" fill="#f8fafc" stroke="#334155" stroke-width="2"/>\n'
    s += S.curve([(a, 0) for a in range(0, 361, 2)], '#0f766e', 2.5)
    lat = 40
    # pole at azimuth 0 altitude lat ; star at az 120 alt 40
    star_az, star_alt = 100, 30
    def gc(p1, p2, n=60):
        # great circle between two (az,alt)
        def vec(az, alt):
            az, alt = R(az), R(alt)
            return (math.cos(alt) * math.sin(az), math.cos(alt) * math.cos(az), math.sin(alt))
        a, b = vec(*p1), vec(*p2)
        dot = max(-1, min(1, sum(i * j for i, j in zip(a, b)))); om = math.acos(dot)
        pts = []
        for k in range(n + 1):
            t = k / n
            f1 = math.sin((1 - t) * om) / math.sin(om); f2 = math.sin(t * om) / math.sin(om)
            v = [f1 * i + f2 * j for i, j in zip(a, b)]
            az = math.degrees(math.atan2(v[0], v[1])); alt = math.degrees(math.asin(max(-1, min(1, v[2]))))
            pts.append((az, alt))
        return pts
    Z = (0, 90); P = (0, lat); X = (star_az, star_alt)
    # observer meridian (az 0 and 180 great circle through zenith)
    s += S.curve([(0, d) for d in range(0, 91, 2)] + [(180, d) for d in range(90, -1, -2)], '#64748b', 1.5)
    # equinoctial: great circle 90 deg from P
    eqpts = []
    for t in range(0, 361, 3):
        # rotate equator of pole frame
        tt = R(t)
        # basis: P vector
        pv = (0, math.cos(R(lat)), math.sin(R(lat)))
        e1 = (1, 0, 0)
        e2 = (pv[1] * e1[2] - pv[2] * e1[1], pv[2] * e1[0] - pv[0] * e1[2], pv[0] * e1[1] - pv[1] * e1[0])
        v = [math.cos(tt) * a + math.sin(tt) * b for a, b in zip(e1, e2)]
        eqpts.append((math.degrees(math.atan2(v[0], v[1])), math.degrees(math.asin(v[2]))))
    s += S.curve(eqpts, '#1d4ed8', 1.8)
    s += S.curve(gc(P, Z), '#b91c1c', 4)
    s += S.curve(gc(P, X), '#7c3aed', 4)
    s += S.curve(gc(Z, X), '#15803d', 4)
    # vertical circle down from X to horizon
    s += S.curve(gc(Z, (star_az, 0)), '#15803d', 1.2)
    for (pt, lab, dx, dy, col) in [(Z, 'Z (Zenith)', 10, -10, '#0f172a'), (P, 'P (Pn)', -78, -6, '#b91c1c'), (X, 'X (ดาว)', 12, 4, '#854d0e')]:
        x, y, _ = S.proj(*pt)
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{col}"/><text x="{x+dx:.1f}" y="{y+dy:.1f}" font-size="16" font-weight="bold" fill="{col}">{lab}</text>\n'
    # labels for sides
    def mid(p1, p2):
        pts = gc(p1, p2); return S.proj(*pts[len(pts) // 2])
    x, y, _ = mid(P, Z); s += f'<text x="{x-140:.1f}" y="{y-6:.1f}" font-size="14" fill="#b91c1c" font-weight="bold">PZ = 90° − Lat</text>\n'
    x, y, _ = mid(P, X); s += f'<text x="{x-60:.1f}" y="{y+28:.1f}" font-size="14" fill="#7c3aed" font-weight="bold">PX = 90° ∓ Dec</text>\n'
    x, y, _ = mid(Z, X); s += f'<text x="{x+12:.1f}" y="{y:.1f}" font-size="14" fill="#15803d" font-weight="bold">ZX = 90° − Alt</text>\n'
    hx, hy, _ = S.proj(star_az, 0)
    s += f'<text x="{hx+6:.1f}" y="{hy+18:.1f}" font-size="12" fill="#0f766e">Horizon</text>\n'
    nx, ny, _ = S.proj(0, 0)
    s += f'<text x="{nx-6:.1f}" y="{ny+18:.1f}" font-size="13" font-weight="bold">N</text>\n'
    sx, sy, _ = S.proj(180, 0)
    s += f'<text x="{sx-6:.1f}" y="{sy-8:.1f}" font-size="13" font-weight="bold">S</text>\n'
    qx, qy, _ = S.proj(*eqpts[20])
    s += f'<text x="{qx+4:.1f}" y="{qy+16:.1f}" font-size="12" fill="#1d4ed8">Equinoctial</text>\n'
    s += '<rect x="640" y="90" width="245" height="215" rx="8" fill="#fff" stroke="#94a3b8"/>\n'
    lines = ['มุมที่ P = Hour angle (LHA)', 'มุมที่ Z = Azimuth angle', 'มุมที่ X = Parallactic angle', '', 'sin Hc = sin L sin D', '        + cos L cos D cos LHA', 'cos Z = (sin D − sin L sin Hc)', '        / (cos L cos Hc)']
    for i, t in enumerate(lines):
        s += f'<text x="652" y="{116 + i*24}" font-size="13" fill="#0f172a">{t}</text>\n'
    s += '</svg>\n'
    open(os.path.join(OUT, 'cel-pzx-triangle.svg'), 'w').write(s)

def star_fix():
    w, h = 820, 690
    s = head(w, h, 'ตัวอย่าง Star Fix — 11 ธ.ค. 2026 เวลา 1120 UT (ข้อมูลจำลอง)')
    cx, cy = 360, 350; sc = 55  # px per n.mile
    lat_dr = 5 + 27.4 / 60; lon_dr = 103 + 36.3 / 60
    # grid
    for i in range(-6, 7):
        s += f'<line x1="{cx+i*sc}" y1="70" x2="{cx+i*sc}" y2="630" stroke="#e2e8f0"/>\n'
    for j in range(-5, 6):
        s += f'<line x1="20" y1="{cy+j*sc}" x2="720" y2="{cy+j*sc}" stroke="#e2e8f0"/>\n'
    # (ชื่อดาว, Zn, intercept (+T/-A), สี, ตำแหน่งป้ายชื่อเทียบปลายเส้น azimuth)
    stars = [('Hamal', 60, 2.0, '#1d4ed8', (-40, -10), (0, 0)), ('Fomalhaut', 193, 0.8, '#b91c1c', (-60, 22), (-30, 6)), ('Altair', 277, -3.0, '#15803d', (-20, -14), (0, 0))]
    s += f'<circle cx="{cx}" cy="{cy}" r="6" fill="none" stroke="#0f172a" stroke-width="2"/><text x="{cx-40}" y="{cy-12}" font-size="14" font-weight="bold">DR</text>\n'
    lops = []
    for name, zn, it, col, (ox, oy), (tx, ty) in stars:
        ux, uy = math.sin(R(zn)), -math.cos(R(zn))
        L = 4.2
        s += f'<line x1="{cx}" y1="{cy}" x2="{cx+ux*L*sc:.1f}" y2="{cy+uy*L*sc:.1f}" stroke="{col}" stroke-width="1.3" stroke-dasharray="6 4"/>\n'
        s += f'<text x="{cx+ux*L*sc+ox:.1f}" y="{cy+uy*L*sc+oy:.1f}" font-size="13" fill="{col}" font-weight="bold">{name} Zn {zn:03d}°</text>\n'
        px, py = cx + ux * it * sc, cy + uy * it * sc
        s += f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{col}" stroke-width="3.5"/>\n'
        # LOP perpendicular
        vx, vy = -uy, ux
        s += f'<line x1="{px-vx*4.5*sc:.1f}" y1="{py-vy*4.5*sc:.1f}" x2="{px+vx*4.5*sc:.1f}" y2="{py+vy*4.5*sc:.1f}" stroke="{col}" stroke-width="2.5"/>\n'
        tag = f'{abs(it):.1f}\' {"T" if it > 0 else "A"}'
        # ป้าย intercept วางกลางเส้น intercept เยื้องออกด้านข้าง ไม่ทับ position line
        mx_, my_ = cx + ux * it * sc / 2, cy + uy * it * sc / 2
        s += f'<text x="{mx_+vx*14-14+tx:.1f}" y="{my_+vy*14+4+ty:.1f}" font-size="12" font-weight="bold" fill="{col}">{tag}</text>\n'
        lops.append((ux, uy, it))
    # fix = least squares ของ position line ทั้งสาม (หน่วยไมล์ เทียบ DR: x = dep ตะวันออก, y = d.lat เหนือ)
    a11 = a12 = a22 = b1 = b2 = 0.0
    for ux, uy, it in lops:
        ex, ny = ux, -uy  # east, north components of azimuth unit vector
        a11 += ex * ex; a12 += ex * ny; a22 += ny * ny; b1 += ex * it; b2 += ny * it
    det = a11 * a22 - a12 * a12
    dep = (a22 * b1 - a12 * b2) / det; dlat = (a11 * b2 - a12 * b1) / det
    fx, fy = cx + dep * sc, cy - dlat * sc
    flat = lat_dr + dlat / 60; flon = lon_dr + dep / math.cos(R(lat_dr)) / 60
    def dm(v): d = int(v); return f"{d:02d}°{(v-d)*60:04.1f}'"
    s += f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="16" fill="none" stroke="#0f172a" stroke-width="2.5"/><circle cx="{fx:.1f}" cy="{fy:.1f}" r="2.5" fill="#0f172a"/>\n'
    s += f'<text x="{fx+22:.1f}" y="{fy+34:.1f}" font-size="14" font-weight="bold">Fix ≈ {dm(flat)}N {dm(flon)}E</text>\n'
    s += f'<text x="{fx+22:.1f}" y="{fy+52:.1f}" font-size="12" fill="#475569">(จุดกลาง cocked hat)</text>\n'
    s += f'<text x="{cx-300}" y="{cy+40}" font-size="13">DR 05°27.4\'N 103°36.3\'E</text>\n'
    # scale bar + legend
    s += f'<line x1="600" y1="662" x2="{600+sc}" y2="662" stroke="#0f172a" stroke-width="3"/><text x="{600+sc+8}" y="667" font-size="12">1 ไมล์ทะเล</text>\n'
    s += '<text x="24" y="667" font-size="12" fill="#475569">เส้นประ = ทิศ azimuth · เส้นทึบหนา = intercept (T เข้าหา / A ออกจาก) · เส้นยาว = position line</text>\n'
    s += '</svg>\n'
    open(os.path.join(OUT, 'cel-star-fix.svg'), 'w').write(s)

def intercept():
    w, h = 820, 560
    s = head(w, h, 'วิธี Intercept (Marcq St Hilaire)')
    cx, cy = 230, 200
    zn = 128; sc = 55
    ux, uy = math.sin(R(zn)), -math.cos(R(zn))
    # azimuth line both ways
    s += f'<line x1="{cx-ux*2.5*sc:.1f}" y1="{cy-uy*2.5*sc:.1f}" x2="{cx+ux*4.8*sc:.1f}" y2="{cy+uy*4.8*sc:.1f}" stroke="#1d4ed8" stroke-width="1.6" stroke-dasharray="7 5" marker-end="url(#ah)"/>\n'
    s += f'<text x="{cx+ux*4.9*sc-150:.1f}" y="{cy+uy*4.9*sc+26:.1f}" font-size="14" fill="#1d4ed8" font-weight="bold">ไปทาง GP ของดวงอาทิตย์ Zn 128°</text>\n'
    s += f'<circle cx="{cx}" cy="{cy}" r="6" fill="none" stroke="#0f172a" stroke-width="2.5"/><text x="{cx-110}" y="{cy+5}" font-size="14" font-weight="bold">DR / AP</text>\n'
    it = 2.2
    px, py = cx + ux * it * sc, cy + uy * it * sc
    s += f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="#b91c1c" stroke-width="4"/>\n'
    s += f'<text x="{cx+6:.1f}" y="{cy-38:.1f}" font-size="14" fill="#b91c1c" font-weight="bold">Intercept 2.2\' Toward</text>\n'
    vx, vy = -uy, ux
    s += f'<line x1="{px-vx*3.6*sc:.1f}" y1="{py-vy*3.6*sc:.1f}" x2="{px+vx*3.2*sc:.1f}" y2="{py+vy*3.2*sc:.1f}" stroke="#15803d" stroke-width="3.5"/>\n'
    s += f'<text x="{px-vx*3.6*sc+10:.1f}" y="{py-vy*3.6*sc+10:.1f}" font-size="14" fill="#15803d" font-weight="bold">Position line (ตั้งฉาก azimuth)</text>\n'
    s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#b91c1c"/><text x="{px+10:.1f}" y="{py+22:.1f}" font-size="12" fill="#b91c1c">ITP</text>\n'
    # away example dashed
    ax, ay = cx - ux * 1.5 * sc, cy - uy * 1.5 * sc
    s += f'<line x1="{ax-vx*2.6*sc:.1f}" y1="{ay-vy*2.6*sc:.1f}" x2="{ax+vx*2.2*sc:.1f}" y2="{ay+vy*2.2*sc:.1f}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="4 4"/>\n'
    s += f'<text x="{ax+vx*2.2*sc-20:.1f}" y="{ay+vy*2.2*sc+20:.1f}" font-size="12" fill="#64748b">ถ้า Ho &lt; Hc → Away (ถอยออกจาก azimuth)</text>\n'
    # north arrow
    s += '<line x1="740" y1="150" x2="740" y2="80" stroke="#0f172a" stroke-width="2" marker-end="url(#ah)"/><text x="733" y="70" font-size="14" font-weight="bold">N</text>\n'
    s += '<rect x="520" y="390" width="285" height="140" rx="8" fill="#f8fafc" stroke="#94a3b8"/>\n'
    for i, t in enumerate(['Intercept = Ho − Hc', 'Ho > Hc → Toward ("HoMoTo")', 'Ho &lt; Hc → Away', 'ตัวอย่าง A: Ho 39°11.1\' Hc 39°08.9\'', '→ 2.2\' Toward 128°']):
        s += f'<text x="534" y="{418+i*24}" font-size="13">{t}</text>\n'
    s += '</svg>\n'
    open(os.path.join(OUT, 'cel-intercept.svg'), 'w').write(s)

if __name__ == '__main__':
    celestial_sphere(); pzx(); star_fix(); intercept()
    print('ok')
