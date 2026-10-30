"""Render the bodr.ing halftone stamp as SVG dots.

Port of drawStamp() in bodr-ing/bodr.ing index.html (rot 0, no lens/ripple,
intro done), so the README mark matches the site's hero.
Usage: python3 scripts/stamp.py R > fragment.svg
"""
import math, sys

SEEDS = [(-.12, -.4, -.49), (0, -.48, 0), (.12, -.4, .49)]

def in_ell(x, y, cx, cy, rx, ry, t):
    dx, dy, c, s = x - cx, y - cy, math.cos(t), math.sin(t)
    u, v = dx * c + dy * s, -dx * s + dy * c
    return (u / rx) ** 2 + (v / ry) ** 2 <= 1

def lobe(x, y, rot=0):
    for k in range(3):
        t = -k * 2 * math.pi / 3 - rot
        c, s = math.cos(t), math.sin(t)
        u, v = x * c - y * s, x * s + y * c
        if in_ell(u, v, 0, -.37, .26, .29, 0):
            return 0 if any(in_ell(u, v, sx, sy, .055, .115, r) for sx, sy, r in SEEDS) else 1
    return 0

def green(d):
    return 1 if d > .9 else (d - .62) / .28 * .85 if d > .62 else 0

def dots(R, step, pink):
    out, n = [], int(R / step)
    for j in range(-n, n + 1):
        for i in range(-n, n + 1):
            x, y = i * step, j * step
            nx, ny = x / R, y / R
            d = math.hypot(nx, ny)
            if d > 1:
                continue
            v = lobe(nx, ny) if pink else green(d)
            if v <= .02:
                continue
            r = step * .5 * min(1.3, v)
            if r >= .3:
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
    return "".join(out)

def stamp(R):
    step = max(5, R / 30)
    px, py = round(R / 48, 1), round(R / 64, 1)
    return (f'<g class="spin" fill="#00915a">{dots(R, step, False)}</g>'
            f'<g transform="translate({px} {py})" style="mix-blend-mode:multiply">'
            f'<g class="spin" fill="#ff4aa2">{dots(R, step, True)}</g></g>')

if __name__ == "__main__":
    print(stamp(float(sys.argv[1]) if len(sys.argv) > 1 else 190))
