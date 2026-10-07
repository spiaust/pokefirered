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

## v0.96 sitting-room guestbook

The four existing table cells (6,4), (7,4), (6,5), (7,5) have any-facing
background interactions. Read from (6,3) facing down or (6,6) facing up.
Background events support old v0.65 indoor saves without cached-object
changes. No artwork, terrain, walking space, objects, exits or IDs change.
The host points visitors to the table. The text grants no items or flags.

Rebuild with scripts/build-berlin-home.py. Static checks use the retained
berlin-home-v095 binary, events and groups fixtures; emulator checks cover
normal visits, repeated reads, Save/Continue, both exits and old batteries.

## v0.97 reading-room catalog

The existing central table at x6-7, y4-5 lists the garden log and travel
field notes. Read from (6,3) facing down or (6,6) facing up. Four background
events work with the retained v0.66 indoor save. The librarian points to
the catalog. No terrain, objects, exits, map IDs, inventory or flags change.
The library and garden generators explicitly own their background events
instead of inheriting the sitting-room guestbook through the layout source.

Rebuild with scripts/build-berlin-library.py. Static compatibility checks
use berlin-library-v096 fixtures; runtime tests cover normal visits, old
batteries, Save/Continue, both exits and return to the countryside.

## v0.98 garden workbench observations

The left bench at x2-3, y5-6 holds seed notes and the right bench at
x10-11, y5-6 holds watering observations. All eight existing solid cells
have any-facing background interactions. Read from (2,4)/(10,4) facing
down or (2,7)/(10,7) facing up. The gardener points to the notes.
No terrain, walking space, objects, exits, map IDs, flags or inventory
change. Unused library catalog script text is removed from this room.

Rebuild with scripts/build-berlin-garden-room.py. Compatibility checks use
berlin-garden-v097 terrain, events and groups fixtures. Emulator coverage
includes the retained berlin-garden-room-v097 battery, north/south reads,
normal visits, Save/Continue, both exits and countryside return.

## v0.99 courtyard notice

The existing sign at (56,34), approached from (56,35), retains its first
two pages of room directions. Two further pages point to the workroom
observations, middle reading-room garden log and western guestbook.
No map tile, event position, object, exit, map ID or progression changes.

Rebuild with scripts/build-capital-maps.py Berlin. The berlin-court-v098
fixtures retain exact map, event and group data. Emulator checks use the
retained berlin-court-v098 battery, read all four pages twice, visit every
room approach, save at the sign, cold Continue, reread and return to the
countryside. Each reading checks exact party/progress data before/after.

## v1.01 northern arrival guidance

The existing Berlin route sign at (14,4), read from (14,5), retains
its two countryside pages and adds visitor-room approach directions and
the travel-map R: Places / L: Rooms shortcut. No terrain, events, objects,
IDs or wild encounters change. Rebuild with build-capital-arrival-signs.py;
the capital-arrival-signs.json source retains the original trail text.
Compatibility hashes are in capital-arrival-v100.json. Emulator checks
cover old batteries, both northern crossings, repeated reads and cold
Continue. Each reading checks exact party and progress before/after.

Berlin compatibility note: the inherited route-sign event is on a walkable
tile at (14,4). Its terrain is retained in this text-only release. Approach
from (14,6) to (14,5) facing up, then press A without another upward step.
A visible marker remains an item for the next navigation review.

## v1.02 visible northern route marker

The marker at (14,4) is restored to native sign tile 0x402. This replaces
only the former pavement tile 0x3165 and keeps its existing background
event. The three adjacent north/south lane columns x15-17 remain open.
No object, event position, map ID or encounter data changes. This resolves
the visible-marker issue recorded in v1.01. Read from (14,5) facing up.

berlin-marker-v101.bin retains the complete earlier map. The helper in
berlin_compatibility.py permits exactly this tile for older terrain tests.
The separate marker static check requires the new tile and exact remainder.
A genuine pre-change berlin-marker-v101 battery was saved at (14,4).
Emulator tests verify unchanged cold-load position, refreshed terrain,
stepping off, repeated reads, routes around the sign, new Save/Continue
and both countryside crossings. Rebuild with build-capital-maps.py Berlin.
