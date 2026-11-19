# Tek material set — `q-` expansion (29 pages)

Generated: 2026-11-19T03:06:27+00:00  
Converter: `../vector2tek/convert_vector.py`, used as-is (defaults `--max-bytes 24576 --fill-mode hatch --hatch-spacing 36 --max-hatch-segments 300 --max-hatch-per-fill 80 --min-text-cell 40`); the script itself was not edited by this pass  
Budget: 24,576 B/page (5 B/point, 1 KB/s at 9600 baud)  
Hatch: 36 Tek units, 45°, ≤300 segments/page, ≤80 lines/fill; short side <40 or area <600 Tek units² → outline  
Text: Tek alpha font, horizontal spans only, min cell 40 Tek units, ASCII 32..126  
Pages: 29; total `.tek`: 382995 B; max page: 23330 B (94.9% of budget, `q-pat-723188`); text rendered: 17 pages / 1453 chars; hatched: 20 pages (1867 segments); filled: 26 pages.

Every page was validated as exactly one `ESC FF` page, all bytes ≤ 0x7F (7-bit), ≤ 24,576 B, and rendered to 640×480 with `tek-render-rgb222 --png` before being accepted.

`.tek` files live in `../tek/` (`q-*.tek`), PNG previews in (generated in the original working tree; not archived) (not archived), contact sheet `contact.png` (not archived). The 50-page base set in [`manifest.md`](manifest.md) is untouched and no page here reuses a base-set source file.

## Subject mix

| subject | new `q-` pages | base set |
|---|---|---|
| Ships | 3 | 6 |
| Architecture / bridges | 3 | 5 |
| Astronomy | 4 | 4 |
| Instruments | 3 | 6 |
| Machinery | 5 | 6 |
| Anatomy | 4 | 4 |
| Biology | 4 | 2 |
| Patent line art | 3 | 6 |
| **total** | **29** | **39** |

Quality: **23 good / 6 marginal** (marginal = sparse but sound, or a source limitation recorded below).

## Ships — 3 pages

