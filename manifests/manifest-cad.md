# CAD / DXF — manifest

`.tek` files live in `../tek/`; this manifest records source, license, author,
command, bytes, quality and the source decisions for the CAD set.

## Summary

| set | pages | `.tek` bytes | quality |
|---|---:|---:|---|
| cad | **11** | **58,882** | **11 good / 0 marginal** |

- 10 pages were authored for this pass; `cad-pillow-block` is the original
  reference page.
- All 11 pages are native DXF geometry, 7-bit, ≤ 24,576 B, and rendered at
  480×640 / 640×480 for review. No raster, scan or potrace input.
- The 10 new pages place **every** source text span (0 rotated, 0 non-ASCII,
  0 truncated). The reference page drops 2 rotated dimension texts by design.
- Contact sheet: not archived (generated in the original build).

No page has an external URL: every shipped drawing is original. External
candidates and their license status are logged below.

## Pages

| id | DXF / source | license · author | `.tek` | budget | Q |
|---|---|---|---:|---:|---|
| `cad-bracket` | [cad-bracket.dxf](../sources/cad/cad-bracket.dxf) — A3, front/top/section B–B | CC0 · original (generated) | [4326 B](../tek/cad-bracket.tek) | 17.6% | G |
| `cad-clamp` | [cad-clamp.dxf](../sources/cad/cad-clamp.dxf) — A3, C-frame section/top/detail | CC0 · original (generated) | [4653 B](../tek/cad-clamp.tek) | 18.9% | G |
| `cad-coupling` | [cad-coupling.dxf](../sources/cad/cad-coupling.dxf) — A3, assembly section/face/BOM | CC0 · original (generated) | [6381 B](../tek/cad-coupling.tek) | 26.0% | G |
| `cad-flange` | [cad-flange.dxf](../sources/cad/cad-flange.dxf) — A3, face/section A–A | CC0 · original (generated) | [6594 B](../tek/cad-flange.tek) | 26.8% | G |
| `cad-gear` | [cad-gear.dxf](../sources/cad/cad-gear.dxf) — A3, face/section + gear data | CC0 · original (generated) | [4933 B](../tek/cad-gear.tek) | 20.1% | G |
| `cad-housing` | [cad-housing.dxf](../sources/cad/cad-housing.dxf) — A3, front/section A–A | CC0 · original (generated) | [5195 B](../tek/cad-housing.tek) | 21.1% | G |
| `cad-pillow-block` | [cad-pillow-block.dxf](../sources/cad/cad-pillow-block.dxf) — copy of the cap sample: 72 entities, 11 blocks, ANSI31 | CC0 · original (`make_dxf_sample.py`) | [7047 B](../tek/cad-pillow-block.tek) | 28.7% | G |
| `cad-pulley` | [cad-pulley.dxf](../sources/cad/cad-pulley.dxf) — A3, section/face/groove detail | CC0 · original (generated) | [5941 B](../tek/cad-pulley.tek) | 24.2% | G |
| `cad-rod` | [cad-rod.dxf](../sources/cad/cad-rod.dxf) — A3, front + 4:1 I-section | CC0 · original (generated) | [4094 B](../tek/cad-rod.tek) | 16.7% | G |
| `cad-shaft` | [cad-shaft.dxf](../sources/cad/cad-shaft.dxf) — A3, front + 2:1 keyway section | CC0 · original (generated) | [3219 B](../tek/cad-shaft.tek) | 13.1% | G |
| `cad-ujoint` | [cad-ujoint.dxf](../sources/cad/cad-ujoint.dxf) — A3, assembly section/end/BOM | CC0 · original (generated) | [6499 B](../tek/cad-ujoint.tek) | 26.4% | G |

## Drawing content

All new sheets use the same A3 frame, revision block, title block, layer set
(`OUTLINE`, `HIDDEN`, `CENTER`, `DIM`, `HATCH`, `TEXT`, `FRAME`), ANSI31
section hatching and ASCII uppercase notes. Dimensions are drawn as line/text
entities so the text stays horizontal; Tek alpha glyphs cannot rotate.

| id | views | hatch sections | texts | polylines · points |
|---|---|---:|---:|---:|
| `cad-bracket` | front, top, section B–B | 3 | 37/37 | 204 · 639 |
| `cad-clamp` | section A–A, top, detail A 2:1 | 5 | 33/33 | 245 · 716 |
| `cad-coupling` | assembly section, face, BOM | 10 | 52/52 | 239 · 991 |
| `cad-flange` | face, section A–A | 8 | 31/31 | 207 · 1116 |
| `cad-gear` | face, section A–A, data table | 6 | 44/44 | 167 · 746 |
| `cad-housing` | front, section A–A | 7 | 33/33 | 219 · 829 |
| `cad-pillow-block` | three views + notes | 1 | 16/18 | 133 · 1294 |
| `cad-pulley` | section A–A, face, detail C 2:1 | 7 | 34/34 | 236 · 965 |
| `cad-rod` | front, section A–A 4:1 | 3 | 34/34 | 183 · 610 |
| `cad-shaft` | front, section A–A 2:1 | 1 | 37/37 | 127 · 435 |
| `cad-ujoint` | assembly section, end view, BOM | 14 | 49/49 | 305 · 1015 |

`cad-pillow-block` keeps its original 16/18 text count: the two rotated
dimension texts (rendered diameter/vertical dimensions) are deliberately
dropped because Tek alpha glyphs cannot rotate. The reference
page remains G from the earlier quality pass.

## Commands

Prerequisites: `python3 -m pip install -r ../vector2tek/requirements.txt`
(ezdxf 1.4.5 is what this pass used).

