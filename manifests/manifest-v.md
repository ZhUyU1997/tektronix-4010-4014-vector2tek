# Tek material set — `v-` expansion (126 pages)

Generated: 2026-11-19T07:46:23Z; P5 satellites/probes appended 2026-11-19T10:51:09Z; P5b spacecraft/stations/telescope appended 2026-11-19T11:07:31Z  
Converter: `../vector2tek/convert_vector.py`, used unchanged (defaults `--max-bytes 24576 --fills hatch --hatch-spacing 36 --max-hatch-segments 300 --max-hatch-per-fill 80 --min-text-cell 40`; per-page overrides noted below)  
Budget: 24,576 B/page, 7-bit Tek stream, exactly one `ESC FF` page  
Text: Tek alpha font, horizontal ASCII spans only, 40-unit minimum cell  
Hatch: 36 Tek units, 45°, ≤300 segments/page, ≤80 lines/fill; short side <40 or area <600 Tek units² → outline  
Pages: 126; total `.tek`: 1985380 B; max page: 24448 B (99.5%, `v-bismarck`; `v-mir` is also 24448 B); text rendered: 91 pages; hatched: 65 pages.

`.tek` files live in `../tek/` (`v-*.tek`), raw 640×480 previews and 480×640 device previews in (generated in the original working tree; not archived) (not archived); contact sheet `contact.png` (not archived). The base 50 and q 29 pages are untouched; no source file is shared with them.

Quality: **97 good / 29 marginal** (marginal = sparse but sound, or a source limitation recorded below).


> **Visual audit 2026-11-19 (pre-P5):** 7 drop pages applied (3 + 4); 10 more G pages are recommended M but not yet applied. The audit's hypothetical tallies predate P5 and are not applied to this set. Audit report: (generated in the original working tree; not archived).

## Subject mix

| subject | `v-` pages | existing (base + q) |
|---|---:|---:|
| Ships | 4 | 9 |
| Instruments | 8 | 9 |
| Machinery | 15 | 11 |
| Architecture | 8 | 8 |
| Anatomy | 4 | 8 |
| Astronomy | 3 | 8 |
| Biology | 4 | 6 |
| Animals | 13 | 0 |
| Plants | 5 | 0 |
| Aerospace | 20 | 0 |
| CAD / mechanical cutaway | 5 | 0 |
| Electronics / PCB | 5 | 0 |
| Mathematics / geometry | 4 | 0 |
| Paleontology | 3 | 0 |
| Chemistry / crystals | 8 | 0 |
| Design / typography | 4 | 0 |
| System anatomy / plants | 3 | 0 |
| Patent line art | 2 | 9 |
| Maps (Natural Earth) | 1 | 3 |
| CAD / PCB / design | 3 | 0 |
| Geology / earth science | 4 | 0 |
| **total** | **126** | **79** |

Base/q predate the animal/plant split: their animal and plant pages are counted under Biology (6 existing pages). The animal/plant, CAD, electronics, mathematics, paleontology, chemistry, typography and system-anatomy additions are the first explicitly labelled pages in those groups.

