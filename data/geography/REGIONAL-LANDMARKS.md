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
The regional bridge detail pass is complete in v1.77, with both walking
lanes retained. v1.78 adds landmark directions to Town Map Places pages.
Further historical scenery and finer river shapes remain future work. The pre-1940 Chantilly building exteriors are also used in the
[v0.54 historical estate](HISTORICAL-CHANTILLY.md), with its own layout and signs.

Landmarks are always visible. WORLD OPTIONS changes regional-map detail and
contrast, flower visibility, avatar presets and outfit colors. Further
character customization remains future work.

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

## v1.75: Oxford bridge parapets

Twelve deck cells at x56-58,y12-13 and x55-57,y19-20 use stone rail overlays
in existing primary palette3. Collision, elevation, behavior and both clear
walking rows remain intact. Eight tiles and two metatiles append without
altering earlier art. build-regional-assets.py Oxford invokes oxford_bridges.py;
apply-oxford-bridges.py updates the current grid without regenerating events.
The full regional map generator also includes the rails. Baseline source is
in oxford-bridges-v174; test_oxford_bridges_static.py and test_oxford_bridges.py
cover exact source compatibility and genuine old-save crossings.

## v1.76: Chantilly moat parapets

Ten deck cells at x50-51,y11-15 use stone rails in existing palette3.
Both walking columns, terrain behavior and prior assets remain intact.
Eight tiles/two metatiles append. build-regional-assets.py Chantilly invokes
chantilly_bridge.py; apply-chantilly-bridge.py updates the current grid
without regenerating events. The regional map generator includes the rails.
Baseline source is chantilly-bridge-v175. Verify test_chantilly_bridge_static.py
and test_chantilly_bridge.py before packaging.

## v1.77: Oranienburg bridge parapets

Twelve deck cells at x55-57,y12-13 and x55-57,y19-20 use stone rail overlays
in existing primary palette3. Collision, elevation, behavior and both clear
walking rows remain intact. Eight tiles and two metatiles append without
altering earlier art. build-regional-assets.py Oranienburg invokes oranienburg_bridges.py;
apply-oranienburg-bridges.py updates the current grid without regenerating events.
The full regional map generator also includes the rails. Baseline source is
in oranienburg-bridges-v176; test_oranienburg_bridges_static.py and test_oranienburg_bridges.py
cover exact source compatibility and genuine old-save crossings.
# Oxford Gym roof refinement, v1.89

The fictional Oxford Gym has a slate-blue native roof variant. Fourteen cells
at x12–18, y6–7 change artwork only. Eight metatiles and nine copied roof tiles
append after the existing Oxford bridge assets. Existing palettes, walls,
door at (15,9), approach (15,10), collision and events remain intact.
This is supporting town architecture, not a replica of a named Oxford building.

# Chantilly Gym roof refinement, v1.90

The fictional Water-type Gym now has a blue roof using existing native palette
3 and nine copied tiles. Fourteen cells at x12–18, y6–7 change artwork only.
Eight metatiles append after the moat bridge assets. Walls, door, approaches,
collision, estate artwork, palettes and map events remain intact.

# Oranienburg Gym roof refinement, v1.91

The fictional Electric-type Gym now has a gold roof using existing native
palette 9 and nine copied tiles. Fourteen roof cells at x12–18, y6–7 change
artwork only; eight metatiles append after the Havel bridge assets. The
entrance, walls, collision, palace/park art, palettes and events remain intact.

# Oxford station roof refinement, v1.92

The fictional station has a terracotta roof using existing palette 8 and nine
copied tiles. Fourteen roof cells at x20–26, y6–7 change artwork only; eight
metatiles append after the Oxford Gym roof variants. The entrance at (23,9),
approach (23,10), walls, collision, rail services and earlier assets stay intact.

# Chantilly station roof refinement, v1.93

The fictional station now uses a terracotta roof matching Oxford's rail visual
identity. Fourteen cells at x20–26, y6–7 change artwork only; eight metatiles
and nine copied tiles append after the Water Gym roof. Existing palette 8,
entrance, collision, travel services, estate assets and map events remain intact.

# Oranienburg station roof refinement, v1.94

The fictional station now shares the terracotta rail identity of Oxford and
Chantilly. Fourteen roof cells at x20–26, y6–7 change artwork only; eight
metatiles and nine tiles append after the gold Gym roof variants. Palette 8,
station entrance, collision, services, Havel paths and prior assets stay intact.

# Oxford clinic wall refinement, v1.95

Nine native wall cells at x5–9, y8–9 gain pale-blue detailing. The doorway
at (6,9) remains exact, as do the red roof, entrance approach (6,10), collision,
events and free care. Nine metatiles and thirteen copied native tiles append
after the station variants; all palettes and prior assets remain untouched.

# Chantilly clinic wall refinement, v1.96

Nine wall cells at x5–9, y8–9 now share Oxford's pale-blue clinic detailing.
The door at (6,9), red roof, approach (6,10), collision, events and free care
remain exact. Nine metatiles and thirteen copied tiles append after the station
variants, preserving palettes, Water Gym, station, château and moat artwork.

# Oranienburg clinic wall refinement, v1.97

Nine wall cells at x5–9, y8–9 now match Oxford and Chantilly's pale-blue clinic
detail. The door at (6,9), red roof, entrance approach (6,10), collision and free
care remain exact. Nine metatiles and thirteen copied native tiles append after
the station variants; prior gold Gym, station, palace and Havel assets remain.


## v2.00: Station train markers

Oxford, Chantilly and Oranienburg stations have train-symbol signs at (22,11).
Read from (22,12), facing UP; enter from (23,10). Four tiles and one metatile
append per town after the clinic sign. Earlier artwork, palettes, sign events,
collision and rail services are preserved. Both regional generators include
the marker, with exact regeneration and native station/rail/save checks.

## v2.01: Gym Poke Ball markers

The three regional Gyms have Poke Ball signs at (14,11). Read from (14,12),
facing UP; enter from (15,10). Four tiles and one metatile append per town
after the station sign. Previous artwork, palettes, collision and events
remain exact. Both regional generators reproduce the markers. Native checks
use earned Gym readiness, saved entrances/interiors, leader declines and exits.
