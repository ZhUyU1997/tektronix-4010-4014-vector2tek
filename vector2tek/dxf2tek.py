#!/usr/bin/env python3
"""Convert a DXF CAD drawing to a Tektronix 4010/4014 page.

Reads the modelspace and block references with ezdxf, flattens the supported
entities to polylines, fits them to 4096x3120 and writes a 7-bit Tek stream.

Supported entities: LINE, LWPOLYLINE, POLYLINE (2D/3D), ARC, CIRCLE, ELLIPSE,
SPLINE, HATCH (boundary and pattern lines), SOLID/TRACE/3DFACE, POINT, TEXT,
MTEXT,
INSERT and DIMENSION (both decomposed, including nested blocks and block
scale/rotation).  Layer visibility, ACI/true colour and block transforms are
honoured; the page is monochrome, so colour can optionally select one of the
four Tek line styles.

Text is placed in the built-in Tek alpha font.  Tek alpha text cannot rotate,
so slanted/rotated TEXT is counted and skipped (use ``--text none`` for a
clean mechanical drawing without labels).

Examples:
  python3 dxf2tek.py bracket.dxf -o bracket.tek --stats
  python3 dxf2tek.py board.dxf -o board.tek --layers 'WALLS,DIM*' \\
      --styles layer --bbox 0,0,200,150
"""

import argparse
import fnmatch
import math
import os
import sys

import ezdxf
from ezdxf import bbox as dxf_bbox
from ezdxf import disassemble, path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tekcore as core  # noqa: E402

CURVE_TYPES = {"LINE", "LWPOLYLINE", "POLYLINE", "ARC", "CIRCLE",
               "ELLIPSE", "SPLINE", "HELIX"}
BLOCK_TYPES = {"INSERT", "DIMENSION"}
POLYGON_TYPES = {"SOLID", "TRACE", "3DFACE"}
TEXT_TYPES = {"TEXT", "MTEXT"}


def parse_patterns(value):
    if not value:
        return []
    return [p.strip() for p in value.split(",") if p.strip()]


def match_layer(name, include, exclude):
    if exclude and any(fnmatch.fnmatch(name, p) for p in exclude):
        return False
    if include and not any(fnmatch.fnmatch(name, p) for p in include):
        return False
    return True


def layer_visible(doc, name):
    try:
        layer = doc.layers.get(name)
    except (KeyError, ezdxf.DXFError):
        return True
    return not (layer.is_off() or layer.is_frozen())


def layer_plots(doc, name):
    """False for AutoCAD's non-plotting Defpoints layer and plot=0 layers."""
    if name.lower() == "defpoints":
        return False
    try:
        layer = doc.layers.get(name)
    except (KeyError, ezdxf.DXFError):
        return True
    return bool(layer.dxf.get("plot", 1))


def layer_rgb(doc, name):
    try:
        layer = doc.layers.get(name)
    except (KeyError, ezdxf.DXFError):
        return None
    rgb = getattr(layer, "rgb", None)
    if rgb:
        return tuple(rgb)
    return None


def entity_color(doc, entity):
    """Return (ACI, apparent RGB) honouring BYLAYER/BYBLOCK."""
    name = entity.dxf.get("layer", "0")
    rgb = None
    try:
        rgb = tuple(entity.rgb) if entity.rgb else None
    except (AttributeError, TypeError):
        rgb = None
    aci = entity.dxf.get("color", 256)
    if aci == 0:  # BYBLOCK
        aci = 256
    if aci == 256:
        try:
            aci = doc.layers.get(name).color
        except (KeyError, ezdxf.DXFError):
            aci = 7
        if rgb is None:
            rgb = layer_rgb(doc, name)
    if rgb is None:
        try:
            rgb = ezdxf.colors.aci2rgb(aci)
        except (ValueError, IndexError):
            rgb = (0, 0, 0)
    return int(aci), tuple(rgb)