## Ships — 4 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-bismarck` | [Battleship Bismark.svg](https://commons.wikimedia.org/wiki/File%3ABattleship_Bismark.svg) | CC0 / charner1963 | 0 (no text layer) | 2 hatch/85 seg; 1 outline; 83 stroke; 6 light skipped; 1265 skipped (1357 fills) | [24448 B](../tek/v-bismarck.tek) | 99.5% | G |
| `v-hungarian` | [Hungarian-1858.svg](https://commons.wikimedia.org/wiki/File%3AHungarian-1858.svg) | Public domain / Bukk | 0 (no text layer) | 24 hatch/293 seg; 7 outline; 59 stroke (90 fills) | [18139 B](../tek/v-hungarian.tek) | 73.8% | G |
| `v-soling` | [Soling Line Drawing.svg](https://commons.wikimedia.org/wiki/File%3ASoling_Line_Drawing.svg) | CC BY-SA 3.0 / VYGOcommons | 0 (no text layer) | 8 hatch/300 seg; 76 outline; 1 stroke; 89 skipped (189 fills) | [7379 B](../tek/v-soling.tek) | 30.0% | G |
| `v-trieste` | [Trieste nh96807.svg](https://commons.wikimedia.org/wiki/File%3ATrieste_nh96807.svg) | Public domain / RalphSutherland | 2/2 spans, 28/28 chars | 13 hatch/299 seg; 27 outline; 3 stroke; 73 skipped (116 fills) | [24443 B](../tek/v-trieste.tek) | 99.5% | G |

- **`v-bismarck`** — Bismarck battleship side profile; hull hatching and full superstructure (640×480 (not archived), device 480×640 (not archived))
- **`v-hungarian`** — 1858 steamship Hungarian side elevation; hull and paddle boxes hatched (640×480 (not archived), device 480×640 (not archived))
- **`v-soling`** — Soling keelboat line drawing; hatched sail and hull sections (640×480 (not archived), device 480×640 (not archived))
- **`v-trieste`** — General-arrangement drawing of the bathyscaphe Trieste; all callouts readable (640×480 (not archived), device 480×640 (not archived))

## Instruments — 3 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-clock-gear` | [Clock gear.svg](https://commons.wikimedia.org/wiki/File%3AClock_gear.svg) | Public domain / Chandler B. Beach (1839-1928) (editor), A.M., associate editor Frank Morton McMurry (1862-1936); User:LA2 (modifications in 2005) | 0 (no text layer) | 1 outline (1 fills) | [6565 B](../tek/v-clock-gear.tek) | 26.7% | G |
| `v-compass-instruments` | [Compass, Protractor, Slide Rule.svg](https://commons.wikimedia.org/wiki/File%3ACompass%2C_Protractor%2C_Slide_Rule.svg) | CC BY 4.0 / Editor B | 0 (no text layer) | 3 hatch/49 seg; 7 outline (10 fills) | [12416 B](../tek/v-compass-instruments.tek) | 50.5% | G |
| `v-vernier` | [Vernier caliper legends.svg](https://commons.wikimedia.org/wiki/File%3AVernier_caliper_legends.svg) | CC BY 2.5 / Joaquim Alves Gaspar, vectorised by Antilived | 54/85 spans, 283/342 chars | 1 hatch/12 seg; 6 outline; 10 stroke (17 fills) | [7972 B](../tek/v-vernier.tek) | 32.4% | G |

- **`v-clock-gear`** — Old anchor escapement wheel and anchor, bold single-path line art (640×480 (not archived), device 480×640 (not archived))
- **`v-compass-instruments`** — Compass, protractor and slide rule still life; bold native line work (640×480 (not archived), device 480×640 (not archived))
- **`v-vernier`** — Vernier caliper with scale and 54 legend labels (640×480 (not archived), device 480×640 (not archived))

## Machinery — 9 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-antikythera` | [Antikythera1.svg](https://commons.wikimedia.org/wiki/File%3AAntikythera1.svg) | CC0 / Createaccount | 45/78 spans, 189/259 chars | 19 hatch/300 seg; 6 outline; 40 stroke; 8 light skipped (73 fills) | [16446 B](../tek/v-antikythera.tek) | 66.9% | M |
| `v-belfast-boiler` | [HMS Belfast - Boiler diagram.svg](https://commons.wikimedia.org/wiki/File%3AHMS_Belfast_-_Boiler_diagram.svg) | CC BY-SA 4.0 / Shakki | 11/11 spans, 13/13 chars | 8 hatch/178 seg; 2 outline; 81 stroke; 1 light skipped; 182 skipped (274 fills) | [24436 B](../tek/v-belfast-boiler.tek) | 99.4% | G |
| `v-epicycloidal` | [Epure cinematique epicycloidal.svg](https://commons.wikimedia.org/wiki/File%3AEpure_cinematique_epicycloidal.svg) | CC BY-SA 3.0 / Ruizo | 0 (no text layer) | 2 outline; 5 skipped (7 fills) | [19514 B](../tek/v-epicycloidal.tek) | 79.4% | M |
| `v-hand-pump` | [Hand pump-en.svg](https://commons.wikimedia.org/wiki/File%3AHand_pump-en.svg) | CC BY-SA 3.0 / Manco Capac | 11/11 spans, 103/103 chars | 22 hatch/244 seg; 23 outline; 50 stroke; 5 light skipped; 55 skipped (155 fills) | [10017 B](../tek/v-hand-pump.tek) | 40.8% | G |
| `v-invincible-engine` | [HMS Invincible 1907 starboard engine room.svg](https://commons.wikimedia.org/wiki/File%3AHMS_Invincible_1907_starboard_engine_room.svg) | CC0 / sas1975kr | 25/25 spans, 41/41 chars | 24 outline; 76 light skipped; 197 skipped (297 fills) | [17531 B](../tek/v-invincible-engine.tek) | 71.3% | G |
| `v-jet-engine` | [Jet engine numbered.svg](https://commons.wikimedia.org/wiki/File%3AJet_engine_numbered.svg) | CC BY-SA 4.0 / Jeff Dahl | 0 (no text layer) | 9 hatch/300 seg; 25 outline; 62 stroke; 206 skipped (302 fills) | [24347 B](../tek/v-jet-engine.tek) | 99.1% | M |
| `v-offset-press` | [Offset press scheme.svg](https://commons.wikimedia.org/wiki/File%3AOffset_press_scheme.svg) | CC BY-SA 4.0 / Inkman | 10/10 spans, 137/137 chars | 37 hatch/258 seg; 7 outline (44 fills) | [9001 B](../tek/v-offset-press.tek) | 36.6% | G |
| `v-powerstation` | [PowerStation3.svg](https://commons.wikimedia.org/wiki/File%3APowerStation3.svg) | CC BY-SA 3.0 / BillC at English Wikipedia | 55/56 spans, 534/538 chars | 13 hatch/300 seg; 50 outline; 34 stroke; 3 light skipped; 339 skipped (439 fills) | [21933 B](../tek/v-powerstation.tek) | 89.2% | G |
| `v-trevithick-loco` | [Locomotive trevithick.svg](https://commons.wikimedia.org/wiki/File%3ALocomotive_trevithick.svg) | Public domain / Locomotive trevithick.jpg: Original uploader was Urizzato at en.wikipedia derivative work: Malyszkz (talk) | 0 (no text layer) | 5 hatch/123 seg; 1 outline; 89 stroke; 5 light skipped; 62 skipped (162 fills) | [19807 B](../tek/v-trevithick-loco.tek) | 80.6% | G |

- **`v-antikythera`** — Antikythera gear-train reconstruction; dense concentric gears, 45/78 labels (640×480 (not archived), device 480×640 (not archived))
- **`v-belfast-boiler`** — HMS Belfast boiler cutaway; numbered callouts 1-11, 99.4% budget (640×480 (not archived), device 480×640 (not archived))
- **`v-epicycloidal`** — Epicycloidal gear-tooth construction; formulas are vector outlines (640×480 (not archived), device 480×640 (not archived))
- **`v-hand-pump`** — Hand pump cross-section with 11 labelled parts (640×480 (not archived), device 480×640 (not archived))
- **`v-invincible-engine`** — HMS Invincible engine-room elevation with 25 numbered callouts (640×480 (not archived), device 480×640 (not archived))
- **`v-jet-engine`** — Turbojet engine section with numbered stations; 99.1% budget (640×480 (not archived), device 480×640 (not archived))
- **`v-offset-press`** — Offset press cylinder stack; every unit labelled (640×480 (not archived), device 480×640 (not archived))
- **`v-powerstation`** — Coal-fired power station schematic with legend and flow labels (640×480 (not archived), device 480×640 (not archived))
- **`v-trevithick-loco`** — Trevithick and Vivian locomotive side elevation (640×480 (not archived), device 480×640 (not archived))

## Architecture — 4 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-acropolis-plan` | [Plan Acropolis of Athens.svg](https://commons.wikimedia.org/wiki/File%3APlan_Acropolis_of_Athens.svg) | CC BY-SA 4.0 / Tomisti | 36/36 spans, 63/63 chars | 8 hatch/232 seg; 92 outline; 34 skipped (134 fills) | [14622 B](../tek/v-acropolis-plan.tek) | 59.5% | M |
| `v-cordoba-hypostyle` | [Hypostyle hall of the Mosque-Cathedral of Córdoba-en.svg](https://commons.wikimedia.org/wiki/File%3AHypostyle_hall_of_the_Mosque-Cathedral_of_C%C3%B3rdoba-en.svg) | CC BY-SA 3.0 / Américo Toledano | 17/17 spans, 161/161 chars | 29 hatch/202 seg; 71 outline; 850 skipped (950 fills) | [7314 B](../tek/v-cordoba-hypostyle.tek) | 29.8% | G |
| `v-denbigh-castle` | [Denbigh Castle plan, labelled.svg](https://commons.wikimedia.org/wiki/File%3ADenbigh_Castle_plan%2C_labelled.svg) | Public domain / Hogweard Ministry of Public Building and Works; cleaned up and labelled by Hchc2009 | 13/13 spans, 13/13 chars | 24 hatch/75 seg; 31 outline (61 fills) | [18325 B](../tek/v-denbigh-castle.tek) | 74.6% | G |
| `v-pinxton-castle` | [Pinxton Castle schematic plan.svg](https://commons.wikimedia.org/wiki/File%3APinxton_Castle_schematic_plan.svg) | CC BY-SA 4.0 / Odysseus1479 | 39/39 spans, 384/390 chars; 3 non-ASCII dropped | 2 hatch/20 seg; 3 outline; 1 stroke; 2 light skipped (8 fills) | [3986 B](../tek/v-pinxton-castle.tek) | 16.2% | M |

- **`v-acropolis-plan`** — Acropolis site plan; 36 labels, hatched hill crowds the centre (640×480 (not archived), device 480×640 (not archived))
- **`v-cordoba-hypostyle`** — Córdoba hypostyle hall plan with aisle labels (640×480 (not archived), device 480×640 (not archived))
- **`v-denbigh-castle`** — Denbigh Castle plan; wall hatching and numbered towers (640×480 (not archived), device 480×640 (not archived))
- **`v-pinxton-castle`** — Pinxton Castle schematic plan with roads, earthworks and a full legend (640×480 (not archived), device 480×640 (not archived))

## Anatomy — 4 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-brain-surface` | [Brain Surface Gyri.SVG](https://commons.wikimedia.org/wiki/File%3ABrain_Surface_Gyri.SVG) | CC BY-SA 4.0 / James.mcd.nz | 0 (no text layer) | 6 hatch/90 seg; 4 outline; 1 light skipped (11 fills) | [20845 B](../tek/v-brain-surface.tek) | 84.8% | G |
| `v-larynx` | [Larynx external en.svg](https://commons.wikimedia.org/wiki/File%3ALarynx_external_en.svg) | CC BY-SA 2.5 / Olek Remesz (wiki-pl: Orem, commons: Orem) | 22/22 spans, 332/332 chars | 46 hatch/292 seg; 52 outline; 1 stroke; 1 light skipped; 27 skipped (127 fills) | [19684 B](../tek/v-larynx.tek) | 80.1% | G |
| `v-skeleton-front` | [Human skeleton front en.svg](https://commons.wikimedia.org/wiki/File%3AHuman_skeleton_front_en.svg) | Public domain / LadyofHats Mariana Ruiz Villarreal | 31/34 spans, 236/267 chars | 11 outline; 51 stroke; 3 light skipped; 862 skipped (927 fills) | [24422 B](../tek/v-skeleton-front.tek) | 99.4% | G |
| `v-tooth` | [Human tooth diagram-en.svg](https://commons.wikimedia.org/wiki/File%3AHuman_tooth_diagram-en.svg) | CC BY-SA 4.0 / KDS4444 | 13/13 spans, 81/81 chars | 3 hatch/11 seg; 2 stroke; 2 light skipped; 549 skipped (556 fills) | [24441 B](../tek/v-tooth.tek) | 99.5% | G |

- **`v-brain-surface`** — Lateral brain surface with gyri; unlabelled but anatomically complete (640×480 (not archived), device 480×640 (not archived))
- **`v-larynx`** — Larynx antero-lateral view with muscle/cartilage labels (640×480 (not archived), device 480×640 (not archived))
- **`v-skeleton-front`** — Full skeleton with regional labels; 99.4% budget (640×480 (not archived), device 480×640 (not archived))
- **`v-tooth`** — Molar cross-section; enamel/dentin/pulp labels; 99.5% budget (640×480 (not archived), device 480×640 (not archived))

## Astronomy — 3 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-callisto` | [Callisto diagram.svg](https://commons.wikimedia.org/wiki/File%3ACallisto_diagram.svg) | CC BY-SA 3.0 / Kelvinsong | 15/24 spans, 141/168 chars | 6 hatch/285 seg; 19 outline; 26 skipped (51 fills) | [24431 B](../tek/v-callisto.tek) | 99.4% | G |
| `v-comet` | [Comet.svg](https://commons.wikimedia.org/wiki/File%3AComet.svg) | CC BY-SA 3.0 / Kelvinsong | 13/13 spans, 265/266 chars; 1 non-ASCII dropped | 11 hatch/285 seg; 89 outline; 75 skipped (175 fills) | [13503 B](../tek/v-comet.tek) | 54.9% | M |
| `v-moons-numbered` | [Moons of solar system numbered.svg](https://commons.wikimedia.org/wiki/File%3AMoons_of_solar_system_numbered.svg) | Public domain / NASA This SVG image was created by Medium69. Cette image SVG a été créée par Medium69. Please credit this : William Crochot | 35/35 spans, 87/87 chars | 17 hatch/300 seg; 15 outline; 265 skipped (297 fills) | [24402 B](../tek/v-moons-numbered.tek) | 99.3% | M |

- **`v-callisto`** — Callisto cutaway with ice/ocean layers and crater labels (640×480 (not archived), device 480×640 (not archived))
- **`v-comet`** — Comet anatomy (coma, nucleus, hydrogen envelope, dust tail); heavy hatching (640×480 (not archived), device 480×640 (not archived))
- **`v-moons-numbered`** — Moons to scale, numbered key; 35 labels, dense but readable (640×480 (not archived), device 480×640 (not archived))

## Biology — 4 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-boletus` | [Boletus-edulis-ramble.svg](https://commons.wikimedia.org/wiki/File%3ABoletus-edulis-ramble.svg) | Public domain / File:Rambles with nature students (Page 155): Brightwen, Eliza (author) derivative work: Jerimee | 0 (no text layer) | 30 hatch/300 seg; 40 outline; 1648 skipped (1718 fills) | [24431 B](../tek/v-boletus.tek) | 99.4% | G |
| `v-culex` | [Culex pipiens diagram en.svg](https://commons.wikimedia.org/wiki/File%3ACulex_pipiens_diagram_en.svg) | Public domain / Mariana Ruiz Villarreal LadyofHats | 48/48 spans, 333/333 chars | 43 hatch/265 seg; 4 outline; 23 stroke; 2 light skipped; 2 skipped (75 fills) | [23326 B](../tek/v-culex.tek) | 94.9% | G |
| `v-fish-organs` | [Internal organs of a fish.svg](https://commons.wikimedia.org/wiki/File%3AInternal_organs_of_a_fish.svg) | CC BY-SA 3.0 / Original: http://sharon-taxonomy2009-p3.wikispaces.com/ Sharon High School Vector: Pixelsquid🎱 | 23/23 spans, 175/175 chars | 7 hatch/44 seg; 38 outline; 6 stroke; 6 light skipped; 2 skipped (59 fills) | [22190 B](../tek/v-fish-organs.tek) | 90.3% | G |
| `v-housefly` | [Housefly anatomy-key.svg](https://commons.wikimedia.org/wiki/File%3AHousefly_anatomy-key.svg) | CC BY 3.0 / Original: User:Al2 Derivative work: Giancarlodessi Derivative work: Georg-Johann | 32/32 spans, 55/55 chars | 14 hatch/300 seg; 25 outline; 59 stroke; 1 light skipped; 87 skipped (186 fills) | [24042 B](../tek/v-housefly.tek) | 97.8% | G |

- **`v-boletus`** — Boletus edulis line engraving from an old natural-history book (640×480 (not archived), device 480×640 (not archived))
- **`v-culex`** — Culex pipiens anatomy; 48/48 labels placed (640×480 (not archived), device 480×640 (not archived))
- **`v-fish-organs`** — Fish internal organs; 23/23 labels placed (640×480 (not archived), device 480×640 (not archived))
- **`v-housefly`** — Housefly anatomy with 32 numbered callouts (640×480 (not archived), device 480×640 (not archived))

## Animals — 5 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-bird-pelvis` | [Bird pelvis.svg](https://commons.wikimedia.org/wiki/File%3ABird_pelvis.svg) | CC BY 2.5 / Squelette_oiseau.JPG: BIODIDAC Derivative work: mario modesto (talk) Derivative work №2: Sittaco (talk) | 3/3 spans, 3/3 chars | 2 outline; 98 light skipped; 4 skipped (104 fills) | [22198 B](../tek/v-bird-pelvis.tek) | 90.3% | G |
| `v-crab-anatomy` | [Fiddler crab anatomy-en.svg](https://commons.wikimedia.org/wiki/File%3AFiddler_crab_anatomy-en.svg) | CC BY-SA 3.0 / Christopher Thomas | 9/9 spans, 65/65 chars | 12 hatch/75 seg; 66 stroke (79 fills) | [9367 B](../tek/v-crab-anatomy.tek) | 38.1% | G |
| `v-dog-skeleton` | [Skeleton of a dog diagram ver.2.svg](https://commons.wikimedia.org/wiki/File%3ASkeleton_of_a_dog_diagram_ver.2.svg) | CC BY-SA 3.0 / Przemek Maksim If you use on your website or in your publication my images, you are obliged to give following details: - "Author:Przemek Maksim,-graphic name.svg from Wikimedia Commons (provide title of the work,provide the URL where the work is hosted),-license: (indicate the type of licence it is available under and provide a link to the licence)", on graphic and in graphic description in clear, visible and easy to read by human eye text. If you create a graphic that is based on graphics created by me, you are obliged to give following details: -"Based on Original graphic: graphic name.svg from Wikimedia Commons (provide the title of the work,provide the URL where the work is hosted),-Author: Przemek Maksim,-license: (indicate the type of licence it is available under and provide a link to the licence)",on graphic and in graphic description in clear, visible and easy to read by human eye text. For more information, write to my e-mail address:przemekmaksimgmail.com Jeśli używasz mojej grafiki jesteś zobowiązany podać nastepujace dane: -"Autor:Przemek Maksim (Poland),-nazwa grafiki.svg pochodzącej z Wikimedia Commons (jesteś zobowiazany do umieszczenia orginalnej nazwy grafiki oraz do podania adresu URL do danej grafiki),-licencja: (jesteś zobowiazany do umieszczenia licencji pod jaka grafika została opublikowana oraz do podania adresu URL do danej licencji)" na grafice oraz w jej opisie przy pomocy czcionki czytelnej,widocznej i łatwej do odczytania przez oko ludzkie. Jeżeli tworzysz grafikę bazująca na stworzonej przeze mnie pracy jesteś zobowiązany podać nastepujace dane: -"Utworzone na podstawie oryginalnej grafiki:nazwa grafiki.svg pochodzącej z Wikimedia Commons (jesteś zobowiazany do umieszczenia orginalnej nazwy grafiki oraz do podania adresu URL do danej grafiki),-Autor: Przemek Maksim, -licencja: (jesteś zobowiazany do umieszczenia licencji pod jaka grafika została opublikowana oraz do podania adresu URL do danej licencji)",na grafice oraz w jej opisie przy pomocy czcionki czytelnej,widocznej i łatwej do odczytania przez oko ludzkie. Jeśli chcesz uzyskać więcej informacji napisz na adres:przemekmaksimgmail.com | 36/36 spans, 53/53 chars | 9 hatch/195 seg; 37 stroke; 1 light skipped (47 fills) | [23941 B](../tek/v-dog-skeleton.tek) | 97.4% | G |
| `v-horse-anatomy` | [Horse anatomy.svg](https://commons.wikimedia.org/wiki/File%3AHorse_anatomy.svg) | CC BY-SA 3.0 / Wikipedian Prolific, vectorization process by Wilfredor | 0 (no text layer) | 11 hatch/44 seg; 2 outline; 84 stroke; 2 light skipped; 40 skipped (139 fills) | [24016 B](../tek/v-horse-anatomy.tek) | 97.7% | G |
| `v-squid-anatomy` | [Composite diagram illustrating basic squid features, ventral aspect.svg](https://commons.wikimedia.org/wiki/File%3AComposite_diagram_illustrating_basic_squid_features%2C_ventral_aspect.svg) | CC0 / Ruthven | 0 (no text layer) | 7 outline; 36 stroke (49 fills) | [21119 B](../tek/v-squid-anatomy.tek) | 85.9% | M |

- **`v-bird-pelvis`** — Bird pelvis (ilium/pubis/ischium) line drawing (640×480 (not archived), device 480×640 (not archived))
- **`v-crab-anatomy`** — Fiddler crab anatomy with carapace, cheliped and walking-leg labels (640×480 (not archived), device 480×640 (not archived))
- **`v-dog-skeleton`** — Dog skeleton, lateral view, 36 callouts; 97.4% budget (640×480 (not archived), device 480×640 (not archived))
- **`v-horse-anatomy`** — Horse skeleton and surface morphology, lateral view (640×480 (not archived), device 480×640 (not archived))
- **`v-squid-anatomy`** — Squid ventral anatomy; labels are vector outlines and too small to read (640×480 (not archived), device 480×640 (not archived))

## Plants — 3 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-gymnosperm` | [Gymnosperm life cycle diagram-en.svg](https://commons.wikimedia.org/wiki/File%3AGymnosperm_life_cycle_diagram-en.svg) | CC BY-SA 4.0 / SiliconProphet | 0 (no text layer) | 20 hatch/172 seg; 5 outline; 21 stroke; 4 light skipped; 888 skipped (938 fills) | [24448 B](../tek/v-gymnosperm.tek) | 99.5% | M |
| `v-leaf-structure` | [Leaf structure (labeled).svg](https://commons.wikimedia.org/wiki/File%3ALeaf_structure_%28labeled%29.svg) | CC BY-SA 4.0 / Melaaanyyy | 0 (no text layer) | 9 hatch/179 seg; 2 outline; 61 stroke; 259 skipped (331 fills) | [24445 B](../tek/v-leaf-structure.tek) | 99.5% | G |
| `v-viola-flower` | [Viola flower diagram.svg](https://commons.wikimedia.org/wiki/File%3AViola_flower_diagram.svg) | CC0 / Afanasovich | 0 (no text layer) | 5 hatch/28 seg; 7 outline; 11 stroke (23 fills) | [11894 B](../tek/v-viola-flower.tek) | 48.4% | G |

- **`v-gymnosperm`** — Gymnosperm life cycle; labels are vector outlines, no text layer (640×480 (not archived), device 480×640 (not archived))
- **`v-leaf-structure`** — Leaf cross-section with epidermis, mesophyll and vascular bundle (640×480 (not archived), device 480×640 (not archived))
- **`v-viola-flower`** — Viola floral diagram: petals, stamens and pistil in plan (640×480 (not archived), device 480×640 (not archived))

## Aerospace — 12 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-falcon-family` | [Falcon rocket family5.svg](https://commons.wikimedia.org/wiki/File%3AFalcon_rocket_family5.svg) | CC BY-SA 4.0 / Lucabon (based on work of Markus Säynevirta and Craigboy and Rressi ) | 0 (no text layer) | 5 hatch/111 seg; 2 outline; 29 stroke; 21 light skipped; 729 skipped (786 fills) | [24442 B](../tek/v-falcon-family.tek) | 99.5% | G |
| `v-mir-shuttle` | [Mir-Shuttle diagram.svg](https://commons.wikimedia.org/wiki/File%3AMir-Shuttle_diagram.svg) | CC BY-SA 3.0 / Orionist | 16/16 spans, 100/103 chars; 3 non-ASCII dropped | 1 hatch/1 seg; 2 outline; 30 stroke; 23 light skipped; 264 skipped (320 fills) | [24447 B](../tek/v-mir-shuttle.tek) | 99.5% | G |
| `v-saturn-v` | [Saturn V - launch tower.svg](https://commons.wikimedia.org/wiki/File%3ASaturn_V_-_launch_tower.svg) | CC0 / charner1963 | 0 (no text layer) | 2 outline; 86 stroke; 2 light skipped; 2016 skipped (2106 fills) | [24443 B](../tek/v-saturn-v.tek) | 99.5% | G |
| `v-shuttle-orbiter` | [RP1357 p182 Space Shuttle Orbiter.svg](https://commons.wikimedia.org/wiki/File%3ARP1357_p182_Space_Shuttle_Orbiter.svg) | Public domain / David S. F. Portree / NASA | 0 (no text layer) | 4 hatch/64 seg; 1 outline; 46 stroke; 61 skipped (112 fills) | [24439 B](../tek/v-shuttle-orbiter.tek) | 99.4% | G |

- **`v-falcon-family`** — Falcon 1/9/Heavy family to scale with payload fairings (640×480 (not archived), device 480×640 (not archived))
- **`v-mir-shuttle`** — Mir-Shuttle docking configuration diagram; 16 labels (640×480 (not archived), device 480×640 (not archived))
- **`v-saturn-v`** — Saturn V on the launch tower, full vehicle and tower line art (640×480 (not archived), device 480×640 (not archived))
- **`v-shuttle-orbiter`** — Space Shuttle orbiter three-quarter line drawing (640×480 (not archived), device 480×640 (not archived))

### Satellite / probe expansion (P5) — 4 pages

The P5 batch adds the satellite/probe layer the earlier set lacked. All four
sources are native SVG line art, have a live text layer (so Tek alpha can place
the callouts), and are NASA-derived public domain. `--fills outline` is used on
every P5 page so no fill is converted to hatch; the ISS and Pioneer pages use
`--max-fills 1000` so `skipped_cap` is zero rather than truncating fills.

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-iss` | [ISS configuration 2016-08 en.svg](https://commons.wikimedia.org/wiki/File%3AISS_configuration_2016-08_en.svg) | Public domain / NASA and Wikimedia editors (Ras67, Colds7ream, Fritzbox, Johndrinkwater); derivative work: Voteins | 89/98 spans, 845/936 chars; 9 small labels dropped, 2 chars truncated, 1 non-ASCII dropped | 0 hatch; 1 outline; 505 stroke; 34 tiny skipped (540 fills) | [23353 B](../tek/v-iss.tek) | 95.0% | G |
| `v-mars-rover` | [Mars Exploration Rover.svg](https://commons.wikimedia.org/wiki/File%3AMars_Exploration_Rover.svg) | Public domain / NASA/JPL; derivative work: FischX | 22/22 spans, 285/286 chars; 1 non-ASCII dropped | none (126 white fills ignored) | [21609 B](../tek/v-mars-rover.tek) | 87.9% | G |
| `v-ranger` | [Ranger 6789.svg](https://commons.wikimedia.org/wiki/File%3ARanger_6789.svg) | Public domain / NASA History; derivative work: Malyszkz | 20/20 spans, 256/256 chars | none (99 tiny fills skipped) | [15314 B](../tek/v-ranger.tek) | 62.3% | G |
| `v-pioneer-10` | [Pioneer 10 systems diagram.svg](https://commons.wikimedia.org/wiki/File%3APioneer_10_systems_diagram.svg) | Public domain / NASA; vectors by Mysid | 15/15 spans, 311/312 chars; 1 non-ASCII (en dash) dropped | 37 outline; 108 stroke; 53 light skipped; 1 tiny; 23 white ignored (199 fills) | [17334 B](../tek/v-pioneer-10.tek) | 70.5% | M |

- **`v-iss`** — ISS 2016-08 configuration; 89 callouts and the orbit/pending legend, solar arrays left as outlines (640×480 (not archived), device 480×640 (not archived))
- **`v-mars-rover`** — Mars Exploration Rover schematic; all 22 callouts, pure stroke art, no fills (640×480 (not archived), device 480×640 (not archived))
- **`v-ranger`** — Ranger 6-9 lunar probe; all 20 callouts (640×480 (not archived), device 480×640 (not archived))
- **`v-pioneer-10`** — Pioneer 10 systems diagram; 15 callouts; full-page crop keeps the right-hand labels. M: `Ultraviolet Photometer` runs under the boom (640×480 (not archived), device 480×640 (not archived))

The planned `v-htv` page is not shipped: HTV's labels are vector outlines, and
at 99.5% budget the glyph strokes are compressed away, leaving single letters
(see the skip table). `v-ranger`/`v-pioneer-10` fill the probe slot instead.

### Spacecraft / stations / telescope expansion (P5b) — 4 pages

P5b widens the same layer to a Soyuz cutaway, an ISS component exploded view,
the Mir station and a Hubble exploded view. All four are native SVG; text is
live `<text>` in every source, so the callouts survive as Tek alpha. Every
page uses `--fills outline --max-fills 1000`, so `hatch=0` and `skipped_cap=0`.
`v-hubble` is the retry of the earlier rejected page; it is kept as M because
7 characters still clip at the right edge (see below). `v-mars-odyssey` was
retried with the same no-hatch/no-cap settings but remains rejected (11 chars
clip, 99.5% budget).

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-soyuz` | [Soyuz Diagram.svg](https://commons.wikimedia.org/wiki/File%3ASoyuz_Diagram.svg) | Public domain / NASA MSFC; anonymous SVG conversion | 63/66 spans, 743/746 chars; 3 one-char spans dropped by overlap | 101 outline; 1 tiny (102 fills); 0 hatch | [7393 B](../tek/v-soyuz.tek) | 30.1% | G |
| `v-iss-components` | [ISS components.svg](https://commons.wikimedia.org/wiki/File%3AISS_components.svg) | Public domain / NASA | 95/95 spans, 930/930 chars | 5 outline; 144 stroke; 38 tiny; 420 white ignored (193 fills) | [24441 B](../tek/v-iss-components.tek) | 99.5% | G |
| `v-mir` | [Mir diagram.svg](https://commons.wikimedia.org/wiki/File%3AMir_diagram.svg) | CC BY-SA 3.0 / Orionist | 15/15 spans, 90/90 chars | 2 outline; 112 stroke; 12 tiny; 12 white (248 fills) | [24448 B](../tek/v-mir.tek) | 99.5% | G |
| `v-hubble` | [HubbleExploded.svg](https://commons.wikimedia.org/wiki/File%3AHubbleExploded.svg) | CC BY-SA 3.0 / AndrewBuck | 39/39 spans, 655/662 chars; 7 chars truncated at the right edge | none (strokes only) | [9629 B](../tek/v-hubble.tek) | 39.2% | M |

- **`v-soyuz`** — Soyuz orbital/descent module cutaway; all 21 legend entries and the brine loop labels (640×480 (not archived), device 480×640 (not archived))
- **`v-iss-components`** — ISS component exploded view by partner nation; 95 labels, 99.5% budget (640×480 (not archived), device 480×640 (not archived))
- **`v-mir`** — Mir after Priroda with Progress-M and Soyuz-TM docked; 15 module labels (640×480 (not archived), device 480×640 (not archived))
- **`v-hubble`** — Hubble exploded view; 39 labels, right-edge truncation is the only M defect (640×480 (not archived), device 480×640 (not archived))



## CAD / mechanical cutaway — 5 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-bulova` | [Bulova Accutron movement fr.svg](https://commons.wikimedia.org/wiki/File%3ABulova_Accutron_movement_fr.svg) | CC BY-SA 4.0 / Raminagrobis | 16/16 spans, 115/116 chars; 1 non-ASCII dropped | 2 hatch/18 seg; 3 stroke (5 fills) | [3415 B](../tek/v-bulova.tek) | 13.9% | G |
| `v-milling` | [Milling machine diagram.svg](https://commons.wikimedia.org/wiki/File%3AMilling_machine_diagram.svg) | CC BY-SA 4.0 / HUB1 | 5/5 spans, 5/5 chars | 8 hatch/144 seg; 9 stroke; 4 light skipped (21 fills) | [3454 B](../tek/v-milling.tek) | 14.1% | M |
| `v-pin-tumbler` | [Pin tumbler with key.svg](https://commons.wikimedia.org/wiki/File%3APin_tumbler_with_key.svg) | CC BY-SA 3.0 / Original: Wapcaplet Vector: Pbroks13 | 0 (no text layer) | 7 hatch/291 seg; 23 outline; 34 skipped (64 fills) | [24439 B](../tek/v-pin-tumbler.tek) | 99.4% | G |
| `v-reflex-camera` | [Reflex camera (description).svg](https://commons.wikimedia.org/wiki/File%3AReflex_camera_%28description%29.svg) | CC BY-SA 3.0 / Anuskafm | 0 (no text layer) | 2 hatch/69 seg; 93 stroke; 243 skipped (338 fills) | [24398 B](../tek/v-reflex-camera.tek) | 99.3% | G |
| `v-stirling` | [BetaStirlingTG4web.svg](https://commons.wikimedia.org/wiki/File%3ABetaStirlingTG4web.svg) | CC BY-SA 3.0 / BetaStirlingTG4web.jpg: Togo derivative work: Ionutzmovie (talk) | 0 (no text layer) | 21 hatch/300 seg; 78 outline; 1 light skipped; 1444 skipped (1544 fills) | [18317 B](../tek/v-stirling.tek) | 74.5% | G |

- **`v-bulova`** — Bulova Accutron tuning-fork movement; French labels readable (640×480 (not archived), device 480×640 (not archived))
- **`v-milling`** — Horizontal milling machine schematic with five numbered parts (640×480 (not archived), device 480×640 (not archived))
- **`v-pin-tumbler`** — Pin-tumbler lock cutaway with key and driver pins (640×480 (not archived), device 480×640 (not archived))
- **`v-reflex-camera`** — SLR camera cross-section; lens, mirror, prism and film path (640×480 (not archived), device 480×640 (not archived))
- **`v-stirling`** — Beta Stirling engine cutaway; heater, regenerator and displacer visible (640×480 (not archived), device 480×640 (not archived))

## Electronics / PCB — 5 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-alu-74181` | [74181aluschematic.svg](https://commons.wikimedia.org/wiki/File%3A74181aluschematic.svg) | CC BY-SA 4.0 / CrowbarBarbarian | 32/36 spans, 35/43 chars | 84 outline (84 fills) | [22117 B](../tek/v-alu-74181.tek) | 90.0% | G |
| `v-pc-psu` | [PC-PowerSupply-Principle-Circuit.svg](https://commons.wikimedia.org/wiki/File%3APC-PowerSupply-Principle-Circuit.svg) | CC BY-SA 3.0 / Hans Haase | 28/29 spans, 104/108 chars; 3 non-ASCII dropped | 6 hatch/25 seg; 64 stroke; 15 light skipped (85 fills) | [20292 B](../tek/v-pc-psu.tek) | 82.6% | G |
| `v-pentium-pro` | [Intel Pentium Pro Microarchitecture Block Diagram.svg](https://commons.wikimedia.org/wiki/File%3AIntel_Pentium_Pro_Microarchitecture_Block_Diagram.svg) | CC0 / NoahSPARC | 31/32 spans, 312/326 chars | 39 hatch/52 seg; 31 stroke (70 fills) | [3927 B](../tek/v-pentium-pro.tek) | 16.0% | G |
| `v-regen-radio` | [Armstrong regenerative receiver circuit.svg](https://commons.wikimedia.org/wiki/File%3AArmstrong_regenerative_receiver_circuit.svg) | CC0 / Chetvorno | 18/18 spans, 60/60 chars | 8 hatch/17 seg (8 fills) | [4065 B](../tek/v-regen-radio.tek) | 16.5% | G |
| `v-rpi-pcb` | [Raspberrypi pcb overview Pinout v01.svg](https://commons.wikimedia.org/wiki/File%3ARaspberrypi_pcb_overview_Pinout_v01.svg) | CC BY-SA 3.0 / TimGremalm | 40/42 spans, 236/251 chars | 49 hatch/273 seg; 34 outline; 9 stroke; 8 light skipped; 80 skipped (180 fills) | [14564 B](../tek/v-rpi-pcb.tek) | 59.3% | G |

- **`v-alu-74181`** — 74181 4-bit ALU transistor-level schematic; 32 labels (640×480 (not archived), device 480×640 (not archived))
- **`v-pc-psu`** — PC power-supply principle circuit; 28/29 labels placed (640×480 (not archived), device 480×640 (not archived))
- **`v-pentium-pro`** — Pentium Pro microarchitecture block diagram; 31 labels (640×480 (not archived), device 480×640 (not archived))
- **`v-regen-radio`** — Armstrong regenerative receiver: one vacuum tube, tickler coil and phones (640×480 (not archived), device 480×640 (not archived))
- **`v-rpi-pcb`** — Raspberry Pi PCB overview with connector and component callouts (640×480 (not archived), device 480×640 (not archived))

## Mathematics / geometry — 4 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-iron-phase` | [Pure iron phase diagram (EN).svg](https://commons.wikimedia.org/wiki/File%3APure_iron_phase_diagram_%28EN%29.svg) | CC BY-SA 3.0 / Diagramma_di_fase_del_ferro_puro.svg: Daniele Pugliesi derivative work: Daniele Pugliesi (talk) | 30/30 spans, 125/129 chars; 4 non-ASCII dropped | 6 hatch/70 seg; 4 outline (10 fills) | [2133 B](../tek/v-iron-phase.tek) | 8.7% | M |
| `v-klein-bottle` | [KleinBottle-01.svg](https://commons.wikimedia.org/wiki/File%3AKleinBottle-01.svg) | CC BY-SA 3.0 / Krishnavedala | 0 (no text layer) | 13 hatch/90 seg; 2 outline; 885 skipped (900 fills) | [24446 B](../tek/v-klein-bottle.tek) | 99.5% | G |
| `v-pipe-knot` | [Pipe-knot-s.svg](https://commons.wikimedia.org/wiki/File%3APipe-knot-s.svg) | CC BY-SA 4.0 / Ag2gaeh | 0 (no text layer) | none | [21766 B](../tek/v-pipe-knot.tek) | 88.6% | G |
| `v-platonic` | [Platonic Solids Transparent.svg](https://commons.wikimedia.org/wiki/File%3APlatonic_Solids_Transparent.svg) | CC0 / Drummyfish | 0 (no text layer) | 8 hatch/97 seg; 39 outline; 3 light skipped (50 fills) | [3021 B](../tek/v-platonic.tek) | 12.3% | G |

- **`v-iron-phase`** — Pure-iron pressure-temperature phase diagram; vapor/liquid/BCC/FCC (640×480 (not archived), device 480×640 (not archived))
- **`v-klein-bottle`** — Klein bottle immersion as a wireframe surface (640×480 (not archived), device 480×640 (not archived))
- **`v-pipe-knot`** — Tube-knot surface; 1,977-path wireframe knot (640×480 (not archived), device 480×640 (not archived))
- **`v-platonic`** — The five Platonic solids as transparent wireframes (640×480 (not archived), device 480×640 (not archived))

## Paleontology — 3 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-ammonite` | [Very ridged ammonite shell.svg](https://commons.wikimedia.org/wiki/File%3AVery_ridged_ammonite_shell.svg) | CC BY-SA 4.0 / Unknown Commons contributor | 0 (no text layer) | 60 light skipped (60 fills) | [14827 B](../tek/v-ammonite.tek) | 60.3% | G |
| `v-trex` | [T. rex skeleton.svg](https://commons.wikimedia.org/wiki/File%3AT._rex_skeleton.svg) | Public domain / American Museum Journal | 0 (no text layer) | 1 outline (1 fills) | [10620 B](../tek/v-trex.tek) | 43.2% | G |
| `v-trilobite` | [Trilobites main morphological groups.svg](https://commons.wikimedia.org/wiki/File%3ATrilobites_main_morphological_groups.svg) | CC0 / Sam Gon III, derivative by Obsidian Soul | 6/6 spans, 6/6 chars | 12 outline; 5 stroke; 1 light skipped; 159 skipped (177 fills) | [24437 B](../tek/v-trilobite.tek) | 99.4% | G |

- **`v-ammonite`** — Ridged ammonite shell, spiral suture line art (640×480 (not archived), device 480×640 (not archived))
- **`v-trex`** — Tyrannosaurus rex skeleton, American Museum mount line art (640×480 (not archived), device 480×640 (not archived))
- **`v-trilobite`** — Trilobite dorsal and ventral morphology with numbered callouts (640×480 (not archived), device 480×640 (not archived))

## Chemistry / crystals — 5 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-ammonium-phase` | [Ammonium nitrate water phase diagram.svg](https://commons.wikimedia.org/wiki/File%3AAmmonium_nitrate_water_phase_diagram.svg) | Public domain / Steffen 962 | 32/32 spans, 69/70 chars; 1 non-ASCII dropped | none | [24313 B](../tek/v-ammonium-phase.tek) | 98.9% | M |
| `v-bravais` | [Bravais lattices.svg](https://commons.wikimedia.org/wiki/File%3ABravais_lattices.svg) | CC BY-SA 3.0 / Napy1kenobi | 14/14 spans, 47/47 chars | 100 hatch/121 seg; 46 skipped (146 fills) | [3956 B](../tek/v-bravais.tek) | 16.1% | G |
| `v-dcd-mo` | [DCD-Model-MO-diagram-part-1.svg](https://commons.wikimedia.org/wiki/File%3ADCD-Model-MO-diagram-part-1.svg) | CC BY-SA 4.0 / Johannes Schneider | 8/8 spans, 24/24 chars | 15 hatch/32 seg; 5 outline; 32 stroke (54 fills) | [4322 B](../tek/v-dcd-mo.tek) | 17.6% | M |
| `v-dna` | [DNA chemical structure 2.svg](https://commons.wikimedia.org/wiki/File%3ADNA_chemical_structure_2.svg) | CC BY 4.0 / Thomas Shafee | 0 (no text layer) | 34 hatch/248 seg; 5 outline; 3 stroke; 3 skipped (45 fills) | [17517 B](../tek/v-dna.tek) | 71.3% | G |
| `v-steel-pd` | [Steel pd.svg](https://commons.wikimedia.org/wiki/File%3ASteel_pd.svg) | CC BY-SA 3.0 / The original uploader was User A1 at English Wikipedia. | 0 (no text layer) | 4 hatch/180 seg; 2 outline; 78 stroke; 119 skipped (203 fills) | [24440 B](../tek/v-steel-pd.tek) | 99.4% | G |

- **`v-ammonium-phase`** — Ammonium-nitrate/water phase diagram; grid-heavy but labelled I-IV (640×480 (not archived), device 480×640 (not archived))
- **`v-bravais`** — The 14 Bravais lattices, numbered (1)-(14) (640×480 (not archived), device 480×640 (not archived))
- **`v-dcd-mo`** — DCD molecular-orbital diagram; 8 labels, sparse but readable (640×480 (not archived), device 480×640 (not archived))
- **`v-dna`** — DNA chemical structure: sugar-phosphate backbone and A/T/G/C pairs (640×480 (not archived), device 480×640 (not archived))
- **`v-steel-pd`** — Iron-carbon phase diagram: ferrite, austenite, cementite, ledeburite (640×480 (not archived), device 480×640 (not archived))

## Design / typography — 4 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-antiquarian` | [Typeface specimen Antiquarian.svg](https://commons.wikimedia.org/wiki/File%3ATypeface_specimen_Antiquarian.svg) | CC BY-SA 4.0 / ZoeB | 0 (no text layer) | 48 hatch/251 seg; 13 outline (61 fills) | [6647 B](../tek/v-antiquarian.tek) | 27.0% | M |
| `v-comic-mono` | [Font-sample-comicmono.svg](https://commons.wikimedia.org/wiki/File%3AFont-sample-comicmono.svg) | CC BY-SA 4.0 / Cormullion | 0 (no text layer) | 23 hatch/299 seg; 35 outline (58 fills) | [9720 B](../tek/v-comic-mono.tek) | 39.6% | G |
| `v-css-grid` | [CSS grid grid-areas.svg](https://commons.wikimedia.org/wiki/File%3ACSS_grid_grid-areas.svg) | CC BY-SA 4.0 / Hunsvotti | 19/51 spans, 27/102 chars; 1 non-ASCII dropped | 11 hatch/297 seg; 5 outline; 81 stroke; 1 light skipped (98 fills) | [11542 B](../tek/v-css-grid.tek) | 47.0% | M |
| `v-junicode` | [Junicode-2207-specimen.svg](https://commons.wikimedia.org/wiki/File%3AJunicode-2207-specimen.svg) | CC0 / SCLu | 0 (no text layer) | 5 hatch/244 seg; 4 outline (9 fills) | [8677 B](../tek/v-junicode.tek) | 35.3% | G |

- **`v-antiquarian`** — Antiquarian typeface specimen; display line readable, small text distorted (640×480 (not archived), device 480×640 (not archived))
- **`v-comic-mono`** — Comic Mono specimen: Handgloves, alphabet and digits (640×480 (not archived), device 480×640 (not archived))
- **`v-css-grid`** — CSS-grid poster layout; 19/51 labels placed, boxes and areas clear (640×480 (not archived), device 480×640 (not archived))
- **`v-junicode`** — Junicode specimen: regular, italic and lowercase alphabet (640×480 (not archived), device 480×640 (not archived))

## System anatomy / plants — 3 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-ear-intl` | [Anatomy of the Human Ear 1 Intl.svg](https://commons.wikimedia.org/wiki/File%3AAnatomy_of_the_Human_Ear_1_Intl.svg) | CC BY-SA 3.0 / Jmarchn | 23/23 spans, 37/37 chars | 15 hatch/265 seg; 19 outline; 4 light skipped (39 fills) | [20596 B](../tek/v-ear-intl.tek) | 83.8% | G |
| `v-nervous` | [Nervous system diagram-en.svg](https://commons.wikimedia.org/wiki/File%3ANervous_system_diagram-en.svg) | CC BY-SA 4.0 / Medium69, Jmarchn | 38/67 spans, 397/429 chars | 6 hatch/54 seg; 2 outline; 2 stroke; 4 light skipped (14 fills) | [20551 B](../tek/v-nervous.tek) | 83.6% | G |
| `v-respiratory-cruk` | [Diagram showing the parts of the respiratory system CRUK 335.svg](https://commons.wikimedia.org/wiki/File%3ADiagram_showing_the_parts_of_the_respiratory_system_CRUK_335.svg) | CC BY-SA 4.0 / Cancer Research UK | 5/5 spans, 80/80 chars | 33 outline; 9 stroke; 58 light skipped; 145 skipped (245 fills) | [14938 B](../tek/v-respiratory-cruk.tek) | 60.8% | G |

- **`v-ear-intl`** — Human ear cross-section, 23 numbered labels (640×480 (not archived), device 480×640 (not archived))
- **`v-nervous`** — Human nervous system with CNS, plexuses and named nerves (640×480 (not archived), device 480×640 (not archived))
- **`v-respiratory-cruk`** — Respiratory system: trachea, bronchi and lung lobes (640×480 (not archived), device 480×640 (not archived))

## Patent line art — 2 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-buckling-spring` | [IBM buckling spring.svg](https://commons.wikimedia.org/wiki/File%3AIBM_buckling_spring.svg) | Public domain / Inventor: Richard Hunter Harris | 71/71 spans, 115/119 chars; 4 non-ASCII dropped | 16 hatch/300 seg; 16 outline (32 fills) | [20955 B](../tek/v-buckling-spring.tek) | 85.3% | G |
| `v-z2` | [Drawing of Z2-de.svg](https://commons.wikimedia.org/wiki/File%3ADrawing_of_Z2-de.svg) | CC0 / Own work, original patent by Konrad Zuse | 50/50 spans, 422/445 chars; 6 non-ASCII dropped | 1 hatch/20 seg (1 fills) | [11471 B](../tek/v-z2.tek) | 46.7% | G |

- **`v-buckling-spring`** — IBM buckling-spring key mechanism, four patent figures with callouts (640×480 (not archived), device 480×640 (not archived))
- **`v-z2`** — Zuse Z2 computer patent-style drawing; 50 labels, 422 chars (640×480 (not archived), device 480×640 (not archived))

## Maps (Natural Earth) — 1 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-ne-world` | [Natural Earth 50m coastline (world, two hemispheres)](https://www.naturalearthdata.com/downloads/50m-physical-vectors/50m-coastline/) | Public domain / Natural Earth | 0 (no text layer) | none (strokes only) | [23931 B](../tek/v-ne-world.tek) | 97.4% | G |

- **`v-ne-world`** — Natural Earth 50m coastline in two orthographic hemispheres (west/east) with a 30-degree graticule (640×480 (not archived), device 480×640 (not archived))

## CAD / PCB / design — 3 pages

| id | source | license / author | text | fill | `.tek` | budget | Q |
|---|---|---|---|---|---:|---:|---|
| `v-pc-exploded` | [Personal computer, exploded 4.svg](https://commons.wikimedia.org/wiki/File%3APersonal_computer%2C_exploded_4.svg) | CC BY 2.5 / Gustavb | 0 (no text layer) | 10 hatch/300 seg; 58 outline; 18 stroke; 14 light skipped; 929 skipped (1029 fills) | [14682 B](../tek/v-pc-exploded.tek) | 59.7% | M |
| `v-steel-detail` | [Stahldetail JoKalliauer.svg](https://commons.wikimedia.org/wiki/File%3AStahldetail_JoKalliauer.svg) | CC BY-SA 4.0 / Johannes Kalliauer | 23/24 spans, 179/183 chars | 4 hatch/9 seg; 16 outline (20 fills) | [11170 B](../tek/v-steel-detail.tek) | 45.5% | M |
| `v-transmitter-pcb-crop` | [TransmitterFM-Copper.svg](https://commons.wikimedia.org/wiki/File%3ATransmitterFM-Copper.svg) | Public domain / Sismanconstant | 0 (no text layer) | 58 hatch/186 seg; 2 stroke (60 fills) | [6701 B](../tek/v-transmitter-pcb-crop.tek) | 27.3% | M |

- **`v-pc-exploded`** — Exploded desktop computer; components read without labels (640×480 (not archived), device 480×640 (not archived))
- **`v-steel-detail`** — Steel connection detail with dimensions and 23 labels (640×480 (not archived), device 480×640 (not archived))
- **`v-transmitter-pcb-crop`** — FM transmitter PCB copper layer, cropped to the board; 58 hatched pads/traces (640×480 (not archived), device 480×640 (not archived))

## Skipped candidates

Each row was downloaded and measured; the reason is the measurement, not a preference.

| id | subject | source | skip reason |
|---|---|---|---|
| `v-bayern` | ships | [SMS Bayern armor front view.svg](https://commons.wikimedia.org/wiki/File%3ASMS_Bayern_armor_front_view.svg) | PyMuPDF returns no vector paths; the SVG is raster-only. |
| `v-i400` | ships | [I-400 class deck compartment plan.svg](https://commons.wikimedia.org/wiki/File%3AI-400_class_deck_compartment_plan.svg) | Good hull art, but 0/15 spans (44 chars) placed: the Japanese callouts are lost. |
| `v-derrick` | ships | [Derrick1.svg](https://commons.wikimedia.org/wiki/File%3ADerrick1.svg) | Clean marine derrick scheme but only 5 label chars; held back as too sparse. |
| `v-verge-foliot` | instr | [Verge and foliot from De Vick's clock.svg](https://commons.wikimedia.org/wiki/File%3AVerge_and_foliot_from_De_Vick%27s_clock.svg) | CSS-only styling: 4-byte page. |
| `v-fuller` | instr | [Fuller's calculator annotated.svg](https://commons.wikimedia.org/wiki/File%3AFuller%27s_calculator_annotated.svg) | 565-byte page: the calculator body is a bitmap/pattern, only labels survive. |
| `v-camera-obscura` | instr | [Distance effect on camera obscura.svg](https://commons.wikimedia.org/wiki/File%3ADistance_effect_on_camera_obscura.svg) | Raster-only: no vector paths. |
| `v-telescope-mirrors` | instr | [Comparison optical telescope primary mirrors.svg](https://commons.wikimedia.org/wiki/File%3AComparison_optical_telescope_primary_mirrors.svg) | A single hatched disc with a tiny label; icon-grade simplification. |
| `v-theodolite` | instr | [Theodolite vermeer.svg](https://commons.wikimedia.org/wiki/File%3ATheodolite_vermeer.svg) | Schematic of the instrument axes; reads as hatched discs rather than a recognizable theodolite, so the clock escapement was kept instead. |
| `v-circular-slide-rule` | instr | [Circular slide rule diagram svg.svg](https://commons.wikimedia.org/wiki/File%3ACircular_slide_rule_diagram_svg.svg) | Scale labels are vector outlines that fall below the Tek text path; dial reads blank. |
| `v-howe-press` | mech | [J. Howe & Co. printing press, 1830.svg](https://commons.wikimedia.org/wiki/File%3AJ._Howe_%26_Co._printing_press%2C_1830.svg) | CSS-only styling: 4-byte page. |
| `v-bulleid` | mech | [Bulleid chain valve gear.svg](https://commons.wikimedia.org/wiki/File%3ABulleid_chain_valve_gear.svg) | Raster-only: no vector paths. |
| `v-blast-furnace` | mech | [Blast furnace 2.svg](https://commons.wikimedia.org/wiki/File%3ABlast_furnace_2.svg) | Raster-only: no vector paths. |
| `v-breastshot` | mech | [Breastshot water wheel schematic de.svg](https://commons.wikimedia.org/wiki/File%3ABreastshot_water_wheel_schematic_de.svg) | 198-byte page: the wheel is a pattern fill, only eight labels survive. |
| `v-haut-fourneau` | mech | [Haut fourneau Cuve auto-portée Gueulard fermé.svg](https://commons.wikimedia.org/wiki/File%3AHaut_fourneau_Cuve_auto-port%C3%A9e_Gueulard_ferm%C3%A9.svg) | Five furnace silhouettes, 0 labels, 6.6 KB: too sparse for a page. |
| `v-gozgep` | mech | [Gőzgép.svg](https://commons.wikimedia.org/wiki/File%3AG%C5%91zg%C3%A9p.svg) | Only the indicator diagram survives (4.1 KB, 2 chars); the engine art is lost. |
| `v-barn-sketches` | arch | [Barn sketches1.svg](https://commons.wikimedia.org/wiki/File%3ABarn_sketches1.svg) | Raster-only: no vector paths. |
| `v-tono-house` | arch | [Rayout of traditional house in Tōno 001.svg](https://commons.wikimedia.org/wiki/File%3ARayout_of_traditional_house_in_T%C5%8Dno_001.svg) | Japanese labels are lost (0/1 span); the plan reads as unlabelled boxes. |
| `v-cordoba-doors` | arch | [Doors of the Mosque-Cathedral of Córdoba.svg](https://commons.wikimedia.org/wiki/File%3ADoors_of_the_Mosque-Cathedral_of_C%C3%B3rdoba.svg) | Second Toledano Córdoba plate; the series cap (2) is used by the hypostyle page. |
| `v-aqueduct` | arch | [Pont-aqueduc en opus reticulatum inspiré de l'aqueduc du Gier.svg](https://commons.wikimedia.org/wiki/File%3APont-aqueduc_en_opus_reticulatum_inspir%C3%A9_de_l%27aqueduc_du_Gier.svg) | Wide arcade elevation: 90% of the budget but the figure is a thin strip with large blank margins; Pinxton Castle plan kept instead. |
| `v-cromwell-castle` | arch | [Cromwell's Castle plan with roof.svg](https://commons.wikimedia.org/wiki/File%3ACromwell%27s_Castle_plan_with_roof.svg) | 99.4% budget with only four labels; the plan hatching crowds the page. |
| `v-hydra-chart` | astro | [Celestial map Hya.svg](https://commons.wikimedia.org/wiki/File%3ACelestial_map_Hya.svg) | 1,708 constellation strokes, 0 text: labels are unreadable hairlines at panel size. |
| `v-somofijahr` | astro | [SoMoFiJahr.svg](https://commons.wikimedia.org/wiki/File%3ASoMoFiJahr.svg) | Calendar construction with 1,928 drawings and no placed text; the ring labels vanish. |
| `v-comet-structure` | astro | [Comet Physical Structure.svg](https://commons.wikimedia.org/wiki/File%3AComet_Physical_Structure.svg) | 4.2 KB, seven label chars; the comet is reduced to a hatched disc. |
| `v-comet-parts` | astro | [Comet Parts.svg](https://commons.wikimedia.org/wiki/File%3AComet_Parts.svg) | Resolves to an embedded raster image; no vector paths. |
| `v-moon-phases` | astro | [Phases of the Moon.svg](https://commons.wikimedia.org/wiki/File%3APhases_of_the_Moon.svg) | 3/29 spans (3/189 chars) placed: the phase labels are lost. |
| `v-lunar-eclipse` | astro | [Lunar eclipse diagram-en.svg](https://commons.wikimedia.org/wiki/File%3ALunar_eclipse_diagram-en.svg) | 5.8 KB, four hatched discs and two boxes, no labels: too simple. |
| `v-nephron` | anat | [Nephron (NIH BioArt 560).svg](https://commons.wikimedia.org/wiki/File%3ANephron_%28NIH_BioArt_560%29.svg) | Beautiful nephron art but 0/57 spans (507 chars): all labels are lost. |
| `v-eye-202011` | anat | [202011 Eye.svg](https://commons.wikimedia.org/wiki/File%3A202011_Eye.svg) | Raster-only: no vector paths. |
| `v-heart-surface` | anat | [Surface anatomy of the heart.svg](https://commons.wikimedia.org/wiki/File%3ASurface_anatomy_of_the_heart.svg) | Only the rib cage survives; the heart itself and labels are absent. |
| `v-skeleton` | anat | [Skeleton diagram.svg](https://commons.wikimedia.org/wiki/File%3ASkeleton_diagram.svg) | CSS-only styling: 4-byte page. |
| `v-schuko` | pat | [SCHUKO-Patent.svg](https://commons.wikimedia.org/wiki/File%3ASCHUKO-Patent.svg) | CSS-only styling: 4-byte page. |
| `v-anderson-1897` | pat | [George Kerr Anderson Patent 1897 1.svg](https://commons.wikimedia.org/wiki/File%3AGeorge_Kerr_Anderson_Patent_1897_1.svg) | Fragmented sub-drawings and labels; the machine does not read as one figure. |
| `v-anderson-1889` | pat | [George Kerr Anderson Patent 1889 1.svg](https://commons.wikimedia.org/wiki/File%3AGeorge_Kerr_Anderson_Patent_1889_1.svg) | 4 KB of scattered small parts; no coherent patent figure. |
| `v-wiki-encyclopedie` | design | [Wiki-Encyclopédie (en).svg](https://commons.wikimedia.org/wiki/File%3AWiki-Encyclop%C3%A9die_%28en%29.svg) | Typographic front matter; text becomes hairlines and the plate is 29% empty. |
| `v-lamp-cad` | design | [Technisch Tekening Kap.svg](https://commons.wikimedia.org/wiki/File%3ATechnisch_Tekening_Kap.svg) | Mostly a dimension table; the lamp part is small and its notes are lost. |
| `v-double-pcb` | design | [Double side PCB process flow chart.svg](https://commons.wikimedia.org/wiki/File%3ADouble_side_PCB_process_flow_chart.svg) | Flow-chart boxes with text as outlines; the labels are unreadable at 640x480. |
| `v-transmitter-pcb` | design | [TransmitterFM-Copper.svg](https://commons.wikimedia.org/wiki/File%3ATransmitterFM-Copper.svg) | Whole-sheet view is a blank frame with a tiny board; the cropped `v-transmitter-pcb-crop` is the kept page. |
| `v-sarracenia` | plant | [Sarracenia flower notitles.svg](https://commons.wikimedia.org/wiki/File%3ASarracenia_flower_notitles.svg) | 136-byte page: the cutaway is an embedded bitmap/pattern, only a few outline fragments survive. |
| `v-fern-morphology` | plant | [Morphologie fougère.svg](https://commons.wikimedia.org/wiki/File%3AMorphologie_foug%C3%A8re.svg) | 2.2 KB: the fern body is labels-only; the frond itself is missing. |
| `v-daffodil` | plant | [Daffodil flower in section, labelled.svg](https://commons.wikimedia.org/wiki/File%3ADaffodil_flower_in_section%2C_labelled.svg) | 307 bytes: the section is CSS/text styling, no drawable vector art. |
| `v-green-fern` | plant | [Green fern.svg](https://commons.wikimedia.org/wiki/File%3AGreen_fern.svg) | CSS-only styling: 4-byte page. |
| `v-pea-development` | plant | [Flower seed fruit development diagram.svg](https://commons.wikimedia.org/wiki/File%3AFlower_seed_fruit_development_diagram.svg) | 482 bytes: only the label spans survive; the pod drawing is styled out. |
| `v-dryopteris` | plant | [Dryopteris carthusiana illustration 2.svg](https://commons.wikimedia.org/wiki/File%3ADryopteris_carthusiana_illustration_2.svg) | A sparse fern plate in one corner at 99.5% budget; rejected in favour of the Viola floral diagram. |
| `v-plant-cell` | plant | [Plant cell structure-en.svg](https://commons.wikimedia.org/wiki/File%3APlant_cell_structure-en.svg) | Good plant-cell plate, but LadyofHats already has two v- pages (skeleton, Culex); series cap. |
| `v-frog-life` | animal | [Greenfrog life stages.svg](https://commons.wikimedia.org/wiki/File%3AGreenfrog_life_stages.svg) | Good frog life-cycle plate, but LadyofHats already has two v- pages; series cap. |
| `v-centrifugal-pump` | mech | [Centrifugal Pump en.svg](https://commons.wikimedia.org/wiki/File%3ACentrifugal_Pump_en.svg) | 258 bytes: the pump is a bitmap/pattern, only labels survive. |
| `v-combustion-turbine` | mech | [Combustion turbine diagram.svg](https://commons.wikimedia.org/wiki/File%3ACombustion_turbine_diagram.svg) | 3.1 KB: a single vertical line remains; the engine section is missing. |
| `v-gas-turbine-configs` | mech | [Gas turbine configurations.svg](https://commons.wikimedia.org/wiki/File%3AGas_turbine_configurations.svg) | Six small sections at 52% budget; labels are vector outlines and do not read at panel size. |
| `v-voyager` | aero | [Voyager spacecraft structure vector.svg](https://commons.wikimedia.org/wiki/File%3AVoyager_spacecraft_structure_vector.svg) | CSS-only styling: 4-byte page. |
| `v-shenzhou` | aero | [Shenzhou spacecraft vector diagram.svg](https://commons.wikimedia.org/wiki/File%3AShenzhou_spacecraft_vector_diagram.svg) | 3.3 KB of sparse callout dots and vectors; the spacecraft outline is incomplete. |
| `v-htv` | aero | [H-II Transfer Vehicle (HTV).svg](https://commons.wikimedia.org/wiki/File%3AH-II_Transfer_Vehicle_%28HTV%29.svg) | Good cutaway, but 0/0 text spans: every label is a vector outline. At 99.5% budget the glyph strokes are compressed away and only single letters survive. Rejected on labels, not on the old NASA cap. |
| `v-mars-rover-mk` | aero | [Mars Exploration Rover mk.svg](https://commons.wikimedia.org/wiki/File%3AMars_Exploration_Rover_mk.svg) | Macedonian original of the rover page: 0 text spans (labels are outlined paths), 155 fills hit `skipped_cap`, labels vanish. The English `Mars Exploration Rover.svg` is shipped as `v-mars-rover`. |
| `v-mars-odyssey` | aero | [Mars Odyssey diagram.svg](https://commons.wikimedia.org/wiki/File%3AMars_Odyssey_diagram.svg) | Retried with `--fills outline --max-fills 1000`: 14/14 spans, `skipped_cap=0`, but 99.5% budget, 375 fill outlines and 11 chars clipped at the right edge; still below `v-hubble`. |
| `v-shuttle-labeled` | aero | [Space Shuttle Orbiter.svg](https://commons.wikimedia.org/wiki/File%3ASpace_Shuttle_Orbiter.svg) | 0/0 text spans: the labels are vector outlines; at 99.5% budget only letter fragments survive. The existing `v-shuttle-orbiter` line-art page is unaffected. |
| `v-soyuz-vehicle` | aero | [Soyuz spacecraft.svg](https://commons.wikimedia.org/wiki/File%3ASoyuz_spacecraft.svg) | 0/0 text spans; outlined labels collapse to fragments at 99.4% budget. The labeled `Soyuz Diagram.svg` is shipped as `v-soyuz`. |
| `v-jwst-hst` | aero | [JWST-HST-primary-mirrors.svg](https://commons.wikimedia.org/wiki/File%3AJWST-HST-primary-mirrors.svg) | 0/0 text spans; the mirror-comparison labels are vector outlines and vanish. Filled golden mirror discs, not line art. |
| `v-iss-simple` | aero | [International Space Station.svg](https://commons.wikimedia.org/wiki/File%3AInternational_Space_Station.svg) | 3 drawings, 0 text: an unlabelled silhouette; no callouts to place. |
| `v-apollo-lm` | aero | [Lądownik Apollo - Diagram.svg](https://commons.wikimedia.org/wiki/File%3AL%C4%85downik_Apollo_-_Diagram.svg) | 51/51 spans placed, but only 1 drawing and 5.0% budget: the LM body collapses to labels with almost no structure. |
| `v-apollo-csm-lm` | aero | [Apolo-1. CSM&LM diagram.svg](https://commons.wikimedia.org/wiki/File%3AApolo-1._CSM%26LM_diagram.svg) | 570 drawings but only numerals (26 words, 0 label text); a numbered figure without a readable key. |
| `v-soyuz-7ktm` | aero | [Soyuz 7K-TM (APAS) drawing.svg](https://commons.wikimedia.org/wiki/File%3ASoyuz_7K-TM_%28APAS%29_drawing.svg) | 1 drawing, 0 text: the labels are not a live layer and the single compound path gives no readable callouts. |
| `v-progress` | aero | [Progress-M spacecraft (with captions).svg](https://commons.wikimedia.org/wiki/File%3AProgress-M_spacecraft_%28with_captions%29.svg) | 0/0 text spans: the captions are vector outlines; only letter fragments survive at 99.5% budget (outline mode). |
| `v-atv` | aero | [Automated Transfer Vehicle.svg](https://commons.wikimedia.org/wiki/File%3AAutomated_Transfer_Vehicle.svg) | 0/0 text spans: outlined labels collapse to fragments; the spacecraft outline is fine but the page reads unlabelled. |
| `v-triode` | elec | [Triode-english-text.svg](https://commons.wikimedia.org/wiki/File%3ATriode-english-text.svg) | 108-byte page: the tube cutaway is an embedded bitmap; only a few outline fragments survive. |
| `v-tuner` | elec | [Tuner1.svg](https://commons.wikimedia.org/wiki/File%3ATuner1.svg) | 0/89 spans (0/218 chars): the schematic labels vanish and the dense network fills only 9.7 KB. |
| `v-trilobite-2020` | paleo | [202003 Trilobite.svg](https://commons.wikimedia.org/wiki/File%3A202003_Trilobite.svg) | Raster-only: no vector paths. |
| `v-jewel-bearing` | cad2 | [Watch jewel bearing and capstone.svg](https://commons.wikimedia.org/wiki/File%3AWatch_jewel_bearing_and_capstone.svg) | Clean jewel-bearing detail but not a full movement; held behind the Bulova movement page. |
| `v-cmos-chip` | elec | [Aufbau CMOS-Chip 2000er.svg](https://commons.wikimedia.org/wiki/File%3AAufbau_CMOS-Chip_2000er.svg) | 8/63 spans (79/663 chars) placed for a 63-label chip cross-section; too much text loss. |
| `v-8086` | elec | [Intel 8086 block scheme.svg](https://commons.wikimedia.org/wiki/File%3AIntel_8086_block_scheme.svg) | 3.0 KB block diagram, 12% budget; too sparse next to the Pentium Pro architecture page. |
| `v-r8555` | elec | [R8555U (Р855-У) survival radio.svg](https://commons.wikimedia.org/wiki/File%3AR8555U_%28%D0%A0855-%D0%A3%29_survival_radio.svg) | 0 text: the Cyrillic front-panel labels are lost; the radio reads as a blank case. |
| `v-water-phase` | math | [Phase diagram of water.svg](https://commons.wikimedia.org/wiki/File%3APhase_diagram_of_water.svg) | Axis grid dominates the page and the phase curves are lost in the hatching; the pure-iron diagram is cleaner. |
| `v-ammonium-phase` | math | [Ammonium nitrate water phase diagram.svg](https://commons.wikimedia.org/wiki/File%3AAmmonium_nitrate_water_phase_diagram.svg) | 24 KB of grid and 3,005 paths; only I-IV remain legible, so the pure-iron phase diagram was kept instead. |
| `v-orbitals-bh2nh3` | chem | [BH2NH3 orbitals.svg](https://commons.wikimedia.org/wiki/File%3ABH2NH3_orbitals.svg) | 68-byte page: the orbital lobes are an embedded bitmap; only two paths survive. |
| `v-fe-c` | chem | [Iron carbon phase diagram.svg](https://commons.wikimedia.org/wiki/File%3AIron_carbon_phase_diagram.svg) | Phase curves are good, but all labels are vector outlines and read as garbled fragments at 640x480. |
| `v-fe-o` | chem | [Fe-O phase diagr.svg](https://commons.wikimedia.org/wiki/File%3AFe-O_phase_diagr.svg) | Same label failure as the Fe-C diagram; only F/O glyph fragments read. |
| `v-vsepr` | chem | [Molekülgeometrie -EPA -VSEPR.svg](https://commons.wikimedia.org/wiki/File%3AMolek%C3%BClgeometrie_-EPA_-VSEPR.svg) | Molecular shapes are clear but the AXE labels are lost; no chemistry labels to place. |
| `v-amino-acids` | chem | [Molecular structures of the 21 proteinogenic amino acids.svg](https://commons.wikimedia.org/wiki/File%3AMolecular_structures_of_the_21_proteinogenic_amino_acids.svg) | 21-molecule grid at 5 KB: side chains collapse into specks and the labels are outlines. |
| `v-superionic` | chem | [Superionic ice conducting.svg](https://commons.wikimedia.org/wiki/File%3ASuperionic_ice_conducting.svg) | 19.8 KB crystal field with no labels and no recognizable unit cell. |
| `v-methanol` | chem | [Monohydrate de méthanol.svg](https://commons.wikimedia.org/wiki/File%3AMonohydrate_de_m%C3%A9thanol.svg) | 4.1 KB crystal packing, no labels; too sparse for a chemistry page. |
| `v-fluorenylidene` | chem | [Fluorenylidene-3D-balls.svg](https://commons.wikimedia.org/wiki/File%3AFluorenylidene-3D-balls.svg) | Raster-only: no vector paths. |
| `v-sp3d` | chem | [Formación de orbitales híbridos sp3d.svg](https://commons.wikimedia.org/wiki/File%3AFormaci%C3%B3n_de_orbitales_h%C3%ADbridos_sp3d.svg) | 3.7 KB of hatch blocks; the orbital labels are unreadable outlines. |
| `v-typo-terms` | type | [Typografische Begriffe.svg](https://commons.wikimedia.org/wiki/File%3ATypografische_Begriffe.svg) | Large labels are distorted letter outlines; the term diagram cannot be read at panel size. |
| `v-ccrige` | type | [CCRIGE font specimen.svg](https://commons.wikimedia.org/wiki/File%3ACCRIGE_font_specimen.svg) | Specimen text breaks into hatch fragments; only the display 'a' survives. |
| `v-kaufmann` | type | [Kaufmann Font Spec.svg](https://commons.wikimedia.org/wiki/File%3AKaufmann_Font_Spec.svg) | 4.9 KB specimen; the script face turns into hatch strokes and the words are unreadable. |
| `v-showcard` | type | [Show-card alphabet by W. A. Thompson, 1902.svg](https://commons.wikimedia.org/wiki/File%3AShow-card_alphabet_by_W._A._Thompson%2C_1902.svg) | CSS-only styling: 4-byte page. |
| `v-blood-vessels` | anat2 | [Blood vessels (retouched) -en.svg](https://commons.wikimedia.org/wiki/File%3ABlood_vessels_%28retouched%29_-en.svg) | Clean circulatory plate, but Kelvinsong already has two v- pages (comet, Callisto); series cap. |
| `v-plant-homology` | anat2 | [Morfologia de plantas - Homologia seriada en organos foliares.svg](https://commons.wikimedia.org/wiki/File%3AMorfologia_de_plantas_-_Homologia_seriada_en_organos_foliares.svg) | Plant outlines read, but all organ labels are garbled outlines; no usable text layer. |
| `v-dicentra` | plant | [Dicentra cucullaria illustration.svg](https://commons.wikimedia.org/wiki/File%3ADicentra_cucullaria_illustration.svg) | Botanical plate is too dense at 640x480: flowers, roots and hatching overlap; held back behind the cleaner Viola diagram. |
| `v-ne-south-america` | maps | [ne:south-america](https://www.naturalearthdata.com/) | Regional coastline crop; removed after the user restricted maps to world outlines. The two-hemisphere `v-ne-world` page replaces it. |

Also rejected at the source level: SVG files whose only content is an embedded bitmap (raster), files styled entirely through CSS classes (PyMuPDF returns one undrawn path, 4-byte page), and pages whose text loss makes the figure unreadable. No potrace, scan tracing, or bitmap source is used anywhere in this set.

## Method

- **Pool**: the v- sweeps covered 2,250 Commons SVG hits, then animals/plants/machinery/aerospace, then CAD/electronics/mathematics/paleontology, then chemistry/typography/system anatomy, bringing the pool to 5,745 files (5,644 license-ok). P5 re-used the cached aerospace pool and added the English `Mars Exploration Rover.svg`, `Ranger 6789.svg` and `Pioneer 10 systems diagram.svg`; HTV, Progress-M, ATV and Mars Odyssey were measured and rejected. P5b added `Soyuz Diagram.svg`, `ISS components.svg`, `Mir diagram.svg` and retried `HubbleExploded.svg`; the Space Shuttle Orbiter, unlabelled Soyuz, JWST/HST mirrors, ISS silhouette, Apollo LM/CSM-LM and Soyuz 7K-TM sources were measured and rejected (see the skip table). Natural Earth 50m coastline supplied the single world-outline page; regional crops were rejected (no memory point).
- **Licenses**: public domain, CC0, CC BY and CC BY-SA only; author and license come from the Commons `imageinfo/extmetadata` API. OSHW/CERN-OHL was allowed for CAD/PCB sources; the selected CAD/PCB pages are public-domain or CC.
- **Fair use of sources**: at most two pages per author/series (Kelvinsong comet + Callisto, charner1963 Bismarck + Saturn V, BIODIDAC bird skeleton + pelvis). The NASA-derived cap is explicitly lifted for P5/P5b at the user's request, so ISS, MER, Ranger, Pioneer 10, Soyuz, ISS components and Mir are added together; outside P5 the two-page cap still applies. Orionist now has two v- pages (`v-mir-shuttle`, `v-mir`), which is exactly the cap; LadyofHats frog/plant-cell remain in the skip table. No base/q source file is reused.
- **Per-page tuning**: only `v-ne-world` uses `--no-text --fills skip`; `v-transmitter-pcb-crop` crops to the board; the P5 pages use `--fills outline` (no hatch), `--max-fills 1000` on ISS/Pioneer, and `--crop 0,0,1,1` on Pioneer so the right-hand callouts stay on-screen. All four P5b pages use `--fills outline --max-fills 1000`, so `hatch=0` and `skipped_cap=0`. Everything else uses the hatch defaults. The converter was not edited.
- **P5 reproduce**: `python3 ../vector2tek/v/p5_final.py` reads (generated in the original working tree; not archived), writes the four `.tek` files and the previews under (generated in the original working tree; not archived), and builds the side-by-side pairs in (generated in the original working tree; not archived) (`p5-contact.png` is the batch sheet). Sources are the Commons files linked above; `../sources/` renders the left-hand original at the same fit.
- **P5b reproduce**: `python3 ../vector2tek/v/p5b_final.py` reads (generated in the original working tree; not archived), writes the four `.tek` files and previews under (generated in the original working tree; not archived), and builds the pairs in (generated in the original working tree; not archived) (`p5b-contact.png` is the batch sheet). The left-hand original is rendered with headless Chrome at the same content bbox; the `.tek` output does not depend on Chrome.
- **Scripts** (new, under `../vector2tek/v/`): `pool.py` (Commons search/metadata), `pool_ext.py` (animal/plant/mech/aero sweep), `pool_ext2.py` (CAD/electronics/math/paleo sweep), `pool_ext3.py` (chemistry/typography/system-anatomy sweep), `fetch.py` (curl fetcher with 429 retry), `world_map.py` (Natural Earth two-hemisphere world outline), `trial.py` (candidate convert/preview), `final.py` (shipped-page conversion), `manifest.py` (this file), plus `p5_final.py`/`p5_render_src.py` and `p5b_final.py`/`p5b_render_src.py` for the P5/P5b batches. No shipped code was left in `build/`.