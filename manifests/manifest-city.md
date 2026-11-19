# Tek material set — city maps (11 pages)

Generated: 2026-11-19T06:05Z  
Source: [OpenStreetMap](https://www.openstreetmap.org/) via Overpass API, **ODbL 1.0**  
Converter: `../vector2tek/map2tek.py`, `--styles layer --layers road-major,water,green,rail`  
Budget: 24,576 B/page, 7-bit Tek stream, exactly one `ESC FF` page  
Pages: 11; total `.tek`: 261451 B; max page: 24463 B (99.5%, `c-hangzhou`); min page: 22950 B (93.4%, `c-nanjing`)  
Labels: caption only (`CITY / OSM CONTRIBUTORS`); no street or place labels.

`.tek` files live in `../tek/` (`c-*.tek`), 480×640 device previews in
(generated in the original working tree; not archived) (not archived), contact sheet
`contact.png` (not archived) (960×1034, Beijing v3 reference + 10 new pages).
Beijing `c-beijing.tek` is the v3 reference from the earlier pass and was **not** regenerated here.

## Pages

| city | bbox (minlon,minlat,maxlon,maxlat) | license | `.tek` | budget | Q | skipped |
|---|---|---|---|---|---:|---:|---|---|
| Beijing `c-beijing` | not recorded (v3 pass) | ODbL 1.0 / OSM contributors | [23316 B](../tek/c-beijing.tek) | 94.9% | G | — |
| Shanghai `c-shanghai` | 121.406,31.184,121.544,31.296 | ODbL 1.0 / OSM contributors | [23518 B](../tek/c-shanghai.tek) | 95.7% | G | — |
| Guangzhou `c-guangzhou` | 113.20,23.08,113.34,23.19 | ODbL 1.0 / OSM contributors | [24058 B](../tek/c-guangzhou.tek) | 97.9% | G | — |
| Shenzhen `c-shenzhen` | 113.96,22.49,114.12,22.60 | ODbL 1.0 / OSM contributors | [24083 B](../tek/c-shenzhen.tek) | 98.0% | G | — |
| Chengdu `c-chengdu` | 103.99,30.52,104.14,30.63 | ODbL 1.0 / OSM contributors | [23704 B](../tek/c-chengdu.tek) | 96.5% | G | — |
| Chongqing `c-chongqing` | 106.48,29.51,106.62,29.62 | ODbL 1.0 / OSM contributors | [24458 B](../tek/c-chongqing.tek) | 99.5% | G | — |
| Wuhan `c-wuhan` | 114.23,30.53,114.38,30.65 | ODbL 1.0 / OSM contributors | [24006 B](../tek/c-wuhan.tek) | 97.7% | G | — |
| Hangzhou `c-hangzhou` | 120.08,30.21,120.23,30.33 | ODbL 1.0 / OSM contributors | [24463 B](../tek/c-hangzhou.tek) | 99.5% | G | — |
| Nanjing `c-nanjing` | 118.72,32.00,118.87,32.12 | ODbL 1.0 / OSM contributors | [22950 B](../tek/c-nanjing.tek) | 93.4% | G | — |
| Tianjin `c-tianjin` | 117.12,39.02,117.28,39.14 | ODbL 1.0 / OSM contributors | [23880 B](../tek/c-tianjin.tek) | 97.2% | G | — |
| Xi'an `c-xian` | 108.86,34.28,109.02,34.40 | ODbL 1.0 / OSM contributors | [23015 B](../tek/c-xian.tek) | 93.6% | G | — |

No city was skipped: all 10 requested extracts were fetched and converted.
`Q` is G (good): one page, 7-bit, ≤ 24,576 B, and legible in the 480×640
device preview. There are no marginal pages in this set.

## Build parameters

The fetch bbox is a margin larger than the page bbox, so the page extent can
be tuned without another request. `min-length` is in Tek units and was raised
per city density to keep the page inside budget without forcing the converter
to over-simplify (`simplify 2.5`; final `simplify_tolerance` equals 2.5 on
every new page, i.e. no further RDP was applied by the budget fitter).

| city | fetch bbox | page bbox | min-length | polylines | points | preview |
|---|---|---|---:|---:|---:|---|
| Beijing | — (v3 pass) | not recorded | — | 1607 | 4332 | 480×640 (not archived) |
| Shanghai | 121.35,31.15,121.60,31.35 | 121.406,31.184,121.544,31.296 | 180 | 416 | 4610 | 480×640 (not archived) |
| Guangzhou | 113.20,23.05,113.40,23.25 | 113.20,23.08,113.34,23.19 | 160 | 565 | 4688 | 480×640 (not archived) |
| Shenzhen | 113.96,22.47,114.16,22.62 | 113.96,22.49,114.12,22.60 | 180 | 534 | 4699 | 480×640 (not archived) |
| Chengdu | 103.97,30.50,104.17,30.65 | 103.99,30.52,104.14,30.63 | 200 | 563 | 4618 | 480×640 (not archived) |
| Chongqing | 106.45,29.49,106.65,29.64 | 106.48,29.51,106.62,29.62 | 220 | 495 | 4782 | 480×640 (not archived) |
| Wuhan | 114.21,30.52,114.41,30.67 | 114.23,30.53,114.38,30.65 | 140 | 787 | 4634 | 480×640 (not archived) |
| Hangzhou | 120.06,30.20,120.26,30.35 | 120.08,30.21,120.23,30.33 | 160 | 681 | 4746 | 480×640 (not archived) |
| Nanjing | 118.70,31.99,118.90,32.14 | 118.72,32.00,118.87,32.12 | 200 | 504 | 4479 | 480×640 (not archived) |
| Tianjin | 117.10,39.01,117.30,39.16 | 117.12,39.02,117.28,39.14 | 180 | 579 | 4650 | 480×640 (not archived) |
| Xi'an | 108.84,34.27,109.04,34.42 | 108.86,34.28,109.02,34.40 | 80 | 997 | 4394 | 480×640 (not archived) |

Per-page statistics are in (generated in the original working tree; not archived)
(`--stats-json`), including the `validate_stream` result.

## What each page shows

- **Shanghai** — Huangpu river bend, inner/outer ring roads and the radial
  arterials; Pudong and Puxi road grid.
- **Guangzhou** — Pearl River channel through the old town and Tianhe, with
  the ring/expressway net.
- **Shenzhen** — coastline and reservoirs, the north–south corridors
  (Bao'an–Futian–Luohu) and the east–west expressways.
- **Chengdu** — concentric ring roads around Tianfu Square, radial spokes.
- **Chongqing** — Yangtze/Jialing confluence and the peninsula; steep-terrain
  road skeleton, dense rail layer.
- **Wuhan** — Yangtze and Han rivers, the three towns, East Lake and the
  bridge crossings.
- **Hangzhou** — Qiantang river, the canal grid and the West Lake area;
  West Lake itself is a multipolygon relation and is not assembled by the
  converter, so its shore outline is not guaranteed.
- **Nanjing** — Yangtze crossing, the walled old town grid and the ring roads.
- **Tianjin** — Haihe river through the centre, the grid and the outer ring.
- **Xi'an** — the walled rectangular grid, the ring road and the rail yard
  (dense dashed rail layer).

## Method / deviations

- **Fetch.** One Overpass query per city:
  `highway ~ ^(motorway|trunk|primary|secondary|tertiary)$`, `waterway`,
  `natural=water`, `leisure=park`, `railway`, `out body; >; out skel qt;`.
  Requests use a descriptive User-Agent; the main endpoint is
  `overpass-api.de` (direct IPv4), with the kumi HTTP endpoint as fallback.
  Transient 502/301 responses were retried; each accepted extract parses as
  `<osm>` with a nonzero way count. Cached `.osm` files are 4.6–15.8 MB.
- **Road levels.** `--road-levels` renames the road classes to
  `road-motorway/road-primary/...`, so combining it with
  `--layers road-major` selects **no roads** (verified: the first Shanghai
  pass had only water/green/rail). The v3 layout keeps a single `road-major`
  layer, so the delivered command uses `road-major,water,green,rail` without
  the level split. Tertiary roads are fetched but not drawn; "main roads
  only" is the v3 intent.
- **Budget.** `min-length` is 80–220 Tek units and pre-simplification is 2.5.
  All 10 new pages fit at 93.4–99.5% of the 24,576 B cap with
  `simplify_tolerance == 2.5`, so the budget fitter did not have to raise
  the RDP tolerance or drop the shortest paths after the min-length filter.
  This follows the brief's "over budget -> shrink bbox or raise min-length";
  the bbox was also cropped from the fetch extent to the city centre.
  Beijing v3 (23,316 B, 94.9%) predates this pass and has no stats JSON.
- **Relations.** Multipolygon relations are counted but not assembled, so
  water/park features mapped only as relations are absent; way-based rivers,
  canals, reservoirs and parks render as outlines.
- **Preview.** `map2tek --preview` writes the 480×640 device view. Pages
  were reviewed on the contact sheet and at 480×640; all are legible, with
  the expected river/ring/grid structure.

## Reproduce

```bash
# all 10 (cached .osm reused; fetch retries 502/429/connection failures)
../vector2tek/city/fetch_convert.sh

# one city
../vector2tek/city/fetch_convert.sh shanghai
```

The script writes (generated in the original working tree; not archived),
(generated in the original working tree; not archived), (generated in the original working tree; not archived) and
`../tek/c-<city>.tek`. Contact sheet:
`python3 ../vector2tek/city/contact.py`.

## Contact / attribution

Map data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright),
available under the [Open Database License (ODbL) 1.0](https://opendatacommons.org/licenses/odbl/1-0/).
The on-page caption `CITY / OSM CONTRIBUTORS` is a short attribution; this
manifest and the license notice must accompany any redistribution.

Visual index: (generated in the original working tree; not archived) (not archived)
