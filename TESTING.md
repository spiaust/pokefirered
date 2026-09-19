# Prototype verification — 2026-09-18

## v0.61 Paris promenade verification - 2026-09-19

53 focused PASS results on the updated build and its generated map data:
41 map/path checks, 3 capital compatibility checks, 3 dialogue/tree/
regeneration checks, 2 full-map Paris preservation/generation checks,
2 emulator walking/save checks and 2 Notre-Dame investigation/save checks.

The walking test visits both garden approaches, the garden loop and the
promenade toward the island. It reads the signs, saves and cold-loads the
new district, checks the loaded terrain and returns through the hub to the
countryside. The Notre-Dame test checks entry cancellation, clues, peaceful
resolution, one-time rewards, exit/re-entry and cold saves inside.
Every v0.60 Paris map cell retains its collision, elevation and land/water
type. Previous v0.60 ROM and user saves are hash-verified during packaging.

## v0.60 landmark, story and visual verification - 2026-09-19

109 focused PASS results across staged build-and-test passes. Each gameplay
stage was built and tested before moving on; the final Notre-Dame visual
correction was followed by another complete case test, the edge-case suite
and the revised story test.

- 41 map/path checks; 7 layout/terrain compatibility checks.
- 3 static checks for dialogue widths, complete tree silhouettes and
  deterministic interior/case generation.
- 8 case play-through/save results, including the final Notre-Dame recheck.
- 7 edge cases: both clue orders in each room, all three full reward pockets,
  and a real, catchable level-12 Gastly battle. Rewards do not repeat.
- 12 new-game country/starter results and 4 Celebi chapter checks.
- 10 story/travel results: deferred reports, Ada's ending, case synthesis,
  Southampton and London travel, journal state and modern rail bookings.
- 11 walking/save results: Paris, Berlin, London, Oranienburg and historical
  London. Berlin's new garden paths and entrance signs were exercised.
- 6 deliberately stale route-save tree caches refresh correctly on cold
  Continue, preserving the player position, team and existing progress.

In-game building, garden, interior and Ghost encounter screenshots were
inspected. Testing uses disposable test-output saves. The package keeps
v0.59, verifies its SHA256, and hashes user artifact saves before and after
copying the new ROM. Existing emulator save states are not upgrade fixtures.

## v0.59 historical London verification - 2026-09-19

52 focused checks passed on the final build:

- 2 landmark walking/save checks: complete loaded terrain, four signs,
  both bridges, cold Continue, historical map and Southampton/Celebi returns.
- 9 story checks: London travel/welcome/journal/booking (3), v0.48 adjacent
  save migration (1), Oxford prerequisite report (2), Southampton travel (3).
- 38 map checks, old terrain/layout compatibility (1), sign widths (1),
  deterministic generation and absence of modern London Eye tiles (1).

In-game palace and river-crossing screenshots were inspected. All original
walkable terrain/elevations and story characters are preserved. Historical
and modern London layouts remain separate. Final logs/screenshots are
archived with v0.59; packaging verifies the previous v0.58 ROM hash. User
saves are not used or changed.

## v0.58 historical Southampton verification - 2026-09-19

59 focused checks passed on the final build:

- 2 landmark walking/save checks: reception bypass, complete loaded terrain,
  four signs, wall-side lanes, pier, cold Continue, map and ferry/Celebi returns.
- 16 story checks: Southampton travel (3), luggage (3), care (3), Oxford
  report (2), London travel (3), v0.44/v0.48 adjacent-save migrations (2).
- 38 map checks, original harbor art/layout compatibility (1), sign widths
  (1), deterministic asset/map generation (1).

All original walkable terrain remains unchanged. Three formerly blocked
edge cells bypass both workers; the original northern exit stays closed.
In-game screenshots of Bargate, Tudor House, walls and quay were inspected.
Final build and test logs are archived with v0.58. Packaging verifies the
previous v0.57 ROM hash; user saves are not used or changed.

## v0.57 historical Le Havre verification - 2026-09-19

59 focused checks passed on the final build:

- 2 landmark walking/save checks: all loaded terrain, four signs, crossings,
  cold Continue in the new district, historical map and Rouen/Celebi returns.
- 16 story checks: Le Havre travel (3), dock task (2), care (3), direct port
  return (3), Southampton travel (3), old dockworker/ferry-clerk saves (2).
- 38 map checks, original harbor art/layout compatibility (1), sign widths
  (1), and deterministic asset/map generation (1).

Initial walking exposed the dockworker blocking the eastbound terminal
path. A two-cell boardwalk bypass resolved it; every old walkable position
and the blocked northern exit are preserved. In-game screenshots of both
landmarks and basin crossings were inspected. The final build and regression
logs are archived with v0.57. The v0.56 ROM hash is checked during packaging;
user saves are never touched by the tests or release script.

## v0.56 Amiens and Rouen verification - 2026-09-19

64 focused checks passed on the final build:

- 4 new walking/save checks: both districts, every loaded terrain cell,
  bridges, signs, preserved quests, cold Continue, Town Map and train/Celebi returns.
- 17 existing quest/travel checks: Amiens (3), bulletin (2), Rouen (3),
  route book (3), riverside (2), v0.35 book migration (1), Le Havre (3).
- 38 map checks, 2 original-terrain/layout checks, 2 dialogue-width checks
  and 1 deterministic-generation check.

The riverside migration test now boots its genuine v0.34 edge battery in
the archived ROM. Its previous setup incorrectly loaded a later cached-map
battery backwards into that ROM. The old-edge fixture and new-ROM migration
both pass. User saves were not used or changed.

Final logs and screenshots are archived with v0.56 in artifacts/releases.
The v0.55 ROM is retained and its SHA256 checked during packaging.

## v0.55 station and Beauvais verification - 2026-09-19

Each district was built and tested before the next. Final coverage is 61
focused checks:

- 4 station/Beauvais walking checks: migrated old batteries, full loaded terrain,
  signs, landmark approaches, Save/cold Continue, era maps and original exits.
- 3 station-post story, 4 evacuation, 2 garden reunion, 3 onward Amiens checks
  and 2 refuge walking/story checks, including real pending rail itineraries.
- 38 static map checks, 2 old-coordinate/layout-isolation checks, 2 sign-width
  checks and 1 byte-for-byte generation check.

A test battery was produced by normal walking/Save in the actual v0.54 ROM
at the expanded post coordinate (26,20), then loaded in this build. Its new
station layout and complete runtime terrain are verified. This addresses
v0.54's shared refuge/post layout, which had spread estate scenery to the post.
A permanent assertion now requires independent layouts for these maps.
All old on-foot coordinates retain elevation/behavior; the inaccessible moat
becomes forecourt. Beauvais keeps its original garden quest area and reception.
New artwork was inspected through actual mGBA screenshots. Logs/screenshots
are archived under artifacts/releases/v0.55-*. Previous ROM and player saves
are retained. This is focused regression, not the entire project test suite.

## v0.54 historical Chantilly verification - 2026-09-19

The expanded refuge/estate passes 55 focused checks:

- 2 new mGBA checks: old battery terrain, landmark/sign walking, preserved
  progress, district Save/cold Continue, historical map, Celebi round trip
  and completion of the original blanket quest.
- 5 original time-travel checks, 3 station-post checks and 4 evacuation checks,
  covering gates, No/B choices, unfinished visits, relocated characters and
  actual pending rail journeys.
- 38 static map checks, 2 old-position/hardware/reproducibility checks and
  1 dialogue-width check.

The 16x14 refuge expands east to 56x32. All formerly walkable coordinates
retain their elevation and terrain behavior. Cached refuge terrain clears on
load; story character flags remain controlled by the original map scripts.
Chateau/stables sprites are reused because these structures predate 1940.
The source history and reconstruction limits are in
 data/geography/HISTORICAL-CHANTILLY.md.
Screenshots were inspected in mGBA. Logs and screenshots are retained under
artifacts/releases/v0.54-*. The previous ROM and player saves are preserved.
This is focused regression coverage, not every project test.

## v0.53 coastal landmark verification - 2026-09-19

Dover and Calais were built and tested sequentially. The final combined ROM
passes 68 focused checks:

- 4 port walking/save checks: old batteries, full terrain comparison, landmark
  paths, signs, cold Continue, regional map return, ferry rounds and coach exits.
- 3 transport checks: badge gating, No/B, coach entry, ferry returns and an old
  genuine coastal rail booking resumed through Paris to Berlin.
- 13 walking/save checks across the six previously expanded modern towns.
- 3 historical London checks for gates, returns and saved rail detours.
- 38 static map checks, 2 port compatibility/hardware checks, 2 sign-width checks.
- 3 generation checks proving all eight modern landmark districts reproduce.

The first old Dover battery exposed the saved Island Harbor layout ID. Port
load now migrates that ID to the new individual layout before terrain loading,
while retaining every original terminal tile and player coordinate. Actual
mGBA screenshots were inspected for castle, cliff face, town hall and lighthouse.
The previous v0.52 ROM is retained; player battery saves are untouched.
Build/test logs and screenshots are archived under artifacts/releases/v0.53-*.
This is focused regression coverage, not a rerun of every project test.

## v0.52 regional landmark verification - 2026-09-19

Oxford, Chantilly and Oranienburg were implemented, built and tested in order.
The final combined ROM passes 67 focused checks:

- 6 regional walking/save checks: old batteries, all loaded terrain, landmarks,
  signs, bridges, cold Continue, map return, service approaches and trail links.
- 2 Oxford transport checks: old surfing battery/dismount and riverboat return.
- 7 capital district checks covering London, Paris and Berlin.
- 3 World Options checks including saved settings, registration and cycling.
- 3 historical London checks including old progress and onward/return travel.
- 38 static map checks, 3 old-coordinate/hardware checks and 3 text-width checks.
- 2 byte-for-byte generation checks covering all six landmark districts.

The pathfinder now excludes elevation-1 shoreline tiles even when their
behavior is normal; mGBA correctly blocks walking onto those water edges.
Regional sprite crops ignore alpha below 128 to prevent faint stray pixels
from shrinking visible architecture. Capital generation remains identical.
Build, test logs and screenshots are archived under artifacts/releases/v0.52-*.
This is a focused regression, not a rerun of the complete project suite.
Player saves are untouched; update with normal in-game Save and CONTINUE.

## Baseline

Upstream: `pret/pokefirered` commit
`c75f352304d529f6ba92d4f74b9cf8b5c3810788`.

The untouched FireRed build passed `make compare` with SHA-1
`41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`. Its ROM, symbols, and checksum are
preserved locally in `artifacts/baseline`. A full new game was also exercised
through the original introduction to the bedroom in mGBA.

## Verified gameplay

The modified ROM was exercised in the mGBA 0.10.5 core using actual emulated
button presses. Each gameplay stage was built and tested before proceeding.

