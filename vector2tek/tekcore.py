#!/usr/bin/env python3
"""Shared Tektronix 4010/4014 geometry, encoding and validation helpers.

This module is the dependency-free core used by the non-PDF importers
(``dxf2tek`` and ``map2tek``).  It contains:

  - the 4096x3120 fit transform for y-up source coordinates;
  - RDP simplification and byte-budget compression;
  - Tek 7-bit stream encoding with optional line styles and alpha text;
  - a strict stream validator used by the tests and by ``--check``;

"""

import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

TEK_W = 4096
TEK_H = 3120
EPS = 1e-9
HEADER = 4  # ESC FF + ESC 60
MAX_BYTES = 24576
# Tek font sizes: (hsize, vsize) in Tek units.
FONT = ((52, 88), (48, 80), (32, 52), (28, 48))
# Tek line styles selected by ESC 0x60..0x63 (solid, dotted, dashed,
# dot-dash).  The panel is monochrome, so styles are the only way to keep
# source colours/layers apart.
LINE_STYLES = 4


# ---------------------------------------------------------------- geometry


def poly_bbox(polys):
    xs = [p[0] for poly in polys for p in poly]
    ys = [p[1] for poly in polys for p in poly]
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def union_bbox(*boxes):
    boxes = [b for b in boxes if b]
    if not boxes:
        return None
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def fit_transform(bbox, margin=96):
    """Return (scale, ox, oy) mapping source coordinates to the Tek frame."""
    x0, y0, x1, y1 = bbox
    bw = max(x1 - x0, EPS)
    bh = max(y1 - y0, EPS)
    avail_w = TEK_W - 2 * margin
    avail_h = TEK_H - 2 * margin
    scale = min(avail_w / bw, avail_h / bh)
    used_w = bw * scale
    used_h = bh * scale
    ox = (TEK_W - used_w) * 0.5
    oy = (TEK_H - used_h) * 0.5
    return scale, ox, oy


def _map_poly(poly, x0, y0, scale, ox, oy):
    q = []
    for p in poly:
        x = int(round(ox + (p[0] - x0) * scale))
        y = int(round(oy + (p[1] - y0) * scale))
        x = max(0, min(TEK_W - 1, x))
        y = max(0, min(TEK_H - 1, y))
        if q and q[-1] == (x, y):
            continue
        q.append((x, y))
    return q


def transform_polys(polys, bbox, margin=96):
    """Map source-space polylines to integer Tek coordinates."""
    x0, y0, _, _ = bbox
    scale, ox, oy = fit_transform(bbox, margin)
    out = []
    for poly in polys:
        q = _map_poly(poly, x0, y0, scale, ox, oy)
        if len(q) >= 2:
            out.append(q)
    return out, scale, ox, oy


def transform_polys_styled(polys, styles, bbox, margin=96):
    """Like transform_polys, but keep the per-polyline style list aligned."""
    x0, y0, _, _ = bbox
    scale, ox, oy = fit_transform(bbox, margin)
    out, out_styles = [], []
    for poly, style in zip(polys, styles):
        q = _map_poly(poly, x0, y0, scale, ox, oy)
        if len(q) >= 2:
            out.append(q)
            out_styles.append(style)
    return out, out_styles, scale, ox, oy



def close_ring(poly):
    if len(poly) < 3:
        return None
    if poly[0] != poly[-1]:
        poly = poly + [poly[0]]
    return poly


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
            if t > t1:
                return None
            if t > t0:
                t0 = t
        else:
            if t < t0:
                return None
            if t < t1:
                t1 = t
    if t0 > t1:
        return None
    return t0, t1


def clip_polyline_rect(poly, rect):
    """Clip an open polyline to a rectangle; return a list of runs."""
    runs = []
    cur = []
    for i in range(len(poly) - 1):
        a, b = poly[i], poly[i + 1]
        cut = clip_segment_rect(a, b, rect)
        if cut is None:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            continue
        t0, t1 = cut
        pa = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
        pb = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
        if not cur or abs(cur[-1][0] - pa[0]) > 1e-9 or \
                abs(cur[-1][1] - pa[1]) > 1e-9:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [pa]
        if pb != cur[-1]:
            cur.append(pb)
        if t1 < 1.0:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def _inside_edge(p, edge, rect):
    x0, y0, x1, y1 = rect
    if edge == 0:
        return p[0] >= x0
    if edge == 1:
        return p[0] <= x1
    if edge == 2:
        return p[1] >= y0
    return p[1] <= y1


