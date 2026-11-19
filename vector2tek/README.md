# vector2tek

Convert native vector sources into Tektronix 4010/4014 `.tek` streams.

## Converters

| file | input |
|---|---|
| `convert_vector.py` | SVG / PDF (native vector) |
| `convert_vector_v1.py` | legacy stroke-only converter for 8 base pages |
| `dxf2tek.py` | DXF |
| `dxf2tek_seeded.py` | DXF with `random.seed()` for byte-identical hatch output |
| `map2tek.py` | OpenStreetMap XML / ESRI Shapefile / GeoJSON |
| `tekcore.py` | 7-bit stream writer, fitter, validator |
| `fix_schmidt_clip.py` | per-page `clipPath` baker for `v-schmidt` |

## Usage

The authoritative per-page commands are in [`../sources.tsv`](../sources.tsv); the driver is [`../reproduce.sh`](../reproduce.sh):

```bash
cd ..
./reproduce.sh --list
./reproduce.sh --check
```

Each command converts one source from `../sources/<set>/` into `../tek/<id>.tek`. The `.tek` output is a 7-bit stream, at most 24,576 bytes, fitted to the 4096×3120 Tek viewport.

## Dependencies

```bash
python3 -m pip install -r requirements.txt
```

| package | version |
|---|---|
| `pymupdf` | 1.28.2 |
| `ezdxf` | 1.4.5 |
| `lxml` | 6.1.1 |
| `pyshp` | 3.1.9 (Shapefile only) |

Byte-identical reproduction depends on the pinned PyMuPDF and ezdxf versions.