- The custom European title boots and accepts Start or A into a new game.
  The rewritten Oak introduction and Eevee demonstration reach country selection.
- All nine regional starter choices lead to the correct city with exactly one
  level-8 partner. Tests decrypt the party species, check the saved choice,
  exercise No/B on every preview, and return from each list to country selection.
  B cannot bypass the initial country menu.
- Cyndaquil and Treecko evolve through the normal Rare Candy flow into Quilava
  and Grovyle, confirming that non-Kanto evolution is enabled.
- All twenty-four map files have valid event coordinates, reciprocal connections,
  door destinations, and reachable required paths.
- Every clinic can be entered/exited, heals the party, and handles a defeat
  without sending the player back to Kanto.
- Each countryside route connects back to its city, produces an encounter from
  its own roster, and allows the battle to finish.
- All thirty directed train journeys between six stations work. B, Exit, and selecting the current
  station leave the player in place with controls released. Arrival doors work,
  and travel preserves the original home country and party. Each journey now
  verifies every intermediate stop against an independent graph search.
- Normal Save -> fresh emulator -> Continue preserves the city, coordinates,
  home country, starter species, and party for all nine starter choices, all
  three standard starts, and a London-to-Berlin journey.
- The Bicycle can be used from Key Items and moves faster than walking.
- The European map opens from the Bag and from the registered SELECT shortcut
  at all six towns/cities. All twenty-four Europe maps retain the correct country indicator
  and return to the original position with controls released.
  Selection wraps, A shows rail information, and B/START return safely.
- Each city's landmark sign is reachable, and the southern paths can be walked
  in both directions. London's river blocks walking outside the crossing.
  Map boards grant a missing Town Map once and work on repeated visits.
- The Town Map and its registration survive Save -> fresh emulator -> Continue
  at all six stops; SELECT still opens the map after loading.
- A wild Pokemon can be caught through the normal battle Bag; it joins the party
  and play resumes on the countryside route.
- The three-city guide quest works in all six visit orders, using actual train
  journeys. Every city stamps once; only the third distinct stamp unlocks the
  single EXP. SHARE reward. Repeated conversations do not duplicate it.
- A full Items pocket leaves all stamps and the unclaimed reward intact.
  After a slot is freed, the guide awards the item exactly once.
- Partial and completed tours survive Save -> fresh emulator -> Continue.
  Speaking to the guide after reloading preserves progress and reward quantity.
- All three local trainers accept No/B without battling, use their intended
  two-Pokemon teams, award prize money on victory, and remember defeat.
  Repeated conversations do not restart battles or pay again. Losing heals the
  player at the correct clinic without awarding victory.
- A single team completes all three trainer challenges through normal train
  travel and clinic healing, with the progress report reaching 3/3.
- Every station supply shop supports cancellation, buys two Poke Balls for 400
  and one Potion for 300, and rejects purchases with zero funds. Inventory,
  money, control release, and the station exit are checked.
- All three individual trainer victories, combined 3/3 completion, and purchases
  in all six stations survive Save -> fresh emulator -> Continue. Talking to
  a defeated trainer after loading does not award another prize.

## London–Oxford extension

- The continuous London -> English Meadow -> Oxford Trail -> Oxford journey
  works in both directions on foot and by Bicycle, without forced encounters
  on the middle path. Oxford Trail is 40 tiles long, beyond the existing meadow.
  Both direction signs open and release controls; screenshots of the trail,
  Oxford, the rail menu, and the updated travel map were visually inspected.
- Oxford's clinic heals normally; its station doors and supply shop work.
  Its guide leaves the three-city stamp quest unchanged. The map board grants
  a missing Town Map once, and Oxford is selectable from every station.
- Oxford Trail produces its intended wild roster. A normal battle finishes
  back on the trail, and the controlled defeat test returns to Oxford's clinic
  with a healed party after visiting Oxford.
- Saving and cold-loading preserve progress in Oxford, on its trail, inside
  its station, after shopping, and after trains to Oxford and onward to Paris.
- A preserved v0.5 London battery save loaded in the new build with its starter,
  home country, and registered map intact, then walked to Oxford. This is one
  migration case, not a general compatibility guarantee for all earlier saves.

The walking extension was built and passed its tests before Oxford was added
to the train menu and travel-map selector. The final build reruns the existing
integration suite with four-city navigation, shops, and rail coverage.
The v0.6 integration run passed, including all twelve directed rail journeys
and 32 Save -> cold boot -> Continue cases.

## Paris–Chantilly extension

The Paris–Chantilly extension follows the same two-stage process: build and
verify the walking/cycling journey first, then add rail and map access.
`test_chantilly.py` exercises both directions through the French Gardens and
the 40-tile forest, town dialogue, clinic healing, station doors, direction
signs, encounters, battle completion, and defeat recovery at Chantilly.
The shared city checks include its shop, map board, and registered Town Map
in all four new maps. Save cases include the town, forest, station, shopping,
registered map, and journeys Paris -> Chantilly and Chantilly -> Berlin.

A preserved v0.6 Paris battery save also loaded and walked to Chantilly while
preserving Chikorita, home-country choice, and Town Map registration. Like the
earlier v0.5 case, this checks one known test save rather than every possible
old save or emulator configuration.

Screenshots of the new garden walk, forest signs, rail menu, and travel map
were visually inspected. Chantilly's map screen correctly identifies France.
The v0.7 integration run passed, including twenty directed rail journeys and
39 Save -> cold boot -> Continue cases. The release ROM matches the tested build.

## Berlin–Oranienburg extension

The Berlin–Oranienburg extension was built and tested before adding the sixth
rail destination. `test_oranienburg.py` verifies both directions on foot and
by Bicycle, park pond collision, clinic healing, station doors, unchanged stamp
progress, both trail signs, local encounters, battle completion, and defeat
recovery. Shared city checks cover its shop, map board, and Town Map access
from all four new maps. Save cases include town, trail, station, shopping,
registered map, and trains Berlin -> Oranienburg and Oranienburg -> London.

A preserved v0.7 Berlin battery save loaded in v0.8 and reached Oranienburg
with Treecko, the original home country, and map registration preserved. This
is one known migration case, not a general guarantee for all earlier saves.

The pond, park sign, and updated travel map were visually inspected. The
six-stop map keeps Oranienburg's country indicator set to Germany.
The seven-entry rail menu (six destinations plus Exit) was also inspected;
the greeting closes before it opens so the windows do not overlap.
The v0.8 integration run passed all thirty directed rail journeys and 46
Save -> cold boot -> Continue cases. The release ROM matches the tested build.

## Saved multi-stop rail journeys

The v0.9 railway uses the London–Paris–Berlin main line and branches to Oxford,
Chantilly, and Oranienburg. `test_rail_journeys.py` verifies No/B preview decline,
the four-train Oxford–Oranienburg journey, retaining or explicitly canceling a
booking, booking another destination, station exits, walking to the destination,
and recalculating the next connection after walking to a different station.
Malformed saved destination values 7 and 65535 are cleared safely.

`rail_test_helpers.py` derives expected paths from an independent adjacency
graph, then checks actual station arrivals, booking state, and the displayed
number of trains remaining. The train regression visits all thirty ordered
origin/destination pairs. Saved bookings use the previously unused variable
`0x40F7`; no save layout change is required.

Save tests include paused trips in London, Paris, and Berlin stations and
outside Berlin's station. After a cold restart they resume the booked journey
to completion. All existing save cases also check that booking state survives.
A preserved v0.8 Berlin battery save completed the new four-train journey from
Oranienburg to Oxford with its starter and home-country choice intact.

The destination/next-stop page and remaining-trains confirmation were inspected
visually. The final boarding flow avoids repeating the next-stop message.
The v0.9 integration run passed all thirty origin/destination routes and 50
Save -> cold boot -> Continue cases, including finishing each paused itinerary
after loading. The release ROM matches the tested build.

## Test details and limits

`scripts/run-tests.py` runs the checks in dependency order. The emulator never
opens a player's normal save file. Temporary states, isolated battery saves,
and screenshots are written under ignored `test-output`.

Healing and defeat tests deliberately set the test party's HP low in emulator
memory; the nurse and defeat recovery then run through the real game logic.
These fixtures are not modifications to the ROM. Capture uses normal catch
rates and retries when the Pokemon breaks free.

Map-board tests remove the Town Map from the test inventory to exercise the
gift path for continuing players; they do not claim a full old-release save
migration test. Outdoor path checks include tile behavior so water is not
mistaken for walkable ground. City screenshots were also visually inspected.

Trainer-loss tests use the same low-HP fixture as wild-battle recovery. Trainer
victories use the actual starter and ordinary attack inputs. Shop tests set
the test save's money to zero only for the insufficient-funds case.

Trainer team validation decrypts the actual enemy party slots: this engine's
trainer setup does not populate `gEnemyPartyCount`. The first test used that
unused count and was corrected. The initial French team proved too strong for
the basic fresh-starter test, so Ralts was replaced with a level-5 Oddish.
Trainer IDs 743-745 use existing reserved defeat flags; save layout is unchanged.

The Bag-capacity test fills the emulated Items pocket with Potion stacks, then
clears one slot. This isolates the reward's full-pocket and retry branches.
`test_tour.py` also checks the decrypted inventory quantity and persistent
stamp variables. The tour uses four previously unused saved variables
(`0x40F2` through `0x40F5`); home country remains at `0x40F0`.

The confirmed starter species is stored at `0x40F6`. Evolution tests insert one
Rare Candy and set the test party's cached level just below the evolution
threshold. The game's actual item handler updates experience and stats and
runs evolution. This fixture does not change normal starter levels or inventory.

Tests assert memory state as well as inspecting screenshots. A test-runner bug
initially checked the OAM flag instead of the battle flag; that was corrected
and all three country battle/recovery tests were rerun successfully.

These checks cover the first playable slice, not the entire inherited FireRed
game. Multiplayer, USA transfer, the original Kanto campaign, long-term save
compatibility, and future story features are not validated. The new map is a
schematic overview of the three implemented countries.
The normal desktop mGBA frontend has not been manually played in this session;
the gameplay checks use its emulation core headlessly.

## Earlier fixes and build verification

The v0.5 build uses a persistent Ubuntu cache under `~/.cache` and a
Windows-created archive for its initial source copy. Both initial and cached
builds succeeded; the final cached rebuild produced the same SHA-256 as the
ROM used for the gameplay tests. All nine starter paths, city/navigation
checks, and the existing gameplay regression checks passed before packaging.

- Removed an extra wait after the country menu that stalled script execution.
- Restored the clinic's standard Union Room initialization, required by the
  shared nurse dialogue, to prevent a healing-time memory overwrite.
- Bounded the original Sevii region lookup so new map sections cannot cause
  out-of-bounds reads when the original region map is requested.