def _edge_intersect(a, b, edge, rect):
    x0, y0, x1, y1 = rect
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    if edge in (0, 1):
        x = x0 if edge == 0 else x1
        t = (x - ax) / dx if abs(dx) > 1e-12 else 0.0
        return (x, ay + t * dy)
    y = y0 if edge == 2 else y1
    t = (y - ay) / dy if abs(dy) > 1e-12 else 0.0
    return (ax + t * dx, y)


def clip_polygon_rect(poly, rect):
    """Sutherland-Hodgman polygon clip; returns (points, was_clipped)."""
    pts = [(p[0], p[1]) for p in poly]
    clipped = False
    for edge in range(4):
        if not pts:
            break
        out = []
        prev = pts[-1]
        for cur in pts:
            if _inside_edge(cur, edge, rect):
                if not _inside_edge(prev, edge, rect):
                    out.append(_edge_intersect(prev, cur, edge, rect))
                    clipped = True
                out.append(cur)
            elif _inside_edge(prev, edge, rect):
                out.append(_edge_intersect(prev, cur, edge, rect))
                clipped = True
            prev = cur
        pts = out
    return pts, clipped


def crop_polys(polys, rect):
    out = []
    for poly in polys:
        out.extend(clip_polyline_rect(poly, rect))
    return out


def crop_fraction_rect(bbox, crop):
    """Turn (x0,y0,x1,y1) page fractions into a source-space rectangle."""
    x0, y0, x1, y1 = bbox
    fx0, fy0, fx1, fy1 = crop
    return (x0 + fx0 * (x1 - x0), y0 + fy0 * (y1 - y0),
            x0 + fx1 * (x1 - x0), y0 + fy1 * (y1 - y0))


# ---------------------------------------------------------------- simplify


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
    """Iterative Ramer-Douglas-Peucker (no recursion limit on long coastlines)."""
    n = len(points)
    if n <= 2 or tol <= 0:
        return list(points)
    keep = [False] * n
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        ax, ay = points[a]
        bx, by = points[b]
        dx, dy = bx - ax, by - ay
        norm = math.hypot(dx, dy)
        best = tol
        best_i = -1
        for i in range(a + 1, b):
            px, py = points[i]
            if norm == 0:
                d = math.hypot(px - ax, py - ay)
            else:
                d = abs(dy * px - dx * py + bx * ay - by * ax) / norm
            if d > best:
                best, best_i = d, i
        if best_i >= 0:
            keep[best_i] = True
            stack.append((best_i, b))
            stack.append((a, best_i))
    return [p for p, k in zip(points, keep) if k]


def simplify(polys, tol):
    if tol <= 0:
        return [list(p) for p in polys]
    out = []
    for poly in polys:
        q = rdp(poly, tol)
        if len(q) >= 2:
            out.append(q)
    return out


def polyline_len(poly):
    return sum(math.hypot(poly[i + 1][0] - poly[i][0],
                          poly[i + 1][1] - poly[i][1])
               for i in range(len(poly) - 1))


# ---------------------------------------------------------------- encoding


def coord(x, y):
    return bytes((
        0x20 | ((y >> 7) & 0x1F),
        0x60 | (((y & 3) << 2) | (x & 3)),
        0x60 | ((y >> 2) & 0x1F),
        0x20 | ((x >> 7) & 0x1F),
        0x40 | ((x >> 2) & 0x1F),
    ))


def decode_coord(buf, pos):
    b0, b1, b2, b3, b4 = buf[pos:pos + 5]
    y = ((b0 & 0x1F) << 7) | ((b2 & 0x1F) << 2) | ((b1 >> 2) & 0x03)
    x = ((b3 & 0x1F) << 7) | ((b4 & 0x1F) << 2) | (b1 & 0x03)
    return x, y


def text_stream(entry):
    out = bytearray()
    out += b"\x1d" + coord(entry["x"], entry["y"])
    out += b"\x1f"
    out += bytes((0x1B, 0x38 + entry["size"]))
    out += entry["text"].encode("ascii")
    out += b"\x1d" + coord(entry["x"], entry["y"])
    return bytes(out)


