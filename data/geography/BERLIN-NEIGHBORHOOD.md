# Berlin street block (v0.63)

Continue east along the Brandenburg Gate's boulevard approach, through the
former tree boundary. Three residential fronts face a public court, with
side lanes, flower beds and a southern walking loop. Two signs identify
the route back to the Gate and explain that the homes are private.

The block is fictional supporting scenery using native building tiles.
It is not a replica of named Berlin residences or the full Unter den Linden
streetscape. Realistic facade variety and additional enterable buildings
remain future work. Existing landmark geography is unchanged.

Berlin expands from 40x44 to 64x44 tiles without shifting the original
district. The only removed collision is the former eastern tree boundary
at x38-39, y37-39. The grass approach at x37 is paved; other old walkable
cells retain their tiles. All new solid buildings are outside the old map.
The loaded-map buffer remains within its hardware limit. Existing city
cache refresh also applies to saves inside the extended district.

Regenerate with scripts/build-capital-maps.py Berlin. Verify with
scripts/test_berlin_neighborhood.py, scripts/test_capital_realism.py Berlin,
and scripts/test_landmark_cases.py Reichstag. The v0.62 map is retained as
the compatibility fixture berlin-v062.bin.

## Courtyard residents (v0.64)

Two stationary residents stand beside the flower beds at (45,36) and
(53,36). They leave both side lanes and the boulevard open. Speak from
the southern path; each conversation releases field controls on closing.
No map tiles, warps, quest flags or inventory are changed by this update.

## Sitting room (v0.65)

The western home admits visitors through an A-button invitation at its
solid door (43,31), approached from (43,32). A native furnished room is
reused without its upstairs stair. The host and notebook offer repeatable
dialogue without rewards or flags. Two southern exit trigger tiles return
to (43,32). EuropeBerlinHome is appended to the map group and layouts,
preserving all older IDs and the entire outdoor tile map.

Regenerate with scripts/build-berlin-home.py, then
scripts/build-capital-maps.py Berlin. Verify visits and indoor saves with
scripts/test_berlin_home.py. The other two homes remain exterior scenery.

## Reading room (v0.66)

A fictional neighborhood reading room opens from the middle doorway at
(51,31), approached from (51,32). It contains a librarian, garden log and
neighborhood memories. Both southern exit tiles return to (51,32). No
rewards, inventory changes or story flags are attached to these records.
The small central reading table leaves all objects and exits reachable.
EuropeBerlinLibrary is appended after EuropeBerlinHome so older indoor
saves retain their map anchor. Exterior tiles and object positions remain
unchanged; courtyard signs and the neighbor explain both open buildings.

Regenerate the home, library and capital with scripts/build-berlin-home.py,
scripts/build-berlin-library.py and scripts/build-capital-maps.py Berlin.
Use scripts/test_berlin_library.py for reading-room visits and cold saves.
The home test also loads a retained v0.65 indoor battery-save fixture.

## Garden workroom (v0.67)

The eastern courtyard door at (58,31), approached from (58,32), opens
a fictional shared garden workroom. A gardener, tool notes and planting
plan explain the care behind the courtyard. Side benches leave a clear
central passage. No rewards, inventory changes or story flags are added.
Both front exit tiles return to (58,32). The workroom map is appended
after the reading room; the prior home and reading-room IDs are retained.

Generate after the home and library with scripts/build-berlin-garden-room.py,
then regenerate the capital. Use scripts/test_berlin_garden_room.py for
visits and indoor cold saves. The library test also exercises a retained
v0.66 indoor save; the home test retains the v0.65 compatibility check.

## Roof variety (v0.68)

Native roof tiles distinguish the terracotta home, green reading room and
slate workroom. Palette 12 is reserved for the green roof and was unused
in the previous Berlin map. Slate roof tiles reuse neutral native colors.
Only the upper three rows of the middle and eastern roofs change: 30
solid map cells. Attributes, collision, elevations and doors are identical
to the retained berlin-v067.bin fixture. The variants occupy 259 of 384
secondary tile slots and preserve the existing landmark assets.

Regenerate with scripts/berlin_facades.py, then the Berlin capital map.
The capital asset generator also invokes the roof compiler after Berlin
landmark generation. Verify with scripts/test_berlin_facades.py and the
existing room and walking checks. These remain fictional native facades.

## Courtyard companion (v0.76)

Native PIKACHU stands at (54,36), immediately east of the neighbor.
Approach from (54,37) for its normal cry and repeatable greeting. The
existing neighbor introduces it. Tiles, visitor door positions, prior
object IDs and map IDs remain unchanged; the companion appends as the
fifth object. Side lanes and all three visitor approaches remain open.
Older Berlin saves restore stationary templates 2 through 4 on Continue,
including the companion, without replacing the original city NPCs.

Use test_berlin_companion.py for an older courtyard battery, blocked
companion cell, repeated greetings, visitor lanes, normal Save/cold
Continue and countryside return. Neighborhood regeneration, capital
walking routes, the garden room and Reichstag case are also rechecked.
