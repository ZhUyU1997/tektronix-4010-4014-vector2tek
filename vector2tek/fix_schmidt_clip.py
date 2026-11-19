#!/usr/bin/env python3
"""Bake the Schmidt clipPath into the hatch group (per-page source fix).

Usage: fix_schmidt_clip.py SRC.svg OUT.svg
"""
import math
import re
import sys

from lxml import etree

NS = "http://www.w3.org/2000/svg"


def nums(s):
    return [float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", s)]


def cubic(p0, p1, p2, p3, n=24):
    out = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        x = u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0]
        y = u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1]
        out.append((x, y))
    return out


def parse_path(d):
    toks = re.findall(r"[MmLlCcZz]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", d)
    i = 0
    cur = (0.0, 0.0)
    start = None
    pts = []
    cmd = None
    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                if start and pts and pts[-1] != start:
                    pts.append(start)
                continue
        if cmd in "Mm":
            x, y = float(toks[i]), float(toks[i+1]); i += 2
            if cmd == "m":
                x, y = cur[0] + x, cur[1] + y
            cur = (x, y); start = cur; pts.append(cur)
            cmd = "L" if cmd == "M" else "l"
        elif cmd in "Ll":
            x, y = float(toks[i]), float(toks[i+1]); i += 2
            if cmd == "l":
                x, y = cur[0] + x, cur[1] + y
            cur = (x, y); pts.append(cur)
        elif cmd in "Cc":
            vals = [float(v) for v in toks[i:i+6]]; i += 6
            p1 = (vals[0], vals[1]); p2 = (vals[2], vals[3]); p3 = (vals[4], vals[5])
            if cmd == "c":
                p1 = (cur[0]+p1[0], cur[1]+p1[1])
                p2 = (cur[0]+p2[0], cur[1]+p2[1])
                p3 = (cur[0]+p3[0], cur[1]+p3[1])
            pts.extend(cubic(cur, p1, p2, p3)); cur = p3
        else:
            raise ValueError("unsupported path command: %r in %r" % (cmd, d))
    return pts


def parse_clip(d):
    toks = re.findall(r"[MmLlCcZz]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", d)
    i = 0; cur = (0.0, 0.0); start = None; pts = []; cmd = None
    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]; i += 1
            if cmd in "Zz":
                if start and pts[-1] != start: pts.append(start)
                continue
        if cmd in "Mm":
            x, y = float(toks[i]), float(toks[i+1]); i += 2
            if cmd == "m": x, y = cur[0]+x, cur[1]+y
            cur = (x, y); start = cur; pts.append(cur)
            cmd = "L" if cmd == "M" else "l"
        elif cmd in "Ll":
            x, y = float(toks[i]), float(toks[i+1]); i += 2
            if cmd == "l": x, y = cur[0]+x, cur[1]+y
            cur = (x, y); pts.append(cur)
        elif cmd in "Cc":
            v = [float(x) for x in toks[i:i+6]]; i += 6
            p1, p2, p3 = (v[0],v[1]), (v[2],v[3]), (v[4],v[5])
            if cmd == "c":
                p1 = (cur[0]+p1[0], cur[1]+p1[1]); p2 = (cur[0]+p2[0], cur[1]+p2[1]); p3 = (cur[0]+p3[0], cur[1]+p3[1])
            pts.extend(cubic(cur, p1, p2, p3, 40)); cur = p3
        else:
            raise ValueError("clip cmd %r" % cmd)
    return pts


def inside(p, poly):
    x, y = p; c = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]; xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            c = not c
        j = i
    return c


def seg_clip(p, q, poly):
    """Return list of (a,b) intervals of segment p-q inside poly."""
    dx, dy = q[0]-p[0], q[1]-p[1]
    ts = [0.0, 1.0]
    for i in range(len(poly)):
        a, b = poly[i], poly[(i+1) % len(poly)]
        ex, ey = b[0]-a[0], b[1]-a[1]
        den = dx*ey - dy*ex
        if abs(den) < 1e-12:
            continue
        t = ((a[0]-p[0])*ey - (a[1]-p[1])*ex) / den
        u = ((a[0]-p[0])*dy - (a[1]-p[1])*dx) / den
        if -1e-9 <= t <= 1+1e-9 and -1e-9 <= u <= 1+1e-9:
            ts.append(min(1, max(0, t)))
    ts = sorted(set(round(t, 9) for t in ts))
    out = []
    for t0, t1 in zip(ts, ts[1:]):
        if t1 - t0 < 1e-9:
            continue
        m = (t0 + t1) / 2
        if inside((p[0]+dx*m, p[1]+dy*m), poly):
            out.append(((p[0]+dx*t0, p[1]+dy*t0), (p[0]+dx*t1, p[1]+dy*t1)))
    return out


def clip_polyline(pts, poly):
    pieces = []
    for p, q in zip(pts, pts[1:]):
        for a, b in seg_clip(p, q, poly):
            if pieces and pieces[-1][-1] == a:
                pieces[-1].append(b)
            else:
                pieces.append([a, b])
    return pieces


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: fix_schmidt_clip.py SRC.svg OUT.svg")
    src, out = sys.argv[1], sys.argv[2]
    tree = etree.parse(src)
    root = tree.getroot()
    clip = root.find(".//*[@id='clipPath5795']/*")
    poly = parse_clip(clip.get("d"))
    g = root.find(".//*[@id='g5693']")
    if g is None:
        raise SystemExit("g5693 not found")
    g.attrib.pop("clip-path", None)
    for child in list(g):
        d = child.get("d")
        if not d:
            continue
        pts = parse_path(d)
        pieces = clip_polyline(pts, poly)
        if not pieces:
            g.remove(child)
            continue
        nd = " ".join(
            "M %.3f,%.3f " % (p[0][0], p[0][1])
            + " ".join("L %.3f,%.3f" % (q[0], q[1]) for q in p[1:])
            for p in pieces)
        child.set("d", nd)
    tree.write(out, encoding="utf-8", xml_declaration=False)
    print("wrote", out, "clip polygon points", len(poly), "hatch children", len(g))


if __name__ == "__main__":
    main()