- Corrected NPC IDs and starter-gift commands caught by the assembler.

The release ROM's SHA-256 is recorded beside it in `artifacts/SHA256SUMS.txt`.

## v0.10 regional challenge coverage

`test_challenges.py` walks from each existing trainer victory through a normal
clinic heal to the new trail trainer. It checks both decline inputs, exact
opponent species, wins and prize money, repeat conversations, and blackout
recovery. The starter-only playthrough uses the supplied Potions through the
normal battle Bag; it does not change player stats. Battle balance is checked
with the default Grass starter in each country, not every possible party.
Forced-loss cases deliberately reduce HP and battle stats.

`test_challenge_rewards.py` checks each regional guide's two-win requirement,
one Rare Candy, duplicate prevention, and full Items-pocket recovery. Missing
victory flags and full Bags are explicit fixtures; successful wins come from
the battle checks. `test_save.py` includes nine challenge cases: wins, claimed
rewards, and pending full-Bag rewards in each country. Reloaded pending rewards
remain claimable once after room is made; claimed rewards do not repeat.
All six trainer flags and the three reward variables are checked on reload.

An archived v0.9 Berlin battery save also loads with its partner, home country,
and registered map intact, then walks to Oranienburg and completes the rail
journey to Oxford. This verifies that particular migration case, not every
possible historical save. Trainer IDs 746–748 and variables 0x40F8–0x40FA use
reserved capacity without changing the save-block layout.

The v0.10 full integration suite passed, including all 59 cold Save/Continue
cases and all 30 directed train journeys. Release logs are preserved under
artifacts/releases/v0.10-tests.log and v0.10-legacy-save.log.

## v0.11 England story coverage

`test_england_story.py` checks mission acceptance and No/B declines for all
three home countries, directions before acceptance, both local trainer
prerequisites, and recognition of earlier real trail victories. The winning
playthrough carries the England challenge team through normal trains, clinic
healing, the Oxford rival battle, and the return report in London. It checks
the Pidgey/Eevee roster, prize money, battle declines, repeat conversations,
exactly one Soothe Bell, and full-Bag recovery. Missing prerequisite branches
use a trainer-flag fixture; forced-loss coverage reduces HP and battle stats.
The rival battle is balanced/tested with the trained Bulbasaur party and
normal Potion use, not every possible party or starter.

Five story save cases cover accepted mission, rival victory, report ready,
completed report, and pending full-Bag reward. Reloaded pending reports remain
claimable exactly once. The new trainer flag and variable 0x40FB use existing
reserved capacity, without resizing save blocks. A preserved v0.10 Oxford
battery save also keeps its partner, regional wins and reward, accepts the
new story, and unlocks the rival using those earlier wins. This migration
check covers that save, not every historical save state.

The v0.11 full integration suite passed, including all 64 cold Save/Continue
cases and all 30 directed train journeys. Release logs are preserved under
artifacts/releases/v0.11-tests.log and v0.11-legacy-save.log.

## v0.12 Oxford Gym coverage

`test_oxford_gym.py` exercises entrance/exit, advice, story prerequisites,
No/B declines, and a real leader victory using the completed story party.
The player uses Grass moves/Leech Seed and supplied Potions through normal
battle menus; no player stats are increased. The badge is checked immediately
after victory, along with TM39 and the automatically granted TM Case. Repeat
conversations cannot repeat money or the TM. Saturated-TM and full-Key-Items
fixtures check that the badge is retained and the TM remains claimable. Save
pointers are reacquired after battle before changing those fixtures.
Forced-loss coverage reduces HP and battle stats, checks clinic recovery,
and returns to the leader to verify the challenge remains available.

`test_gym_ui.py` opens the actual Trainer Card before and after the win,
checks that only the first badge appears, opens the TM Case, and opens the
European map inside the Gym (Oxford, not an inferred map-number grouping).
Four additional cold-save cases cover Gym entry, completion, and both kinds
of pending TM. They verify badge, leader defeat, TM quantity, reward variable,
and retry after making room. Battle balance is tested with the trained
Bulbasaur story party, not every possible starter/team.

The Gym is appended as Europe map 24, preserving previous map numbers.
Trainer 750, existing badge flag 0x820, and reserved variable 0x40FC preserve
the save layout. An existing v0.11 completed-story battery save can travel to
Oxford and challenge Ellis. Existing Gym tiles/art and first-badge engine
behavior are intentionally reused for this prototype.

The v0.12 full integration suite passed, including all 68 cold Save/Continue
cases and all 30 directed train journeys. Release logs are preserved under
artifacts/releases/v0.12-tests.log and v0.12-legacy-save.log.

## v0.13 French survey coverage

`test_france_story.py` verifies first-badge gating, No/B declines, and neutral
marker visits before the quest starts. It walks to both study sites in both
orders, checks that repeat visits cannot substitute for the other site,
requires both observations before Remy's review, and requires that review
before the Paris reward. Return visits to every participant and marker after
completion leave progress and the single Miracle Seed intact. A full Items
pocket is a capacity fixture; clearing one slot permits exactly one claim.
The normal winning Gym save supplies the first badge in the full suite.

Seven cold-save checkpoints cover accepted survey, each individual site,
both sites, reviewed report, completion, and a pending full-Bag reward.
Reopening each individual marker preserves its recorded state; Remy can
review reloaded notes, and Celine can reward a reloaded report once.

Reserved variable 0x40FD stores the survey state (0 unstarted, 1 accepted,
2 gardens only, 3 forest only, 4 both notes, 5 reviewed, 6 rewarded). No map
numbers or save-block sizes change. A preserved v0.12 completed-Gym battery
save also loads with its badge, TM and England story intact, and completes
the new survey in the focused migration playthrough.

The French wild-encounter check enters the grass below the new study marker.
Its previous scripted approach walked directly into the sign. After updating
that test route, encounter and blackout checks were rerun successfully; the
remaining regression checks continued on the unchanged ROM.

The v0.13 complete regression set passed, including all 75 cold Save/Continue
cases and all 30 directed train journeys. Consolidated results are preserved
in artifacts/releases/v0.13-tests.log; migration and focused survey results
are in v0.13-legacy-survey-tests.log.


## Chantilly Gym checks (v0.14)

The focused emulator playthrough imports a preserved v0.13 completed-survey
battery save, heals normally, walks the pool bridges, and defeats Marine using
the existing trained Bulbasaur and ordinary battle inputs. No stats are raised
for that victory. It checks Psyduck and Horsea, immediate Cascadebadge credit,
TM03, retained first badge/TM39, declines, and no repeated battle payout or TM.
The Trainer Card displays exactly two badges, the Town Map identifies Chantilly,
and the TM Case visibly lists Water Pulse alongside Rock Tomb.

Explicit fixtures cover all six unfinished survey states, a saturated TM03
stack, a missing TM Case with a full Key Items pocket, and a forced loss with
reduced player HP/defenses. These exercise locked challenges, pending rewards,
clinic recovery, and retry; they are not claims of unmodified difficulty runs.
Balance is verified with one trained starter, not every possible team.

Variable 0x40FE tracks the one-time TM03 reward. Trainer 751 stores Marine's
victory; map 25 is appended to the Europe group. Existing map numbers and save
block sizes remain unchanged. Four additional cold-save cases cover entering
the Gym, completion, and each pending reward condition. All save cases also
compare the second badge, TM03, its reward flag, and the new trainer flag.

The complete v0.14 regression suite passed on ROM SHA256
4327773638209b907d7b14654f46138c84c8ea5440660899069cf8733944b390,
including 79 cold Save/Continue cases and 30 directed train journeys.
Results are preserved in artifacts/releases/v0.14-tests.log, with the
v0.13 battery migration and focused Gym checks in v0.14-legacy-gym-tests.log.


## German courier chapter (v0.15)

A preserved v0.14 completed-Chantilly-Gym battery save loads with both badges,
claimed Water Pulse, and an unstarted courier mission. The focused check uses
normal buttons to leave the pool Gym, take trains to Berlin and Oranienburg,
accept and deliver the parcel, return the report, and receive one Magnet.
It tests No/B, Karl before acceptance, Lena before delivery, repeated visits
to both NPCs, and a full Items pocket followed by reward recovery.

Fixtures independently clear each required badge to check both prerequisites,
and fill the Items pocket to test deferred rewards. They do not award badges
or bypass travel in the normal completion playthrough. Walking routes retain
their existing integration checks; the courier completion uses trains.

Variable 0x40FF tracks 0 unstarted, 1 carrying parts, 2 carrying the report,
and 3 rewarded. No map IDs, trainer IDs, or save-block sizes change. Five new
cold-save checkpoints cover accepted, delivered, report-ready, completed, and
pending-reward progress. Every save case also compares this variable and its
Magnet count. Parcel and report are mission states, not inventory objects.


The v0.15 regression set passed on ROM SHA256
31cfd3f0a6a742248afa908c9fcfc7cb09c12758389552262ea80bcf8e334836,
including all 84 cold Save/Continue cases and all 30 directed train journeys.
The old 300-second runner limit interrupted the save suite after 83 passing
cases. The last pending-Magnet case and remaining bicycle/capture checks were
run separately on the unchanged ROM and passed. Future full save runs allow
420 seconds; --case can select an individual checkpoint for diagnosis.
Consolidated results are in artifacts/releases/v0.15-tests.log; the original
timeout and resumed output are also preserved alongside it. The focused
v0.14 battery migration results are in v0.15-legacy-courier-tests.log.


## Oranienburg Gym (v0.16)

The focused test loads a preserved v0.15 completed-courier battery save, travels
to Oranienburg, heals through the clinic, and challenges Conrad using ordinary
battle inputs and the existing level-14 trained starter. The test buys five
Potions with earned money at the station before the fight. An initial
unprepared run had no Potions left and lost; the prepared run wins without
raising stats. The driver explicitly selects Potion regardless of Bag cursor
position. Difficulty is checked with this team, not every starter. It checks the actual Voltorb
and Pikachu team, immediate third-badge credit, one Shock Wave TM, repeat-safe
payouts, and the Trainer Card, Town Map, and TM Case screens.

Fixtures cover all three incomplete delivery states, a saturated TM34 stack,
a missing TM Case with a full Key Items pocket, and forced loss through
reduced HP/defenses. These exercise gating, deferred rewards, and recovery;
they are separate from the ordinary victory playthrough. The decline test
waits for the Yes/No menu's input delay before sending its choice.

Unused variable 0x40EF records the TM claim. Repository search found no prior
use outside its definition. Trainer 752 and appended Europe map 26 leave
older map IDs and save-block sizes unchanged. Four additional cold-save cases
cover entry, completion, and both pending reward conditions. All save cases
compare the third badge, TM34, claim variable, and Conrad's victory flag.
The expanded 88-case save suite has a 450-second timeout.

