# Regional landmark districts (v0.52)

Walk EAST from the original central squares in Oxford, Chantilly and
Oranienburg. London, Paris and Berlin still have their landmark districts
to the SOUTH. Signs identify the new landmarks and paths.

| Town | Recognizable features |
| --- | --- |
| Oxford | Radcliffe Camera and square, Magdalen Tower beside the High Street approach, Cherwell to the east, two river crossings and meadow paths |
| Chantilly | Chateau on a moated island, Great Stables southwest of the chateau, formal gardens and an east-west Grand Canal |
| Oranienburg | White baroque palace with terracotta roofs and an accessible central forecourt, Schlosspark to the west, Havel to the east and two crossings |

The layouts compress real landmark relationships into playable districts.
They are not street-by-street replicas: prototype service hubs are retained,
and route distances and some paths are simplified. Landmarks are exterior
scenery. Ports received their first pass in [v0.53](COASTAL-LANDMARKS.md).
Historical towns, neighborhood architecture, bridge artwork
and finer river shapes still need further work. The pre-1940 Chantilly building exteriors are also used in the
[v0.54 historical estate](HISTORICAL-CHANTILLY.md), with its own layout and signs.

Landmarks are always visible. WORLD OPTIONS currently changes regional-map
detail/contrast and avatar presets; walking-map decoration settings and full
character customization remain future work.

## Geographic references

The following official sources informed the landmark choices and relative
layout; the sprites are original generated artwork, not copied source images.

- [Oxford visitor map](https://www.ox.ac.uk/sites/files/oxford/field/field_document/Explore%20Map%20and%20Visitor%20Information_2025.pdf)
- [Radcliffe Camera](https://www.ox.ac.uk/about/how-we-are-run/equality-diversity/access-guide/glam/radcliffe-camera)
- [Magdalen, High Street and the Cherwell](https://www.magd.ox.ac.uk/waynflete-project/)
- [Chantilly estate](https://chateaudechantilly.fr/)
- [Great Stables](https://chateaudechantilly.fr/grandes-ecuries/)
- [Chantilly estate illustrated plan](https://chateaudechantilly.fr/app/uploads/2024/06/ENS-Brochure-2024-2025_BD.pdf)
- [Oranienburg palace](https://www.spsg.de/schloesser-gaerten/objekt/schlossmuseum-oranienburg)
- [Schlosspark plan](https://www.oranienburg-erleben.de/wp-content/uploads/schlossparkplan-mit-parkordnung-2022.pdf)
- [Schlossplatz and Havel planning reference](https://oranienburg.de/media/custom/2967_576_1.PDF?1526622099=)

## Generation and save compatibility

Original source atlases and full built-in image-tool prompts are in
[`graphics/europe/landmarks/REGIONAL-PROMPTS.md`](../../graphics/europe/landmarks/REGIONAL-PROMPTS.md).
Regenerate with `scripts/build-regional-assets.py`, followed by
`scripts/build-regional-maps.py`. The regional compiler bounds crops and
trains palettes on pixels with alpha at least 128, excluding faint invisible
speckles. Each city uses a shared 15-color landmark palette and appended
metatile IDs. The original capital conversion defaults remain unchanged.

The immutable `*-v051.bin` inputs preserve the original 32x24 hubs. Maps extend
east while keeping their original height, southern trail connections, events,
doors and quest characters. Old walkable coordinates retain their land/water
classification and elevation. Tree edges are recapped at the new boundaries.

All six expanded modern towns clear their cached tile views when loading so
old saves receive the new scenery. Use in-game Save and cold CONTINUE, not
emulator states from another ROM. Packaging never modifies player saves.

## Verification

The focused regression walks every new district through mGBA button input,
checks all loaded map tiles against the authored layouts, reads signs, crosses
bridges, saves inside each district and cold-loads the resulting batteries.
It also checks service approaches, map return, southern trail connections,
old Oxford surfing and ferry saves, capital districts, World Options and
historical London travel. Static checks cover all 38 maps, old-coordinate
compatibility, hardware limits, dialogue widths and byte-for-byte generation.
This is focused regression coverage, not a rerun of every project test.
