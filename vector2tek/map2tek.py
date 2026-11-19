#!/usr/bin/env python3
"""Convert map data (OSM XML, Shapefile, GeoJSON) to a Tektronix page.

The converter projects lon/lat to a plane (Web Mercator or equirectangular),
optionally clips to a bounding box, assigns every feature to a named layer,
fits the result to 4096x3120 and writes a 7-bit Tek stream.  Layers can be
filtered with globs and mapped to the four Tek line styles; optional labels
use the built-in Tek alpha font.

Supported inputs:
  * OSM XML (Overpass ``out body`` / planet extract): nodes and ways.  Ways
    are classified into building / road-major / road-minor / road-path /
    rail / water / green / boundary / route; relations are counted but not
    assembled (multipolygon holes are therefore missing).
  * ESRI Shapefile (.shp, read with pyshp): polylines, polygons and points.
    Coordinates must be WGS84 lon/lat; the .prj file is not honoured.
  * GeoJSON (.geojson/.json, RFC 7946 WGS84): all geometry types except
    GeometryCollection nesting is flattened.

SHP/GeoJSON layers default to the file stem, or to one attribute with
``--layer-field`` (e.g. ``featurecla``).  OSM layers are the classes above.

Examples:
  python3 map2tek.py city.osm -o city.tek --styles layer
  python3 map2tek.py ne_50m_coastline.shp ne_50m_lakes.shp -o world.tek \\
      --layer-field featurecla --bbox -180,-56,180,85 --projection mercator
"""

import argparse
import fnmatch
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tekcore as core  # noqa: E402

# OSM way classes, first match wins.
OSM_MAJOR = {"motorway", "trunk", "primary", "secondary", "motorway_link",
             "trunk_link", "primary_link", "secondary_link"}
OSM_MINOR = {"tertiary", "tertiary_link", "residential", "unclassified",
             "service", "living_street", "track", "road"}
OSM_PATH = {"footway", "path", "steps", "cycleway", "pedestrian",
            "bridleway", "corridor", "platform", "crossing"}
OSM_PLACES = {"city", "town", "village", "hamlet", "suburb",
              "neighbourhood", "quarter", "isolated_dwelling"}
OSM_GREEN = {"park", "garden", "nature_reserve", "pitch", "playground",
             "golf_course", "cemetery"}
OSM_LANDUSE = {"grass", "forest", "meadow", "recreation_ground",
               "cemetery", "orchard", "vineyard", "farmland"}
WATER_VALUES = {"water", "wetland", "riverbank", "reservoir", "basin"}


def parse_patterns(value):
    if not value:
        return []
    return [p.strip() for p in value.split(",") if p.strip()]


def layer_selected(name, include, exclude):
    if exclude and any(fnmatch.fnmatch(name, p) for p in exclude):
        return False
    if include and not any(fnmatch.fnmatch(name, p) for p in include):
        return False
    return True


ROAD_LEVELS = {
    "motorway": "road-motorway", "trunk": "road-motorway",
    "primary": "road-primary", "secondary": "road-secondary",
    "tertiary": "road-tertiary",
    "residential": "road-local", "unclassified": "road-local",
    "service": "road-local", "living_street": "road-local",
    "road": "road-local",
}


def osm_class(tags, road_levels=False):
    if "building" in tags or "building:part" in tags:
        return "building"
    if tags.get("natural") in WATER_VALUES or "waterway" in tags \
            or "water" in tags:
        return "water"
    if tags.get("leisure") in OSM_GREEN \
            or tags.get("landuse") in OSM_LANDUSE \
            or tags.get("natural") in ("wood", "scrub", "heath"):
        return "green"
    if "railway" in tags:
        return "rail"
    hw = tags.get("highway")
    if hw:
        if road_levels:
            base = hw[:-5] if hw.endswith("_link") else hw
            if base in OSM_PATH:
                return "road-path"
            return ROAD_LEVELS.get(base, "road-other")
        if hw in OSM_MAJOR:
            return "road-major"
        if hw in OSM_PATH:
            return "road-path"
        return "road-minor"
    if "boundary" in tags:
        return "boundary"
    if "route" in tags:
        return "route"
    return "other"


