# Manifests

Per-set notes for the 227 pages in [`../tek/`](../tek/). The authoritative
per-page commands are in [`../sources.tsv`](../sources.tsv); the driver is
[`../reproduce.sh`](../reproduce.sh).

| set | pages | manifest |
|---|---:|---|
| base | 50 | `manifest.md` |
| q | 29 | `manifest-q.md` |
| v | 126 | `manifest-v.md` |
| cad | 11 | `manifest-cad.md` |
| city | 11 | `manifest-city.md` |

Also here: `manifest-quality.md` (quality counts), `directions.md` (subject
coverage notes).

Sources live in `../sources/<set>/`; `.tek` outputs in `../tek/`. The
converter is in `../vector2tek/`. Install once with
`python3 -m pip install -r ../vector2tek/requirements.txt`, then:

```bash
cd ..
./reproduce.sh --check
```