def caption_stream(text, size=1):
    x, y = 96, TEK_H - 120
    out = bytearray()
    out += b"\x1d" + coord(x, y)
    out += b"\x1f"
    out += bytes((0x1B, 0x38 + size))
    out += text.encode("ascii", "replace")
    out += b"\x1d" + coord(x, y)
    return bytes(out)


def _style_runs(polys, styles):
    """Group polyline indices by line style, preserving first-appearance order."""
    if styles is None:
        return [(0, list(range(len(polys))))]
    order = []
    groups = {}
    for i, st in enumerate(styles):
        st = max(0, min(LINE_STYLES - 1, int(st)))
        if st not in groups:
            order.append(st)
            groups[st] = []
        groups[st].append(i)
    return [(st, groups[st]) for st in order]


def encode(polys, texts=(), caption=None, styles=None):
    """Encode polylines (and optional alpha text) as a 7-bit Tek stream."""
    out = bytearray(b"\x1b\x0c\x1b\x60")
    runs = _style_runs(polys, styles)
    for n, (style, indices) in enumerate(runs):
        if styles is not None and (n > 0 or style != 0):
            out += bytes((0x1B, 0x60 + style))
        for i in indices:
            poly = polys[i]
            out.append(0x1D)
            for x, y in poly:
                out += coord(x, y)
    for t in texts:
        out += text_stream(t)
    if caption:
        out += caption_stream(caption)
    return bytes(out)


def encoded_size(polys, texts=(), caption=None, styles=None):
    n = HEADER + sum(1 + 5 * len(p) for p in polys)
    if styles is not None:
        n += 2 * len(_style_runs(polys, styles))
    n += sum(15 + len(t["text"]) for t in texts)
    if caption:
        n += 15 + len(caption)
    return n


def compress_to_budget(polys, max_bytes, styles=None):
    """RDP then rank-drop until the stream fits max_bytes.

    Returns (polys, size, tolerance, styles); tolerance -1 means whole
    polylines were dropped.
    """
    total = encoded_size(polys, styles=styles)
    tol = 1.0
    while total > max_bytes and tol <= 64:
        cand = simplify(polys, tol)
        if styles is not None:
            cand_styles = styles[:len(cand)]
        else:
            cand_styles = None
        total = encoded_size(cand, styles=cand_styles)
        if total <= max_bytes:
            return cand, total, tol, cand_styles
        tol *= 1.5
    if total <= max_bytes:
        return polys, total, 0.0, styles
    # Drop the shortest polylines first: keeping a few long paths and
    # discarding every small one loses the whole drawing texture.  The byte
    # accounting is conservative (style-group escapes are not subtracted
    # per drop), so the final encoded size is recomputed below.
    total = encoded_size(polys, styles=styles)
    order = sorted(range(len(polys)), key=lambda i: polyline_len(polys[i]))
    drop = set()
    for i in order:
        if total <= max_bytes:
            break
        total -= 1 + 5 * len(polys[i])
        drop.add(i)
    keep = [i for i in range(len(polys)) if i not in drop]
    out = [polys[i] for i in keep]
    out_styles = [styles[i] for i in keep] if styles is not None else None
    return out, encoded_size(out, styles=out_styles), -1.0, out_styles


def compose(polys, texts=(), max_bytes=MAX_BYTES, caption=None, styles=None):
    """Budget-aware encode: text is priority, graphics are compressed to fit."""
    texts = list(texts)
    text_cost = sum(15 + len(t["text"]) for t in texts)
    target = max(32, max_bytes - text_cost - 256)
    polys, _, tol, styles = compress_to_budget(polys, target, styles)
    data = encode(polys, texts, caption, styles)
    dropped = 0
    while len(data) > max_bytes and texts:
        texts.pop()
        dropped += 1
        data = encode(polys, texts, caption, styles)
    if len(data) > max_bytes:
        polys, _, tol, styles = compress_to_budget(
            polys, max(8, max_bytes - text_cost - 2), styles)
        data = encode(polys, texts, caption, styles)
    return data, {
        "polylines": len(polys),
        "points": sum(len(p) for p in polys),
        "tek_bytes": len(data),
        "simplify_tolerance": tol,
        "texts": len(texts),
        "text_dropped_budget": dropped,
    }


# ---------------------------------------------------------------- text


def _text_width(text, hsize):
    return len(text) * hsize


