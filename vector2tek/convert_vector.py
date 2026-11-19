#!/usr/bin/env python3
"""Vector page -> Tektronix 4010/4014 stream, with optional Tek text and fill hatching.

Pipeline: PyMuPDF page -> strokes / fill polygons / text spans -> optional
crop and rotation -> optional split reflow -> fit to 4096x3120 -> hatch dark
fills + place horizontal text in the built-in Tek font -> 7-bit Tek stream.

Every option applies to the one page being converted, so a marginal page can
override the defaults without touching the other pages:

  --fills outline|hatch|skip   fill policy
  --rotate 0|90|180|270        rotate the page clockwise
  --crop x0,y0,x1,y1           page fractions, clipped for real
  --split-aspect R             reflow a long page into bands on one page
  --text-min N                 minimum Tek cell height for a text span
  --outline-tol N              RDP tolerance for fill outlines


Default fill mode is "outline" (the old behaviour).  Use --fills hatch for
the recovery pages.  Text is optional via --no-text.  Raster-only pages are
rejected; mixed pages keep only their vector content.
"""

import argparse
import math
import os
import shutil
import subprocess
import sys
import tempfile

import pymupdf

TEK_W = 4096
TEK_H = 3120
EPS = 1e-4
HEADER = 4  # ESC FF + ESC 60
# Tek font sizes: (hsize, vsize) in Tek units.
FONT = ((52, 88), (48, 80), (32, 52), (28, 48))


# ---------------------------------------------------------------- geometry


