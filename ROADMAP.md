# European Tour roadmap

The project grows in playable releases. Build and test each gameplay change
before adding the next; preserve the previous ROM in `artifacts/releases`.

## To do: complete game walkthrough

- [ ] Write an exact, step-by-step walkthrough from a new game through the
  final completion sequence, covering each starting-country choice.
- [ ] Include required quest order, prerequisites, locations, travel routes,
  NPC interactions, menu choices, battles, rewards and completion checks.
- [ ] Clearly label optional activities and explain how to resume after saving.
- [ ] Verify the instructions against the current playable ROM from fresh
  saves, and record the release version the walkthrough covers.

## v1.09: route guidance after walking detours

The saved-trip prompt explains that the route starts at the current station.
Only one dialogue line changes. Genuine v1.08 saves after walking detours to
Oxford and Chantilly verify recalculated connections and remaining trains,
kept bookings, cold Continue after rejoining and final Oranienburg arrival.
Next: review the local walking guidance in branch-town stations.

## v1.08: walking-arrival completion guidance

Reaching a booked destination on foot now names the destination, confirms
the cleared booking and explains how to choose another trip. Rail commands
remain exact. Genuine v1.07 saves cover Oxford, Chantilly and Oranienburg,
then cold Continue and return bookings. Compatibility helpers now preserve
mixed source line endings when restoring individual dialogue blocks.
Next: review guidance for walking detours to a different rail station.

## v1.07: returning passenger choices

Saved-trip guidance explains that bookings stay during exploration and
that NO opens a separate cancellation choice. YES boards the next train.
Only resume dialogue changes; all rail commands remain exact. Old transfer
and Paris exploration saves exercise every page and both decision paths.
Next: improve final-arrival guidance for travelers exploring on foot.

## v1.06: intermediate rail exploration guidance

Intermediate boarding shows both the next stop and final destination.
It points to the station wall notice and explains that the booking stays
while exploring. Only this dialogue changes; all rail commands remain exact.
Focused checks cover a Paris garden visit, Save/Continue and onward travel.
Next: review arrival guidance for passengers returning from local walks.

## v1.05: clear rail-clerk booking cues

The welcome message explains that selecting a stop previews a journey,
B/Exit closes the list and booking starts only when boarding. Selecting
the current station explains how to choose another stop. Existing routing,
preview, transfer, saved-journey and cancellation commands remain exact.
Focused checks cover all six stations and a genuine v1.04 saved transfer.
Next: review guidance at intermediate rail stops before local exploration.

## v1.04: station local-walk notices

Each capital station's existing framed wall picture is a readable local
walking notice. It points to the river/Gate paths and describes the east
neighborhood rooms. Background interactions work in genuine v1.03 indoor
saves. No furniture, terrain, staff, service scripts, exits or IDs change.
Next: review the station clerk's destination cues and cancellation flow.

## v1.03: station-to-neighborhood guidance

Each capital's station sign retains its ticket-office page and adds the
visitor-room names, south-then-east approach and travel-map Rooms shortcut.
Station staff, train scripts, terrain, events and map IDs remain exact.
Focused checks cover normal and side approaches to the station exit, every room approach, repeat reads,
cold Continue, northern arrival guidance and Rooms controls.
Next: review destination cues inside the three stations.

## v1.02: visible Berlin northern sign

Berlin's northern route-sign event now has native sign artwork and solid
collision at (14,4). The three adjacent north/south lane columns remain
open. A v1.01 battery saved directly on the former pavement retains its
position and can step off, read the sign and continue through the city.
Only this tile changes; events, objects, IDs and encounters are retained.
Next: improve the station-to-neighborhood directions.

## v1.01: northern arrival guidance

Each capital's existing northern route sign retains its countryside pages
and adds directions to the visitor rooms and travel-map Rooms shortcut.
London points to the east home/reading lane, Paris to sketches/garden rooms,
and Berlin to its three-room courtyard. Terrain, events, encounters and
map IDs stay exact. Next: review visible northern markers and station-to-neighborhood directions.