The complete v0.16 regression suite passed without a timeout, including all
88 cold Save/Continue cases and all 30 directed train journeys. The tested ROM
SHA256 is 7a04dd3841aa04f18dea9f476656ce4e4036eb8b1162703d47d689660fcb6719.
Full results are in artifacts/releases/v0.16-tests.log; the preserved v0.15
battery migration and focused Gym tests are in v0.16-legacy-gym-tests.log.


## London�Oxford riverboats (v0.17)

A preserved v0.16 third-badge battery save loads on the boat build. Real-button
checks travel to both captains, read signs, reject boarding with No/B, and
complete free crossings in both directions. A fixture clears the third badge
at each landing to check locked service. The tests compare money, home country,
party species, courier progress, Magnet count, and rail booking across travel.
The Town Map identifies the destination correctly. Boarding while mounted on
the Bicycle returns to controllable outdoor movement; the movement check holds
the direction long enough for movement rather than using a two-frame tap.

A real Oxford-to-Berlin booking is made, then the player takes its first train
to London and detours back to Oxford by boat. The itinerary survives and the
Oxford clerk recalculates the remaining route and completes it to Berlin.
Four cold-save cases cover both landings, a mounted arrival, and a boat detour
with a pending rail journey; after reload they cross again or finish the booking.

No new map IDs, saved variables, or save structures are required. The new
captains use the existing third-badge flag. Static map checks verify that both
captains and their signs remain reachable. Visual inspection covers both
riverbank landings. Crossings use the normal warp transition, not boat animation.
The 92-case save suite has a 480-second timeout.

The complete v0.17 regression suite passed, including 92 cold Save/Continue
cases and all 30 directed train journeys. Both riverboat directions and a
rail detour work before and after reloading. Tested ROM SHA256:
c090b93deb70884fdf70e7bebf342b010137a67b86025181412e859172b25a81.
Results are preserved in artifacts/releases/v0.17-tests.log, with v0.16
battery migration and focused crossings in v0.17-legacy-ferry-tests.log.


## Rental Lapras riding (v0.18)

A preserved v0.17 battery save with the third badge loads on the riding build.
Focused tests reach both instructors through normal travel, check the badge
gate with a cleared-flag fixture, decline with No/B, and mount with normal
buttons. They compare the complete party byte-for-byte, money, home country,
and rail booking before/after rental. The player steers both ways on water,
dismounts onto clear ground, and repeats the rental. Bicycle-to-water-to-foot
transitions are also exercised. Surfing is faster than walking, so the test
releases direction input after each tile rather than assuming walking speed.

A real saved rail booking survives a rental and shoreline exit, then completes
to Berlin through the normal clerk. Four cold-save cases cover both water
locations, the bank after dismounting, and riding with a pending rail itinerary.
Reloaded riders retain Surf state, can dismount, and can complete the booking.
The existing ferry tests run alongside these checks.

No new saved variables, flags, map IDs, or party changes are introduced.
Arrival on the existing surfable tile initializes the engine's normal Surf
state; entering clear ground uses its existing dismount behavior. These are
short town-water rides, not a custom mount system or a long water route.
Visual inspection verifies the generic rider rendering. The 96-case save
suite has a 510-second timeout.

The complete v0.18 regression suite passed, including 96 cold Save/Continue
cases and all 30 directed train journeys. Reloaded riders retain Surf state,
dismount normally, and complete a pending rail trip. Tested ROM SHA256:
294bf8b83731f3231d003d3498fd2b837e2d78eb9dca5dffed58a031f9808066.
Results are in artifacts/releases/v0.18-tests.log, with the v0.17 battery
migration and focused rentals in v0.18-legacy-riding-tests.log.


## Coastal ferry destinations (v0.19)

A preserved v0.18 third-badge battery save loads on the coastal build.
Real-button tests take each station coach, decline with No/B, cross from both
ports and back, and use each north return exit. Cleared-badge fixtures check
both coaches and both captains. Travel compares the complete party bytes,
money, home country, and rail booking. Port Town Maps show the correct country,
selected destination, and ferry/coach information. Screenshots verify the
reused harbor artwork and both added travel-map nodes.

A real Oxford-to-Berlin booking survives a riverboat detour, London coach,
and Dover-to-Calais ferry. The return coach reaches Paris, whose normal rail
clerk finishes the saved journey to Berlin. Four cold-save cases cover Dover,
Calais, a return-city arrival, and Calais with the pending itinerary. Reloaded
port saves complete round trips and exits, or resume the booked train journey.

Europe map IDs 27 and 28 and region-map sections are appended. Existing IDs,
save layouts, and six-stop rail tables remain unchanged. The travel map now
has eight browsable destinations; navigation checks verify wraparound in both
directions. Ports have existing harbor layout/artwork, no encounters, and use
London/Paris clinic respawns. No new saved quest state is needed. The expanded
100-case save suite has a 540-second timeout.

The complete v0.19 regression suite passed, including 100 cold Save/Continue
cases, eight-destination map navigation, and all 30 directed rail journeys.
Reloaded port saves complete crossings, return coaches, and the Berlin rail
detour. Tested ROM SHA256:
eb9f366af7aa4ed18ca084e7a97bf31312f98c5cead5f43697159ffed06077c9.
Results are preserved in artifacts/releases/v0.19-tests.log; v0.18 battery
migration and focused crossings are in v0.19-legacy-coastal-tests.log.


## Tree edge correction (v0.19.1)

Replaced exposed interior forest metatiles with native canopy, side, and trunk
edges on all twelve European outdoor maps. Tile collision/elevation bits and
map coordinates are preserved. The initial map generator applies the same
edge finishing. Layout map.bin and border.bin files now explicitly invalidate
maps.o, so binary-only map edits rebuild the ROM correctly.

Six existing battery saves cold-booted successfully on the corrected ROM.
Real-button walks reached each town's southern and western forest boundaries;
emulator screenshots verified the finished edges. Static map/path checks,
all six city checks, and the Oxford, Chantilly, and Oranienburg route suites
passed, including walking/cycling both ways, clinics, stations, signs, local
encounters, and defeat respawns. This patch used focused regression checks;
the complete 100-case save suite was last run for v0.19.

Tested ROM SHA256: 8a59c7160d56a5a06c28593d349180152eb49ead67f3dbd57523f08a67bbe725.
Results: artifacts/releases/v0.19.1-tree-tests.log. Representative screenshots:
v0.19.1-london-trees.png and v0.19.1-chantilly-trees.png in the same directory.


## Celebi prologue (v0.20)

Ada in Oxford offers a Thunderbadge-gated investigation. Celebi beside the
Chantilly Forest path offers an optional dialogue vision, followed by a return
report and one Rare Candy. VAR_EUROPE_CELEBI_STORY aliases reserved 0x40EE;
no save structures or map IDs change. The sighting is not a battle, capture,
or time-travel warp. Historical maps and the larger WWII arc remain future work.

Real-button checks cover the badge gate, premature forest visit, No/B at both
prompts, acceptance, repeated directions, the picture opening/closing, recorded
sighting, return report, repeated visits, and full-Bag reward recovery. Existing
starter and third-Gym battery saves are cold-loaded on the new build. Party
bytes, money, home country, regional quests, and rail-booking value are compared
through the chapter. Six new normal Save/Continue checkpoints cover acceptance,
arrival at Celebi, the sighting, return report, completion, and a pending reward;
reloaded players can continue their quests or collect exactly one reward.

Adjacent regression checks cover all six town landmarks/map boards, the Oxford
and Chantilly walking/cycling routes, clinics, stations, signs, encounters and
respawns, both French survey orders, and booked rail transfers/cancellation/
detours. Tree-edge screenshots are retained during battery migration. These
checks passed before a final dialogue-width adjustment; chapter/save/map and
portrait checks were repeated on the final ROM. The complete suite was not
rerun for this release. Its runner now includes the prologue and 106 save cases
with a 570-second save-test timeout.

Final ROM SHA256: eb420253a145b60dd020fde209f0ab0fe1b022192495cb4d192f3249692b206c.
Release logs: v0.20-celebi-tests.log and v0.20-adjacent-regression.log in
artifacts/releases. Portrait and forest screenshots accompany the release.


## First historical visit (v0.21)

Celebi now transports players with a completed prologue to a fictional
Chantilly station-refuge courtyard in 1940. The fixed Celebi return NPC is
available before, during and after the blanket task. The historical map is
appended at Europe map ID 29, with a new layout and region section; existing
map IDs stay unchanged. Reserved variable 0x40ED tracks arrival, Elise's request,
the keeper's blanket and completion, separately from prologue variable 0x40EE
and all regional quests. No save structure changes are needed.

Real-button mGBA checks cover the unreviewed-report gate, No/B in both eras,
immediate round trips, returning midway and resuming, the sign, quest order,
repeat NPC conversations, and a one-way blanket handoff without Bag items.
Party bytes, decoded contents of every Bag pocket, money, all badge flags,
home country, rail booking and present quest variables remain intact through
crossings and the historical task. Raw encrypted inventory bytes can change
when the engine relocates save blocks, so tests compare decoded quantities.
Cycling becomes walking on arrival. A real Chantilly-to-Oxford rail itinerary
survives a walking/time-travel detour from Paris, then completes at its clerk.

Seven normal Save -> cold boot -> Continue cases cover departure readiness,
arrival, Elise's request, carrying the blanket, returning midway, completion,
and a booked train detour. Reloaded players finish the task and return, or
resume the train itinerary. The existing prologue tests and its six cold-save
cases also passed. All 30 Europe maps passed static bounds/link/path checks.
Six existing town battery saves loaded successfully; present-day map browsing,
registration, both exit keys, and town/route/station/clinic context passed.
The historical map UI labels France, 1940 and identifies its schematic as a
present-day reference with a Celebi return reminder. Visual checks cover the
courtyard, tree edges, Eevee portrait, blanket handoff and era-aware map.

This release used focused regression coverage, not a rerun of the entire
suite. The full runner includes test_time.py and now has 113 cold-save cases,
with a 630-second save-suite timeout. Existing artwork represents a compact
fictional refuge, not a reconstruction of a documented station. The wider
wartime story remains unfinished; this area has no battles or wild encounters.

Tested ROM SHA256: 698fe2b513d75b43748d9d79393a01201d22dac76acf11809273ec409decbaff.
Logs: artifacts/releases/v0.21-time-tests.log and v0.21-regression-tests.log.
Screenshots of the refuge, Eevee, handoff and map accompany the release.


## Historical station news (v0.22)

A guide at the 1940 refuge unlocks after the blanket task. The station post
is appended at Europe map ID 30 and reuses the existing courtyard layout.
Players read its notice, obtain dispatcher confirmation, and deliver the
message to the refuge keeper. Elise and present-day Ada acknowledge completion.
Reserved variable 0x40EC stores this task separately from 0x40ED (blanket) and
0x40EE (prologue); existing map IDs and save layouts remain unchanged. Both
historical areas retain a Celebi portal to the present-day forest. Re-entry
always arrives at the refuge and does not reset historical progress.