def text_entries(spans, bbox, scale, ox, oy, min_cell=40.0,
                 overlap=0.35, max_width=TEK_W):
    """Place horizontal text spans in the built-in Tek alpha font.

    Each span is ``{"text", "x", "y", "size", "angle"}`` with x/y the
    baseline origin in source units.  Rotated spans are counted and skipped;
    Tek alpha glyphs cannot rotate.
    """
    x0, y0, _, _ = bbox
    stats = {"spans": 0, "rotated": 0, "small": 0, "overflow": 0,
             "overlap": 0, "empty": 0, "rendered": 0,
             "chars_source": 0, "chars_rendered": 0,
             "chars_nonascii": 0, "chars_truncated": 0}
    out = []
    placed = []
    for s in spans:
        text = s.get("text", "").replace("\n", " ").strip()
        if not text:
            continue
        stats["spans"] += 1
        angle = float(s.get("angle", 0.0) or 0.0) % 180.0
        if min(angle, 180.0 - angle) > 2.0:
            stats["rotated"] += 1
            continue
        stats["chars_source"] += len(text)
        size = float(s.get("size", 0.0) or 0.0)
        if size <= 0:
            stats["empty"] += 1
            continue
        target_cell = size * scale
        if target_cell < min_cell:
            stats["small"] += 1
            continue
        idx = min(range(4), key=lambda i: abs(FONT[i][1] - target_cell))
        hsize, vsize = FONT[idx]

        ascii_chars = []
        dropped = 0
        for ch in text:
            if 32 <= ord(ch) <= 126:
                ascii_chars.append(ch)
            else:
                dropped += 1
        stats["chars_nonascii"] += dropped
        ascii_text = "".join(ascii_chars).strip()
        if not ascii_text:
            stats["empty"] += 1
            continue

        x = int(round(ox + (s["x"] - x0) * scale))
        y = int(round(oy + (s["y"] - y0) * scale))
        if not (0 <= x < TEK_W and 0 <= y < TEK_H):
            stats["overflow"] += 1
            continue
        max_chars = (max_width - 4 - x) // hsize
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
        area = max(1, (tx1 - tx0) * (ty1 - ty0))
        clash = 0.0
        for b in placed:
            ix = max(0, min(tx1, b[2]) - max(tx0, b[0]))
            iy = max(0, min(ty1, b[3]) - max(ty0, b[1]))
            clash = max(clash, ix * iy / area)
        if clash > overlap:
            stats["overlap"] += 1
            continue

        entry = {"text": ascii_text, "size": idx, "x": x, "y": y,
                 "hsize": hsize, "vsize": vsize,
                 "bbox": (tx0, ty0, tx1, ty1),
                 "source_size": size}
        out.append(entry)
        placed.append(entry["bbox"])
        stats["rendered"] += 1
        stats["chars_rendered"] += len(ascii_text)
    out.sort(key=lambda e: (-e["source_size"], e["y"], e["x"]))
    return out, stats


# ---------------------------------------------------------------- validate