## v1.00: capital Rooms pages

The travel map's Places view offers L: Rooms for London, Paris and Berlin.
Four lines explain each neighborhood's approach, room order and readable
details. Existing landmark guidance stays on the Places page. L switches
back, changing stops resets to Places, and R/B/START/A/story controls retain
their behavior. No map, event or save-format changes.
Next: review the countryside approaches to the capital neighborhoods.

## v0.99: Berlin courtyard notice

The existing courtyard sign keeps its room directions and adds a notice
linking the workbench observations, reading-room garden log and western
home guestbook. It is readable in retained v0.98 outdoor saves. Terrain,
objects, events and map IDs stay exact. Next: review the three capital
neighborhoods together and improve any remaining navigation gaps.

## v0.98: Berlin garden observations

The garden workroom's left bench holds seed observations and the right
bench holds watering observations. Both are readable from north and south,
including in retained v0.97 indoor saves. The gardener points to the notes.
All room terrain, walking space, objects, exits and map IDs remain.
Next: a local detail along Berlin's residential courtyard.

## v0.97: Berlin library catalog

The reading-room table lists the garden log and travel field notes. Its
four existing solid cells are readable from north and south, including
in retained v0.66 indoor saves. Each room owns its background events;
the garden workroom no longer inherits the sitting-room guestbook.
Terrain, objects, exits and map IDs remain. Next: Berlin garden detail.

## v0.96: Berlin courtyard guestbook

The sitting-room table holds shared memories of the courtyard flowers,
trees and a quiet walk by the Gate. All four existing solid table cells
are readable, including from retained v0.65 indoor saves. Terrain, objects,
exits and map IDs are unchanged. Next: a detail for the Berlin library.

## v0.95: Paris workbench plans

The garden workroom's left bench holds a planting plan and the right bench
holds a shared care rota. Both are readable from their exposed sides,
including in pre-change indoor saves. The gardener points to the benches.
All room/outdoor tiles, walking space, objects, exits and map IDs remain.
Next: more local detail in the Berlin neighborhood rooms.

## v0.94: Paris sketch display

A back-wall display in the western sketch room describes three river views
in changing light. The host points visitors toward it. Only four existing
solid wall tiles change; every walking tile, object and exit is retained.
Older indoor saves refresh the artwork on Continue without moving players.
Next: a local planning detail inside the Paris garden workroom.

## v0.93: distinct Paris neighborhood roofs

The eastern garden workroom has a slate-blue native roof; the western
sketch room retains its red roof. Copied roof tiles use an existing
blue-gray palette, preserving all shared palette colors. Paths, walls,
doors, interiors, collision and earlier map IDs remain unchanged.
Next: local display details inside the Paris sketch room.

## v0.92: Paris eastern garden workroom

The eastern home opens a garden workroom with two side benches, a gardener
and a shared-planning notebook. A clear central passage reaches both front
exits. Normal Save/Continue and the France map label work indoors. The room
appends after all 50 prior Europe maps; outdoor tiles and earlier IDs stay
unchanged. Next: visually distinguish the two Paris neighborhood fronts.

## v0.91: Paris western home sketch room

The western lane door opens a native visitor room with a host and a
river/garden sketchbook. Both front exits return to its own approach,
and normal Save/Continue works indoors. The room appends after the 49
previous Europe maps. All outdoor tiles and earlier IDs remain unchanged.
Next: a complementary room in the eastern Paris home.

## v0.90: Paris promenade side lane

A fictional neighborhood lane extends east from the promenade, with two
native home fronts, flower beds, signs and a southern walking loop. Both
homes remain private scenery. Paris expands to 64x46 without moving old
walking coordinates, objects, entrances or map IDs. Only the lane mouth
opens the old tree boundary. Next: a visitor room in the western home.