| id | source | license / author | text | fill | .tek | Q |
|---|---|---|---|---|---|---|
| `q-kairyu` | [A drawing depicting the general arrangement and sections of the Japanese (WW2 era) Kair...](https://commons.wikimedia.org/wiki/File:Kairyu_general_arrangement_sections.svg) | Public domain / Lakkasuo | 38/41 spans, 268/319 chars; dropped 3 small | 1 stroke; 1 fills | [10802 B](../tek/q-kairyu.tek) 44.0% | G |
| `q-trireme` | [Cross-section of a trireme, an ancient Greek combat galley, following the last archaeol...](https://commons.wikimedia.org/wiki/File:Trireme_cut-en.svg) | CC BY-SA 3.0 / Eric Gaba (Sting - fr:Sting) | 0 (no text layer) | hatch 7 (192 seg), 6 outline, 14 stroke; 27 fills | [6899 B](../tek/q-trireme.tek) 28.1% | M |
| `q-torpedo-bulge` | [The anti-torpedo bulge (also known as an anti torpedo blister) is a form of passive def...](https://commons.wikimedia.org/wiki/File:Anti-torpedo_bulge.svg) | CC BY-SA 3.0 / fullofstars | 0 (no text layer) | hatch 8 (115 seg), 1 outline, 3 stroke; 12 fills | [19145 B](../tek/q-torpedo-bulge.tek) 77.9% | G |

- **`q-kairyu`** — General-arrangement plan/section of the Kairyu midget submarine; 3 views, clean strokes (PNG (not archived))
- **`q-trireme`** — Trireme midship section; the Commons figure is a partial crop, hull and oar tips bleed off the page edges (PNG (not archived))
- **`q-torpedo-bulge`** — Hull midship section with anti-torpedo bulge; hull shell hatched, 78% budget (PNG (not archived))

## Architecture / bridges — 3 pages

| id | source | license / author | text | fill | .tek | Q |
|---|---|---|---|---|---|---|
| `q-millau` | [Coupe du tablier du viaduc de Millau (France).](https://commons.wikimedia.org/wiki/File:Viaduc-Millau_tablier.svg) | CC BY-SA 3.0 / Roulex 45 | 0 (no text layer) | hatch 18 (56 seg), 69 outline, 13 stroke; 148 fills | [16763 B](../tek/q-millau.tek) 68.2% | G |
| `q-nanjing3` | [Third Nanjing Yangtze Bridge over the Yangtze river](https://commons.wikimedia.org/wiki/File:Nanjing-3-bridge.svg) | CC BY-SA 3.0 / Roulex_45 | 0 (no text layer) | hatch 3 (162 seg), 38 outline, 59 stroke; 119 fills | [9173 B](../tek/q-nanjing3.tek) 37.3% | G |
| `q-chongming` | [Elevation of Shanghai Yangtze River Tunnel and Bridge](https://commons.wikimedia.org/wiki/File:Chongming_bridge_elevation.svg) | CC BY-SA 3.0 / Glabb | 8/8 spans, 34/34 chars | hatch 1 (78 seg), 7 outline, 37 stroke; 49 fills | [3894 B](../tek/q-chongming.tek) 15.8% | G |

- **`q-millau`** — Millau Viaduct deck cross-section/elevation; 18 hatched + 69 outlined fills (PNG (not archived))
- **`q-nanjing3`** — Nanjing No.3 Yangtze bridge elevation + pylon sections; 37% budget (PNG (not archived))
- **`q-chongming`** — Shanghai Yangtze bridge elevation with cable fans; 16% budget, sparse but clean (PNG (not archived))

## Astronomy — 4 pages

| id | source | license / author | text | fill | .tek | Q |
|---|---|---|---|---|---|---|
| `q-flammarion73` | [Illustration de l’ouvrage de Camille Flammarion « Les Étoiles et les curiosités du ciel...](https://commons.wikimedia.org/wiki/File:Flammarion_-_Curiosit%C3%A9s_du_ciel_-_fig-073.svg) | CC0 / F0x1 | 67/68 spans, 305/315 chars; dropped 6 non-ASCII, 1 overlap | 2 outline; 2 fills | [10037 B](../tek/q-flammarion73.tek) 40.8% | G |
| `q-closed-orbits` | [Kształty orbit obiektów w polu sił grawitacyjnych, Orbity zamknięte: a) eliptyczna, b) ...](https://commons.wikimedia.org/wiki/File:Closed_orbits_shapes.svg) | Public domain / Malyszkz | 4/4 spans, 8/8 chars | hatch 4 (7 seg), 4 stroke; 8 fills | [1751 B](../tek/q-closed-orbits.tek) 7.1% | M |
| `q-retrograde` | [The motions that produce retrograde motion. As Earth passes a superior planet, such as ...](https://commons.wikimedia.org/wiki/File:Retrograde_Motion.bjb.svg) | CC BY-SA 3.0 / Brian Brondel | 10/10 spans, 10/10 chars | hatch 17 (102 seg), 1 stroke; 44 fills | [19441 B](../tek/q-retrograde.tek) 79.1% | G |
| `q-lunar-orbit` | [Diagram showing the precession of nodes of the Earth-Moon system](https://commons.wikimedia.org/wiki/File:Lunar_orbit.svg) | Public domain / Rayd8 | 15/15 spans, 81/81 chars | hatch 1 (3 seg), 1 stroke; 3 fills | [2414 B](../tek/q-lunar-orbit.tek) 9.8% | M |

- **`q-flammarion73`** — Flammarion analemma figure; 67 date labels placed, 41% budget (PNG (not archived))
- **`q-closed-orbits`** — Four orbit-shape panels; correct geometry but only 8 labels and 7% budget (PNG (not archived))
- **`q-retrograde`** — Retrograde-motion construction; 17 hatched + 10 labels, 79% budget (PNG (not archived))
- **`q-lunar-orbit`** — Lunar orbit / node precession diagram; 15 labels, 10% budget, sparse (PNG (not archived))

## Instruments — 3 pages

| id | source | license / author | text | fill | .tek | Q |
|---|---|---|---|---|---|---|
| `q-goniometer` | [Goniometer / angle scale diagram](https://commons.wikimedia.org/wiki/File:Goniometer-en.svg) | CC BY-SA 4.0 / Jooja | 63/64 spans, 122/124 chars; dropped 1 overlap | 1 outline; 1 fills | [12774 B](../tek/q-goniometer.tek) 52.0% | G |
| `q-microscope-diag` | [Simple microscope optical diagram](https://commons.wikimedia.org/wiki/File:Microscope_diag.svg) | CC BY-SA 3.0 / Cmprince | 8/10 spans, 25/27 chars; dropped 2 overlap | hatch 5 (93 seg), 1 stroke; 9 fills | [12394 B](../tek/q-microscope-diag.tek) 50.4% | G |
| `q-telescope-sch` | [Keplerian telescope, schematic](https://commons.wikimedia.org/wiki/File:Telescope-schematic.svg) | CC BY-SA 2.0 at / Michael Schmid | 13/13 spans, 27/27 chars | hatch 9 (26 seg), 86 outline, 2 stroke; 339 fills | [3907 B](../tek/q-telescope-sch.tek) 15.9% | M |

- **`q-goniometer`** — Goniometer/protractor scale; 63 labels, 122 chars, dense degree ticks (PNG (not archived))
- **`q-microscope-diag`** — Simple microscope optical diagram; 8/10 labels placed (PNG (not archived))
- **`q-telescope-sch`** — Keplerian telescope schematic; 9 hatch + 86 outline, sparse (PNG (not archived))

## Machinery — 5 pages

| id | source | license / author | text | fill | .tek | Q |
|---|---|---|---|---|---|---|
| `q-flintlock` | [SVG diagramme of a flintlock.](https://commons.wikimedia.org/wiki/File:Flintlock_diagramme.svg) | CC BY-SA 3.0 / Bastique | 5/5 spans, 27/27 chars | hatch 6 (300 seg), 5 outline, 23 stroke; 34 fills | [20788 B](../tek/q-flintlock.tek) 84.6% | G |
| `q-impulse-turbine` | [Schema einer Impulsturbine](https://commons.wikimedia.org/wiki/File:Impulsturbine.svg) | CC BY-SA 3.0 / Kopiersperre, Jahobr | 5/5 spans, 35/36 chars; dropped 1 non-ASCII | hatch 4 (11 seg), 12 stroke; 16 fills | [7262 B](../tek/q-impulse-turbine.tek) 29.5% | G |
| `q-reaction-turbine` | [Schema einer Reaktionsturbine](https://commons.wikimedia.org/wiki/File:Reaktionsturbine.svg) | CC BY-SA 3.0 / Kopiersperre, Jahobr | 5/5 spans, 31/32 chars; dropped 1 non-ASCII | hatch 3 (9 seg), 1 outline, 11 stroke; 15 fills | [11888 B](../tek/q-reaction-turbine.tek) 48.4% | G |
| `q-kaiten` | [Drawings of the fuel and oxidiser injection nozzle from a type 2 kaiten's engine compar...](https://commons.wikimedia.org/wiki/File:Kaiten_type_2_fuel_injection_details-1.svg) | Public domain / Lakkasuo | 14/14 spans, 200/200 chars | none | [5909 B](../tek/q-kaiten.tek) 24.0% | G |
| `q-segner` | [Segner water turbine: A - water inlet, B - vertical tube with rotor, C - rotor with noz...](https://commons.wikimedia.org/wiki/File:Segner_turbine.svg) | CC BY 3.0 / Zureks | 7/7 spans, 7/7 chars | hatch 2 (6 seg); 2 fills | [6479 B](../tek/q-segner.tek) 26.4% | M |

- **`q-flintlock`** — Flintlock lock mechanism cutaway; 27 chars labels, 85% budget (PNG (not archived))
- **`q-impulse-turbine`** — Impulse turbine stage diagram; velocity triangles + rotor section (PNG (not archived))
- **`q-reaction-turbine`** — Reaction turbine stage diagram; velocity triangles + rotor section (PNG (not archived))
- **`q-kaiten`** — Kaiten torpedo fuel/oxidiser injector drawing; 200 chars labels (PNG (not archived))
- **`q-segner`** — Segner water-wheel turbine scheme; labelled A-G, 26% budget (PNG (not archived))

## Anatomy — 4 pages

| id | source | license / author | text | fill | .tek | Q |
|---|---|---|---|---|---|---|
| `q-gray424` | [Gray's Anatomy plate 424 — bones of the hand](https://commons.wikimedia.org/wiki/File:Gray424.svg) | Public domain / Henry Vandyke Carter (Gray's Anatomy) | 0 (no text layer) | 1 outline; 29 fills | [18297 B](../tek/q-gray424.tek) 74.5% | G |
| `q-gray511` | [Plan of branches of maxillary artery.](https://commons.wikimedia.org/wiki/File:Gray511.svg) | Public domain / Henry Vandyke Carter (Gray's Anatomy) | 0 (no text layer) | 100 outline; 258 fills | [23209 B](../tek/q-gray511.tek) 94.4% | G |
| `q-digastricus` | [Scheme of muscles of neck, with marked digastric muscle marked.](https://commons.wikimedia.org/wiki/File:Musculi_colli_digastricus.svg) | CC BY-SA 2.5 / Olek Remesz (wiki-pl: Orem, commons: Orem) | 3/3 spans, 49/49 chars | hatch 10 (89 seg), 30 outline, 3 stroke; 61 fills | [22271 B](../tek/q-digastricus.tek) 90.6% | G |
| `q-fossa` | [Scheme of fossa pterygopalatina - numbered; a–processus pterygoideus; b–facies maxillar...](https://commons.wikimedia.org/wiki/File:Fossa_pterygopalatina.svg) | CC BY-SA 3.0 / Tikaa | 0 (no text layer) | hatch 6 (38 seg), 40 outline, 2 stroke; 53 fills | [13119 B](../tek/q-fossa.tek) 53.4% | M |

- **`q-gray424`** — Gray's plate: bones of the hand; outlined engraved lines, 75% budget (PNG (not archived))
- **`q-gray511`** — Gray's plate: branches of the maxillary artery; hatching would flood the arterial tree, so fills are outlined (100 outlines) (PNG (not archived))
- **`q-digastricus`** — Neck muscles scheme with digastric highlighted; 49 chars labels, 91% budget (PNG (not archived))
- **`q-fossa`** — Pterygopalatine fossa scheme; 40 outlined structures, labels are paths (PNG (not archived))

## Biology — 4 pages

| id | source | license / author | text | fill | .tek | Q |
|---|---|---|---|---|---|---|
| `q-bird-skeleton-fr` | [A stylised bird skeleton 1. Skull, 2. Cervical vertebrae, 3. Furcula, 4. Coracoid, 5. U...](https://commons.wikimedia.org/wiki/File:Squelette_oiseau.svg) | CC BY 2.5 / BIODIDAC / mario m | 27/27 spans, 45/45 chars | hatch 1 (4 seg), 1 outline; 105 fills | [21681 B](../tek/q-bird-skeleton-fr.tek) 88.2% | G |
| `q-tulip-leaf` | [Tulip Tree Leaf](https://commons.wikimedia.org/wiki/File:Tulip_Tree_Leaf-vector.svg) | CC0 / Offnfopt | 0 (no text layer) | 1 outline; 1 fills | [15950 B](../tek/q-tulip-leaf.tek) 64.9% | G |
| `q-barnacle` | [Anatomy of a sessile barnacle](https://commons.wikimedia.org/wiki/File:Barnacles_Sessile_anatomy.svg) | CC0 / WikiLeaxus | 20/20 spans, 179/179 chars | hatch 7 (61 seg), 86 outline, 6 stroke; 746 fills | [11320 B](../tek/q-barnacle.tek) 46.1% | G |
| `q-crossopterygii` | [Comparison between the fins of A., Crossopterygiin fishes and the legs of B., tetrapods...](https://commons.wikimedia.org/wiki/File:Crossopterygii_fins_tetrapod_legs.svg) | Public domain / Conty | 0 (no text layer) | hatch 14 (450/120 cap), 49 outline; 64 fills | [13383 B](../tek/q-crossopterygii.tek) 54.5% | G |

- **`q-bird-skeleton-fr`** — Bird skeleton, 27 numbered labels; 88% budget (PNG (not archived))
- **`q-tulip-leaf`** — Tulip-tree leaf with vein network; single compound path, 65% budget (PNG (not archived))
- **`q-barnacle`** — Sessile barnacle anatomy; 20 labels/179 chars (PNG (not archived))
- **`q-crossopterygii`** — Crossopterygian fin to tetrapod limb comparison; hatch cap 450/120, 49 outline; 54.5% budget (PNG (not archived))

## Patent line art — 3 pages

| id | source | license / author | text | fill | .tek | Q |
|---|---|---|---|---|---|---|
| `q-pat-1233841` | [US patent 1,233,841, figure 1](https://commons.wikimedia.org/wiki/File:US_patent_1233841-001-001.svg) | Public domain / Elmer E. Bucher | 0 (no text layer) | none | [20837 B](../tek/q-pat-1233841.tek) 84.8% | G |
| `q-pat-723188` | [US patent 723,188 (Tesla) — Method of Signaling, Fig. 1](https://commons.wikimedia.org/wiki/File:US_patent_723188-001-1.svg) | Public domain / Nikola Tesla | 0 (no text layer) | none | [23330 B](../tek/q-pat-723188.tek) 94.9% | G |
| `q-pat-1180648` | [US patent 1,180,648, figures 4 and 5 — polarized socket and plug](https://commons.wikimedia.org/wiki/File:US_patent_1180648,_fig_4_and_5.svg) | CC0 / Comrade Mmirg | 0 (no text layer) | outline 39 (tol 2); 39 fills | [17878 B](../tek/q-pat-1180648.tek) 72.7% | G |

- **`q-pat-1233841`** — US patent 1,233,841 (Bucher): circuit figure with tuning coil, capacitor and antenna terminals; 85% budget (PNG (not archived))
- **`q-pat-723188`** — US patent 723,188 (Tesla) signalling figure; 95% budget, dense (PNG (not archived))
- **`q-pat-1180648`** — US patent 1,180,648, figs 4-5: polarized socket and plug; outline-tol 2, socket slots/plug readable (72.7% budget) (PNG (not archived))

## Held back / not usable (56)

Inspected and converted or measured, but not put in the final set. Numbers are measured from the converter's own stats.

| candidate | subject | file | why |
|---|---|---|---|
| `q-i201` | ships | [I-201 class general arrangement sections.svg](https://commons.wikimedia.org/wiki/File:I-201_class_general_arrangement_sections.svg) | All 227 text spans are Japanese: 0/1,739 chars placed, so the sheet would carry no annotations; art itself is good (91% budget). |
| `q-navio` | ships | [Esquema de un navio de linea.svg](https://commons.wikimedia.org/wiki/File:Esquema_de_un_navio_de_linea.svg) | Source viewBox clips the hull on both sides (24,441 B / 99.5% budget spent on a cropped drawing). |
| `q-clinker` | ships | [Clinker-carvel.svg](https://commons.wikimedia.org/wiki/File:Clinker-carvel.svg) | 825 B: two bare arcs, severe simplification. |
| `q-ship-dims` | ships | [Ship main dimensions.svg](https://commons.wikimedia.org/wiki/File:Ship_main_dimensions.svg) | 1,062 B; dimension lines only, labels unreadable. |
| `q-double-hull` | ships | [DoubleBottomDoubleHull.svg](https://commons.wikimedia.org/wiki/File:DoubleBottomDoubleHull.svg) | Narrow strip section, reads as a crop rather than a page. |
| `q-pont-coupe` | arch | [Pont-haubané-nappe-axiale-coupe.svg](https://commons.wikimedia.org/wiki/File:Pont-hauban%C3%A9-nappe-axiale-coupe.svg) | Figure occupies two corners with ~80% blank page. |
| `q-suspension` | arch | [Suspension bridge.svg](https://commons.wikimedia.org/wiki/File:Suspension_bridge.svg) | 1,958 B CC0 icon-grade schematic, severe simplification. |
| `q-truss` | arch | [Truss bridge.svg](https://commons.wikimedia.org/wiki/File:Truss_bridge.svg) | 860 B CC0 icon-grade schematic. |
| `q-cantilever` | arch | [Cantilever bridge, balanced.svg](https://commons.wikimedia.org/wiki/File:Cantilever_bridge,_balanced.svg) | 1,153 B CC0 icon-grade schematic. |
| `q-brit-orbit` | astro | [1911 Britannica - Astronomy - Orbit.svg](https://commons.wikimedia.org/wiki/File:1911_Britannica_-_Astronomy_-_Orbit.svg) | 416 B: one circle plus one chord. |
| `q-brit-telescope` | astro | [1911 Britannica - Astronomy - Telescope.svg](https://commons.wikimedia.org/wiki/File:1911_Britannica_-_Astronomy_-_Telescope.svg) | 1,213 B, 4 chars of text; too sparse. |
| `q-analemma` | astro | [Analemme.svg](https://commons.wikimedia.org/wiki/File:Analemme.svg) | 17.7% budget but the 2024 date labels collide (overlap-skipped spans); rejected in favour of the Flammarion analemma. |
| `q-hubble-fork` | astro | [Hubble Tuning Fork diagram.svg](https://commons.wikimedia.org/wiki/File:Hubble_Tuning_Fork_diagram.svg) | Only the two fork arms survive — the galaxy thumbnails are raster, so the diagram is incomplete (5,263 B). |
| `q-diurnal` | astro | [Diurnal motion by latitude.svg](https://commons.wikimedia.org/wiki/File:Diurnal_motion_by_latitude.svg) | 24,415 B (99.3%) for a row of five hatched circles: visually near-empty. |
| `q-eclipse-geom` | astro | [Geometry of Solar eclipses and Lunar eclipses.svg](https://commons.wikimedia.org/wiki/File:Geometry_of_Solar_eclipses_and_Lunar_eclipses.svg) | 532 B: content is a 3-circle strip at the page bottom. |
| `q-eratosthenes` | astro | [Eratosthenes.bjb.svg](https://commons.wikimedia.org/wiki/File:Eratosthenes.bjb.svg) | Drawing sits in one corner of a 400x400 page; ~85% blank. |
| `q-gnss-orbits` | astro | [Comparison satellite navigation orbits.svg](https://commons.wikimedia.org/wiki/File:Comparison_satellite_navigation_orbits.svg) | 48.3% budget but the altitude labels fall below the 40-unit Tek cell and are dropped: an unlabelled ring drawing. |
| `q-flammarion74` | astro | [Flammarion - Curiosités du ciel - fig-074.svg](https://commons.wikimedia.org/wiki/File:Flammarion_-_Curiosit%C3%A9s_du_ciel_-_fig-074.svg) | 1,298 B, one circle. |
| `q-kepler1` | astro | [Kepler's law 1 en.svg](https://commons.wikimedia.org/wiki/File:Kepler's_law_1_en.svg) | Good, but repeats the topic of the existing `kepler` page; not added. |
| `q-ptolemy` | astro | [Ptolemaic elements.svg](https://commons.wikimedia.org/wiki/File:Ptolemaic_elements.svg) | 2,250 B of concentric rings at 168x168 source. |
| `q-inner-orbits` | astro | [Inner Planet Orbits 01.svg](https://commons.wikimedia.org/wiki/File:Inner_Planet_Orbits_01.svg) | 2,605 B unlabelled rings. |
| `q-outer-orbits` | astro | [Outer Planet Orbits 02.svg](https://commons.wikimedia.org/wiki/File:Outer_Planet_Orbits_02.svg) | 6,544 B rings, no labels. |
| `q-orbital-planes` | astro | [Orbital Planes.svg](https://commons.wikimedia.org/wiki/File:Orbital_Planes.svg) | 14.3% budget; 22/104 label chars lost and the bodies hatch into blobs. |
| `q-planet-sizes` | astro | [Solar system planet relative sizes.svg](https://commons.wikimedia.org/wiki/File:Solar_system_planet_relative_sizes.svg) | Planet discs are fills only: 0/263 chars placed, 2,248 B. |
| `q-microscope-path` | instr | [Microscope-optical path.svg](https://commons.wikimedia.org/wiki/File:Microscope-optical_path.svg) | 99.3% budget and the ray bundle collapses into one hatched band; unreadable. |
| `q-mikroskop` | instr | [Mikroskop Strahlengang.svg](https://commons.wikimedia.org/wiki/File:Mikroskop_Strahlengang.svg) | 99.4% budget, same collapse as the previous file. |
| `q-refractor` | instr | [Refractor.svg](https://commons.wikimedia.org/wiki/File:Refractor.svg) | 6,978 B: tube outline plus one lens, no labels. |
| `q-galileo-scope` | instr | [Fernrohr galilei.svg](https://commons.wikimedia.org/wiki/File:Fernrohr_galilei.svg) | 1,081 B, two labels. |
| `q-grades-degrees` | instr | [Grades degrees.svg](https://commons.wikimedia.org/wiki/File:Grades_degrees.svg) | 1,742 B; table of 234 chars dominates, geometry is a thin fan. |
| `q-newcomen` | mech | [Engine newcomen.svg](https://commons.wikimedia.org/wiki/File:Engine_newcomen.svg) | MdeVicente engine drawings split boiler/cylinder/pump into disconnected fragments; also the same author as existing `engine-watt`. |
| `q-savery` | mech | [Engine savery.svg](https://commons.wikimedia.org/wiki/File:Engine_savery.svg) | Same author/series; fragmented sub-drawings (3,854 B). |
| `q-papin` | mech | [Engine papin.svg](https://commons.wikimedia.org/wiki/File:Engine_papin.svg) | Same author/series; fragmented sub-drawings. |
| `q-trevithick` | mech | [Engine trevithick puffer.svg](https://commons.wikimedia.org/wiki/File:Engine_trevithick_puffer.svg) | Same author/series; fragmented sub-drawings. |
| `q-furutaka-turbine` | mech | [Starboard turbine sets of Furutaka and Aoba class cruisers.svg](https://commons.wikimedia.org/wiki/File:Starboard_turbine_sets_of_Furutaka_and_Aoba_class_cruisers.svg) | 1,423 B at 5.8% budget; too small to read. |
| `q-turbine-schema` | mech | [Schéma de principe d'une turbine.svg](https://commons.wikimedia.org/wiki/File:Sch%C3%A9ma_de_principe_d'une_turbine.svg) | 821 B, 3.3% budget: three boxes and arrows. |
| `q-combined-cycle` | mech | [Combined cycle-diagram.svg](https://commons.wikimedia.org/wiki/File:Combined_cycle-diagram.svg) | 1,745 B box-and-arrow schematic. |
| `q-drill-geom` | mech | [Geometria wiertla krętego 16x120.svg](https://commons.wikimedia.org/wiki/File:Geometria_wiertla_kr%C4%99tego_16x120.svg) | 3,259 B; ambiguous drill profile plus a sine wave, no labels. |
| `q-ballista` | mech | [Ballista (PSF) vector.svg](https://commons.wikimedia.org/wiki/File:Ballista_(PSF)_vector.svg) | The SVG carries all stroke/fill styling in CSS classes, so PyMuPDF returns one undrawn path: 4-byte page. |
| `q-gray2` | anat | [Gray2.svg](https://commons.wikimedia.org/wiki/File:Gray2.svg) | 98% budget spent on eight dense tooth cross-sections; subject unreadable at 640x480. |
| `q-gray726` | anat | [Gray726.svg](https://commons.wikimedia.org/wiki/File:Gray726.svg) | 54 labels/396 chars crowd into an unreadable mass at panel size. |
| `q-gray812` | anat | [Gray812.svg](https://commons.wikimedia.org/wiki/File:Gray812.svg) | Good plate, but the Gray's series cap (2) was spent on plates 424 and 511. |
| `q-gray1220` | anat | [Gray1220.svg](https://commons.wikimedia.org/wiki/File:Gray1220.svg) | Same series cap. |
| `q-gray826` | anat | [Gray826and831.svg](https://commons.wikimedia.org/wiki/File:Gray826and831.svg) | 13.9 KB of very faint outline; only 56.6% budget and hard to read. |
| `q-balanus` | bio | [Balanus anatomy.svg](https://commons.wikimedia.org/wiki/File:Balanus_anatomy.svg) | Embedded base64 JPEG, no vector paths: raster, rejected. |
| `q-dragonfly` | bio | [Dragonfly 2 (PSF).svg](https://commons.wikimedia.org/wiki/File:Dragonfly_2_(PSF).svg) | CSS-only styling: 4-byte page. |
| `q-cauliflower` | bio | [Cauliflower (PSF).svg](https://commons.wikimedia.org/wiki/File:Cauliflower_(PSF).svg) | CSS-only styling: 4-byte page. |
| `q-bird-skeleton` | bio | [Bird squeleton.svg](https://commons.wikimedia.org/wiki/File:Bird_squeleton.svg) | CSS-only styling: 4-byte page; the French derivative converted cleanly and is used instead. |
| `q-starfish` | bio | [Starfish (PSF).svg](https://commons.wikimedia.org/wiki/File:Starfish_(PSF).svg) | 99.4% budget; the stipple body aliases into speckle. |
| `q-squid` | bio | [Squid (PSF).svg](https://commons.wikimedia.org/wiki/File:Squid_(PSF).svg) | 6,168 B of extremely faint strokes. |
| `q-leaf-morph` | bio | [Leaf morphology.svg](https://commons.wikimedia.org/wiki/File:Leaf_morphology.svg) | 99.5% budget and 64/134 spans (547/1,997 chars) placed: too much text loss. |
| `q-leaf-layers` | bio | [Layers of a Leaf.svg](https://commons.wikimedia.org/wiki/File:Layers_of_a_Leaf.svg) | 99.4% budget, 0 text; cell layers smear together. |
| `q-leaf-simple` | bio | [Diagram of simple leaf.svg](https://commons.wikimedia.org/wiki/File:Diagram_of_simple_leaf.svg) | 40.6% budget but the section collapses into a hatched rectangle. |
| `q-serrated-leaf` | bio | [Serrated leaf (PSF).svg](https://commons.wikimedia.org/wiki/File:Serrated_leaf_(PSF).svg) | Clean 6,364 B leaf; held back to keep the biology group at four pages. |
| `q-pat-774250` | pat | [US patent 774250, fig 1.svg](https://commons.wikimedia.org/wiki/File:US_patent_774250,_fig_1.svg) | Fill-only line art: 5 drawings, 243 B extracted. |
| `q-pat-1064833` | pat | [US Patent 1064833, fig 1 and 3.svg](https://commons.wikimedia.org/wiki/File:US_Patent_1064833,_fig_1_and_3.svg) | 13,422 B but only one small device on the sheet. |
| `q-pat-8470` | pat | [Mathushek US patent 8470, fig 1 colorized.svg](https://commons.wikimedia.org/wiki/File:Mathushek_US_patent_8470,_fig_1_colorized.svg) | 50 labels placed but the perspective action is unreadable at panel size (28.8% budget). |

Also rejected at source level by the converter's raster check, not listed above: pages whose only content is an embedded bitmap.

## PDF sampling

(generated in the original working tree; not archived) (NASA, public domain) was sampled as the PD-manual vector-PDF source: 356 pages, 177 with `get_drawings() > 0`. The three densest figure pages (294, 253, 227) were converted: they are text documents whose drawings are table rules and callout boxes — 2/64, 51/164 and 49/50 text spans placeable, 2.6–5.5 KB per page. No PDF page met the line-art bar, so the set keeps SVG/dataset sources only; no half-converted PDF page was forced in.

## Method

- **Pool**: 89 candidates — Wikimedia Commons SVG category sweeps (Astronomical diagrams, Cross sections of ships, Diagrams of bridges, Turbine/Water turbine diagrams, Anatomy diagrams, Bird skeletons, Leaf diagrams, Refracting telescope diagrams, Drawings of light microscopes, Drawings of steam engines, Gray's Anatomy SVGs, Pearson Scott Foresman SVGs), Commons `intitle:"US patent"` searches.
- **Licenses**: only public domain, CC0, CC BY and CC BY-SA files; each page's license and author come from the Commons `imageinfo/extmetadata` API.
- **Fair use of sources**: at most two pages per author/series (e.g. Gray's plates 424+511, Roulex_45's Millau+Nanjing bridges, Lakkasuo's Kairyu+Kaiten, Kopiersperre/Jahobr's impulse+reaction turbines).
- **No duplicates**: no source file here appears in the base 50-page set; topics were checked against `manifest.md` (aviation was deliberately avoided, a single 1911 Kepler's-law figure was dropped because `kepler` already covers that diagram).
- **Per-page tuning**: `--fills hatch` everywhere except `q-gray511`, where hatching floods the arterial tree and `--fills outline` is used (100 outlines, 94.4% budget); maps use `--no-text`.
- **Skips are not padding**: 56 candidates were dropped for the measured reasons above (raster, CSS-only styling, icon-grade sparseness, clipped sources, text loss, or unreadable density).