def validate_stream(data, max_bytes=MAX_BYTES):
    """Strictly parse a Tek stream; raise ValueError on any violation."""
    if len(data) > max_bytes:
        raise ValueError(f"{len(data)} bytes > limit {max_bytes}")
    if any(b >= 0x80 for b in data):
        raise ValueError("stream contains a byte >= 0x80 (not 7-bit)")
    if len(data) < HEADER or data[:2] != b"\x1b\x0c" or data[2:4] != b"\x1b\x60":
        raise ValueError("missing ESC FF / ESC 60 header")
    pos = HEADER
    runs = []
    texts = []
    max_x = max_y = -1
    min_x = min_y = TEK_W + TEK_H
    n = len(data)
    while pos < n:
        # Line-style changes (ESC 0x60..0x63) may precede any polyline.
        while (pos + 1 < n and data[pos] == 0x1B and
               0x60 <= data[pos + 1] <= 0x63):
            pos += 2
        if pos >= n:
            break
        if data[pos] != 0x1D:
            raise ValueError(f"expected GS at offset {pos}")
        pos += 1
        cur = []
        while True:
            if pos + 5 > n:
                raise ValueError(f"truncated coordinate at {pos}")
            x, y = decode_coord(data, pos)
            if not (0 <= x < TEK_W and 0 <= y < TEK_H):
                raise ValueError(f"coordinate out of range at {pos}: {x},{y}")
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)
            cur.append((x, y))
            pos += 5
            if pos >= n:
                break
            if data[pos] == 0x1F:
                # Text block: US ESC 38+n ASCII GS coord (park).
                if pos + 3 > n or data[pos + 1] != 0x1B:
                    raise ValueError(f"bad text header at {pos}")
                size = data[pos + 2] - 0x38
                if size < 0 or size > 3:
                    raise ValueError(f"bad font select at {pos}")
                pos += 3
                start = pos
                while pos < n and data[pos] != 0x1D:
                    if not (32 <= data[pos] <= 126):
                        raise ValueError(f"non-ASCII text byte at {pos}")
                    pos += 1
                texts.append({"size": size,
                              "text": data[start:pos].decode("ascii"),
                              "x": x, "y": y})
                if pos + 6 > n:
                    raise ValueError("text park coordinate missing")
                if data[pos] != 0x1D:
                    raise ValueError(f"expected park GS at {pos}")
                px, py = decode_coord(data, pos + 1)
                if (px, py) != (x, y):
                    raise ValueError("text park does not return to anchor")
                pos += 6
                # The single coordinate before US is the text anchor, not a
                # stroke; drop it from the current run.
                if cur and cur[-1] == (x, y):
                    cur.pop()
                break
            if data[pos] == 0x1D:
                break
            if data[pos] == 0x1B:
                # A line-style escape starts the next polyline group.
                break
            # Any other byte starts the next 5-byte coordinate of this run.
        if len(cur) >= 2:
            runs.append(cur)
    return {
        "bytes": len(data),
        "polylines": len(runs),
        "points": sum(len(r) for r in runs),
        "texts": texts,
        "bbox": [min_x, min_y, max_x, max_y],
        "seven_bit": True,
    }



# ---------------------------------------------------------------- cli utils


def parse_crop(value):
    try:
        vals = [float(v) for v in value.split(",")]
    except ValueError:
        raise ValueError("crop must be x0,y0,x1,y1 floats")
    if len(vals) != 4:
        raise ValueError("crop must have four values")
    if not all(0.0 <= v <= 1.0 for v in vals):
        raise ValueError("crop values are fractions 0..1")
    if vals[0] >= vals[2] or vals[1] >= vals[3]:
        raise ValueError("crop needs x0<x1 and y0<y1")
    return tuple(vals)


def parse_text_min(value):
    try:
        v = float(value)
    except ValueError:
        raise ValueError("expected a number")
    if v < 0:
        raise ValueError("must be >= 0")
    return v


def write_stats(stats, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2, sort_keys=True)
        fh.write("\n")


def fmt_bytes(n, limit=MAX_BYTES):
    return f"{n} / {limit} ({n * 100.0 / limit:.1f}%)"


def add_common_args(ap):
    ap.add_argument("--max-bytes", type=int, default=MAX_BYTES,
                    help="hard page budget")
    ap.add_argument("--margin", type=int, default=96,
                    help="Tek-unit margin around the fitted page")
    ap.add_argument("--simplify", type=float, default=0.8, metavar="N",
                    help="RDP tolerance in Tek units")
    ap.add_argument("--crop", type=parse_crop, default=None,
                    metavar="X0,Y0,X1,Y1",
                    help="fractions of the source bbox, clipped for real")
    ap.add_argument("--caption", default=None,
                    help="caption placed in the top-left corner")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--stats-json", default=None, metavar="PATH",
                    help="write stats as JSON")
    ap.add_argument("--check", action="store_true",
                    help="strictly parse the written stream")


def finish(data, output, args, stats):
    """Write the stream, optional check, and print a summary."""
    with open(output, "wb") as fh:
        fh.write(data)
    if args.check:
        stats["check"] = validate_stream(data, args.max_bytes)
    if args.stats_json:
        write_stats(stats, args.stats_json)
    if args.stats:
        print(f"source: {stats.get('source')}")
        print(f"input: {stats.get('input_kind')}  "
              f"features/entities: {stats.get('source_items')}")
        print(f"polylines: {stats['polylines']}  "
              f"points: {stats['points']}  texts: {stats['texts']}")
        print(f"simplify tolerance: {stats['simplify_tolerance']}")
        print(f"stream bytes: {fmt_bytes(len(data))}")
        if stats.get("check"):
            c = stats["check"]
            print(f"check: {c['polylines']} polylines, "
                  f"{c['points']} points, bbox {c['bbox']}, "
                  f"{len(c['texts'])} texts")
    return 0