## v0.89: Paris promenade sketcher

A stationary sketcher stands on the grass south of the paved promenade,
sharing a short observation about the river and keeping public paths clear.
Older Paris saves restore the new template without leaving the city. All
outdoor tiles, earlier objects, entrances and map IDs remain unchanged.
Next: Paris neighborhood fronts beyond the landmark district.

## v0.88: London sitting-room photo album

A photo album on the western home's table tells a short neighborhood
garden story. The host points visitors toward it. Indoor/outdoor tiles,
existing objects, exits and map IDs stay unchanged. A pre-change indoor
battery reaches the album and exits normally. Next: neighborhood detail
along the Paris promenade.

## v0.87: London reading-room furnishings

The eastern home has a compact reading table and shared-book cabinet,
with the sitting-room rug and chairs removed. The cabinet adds a short
reading interaction. Every previously walkable indoor tile stays open;
existing objects, exits, map IDs and the outdoor district are unchanged.
Next: more local character in the western sitting room.

## v0.86: distinct London home roofs

The eastern reading room has a slate-blue native roof; the western sitting
room retains its red roof. Only the eastern roof art changes. Paths, door
positions, collision, elevation, existing map IDs and interiors remain.
Next: distinctive interior furnishings for the reading room.

## v0.85: London eastern home reading room

The eastern door now opens a reading room with a neighbor and a notebook
of local walks. Both homes support normal Save/Continue and return to
their own front paths. All earlier IDs and outdoor tiles remain unchanged.
Next: more distinctive neighborhood facades and interior furnishings.

## v0.84: London western home sitting room

The western home opens through a front-door invitation. A host and garden
notebook add an indoor stop with two exits and normal Save/Continue.
The eastern home stays private. Previous map IDs and every outdoor tile
remain unchanged. Next: the eastern home and distinctive facades.

## v0.83: London residential side lane

A small fictional residential lane extends east from the South Bank garden
loop. Two native home fronts face public paths, with flower beds and a
southern walking circuit. Signs point back to the Eye and explain that
the homes remain private scenery. London expands east without moving old
coordinates or map IDs; only the lane mouth opens the former tree boundary.
Next: distinctive facades and enterable neighborhood rooms.

## v0.82: saved Purple outfit

World Options adds PURPLE after GREEN in the outfit cycle. The native
walking/cycling sprites and four-direction preview use the new clothing
ramp, including corresponding reflection shades. Only the same three
clothing palette entries change. Old Classic/Blue/Green values retain
their meaning, normal Save/Continue retains Purple, and Restore Defaults
returns to Classic. Next: street and building detail across the districts.

## v0.81: four-direction avatar preview

R turns the World Options avatar preview through front, left, back and
right views. SELECT retains walking/cycling switching; avatar and outfit
changes retain the preview direction. Reopening begins facing forward.
Confirmation ignores rotation, and native R-button Help behavior returns
on closing. No saved movement or direction is changed. Next: street and
building detail across the tour districts.

## v0.80: travel-map Places guide

R opens a Places page for the selected travel-map stop. Capital pages give
visitor-room and garden directions; country towns and ports list useful
walks and transport. Browse all eight stops with the D-pad. B/START/R
returns to the map, A shows route information, and SELECT opens the story.
The guide labels its information as present-day when viewed from a past
save. Native R-button Help behavior is restored on exit. Next: street and
building detail across the tour districts.

## v0.79: London garden visitor and Jigglypuff

A visitor and native JIGGLYPUFF now rest beside the South Bank flower beds.
Repeatable dialogue and a cry connect the garden loop to the Eye gallery.
Older London saves restore both stationary visitors on Continue. Every
outdoor tile, original city object and map ID is retained. Next: more
street and building detail across the tour districts.

## v0.78: Paris garden observer and Psyduck