def flatten_path(entity, flatten):
    """Flatten one curve entity to a list of (x, y) runs in WCS."""
    try:
        p = path.make_path(entity)
    except (TypeError, ValueError, NotImplementedError):
        return []
    runs = []
    try:
        sub_paths = list(p.sub_paths())
    except (AttributeError, ValueError):
        sub_paths = [p]
    if not sub_paths:
        sub_paths = [p]
    for sp in sub_paths:
        try:
            pts = [(v.x, v.y) for v in sp.flattening(flatten)]
        except (ValueError, ZeroDivisionError):
            continue
        if len(pts) >= 2:
            runs.append(pts)
    return runs


def hatch_runs(entity, flatten, patterns=False, pattern_limit=1500):
    runs = []
    try:
        hatches = path.from_hatch(entity)
    except (TypeError, ValueError, NotImplementedError):
        return runs
    for hp in hatches:
        try:
            sub_paths = list(hp.sub_paths()) or [hp]
        except (AttributeError, ValueError):
            sub_paths = [hp]
        for sp in sub_paths:
            pts = [(v.x, v.y) for v in sp.flattening(flatten)]
            if len(pts) >= 2:
                runs.append(pts)
    if patterns:
        # The boundary alone leaves a section looking hollow; render the
        # pattern definition (ANSI31 etc.) as two-point runs.  Cap the count
        # so a huge solid fill cannot flood the page budget.
        try:
            lines = entity.render_pattern_lines()
        except (AttributeError, TypeError, ValueError, NotImplementedError):
            return runs
        for n, (a, b) in enumerate(lines):
            if n >= pattern_limit:
                break
            runs.append([(a.x, a.y), (b.x, b.y)])
    return runs


def point_wcs(entity):
    try:
        loc = entity.dxf.location
        ocs = entity.ocs()
        v = ocs.to_wcs(loc)
        return (v.x, v.y)
    except (AttributeError, ValueError):
        return None


def solid_runs(entity):
    pts = []
    for name in ("vtx0", "vtx1", "vtx2", "vtx3"):
        if entity.dxf.hasattr(name):
            pts.append(tuple(entity.dxf.get(name))[:2])
    if len(pts) < 3:
        return []
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    return [pts]


def text_span(entity):
    """Convert TEXT/MTEXT into alpha-text spans (baseline anchors)."""
    kind = entity.dxftype()
    text = entity.plain_text()
    if not text.strip():
        return []
    if kind == "TEXT":
        height = float(entity.dxf.get("height", 0.0) or 0.0)
        angle = float(entity.dxf.get("rotation", 0.0) or 0.0)
        align, p1, p2 = entity.get_placement()
        name = align.name
        width = len(text) * height * 0.62 * float(
            entity.dxf.get("width", 1.0) or 1.0)
        if name in ("ALIGNED", "FIT") and p2 is not None:
            width = math.hypot(p2.x - p1.x, p2.y - p1.y)
        x, y = p1.x, p1.y
        if name in ("CENTER", "MIDDLE", "MIDDLE_CENTER", "TOP_CENTER",
                    "BOTTOM_CENTER", "ALIGNED", "FIT"):
            x -= width * 0.5
        elif name in ("RIGHT", "MIDDLE_RIGHT", "TOP_RIGHT", "BOTTOM_RIGHT"):
            x -= width
        if name.startswith("MIDDLE") or name == "MIDDLE":
            y -= height * 0.5
        elif name.startswith("TOP"):
            y -= height
        return [{"text": text, "x": x, "y": y, "size": height,
                 "angle": angle}]

    height = float(entity.dxf.get("char_height", 0.0) or 0.0)
    angle = float(entity.get_rotation() or 0.0)
    insert = entity.dxf.insert
    attach = int(entity.dxf.get("attachment_point", 1) or 1)
    raw_lines = text.splitlines() or [text]
    line_h = height * 1.6
    out = []
    for i, line in enumerate(raw_lines):
        if not line.strip():
            continue
        width = len(line) * height * 0.62
        x = insert.x
        y = insert.y
        col = (attach - 1) % 3  # 0 left, 1 center, 2 right
        row = (attach - 1) // 3  # 0 top, 1 middle, 2 bottom
        if col == 1:
            x -= width * 0.5
        elif col == 2:
            x -= width
        if row == 0:
            y -= height * 0.85 + i * line_h
        elif row == 1:
            y += (len(raw_lines) * line_h) * 0.5 - height * 0.85 - i * line_h
        else:
            y += (len(raw_lines) - i) * line_h - height * 0.85
        out.append({"text": line, "x": x, "y": y, "size": height,
                    "angle": angle})
    return out