Real-button checks cover the blanket gate, No/B on both guides, attempted
early confirmation/report, repeated notice/dispatcher visits, leaving and
resuming across eras, delivered news, repeat completion, and Ada's dialogue.
Crossings preserve party bytes, decoded Bag contents, money, badges, home
country and present quests. A long walk can legitimately update friendship;
the Ada check compares party bytes immediately around her conversation and
other invariants across the journey. An actual saved Oxford rail itinerary
survives the station-post detour and completes afterward. That case uses a
setup fixture for completed blanket progress, not for the rail booking.

Six new normal Save/Continue cases cover acceptance, copied notice, confirmed
news, return to the present, delivered report and the pending train journey.
Reloaded players complete the task or train trip. The original refuge chapter
and its seven cold-save cases also pass on the final ROM. All 31 Europe maps
pass static checks. Visual inspection covers the post notice, refuge report
and the era-aware travel map. Six-town map navigation and legacy town battery
migration passed before the final refuge-only guide-spawn correction.

A v0.21 save inside the refuge originally retained its three-NPC template list.
Loading now restores the fourth stationary guide template, and a return-to-field
script spawns the guide immediately. scripts/test_departure_migration.py uses
the archived v0.21 ROM to create a battery save directly beside the future
guide; the final ROM loads it and can talk to him without a movement step.
This archived-ROM migration check is separate from the normal suite.

This release uses focused regressions, not a complete-suite rerun. The full
runner includes test_departure.py and 119 cold-save cases with a 690-second
save timeout. Historical train departure and larger wartime locations remain
unfinished; this milestone is a fictional information-gathering task.

Tested ROM SHA256: 224419f88cd34f6b0410b62524b756d0d4e5577da75586701b57e5d32476c390.
Release logs: v0.22-chapter-tests.log, v0.22-adjacent-regression.log, and
v0.22-legacy-migration.log in artifacts/releases. Notice, report and map
screenshots are stored alongside the release.


## Historical train and Beauvais reception (v0.23)

After the departure report, the station-post board offers a historical train
to Beauvais reception. Europe map ID 31 and its region section are appended;
the room reuses the rival-house interior. A host checks Elise and Eevee in,
and Celebi or the south return-service exit takes the player out. A return
warp is appended to the station post on an ordinary non-warp ground tile;
it serves as the reception exit's destination without auto-triggering travel.
Reserved 0x40E5 tracks not departed, arrived, and checked in. Existing variables,
map IDs and save structures are preserved.

Elise's refuge object uses a temporary hide flag, derived from saved arrival
progress on map transition/return to field. Her old location stays empty after
travel and after saving in the refuge. Reception keeps her available before
and after check-in; revisiting never resets progress. Ada acknowledges a
completed check-in. Town Map text identifies Beauvais, 1940 while retaining
the existing present-day diagram and Chantilly entry-point selection.

Real-button checks passed for the delivered-report gate, No/B, boarding,
arrival, host/Elise interactions in both stages, repeat conversations, the
south exit, repeat trips, direct Celebi return, Elise's relocation, Ada's
acknowledgement and an actual booked Oxford journey after the historical train.
The booking case uses a delivered-news setup fixture; the rail itinerary is
from the existing real-booking checkpoint. Transition and conversation checks
preserve party bytes, decoded Bag contents, money, badges and present quests;
long walking comparisons allow normal friendship changes. Leaving before
check-in, returning through the refuge and reboarding also completes normally.

Five new cold Save/Continue cases cover boarding readiness, arrival, completed
check-in, the old refuge after relocation and a pending present-day itinerary.
The six station-news cold-save cases and original refuge gameplay regression
also pass. All 32 Europe maps pass static link/bounds checks. Visual inspection
covers reception, welcome text, Eevee's portrait, the now-empty old location,
and the historical Town Map. Dialogue widths fit the standard text window.
The station-news notice helper now explicitly declines the boarding offer
when inspecting the board after completion.

This release used focused coverage, not a complete-suite rerun. The full
runner includes test_evac.py and 124 cold-save cases with a 720-second timeout.
The journey uses dialogue and a transition, not moving train artwork. The
interior is placeholder art; the wartime journey is fictional.

Tested ROM SHA256: 904dacff26d9c330979d3d1cb1393e1c357d3514b040ec223da875e30156cd58.
Logs: v0.23-train-tests.log, v0.23-regression-tests.log and
v0.23-unfinished-visit.log in artifacts/releases. Reception, portrait,
relocation and map screenshots accompany the release.

## v0.24 - A message home and Ada's first account

Elise offers an optional message after Beauvais check-in. The refuge keeper
replies, Elise acknowledges the reply, and Ada in Oxford records the account
and awards one Luxury Ball. VAR_0x40E4 tracks five saved stages without changing
the save layout. Completed visits retain appropriate dialogue and progress.

Focused real-button emulator checks passed for the check-in gate, No/B,
acceptance, delivery, reply, era detours, no early archive reward, repeat visits,
and a one-time reward. A full Poke Balls pocket leaves the reward pending;
freeing a slot grants exactly one ball. Party, money and earlier quest progress
remain intact across the checked conversations.

Six message Save -> cold boot -> Continue cases passed: active, delivered,
acknowledged, report-ready, complete, and full-pocket pending. Five train save
cases also passed: ready, arrival, complete, returned, and pending rail booking.
The train gameplay regression passed, including leaving before check-in,
returning later, Elise's relocation and preserving an actual Oxford itinerary.
Existing battery saves load through Continue. The Elise train helper declines
the optional message offer to keep the earlier quest checks independent.

Visual inspection passed for the offer, Ada's account, archived acknowledgement
and full-pocket dialogue. New text widths fit the standard dialogue window.
This release used focused coverage, not a complete-suite rerun. The full runner
now includes test_message.py and 130 cold-save cases with a 780-second timeout.

Tested ROM SHA256: 95934c5602043840e5505abd2a11a1b20f2eebec14676e6e60f31dd2ea89ad8a.
Logs: v0.24-message-tests.log and v0.24-regression-tests.log in artifacts/releases.
Dialogue screenshots accompany the release. The wider wartime story remains
in development.

## v0.25 - Beauvais relief supplies and repeatable rest

After Ada records the first account (message stage 4), the Beauvais host offers
an optional care-parcel request. The station dispatcher supplies it and the
host accepts delivery. VAR_0x40E3 stores 0 none, 1 requested, 2 parcel and
3 rest unlocked; no save format or map ordering changes. Ada points players
to the host after recording the account. The parcel occupies no Bag slot.

Real-button checks passed for the archive gate, No/B at acceptance, reminders,
collection, repeated dispatcher visits, delivery, a detour through Celebi,
and repeat visits after completion. Full Items-pocket fixture checks confirm
collection/delivery neither need space nor alter Bag contents. Rest is a
separate Yes/No interaction after delivery; declining with No/B preserves
health. Accepting restores HP, status and PP without charging money or changing
items, Pokemon identity, or earlier quest progress. Repeated rest works.
A damaged/burned/zero-PP fixture and a six-member fixture with one fainted slot
verify healing through the actual host interaction; fixture Pokemon are cloned
only inside the test emulator, never in player saves.

Six new normal Save -> cold boot -> Continue cases passed: ready, active,
parcel, returned to present, complete and tired party. Each can resume and use
the rest service. Earlier historical train and message gameplay regressions
passed, including relocation, unfinished check-in, real pending Oxford rail
travel, message refusal, one-time reward, full Poke Balls pocket and retry.
Three earlier cold-save cases passed: evac-complete, message-pending and
message-complete. Legacy mode loads existing battery saves through Continue.

New dialogue was measured with normal, male and female font tables; maximum
width 212 pixels within the 216-pixel limit. Visual inspection passed for the
parcel offer, rest offer and healed acknowledgement. This is a dialogue-based
care corner using the existing reception interior, without new room artwork.
The wider historical storyline remains in development.

This release used focused coverage, not a complete-suite rerun. The full
runner includes test_relief.py and 136 cold-save cases with an 840-second limit.
Tested ROM SHA256: 4c783910045076b0cd8b09c396fdce5a819330e97533dfe4b0a187ec47346afe.
Logs: v0.25-relief-tests.log, v0.25-save-tests.log and v0.25-regression-tests.log
in artifacts/releases. Supply and rest dialogue screenshots accompany them.

## v0.26 - Beauvais garden and Luc's Pidgey

After the supply parcel is delivered, Elise offers a garden visit. The new
24x20 map is appended as Europe map 32, retaining all earlier map identities.
It reuses existing General/Pallet tiles and sprites, with complete forest
edges, flower beds, a return guide and a Celebi anchor. The historical Town
Map recognizes the garden as Beauvais, 1940. Earlier exits are unchanged.

VAR_0x40E2 saves four reunion stages: none, learned whistle, Pidgey found and
reunited. The bird is shy before Luc's request; after pickup it disappears
from the trees, then appears beside Luc on reunion. Derived temporary flags
restore its proper location on transitions and return to field. This is a
scripted story companion, not an addition to the battle party or Bag.

Real-button checks passed for the relief prerequisite, No/B on entry, exit
and Luc's request, initial shy bird, hints, pickup and reunion. Both exits,
reception healing during the search, a present-day detour, repeat visits and
both bird locations passed. Conversation/transition checks preserve party,
money, Bag contents, badges and earlier quests; normal walking can change
friendship. Legacy mode boots existing battery saves through Continue.

Six garden normal Save -> cold boot -> Continue cases passed: ready, active,
found, reception, returned to present and complete. Each resumes the reunion
and verifies the bird's location. Earlier supply/healing and message gameplay
regressions passed, including full Bags, six-party healing and pending rewards.
Three earlier cold-save cases passed: relief-complete, relief-tired and
message-complete. All 33 Europe maps pass static link/bounds/path checks.

Visual inspection passed for the entrance/tree edges, northeast search area,
reunion dialogue and historical Town Map. New dialogue measures at most 204
pixels with all three standard Latin font-width tables, within 216 pixels.
The first test route was corrected to walk around Celebi's occupied tile.
This release used focused coverage, not a complete-suite rerun. The full runner
includes test_garden.py and 142 cold-save cases with a 900-second timeout.

Tested ROM SHA256: 305fef8bbddc293a02a891c80821273bd6ee794e2654e1993e432002ab0e44a3.
Logs: v0.26-garden-tests.log, v0.26-save-tests.log and v0.26-regression-tests.log
in artifacts/releases. Garden/reunion/map screenshots accompany the release.
The wider wartime story and further historical locations remain planned.

## v0.27 - Town Map story journal

