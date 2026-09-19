# European Tour roadmap

The project grows in playable releases. Build and test each gameplay change
before adding the next; preserve the previous ROM in `artifacts/releases`.

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