def collect(doc, args, flatten):
    """Walk the modelspace (and blocks) and return runs, points, spans.

    Returns (runs, styles, points, spans, stats).  Text spans are dropped
    here only if text is disabled; cropping happens later.
    """
    stats = {"entities": 0, "skipped_layer": 0, "skipped_hidden": 0,
             "unsupported": {}, "decomposed": 0, "blocks": 0,
             "layers": {}, "colors": {}, "hatches": 0, "points": 0,
             "texts": 0, "text_rotated": 0}
    include = parse_patterns(args.layers)
    exclude = parse_patterns(args.exclude_layers)
    layer_style = {}
    runs, styles, points, spans = [], [], [], []

    def style_for(layer, aci):
        if args.styles == "none":
            return 0
        if args.styles == "layer":
            if layer not in layer_style:
                layer_style[layer] = len(layer_style) % core.LINE_STYLES
            return layer_style[layer]
        return max(0, aci) % core.LINE_STYLES

    def emit(run, layer, aci):
        runs.append(run)
        styles.append(style_for(layer, aci))

    def process(entity):
        nonlocal stats
        stats["entities"] += 1
        kind = entity.dxftype()
        layer = entity.dxf.get("layer", "0")
        if entity.dxf.get("invisible", 0):
            stats["skipped_hidden"] += 1
            return
        if not match_layer(layer, include, exclude):
            stats["skipped_layer"] += 1
            return
        if not args.include_off and not layer_visible(doc, layer):
            stats["skipped_layer"] += 1
            return
        if not layer_plots(doc, layer):
            stats["skipped_layer"] += 1
            return
        aci, rgb = entity_color(doc, entity)
        stats["layers"][layer] = stats["layers"].get(layer, 0) + 1
        stats["colors"][str(aci)] = stats["colors"].get(str(aci), 0) + 1

        if kind in TEXT_TYPES:
            stats["texts"] += 1
            if args.text != "none":
                for span in text_span(entity):
                    spans.append(span)
            return
        if kind in BLOCK_TYPES:
            try:
                subs = list(disassemble.recursive_decompose([entity]))
            except Exception:  # noqa: BLE001 - a damaged block is non-fatal
                stats["unsupported"][kind] = \
                    stats["unsupported"].get(kind, 0) + 1
                return
            stats["decomposed"] += 1
            stats["blocks"] += len(subs)
            for sub in subs:
                process(sub)
            return
        if kind == "HATCH":
            stats["hatches"] += 1
            for run in hatch_runs(entity, flatten,
                                  patterns=args.hatch_patterns):
                emit(run, layer, aci)
            return
        if kind in POLYGON_TYPES:
            for run in solid_runs(entity):
                emit(run, layer, aci)
            return
        if kind == "POINT":
            stats["points"] += 1
            pt = point_wcs(entity)
            if pt:
                points.append(pt)
            return
        if kind in CURVE_TYPES:
            found = flatten_path(entity, flatten)
            if not found and kind == "POLYLINE":
                # Old-style polyline without a path: use its vertices.
                pts = [(v.dxf.location.x, v.dxf.location.y)
                       for v in entity.vertices]
                if len(pts) >= 2:
                    found = [pts]
            if not found:
                stats["unsupported"][kind] = \
                    stats["unsupported"].get(kind, 0) + 1
                return
            for run in found:
                emit(run, layer, aci)
            return
        stats["unsupported"][kind] = stats["unsupported"].get(kind, 0) + 1

    for entity in doc.modelspace():
        process(entity)
    return runs, styles, points, spans, stats