A stationary observer and native PSYDUCK now rest beside the garden flower
beds. Repeatable conversation and a cry connect quiet observation with
the Eiffel visitor room. Older Paris saves restore both residents on
Continue. All outdoor tiles, original city objects and map IDs are retained.
Next: additional street detail and remaining landmark areas.

## v0.77: Brandenburg Gate visitor room

A compact fictional visitor room opens from the Gate's west pillar.
A guide and garden/courtyard displays connect the landmark passage to
nearby walks and shared neighborhood care. Two front exit tiles return
to the same approach. Outdoor terrain and all previous map IDs are
retained, and the indoor regional map identifies Germany. Next: further
street detail and remaining landmark areas.

## v0.76: Berlin courtyard companion

A native PIKACHU now keeps the courtyard neighbor company. Its repeatable
cry and greeting add life beside the flower beds; the neighbor introduces
it and still identifies the visitor rooms. Older Berlin saves restore the
new stationary companion on Continue. Street tiles, doors and map IDs are
retained. Next: more street detail and remaining landmark areas.

## v0.75: walking and cycling avatar preview

SELECT in WORLD OPTIONS toggles the preview between native walking and
cycling poses. Avatar and outfit changes update either pose immediately.
The preview starts in walking mode each time the menu opens; this display
choice does not change the player's field movement or saved preferences.
Next: street detail and remaining landmark areas.

## v0.74: live avatar preview and indoor map labels

WORLD OPTIONS displays the selected Red/Leaf avatar and outfit immediately.
The preview updates when choices change and after Restore Defaults. It is
hidden during reset confirmation and removed on returning to the field or
regional map. Eiffel and Berlin visitor-room map labels now identify their
correct countries instead of falling back to London. Next: further avatar
polish, street detail and remaining landmark areas.

## v0.73: saved avatar outfit colors

WORLD OPTIONS adds CLASSIC, BLUE and GREEN outfit colors for Red and Leaf.
The change recolors three clothing entries in the player's overworld
palette and corresponding reflection shades. Skin, hair, other sprite
colors and trainer identity retain their original values. Walking and
cycling use the existing sprite frames. Restore Defaults includes the
new outfit preference. Next: further customization and broader street detail.

## v0.72: confirmed World Options defaults

WORLD OPTIONS adds RESTORE DEFAULTS as a fifth row. Press A to open a
confirmation, then A to restore simple map detail, the original avatar,
natural map colors and flowers on. B/START cancels the confirmation.
No trainer identity, inventory or journey progress is reset. Save normally
to retain the defaults. Next: further customization and broader street detail.

## v0.71: saved flower decoration option

WORLD OPTIONS now includes FLOWERS: ON/OFF. Turning flowers off renders
European outdoor flower beds as plain lawn. This is a visual-only option:
the map grid, collision, gameplay attributes, encounters and quest triggers
are retained. Old saves default to flowers on. The preference is saved
with normal Save/Continue. Next: further customization and street detail.

## v0.70: London Eye visitor gallery

A window-lined visitor gallery now opens from the wheel's southern base.
An attendant and garden/bridge displays connect the gallery to the South
Bank walking routes. Both front exit tiles return to the same approach.
The outdoor London map and prior indoor map IDs are retained.
Next: additional landmark areas and broader street detail, followed by
remaining World Options and character customization.

## v0.69: Eiffel visitor room

A compact fictional visitor room now opens from the Eiffel Tower's south
base. A guide and garden/river exhibits connect observation to shared care.
Both front exit tiles return to the same landmark approach. Existing Paris
terrain and prior map IDs remain unchanged. Next: more landmark rooms and
broader street detail, then remaining World Options/customization work.

## v0.68: Berlin courtyard roof variety

The sitting room keeps its terracotta roof; the reading room has a green
roof and the garden workroom a slate roof. These native-tile variants
make the three visitor doors easier to recognize. The change preserves
all collision, elevation, behavior, door positions and indoor map IDs.
Next: broader street detail and additional landmark interiors.

