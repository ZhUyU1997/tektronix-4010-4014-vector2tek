# Tektronix 4010/4014 Vector-to-Tek Converter

A converter for the **Tektronix 4010 / 4014 storage-tube terminal**: vector **SVG / PDF / DXF / OpenStreetMap** sources are converted to 7-bit `.tek` streams.

**Keywords:** Tektronix 4010, Tektronix 4014, Tek 4010, Tek 4014, storage tube, vector display, vector art, line art, SVG to Tek, PDF to Tek, DXF to Tek, OpenStreetMap to Tek, 7-bit, GS, 4096×3120, retro computing, CAD, OSM.

---

## Contents

- [What is this?](#what-is-this)
- [Quick start](#quick-start)
- [Repository layout](#repository-layout)
- [Reproduce and verify](#reproduce-and-verify)
- [The `.tek` format](#the-tek-format)
- [Sources and licenses](#sources-and-licenses)
- [Special pages](#special-pages)
- [Verification](#verification)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## What is this?

The **Tektronix 4010 / 4014** are storage-tube terminals: a monochrome green CRT that stores a vector image as charge on a dielectric mesh. Their command language is a 7-bit byte stream of moves, lines, alpha text and pages, addressable on a **4096 × 3120** grid.

This repository contains the **vector2tek converter** and the 227 pages it produced from original vector documents:

| set | pages | `.tek` bytes | source kind | converter |
|---|---:|---:|---|---|
| base | 50 | 679,293 | SVG | `convert_vector.py` (42) / `convert_vector_v1.py` (8) |
| q | 29 | 382,995 | SVG | `convert_vector.py` |
| v | 126 | 1,985,505 | SVG | `convert_vector.py` |
| cad | 11 | 58,882 | DXF | `dxf2tek.py` via `dxf2tek_seeded.py` |
| city | 11 | 257,417 | OSM XML | `map2tek.py` |
| **total** | **227** | **3,364,092** | 205 SVG + 11 DXF + 11 OSM | |

The pages span ships, aircraft, spacecraft, machinery, architecture, anatomy, animals, plants, instruments, chemistry, geology, CAD, electronics, mathematics, patents and city maps. The common thread is **line work**: outlines, sections, cutaways and diagrams that survive the 4010/4014's single-stroke display.

## Quick start

```bash
git clone <this-repo> ~/tek-resource
cd ~/tek-resource

python3 -m pip install -r vector2tek/requirements.txt

./reproduce.sh --check
# pages=227 identical=227 different=0 failed=0 missing=0
```

Requirements: Python 3.10, **PyMuPDF 1.28.2**, **ezdxf 1.4.5**, `lxml` 6.1.1. PyMuPDF version matters for byte-identical output; see [Dependencies](#dependencies).

## Repository layout

```
~/tek-resource/
  README.md
  sources.tsv          227 data rows; one complete command per page
  reproduce.sh         227-page driver; --check compares with cmp -s
  checksums.sha256     227 SHA-256 entries for tek/*.tek
  sources/             227 original sources, one directory per set:
    base/ q/ v/ cad/ city/   (50 / 29 / 126 / 11 / 11)
  tek/                 227 .tek pages, flat output directory
  vector2tek/          converters + the v-schmidt per-page source fix
  manifests/           original per-set manifests, unchanged
```

The `sources/` tree is 162,899,221 bytes. The largest files are the eleven cached Overpass city extracts (4.6–17.4 MB each). All sources are archived; no network access is needed to reproduce.

## Reproduce and verify

```bash
cd ~/tek-resource

./reproduce.sh --list | wc -l        # 227
./reproduce.sh --check               # 227/227, tek/ untouched
./reproduce.sh --only v-schmidt --check
./reproduce.sh                       # rebuild tek/<id>.tek in place
sha256sum -c checksums.sha256        # 227 x OK
```

`--check` runs each command with its output redirected to `work/repro/<id>.tek` and compares it with `tek/<id>.tek` using `cmp -s`; it never writes to `tek/`. `--list` prints the commands; `--only ID` restricts either mode to one page. The script fails on a missing source, a failed command, a missing output, or a byte difference.

### Per-page commands

`sources.tsv` is tab-separated with a header plus 227 data rows:

```
id  output  source  license  author  command
```

`output` and `source` are paths relative to the repository root (`tek/<id>.tek`, `sources/<set>/<file>`). `command` is a complete shell command with paths spelled `"$HOME/tek-resource/..."`; it can be copied into a shell as-is. Rows are grouped base (50), q (29), v (126), cad (11), city (11). Empty author fields are preserved; read the file with a tab-aware parser.

## The `.tek` format

A `.tek` file is a raw 7-bit Tektronix 4010/4014 stream:

- Header: `ESC FF` + `ESC 60`.
- Vector: `GS` (0x1D) + four coordinate bytes = 5 bytes per endpoint.
- Text: `US` + size/character bytes + `GS` park anchor.
- Line styles: `ESC 0x60..0x63`.
- One `ESC FF` per page.
- Coordinates fit the 4096 × 3120 addressable grid; the display draws a 1.25 px line.

The stream can be replayed on real hardware, an emulator, or the included `tek-render` host tooling from the originating project.

## Sources and licenses

Per-page license and author are recorded in `sources.tsv` and in `manifests/`.

| license family | pages |
|---|---:|
| Public domain | 60 |
| CC0 (CC0 / CC0 1.0) | 38 |
| CC BY (2.5 / 3.0 / 4.0) | 18 |
| CC BY-SA (2.0 / 2.5 / 3.0 / 4.0) | 100 |
| ODbL 1.0 (OpenStreetMap contributors) | 11 |

The city maps are derived from OpenStreetMap data, © OpenStreetMap contributors, **ODbL 1.0**. SVG and DXF pages retain the Wikimedia Commons / patent / original-work attribution stored in the `author` and `license` columns. No new license is asserted over the archived `.tek` renderings beyond the source licenses.

## Special pages

- **`v-schmidt`** — the source SVG uses a `clipPath` on a hatch group. The converter does not apply that clip to fill outlines, so `fix_schmidt_clip.py` bakes the clip into the group first (44-point clip polygon, 32 hatch children), writing a temporary clipped SVG. The archived page is the converted clipped result; the command does both steps.
- **`v-saturn-sla`** — the source contains Polish diacritics. The command folds them to ASCII with `sed` before conversion (`ą→a`, `ć→c`, `ę→e`, `ł→l`, `ń→n`, `ó→o`, `ś→s`, `ź→z`, `ż→z`, and the uppercase forms), then uses `--fills outline --max-fills 1000`.
- **`c-beijing`** — the Beijing page was redone outside the ten-city pass: bbox `116.30,39.84,116.48,39.98`, `--min-length 160`, `--simplify 2.5`, producing **19,282 B**. The other ten city pages use the page bboxes and min-lengths from the original `fetch_convert.sh`:

| city | page bbox (minlon,minlat,maxlon,maxlat) | min-length | `.tek` B |
|---|---|---|---:|---:|
| Beijing | 116.30,39.84,116.48,39.98 | 160 | 19,282 |
| Shanghai | 121.406,31.184,121.544,31.296 | 180 | 23,518 |
| Guangzhou | 113.20,23.08,113.34,23.19 | 160 | 24,058 |
| Shenzhen | 113.96,22.49,114.12,22.60 | 180 | 24,083 |
| Chengdu | 103.99,30.52,104.14,30.63 | 200 | 23,704 |
| Chongqing | 106.48,29.51,106.62,29.62 | 220 | 24,458 |
| Wuhan | 114.23,30.53,114.38,30.65 | 140 | 24,006 |
| Hangzhou | 120.08,30.21,120.23,30.33 | 160 | 24,463 |
| Nanjing | 118.72,32.00,118.87,32.12 | 200 | 22,950 |
| Tianjin | 117.12,39.02,117.28,39.14 | 180 | 23,880 |
| Xi'an | 108.86,34.28,109.02,34.40 | 80 | 23,015 |

All eleven use `--styles layer --layers road-major,water,green,rail --simplify 2.5`, a single-line `CITY / OSM CONTRIBUTORS` caption, and the default 24,576-byte page budget.

The 8 base pages that use `convert_vector_v1.py` are `bell-mv22`, `boeing-ch47`, `curtiss-p40e`, `dornier-patent`, `javelin-thinwing`, `locomotive-040`, `rogozarski-ik3`, and `wright-flyer`.

## Verification

Recorded 2026-11-20 against the pinned PyMuPDF 1.28.2 / ezdxf 1.4.5 dependencies:

```
$ ./reproduce.sh --check
pages=227 identical=227 different=0 failed=0 missing=0
```

All 227 sources were present, all 227 commands completed, and every regenerated stream matched `tek/<id>.tek` byte-for-byte. `sha256sum -c checksums.sha256` reports 227 × `OK`.

## Dependencies

| package | tested version | needed for |
|---|---|---|
| `pymupdf` | **1.28.2** | every SVG/PDF page (`convert_vector*.py`) |
| `ezdxf` | **1.4.5** | 11 CAD pages |
| `lxml` | 6.1.1 | the `v-schmidt` clip fix |
| `Pillow` | 12.3 | `--preview` only, not reproduction |
| `pyshp` | 3.1.9 | Shapefile input, not used by these 227 pages |

PyMuPDF version matters for byte-identical output: the converters consume PyMuPDF's flattened drawing primitives, and a different version can change point counts or curve flattening. `dxf2tek_seeded.py` pins `random.seed()` before importing `dxf2tek.py` because ezdxf jitters hatch pattern-line origins; the seeds are per-page and are part of each command.

## Contributing

Issues and pull requests are welcome. For a new page, include:

1. the original vector source (SVG/PDF/DXF/OSM), with license and author;
2. the exact conversion command;
3. the `.tek` output and a source-vs-Tek side-by-side image;
4. the page in `sources.tsv`, `tek/`, and `checksums.sha256`.

Please keep the source native vector — no bitmaps, photos or scans.

## License

The `.tek` renderings are derived works of their sources; the source licenses are recorded per page in `sources.tsv` and `manifests/`. No new license is asserted over the archive beyond those source licenses. The city maps are ODbL 1.0, © OpenStreetMap contributors.

## Acknowledgements

- The original vector sources: Wikimedia Commons contributors, NASA, USGS, Pearson Scott Foresman, and the OpenStreetMap contributors.
- The Tektronix 4010/4014 command set and the original storage-tube documentation.
- The `vector2tek` converters and the host project that produced the initial pages.
