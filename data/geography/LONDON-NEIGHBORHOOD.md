# London residential lane (v0.83)

A fictional supporting street block extends east from the South Bank
garden loop. It uses native building fronts, not replicas of named homes
or a reconstruction of a real London street. Buildings at x44 and x54,
y28-32 face the front lane at y33-34. Their doors remain solid scenery.
Flower beds and a southern path at y40-41 form a complete public circuit.
Signs at (43,35) and (55,35) point toward the Eye and explain the homes.

London expands from 40x44 to 64x44 without shifting the old district.
The former boundary at x38-39, y36-37 opens for the new lane. Four old
walkable grass cells at x36-37, y36-37 become paving, retaining collision
and elevation. Other old walkable cells retain their exact metatiles.
Existing solid tree caps can adapt to the new opening; their collision
and elevation remain unchanged outside it. All buildings are outside the
old footprint. Existing objects, entrances, map IDs and layout IDs remain.
The loaded-map grid fits the existing hardware buffer. Normal Continue
uses the existing city cache refresh and preserves player coordinates.

london-v082.bin preserves the previous full outdoor footprint. Regenerate
with build-london-map.py. Verify with test_london_neighborhood_static.py,
test_london_neighborhood.py, the London walking/bridge checks, Eye gallery
and Westminster case. The shared london_compatibility.py assertion checks
the retained footprint for older garden/gallery fixtures too. Save/cold
Continue is exercised at (60,40), beyond the old map width.

## v0.84: western home sitting room

The western door at (45,32) offers a Yes/No invitation from (45,33).
EuropeLondonHome is appended after all 47 previous Europe maps. Its native
13x10 room has a host at (8,4), a notebook at (3,3), and exit triggers at
(4,8) and (5,8), both returning to (45,33). Conversations award no items
and alter no progression flags. Save/cold Continue preserves indoor state.
The travel map identifies London, England. The eastern door stays private.

london-v083.bin preserves the exact outdoor grid; the v0.83 map-ID fixture
preserves the prior ID prefix. Regenerate with build-london-home.py then
build-london-map.py. test_london_home_static.py checks stable generation,
entrances, unchanged outdoor tiles and prior IDs. test_london_home.py
checks declined invitations, conversations, reentry, both exits, indoor
Save/Continue, travel-map country and return to the countryside.

## v0.85: eastern reading room

EuropeLondonReadingRoom appends after the 48 v0.84 maps. The door at
(55,32) offers a Yes/No invitation from (55,33). A neighbor shares local
walking advice and a notebook points to the Eye, bridges and Westminster.
Both exit triggers return to (55,33). No conversation grants rewards or
changes progression. Normal Save/Continue works indoors. Both homes are
identified as London on the travel map. The lane sign describes both rooms.

Outdoor tiles remain byte-identical to v0.83/v0.84. The reading-v084 ID
fixture retains the complete earlier prefix, including the western home.
Regenerate with build-london-reading-room.py then build-london-map.py.
Tests test_london_reading_static.py and test_london_reading.py cover IDs,
generation, invitations, conversations, both exits, cold Continue and map
country; the western home and older London checks run alongside them.

## v0.86: slate-blue eastern roof

Only the eastern roof at x54-58, y28-30 uses new metatile IDs. The asset
generator appends copies of the original native roof metatiles, retaining
every flip bit and behavior attribute. Referenced native roof artwork is
copied and its color indices map to existing blue-gray palette 8. Four red
roof shades become distinct slate-blue shades. Shared palettes are intact.
The western roof, wall/door tiles and every other outdoor tile are intact.
No map IDs, object positions, entrances or indoor layouts change.

london-v085.bin records the preceding full outdoor map. The shared facade
assertion permits only the specified roof substitutions. The dedicated
facade static checks validate copied tile attributes, artwork references
and the four shade mappings. Regenerate assets before build-london-map.py.
Normal lane cold Continue refreshes the changed artwork in older saves.

## v0.87: compact reading area and shared books