## v0.67: Berlin garden workroom

The eastern courtyard building now contains a gardener, shared tool notes
and a planting plan. Two side benches leave a clear central passage.
All three courtyard doors now admit visitors: sitting room, reading room
and garden workroom. Earlier indoor map IDs are retained.
Next: facade variety, additional street detail and landmark interiors.

## v0.66: Berlin neighborhood reading room

The middle courtyard building now opens into a reading room. A librarian,
garden log and neighborhood memories extend the theme of shared care.
A compact reading table gives this room a different layout from the home.
The eastern home remains private scenery. Previous map IDs are retained.
Next: facade variety, further neighborhood detail and landmark rooms.

## v0.65: first enterable Berlin courtyard home

The western courtyard home now opens into a furnished sitting room with
an inviting host and a garden notebook. The entrance offers Yes/No;
both floor tiles of the front exit return to the courtyard. Existing
map IDs and outdoor terrain are retained. Other homes remain scenery.
Next: more facade variety, neighborhood rooms and landmark interiors.

## v0.64: Berlin courtyard residents

Two residents now bring the courtyard to life: a gardener tending flowers
with ODDISH and a neighbor explaining the public lanes and nearby landmarks.
Both conversations are repeatable and give no rewards or story flags.
Next: facade variety, enterable neighborhood buildings and landmark rooms.

## v0.63: Berlin street block delivered

A compact residential court now extends east of the Brandenburg Gate's
boulevard approach. Three building fronts, side lanes, flower beds and
a southern loop begin the neighborhood-building pass. Two signs give
local directions. New buildings lie outside the old map footprint.

Existing landmark routes and the Reichstag case remain available. The
supporting homes use native art and are fictional private residences;
more authentic facade variety and enterable neighborhood buildings remain
next steps, alongside additional landmark rooms and World Options work.
See data/geography/BERLIN-NEIGHBORHOOD.md for the layout and save limits.

## v0.62: London waterfront and bridge detail delivered

Modern Westminster Bridge now has green rail details and the southern
Lambeth crossing has red rails. A connected garden loop joins the South
Bank paths beside the London Eye. Existing signs explain the crossings.
All v0.61 collision, elevation and land/water cells remain unchanged.
The interior generator now retains exterior event ordering on regeneration.

Next: street/building infill, additional landmark rooms, and remaining
World Options/customization. Historical London retains its separate map.
See data/geography/LONDON-WATERFRONT.md for design and references.

## v0.61: Paris garden and promenade detail delivered

Added connected paved loops around the Champ de Mars flower beds, two
side approaches and a clearer left-bank promenade toward Notre-Dame's
island bridge. Updated the existing signs with walking directions.
Every v0.60 Paris collision, elevation and land/water cell is preserved.
The Notre-Dame case remains accessible and save-compatible.

Next: London's waterfront and bridge details, then street/building infill,
additional landmark rooms and the remaining World Options/customization.
See data/geography/PARIS-PROMENADE.md for the reference and layout limits.

## v0.60: landmark cases, visual fixes and story revision

Delivered three explorable landmark visitor areas: Notre-Dame, Westminster
and the Reichstag, with saved investigations and one-time rewards. Gastly
can be caught at Notre-Dame after its peaceful resolution. Corrected tree
silhouettes and filtered landmark art address the reported visual issues.

The revised opening, regional dialogue and Ada/Rose conclusion connect
fieldwork to the historical chain of care. Two later Oxford report detours
are now optional. Existing chapter flags, badges and saves are retained.

Resumed town-detail work with connected Tiergarten paths and visitor
entrance directions. Next: fuller street/building infill and distinctive
waterfront details, followed by additional landmark interiors and the
remaining World Options/character-customization work. The three new rooms
are a first playable set, not completion of every landmark.
See data/geography/LANDMARK-CASES.md for the story and case design.