SELECT on the European Town Map opens a Celebi journey journal. A switches
between the current lead and seven milestone records; SELECT returns to the
map and retains the selected destination. B/START closes either view through
the existing caller. Reopening starts on the map. The journal reads existing
quest variables and the Thunderbadge; it writes no new persistent state.

Twenty-five current leads cover the badge prerequisite, Ada and the vision,
refuge blanket, departure news, reception check-in, message/reply/account,
care parcel, garden search and reunion. Pending reward leads identify the
required Bag pocket. Milestones require the corresponding completed stage,
so a reward still awaiting Bag space is not shown as complete.

Real-button checks passed against 27 existing battery saves loaded through
Continue, covering every lead and both full-pocket pending rewards. Checks
verify the expected lead and milestone mask, both journal pages, SELECT
round-trip, ignored directional input in the journal, retained map selection,
existing map browsing/travel help and return to the Bag. Party bytes, money,
Bag contents, badges, quest variables and location remain unchanged.
Registered-map checks pass for B/START, fresh reopening and field movement.
Two new normal Save -> cold boot -> Continue cases reconstruct the pending
account and completed garden journal correctly. The garden gameplay regression
also passes, including both exits, healing, era detour, bird relocation and
historical Town Map context.

Visual inspection covers early/late leads, the pending vision reward, partial
and completed milestones. All map/journal strings fit the 226-pixel content
width; the widest is 214 pixels in FONT_SMALL. This release used focused
coverage, not a complete-suite rerun. The full runner includes test_journal.py
and 144 cold-save cases with a 900-second timeout. No new story chapter or
regional Gym/stamp journal is added in this release.

Tested ROM SHA256: 876cf8731e2eae8c4b3d99f47490f002323be2a070e862d1c08c61a855fb4944.
Logs: v0.27-journal-tests.log, v0.27-save-tests.log and v0.27-regression-tests.log
in artifacts/releases. Journal screenshots accompany the release.

## v0.28 - Regional journal topic

Up/Down inside the journal switches between the Celebi journey and Europe
tour while retaining the lead/milestones page. A changes pages; SELECT returns
to the map without changing its destination selection. Reopening the journal
starts on the Celebi lead. Map directions remain normal destination browsing.
Shoulder keys retain the original Help function; an initial shoulder-button
prototype was replaced after the emulator exposed the Help conflict.

The regional topic adds 25 leads covering the England study, trail opponents,
rival, France's either-order survey, Germany's delivery, three Gyms and their
pending TMs, missing city stamps, pending EXP. SHARE and completion. Seven
independent records show stamps, claimed tour reward and badges. Pending TMs
do not erase earned badges. Gym/story leads take priority over optional stamps;
stamps may still be collected at any point. No new save variables are used.

Real-button journal tests passed on 28 existing battery checkpoints loaded
through Continue. Two targeted trainer-win fixtures cover the remaining
England prerequisite branches; five stamp-variable fixtures cover missing
stamps, pending reward and completion. Full Key Items fixtures replace one
Bicycle with a Town Map while retaining all occupied slots and no TM Case.
Normal Bag compaction is allowed in inventory comparisons; item quantities,
party bytes, money, badges, quest variables and location remain unchanged.
The stamp fixture refreshes the save-block pointer after returning from Bag.

Checks cover both topic directions, switching on both pages, correct saved
records, returning to map, default topic on reopening and START exit to Bag.
All 27 existing Celebi journal checkpoints and registered-map B/START/field
controls passed again. Two new Save -> cold boot -> Continue cases verify
regional pending-TM and completed-tour views. The completed-tour checkpoint
uses the documented stamp-variable fixture, not a newly played full tour.

Visual checks passed for regional introductions, survey reminders, pending
story/Gym/tour rewards and completed records. All map/journal strings fit
226 pixels in FONT_SMALL (maximum 214). This release used focused coverage,
not a complete-suite rerun. The full runner includes test_tour_journal.py and
146 cold-save cases with a 900-second timeout. No new story chapter is added.

Tested ROM SHA256: d751e5fb100928f9eaa84840b13b35811bf1ad0bd65275586b4c2d281ecd6af6.
Logs: v0.28-tour-journal-tests.log, v0.28-save-tests.log and
v0.28-journal-regression.log in artifacts/releases, with selected screenshots.

## v0.29 - Onward to Amiens and meeting-point briefing

After the garden reunion, the Chantilly post dispatcher offers a free onward
train to Amiens. The old noticeboard still boards Beauvais. Amiens is appended
as Europe map 33; its new courtyard layout reuses the garden tiles/tree borders
with a lighter central area, a noticeboard, Nora, return guide and Celebi.
VAR_0x40E1 tracks none, arrived, briefed, notice read and confirmed. No earlier
map IDs or save layout change. The guide returns to the post; Celebi returns
to the present forest. The service is fictional, not a historical timetable.

Nora asks the player to read the meeting instructions and confirm them with
her. Reading before the briefing cannot skip it. Repeat conversations and
travel preserve completion. The journal adds four leads after the onward
invitation and an eighth historical milestone. The map labels Amiens, 1940;
a named location selector replaces the former nested location expression.

Real-button checks passed for the reunion gate, boarding and return No/B,
early notice, briefing, confirmation, repeats, leaving before briefing and
returning later, and a mid-task Celebi detour. The old Beauvais train remains
usable after unlocking Amiens. A separate unlock fixture on a checkpoint with
an actual modern Oxford booking verifies Amiens travel, Celebi return and
completion of that booked journey. The fixture sets garden/relief completion;
it does not fabricate the modern booking. Dialogue/transition checks preserve
party, money, Bag, badges and prior progress; normal walking may alter friendship.

Six normal Save -> cold boot -> Continue cases passed: ready, arrival, briefed,
notice, returned and complete. Every case can finish Nora's objective. Garden
gameplay and all 27 earlier journal checkpoints pass again, including registered
map controls. All 34 Europe maps pass static link/bounds/path checks. The new
journal leads and final 255-bitmask milestone display pass real UI checks.

Visual inspection covers the arrival, Nora, noticeboard, Amiens map label,
current lead and eight completed records. Dialogue widths fit 216 pixels
(maximum 210); map/journal text fits 226 pixels (maximum 214). No new battle,
item reward or historical train animation is introduced. Further Amiens story
remains planned. This release used focused coverage, not a complete-suite
rerun. The full runner includes test_amiens.py and 152 cold-save cases with a
960-second timeout.

Tested ROM SHA256: d30a25016eb7a64e5f0bee62eb1070892082a994fa675563a900426031393676.
Logs: v0.29-amiens-tests.log, v0.29-save-tests.log, v0.29-regression-tests.log
and v0.29-map-tests.log in artifacts/releases, with selected screenshots.


## v0.30 - Amiens reunion (2026-09-18)

Focused verification on the final ROM; the entire integration suite was not
rerun. Real mGBA button input passed the arrival prerequisite, Nora's No/B
choices, both witness orders, repeat conversations, early verification
checks, reunion and Meowth relocation. Party, money, Bag, badges and modern
quest state remain unchanged by the conversations. Checks cover the return
service and a Celebi detour, with six new journal leads and milestone bit 8.

Seven normal Save -> fresh boot -> Continue checkpoints cover active, Mira,
porter, both reports, verified, present-day detour and completed states. Each
resumed to completion and checked Meowth at its new position. A separate
migration check creates a real battery save using archived v0.29 beside the
future Mira, then verifies immediate interaction on the new ROM.

The v0.29 arrival regression passed, including its No/B choices, early notice,
repeat visits, Beauvais service and a genuinely booked modern rail journey.
All 27 earlier historical journal cases passed, including registered-map
B/START exits and field movement. Static checks passed for all 34 custom
maps, including access to the new characters. Dialogue fits the 216-pixel
text area (maximum 215); journal text fits 226 pixels (maximum 214).

Visual inspection caught a bool8 truncation of the ninth milestone's DONE
marker. The mask now uses u16 and completion is converted to an explicit
boolean. The final rebuild, reunion checks and seven cold saves were rerun;
the nine-row completed checklist was visually verified. An earlier journal
run overlapped the rebuild and failed; the full 27-case final-ROM rerun passed.
The full runner now includes reunion checks and 159 cold-save checkpoints.


## v0.31 - Amiens party care (2026-09-18)

Focused final-ROM mGBA tests passed; the full integration suite was not rerun.
Nora does not heal before the reunion. After reunion, Yes restores HP, status
and PP, while No/B preserves the complete tired party. Repeat care, return
service, Celebi travel and a v0.30 completed-reunion battery save passed.
A targeted six-member fixture includes depleted PP, burns and a fainted slot;
all members heal with a full Items pocket. Non-health Pokemon identity,
items, money, badges and all historical/present quest variables are checked
around the healing interaction. These health and capacity fixtures are
explicit setup edits; travel, dialogue and care use actual button input.

Two normal Save -> cold boot -> Continue cases preserve tired/rested health
and allow care afterward. The full reunion regression passes both report
orders, prerequisites, repeated dialogue, relocation, returns and journal
milestones. The old reunion helper explicitly declines Nora's new care offer
so its unchanged-party assertion still checks only reunion interactions.
The full runner now includes the care test and 161 cold-save checkpoints.

Dialogue widths remain at most 215/216 pixels; map/journal text is at most
215/226 pixels. Screenshots of Nora's choice and completed journal guidance
were visually inspected. No map layout or save-variable allocation changed.


## v0.32 - Ada's Amiens account (2026-09-18)

Focused mGBA verification, not a complete integration-suite rerun. The new
account test uses older battery saves and actual travel from Amiens through
Celebi and the regional railway to Oxford. Ada does not offer the account
before the reunion. Afterward, No/B leaves it unrecorded, Yes records it,
and repeat reports preserve party, Bag, money and other story progress.
The player revisits Amiens, checks Meowth's relocation and uses Nora's care
service after recording the account. No artificial quest unlock is needed.

Pending and completed report checkpoints passed normal Save -> cold boot ->
Continue and subsequent Ada interaction. The journal checks lead 34 before
recording, lead 35 afterward, and the tenth milestone (mask 1023). Earlier
journal cases also exercise topic switches and registered-map B/START exits.
The full runner includes the new account scenario and 163 cold-save cases.

Visual review caught clipped glyphs at ten-pixel row spacing. Historical
records retain eleven-pixel spacing and move their action hint down to fit
ten rows; screenshots of the final checklist and account lead are readable.
All new dialogue fits 216 pixels (215 maximum); journal text fits 226 pixels
(214 maximum). An initial test process exited without diagnostic output;
the return-trip diagnostic and full final-build scenario both passed on rerun.


## v0.33 - Checked Amiens travel bulletin (2026-09-18)

Focused final-ROM mGBA checks; the full suite was not rerun. Real button input
checks the archived-account prerequisite, porter's No/B choices, early board
and Nora interactions, reading the bulletin, porter verification, delivery
to Nora and repeated conversations. Five journal leads describe the actual
saved stage. The existing ten-milestone checklist is unchanged. Checks also
cover a Celebi detour midway and the return service after completion.