def auto_flatten(doc, fallback=0.5):
    try:
        ext = dxf_bbox.extents(doc.modelspace(), fast=False)
        if not ext.has_data:
            return fallback
        dx = ext.extmax.x - ext.extmin.x
        dy = ext.extmax.y - ext.extmin.y
        span = max(dx, dy)
        if span <= 0:
            return fallback
        return max(span / 6000.0, 1e-6)
    except Exception:  # noqa: BLE001 - extents are only a hint
        return fallback


def convert(inp, output, args):
    try:
        doc = ezdxf.readfile(inp)
    except (IOError, ezdxf.DXFError) as exc:
        raise SystemExit(f"error: cannot read DXF {inp}: {exc}")
    flatten = args.flatten if args.flatten > 0 else auto_flatten(doc)
    runs, styles, points, spans, stats = collect(doc, args, flatten)
    if not runs and not points:
        raise SystemExit("error: no supported geometry in the DXF")

    source_bbox = core.poly_bbox(runs)
    if args.bbox:
        rect = args.bbox
        runs = core.crop_polys(runs, rect)
        points = [p for p in points
                  if rect[0] <= p[0] <= rect[2] and rect[1] <= p[1] <= rect[3]]
        spans = [s for s in spans
                 if rect[0] <= s["x"] <= rect[2] and
                 rect[1] <= s["y"] <= rect[3]]
        source_bbox = core.poly_bbox(runs)
    if args.crop:
        rect = core.crop_fraction_rect(source_bbox, args.crop)
        if not args.no_clip:
            runs = core.crop_polys(runs, rect)
            points = [p for p in points
                      if rect[0] <= p[0] <= rect[2] and
                      rect[1] <= p[1] <= rect[3]]
        spans = [s for s in spans
                 if rect[0] <= s["x"] <= rect[2] and
                 rect[1] <= s["y"] <= rect[3]]
        source_bbox = core.poly_bbox(runs)
    if source_bbox is None:
        raise SystemExit("error: no geometry after cropping")

    layout_bbox = source_bbox
    boxes = [source_bbox]
    if points:
        boxes.append((min(p[0] for p in points), min(p[1] for p in points),
                      max(p[0] for p in points), max(p[1] for p in points)))
    if args.text != "none" and spans:
        for s in spans:
            w = len(s["text"]) * s["size"] * 0.62
            boxes.append((s["x"], s["y"], s["x"] + w,
                          s["y"] + s["size"]))
    layout_bbox = core.union_bbox(*boxes)

    if args.styles != "none" and styles:
        tek, styles, scale, ox, oy = core.transform_polys_styled(
            runs, styles, layout_bbox, args.margin)
    else:
        tek, scale, ox, oy = core.transform_polys(
            runs, layout_bbox, args.margin)
        styles = None
    if args.simplify > 0:
        tek = core.simplify(tek, args.simplify)

    point_polys = []
    for x, y in points:
        tx = int(round(ox + (x - layout_bbox[0]) * scale))
        ty = int(round(oy + (y - layout_bbox[1]) * scale))
        s = args.point_size
        tx = max(s, min(core.TEK_W - 1 - s, tx))
        ty = max(s, min(core.TEK_H - 1 - s, ty))
        point_polys.append([(tx - s, ty), (tx + s, ty)])
        point_polys.append([(tx, ty - s), (tx, ty + s)])
    if point_polys:
        tek.extend(point_polys)
        if styles is not None:
            styles.extend([0] * len(point_polys))

    texts = []
    tstats = {}
    if args.text != "none":
        texts, tstats = core.text_entries(
            spans, layout_bbox, scale, ox, oy,
            min_cell=args.text_min, overlap=args.text_overlap)
    texts = texts[:args.max_texts]
    if len(texts) < tstats.get("rendered", 0):
        tstats["dropped_max_texts"] = tstats["rendered"] - len(texts)

    data, cstats = core.compose(
        tek, texts, max_bytes=args.max_bytes,
        caption=args.caption, styles=styles)

    tstats["rendered"] = len(texts)
    tstats["chars_rendered"] = sum(len(t["text"]) for t in texts)
    result = {
        "source": inp,
        "output": output,
        "input_kind": "dxf",
        "source_items": stats["entities"],
        "dxf_version": doc.dxfversion,
        "flatten": round(flatten, 6),
        "bbox": [round(v, 3) for v in layout_bbox],
        "scale": round(scale, 6),
        "polylines": cstats["polylines"],
        "points": cstats["points"],
        "point_markers": len(points),
        "texts": len(texts),
        "tek_bytes": len(data),
        "max_bytes": args.max_bytes,
        "simplify_tolerance": cstats["simplify_tolerance"],
        "text_stats": tstats,
        "entity_stats": stats,
        "crop": list(args.crop) if args.crop else None,
        "bbox_filter": list(args.bbox) if args.bbox else None,
        "styles": args.styles,
        "text_mode": args.text,
        "check": core.validate_stream(data, args.max_bytes),
    }
    return data, result