## v0.59: historical London first landmark pass delivered

Westminster, Parliament Square, Whitehall and two Thames crossings now
form a district east of the original reception. The existing palace art
is reused, with no London Eye placed in the historical map. Old positions,
quests and Southampton return travel remain available and tested.
The playable historical destinations now have first landmark passes.
Next: fuller street/building infill, distinctive bridge/waterfront details,
then the remaining World Options and character-customization work.
See data/geography/HISTORICAL-LONDON.md for references and remaining gaps.

## v0.58: historical Southampton old town delivered

Bargate anchors the north end of High Street; Tudor House and wall-side
lanes lead to Town Quay. A three-cell boardwalk bypass opens the eastbound
route without moving the luggage worker or London clerk. Old positions,
quests, care and ferry travel remain available. The new district has been
built and tested before moving on. Next: historical London, then finer
street layouts and the remaining World Options/customization work.
See data/geography/HISTORICAL-SOUTHAMPTON.md for sources and limits.

## v0.57: historical Le Havre harbor delivered

Notre-Dame church, Maison de l'Armateur and the Commerce/Roy basins now
form a compressed district east of the existing terminal. A two-tile
boardwalk bypass keeps the dockworker in place while opening the route.
Old positions, quests, care and ferry travel remain available. The new
district has been built and tested before moving on.
Next: historical Southampton and London, followed by finer street layouts
and the remaining World Options/customization work.
See data/geography/HISTORICAL-LE-HAVRE.md for period references and limits.

## v0.56: Amiens and Rouen landmark districts delivered

Amiens now includes Notre-Dame, Saint-Leu houses and Somme canals. Rouen
includes Notre-Dame, the Gros-Horloge and Seine quays. Existing quest hubs
remain accessible, with cold-save migration and expanded-area saving tested.
Each city was built and tested before moving on. These compressed districts
use intact pre-destruction geography, not day-specific wartime damage.
Next: historical Le Havre, Southampton and London; finer streets and the
remaining World Options/customization work continue afterward.
See data/geography/AMIENS-ROUEN.md for directions, sources and limits.

## v0.55: station context and Beauvais delivered

The Chantilly post has its own station/trackside layout, separate from the
refuge estate. Beauvais Garden opens east into a cathedral/palace district
and river crossings. Original reception and quest routes are retained.
Next: historical Amiens and Rouen; finer streets, measured station facades
and day-specific wartime conditions remain future refinements.
See data/geography/STATION-BEAUVAIS.md for scope and verification.

## v0.54: historical Chantilly estate delivered

The 1940 refuge now opens east into a compressed estate with the chateau,
moat, Great Stables, garden paths and Grande Pelouse. Original story tasks,
characters and return coordinates are retained. The station post and other
historical towns still need geographic/architectural passes. Next: historical
station context and Beauvais, then the remaining historical destinations.
See data/geography/HISTORICAL-CHANTILLY.md for period sources and limitations.

## v0.53: coastal landmark districts delivered

Dover and Calais now have coastal walking districts east of their preserved
ferry terminals. Dover has its Great Tower, white cliffs and harbor paths;
Calais has its town hall/belfry, lighthouse and northern seafront. Cold saves,
ferry journeys, coach returns and saved rail bookings remain supported.
Next are period-correct historical town layouts, followed by finer modern
neighborhood/street detail and walking-map decoration settings.
See data/geography/COASTAL-LANDMARKS.md for scope and references.

## v0.52: regional landmark districts delivered

Oxford, Chantilly and Oranienburg now have compressed landmark districts EAST
of their original hubs, with custom architecture, rivers, crossings and paths.
All six modern rail stops have received a first landmark pass. Ports (Dover
and Calais), historical towns and finer neighborhood architecture remain next.
Walking-map decoration settings and expanded customization remain pending.
See data/geography/REGIONAL-LANDMARKS.md for scope, references and limitations.