Six normal Save -> fresh boot -> Continue checkpoints cover ready, active,
board copied, present-day detour, checked and delivered states; each resumes
to completion. The save verifier now checks the new variable on every case.
The full runner includes this scenario and 169 cold-save checkpoints.

The prior Ada-account regression passed its prerequisite, Oxford journey,
No/B, repeat report, journal, Amiens revisit, Meowth relocation and party care.
Dialogue fits the 216-pixel text area (215 maximum); journal text fits 226
pixels (214 maximum). The checked-news and completed-waiting-plan journal
screenshots were visually inspected. The bulletin explicitly states that no
onward service is available yet; return travel remains usable. Map layouts,
NPC placement, inventory and rewards are unchanged.


## v0.34 - Onward Rouen journey (2026-09-18)

Focused verification, not a full integration-suite rerun. Real mGBA button
input passed the bulletin prerequisite, boarding and return No/B choices,
arrival, repeated Leon welcome, Celebi No/B and return, unfinished re-entry,
three journal leads and Rouen historical map context. A separate booking
check uses an actual booked modern journey plus explicit historical unlock
fixtures; after visiting Rouen and returning through Celebi, that original
rail booking resumes successfully. Conversation/travel checks preserve
party, money, inventory, badges and present-day quest state.

Four normal Save -> cold boot -> Continue cases cover ready, arrival,
present-day detour and welcomed states; each resumes to the welcome. The
save verifier checks Rouen progress for every case. The full runner includes
Rouen and now has 173 cold-save checkpoints. The prior Amiens bulletin test
passes with the new train explicitly declined in its repeat-porter helper.

All 35 custom maps pass event bounds, connections and path checks. Rouen
reuses the tested Amiens layout; its map ID and region section were appended
without renumbering existing entries. It has no cycling, running, escaping
or wild encounters, and uses the historical Chantilly respawn. The engine's
OLD_MAN_1 sprite constant corrected an initial link error before emulator
checks. Dialogue fits 216 pixels (215 maximum); journal text fits 226 pixels
(214 maximum). Arrival and historical-map screenshots were visually checked.


## v0.35 - Rouen riverside layout (2026-09-18)

Focused final-ROM verification; the complete integration suite was not rerun.
Rouen has a separate 36x20 layout, expanded east of the old 24x20 courtyard.
Static checks pass on all 35 custom maps and assert that every previously
reachable courtyard tile remains reachable. River cells are not walkable;
both banks, crossing and reception paths are reachable. Existing events,
arrival coordinates and map IDs are preserved.

Real-button mGBA tests walk both banks and the crossing, attempt to walk into
water and the outer forest, and return to Leon. Screenshots of the northern
bank, southern bank and crossing were visually reviewed, including tree caps,
trunks and side edges. Updated notice dialogue fits all three text fonts.

The first old-save test exposed the saved layout ID and cached old tiles.
A Rouen-only migration updates the layout and clears its cached map view when
the saved layout differs, preserving coordinates and all quest state. A real
v0.34 battery save made at (21,16), beside the old east boundary, loads at
that exact location and can immediately walk to the expanded bank. The normal
full runner skips the archived-ROM migration; --legacy enables that check.

Normal Save -> cold boot -> Continue passes on the far bank and four existing
Rouen checkpoints. The complete Rouen travel regression also passes boarding,
return and Celebi No/B, welcome, journal/map context and resumption of a real
modern rail booking. The full runner now includes riverside walking and 174
cold-save cases. No new quest stage or reward is introduced in this release.


## v0.36 - Rouen route-book recovery (2026-09-18)

Focused final-ROM checks; the full integration suite was not rerun. Real
mGBA button input covers the arrival prerequisite, Leon's No/B, acceptance,
reminder, far-bank pickup, return and repeat dialogue. Pickup visibility is
checked nearby before acceptance, while active, after collection and after
returning. Travel through Amiens and Celebi preserves progress. Four journal
leads and unchanged party, inventory, money and modern progress are checked.
A full Items-pocket fixture still permits collection and completion without
consuming or adding inventory items.

Five normal Save -> cold boot -> Continue stages (ready, active, found,
present-day detour and completed) resume to completion and verify that the
pickup stays removed. The save verifier checks the new variable in every
case. The full runner includes this quest and 179 cold-save checkpoints.

A standalone migration test creates an actual v0.35 battery save beside Leon
using the archived ROM, then loads the new ROM, accepts immediately and
collects the newly spawned book without leaving the map. The new object
template is refreshed for old Rouen saves and its temporary visibility flag
is restored from persistent quest progress. The archived-ROM check remains
separate from the normal full runner.

The prior Rouen travel regression passes No/B choices, welcome, both exits,
map/journal context and resuming an actual modern rail booking. All 35 custom
maps pass static checks, including the pickup's accessible approach. Dialogue
fits the 216-pixel text area (216 maximum); journal text fits 226 pixels
(214 maximum). The pickup and active-journal screenshots were inspected.


## v0.37 - Rouen party care (2026-09-18)

Focused final-ROM mGBA checks; the entire integration suite was not rerun.
Returning the route book unlocks free care but does not automatically heal.
No/B preserves tired-party health. Yes and repeat use restore HP, status
and PP. Care remains available after the Amiens return route and a Celebi
round trip. An existing completed route-book battery save unlocks it directly.
A six-member fixture with burns, empty PP and a fainted slot verifies whole-
party healing. A full Items pocket does not block care. Non-health Pokemon
identity, inventory, money and story variables remain unchanged.

Two normal Save -> cold boot -> Continue cases preserve tired/rested health
and permit care afterward. The route-book regression passes its request,
pickup visibility, return, No/B, repeats, travel, full Bag and journal checks.
The full runner includes Rouen care and 181 cold-save checkpoints.
Dialogue fits 216 pixels; map/journal text fits 226 pixels. The care offer
and completed journal guidance were visually inspected. An initial test
started before the delayed build finished and saw the old behavior; all
reported tests were rerun on the completed final ROM and passed.


## v0.38 - Paged historical records (2026-09-18)

Focused final-ROM checks; not a complete integration-suite rerun. Historical
records now show ten entries on page one and three on page two. New bits
record the delivered Amiens bulletin, Rouen welcome and returned route book.
The existing u16 milestone mask holds all thirteen entries. No new save
variable is needed; completed older quests automatically populate the list.

Five real battery-save stages (empty, Amiens account, Rouen arrival, Rouen
welcome and route-book complete) pass mask checks, both paging directions,
page wrap, lead/records toggle, topic reset, map round trip and read-only
exit. The second page displays incomplete and completed entries correctly
in visually inspected screenshots. The regional topic stays on one page.
Two normal Save -> cold boot -> Continue cases preserve empty/full progress
and allow the same paging checks afterward.

All 27 earlier historical journal cases and registered-map B/START exits
pass. The regional journal suite passes 28 saved cases plus targeted trainer
and stamp fixtures. Expected masks in affected newer quest tests now include
the additional completion bits. The full runner includes paging checks and
183 cold-save checkpoints. All journal text fits the 226-pixel area.


## v0.39 - Historical Le Havre connection (2026-09-18)

Focused final-ROM mGBA verification, not a full-suite rerun. Real button input
passes the route-book prerequisite, Rouen boarding No/B, port arrival,
captain welcome and return No/B, repeat visits, Celebi choices and unfinished
re-entry. The blocked north entrance prevents accidental travel into an
unconnected map. The port label and journal objectives are verified, and
paging checks confirm the fourteenth milestone with mask 16383. Screenshots
of the harbor, map label and second records page were visually inspected.

Four normal Save -> cold boot -> Continue cases resume before departure,
after arrival, after a present-day detour and after the welcome. A separate
migration test makes an actual archived v0.38 battery save beside the new
Rouen clerk and successfully boards immediately on the new ROM. Its object
template is restored for old saves. New map, region and layout entries are
appended; existing identifiers and Rouen event positions are retained.

A genuine modern rail booking plus explicit historical-unlock fixtures
survives the port journey and resumes afterward. The Rouen care regression
passes its gate, both return routes, No/B, old completed saves, six-member
healing and full Bag. All 36 custom maps pass bounds and path checks; the
validator selects harbor metatile attributes for harbor layouts. Dialogue
fits 216 pixels and journal text fits 226 pixels. The full runner includes
Le Havre before paging tests and now covers 187 cold-save checkpoints.


## v0.40 Le Havre dock instructions

The final ROM built successfully. Focused mGBA input tests passed the welcome
gate, early notice and captain interactions, request No/B, all three task
steps, repeated conversations, both return routes and four journal leads.
The completed journal has fifteen milestones (mask 32767); its second page
was visually checked with all five rows visible and marked DONE. The notice
interaction was also visually checked at the closed entrance.

Five normal Save -> cold boot -> Continue cases passed: ready, accepted,
notice read, returned to the present and completed. A genuine archived
v0.39 save made beside the new worker starts and completes the task on the
new ROM without leaving the map. The prior Le Havre travel regression also
passed, including preservation and resumption of a real modern rail booking.

All 36 custom-map bounds/path checks passed, including the worker approach.
Dialogue width checks pass at 216 pixels; journal text fits 226 pixels.
The full runner now includes this task and 192 cold-save checkpoints.
This release ran the focused tests above, not the entire suite.


## v0.41 Le Havre dockworker care

The final ROM built successfully. Focused mGBA input tests passed the
dock-task gate, completion without automatic healing, No/B, free repeat
healing of HP/status/PP, and both return routes. An existing completed
v0.40 battery-save checkpoint unlocks care immediately. Targeted health
fixtures exercised damage, burn and depleted PP; an explicit six-member
party/full Bag fixture included a fainted slot. Healing preserved Pokemon
identity, inventory, money, rail booking and quest progress.

The full dock-instructions regression passed its welcome gate, early
interactions, request choices, repeated conversations, four leads and
fifteen-record paging. Seven normal Save -> cold boot -> Continue checks
passed: tired/rested care states and all five dock-task checkpoints.
The care cases verify health survives reloading and care remains usable.

The care offer and updated journal lead were visually checked in mGBA
screenshots. Dialogue fits 216 pixels; journal text fits 226 pixels.
The full runner now includes dock care and 194 cold-save checkpoints.
This release ran the focused checks above, not the entire suite.


## v0.42 Ada's port account

The final ROM built successfully. Focused mGBA input tests passed the dock
confirmation prerequisite, an actual Oxford rail journey, No/B, recording
the account and repeated reports. Party, items and other quest variables
remain unchanged. An existing completed dock-task battery checkpoint can
report immediately. A real Le Havre revisit retains the account and free
dockworker care; returning to Ada again retains the recorded report.