```bash
# 1. author the 10 new DXF sheets (../sources/cad/cad-*.dxf)
python3 ../vector2tek/make_cad_pages.py

# 2. convert, validate, preview, and rebuild the contact sheet
python3 ../vector2tek/convert_cad_set.py

# 3. the reference page is not regenerated; its source command is
python3 ../vector2tek/dxf2tek.py \
  ../sources/cad/cad-pillow-block.dxf -o "work/repro/cad-pillow-block.tek" \
  --styles layer --stats
# (this reproduces the shipped 7,047 B stream byte-for-byte)
```

Per-page equivalent of step 2 (the driver runs exactly this):

```bash
python3 ../vector2tek/dxf2tek.py \
  ../sources/cad/cad-<part>.dxf -o ../tek/cad-<part>.tek \
  --styles color --text-min 40 --check \
  --stats-json ../sources/cad/cad-<part>.json \
  
```

`--styles color` maps ACI 4/2/7 to solid/dashed/dash-dot, so outlines,
hidden lines and centre lines stay distinguishable in the monochrome stream.
`--text-min 40` accepts the 4.6 mm revision/title text (the 40-unit cell snaps
to the 48-row Tek alpha glyph). The driver validates every stream with
`tekcore.validate_stream` (bytes, 7-bit, syntax) and records the result in
`../sources/cad/*.json` plus `../sources/cad/set.json`.

Files:

- `../sources/cad/cad-*.dxf` — DXF sources (52 KB reference + 60–68 KB each new)
- previews and the contact sheet were generated in the original build and are not archived
- `../tek/cad-*.tek` — shipped streams

## Source and license log

### Original sheets — CC0 (used)

`make_cad_pages.py` (not archived; see `../sources.tsv`) authored all 10 new sheets directly with
ezdxf from dimensions and construction geometry written in this repository.
No third-party drawing data is copied or traced. License: **CC0 / public
domain**, author: this repository (generated). `make_dxf_sample.py` is the
same arrangement for the reference page.

### LibreCAD 2.1.3 symbol library — GPL-2 (surveyed, not shipped)

- Path: `/usr/share/librecad/library` (`librecad-data` 2.1.3-3 Debian
  package); **1,334 DXF** files. Upstream: <https://www.librecad.org/>.
- License: **GPL-2** per `/usr/share/doc/librecad-data/copyright`
  (RibbonSoft/QCAD 2001–2003; LibreCAD contributors 2010–2016). If any page is
  ever based on this library, that GPL-2 notice and the source must be carried
  with the page.
- Why none is used:
  - the library contains individual symbols and templates, not complete
    mechanical sheets: `block/*.dxf` are single polylines, `elektro/`,
    `plan/` and `power_station/` are electrical/civil symbols, and
    `kinetics/`/`algoritm/` are mechanism/construction fragments with no
    title block or dimensions;
  - `sheets/*_draw.dxf` are Russian-language title-block templates
    (`\U+041a...` text) with no part views; their non-ASCII text would be
    dropped by the Tek alpha font;
  - `misc/screw.dxf`, `misc/t-part.dxf` and `misc/a3.dxf` fail to parse
    (`DXFStructureError: found ENDSEC tag without previous SECTION tag`);
  - no candidate met the "mechanical part/assembly, multi-view, dimensions,
    hatch, title block" bar, so none was shipped. No GPL-2 content is in the
    set; the license is recorded here for a future pass.

### Wikimedia Commons — no DXF (not shipped)

Commons image search (`https://commons.wikimedia.org/w/api.php`) for
`filetype:dxf` across mechanical/gear/flange/bearing/part/CAD queries returned
**0 files**; Commons does not host DXF. No page was taken from Commons in this
pass.

### FreeCAD / open-hardware examples — not used

FreeCAD is not installed on this machine and no local FreeCAD example DXF was
found. No open-hardware DXF with a clear license and a complete title-blocked
drawing was fetched; the generator path was used instead. Any future public
DXF must record its URL, author and license in this table.

## Skip log

| candidate | result | reason |
|---|---|---|
| LibreCAD `misc/screw.dxf` | skip | structurally corrupt DXF |
| LibreCAD `misc/t-part.dxf` | skip | structurally corrupt DXF |
| LibreCAD `misc/a3.dxf` | skip | structurally corrupt DXF |
| LibreCAD `sheets/A*_draw.dxf` | skip | title-block template only; Cyrillic text not renderable |
| LibreCAD `block/*.dxf` | skip | single polyline, no part or annotations |
| LibreCAD `kinetics/`, `algoritm/` | skip | geometry fragments, no title block/dimensions |
| Wikimedia Commons DXF search | skip | 0 DXF files on Commons |
| bitmap / scan / potrace | not considered | native DXF only, per task |

## Verification

- `tekcore.validate_stream` passes for all 11 `.tek`: 7-bit, header/syntax,
  ≤ 24,576 B. Largest page is 6,594 B (26.8%).
- New-page text: 37/37, 33/33, 52/52, 31/31, 44/44, 33/33, 34/34, 34/34,
  37/37, 49/49; `chars_nonascii = 0`, `rotated = 0`, `chars_truncated = 0`.
- Byte counts are stable across repeated runs. SHA-256 is deliberately not
  recorded: ezdxf emits HATCH pattern lines in a process-dependent order, so
  two conversions of the same sheet are visually identical but not
  byte-identical. `tekcore.validate_stream` is the acceptance check; it passed
  on every run. (The pillow-block stream is byte-for-byte reproducible with
  `--styles layer` because its pattern is a single ANSI31 hatch.)
- Review at 640×480 page view: all pages readable; no page was kept with
  missing labels or a simplified view that lost its dimensions.