## Active priority: geographic realism and customization

User selected compressed, recognizable real-world layouts. Town redesign now
takes priority over further story chapters. The first foundation adds a
geographically projected regional map and the persistent WORLD OPTIONS key
item. Eight modern destinations now have first-pass landmark districts. See
`data/geography/README.md` for scope, references and remaining work.

v0.51 adds explorable landmark districts to London, Paris and Berlin, with
custom architecture, rivers, crossings and paths. v0.52 adds Oxford, Chantilly and Oranienburg; v0.53 adds the coastal ports.
Period-correct historical towns remain next. More
capital street/building detail remains. See `data/geography/LANDMARKS.md`.

| Stage | Scope | Status |
| --- | --- | --- |
| 1. Playable foundation | London, Paris, Berlin; countryside encounters; trains; clinics; saving | Complete, v0.1 |
| 2. First tour objective | Three city stamps and one EXP. SHARE reward | Complete, v0.2 |
| 3. European opening | Custom title, professor welcome, nine regional starter choices | Complete, v0.3 |
| 4. Trainer progression and supplies | Optional local trainers, saved victories, prize money, station shops | Complete, v0.4 |
| 5. City identity and navigation | Distinct outdoor layouts, landmark signs, and a schematic European travel map | Complete prototype pass, v0.5 |
| 6. Connected regional journeys | More real towns, longer walking/cycling routes, multi-stop trains | Complete prototype pass, v0.10; six trainers and three regional rewards |
| 7. Regional story and Gyms | A coherent first country arc, rival encounters, Gym progression and rewards | Three country arcs and three Gyms complete prototype pass, v0.16 |
| 8. Additional transportation | Pokemon riding and suitable ferry connections | Riverboats, rental water riding, and Dover�Calais ferry complete prototype pass, v0.19 |
| 9. Celebi storyline | Time-travel rules, historical Europe maps, and the WWII story arc | First arc and two-topic journal complete; London reception and arrival added, v0.49; twenty records; wider wartime story continues |
| 10. USA companion connection | Agree on engine/data formats, then prototype player transfer with the companion project | Requires coordination |

Stage 5 adds a London river crossing, Paris gardens, and Berlin tree-lined
plaza using existing tiles. Custom architecture and detailed geographic map art
remain future polish. Stage 7 needs a complete short story arc before expanding that story
across the continent. Celebi's historical maps should reuse the established
travel and quest systems while storing present/past progress separately.