Three normal Save -> cold boot -> Continue checks passed: before reporting,
after reporting and after returning to the port. The new account variable
is included in journal read-only snapshots and save preservation checks.
Ada's earlier Amiens account regression also passed its gates, choices,
journey, report, journal and revisit/care checks.

Eight historical journal states passed page wrapping, lead toggling, topic
reset and read-only exits. All sixteen completed milestones produce 65535;
the existing unsigned rendering handles bit 15 correctly. Screenshots of
the finished lead and second page were inspected: six DONE rows fit with
the controls visible. Dialogue fits 216 pixels; journal text fits 226.
The full runner now includes the port report and 197 cold-save checkpoints.
This release ran the focused checks above, not the entire suite.


## v0.43 Celebi direct port revisits

The final ROM built successfully. Focused mGBA input tests passed the port
account gate, the original refuge route before the unlock, initial No/B,
destination-menu Exit/B, both destination choices and repeated direct port
visits. Existing recorded-account battery saves unlock the menu immediately.
All tested trips preserve party, inventory, money and quest variables.
Dockworker care, the Rouen return and the Celebi return remain functional.

A genuine pending modern rail booking survived the shortcut and resumed
afterward. That case uses an explicit historical-unlock fixture on the
existing rail itinerary; the other unlock case uses the recorded-account
checkpoint. Three normal Save -> cold boot -> Continue cases passed in the
forest, at direct port arrival and after returning to the forest, with the
shortcut usable after each reload.

The port-account regression also passed its prerequisite, real Oxford trip,
No/B, report/repeat, sixteen-record paging and normal-route port revisit.
The destination menu was visually inspected; its labels and underlying
dialogue fit. Dialogue checks fit 216 pixels; journal text fits 226 pixels.
The full runner now includes the shortcut and 200 cold-save checkpoints.
This release ran these focused checks, not the entire suite.


## v0.44 Southampton crossing and reception

The final ROM built successfully after shortening one over-width dialogue
line. Focused mGBA input tests passed the recorded-account gate, clerk No/B,
crossing, arrival, host welcome and return choices, repeated visits, blocked
north entrance, both return routes and dockworker care after returning.
The historical Southampton map correctly uses England's modern reference
node. A genuine modern rail booking survived the journey and resumed;
that case uses explicit historical-unlock fixtures on a real itinerary.

A genuine v0.43 battery save made beside the future ferry clerk boarded
immediately on the new ROM. The new object's template is restored on load;
existing map, layout and region identifiers remain stable with new entries
appended. Four normal Save -> cold boot -> Continue cases passed before
departure, after arrival, after a present-day detour and after the welcome.

The journal now carries a 32-bit completion mask across two task fields.
Nine old/new progress states passed paging, topic reset, lead toggling and
read-only exits, including all seventeen records (131071). The high word
clears for regional records and restores for the historical topic. The new
map, completed lead and second records page were visually inspected; all
seven second-page records and controls fit. All 37 map path checks passed.
Dialogue fits 216 pixels and journal text fits 226 pixels.

The previous direct-port shortcut regression passed its choices, returns,
care and real rail-booking resumption. Concurrent cancellation tests exposed
a shared temporary snapshot filename; each process now uses its own file,
and the Southampton suite passed on rerun. The full runner includes this
chapter and 204 cold-save checkpoints. This release ran the focused tests
above, not the entire suite.


## v0.45 Southampton luggage task

The final ROM built successfully. Focused mGBA input tests passed the host
welcome gate, request No/B, acceptance, reminder, pickup and return. The
pickup appears only while requested, disappears when collected and stays
hidden after completion and revisits. Both return routes work during the
task, including a present-day detour while carrying the bag. An explicit
full Bag fixture still allows collection and return without altering the
inventory or party. Repeated conversations do not duplicate progress.

A genuine v0.44 battery save made beside the new worker starts and completes
the task without leaving the map. The worker and pickup templates refresh
on load; visibility derives from the saved quest variable. Five normal
Save -> cold boot -> Continue cases passed: ready, active, found, returned
to the present and complete. Each resumes the task or verifies completion.

Four journal leads and the eighteenth record passed. Ten journal progress
states passed paging, topic reset and read-only exits, including mask
262143 for all eighteen milestones. Pickup dialogue and the eight completed
rows on page two were visually inspected. Dialogue fits 216 pixels and
journal text fits 226 pixels. All 37 map path checks passed.

The Southampton travel regression passed its gates, welcome, choices,
return routes, care, historical England map context and real modern rail
booking resumption. The full runner includes luggage and 209 cold-save
checkpoints. This release ran these focused tests, not the entire suite.


## v0.46 Southampton party care

The final ROM built successfully. Focused mGBA input tests passed the
luggage-task prerequisite, hand-in without automatic healing, No/B and
repeat free healing of HP/status/PP. Both return routes retain care. An
existing completed luggage battery save unlocks care immediately. Targeted
health fixtures exercise damage, burn and depleted PP; a six-member party
fixture includes a fainted slot and a full Bag. Healing preserves Pokemon
identity, inventory, money and all historical/regional quest variables.

Two normal Save -> cold boot -> Continue cases passed, verifying damaged
and healed health data survive and care remains usable after reloading.
The luggage regression passed its welcome gate, choices, pickup visibility,
return, repeats, both travel routes, four leads, eighteenth milestone,
paging and full Bag handling. The care menu and updated journal lead were
visually inspected. Dialogue fits 216 pixels and journal text fits 226.
The full runner now includes Southampton care and 211 cold-save checkpoints.
This release ran the focused checks above, not the entire suite.


## v0.47 Direct Southampton revisits

The final ROM built successfully. Focused mGBA input tests passed the
luggage-completion gate, initial No/B, destination Exit/B, all three
destinations and repeated direct Southampton visits. The pre-unlock menu
still exits at its original third entry. Existing completed luggage battery
saves unlock the expanded menu immediately. Every trip preserves party,
inventory, money and all saved historical/regional quest variables.

Southampton care and both return routes passed. A genuine modern rail
booking survived direct Southampton travel and resumed afterward, with
explicit historical-unlock fixtures on the real pending itinerary. Three
normal Save -> cold boot -> Continue cases passed in the forest, at direct
arrival and after returning, with the shortcut and care usable after reload.

The earlier Le Havre shortcut regression passed its gate, choices, routes,
care and rail-booking resumption. The luggage regression passed its gate,
choices, pickup/return, visibility, repeats, full Bag case, journal leads
and eighteen-record paging. The expanded destination menu was visually
inspected. Dialogue fits 216 pixels; journal text fits 226 pixels.
The full runner now includes the shortcut and 214 cold-save checkpoints.
This release ran these focused tests, not the entire suite.


## v0.48 Southampton account

The final ROM built successfully. Focused mGBA input tests passed the
luggage prerequisite, actual Oxford journey, No/B, recording and repeated
reports. Party, inventory, money and previous quest progress are preserved.
An existing completed luggage battery checkpoint can report immediately.
A direct Southampton revisit retains the report and free party care; a
second Oxford visit retains the recorded account.

Three normal Save -> cold boot -> Continue cases passed before reporting,
after reporting and after revisiting Southampton. The new variable is
included in save preservation and read-only journal snapshots. Ada's earlier
Le Havre report regression passed its prerequisite, choices, real journey,
report/repeats, journal and revisit/care behavior.

Eleven historical progress states passed paging, topic reset, lead toggling
and read-only exit. All nineteen milestones produce mask 524287. The second
page's nine DONE rows and completed lead were visually inspected with no
clipping. Dialogue fits 216 pixels; journal text fits 226 pixels.
The full runner now includes this account and 217 cold-save checkpoints.
This release ran the focused checks above, not the entire suite.


## v0.49 Historical London reception

The final ROM built successfully. Focused mGBA input tests passed the
Southampton-account prerequisite, boarding No/B, arrival, Rose's welcome,
repeated conversations and both exits. The return guide works before and
after the welcome, and unfinished visits resume after a Celebi detour.
Southampton care remains usable after returning. London uses the historical
map label and modern England reference correctly. A real modern rail
booking survived the London journey and resumed; that case uses explicit
historical-unlock fixtures on a genuine pending itinerary.

A genuine v0.48 battery save made beside the future transport clerk boarded
and checked in immediately on the new ROM. Its template is restored on load;
map, layout and region identifiers are appended. Four normal Save -> cold
boot -> Continue cases passed before departure, after arrival, after a
present-day detour and after the welcome. The London variable is included
in save preservation and journal read-only snapshots.

Twelve historical journal states passed page wrapping, lead toggling, topic
reset and read-only exit. All twenty milestones produce mask 1048575. The
arrival scene, historical map and all ten second-page DONE rows were
visually inspected. All 38 map path checks passed after adding London's
return guide to the validator. Dialogue fits 216 pixels; journal fits 226.

The direct Southampton shortcut regression passed its gates, all choices,
returns, care and real rail-booking resumption. The full runner includes
London and 221 cold-save checkpoints. This release ran these focused tests,
not the entire suite.


## v0.50 Geography and World Options foundation

ROM build passed. Emulator input tests passed map-board item grant and
duplicate protection, all eight map selections, cosmetic identity/party
preservation, normal Save/cold Continue preferences, restoration of the
original avatar, real Bag registration, SELECT opening and START return,
cycling avatar changes and dismount. The first movement test used a stale
save-block address after menu transitions; reading the live pointer fixed
the test and confirmed identity preservation. All 38 static map path checks
passed. Geographic data generation is byte-for-byte reproducible. Map,
options and avatar screenshots were inspected. No full-suite run, surfing
regression, or town-layout overhaul is claimed by this checkpoint.


## v0.51 Capital landmark districts

The release adds London/Paris/Berlin walking-map districts and independent
landmark tilesets. Each capital was built and tested before the next. Static
checks cover all old traversable positions, unchanged land/water/elevation,
GBA metatile/palette limits, and all 38 existing map path/link checks. Real
input tests compare every loaded capital map tile with its authored data,
walk the new districts, read signs, cross bridges, save normally and cold
Continue. Berlin's central Gate passage is traversable. London also checks
the clinic/station and an old surfing save; Paris and Berlin reconnect to
the countryside. Screenshots were inspected for all six landmark sprites.

The surfing check exposed the existing SavedMapViewIsEmpty out-of-bounds
read: clearing the cache could still appear nonempty, restoring zero tiles.
The loop now uses the actual array bound. The same old battery dismounted
correctly in v0.50, failed before this fix, and passes after it. All final
capital reload tests now check the complete terrain buffer to catch this.

Early test-harness corrections accounted for legitimate walking friendship
gains and the clinic's central exit tile. The final ROM was then retested
for all three districts, World Options persistence, registered-item use and
cycling avatar continuity. The historical London regression was also run.
This is a focused regression pass; the entire project suite was not run.