def osm_label(tags, prefer_en):
    """Return a printable label, preferring Latin OSM names."""
    if not prefer_en:
        return tags.get("name")
    for key in ("name:en", "int_name", "name:zh-Latn-pinyin",
                "official_name:en"):
        value = tags.get(key)
        if value and value.isascii():
            return value
    value = tags.get("name")
    if value and value.isascii():
        return value
    return None


def in_rect(x, y, rect):
    return rect is None or (rect[0] <= x <= rect[2] and
                            rect[1] <= y <= rect[3])


def project(lon, lat, mode):
    if mode == "mercator":
        lat = max(-85.0, min(85.0, lat))
        return (math.radians(lon),
                math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
    return (lon, lat)


def split_dateline(run):
    """Split a lon/lat run where consecutive points jump across +/-180."""
    out, cur = [], []
    for p in run:
        if cur and abs(p[0] - cur[-1][0]) > 180.0:
            if len(cur) >= 2:
                out.append(cur)
            cur = [p]
        else:
            cur.append(p)
    if len(cur) >= 2:
        out.append(cur)
    return out


def bbox_rect(box, mode):
    x0, y0 = project(box[0], box[1], mode)
    x1, y1 = project(box[2], box[3], mode)
    return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def clip_run(proj, rect):
    if rect is None:
        return [proj] if len(proj) >= 2 else []
    return core.clip_polyline_rect(proj, rect)


# ------------------------------------------------------------------ OSM

def read_osm(path, args):
    import xml.etree.ElementTree as ET
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        raise SystemExit(f"error: cannot read OSM XML {path}: {exc}")
    nodes = {}
    node_tags = {}
    bounds = None
    ways = []
    relations = 0
    for el in root:
        if el.tag == "bounds":
            bounds = (float(el.get("minlon")), float(el.get("minlat")),
                      float(el.get("maxlon")), float(el.get("maxlat")))
        elif el.tag == "node":
            nodes[el.get("id")] = (float(el.get("lon")), float(el.get("lat")))
            tags = {t.get("k"): t.get("v") for t in el.findall("tag")}
            if tags:
                node_tags[el.get("id")] = tags
        elif el.tag == "way":
            ways.append(el)
        elif el.tag == "relation":
            relations += 1

    box = args.bbox or bounds
    if box is None:
        xs = [p[0] for p in nodes.values()]
        ys = [p[1] for p in nodes.values()]
        box = (min(xs), min(ys), max(xs), max(ys))
    rect = bbox_rect(box, args.projection)
    args._rect = rect

    runs, styles, labels = [], [], []
    layer_counts = {}
    skipped = 0
    missing = 0
    for way in ways:
        tags = {t.get("k"): t.get("v") for t in way.findall("tag")}
        name = osm_class(tags, args.road_levels)
        if not layer_selected(name, parse_patterns(args.layers),
                              parse_patterns(args.exclude_layers)):
            skipped += 1
            continue
        run = []
        for nd in way.findall("nd"):
            p = nodes.get(nd.get("ref"))
            if p is None:
                missing += 1
                continue
            run.append(p)
        if len(run) < 2:
            continue
        closed = run[0] == run[-1]
        for part in split_dateline(run):
            proj = [project(lon, lat, args.projection) for lon, lat in part]
            for seg in core.clip_polyline_rect(proj, rect):
                if len(seg) >= 2:
                    runs.append(seg)
                    styles.append(name)
                    layer_counts[name] = layer_counts.get(name, 0) + 1
        road_label = name in ("road-major", "road-minor", "road-motorway",
                              "road-primary", "road-secondary",
                              "road-tertiary", "road-local", "water", "green")
        if args.labels and road_label and layer_selected(
                name, parse_patterns(args.label_layers), None):
            text = osm_label(tags, args.label_en)
            if text:
                x, y = project(run[len(run) // 2][0], run[len(run) // 2][1],
                               args.projection)
                labels.append((x, y, text, name))

    if args.labels:
        for nid, tags in node_tags.items():
            place = tags.get("place")
            if place not in OSM_PLACES:
                continue
            if not layer_selected(place, parse_patterns(args.layers),
                                  parse_patterns(args.exclude_layers)):
                continue
            if not layer_selected(place, parse_patterns(args.label_layers),
                                  None):
                continue
            text = osm_label(tags, args.label_en)
            if not text:
                continue
            lon, lat = nodes[nid]
            x, y = project(lon, lat, args.projection)
            if not (rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]):
                continue
            labels.append((x, y, text, place))

    items = {"ways": len(ways), "relations": relations,
             "nodes": len(nodes), "missing_nodes": missing}
    return runs, styles, labels, [], box, layer_counts, skipped, items


# ------------------------------------------------------------- SHP/GeoJSON

def shp_kind(shape_type):
    if shape_type in (1, 11, 21):
        return "point"
    if shape_type in (3, 13, 23):
        return "line"
    if shape_type in (5, 15, 25):
        return "polygon"
    if shape_type in (8, 18, 28):
        return "multipoint"
    return None


def ring_area_centroid(ring):
    """Signed area and centroid of a lon/lat ring (shoelace)."""
    a = 0.0
    cx = cy = 0.0
    n = len(ring)
    closed = list(ring) + [ring[0]] if ring[0] != ring[-1] else list(ring)
    for i in range(len(closed) - 1):
        x0, y0 = closed[i]
        x1, y1 = closed[i + 1]
        cross = x0 * y1 - x1 * y0
        a += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    if abs(a) < 1e-12:
        return None, 0.0
    return (cx / (3.0 * a), cy / (3.0 * a)), abs(a) * 0.5


def shp_parts(shape):
    pts = shape.points
    parts = list(shape.parts) + [len(pts)]
    for i in range(len(parts) - 1):
        run = pts[parts[i]:parts[i + 1]]
        if len(run) >= 2:
            yield run


def prop_value(props, name):
    """Case-insensitive GeoJSON property lookup."""
    if not name or not props:
        return None
    if name in props:
        return props[name]
    low = name.lower()
    for key, value in props.items():
        if key.lower() == low:
            return value
    return None


def record_value(record, fields, name):
    """Case-insensitive attribute lookup on a pyshp record."""
    if not name:
        return None
    low = name.lower()
    for i, f in enumerate(fields):
        if f[0].lower() == low:
            try:
                return record[i]
            except IndexError:
                return None
    return None


def read_shp(path, args):
    try:
        import shapefile
    except ImportError:
        raise SystemExit("error: pyshp is required for Shapefiles")
    try:
        reader = shapefile.Reader(path)
    except Exception as exc:  # noqa: BLE001 - pyshp raises many types
        raise SystemExit(f"error: cannot read Shapefile {path}: {exc}")
    fields = [f for f in reader.fields[1:]]
    stem = os.path.splitext(os.path.basename(path))[0]
    runs, styles, labels, points = [], [], [], []
    counts, skipped = {}, 0
    for sr in reader.iterShapeRecords():
        shape = sr.shape
        kind = shp_kind(shape.shapeType)
        if kind is None:
            skipped += 1
            continue
        layer = record_value(sr.record, fields, args.layer_field) or stem
        layer = str(layer).strip() or stem
        if not layer_selected(layer, parse_patterns(args.layers),
                              parse_patterns(args.exclude_layers)):
            skipped += 1
            continue
        label = record_value(sr.record, fields, args.label_field)
        if args.labels and label and kind == "polygon":
            rings = list(shp_parts(shape))
            best, best_area = None, 0.0
            for r in rings:
                c, area = ring_area_centroid(list(r))
                if c and area > best_area:
                    best, best_area = c, area
            if best:
                x, y = project(best[0], best[1], args.projection)
                if in_rect(x, y, args._rect):
                    labels.append((x, y, str(label), layer))
        if kind in ("point", "multipoint"):
            for lon, lat in shape.points:
                x, y = project(lon, lat, args.projection)
                if not in_rect(x, y, args._rect):
                    continue
                points.append((x, y, layer))
                counts[layer] = counts.get(layer, 0) + 1
                if args.labels and label:
                    labels.append((x, y, str(label), layer))
            continue
        for run in shp_parts(shape):
            closed = kind == "polygon" and run[0] != run[-1]
            for part in split_dateline(list(run)):
                proj = [project(lon, lat, args.projection)
                        for lon, lat in part]
                segs = clip_run(proj, args._rect)
                for seg in segs:
                    if len(seg) < 2:
                        continue
                    if closed and len(segs) == 1 and seg[0] != seg[-1]:
                        seg = seg + [seg[0]]
                    runs.append(seg)
                    styles.append(layer)
                    counts[layer] = counts.get(layer, 0) + 1
    return (runs, styles, labels, points, counts, skipped,
            {"features": len(reader)})


def geojson_kind(geom):
    t = geom.get("type")
    if t in ("Point", "MultiPoint"):
        return "point"
    if t in ("LineString", "MultiLineString"):
        return "line"
    if t in ("Polygon", "MultiPolygon"):
        return "polygon"
    if t == "GeometryCollection":
        return "collection"
    return None


def geojson_parts(geom):
    """Yield (kind, run) for every coordinate ring/line in a geometry."""
    t = geom.get("type")
    c = geom.get("coordinates")
    if t == "LineString":
        yield "line", c
    elif t == "Polygon":
        for ring in c:
            yield "polygon", ring
    elif t == "MultiLineString":
        for line in c:
            yield "line", line
    elif t == "MultiPolygon":
        for poly in c:
            for ring in poly:
                yield "polygon", ring
    elif t == "GeometryCollection":
        for sub in geom.get("geometries", []):
            for item in geojson_parts(sub):
                yield item


def read_geojson(path, args):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"error: cannot read GeoJSON {path}: {exc}")
    if doc.get("type") == "FeatureCollection":
        features = doc.get("features", [])
    elif doc.get("type") == "Feature":
        features = [doc]
    else:
        features = [{"type": "Feature", "geometry": doc, "properties": {}}]
    stem = os.path.splitext(os.path.basename(path))[0]
    runs, styles, labels, points = [], [], [], []
    counts, skipped = {}, 0
    for feat in features:
        geom = feat.get("geometry") or {}
        props = feat.get("properties") or {}
        kind = geojson_kind(geom)
        if kind is None:
            skipped += 1
            continue
        layer = prop_value(props, args.layer_field)
        layer = str(layer).strip() if layer is not None else stem
        layer = layer or stem
        if not layer_selected(layer, parse_patterns(args.layers),
                              parse_patterns(args.exclude_layers)):
            skipped += 1
            continue
        label = prop_value(props, args.label_field)
        if args.labels and label and kind == "polygon":
            rings = [r for k, r in geojson_parts(geom) if k == "polygon"]
            best, best_area = None, 0.0
            for r in rings:
                c, area = ring_area_centroid(r)
                if c and area > best_area:
                    best, best_area = c, area
            if best:
                x, y = project(best[0], best[1], args.projection)
                if in_rect(x, y, args._rect):
                    labels.append((x, y, str(label), layer))
        if kind == "point":
            pts = geom["coordinates"]
            if geom.get("type") == "Point":
                pts = [pts]
            for lon, lat in pts:
                x, y = project(lon, lat, args.projection)
                if not in_rect(x, y, args._rect):
                    continue
                points.append((x, y, layer))
                counts[layer] = counts.get(layer, 0) + 1
                if args.labels and label:
                    labels.append((x, y, str(label), layer))
            continue
        for subkind, run in geojson_parts(geom):
            if len(run) < 2:
                continue
            closed = subkind == "polygon" and run[0] != run[-1]
            for part in split_dateline(run):
                proj = [project(lon, lat, args.projection)
                        for lon, lat in part]
                segs = clip_run(proj, args._rect)
                for seg in segs:
                    if len(seg) < 2:
                        continue
                    if closed and len(segs) == 1 and seg[0] != seg[-1]:
                        seg = seg + [seg[0]]
                    runs.append(seg)
                    styles.append(layer)
                    counts[layer] = counts.get(layer, 0) + 1
    return (runs, styles, labels, points, counts, skipped,
            {"features": len(features)})


