#!/usr/bin/env python3
"""Minimal vector-page -> Tektronix 4010/4014 stream converter.

Reads one page of a vector PDF or SVG through PyMuPDF, takes the stroke
outlines, flattens curves, fits the drawing into the 4096x3120 Tek viewport
and emits a 7-bit Tek stream (ESC FF, solid line, GS polylines).

This is deliberately stroke-only: fills are represented by their outline.
It is meant for line art (patent-style drawings, technical diagrams, maps),
not for photographs.  Raster-only pages are rejected instead of traced.

Requires: pymupdf (tested 1.28.2).
"""

import argparse
import math
import sys

import pymupdf

TEK_W = 4096
TEK_H = 3120
EPS = 1e-4


def flatten_drawing(drawing, tol):
    """Return a list of page-space polylines for one PyMuPDF drawing.

    PyMuPDF concatenates subpaths without explicit move items, so a jump
    between the previous endpoint and the next item starts a new polyline.
    """
    polys = []
    cur = []

    def flush():
        nonlocal cur
        if len(cur) >= 2:
            polys.append(cur)
        cur = []

    def add(pt):
        if not cur:
            cur.append(pt)
            return
        last = cur[-1]
        if abs(last.x - pt.x) <= EPS and abs(last.y - pt.y) <= EPS:
            return
        cur.append(pt)

    def cubic(p0, p1, p2, p3, depth=0):
        dx = p3.x - p0.x
        dy = p3.y - p0.y
        d1 = abs((p1.x - p0.x) * dy - (p1.y - p0.y) * dx)
        d2 = abs((p2.x - p0.x) * dy - (p2.y - p0.y) * dx)
        chord = math.hypot(dx, dy)
        if depth >= 18 or (chord > 0 and d1 + d2 <= tol * chord * 0.5):
            add(p3)
            return
        p01 = pymupdf.Point((p0.x + p1.x) * 0.5, (p0.y + p1.y) * 0.5)
        p12 = pymupdf.Point((p1.x + p2.x) * 0.5, (p1.y + p2.y) * 0.5)
        p23 = pymupdf.Point((p2.x + p3.x) * 0.5, (p2.y + p3.y) * 0.5)
        p012 = pymupdf.Point((p01.x + p12.x) * 0.5, (p01.y + p12.y) * 0.5)
        p123 = pymupdf.Point((p12.x + p23.x) * 0.5, (p12.y + p23.y) * 0.5)
        p0123 = pymupdf.Point((p012.x + p123.x) * 0.5,
                              (p012.y + p123.y) * 0.5)
        cubic(p0, p01, p012, p0123, depth + 1)
        cubic(p0123, p123, p23, p3, depth + 1)

    for item in drawing["items"]:
        kind = item[0]
        if kind == "l":
            a, b = item[1], item[2]
            if cur and (abs(cur[-1].x - a.x) > EPS or
                        abs(cur[-1].y - a.y) > EPS):
                flush()
            add(a)
            add(b)
        elif kind == "c":
            a, b, c, d = item[1], item[2], item[3], item[4]
            if cur and (abs(cur[-1].x - a.x) > EPS or
                        abs(cur[-1].y - a.y) > EPS):
                flush()
            add(a)
            cubic(a, b, c, d)
        elif kind in ("re", "qu"):
            flush()
            r = item[1]
            if kind == "re":
                pts = [pymupdf.Point(r.x0, r.y0), pymupdf.Point(r.x1, r.y0),
                       pymupdf.Point(r.x1, r.y1), pymupdf.Point(r.x0, r.y1),
                       pymupdf.Point(r.x0, r.y0)]
            else:
                pts = [r.ul, r.ur, r.lr, r.ll, r.ul]
            polys.append(pts)
    flush()
    return polys


