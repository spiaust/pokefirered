# Paris garden and promenade pass (v0.61)

The compressed Eiffel Tower / Champ de Mars district now has paved loops
around its flower beds, western and eastern garden approaches, and a
clearer left-bank promenade leading toward Notre-Dame's island bridge.
The Eiffel and Seine signs describe these routes.

The tower remains west of the island landmark, with the gardens south of
the river. This is a condensed gameplay arrangement, not a street-by-street
reconstruction. The paths are inspired by the relationships shown on the
[Eiffel Tower's official access map](https://www.toureiffel.paris/en/access-map).
No additional real street names are assigned to the compressed paths.

Every v0.60 map cell retains its collision, elevation and land/water type.
The river, bridges, landmark footprints, services and Notre-Dame entrance
stay in place. The map refresh on normal Continue displays the new paving
without relocating the player. The v0.60 terrain snapshot is retained as
an automated compatibility fixture.

Regenerate with `scripts/build-capital-maps.py Paris`. Verify with
`scripts/test_paris_promenade.py`, `scripts/test_capital_realism.py Paris`
and `scripts/test_landmark_cases.py NotreDame`.

Next town-detail work: more distinctive waterfront/bridge treatment in
London, followed by street and building infill that respects saved positions.

## Garden visitors (v0.78)

The observer at (6,40) and native PSYDUCK at (7,40) rest beside the flower
beds, clear of the paved garden loops. Speak from (6,41) or (7,41). These
stationary supporting characters add repeatable dialogue and a normal
cry; they give no reward and change no story or inventory state.

Every v0.77 outdoor tile is retained in paris-v077.bin. The original city
objects retain their template order; the two visitors append afterward.
Older Paris saves restore only the two new stationary templates on
Continue. All map and layout IDs remain unchanged.

Regenerate with build-capital-maps.py Paris. Verify with
 test_paris_garden_static.py, test_paris_garden.py, the promenade and capital
walking/save checks, the Eiffel visitor room and the Notre-Dame case.

## Promenade sketcher (v0.89)

A fictional stationary sketcher at (30,42) stands on the grass below the
paved promenade. Speak from (30,43). Repeated dialogue describes watching
the changing light and keeping the path clear; it grants no rewards and
changes no progression. The existing four city/garden objects retain
their template indices. Every outdoor tile and map/layout ID is unchanged.

Older Paris batteries restore the fifth stationary template alongside the
garden visitors. test_paris_artist_static.py checks exact terrain and old
event/ID preservation using paris-artist-v088 fixtures. test_paris_artist.py
checks an old battery, three readings, collision, promenade routes, normal
Save/cold Continue and countryside return. Regenerate with
build-capital-maps.py Paris. Garden, promenade, capital walking, Eiffel
visitor and Notre-Dame case checks run with the new feature.

## Neighborhood side lane (v0.90)

Paris expands from 40x46 to 64x46. A two-row opening at x38-39, y40-41
connects the existing promenade to a fictional supporting neighborhood.
Old walkable tiles retain their exact metatiles, including the grass
approach at x37. Other old collision/elevation and land/water are unchanged;
solid tree caps can visually adapt to the new opening. No old coordinates,
objects, entrances, map IDs or layout IDs move. The loaded grid fits the
existing hardware buffer. Normal Continue uses the city cache refresh.

Native home fronts at x44-48 and x54-58, y34-38 have solid doors and clear
approaches at (45,39) and (55,39). Public paths at y39-41 and a southern
loop at y43 circle the flower beds at y42. Signs at (43,41) and (55,41)
explain that both homes are private and point west toward the landmarks.
The Places guide points east along the promenade to the lane.

paris-v089.bin and paris-lane-v089-events.json preserve the preceding
footprint and events. paris_compatibility.py checks older 40x46 fixtures
against the expanded grid. test_paris_lane_static.py verifies old walking
cells, events, IDs, approaches and hardware bounds. test_paris_lane.py
walks both fronts and the circuit, reads both signs, and checks the full
loaded grid before and after a cold save at (60,43), beyond the old width.
Regenerate with build-capital-maps.py Paris. Earlier Paris garden, sketcher,
promenade, Eiffel, Notre-Dame and capital walking checks run alongside it.

## Western home sketch room (v0.91)

EuropeParisHome appends after the 49 prior Europe maps. The western door
at (45,38) offers a Yes/No invitation from (45,39), entering at (5,7).
A host at (8,4) and sketchbook at (3,3) describe the river and shared
gardens. They give no rewards and alter no progression flags. Front-exit
triggers at (4,8) and (5,8) both return to (45,39). The eastern home stays
private. Signs and the Places guide identify the open western room.
The travel map labels this indoor stop Paris, France.

paris-v090.bin preserves the exact outdoor lane. The v0.90 group fixture
preserves every earlier group/map ID. test_paris_home_static.py checks
appended IDs, entrance reachability and stable indoor/outdoor generation.
test_paris_home.py checks No/B cancellation, entry, conversations, reentry,
normal Save/cold Continue, both exits, country display and countryside
return. Older static checks now assert prior ID prefixes so appended maps
can coexist while every older ID retains its meaning. Regenerate with
build-paris-home.py then build-capital-maps.py Paris.

## Eastern garden workroom (v0.92)

EuropeParisGardenRoom appends after all 50 earlier Europe maps. The eastern
door at (55,38) offers a Yes/No invitation from (55,39), entering at (5,7).
Two native side workbenches at x2-3 and x10-11, y5-6 leave the center open.
The gardener at (8,4) and notebook at (3,3) discuss shared planning, quiet
space for POKEMON and keeping public paths clear. No reward or progression
state changes. Front exits at (4,8) and (5,8) return to (55,39). The travel
map identifies Paris, France. Lane signs identify both open rooms.

The v0.91 group fixture preserves the entire preceding ID prefix, including
the western home. Exact outdoor terrain remains paris-v090.bin. New checks
in test_paris_workroom_static.py and test_paris_workroom.py cover IDs,
generation, invitations, conversations, reentry, both exits, indoor
Save/cold Continue, map country and countryside return. Regenerate with
build-paris-garden-room.py then build-capital-maps.py Paris.

## Distinct neighborhood roofs (v0.93)

The eastern workroom roof at x54-58, y34-36 uses appended copies of the
native roof metatiles. Referenced tile artwork is copied with color indices
mapped to existing blue-gray palette 8. Four red roof shades become distinct
slate shades, retaining transparency, artwork shapes, flip bits and behavior
attributes. Shared palettes, earlier tile IDs, western roof, wall/door tiles,
all other outdoor terrain, interiors, entrances and map IDs are unchanged.

paris-v092.bin records the preceding full map. assert_paris_facade permits
only the eastern roof substitutions; dedicated facade checks validate
native tile references, behavior attributes and unchanged shared palettes.
Assets regenerate identically. Regenerate assets before the Paris map.
The normal lane test checks the entire loaded grid on old battery Continue
and after a new cold save beyond the old map width. Both room tests continue
to cover invitations, conversations, exits, indoor saves and country display.

## Back-wall sketch display (v0.94)

The western sketch room replaces four solid back-wall cells at (9,0),
(10,0), (9,1) and (10,1) with native cabinet artwork. The display interaction
at (9,1) is read from (9,2). Its short fictional description follows three
river views in morning, midday and evening light. No reward or progression
state changes. All walking cells, elevations, objects, exits, outdoor
terrain and map IDs remain unchanged. The host points toward the display.

The room has no persistent dynamic tiles, so normal Continue clears its
cached map view just as the existing outdoor refresh does. A v0.93 indoor
battery loads the exact new 13x10 grid at its saved coordinates, reads the
display and exits with progress retained. New cold saves also match the
complete grid. paris-home-v093 fixtures preserve the former room and events.
test_paris_display_static.py checks wall-only artwork changes and unchanged
objects/exits; test_paris_home.py covers the old battery and new interaction.
Regenerate with build-paris-home.py. Existing generator and font-width
checks include the display dialogue.

## Workbench planning notes (v0.95)

The eastern workroom's existing left bench (x2-3, y5-6) holds a planting
plan, and the right bench (x10-11, y5-6) a shared care rota. Each of the
eight solid furniture tiles has a background interaction with any-facing
access, supporting reading from any exposed side. The gardener points
visitors toward both benches. Descriptions concern quiet POKEMON space,
open public paths and sharing small garden tasks. No rewards or progression
state changes. Every indoor/outdoor tile, object, exit and ID is unchanged.

A v0.94 indoor battery reads both benches from north and south and exits
with party/inventory/progress retained. Normal visits read both plans too.
paris-workroom-v094 fixtures preserve the previous room and events.
test_paris_plans_static.py checks exact room tiles, unchanged objects/exits,
solid bench coverage and reward-free dialogue. test_paris_workroom.py
covers the old battery alongside the normal invitation, conversation,
both-exit, cold-save and country-display checks. Regenerate with
build-paris-garden-room.py; native font-width checks cover the new notes.

## v1.01 northern arrival guidance

The existing Paris route sign at (14,4), read from (14,5), retains
its two countryside pages and adds visitor-room approach directions and
the travel-map R: Places / L: Rooms shortcut. No terrain, events, objects,
IDs or wild encounters change. Rebuild with build-capital-arrival-signs.py;
the capital-arrival-signs.json source retains the original trail text.
Compatibility hashes are in capital-arrival-v100.json. Emulator checks
cover old batteries, both northern crossings, repeated reads and cold
Continue. Each reading checks exact party and progress before/after.