# ------------------------------------------------------------------ sample

def detect_format(path, forced):
    if forced and forced != "auto":
        return forced
    low = path.lower()
    if low.endswith((".osm", ".xml")):
        return "osm"
    if low.endswith(".shp"):
        return "shp"
    if low.endswith((".geojson", ".json")):
        return "geojson"
    try:
        with open(path, "rb") as fh:
            head = fh.read(256).lstrip()
    except OSError as exc:
        raise SystemExit(f"error: cannot read {path}: {exc}")
    if head.startswith(b"<?xml") or b"<osm" in head:
        return "osm"
    if head.startswith(b"{"):
        return "geojson"
    return "shp"


def fit_budget(teks, styles, texts, caption, max_bytes, simplify_tol,
               simplify_max=32.0, priorities=None):
    """Simplify, then drop the shortest polylines until the page fits.

    ``core.compress_to_budget`` keeps the longest paths when a page cannot be
    simplified enough; for a map that throws away the whole street network and
    leaves four coastlines.  Maps do the opposite: keep coverage and drop the
    least visible (shortest) features first.
    """
    text_cost = sum(15 + len(t["text"]) for t in texts)
    if caption:
        text_cost += 15 + len(caption)
    target = max(64, max_bytes - text_cost - 2)
    tol = max(0.5, simplify_tol)
    cur = teks
    while core.encoded_size(cur, styles=styles) > target \
            and tol <= simplify_max:
        cur = core.simplify(cur, tol)
        tol *= 1.5
    if core.encoded_size(cur, styles=styles) > target:
        total = core.encoded_size(cur, styles=styles)
        if priorities is None:
            order = sorted(range(len(cur)),
                           key=lambda i: core.polyline_len(cur[i]))
        else:
            order = sorted(range(len(cur)),
                           key=lambda i: (priorities[i],
                                          core.polyline_len(cur[i])))
        drop = set()
        for i in order:
            if total <= target:
                break
            total -= 1 + 5 * len(cur[i])
            drop.add(i)
        keep = [i for i in range(len(cur)) if i not in drop]
        cur = [cur[i] for i in keep]
        if styles is not None:
            styles = [styles[i] for i in keep]
    return cur, styles, tol