def flatten_drawing(drawing, tol):
    """Return page-space polylines for one PyMuPDF drawing.

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


def union_bbox(*boxes):
    if not any(boxes):
        return None
    xs0 = [b[0] for b in boxes if b]
    ys0 = [b[1] for b in boxes if b]
    xs1 = [b[2] for b in boxes if b]
    ys1 = [b[3] for b in boxes if b]
    return min(xs0), min(ys0), max(xs1), max(ys1)


def transform_polys(polys, bbox, margin):
    """Map page-space polylines to integer Tek coordinates, y up."""
    x0, y0, x1, y1 = bbox
    bw = max(x1 - x0, 1e-9)
    bh = max(y1 - y0, 1e-9)
    avail_w = TEK_W - 2 * margin
    avail_h = TEK_H - 2 * margin
    scale = min(avail_w / bw, avail_h / bh)
    used_w = bw * scale
    used_h = bh * scale
    ox = (TEK_W - used_w) * 0.5
    oy = (TEK_H - used_h) * 0.5

    out = []
    for poly in polys:
        q = []
        for p in poly:
            x = int(round(ox + (p[0] - x0) * scale))
            y = int(round(TEK_H - oy - (p[1] - y0) * scale))
            x = max(0, min(TEK_W - 1, x))
            y = max(0, min(TEK_H - 1, y))
            if q and q[-1] == (x, y):
                continue
            q.append((x, y))
        if len(q) >= 2:
            out.append(q)
    return out, scale, ox, oy


def close_ring(poly):
    if len(poly) < 3:
        return None
    if poly[0] != poly[-1]:
        poly = poly + [poly[0]]
    return poly


def rotate_point(pt, cx, cy, degrees):
    """Rotate one (x, y) point clockwise on screen (y down)."""
    if not degrees:
        return pt
    a = math.radians(degrees)
    ca, sa = math.cos(a), math.sin(a)
    dx = pt[0] - cx
    dy = pt[1] - cy
    return (cx + dx * ca - dy * sa, cy + dx * sa + dy * ca)


def rotate_rect(rect, cx, cy, degrees):
    x0, y0, x1, y1 = rect
    pts = [rotate_point(p, cx, cy, degrees)
           for p in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def clip_segment_rect(a, b, rect):
    """Liang-Barsky; return (t0, t1) of the visible part, or None."""
    x0, y0, x1, y1 = rect
    ax, ay = a
    dx = b[0] - ax
    dy = b[1] - ay
    ps = (-dx, dx, -dy, dy)
    qs = (ax - x0, x1 - ax, ay - y0, y1 - ay)
    t0, t1 = 0.0, 1.0
    for p, q in zip(ps, qs):
        if abs(p) <= 1e-12:
            if q < 0:
                return None
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return None
    return t0, t1


def clip_polyline_rect(poly, rect):
    """Clip an open polyline to a rectangle; return a list of runs."""
    runs = []
    cur = []
    for a, b in zip(poly, poly[1:]):
        hit = clip_segment_rect(a, b, rect)
        if hit is None:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            continue
        t0, t1 = hit
        p0 = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
        p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
        if cur and abs(cur[-1][0] - p0[0]) <= 1e-7 and \
                abs(cur[-1][1] - p0[1]) <= 1e-7:
            cur.append(p1)
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [p0, p1]
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def _inside_edge(p, edge, rect):
    x0, y0, x1, y1 = rect
    return (p[0] >= x0 if edge == 0 else
            p[0] <= x1 if edge == 1 else
            p[1] >= y0 if edge == 2 else p[1] <= y1)


def _edge_intersect(a, b, edge, rect):
    x0, y0, x1, y1 = rect
    if edge in (0, 1):
        x = x0 if edge == 0 else x1
        t = (x - a[0]) / (b[0] - a[0])
        return (x, a[1] + (b[1] - a[1]) * t)
    y = y0 if edge == 2 else y1
    t = (y - a[1]) / (b[1] - a[1])
    return (a[0] + (b[0] - a[0]) * t, y)


def clip_polygon_rect(poly, rect):
    """Sutherland-Hodgman.  Return (points, clipped) or (None, True).

    The returned polygon is closed when it was fully inside the rectangle,
    and left open when the rectangle cut it (so the cut edge is not drawn).
    """
    pts = list(poly)
    if len(pts) > 1 and pts[0] == pts[-1]:
        pts = pts[:-1]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    clipped = not (rect[0] <= min(xs) and max(xs) <= rect[2] and
                   rect[1] <= min(ys) and max(ys) <= rect[3])
    for edge in range(4):
        if not pts:
            return None, True
        out = []
        for i, cur in enumerate(pts):
            prev = pts[i - 1]
            ci = _inside_edge(cur, edge, rect)
            pi = _inside_edge(prev, edge, rect)
            if ci:
                if not pi:
                    out.append(_edge_intersect(prev, cur, edge, rect))
                out.append(cur)
            elif pi:
                out.append(_edge_intersect(prev, cur, edge, rect))
        pts = out
    if len(pts) < 3:
        return None, True
    if not clipped:
        pts = pts + [pts[0]]
    return pts, clipped



# ---------------------------------------------------------------- text


def collect_spans(page):
    """Return all non-empty text spans with their page-space geometry."""
    spans = []
    for block in page.get_text("dict").get("blocks", []):
        for line in block.get("lines", []):
            for s in line.get("spans", []):
                text = s.get("text", "").replace("\n", " ")
                if not text.strip():
                    continue
                bb = s.get("bbox")
                if not bb:
                    continue
                size = float(s.get("size") or 0.0)
                if size <= 0:
                    size = float(bb[3] - bb[1])
                origin = s.get("origin")
                if origin is None:
                    origin = (bb[0], bb[3])
                spans.append({
                    "text": text, "dir": s.get("dir", (1, 0)),
                    "bbox": tuple(float(v) for v in bb),
                    "origin": (float(origin[0]), float(origin[1])),
                    "size": size,
                })
    return spans


def text_bbox(spans):
    """Union bbox of horizontal spans (the only ones that can be placed)."""
    boxes = []
    for s in spans:
        d = s["dir"]
        if abs(d[1]) > 0.02 or d[0] < 0.9:
            continue
        boxes.append(s["bbox"])
    if not boxes:
        return None
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def crop_spans(spans, rect):
    out = []
    for s in spans:
        b = s["bbox"]
        cx = (b[0] + b[2]) * 0.5
        cy = (b[1] + b[3]) * 0.5
        if rect[0] <= cx <= rect[2] and rect[1] <= cy <= rect[3]:
            out.append(s)
    return out


def rotate_spans(spans, cx, cy, degrees):
    if not degrees:
        return spans
    out = []
    for s in spans:
        b = s["bbox"]
        corners = [rotate_point((x, y), cx, cy, degrees)
                   for x, y in ((b[0], b[1]), (b[2], b[1]),
                                (b[2], b[3]), (b[0], b[3]))]
        xs = [p[0] for p in corners]
        ys = [p[1] for p in corners]
        out.append(dict(s,
                        origin=rotate_point(s["origin"], cx, cy, degrees),
                        bbox=(min(xs), min(ys), max(xs), max(ys))))
    return out


def translate_spans(spans, dx, dy):
    return [dict(s, origin=(s["origin"][0] + dx, s["origin"][1] + dy),
                 bbox=(s["bbox"][0] + dx, s["bbox"][1] + dy,
                       s["bbox"][2] + dx, s["bbox"][3] + dy))
            for s in spans]


def text_entries(spans, bbox, scale, ox, oy, args):
    """Return (entries, stats) for horizontal text spans that fit the Tek font."""
    x0, y0, x1, y1 = bbox
    stats = {
        "spans": 0, "rotated": 0, "small": 0, "overflow": 0,
        "overlap": 0, "empty": 0, "rendered": 0,
        "chars_source": 0, "chars_rendered": 0, "chars_nonascii": 0,
        "chars_truncated": 0, "dropped_budget": 0,
    }
    out = []
    placed = []
    for s in spans:
        text = s["text"].replace("\n", " ").strip()
        if not text:
            continue
        stats["spans"] += 1
        d = s["dir"]
        if abs(d[1]) > 0.02 or d[0] < 0.9:
            stats["rotated"] += 1
            continue
        stats["chars_source"] += len(text)
        size = s["size"]
        if size <= 0:
            stats["empty"] += 1
            continue
        target_cell = size * scale
        if target_cell < args.min_text_cell:
            stats["small"] += 1
            continue
        idx = min(range(4),
                  key=lambda i: abs(FONT[i][1] - target_cell))
        hsize, vsize = FONT[idx]

        ascii_chars = []
        dropped = 0
        for ch in text:
            o = ord(ch)
            if 32 <= o <= 126:
                ascii_chars.append(ch)
            else:
                dropped += 1
        stats["chars_nonascii"] += dropped
        ascii_text = "".join(ascii_chars).strip()
        if not ascii_text:
            stats["empty"] += 1
            continue

        origin = s["origin"]
        x = int(round(ox + (origin[0] - x0) * scale))
        y = int(round(TEK_H - oy - (origin[1] - y0) * scale))
        if not (0 <= x < TEK_W and 0 <= y < TEK_H):
            stats["overflow"] += 1
            continue
        max_chars = (TEK_W - 4 - x) // hsize
        if max_chars < 1:
            stats["overflow"] += 1
            continue
        if len(ascii_text) > max_chars:
            stats["chars_truncated"] += len(ascii_text) - max_chars
            ascii_text = ascii_text[:max_chars]
            if not ascii_text:
                stats["overflow"] += 1
                continue

        tx0 = x
        tx1 = x + len(ascii_text) * hsize
        ty0 = y - 16
        ty1 = y + vsize - 16
        new_area = max(1, (tx1 - tx0) * (ty1 - ty0))
        clash = 0.0
        for b in placed:
            ix = max(0, min(tx1, b[2]) - max(tx0, b[0]))
            iy = max(0, min(ty1, b[3]) - max(ty0, b[1]))
            clash = max(clash, ix * iy / new_area)
        if clash > args.text_overlap:
            stats["overlap"] += 1
            continue

        entry = {
            "text": ascii_text, "size": idx, "x": x, "y": y,
            "hsize": hsize, "vsize": vsize,
            "bbox": (tx0, ty0, tx1, ty1),
            "source_size": size,
        }
        out.append(entry)
        placed.append(entry["bbox"])
        stats["rendered"] += 1
        stats["chars_rendered"] += len(ascii_text)
    out.sort(key=lambda e: (-e["source_size"], e["y"], e["x"]))
    return out, stats


def poly_bbox(polys):
    xs = [p[0] for poly in polys for p in poly]
    ys = [p[1] for poly in polys for p in poly]
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def crop_fills(fills, rect):
    out = []
    for f in fills:
        rings = []
        for ring in f["rings"]:
            q, _ = clip_polygon_rect(ring, rect)
            if q:
                rings.append(q)
        if rings:
            g = dict(f)
            g["rings"] = rings
            g["bbox"] = poly_bbox(rings)
            out.append(g)
    return out


def rotate_polys(polys, cx, cy, degrees):
    if not degrees:
        return polys
    return [[rotate_point(p, cx, cy, degrees) for p in poly]
            for poly in polys]


def rotate_fills(fills, cx, cy, degrees):
    if not degrees:
        return fills
    out = []
    for f in fills:
        g = dict(f)
        g["rings"] = [[rotate_point(p, cx, cy, degrees) for p in ring]
                      for ring in f["rings"]]
        g["bbox"] = poly_bbox(g["rings"])
        out.append(g)
    return out


def split_layout(strokes, fills, spans, bbox, split_aspect, gap_tek, margin):
    """Reflow a long page into bands on the same Tek page.

    The bands are translated into a virtual page in source units; the normal
    fit then scales that virtual page once, so a band keeps a single scale.
    """
    x0, y0, x1, y1 = bbox
    width = x1 - x0
    height = y1 - y0
    if split_aspect <= 0 or width <= 0 or height <= 0:
        return strokes, fills, spans, bbox, {"bands": 1, "axis": None,
                                             "gap_tek": 0.0}
    aspect = max(width, height) / min(width, height)
    if aspect <= split_aspect:
        return strokes, fills, spans, bbox, {"bands": 1, "axis": None,
                                             "gap_tek": 0.0}

    avail_w = TEK_W - 2 * margin
    avail_h = TEK_H - 2 * margin
    if width >= height:
        bands = min(8, max(2, int(math.ceil(aspect / split_aspect))))
        band_w = width / bands
        est = min(bands * avail_w / width, avail_h / (bands * height))
        gap = gap_tek / max(est, 1e-6)
        v_strokes = []
        v_fills = []
        v_spans = []
        for i in range(bands):
            rect = (x0 + i * band_w, y0, x0 + (i + 1) * band_w, y1)
            dx = -(x0 + i * band_w)
            dy = -y0 + i * (height + gap)
            for poly in strokes:
                for run in clip_polyline_rect(poly, rect):
                    v_strokes.append([(p[0] + dx, p[1] + dy) for p in run])
            for f in fills:
                rings = []
                for ring in f["rings"]:
                    q, _ = clip_polygon_rect(ring, rect)
                    if q:
                        rings.append([(p[0] + dx, p[1] + dy) for p in q])
                if rings:
                    g = dict(f)
                    g["rings"] = rings
                    g["bbox"] = poly_bbox(rings)
                    v_fills.append(g)
            for span in spans:
                ox, oy = span["origin"]
                if rect[0] <= ox <= rect[2]:
                    v_spans.append(translate_spans([span], dx, dy)[0])
        v_bbox = (0.0, 0.0, band_w,
                  bands * height + (bands - 1) * gap)
        info = {"bands": bands, "axis": "x", "gap_tek": round(gap * est, 1),
                "source_band": [round(band_w, 2), round(height, 2)]}
    else:
        bands = min(8, max(2, int(math.ceil(aspect / split_aspect))))
        band_h = height / bands
        est = min(avail_w / (bands * width), bands * avail_h / height)
        gap = gap_tek / max(est, 1e-6)
        v_strokes = []
        v_fills = []
        v_spans = []
        for i in range(bands):
            rect = (x0, y0 + i * band_h, x1, y0 + (i + 1) * band_h)
            dx = -x0 + i * (width + gap)
            dy = -(y0 + i * band_h)
            for poly in strokes:
                for run in clip_polyline_rect(poly, rect):
                    v_strokes.append([(p[0] + dx, p[1] + dy) for p in run])
            for f in fills:
                rings = []
                for ring in f["rings"]:
                    q, _ = clip_polygon_rect(ring, rect)
                    if q:
                        rings.append([(p[0] + dx, p[1] + dy) for p in q])
                if rings:
                    g = dict(f)
                    g["rings"] = rings
                    g["bbox"] = poly_bbox(rings)
                    v_fills.append(g)
            for span in spans:
                ox, oy = span["origin"]
                if rect[1] <= oy <= rect[3]:
                    v_spans.append(translate_spans([span], dx, dy)[0])
        v_bbox = (0.0, 0.0, bands * width + (bands - 1) * gap, band_h)
        info = {"bands": bands, "axis": "y", "gap_tek": round(gap * est, 1),
                "source_band": [round(width, 2), round(band_h, 2)]}
    return v_strokes, v_fills, v_spans, v_bbox, info


def text_stream(t):
    out = bytearray()
    out += b"\x1d" + coord(t["x"], t["y"])
    out += b"\x1f"
    out += bytes((0x1B, 0x38 + t["size"]))
    out += t["text"].encode("ascii")
    out += b"\x1d" + coord(t["x"], t["y"])
    return bytes(out)


# ---------------------------------------------------------------- hatching


def hatch_rings(rings, spacing, angle, max_lines):
    """Scanline-hatch closed Tek-coordinate rings; return 2-point polylines.

    Uses even-odd pairing, so a ring inside another ring becomes a hole.
    Returns None if more than max_lines would be produced.
    """
    if spacing <= 0:
        return []
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    # Rotate by -angle: scan horizontal lines in the rotated frame.
    rrings = []
    for ring in rings:
        rrings.append([(x * ca + y * sa, -x * sa + y * ca) for x, y in ring])
    ys = [p[1] for ring in rrings for p in ring]
    if not ys:
        return []
    ymin, ymax = min(ys), max(ys)
    y = math.ceil(ymin / spacing) * spacing
    lines = []
    while y <= ymax:
        xs = []
        for ring in rrings:
            n = len(ring) - 1 if ring[0] == ring[-1] else len(ring)
            for i in range(n):
                ax, ay = ring[i]
                bx, by = ring[(i + 1) % n]
                if (ay <= y < by) or (by <= y < ay):
                    t = (y - ay) / (by - ay)
                    xs.append(ax + t * (bx - ax))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] <= 0.7:
                continue
            xa = xs[i] * ca - y * sa
            ya = xs[i] * sa + y * ca
            xb = xs[i + 1] * ca - y * sa
            yb = xs[i + 1] * sa + y * ca
            pa = (int(round(xa)), int(round(ya)))
            pb = (int(round(xb)), int(round(yb)))
            if pa == pb:
                continue
            lines.append([pa, pb])
            if len(lines) > max_lines:
                return None
        y += spacing
    return lines


def transform_one(poly, bbox, scale, ox, oy):
    x0, y0, _, _ = bbox
    return [(int(round(ox + (p[0] - x0) * scale)),
             int(round(TEK_H - oy - (p[1] - y0) * scale))) for p in poly]


# ---------------------------------------------------------------- fills


def luminance(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def collect_fills(drawings, tol):
    fills = []
    white = 0
    for d in drawings:
        fill = d.get("fill")
        if fill is None:
            continue
        if all(c >= 0.97 for c in fill):
            white += 1
            continue
        rings = []
        for r in flatten_drawing(d, tol):
            if len(r) < 3:
                continue
            if abs(r[0].x - r[-1].x) > EPS or abs(r[0].y - r[-1].y) > EPS:
                r = r + [r[0]]
            rings.append([(p.x, p.y) for p in r])
        if not rings:
            continue
        xs = [p[0] for r in rings for p in r]
        ys = [p[1] for r in rings for p in r]
        fills.append({
            "rings": rings,
            "fill": fill,
            "stroke": d.get("color") is not None,
            "lum": luminance(fill),
            "bbox": (min(xs), min(ys), max(xs), max(ys)),
        })
    return fills, white


def add_fills(fills, bbox, scale, ox, oy, base_size, text_cost, args):
    """Greedily add hatch or outline polylines under the byte budget."""
    stats = {
        "mode": args.fills, "total": len(fills), "white_skipped": 0,
        "hatched": 0, "outlined": 0, "stroke_only": 0,
        "already_stroked": 0,
        "skipped_light": 0, "skipped_tiny": 0, "skipped_budget": 0,
        "skipped_cap": 0, "hatch_failed": 0, "hatch_skipped_small": 0,
        "hatch_segments": 0, "outline_polylines": 0,
        "hatch_spacing": args.hatch_spacing, "hatch_angle": args.hatch_angle,
        "min_hatch_short": args.min_hatch_short,
        "min_hatch_area": args.min_hatch_area,
        "outline_tol": args.outline_tol,
    }
    if args.fills == "skip":
        stats["skipped_cap"] = len(fills)
        return [], stats

    budget = max(0, args.max_bytes - base_size - text_cost - 128)
    used = 0
    hatch_total = 0
    out = []
    # Big areas first; hatching a large fill is visually more important than
    # spending the same bytes on hundreds of tiny ticks.
    ranked = sorted(fills, key=lambda f: -(f["bbox"][2] - f["bbox"][0]) *
                    (f["bbox"][3] - f["bbox"][1]))
    for i, f in enumerate(ranked):
        if i >= args.max_fills:
            stats["skipped_cap"] += 1
            continue
        if f["lum"] >= args.fill_light_lum:
            stats["skipped_light"] += 1
            continue
        bw = f["bbox"][2] - f["bbox"][0]
        bh = f["bbox"][3] - f["bbox"][1]
        if bw * bh * scale * scale < args.min_fill_area:
            stats["skipped_tiny"] += 1
            continue

        rings = []
        for r in f["rings"]:
            q = transform_one(r, bbox, scale, ox, oy)
            q = close_ring(q)
            if q:
                rings.append(q)
        if not rings:
            stats["skipped_budget"] += 1
            continue

        if f["stroke"]:
            stats["already_stroked"] += 1

        # Small fills stay outlines; they cannot carry readable hatching and
        # would only burn the per-page segment cap.
        tw = bw * scale
        th = bh * scale
        small_for_hatch = (min(tw, th) < args.min_hatch_short or
                           tw * th < args.min_hatch_area)

        # Dark solids get hatching if they fit.
        if (args.fills == "hatch" and f["lum"] <= args.fill_dark_lum and
                not small_for_hatch):
            segs = hatch_rings(rings, args.hatch_spacing,
                               args.hatch_angle, args.max_hatch_per_fill)
            if segs is None:
                stats["hatch_failed"] += 1
            elif segs:
                cost = sum(1 + 5 * len(s) for s in segs)
                if (cost <= budget - used and
                        hatch_total + len(segs) <= args.max_hatch_segments):
                    out.extend(segs)
                    used += cost
                    hatch_total += len(segs)
                    stats["hatched"] += 1
                    stats["hatch_segments"] += len(segs)
                    continue
                stats["hatch_failed"] += 1
            else:
                stats["hatch_failed"] += 1

        # Fallback: outline shapes that have no stroke of their own.
        if not f["stroke"]:
            outline = []
            for r in rings:
                q = rdp(r, args.outline_tol)
                if len(q) >= 2:
                    outline.append(q)
            cost = sum(1 + 5 * len(p) for p in outline)
            if outline and cost <= budget - used:
                out.extend(outline)
                used += cost
                stats["outlined"] += 1
                stats["outline_polylines"] += len(outline)
            else:
                stats["skipped_budget"] += 1
        else:
            # The stroke already carries the shape; hatching was optional.
            stats["stroke_only"] += 1
        if small_for_hatch and args.fills == "hatch" and \
                f["lum"] <= args.fill_dark_lum:
            stats["hatch_skipped_small"] += 1
    return out, stats


# ---------------------------------------------------------------- encoding


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
    return HEADER + sum(1 + 5 * len(p) for p in polys)


def coord(x, y):
    return bytes((
        0x20 | ((y >> 7) & 0x1F),
        0x60 | (((y & 3) << 2) | (x & 3)),
        0x60 | ((y >> 2) & 0x1F),
        0x20 | ((x >> 7) & 0x1F),
        0x40 | ((x >> 2) & 0x1F),
    ))


def encode(polys, texts=(), caption=None):
    out = bytearray(b"\x1b\x0c\x1b\x60")  # clear page, solid line
    for poly in polys:
        out.append(0x1D)
        for x, y in poly:
            out += coord(x, y)
    for t in texts:
        out += text_stream(t)
    if caption:
        out += caption_stream(caption)
    return bytes(out)


def caption_stream(text):
    x, y = 96, 120
    out = bytearray()
    out += b"\x1d" + coord(x, y)
    out += b"\x1f"
    out += b"\x1b\x39"
    out += text.encode("ascii", "replace")
    out += b"\x1d" + coord(x, y)
    return bytes(out)


def polyline_len(poly):
    return sum(math.hypot(poly[i + 1][0] - poly[i][0],
                          poly[i + 1][1] - poly[i][1])
               for i in range(len(poly) - 1))


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
    ranked = sorted(range(len(polys)), key=lambda i: -polyline_len(polys[i]))
    keep = []
    total = HEADER
    for i in ranked:
        cost = 1 + 5 * len(polys[i])
        if total + cost > max_bytes:
            continue
        keep.append(i)
        total += cost
    keep.sort()
    out = [polys[i] for i in keep]
    return out, encoded_size(out), -1.0



# ---------------------------------------------------------------- convert


def convert(inp, output, page_no=0, margin=96, tolerance=0.6,
            max_bytes=24576, caption=None, text=True, fill_mode="outline",
            min_text_cell=40.0, text_overlap=0.35,
            hatch_spacing=36.0, hatch_angle=45.0,
            max_fills=100, max_hatch_segments=300,
            max_hatch_per_fill=80, fill_dark_lum=0.55,
            fill_light_lum=0.90, min_fill_area=60.0,
            min_hatch_short=40.0, min_hatch_area=600.0,
            outline_tol=1.0, rotate=0, crop=None,
            split_aspect=0.0, split_gap=48.0,
            ):
    doc = pymupdf.open(inp)
    if page_no < 0 or page_no >= len(doc):
        raise ValueError(f"page {page_no} out of range (0..{len(doc)-1})")
    page = doc[page_no]
    images = page.get_images(full=True)
    drawings = page.get_drawings()
    if not drawings and not page.get_text("text").strip():
        raise ValueError(f"no vector paths on page {page_no} "
                         f"({len(images)} raster images) -- raster-only")

    # Strokes, fill rings and text spans in page space.
    strokes = []
    for d in drawings:
        if d.get("color") is not None:
            for poly in flatten_drawing(d, tolerance):
                strokes.append([(p.x, p.y) for p in poly])
    strokes = [p for p in strokes if len(p) >= 2]
    fill_list, white_fills = collect_fills(drawings, tolerance)
    spans = collect_spans(page) if text else []

    source_bbox = None
    if crop:
        pr = page.rect
        cr = (pr.x0 + crop[0] * pr.width, pr.y0 + crop[1] * pr.height,
              pr.x0 + crop[2] * pr.width, pr.y0 + crop[3] * pr.height)
        strokes = [run for poly in strokes
                   for run in clip_polyline_rect(poly, cr)]
        fill_list = crop_fills(fill_list, cr)
        spans = crop_spans(spans, cr)
        source_bbox = cr
    else:
        geom_bbox = poly_bbox(
            strokes + [ring for f in fill_list for ring in f["rings"]])
        tb = text_bbox(spans) if text else None
        source_bbox = union_bbox(geom_bbox, tb)
    if source_bbox is None:
        raise ValueError(f"page {page_no} has no content after crop")

    cx = (source_bbox[0] + source_bbox[2]) * 0.5
    cy = (source_bbox[1] + source_bbox[3]) * 0.5
    strokes = rotate_polys(strokes, cx, cy, rotate)
    fill_list = rotate_fills(fill_list, cx, cy, rotate)
    spans = rotate_spans(spans, cx, cy, rotate)
    layout = rotate_rect(source_bbox, cx, cy, rotate)

    strokes, fill_list, spans, bbox, split_info = split_layout(
        strokes, fill_list, spans, layout, split_aspect, split_gap, margin)

    # Fit the (possibly stacked) virtual page to 4096x3120.
    base, scale, ox, oy = transform_polys(strokes, bbox, margin)
    texts, tstats = ([], {})
    if text:
        texts, tstats = text_entries(
            spans, bbox, scale, ox, oy,
            argparse.Namespace(min_text_cell=min_text_cell,
                               text_overlap=text_overlap))
    text_cost = sum(15 + len(t["text"]) for t in texts)

    base_target = max(32, max_bytes - text_cost - 256)
    base, base_size, base_tol = compress_to_budget(base, base_target)

    fill_polys, fstats = add_fills(
        fill_list, bbox, scale, ox, oy, base_size, text_cost,
        argparse.Namespace(
            fills=fill_mode, max_bytes=max_bytes,
            hatch_spacing=hatch_spacing, hatch_angle=hatch_angle,
            max_fills=max_fills, max_hatch_segments=max_hatch_segments,
            max_hatch_per_fill=max_hatch_per_fill,
            fill_dark_lum=fill_dark_lum, fill_light_lum=fill_light_lum,
            min_fill_area=min_fill_area,
            min_hatch_short=min_hatch_short,
            min_hatch_area=min_hatch_area,
            outline_tol=outline_tol))
    fstats["white_skipped"] = white_fills

    polys = base + fill_polys
    poly_target = max(8, max_bytes - text_cost - 2)
    if encoded_size(polys) > poly_target:
        polys, _, final_tol = compress_to_budget(polys, poly_target)
    else:
        final_tol = base_tol

    data = encode(polys, texts, caption)
    dropped_text = 0
    # Text is priority: drop the smallest spans only if the page is still over.
    while len(data) > max_bytes and texts:
        texts.pop()
        dropped_text += 1
        data = encode(polys, texts, caption)
    if len(data) > max_bytes:
        polys, _, final_tol = compress_to_budget(polys, max_bytes - 4)
        data = encode(polys, texts, caption)
    tstats["dropped_budget"] = tstats.get("dropped_budget", 0) + dropped_text
    tstats["rendered"] = max(0, tstats.get("rendered", 0) - dropped_text)
    tstats["chars_rendered"] = sum(len(t["text"]) for t in texts)

    stats = {
        "source": inp, "page": page_no,
        "source_px": [round(page.rect.width), round(page.rect.height)],
        "raster_images": len(images), "drawings": len(drawings),
        "bbox": [round(v, 2) for v in source_bbox],
        "layout_bbox": [round(v, 2) for v in bbox],
        "scale": round(scale, 4),
        "options": {
            "fills": fill_mode, "rotate": rotate,
            "crop": list(crop) if crop else None,
            "split_aspect": split_aspect, "text_min": min_text_cell,
            "outline_tol": outline_tol,
        },
        "split": split_info,
        "strokes": {"polylines": len(base),
                    "points": sum(len(p) for p in base)},
        "fills": fstats,
        "text": tstats,
        "text_entries": [
            {"text": t["text"], "size": t["size"], "x": t["x"],
             "y": t["y"], "source_size": round(t["source_size"], 2)}
            for t in texts
        ],
        "tek_bytes": len(data), "max_bytes": max_bytes,
        "budget_pct": round(len(data) * 100.0 / max_bytes, 1),
        "polylines": len(polys),
        "points": sum(len(p) for p in polys),
        "simplify_tolerance": final_tol,
        "text_bytes": sum(15 + len(t["text"]) for t in texts),
    }
    with open(output, "wb") as fh:
        fh.write(data)
    return stats


def parse_crop(value):
    try:
        vals = [float(v) for v in value.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError("crop must be x0,y0,x1,y1 floats")
    if len(vals) != 4:
        raise argparse.ArgumentTypeError("crop must have four values")
    if not all(0.0 <= v <= 1.0 for v in vals):
        raise argparse.ArgumentTypeError("crop values are page fractions 0..1")
    if vals[0] >= vals[2] or vals[1] >= vals[3]:
        raise argparse.ArgumentTypeError("crop needs x0<x1 and y0<y1")
    return tuple(vals)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--page", type=int, default=0)
    ap.add_argument("--margin", type=int, default=96)
    ap.add_argument("--tolerance", type=float, default=0.6)
    ap.add_argument("--max-bytes", type=int, default=24576)
    ap.add_argument("--caption", default=None)
    ap.add_argument("--text", action=argparse.BooleanOptionalAction,
                    default=True)
    ap.add_argument("--fills", choices=("outline", "hatch", "skip"),
                    default="outline")
    ap.add_argument("--text-min", "--min-text-cell", dest="min_text_cell",
                    type=float, default=40.0, metavar="N",
                    help="minimum Tek cell height for a text span")
    ap.add_argument("--text-overlap", type=float, default=0.35)
    ap.add_argument("--rotate", type=int, choices=(0, 90, 180, 270),
                    default=0, help="rotate page clockwise before fitting")
    ap.add_argument("--crop", type=parse_crop, default=None, metavar="X0,Y0,X1,Y1",
                    help="page fractions, applied before --rotate")
    ap.add_argument("--split-aspect", type=float, default=0.0, metavar="R",
                    help="reflow a page longer than R:1 into bands on one page")
    ap.add_argument("--split-gap", type=float, default=48.0, metavar="N",
                    help="gap between split bands in Tek units")
    ap.add_argument("--outline-tol", type=float, default=1.0, metavar="N",
                    help="RDP tolerance for fill outlines in Tek units")
    ap.add_argument("--hatch-spacing", type=float, default=36.0)
    ap.add_argument("--hatch-angle", type=float, default=45.0)
    ap.add_argument("--max-fills", type=int, default=100)
    ap.add_argument("--max-hatch-segments", type=int, default=300)
    ap.add_argument("--max-hatch-per-fill", type=int, default=80)
    ap.add_argument("--fill-dark-lum", type=float, default=0.55)
    ap.add_argument("--fill-light-lum", type=float, default=0.90)
    ap.add_argument("--min-fill-area", type=float, default=60.0)
    ap.add_argument("--min-hatch-short", type=float, default=40.0)
    ap.add_argument("--min-hatch-area", type=float, default=600.0)
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    try:
        stats = convert(
            args.input, args.output, page_no=args.page, margin=args.margin,
            tolerance=args.tolerance, max_bytes=args.max_bytes,
            caption=args.caption, text=args.text, fill_mode=args.fills,
            min_text_cell=args.min_text_cell, text_overlap=args.text_overlap,
            hatch_spacing=args.hatch_spacing, hatch_angle=args.hatch_angle,
            max_fills=args.max_fills,
            max_hatch_segments=args.max_hatch_segments,
            max_hatch_per_fill=args.max_hatch_per_fill,
            fill_dark_lum=args.fill_dark_lum,
            fill_light_lum=args.fill_light_lum,
            min_fill_area=args.min_fill_area,
            min_hatch_short=args.min_hatch_short,
            min_hatch_area=args.min_hatch_area,
            outline_tol=args.outline_tol, rotate=args.rotate, crop=args.crop,
            split_aspect=args.split_aspect, split_gap=args.split_gap)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if stats["raster_images"]:
        print(f"warning: page {args.page} has both vector paths and "
              f"{stats['raster_images']} raster image(s); raster ignored",
              file=sys.stderr)
    if args.stats:
        print(f"source: {stats['source']} page {stats['page']}")
        print(f"vector paths: {stats['drawings']}  raster images: "
              f"{stats['raster_images']}")
        print(f"source bbox: {stats['bbox']}  scale={stats['scale']}")
        print(f"options: {stats['options']}")
        print(f"split: {stats['split']}")
        print(f"strokes: {stats['strokes']['polylines']} polylines / "
              f"{stats['strokes']['points']} points")
        print(f"fills: {stats['fills']}")
        print(f"text: {stats['text']}")
        print(f"polylines: {stats['polylines']}  points: {stats['points']}")
        print(f"simplify tolerance: {stats['simplify_tolerance']} Tek units")
        print(f"stream bytes: {stats['tek_bytes']} / {stats['max_bytes']} "
              f"({stats['budget_pct']}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