The eastern room clears the former rug/chair area at x4-9, y3-6, retaining
the native table at x6-7, y4-5. Cabinet artwork at x9-10, y0-1 occupies the
existing solid back wall. A reading interaction at (9,1) is reached from
(9,2); it shares a short note about neighbors' books and favorite walks.
It grants no rewards and changes no progression flags. Existing host and
notebook objects, entry, both exits and all map IDs remain unchanged.

london-reading-v086.bin and the event/group fixtures preserve the previous
room. Static checks require every old walkable tile to remain open at the
same elevation and confine art changes to the reading area/back cabinet.
london-v086.bin verifies the outdoor map is byte-identical. A v0.86 indoor
battery is cold-loaded in the new ROM, reads the cabinet and exits before
the usual invitation, conversation, reentry and Save/Continue checks.
Regenerate with build-london-reading-room.py. New checks are in
test_london_furnishings_static.py; interactions use test_london_reading.py.

## v0.88: sitting-room photo album

The western home appends an album object at (6,4), on the existing solid
table. Read it from (6,3), facing down. The host points to the album, which
shares a short fictional sequence of neighborhood garden photos. It gives
no rewards and changes no progression flags. Previous host/notebook object
indices, exit triggers, all map IDs and both indoor/outdoor grids remain.

The london-home-v087 layout/event/group fixtures capture the preceding
room. test_london_album_static.py checks exact indoor and outdoor grids,
table collision, unchanged earlier events/IDs and reward-free dialogue.
A v0.87 indoor battery is cold-loaded in test_london_home.py, reaches the
album and exits before the usual invitation, conversation and save checks.
Regenerate with build-london-home.py. Existing generator stability checks
include the new object and dialogue; normal font-width checks cover it.

An equivalent table background interaction supports pre-change indoor saves
whose saved object list lacks the new album. The visible album refreshes
when the room is re-entered; the story is readable immediately.

## v1.01 northern arrival guidance

The existing London route sign at (14,4), read from (14,5), retains
its two countryside pages and adds visitor-room approach directions and
the travel-map R: Places / L: Rooms shortcut. No terrain, events, objects,
IDs or wild encounters change. Rebuild with build-capital-arrival-signs.py;
the capital-arrival-signs.json source retains the original trail text.
Compatibility hashes are in capital-arrival-v100.json. Emulator checks
cover old batteries, both northern crossings, repeated reads and cold
Continue. Each reading checks exact party and progress before/after.

## v1.03 station approach guidance

The existing London station sign at (22,11), read from (22,12),
keeps its ticket-office page and adds two pages of neighborhood guidance.
The route is south along the city paths, then east to the visitor rooms.
The sign also explains the travel-map R: Places / L: Rooms shortcut.
No terrain, events, IDs, station staff or train logic changes. Rebuild
with scripts/build-capital-station-signs.py; source text is retained in
capital-station-signs.json, compatibility hashes in capital-station-v102.json.
Focused emulator checks cover normal and side exit approaches, sign repeats, every
room approach and cold Continue. Earlier full regressions are archived
with v1.02; v1.03 records 23 freshly run checks for the changed guidance.

## v1.04 local walks inside the station

The London station framed wall picture at (9,1), read from (9,2),
holds local walking guidance. It describes the south paths and east
neighborhood rooms. The solid furniture tile 0x585 and all room terrain,
staff, service scripts, exits and IDs stay unchanged. A background event
works in retained v1.03 indoor saves without cached-object changes.

Build with scripts/build-station-boards.py. Source notes are stored in
station-boards.json; station-boards-v103.json retains prior maps/scripts
and the room-grid hash. Focused tests cover genuine earlier indoor saves,
repeat readings, exits, re-entry, new cold saves, outdoor signs and Rooms
controls. Each read checks exact party and progress before and after.

## v1.72: warm western-home walls

Nine wall cells at x44-48, y31-32 use appended native tile variants in existing
palette8. Native window art, flips and attributes are retained. The door at
(45,32), red roof, neighboring slate roof, paths and all events stay intact.
Build assets with build-london-assets.py; apply-london-facade.py updates the
current grid without regenerating its events/scripts. build-london-map.py
also includes the wall mapping for full regeneration. Baseline assets are in
london-facade-v171. Verify test_london_western_static.py and the two native
runtime suites before replacing the playable ROM.