Stage 6 now includes London–Oxford, Paris–Chantilly, and Berlin–Oranienburg.
Every starting country has a second town and a longer walking/cycling journey,
with six destinations in the rail menu. Rail journeys now connect through the
London–Paris–Berlin line and its three local branches, with intermediate stops
and saved itineraries. Each country also has two optional trail trainers and
a one-time regional reward from its secondary-town guide. The first story chapter now follows Oak's England field study: London aide,
local trainer preparation, Oxford rival match, and a return report reward.
Oxford Gym now concludes this first arc with Ellis, a Rock-type battle,
the first badge, and a one-time Rock Tomb TM. France now has a garden survey: two observations collected in either order,
a review in Chantilly, and a return report in Paris. Chantilly Gym concludes the survey with Marine, a Water-type battle,
the second badge, and a one-time Water Pulse TM. Germany now adds Lena and Karl's signal-repair delivery between Berlin and
Oranienburg, with a one-time Magnet reward. Oranienburg Gym concludes this arc with Conrad, the Thunderbadge, and a
one-time Shock Wave TM. Additional transportation now starts with a free London�Oxford riverboat
link unlocked by the third badge. It preserves rail itineraries and uses
existing town landings. Rental Lapras rides now add player-controlled water travel and shoreline
dismounting at both landings. They reuse Surf visuals; custom mount artwork,
land mounts and longer water routes remain planned. Dover and Calais now
add compact coastal ports, connected to London/Paris by coach and to each
other by ferry. The Celebi prologue now connects an Oxford researcher to a Chantilly Forest
sighting, a vision of 1940, and a saved return report. Celebi now opens a
playable Chantilly refuge in 1940, with a short task to
help Elise and her Eevee and an always-available return anchor. Past progress
is stored separately from present-day quests. The station post now adds a
notice, dispatcher confirmation and report to the refuge, with a second
Celebi return point. A historical train now connects the post to Beauvais
reception, where Elise and Eevee check in and remain after departure. Both
return services and saved unfinished visits work. Elise now sends a message
back to the refuge; carrying the reply and reporting to Ada closes the first
short historical arc with a one-time Luxury Ball. A follow-up supply run now
opens repeatable party care at Beauvais, with saved parcel progress across
era changes. The new Beauvais garden adds a saved search and reunion for Luc
and his Pidgey, with reception and Celebi return paths. A Town Map journal
now tracks the current historical objective and seven milestones from saved
progress. A regional journal topic also guides the three country arcs, Gym
rewards and optional city stamps. An onward historical train now opens an
Amiens reception courtyard and Nora's meeting-point briefing, with saved
progress and both return routes. Nora now coordinates a reunion for Mira and
Meowth, with reports collected in either order and a ninth journal milestone.
Completing that reunion opens free, repeatable party care with Nora. A return
report to Ada in Oxford records the Amiens account and a tenth milestone.
The porter now requests a checked bulletin for Nora, establishing the waiting
plan while the existing return routes remain open. Delivering it now unlocks
the onward Rouen train, Leon's arrival welcome, a direct Amiens return and a
Celebi exit, with saved progress and journal guidance. Rouen now has a separate
riverside layout, paved banks and a crossing, preserving old-save positions.
Leon now requests a missing route book from the far bank, with a persistent
pickup, return objective and journal guidance. Returning the book now unlocks
free, repeatable party care with Leon, including existing completed saves.
The historical journal now records thirteen milestones across two pages,
including the later Amiens and Rouen tasks. Returning the route book now
also unlocks transport to Le Havre reception, a captain's welcome, a Rouen
return service and Celebi exit, with a fourteenth milestone. Later milestones expand
the historical locations and story; this remains a fictional prototype.

The USA connection remains a design objective. Existing Pokemon trading does
not transfer the player into another ROM; the two projects need an explicit
shared approach to species, items, saves, and world transfer.

Automated tests use real button input in the mGBA core. Any setup fixtures,
coverage limits, and verified behaviors belong in `TESTING.md`.

Version 0.40 continues Le Havre with a dockworker request, entrance notice
and captain confirmation. Its fifteenth journal record and saved stages
preserve both return routes. Onward historical travel remains future work.

Version 0.41 adds free, repeatable dockworker care after the captain checks
the dock instructions, including previously completed saves.

Version 0.42 closes the port reception chapter with an optional account
recorded by Ada in Oxford and a sixteenth historical journal milestone.

Version 0.43 rewards the completed port account with a Celebi destination
choice: the original refuge or a direct Le Havre revisit.

Version 0.44 opens a fictional Southampton crossing and reception welcome,
with a Le Havre return, Celebi exit and seventeenth journal record. Journal
completion bits now support more than sixteen milestones.

Version 0.45 adds a traveler luggage search and return at Southampton,
with persistent pickup state, both return routes and an eighteenth record.

Version 0.46 rewards the luggage return with free, repeatable party care
at Southampton, including previously completed saves.

Version 0.47 adds a direct Celebi return to Southampton after the luggage
task, preserving both previous destinations and cancellation choices.

Version 0.48 closes Southampton reception with an optional return report
to Ada in Oxford and a nineteenth historical journal milestone.

Version 0.49 opens onward transport to a fictional London reception
courtyard, Rose's welcome, both return paths and the twentieth record.