def parse_style_map(value, limit=None):
    mapping = {}
    if not value:
        return mapping
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        key, sep, val = item.partition("=")
        if not sep:
            raise argparse.ArgumentTypeError(
                "style map entries look like layer=0 (0..3)")
        try:
            style = int(val)
        except ValueError:
            raise argparse.ArgumentTypeError(f"bad style index in {item!r}")
        if style < 0 or (limit is not None and style >= limit):
            raise argparse.ArgumentTypeError(f"style index out of range in {item!r}")
        mapping[key.strip()] = style
    return mapping


def parse_bbox(value):
    try:
        vals = [float(v) for v in value.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError("bbox must be minlon,minlat,maxlon,maxlat")
    if len(vals) != 4 or vals[0] >= vals[2] or vals[1] >= vals[3]:
        raise argparse.ArgumentTypeError(
            "bbox needs four values with minlon<maxlon, minlat<maxlat")
    return tuple(vals)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", metavar="INPUT",
                    help="OSM XML, .shp or GeoJSON file")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--format", choices=("auto", "osm", "shp", "geojson"),
                    default="auto", help="input format (default: by extension)")
    ap.add_argument("--bbox", type=parse_bbox, default=None,
                    metavar="MINLON,MINLAT,MAXLON,MAXLAT",
                    help="clip to this lon/lat rectangle")
    ap.add_argument("--projection", choices=("mercator", "equirect"),
                    default="mercator", help="lon/lat projection")
    ap.add_argument("--layers", default=None, metavar="GLOB[,GLOB]",
                    help="only these layer names")
    ap.add_argument("--exclude-layers", default=None, metavar="GLOB[,GLOB]",
                    help="drop these layer names")
    ap.add_argument("--layer-field", default=None, metavar="NAME",
                    help="attribute used as the layer name (SHP/GeoJSON)")
    ap.add_argument("--styles", choices=("none", "layer"), default="none",
                    help="map layers to the four Tek line styles")
    ap.add_argument("--style-map", default=None, metavar="LAYER=N,...",
                    help="explicit layer to style index (0..3)")
    ap.add_argument("--road-levels", action="store_true",
                    help="split OSM roads into motorway/primary/secondary/"
                         "tertiary/local layers")
    ap.add_argument("--labels", action="store_true",
                    help="place point/name labels in the Tek alpha font")
    ap.add_argument("--label-layers", default=None, metavar="GLOB[,GLOB]",
                    help="only these layers provide labels")
    ap.add_argument("--label-en", action="store_true",
                    help="prefer name:en/int_name, skip non-ASCII names")
    ap.add_argument("--label-field", default=None, metavar="NAME",
                    help="attribute used for labels (SHP/GeoJSON)")
    ap.add_argument("--label-cell", type=float, default=60.0, metavar="N",
                    help="label height in Tek units")
    ap.add_argument("--min-length", type=float, default=6.0, metavar="N",
                    help="drop polylines shorter than N Tek units")
    ap.add_argument("--point-size", type=int, default=12, metavar="N",
                    help="point feature marker radius in Tek units")
    core.add_common_args(ap)
    ap.add_argument("--simplify-max", type=float, default=32.0, metavar="N",
                    help="stop raising the RDP tolerance at N; drop short "
                         "polylines after that")
    ap.add_argument("--drop-priority", default=None, metavar="LAYER=N,...",
                    help="drop low-priority layers first when over budget")
    args = ap.parse_args()

    runs, styles, labels, points = [], [], [], []
    layer_counts, skipped, items = {}, 0, {}
    source_box = None
    args._rect = (bbox_rect(args.bbox, args.projection)
                  if args.bbox else None)
    for path in args.inputs:
        fmt = detect_format(path, args.format)
        if fmt == "osm":
            if len(args.inputs) > 1:
                raise SystemExit("error: OSM input must be the only input")
            r, s, lab, pts, box, counts, sk, it = read_osm(path, args)
            source_box = box
        elif fmt == "shp":
            r, s, lab, pts, counts, sk, it = read_shp(path, args)
        else:
            r, s, lab, pts, counts, sk, it = read_geojson(path, args)
        if not r and not lab and not pts:
            continue
        runs.extend(r)
        styles.extend(s)
        labels.extend(lab)
        points.extend(pts)
        skipped += sk
        for k, v in counts.items():
            layer_counts[k] = layer_counts.get(k, 0) + v
        items[os.path.basename(path)] = it

    if not runs and not points:
        raise SystemExit("error: no supported geometry in the input")

    proj_bbox = core.poly_bbox(runs)
    if proj_bbox is None and not points:
        raise SystemExit("error: no supported geometry after layer filtering")
    if points:
        pb = core.union_bbox(proj_bbox,
                             (min(p[0] for p in points),
                              min(p[1] for p in points),
                              max(p[0] for p in points),
                              max(p[1] for p in points)))
        proj_bbox = pb
    if args.crop:
        rect = core.crop_fraction_rect(proj_bbox, args.crop)
        runs = core.crop_polys(runs, rect)
        proj_bbox = core.poly_bbox(runs)
        if proj_bbox is None:
            raise SystemExit("error: no geometry after cropping")

    layer_names = []
    for name in styles + [p[2] for p in points]:
        if name not in layer_names:
            layer_names.append(name)
    if not layer_names:
        layer_names = ["features"]
    style_map = parse_style_map(args.style_map, core.LINE_STYLES)
    priority_map = parse_style_map(args.drop_priority)
    style_of = {}
    for i, name in enumerate(layer_names):
        style_of[name] = style_map.get(name, i % core.LINE_STYLES)
    teks, tek_styles, scale, ox, oy = core.transform_polys_styled(
        runs, [style_of[s] for s in styles], proj_bbox, args.margin)
    if priority_map and tek_styles is not None:
        style_prio = {}
        for name, st in style_of.items():
            style_prio[st] = max(style_prio.get(st, 0),
                                 priority_map.get(name, 2))
        priorities = [style_prio.get(st, 2) for st in tek_styles]
    else:
        priorities = None
    for x, y, layer in points:
        tx = int(round(ox + (x - proj_bbox[0]) * scale))
        ty = int(round(oy + (y - proj_bbox[1]) * scale))
        size = args.point_size
        tx = max(size, min(core.TEK_W - 1 - size, tx))
        ty = max(size, min(core.TEK_H - 1 - size, ty))
        teks.append([(tx - size, ty), (tx + size, ty)])
        teks.append([(tx, ty - size), (tx, ty + size)])
        if tek_styles is not None:
            tek_styles.append(style_of[layer])
            tek_styles.append(style_of[layer])
    if args.styles == "none":
        tek_styles = None
    if args.simplify > 0:
        teks = core.simplify(teks, args.simplify)
    if args.min_length > 0:
        keep = [i for i, p in enumerate(teks)
                if core.polyline_len(p) >= args.min_length]
        teks = [teks[i] for i in keep]
        if tek_styles is not None:
            tek_styles = [tek_styles[i] for i in keep]
        if priorities is not None:
            priorities = [priorities[i] for i in keep]
    texts, tstats = [], {}
    if args.labels and labels:
        spans = []
        for x, y, text, layer in labels:
            cell = args.label_cell
            if layer in ("city",):
                cell = 88.0
            elif layer in ("town", "suburb", "road-major", "road-motorway",
                           "road-primary", "water"):
                cell = 64.0
            elif layer in ("quarter", "neighbourhood"):
                cell = 52.0
            # Nudge labels off the point marker / centroid cross.
            dx = 18.0 / scale if scale > 0 else 0.0
            dy = 24.0 / scale if scale > 0 else 0.0
            spans.append({"text": str(text), "x": x + dx, "y": y + dy,
                          "size": cell / scale if scale > 0 else 1.0,
                          "angle": 0.0})
        texts, tstats = core.text_entries(
            spans, proj_bbox, scale, ox, oy, min_cell=40.0, overlap=0.25)

    caption = args.caption
    if caption is None and any(p.lower().endswith((".osm", ".xml"))
                               for p in args.inputs):
        caption = "OSM (C) CONTRIBUTORS"
    teks, tek_styles, ftol = fit_budget(
        teks, tek_styles, texts, caption, args.max_bytes, args.simplify,
        args.simplify_max, priorities)
    data = core.encode(teks, texts, caption=caption, styles=tek_styles)
    while len(data) > args.max_bytes and texts:
        texts.pop()
        data = core.encode(teks, texts, caption=caption, styles=tek_styles)
    if len(data) > args.max_bytes:
        raise SystemExit("error: caption and labels exceed the page budget")
    check = core.validate_stream(data, args.max_bytes)
    cstats = {
        "polylines": len(teks),
        "points": sum(len(p) for p in teks),
        "simplify_tolerance": round(ftol, 3),
    }

    stats = {
        "source": ", ".join(args.inputs),
        "input_kind": "map",
        "sources": items,
        "projection": args.projection,
        "bbox_source": (list(source_box) if source_box else None),
        "bbox_geom": [round(v, 6) for v in proj_bbox],
        "source_items": sum(v.get("features", v.get("ways", 0))
                            for v in items.values()),
        "layers": dict(layer_counts),
        "layers_in": layer_counts,
        "skipped_layer": skipped,
        "polylines_in": len(runs),
        "points_in": sum(len(r) for r in runs),
        "polylines": cstats["polylines"],
        "points": cstats["points"],
        "min_length": args.min_length,
        "texts": len(texts),
        "text_stats": tstats,
        "tek_bytes": len(data),
        "max_bytes": args.max_bytes,
        "simplify_tolerance": cstats["simplify_tolerance"],
        "pre_simplify": args.simplify,
        "check": check,
        "caption": caption,
    }
    if args.crop:
        stats["crop"] = list(args.crop)
    args.check = True
    return core.finish(data, args.output, args, stats)


if __name__ == "__main__":
    sys.exit(main())