def parse_bbox(value):
    try:
        vals = [float(v) for v in value.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError("bbox must be x0,y0,x1,y1 floats")
    if len(vals) != 4 or vals[0] >= vals[2] or vals[1] >= vals[3]:
        raise argparse.ArgumentTypeError(
            "bbox needs four values with x0<x1, y0<y1")
    return tuple(vals)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="DXF file")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--layers", default=None, metavar="GLOB[,GLOB]",
                    help="only these layer names")
    ap.add_argument("--exclude-layers", default=None, metavar="GLOB[,GLOB]",
                    help="drop these layer names")
    ap.add_argument("--include-off", action="store_true",
                    help="also draw entities on off/frozen layers")
    ap.add_argument("--styles", choices=("none", "layer", "color"),
                    default="none",
                    help="map layers or ACI colours to Tek line styles")
    ap.add_argument("--text", choices=("alpha", "none"), default="alpha",
                    help="place TEXT/MTEXT in the Tek alpha font")
    ap.add_argument("--text-min", type=float, default=40.0, metavar="N",
                    help="minimum Tek cell height for alpha text")
    ap.add_argument("--text-overlap", type=float, default=0.35)
    ap.add_argument("--max-texts", type=int, default=250)
    ap.add_argument("--bbox", type=parse_bbox, default=None,
                    metavar="X0,Y0,X1,Y1",
                    help="clip to this model-space rectangle")
    ap.add_argument("--flatten", type=float, default=0.0, metavar="N",
                    help="curve flattening distance (0 = auto)")
    ap.add_argument("--point-size", type=int, default=16, metavar="N",
                    help="POINT marker radius in Tek units")
    ap.add_argument("--hatch-patterns", dest="hatch_patterns",
                    action="store_true", default=True,
                    help="render HATCH pattern lines as well as boundaries")
    ap.add_argument("--no-hatch-patterns", dest="hatch_patterns",
                    action="store_false",
                    help="draw HATCH boundaries only")
    core.add_common_args(ap)
    ap.add_argument("--no-clip", action="store_true",
                    help="do not clip geometry to --crop")
    args = ap.parse_args()

    if args.crop:
        try:
            args.crop = core.parse_crop(",".join(map(str, args.crop)))
        except ValueError as exc:
            ap.error(str(exc))
    data, stats = convert(args.input, args.output, args)
    with open(args.output, "wb") as fh:
        fh.write(data)
    if args.stats_json:
        core.write_stats(stats, args.stats_json)
    if args.stats:
        print(f"source: {args.input} ({stats['dxf_version']})")
        print(f"entities: {stats['source_items']}  "
              f"decomposed blocks: {stats['entity_stats']['decomposed']}")
        print(f"layers: {len(stats['entity_stats']['layers'])}  "
              f"colors: {len(stats['entity_stats']['colors'])}")
        print(f"flat: {stats['entity_stats']['unsupported']}")
        print(f"bbox: {stats['bbox']}  scale={stats['scale']}")
        print(f"text: {stats['text_stats']}")
        print(f"polylines: {stats['polylines']}  points: {stats['points']}"
              f"  texts: {stats['texts']}")
        print(f"stream bytes: {core.fmt_bytes(len(data), args.max_bytes)}")
        print(f"check: {stats['check']['polylines']} polylines, "
              f"bbox {stats['check']['bbox']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