def bbox_of(polys):
    xs = [p.x for poly in polys for p in poly]
    ys = [p.y for poly in polys for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def transform(polys, bbox, margin):
    x0, y0, x1, y1 = bbox
    bw = max(x1 - x0, 1e-9)
    bh = max(y1 - y0, 1e-9)
    avail_w = TEK_W - 2 * margin
    avail_h = TEK_H - 2 * margin
    scale = min(avail_w / bw, avail_h / bh)
    # Center the used extent in the viewport.
    used_w = bw * scale
    used_h = bh * scale
    ox = (TEK_W - used_w) * 0.5
    oy = (TEK_H - used_h) * 0.5

    out = []
    for poly in polys:
        q = []
        for p in poly:
            x = int(round(ox + (p.x - x0) * scale))
            y = int(round(TEK_H - oy - (p.y - y0) * scale))
            x = max(0, min(TEK_W - 1, x))
            y = max(0, min(TEK_H - 1, y))
            if q and q[-1] == (x, y):
                continue
            q.append((x, y))
        if len(q) >= 2:
            out.append(q)
    return out, scale


def perp_dist(p, a, b):
    ax, ay = a
    bx, by = b
    px, py = p
    dx = bx - ax
    dy = by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    return abs(dx * (ay - py) - (ax - px) * dy) / math.hypot(dx, dy)


def rdp(points, tol):
    if len(points) <= 2:
        return points
    a, b = points[0], points[-1]
    best = -1.0
    best_i = 0
    for i in range(1, len(points) - 1):
        d = perp_dist(points[i], a, b)
        if d > best:
            best = d
            best_i = i
    if best > tol:
        left = rdp(points[:best_i + 1], tol)
        right = rdp(points[best_i:], tol)
        return left[:-1] + right
    return [a, b]


def simplify(polys, tol):
    if tol <= 0:
        return polys
    out = []
    for poly in polys:
        q = rdp(poly, tol)
        if len(q) >= 2:
            out.append(q)
    return out


def encoded_size(polys):
    return 2 + sum(1 + 5 * len(p) for p in polys)


def coord(x, y):
    return bytes((
        0x20 | ((y >> 7) & 0x1F),
        0x60 | (((y & 3) << 2) | (x & 3)),
        0x60 | ((y >> 2) & 0x1F),
        0x20 | ((x >> 7) & 0x1F),
        0x40 | ((x >> 2) & 0x1F),
    ))


def encode(polys, caption=None):
    out = bytearray(b"\x1b\x0c\x1b\x60")  # clear page, solid line
    for poly in polys:
        out.append(0x1D)  # GS: first coordinate is a move
        for x, y in poly:
            out += coord(x, y)
    if caption:
        out += caption_stream(caption)
    return bytes(out)


def caption_stream(text):
    # Put a one-line caption at font size 1, left margin 96, baseline 120.
    # US moves the alpha cursor to the beam; GS returns to graph mode.
    x, y = 96, 120
    out = bytearray()
    out += b"\x1d" + coord(x, y)     # move beam
    out += b"\x1f"                    # US: alpha cursor = beam
    out += b"\x1b\x39"                # font 1: 48x80 units
    out += text.encode("ascii", "replace")
    out += b"\x1d" + coord(x, y)      # leave graph mode, cursor off
    return bytes(out)


def compress_to_budget(polys, max_bytes):
    total = encoded_size(polys)
    tol = 1.0
    while total > max_bytes and tol <= 64:
        cand = simplify(polys, tol)
        cand = [p for p in cand if len(p) >= 2]
        total = encoded_size(cand)
        if total <= max_bytes:
            return cand, total, tol
        tol *= 1.5
    if total <= max_bytes:
        return polys, total, 0.0
    # Last resort: drop the shortest polylines until it fits.
    ranked = sorted(range(len(polys)), key=lambda i: -polyline_len(polys[i]))
    keep = []
    total = 2
    for i in ranked:
        cost = 1 + 5 * len(polys[i])
        if total + cost > max_bytes:
            continue
        keep.append(i)
        total += cost
    keep.sort()
    out = [polys[i] for i in keep]
    return out, encoded_size(out), -1.0


def polyline_len(poly):
    return sum(math.hypot(poly[i + 1][0] - poly[i][0],
                          poly[i + 1][1] - poly[i][1])
               for i in range(len(poly) - 1))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--page", type=int, default=0)
    ap.add_argument("--margin", type=int, default=96)
    ap.add_argument("--tolerance", type=float, default=0.6,
                    help="curve flattening tolerance in source units")
    ap.add_argument("--max-bytes", type=int, default=24576)
    ap.add_argument("--caption", default=None)
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    doc = pymupdf.open(args.input)
    if args.page < 0 or args.page >= len(doc):
        sys.exit(f"page {args.page} out of range (0..{len(doc)-1})")
    page = doc[args.page]
    images = page.get_images(full=True)
    drawings = page.get_drawings()
    if not drawings:
        sys.exit(f"no vector paths on page {args.page} "
                 f"({len(images)} raster images) -- raster-only, not converting")

    polys = []
    for d in drawings:
        # A white fill with no stroke is a background/knockout shape.  Stroking
        # it would add a bogus page frame or centre line to the Tek page.
        if d.get("color") is None and d.get("fill") is not None:
            if all(c >= 0.999 for c in d["fill"]):
                continue
        polys.extend(flatten_drawing(d, args.tolerance))
    polys = [p for p in polys if len(p) >= 2]
    if not polys:
        sys.exit("vector paths present but no drawable polylines")

    bbox = bbox_of(polys)
    tek_polys, scale = transform(polys, bbox, args.margin)
    tek_polys, size, used_tol = compress_to_budget(tek_polys, args.max_bytes)
    data = encode(tek_polys, args.caption)
    with open(args.output, "wb") as f:
        f.write(data)

    if images:
        print(f"warning: page {args.page} has both vector paths and "
              f"{len(images)} raster image(s); raster content is ignored",
              file=sys.stderr)

    if args.stats:
        print(f"source: {args.input} page {args.page}")
        print(f"vector paths: {len(drawings)}  raster images: {len(images)}")
        print(f"source bbox: {bbox[0]:.1f},{bbox[1]:.1f} .. "
              f"{bbox[2]:.1f},{bbox[3]:.1f}  scale={scale:.4f} Tek/source")
        print(f"polylines: {len(tek_polys)}  points: "
              f"{sum(len(p) for p in tek_polys)}")
        print(f"simplify tolerance: {used_tol} Tek units")
        print(f"stream bytes: {len(data)} / {args.max_bytes} "
              f"({len(data)*100.0/args.max_bytes:.1f}%)")


if __name__ == "__main__":
    main()
