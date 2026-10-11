# Eclipse verification â€” 2026-10-11

Separate clone: `S:/pokemon-europe-shadow`, branch `codex/europe-eclipse`.
The original project's tracked source and player saves were preserved.

## Delivered systems

- 21 chapters, eight badge battles, recurring counter-starter rival, Team
  Eclipse, WWII resistance missions, League council and champion ending.
- 42 campaign shelter/route maps, 78 country era maps and Krakow sanctuary: 39 independently
  authored compact districts, landmarks, a country passport and station menu.
- 292 new trainer teams, repeatable practice, six shadow rescues, saved care,
  purification, evolution lock, damage modifiers and purple battle palettes.
- Bidirectional era travel, sepia historical colors, 39 saved local decisions,
  two present-day outcomes, an all-country epilogue and one-time reward.
- World Gear: Normal/Easy/Hard, independent optional Nuzlocke, and optional
  rate-based visible encounters and a 1,025-species country reserve roster.
- Seven stationary legendary guardians: three before the League and four
  after the ending, native sprites/battles, story/care gates and saved catches.
- Native credits and ordinary Start-menu saving.

## Native checks

Static checks verify trainer IDs, all scripted references, dialogue widths,
map connectivity and every NPC/landmark approach. The final agbcc build links
successfully: 261,196 bytes EWRAM, 29,824 bytes IWRAM, 17,266,984 bytes linked ROM,
padded to 32 MiB. RAM headroom is limited and must be checked on future additions.

Emulator checks include all nine starters from New Game, all rival counters,
all three campaign entrances, decline and chapter gates, nurse and route travel,
real difficulty-adjusted opponent levels, World Gear controls, visible wild
battles, rescue and purification, duplicate protection, and native Save/cold
Continue. All 39 countries pass both era transitions, landmark access, palette
restoration, saved garden/archive consequences and a cold restart with all
choices retained. Credits return to the field; the epilogue gives one Master
Ball without duplication.

A real battle faint verifies Nuzlocke retirement, blackout/healing restrictions,
OFF healing and ON retirement restoration. First-encounter allowances, shared
past/present limits, matching visible species and field-spawn toggles are checked
through native interaction. Those tests use explicit low-HP and escape-speed
fixtures to isolate rules. No player's actual save is opened by the test runner.

All 21 main chapter victories pass, with all eight native badge flags and
game-clear set. A cold Continue retains the completed journal and ending.
All 39 historical victory callbacks pass and unlock their local choices. A
single emulator host-process SIGILL stopped the main progression at Zurich;
resuming its checkpoint passed Zurich and subsequent chapters. This occurrence
was not reproduced and remains a reason for broader emulator/hardware checks.

Battle-progression tests use accelerated damage and survival fixtures, while
still exercising the real battle victory callbacks. They verify chapter and
badge transitions and historical-operation unlocks; they do not establish
natural difficulty or a full grinding/balancing playthrough. Country-choice
travel tests set the operation-clear bits to isolate map consequences; separate
combat checks exercise the actual operation victories. Epilogue UI tests set
39 memory bits to isolate reward and duplicate handling.

## Balance and rule follow-up — October 11, 2026

All nine starter choices won the revised level-six opening rival battle using
normal button inputs, original HP/stats/PP/EXP, and native opponent AI. Each
advanced the story and reached level eight. This is narrow opening evidence,
not a complete natural-level campaign playthrough. The tester asserts the
compiled move-table stride (12 bytes); earlier results using nine bytes are
invalid and excluded from balance conclusions.

A separate native Totodile run won the rival, healed normally, trained through
five repeatable Oxford practice sessions and incidental wild battles to level
thirteen, then won the Rock gym and reached level fourteen. The badge and
chapter survived a cold Continue. No stats, HP, PP, levels or EXP were injected.
An immediate level-eight gym attempt lost; route preparation is necessary.
The current campaign replay also passed all chapter callbacks through the
champion, native credits, cold ending saves and the one-time epilogue reward.

The actual second-encounter Ball action reaches the dedicated Nuzlocke refusal
script, returns the Ball, leaves party size unchanged and permits the battle
to continue. Retirement, both-era encounter limits, difficulty opponent levels
and field-sprite toggles also pass. Native bag navigation in the tester now
respects pocket clamping after a Ball has been used.

## Second badge natural playtest

A cold-loaded first-badge save trained through seven normal London practice
sessions, incidental wild battles and native evolution to Croconaw at level
eighteen. The Paris Water gym passed twice, in thirteen and fifteen attack selections,
reaching level nineteen, with the second badge/chapter preserved on cold
Continue. This remains one starter/team path, not proof of balance for every
team. An earlier automated attempt stalled; Psyduck can Disable a move, so the
tester now excludes the native disabled move from selection. No game balance
change was inferred from that stalled attempt.

## Local storage follow-up

All 21 shelters and 78 country-era districts now provide a native storage
attendant. Static checks cover NPC capacity and approach reachability, and
require exactly one attendant in every country-era map. Cold-save runtime
checks open Move Pokemon and return safely from a shelter, a present district
and a wartime district, with unchanged party counts/species and field controls
restored. The native storage system supplies deposit, withdraw and box tools;
no new RAM buffers or storage rules were introduced.

## Gym TM rewards

All eight leaders supply their themed TM once, including when revisited from
an existing completed save. Rewards and claim flags (unused flags 0x8C6-0x8CD)
survive cold Continue; native item delivery supplies a TM Case. Explicit
full-stack fixtures verify that failed delivery keeps a reward unclaimed and
that making room allows exactly one collection. A naturally earned second-badge
save teaches Water Pulse to Croconaw through the TM Case, consumes one TM,
updates only the selected move/PP and persists the result through a cold save.
The leader does not replace a consumed TM. No reward test changes catch rates,
trainer AI or battle damage.

## Third badge and party stability

A naturally earned second-badge save catches a full-HP Pidgey with one ordinary
Poke Ball, switches its lead partner through the native party menu, and trains
through six Grass-route practice sessions from level seventeen to twenty-two.
The Flying partner wins the third gym and reaches level twenty-four. A cold
Continue preserves the badge and team; a final-ROM replay also wins. These
runs use ordinary stats, encounter/catch rates, trainer AI and experience.
Native optional opponent-switch prompts are now handled by the tester, avoiding
repeated attempts to send out a partner already in battle.

The base party menu leaked both temporary tilemap buffers after each party-slot
swap. They are now freed and cleared after the animation's final use. A native
20-swap test verifies NULL buffer pointers, stable allocated heap use, unchanged
party order after an even number of swaps, and restored field controls. Native
storage access in shelters and both country eras also passes after the fix.

The supplies test starts from the naturally earned third-badge save. Native
shop scrolling and cancellation pass, and earned money buys Thunder and Moon
Stones for exactly 2,100 each. A rescued shadow Pikachu refuses the stone
without consuming it. Ordinary caretaker visits purify it; native item use
then evolves it to Raichu and consumes one stone. Cold Continue preserves the
evolution, purification, inventory and story progress. Storage access in a
shelter and both country eras, plus earned Water Pulse teaching, also pass
on this release.

The natural Amsterdam run continues from the earned third-badge team and
purified Raichu save. Ordinary station travel reaches Belgium, where a
full-HP Nidoran is caught in two native Poke Ball attempts. Two Grass-route
practice battles raise it to level 22 and Nidorina; the purchased Moon Stone
evolves it into Nidoqueen. Five more practice battles reach level 25. The
Normal level-25 Electric gym is won in six move selections, reaching level 26.
Cold Continue preserves the four-partner team and fourth badge. A final replay
also checks the actual badge flag and earned Shock Wave TM (seven selections).
No encounter, catch-rate, stats, damage, experience or AI fixtures are used in
this run. The runner handles delayed grass transitions and Abra teleport
outcomes. Purification and Raichu evolution also pass again on this ROM.

The natural Berlin run continues from the earned fourth-badge save. Five
Grass-route practice battles raise the original Flying partner from level 24
to 27, learning Wing Attack through the native move-replacement menu. Six
Berlin practice battles then reach level 29. The Normal level-29 gym is won
in six move selections, reaching level 30. Native Save and cold Continue
preserve the four-partner team, fifth badge, Wing Attack and Brick Break TM.
No levels, stats, damage, experience or AI were overridden. An initial attempt
to train a level-24 Pidgeotto directly in Berlin frequently fainted; the leader
now suggests earlier Brussels practice if a Flying partner struggles.
A final-ROM Berlin replay also wins (five selections), and Amsterdam's
natural fourth-gym regression passes (seven selections) with its cold-save
checks after the battle-runner update.

The natural Prague and Vienna runs continue from the earned fifth-badge
checkpoint on the current release ROM. The same four-partner party defeats
Prague's level-32 Eclipse handler in 15 move selections, then Vienna's
level-35 Psychic gym in eight. Neither chapter needs extra practice battles.
Native Save and a fresh-emulator cold Continue preserve stage 7 after Prague
and stage 8 after Vienna. No party, progress, inventory, encounter, damage,
experience or AI memory writes are used. Reproduce with
`scripts/test_eclipse_natural_prague.py`, then
`scripts/test_eclipse_natural_vienna.py`. The latter also reports a native loss
without advancing progress if a future balance change makes this party fail.
These checks establish natural campaign progression through the sixth badge.

Zurich initially defeats the same party with its level-37 Magneton, Haunter and
Houndoom. A preparation run teaches the earned Brick Break TM to the level-30
Nidoqueen through the native TM Case, replacing Double Kick and retaining Bite.
The first Magneton/Haunter practice trainer can still cause a native blackout.
The finalized reproducible route uses the Houndoom/Pidgey trainer instead:
13 victories raise Nidoqueen to level 37, then Veil is defeated in five move
selections. Native Save and cold Continue preserve the consumed TM, learned
Brick Break and stage 9. Run `scripts/test_eclipse_natural_zurich.py`; `--training`
resumes a saved preparation and `--resume` replays the boss from its trained save.
An earlier mixed-trainer preparation also defeated Veil in six selections.

The saved Zurich party then wins Rome's level-40 Fire gym in 15 selections
(16 in the earlier preparation branch). `scripts/test_eclipse_natural_rome.py`
checks the actual seventh badge, earned Overheat TM and stage 10 before and
after a fresh-emulator cold Continue. All preparation, battles, healing, TM
teaching and saving use native controls with no stats, inventory, progress,
experience, damage or AI writes. The natural battle runner now handles a late
grass encounter interrupting a route trainer's menu, finishing the wild battle
before retrying the conversation.

Madrid's level-43 gym is won in 16 move selections with the saved Rome party.
`scripts/test_eclipse_natural_madrid.py` checks all eight actual badge flags,
the Earthquake TM and stage 11 before and after a fresh-emulator cold Continue.
Lisbon initially defeats that party. `scripts/test_eclipse_natural_lisbon.py`
teaches the earned Earthquake TM to Nidoqueen, replacing Poison Sting through
the native TM Case. Thirteen ordinary Rome Fire-route practice victories raise
Nidoqueen to level 45. An attack-only retry still loses: Weezing's Explosion
knocks out the healthy lead, leaving undertrained partners against Magneton.
The successful Normal, non-Nuzlocke retry buys five Hyper Potions and one
Revive with earned money (7,500 total), then spends two Hyper Potions and the
Revive through the native battle Bag. The handler falls in six attack
selections; stage 12, Earthquake and the consumed TM survive cold Continue.
The runner selects healing targets using the Bag's current party order after
switches. This establishes one ordinary-item route through the battle, not
Nuzlocke balance or item-free viability. `--resume` repeats it from the saved
trained Lisbon checkpoint.

`scripts/test_eclipse_natural_past.py` enters Paris 1940 through the naturally
unlocked Lisbon porter. Declining travel leaves the player in place; returning
to Lisbon restores modern colors and preserves story progress. The level-46
patrol is defeated in seven attack selections, spending two remaining Hyper
Potions. Native Save and cold Continue preserve stage 13 and the past palette.
This exposed a release bug: FireRed's Continue recap restored untinted palette
backups even when the saved map was historical. `QuestLog_BackUpPalette` now
stores the saved map's sepia tint for both tiles and object palettes. The
regression compares all 13 map palette slots and the player's sprite colors.
`scripts/test_eclipse_past_continue.py` also cold-saves a historical French
country district, checks both palette sets after Continue, returns to its
modern district and verifies modern colors after another cold save. All four
new runners pass on the rebuilt release. No stats, inventory, story progress,
experience, damage, AI, encounter or RNG memory writes are used. Native item
purchases and consumption are asserted.

Warsaw initially defeats the four-partner team in six attack selections.
`scripts/test_eclipse_natural_warsaw.py` returns to the already completed Prague
shelter, collects its level-29 shadow Houndour, purifies it through native care,
and evolves it into Houndoom after two Vienna Abra/Kadabra practice battles.
The rescue bit, purification count and evolved partner are checked. Purchases
of three Hyper Potions and one Revive cost 5,100 in earned money. The prepared
five-partner team wins Warsaw in 11 attack selections (12 in an earlier saved
branch), spending none of those supplies. The native saved party and historical
tile/player colors survive cold Continue. `--probe` records the original team;
`--resume` repeats the boss from the saved preparation.

This exposed a test-runner error: its type-only scoring chose Earthquake against
Weezing despite Levitate. The scorer now excludes that ability immunity. Native
battle Pokemon menus also support specified matchup switches, choose an
appropriate surviving replacement, and use the announced opponent in the free
Shift prompt. Optional finishing logic accounts for Speed stages and paralysis;
healing normally starts below half HP instead of repeatedly healing at two-thirds.
These are runner input-policy changes, not edits to battle stats or native AI.

`scripts/test_eclipse_natural_berlin1944.py` uses Nidoqueen against Magneton,
Crobat and Houndoom, with the purified Houndoom against Hypno. The finalized
replay wins in 11 attack selections using three Hyper Potions; an earlier
paid-switch replay won in nine using one. Historical tile/player palettes and
stage 15 survive cold Continue. Declining travel leaves the player in Berlin;
returning to modern Geneva restores modern colors, which persist after another
native save and cold restart.

`scripts/test_eclipse_natural_geneva.py` adds Warsaw's level-45 shadow Lapras
through its earned rescue, purifies it, and verifies Ice Beam. The party reaches
six and three total purifications. Five Hyper Potions and one Revive are bought
with 7,500 in earned money. The newly evolved Dark partner is initially too weak
for Veil's level-52 Gengar; 23 ordinary Vienna practice victories raise it from
level 31 to 40. The final team uses Nidoqueen for Magneton/Tyranitar/Houndoom,
Houndoom for Gengar and Lapras for Dragonite. The finalized cold-save replay
wins in seven attack selections without consuming an item. An earlier continuous
run also won in seven using two Hyper Potions. Destiny Bond in failed retries
helped identify poor replacement and recovery choices in the old runner.
`--resume` repeats the finale from the trained preparation; `--train` can resume
its training. Stage 16, six partners, the purified Lapras and modern tile/player
colors survive cold Continue. These Normal, non-Nuzlocke playtests use native
controls and earned resources, with no party, progress, inventory, experience,
damage, AI, encounter or RNG memory writes. Lisbon still passes with its two
Hyper Potions and Revive after the runner changes; Paris 1940 passes in seven
selections with one Hyper Potion and a cold sepia save. League progression,
postgame natural balancing and broad hardware/emulator checks remain outstanding.

Legendary checks use explicit stage/purification, Master Ball and disabled
incidental-encounter fixtures; these are encounter-system checks, not a natural
legendary balancing playthrough. All seven native battles have the correct
species and levels. Story gates, purification gates and declining pass. Articuno
can be retried after a native flee and fixture-assisted knockout. All seven
are caught through native Ball input; their hide flags and exact Ball consumption
survive cold Continue. Captures beyond six party slots persist in PC storage,
and revisiting every refuge shows no duplicate guardian. The challenge test
checks first-encounter allowance, the native Nuzlocke refusal/refund script on a
retry, and successful capture after disabling the rule. The final-ROM natural
Berlin regression also passes with badge, move and TM persistence.

The Scandinavian postgame hunt passes native pre-League, acceptance, decline
and ordered-investigation gates. All three commanders are battled in Easy,
Normal and Hard: real levels change by -4/0/+5 while curated moves, held items
and shadow status remain intact. Explicit HP/damage fixtures accelerate those
nine victories; this does not establish natural battle balance. Each victory
advances only the hunt, keeping the main ending complete. Defeated commanders
cannot be farmed. A full Shadow Ball stack leaves the reward pending; native
delivery succeeds after space is available, cannot be duplicated, and persists
with quest completion after cold Continue. The final-ROM natural Berlin and
legendary Nuzlocke regressions also pass. The quest uses previously unused
VAR_0x40BD and reward flag 0x8D5 without adding RAM allocations.

The Krakow restoration passes both native saved-timeline branches: garden/EEVEE
and archive/VOLTORB. Tests cover pre-League travel, declined travel/project/work,
missing historical memory, work before acceptance, exact material deductions,
repeat-work guards, missing materials and all three visible courtyard changes.
Partial work survives cold Continue. Completing the jobs brings back only the
appropriate partner, with adoption refusal, level-30 delivery and duplicate guards.
A full item pocket leaves Lucky Egg pending; delivery succeeds once space exists.
Quest, reward, partner and return travel persist after cold Continue in both branches.
Explicit progress, memory and inventory fixtures isolate these rules; they do
not assert a natural playthrough of the historical prerequisites or economy.

Additional native full-party/storage fixtures confirm adoption remains pending
when both are full. With room in the PC, the native gift goes there and survives
cold Continue, including with Nuzlocke enabled and Poland's encounter allowance
already used. Krakow uses the unused VAR_0x40BE and flags 0x8D6 through 0x8DC;
it adds no persistent RAM allocations and keeps continental country indexing
unchanged in a separate map group. The new city reuses Polish castle tiles in
an independent courtyard layout. Static checks include every event approach.
The updated scrolling shop also sells Escape Rope; its native purchase at 550,
cancellation and the existing stone/purification/evolution flow pass using earned
money. Both restoration branches have been replayed on the final built ROM.

The champion circuit passes native acceptance, decline, ordered-opponent and
pre-League gates. All thirteen new teams are checked in Easy, Normal and Hard:
levels change by -4/0/+5 while every species, held item and four-move set remains
correct. These opponents are not marked shadow. Thirteen Normal victories use
explicit HP/damage fixtures to verify real native callbacks, not natural combat
balance. Unclaimed badge TMs are delivered before the rematch prompt. Partial
progress survives cold Continue, and the main ending stays complete.

All nine starter choices produce the correct fully evolved rival ace in each
of the three difficulty modes, with its intended four moves and Lum Berry.
The World Gear UI changes difficulty during the saved circuit without changing
its card. A separate regression checks all nine original opening counter-starters:
they remain level-six unevolved partners with one basic attack.

A full Master Ball stack leaves the first circuit reward pending. Normal delivery
adds one, saves the completion flag, survives cold Continue and cannot repeat.
A free champion rematch leaves completion intact; starting another lap works,
and a completed-lap progress fixture confirms that it gives no second reward.
An explicit one-partner/low-HP/harmless-move fixture causes a real native defeat.
Blackout preserves the pending match; clinic exit, campaign re-entry and a retry
victory work through ordinary controls. Navigation tests now read each map's
actual compiled tileset attributes rather than guessing the shared clinic tileset.

The steward and archivist restore their templates in older completed saves.
Cold Continue of a pre-circuit save can reach the steward without leaving the
shelter. The archivist replays all three credits pages and returns safely to the
field; the existing all-country epilogue still gives only one Master Ball.
The circuit uses unused VAR_0x40BF and reward flag 0x8DD, adding no persistent
RAM allocations. Existing shelter approaches and native dialogue widths pass.
An original-Champion regression resets only its completed trainer flag and stage
in the test fixture, wins the native first Champion match, and verifies that it
advances the main ending, launches all three credits pages and returns to the
shelter without starting the circuit. Final-ROM checks include the full circuit,
all rival choices, loss/retry, settings, classic opening rivals, the original
Champion ending and preserved credits/network rewards.

## Reproduce

Run the build, then the Python scripts in WSL with the base mGBA test bridge:

1. `scripts/test_shadow_static.py` and `scripts/test_continent_static.py`
2. `scripts/test_country.py` (regenerates checkpoints for the current ROM)
3. `scripts/test_continent_runtime.py` (also creates continent-ready checkpoint)
4. `scripts/test_shadow_runtime.py` and `scripts/test_shadow_ui.py`
5. `scripts/test_shadow_progression.py` and `scripts/test_shadow_ending_save.py`
6. `scripts/test_eclipse_combat.py`, `scripts/test_eclipse_challenges.py`,
   and `scripts/test_eclipse_credits.py`
7. `scripts/test_eclipse_natural.py` and `scripts/test_eclipse_natural_gym.py`
8. `scripts/test_eclipse_storage.py` and `scripts/test_eclipse_natural_paris.py`
9. `scripts/test_eclipse_tm_rewards.py`, `scripts/test_eclipse_tm_teaching.py`,
   `scripts/test_eclipse_natural_brussels.py` and `scripts/test_eclipse_party_memory.py`
10. `scripts/test_eclipse_supplies.py` (requires the natural third-badge save)
11. `scripts/test_eclipse_natural_amsterdam.py` (requires the purified Raichu save;
    `--caught` resumes after the Belgian catch and `--resume` replays the gym)
12. `scripts/test_eclipse_natural_berlin.py` (requires the natural fourth-badge
    save; `--resume` replays the gym from the trained-team save)
13. `scripts/test_eclipse_legendaries.py` and
    `scripts/test_eclipse_legendary_challenge.py` (use the cold completed save)
14. `scripts/test_eclipse_nordic.py` (uses the cold completed save; victory
    and bag-capacity fixtures are explicitly documented in the script)

15. `scripts/test_eclipse_krakow.py`, then
    `scripts/test_eclipse_krakow_capacity.py` (use cold completed checkpoints;
    timeline, progress, materials and capacity fixtures are documented)

16. `scripts/test_eclipse_circuit.py` and
    `scripts/test_eclipse_circuit_rival.py` (native teams and ordered callbacks)
17. `scripts/test_eclipse_circuit_loss.py` and
    `scripts/test_eclipse_circuit_settings.py` (native blackout retry, World Gear
    and opening-rival regression; requires the circuit partial checkpoint)
18. `scripts/test_eclipse_credits.py` and `scripts/test_eclipse_first_ending.py`
    (archivist replay, original Champion ending and network reward)
19. `scripts/test_eclipse_natural_warsaw.py`,
    `scripts/test_eclipse_natural_berlin1944.py`, then
    `scripts/test_eclipse_natural_geneva.py` (earned rescues, native training,
    wartime victories, modern return and final Veil battle)

20. `scripts/test_eclipse_natural_league.py` (earned Shock Wave, held EXP. SHARE,
    native practice, four council victories, champion and cold ending save)

21. `scripts/test_eclipse_natural_legendaries.py`, then
    `scripts/test_eclipse_natural_legendary_saves.py` (earned-party catches,
    purchased Ultra Balls, PC delivery and cold persistence; `--post` for Suicune)

22. `scripts/test_eclipse_timer_rules.py` (explicit Nuzlocke allowance/Ball/escape
    fixtures; native blocked refund and unrestricted Timer throw)

Checkpoints and screenshots are under ignored `test-output`. Native save files
can cold-load between builds; emulator state files must be regenerated whenever
the ROM changes. Preview capture: `scripts/preview_eclipse.py`.

## Natural League and first ending

The earned England/Totodile campaign now reaches the champion ending in Normal
mode with Nuzlocke disabled. The first unprepared Thalia attempt lost to Dewgong
and left chapter 16 pending. Ice Beam alone was ineffective against its healing;
the level-15 Raichu had no damaging Electric move after its early evolution.
No opponent, party, progression or inventory fixtures were used in this run.

`test_eclipse_natural_league.py` teaches the truly earned Amsterdam Shock Wave
TM to Raichu through the native TM Case, replacing Growl. It gives the already
awarded EXP. SHARE through the Bag's Give menu and verifies that the item leaves
the Bag and becomes held. Thirty-seven completed Geneva first-trainer practices
in the saved progression raise Raichu to 45 and Nidoqueen to 59. Incidental
encounters remain enabled. Each practice uses original experience, HP, PP, AI
and native healing; no stat or experience writes are made. The prepared party
also contains Croconaw 23, Pidgeotto 33, purified Houndoom 40 and purified Lapras
45. This is one successful route, not a claim that every starter or similarly
leveled team has been balanced.

The runner buys ten Hyper Potions and three Revives with earned money for
16,500, heals between council chambers, and selects ordinary moves and native
matchup switches. The initial successful pass takes 10/13/8/8/18 attack selections
against Thalia, Nikos, Eleni, Leon and the rival respectively. The final cold
replay passes in 11/9/8/8/19 selections with exact party-record comparisons.
Its rival uses
Meganium as the evolved counter to Totodile. All three ending pages open after
the real champion victory; the game-clear flag is set and the player returns
to the champion shelter with chapter 21 saved. League shelters remain usable.

Every chamber is saved through the Start menu and loaded in a fresh emulator.
The final replay also compares species, held items, experience, levels, moves,
HP and purification records after cold Continue, together with the map and
player palettes. `--resume` replays the prepared League; `--train` resumes the
saved training route, and `--stage=17` through `--stage=20` resume individual
remaining chapters from the previous native victory. The native battle helper's
optional `finish=False` lets the champion test inspect the credits before
closing them. Other callers retain automatic field-dialogue completion.

Remaining natural legendary captures, postgame combat, other full starting
routes and broad hardware/emulator checks remain outstanding. Earlier postgame victory and
capacity fixtures remain explicitly separate from this natural campaign.

## Natural legendary captures

`test_eclipse_natural_legendaries.py` uses the earned prepared-League save at
chapter 16 for the three birds, and the earned champion save at chapter 21 for
`--post` (Suicune). These are separate natural branches of the same campaign;
the pre-League catches are not claimed to have been used in the League run.
Native station menus reach Iceland, Norway, Italy and Finland. Normal difficulty
and Nuzlocke OFF remain in effect. Encounter rates, catch odds, HP, PP, stats,
experience, storage and inventory are never patched.

The initial 50-Ultra-Ball Articuno pilot exhausted its supply without catching
it. The successful preparation buys 90 Ultra Balls, 15 Hyper Potions and five
Full Restores for 141,000 in earned money; the pre-League budget starts at
144,644, and the postgame budget at 172,844. All purchases verify the proper
Ball or item pocket and exact money deductions. The shared shop helper now
supports Ball purchases instead of assuming every purchase enters the item
pocket.

The native capture helper paralyzes with Thunder Wave and weakens with Quick
Attack. A Zapdos pilot suffered a critical-hit knockout before throwing a Ball;
the helper now checks a conservative critical-damage bound before attacking
again. It uses real healing and native replacements when a partner faints,
rather than extending HP or disabling attacks. The recorded successful catches
use 1/49/13 Ultra Balls for Articuno/Zapdos/Moltres; the final guarded replay
passes all three in 13/61/13 Balls, with exact boxed-record and Ball-count checks
across cold Continue. The Suicune run uses 80 Ultra
Balls, 14 heals and 13 move selections. Raichu faints in the long Suicune battle
and Nidoqueen finishes the catch. These counts describe observed runs and do
not promise that a fixed number of Balls will catch a guardian.

Each successful catch sets the native removal flag, adds exactly one guardian
to the PC with the six-member party retained, and preserves the campaign stage
after cold Continue. `test_eclipse_natural_legendary_saves.py` independently
cold-loads all four catches, verifies their exact native level via the Slow
experience curve, confirms the actor is absent, and checks that no unearned
Master Ball is present. The capture runner also compares complete decrypted
boxed records and remaining Ultra Balls across its save/load boundary.
`--resume` replays purchased preparation; `--after=articuno` or `--after=zapdos`
continues from a native caught checkpoint. Use `--post --resume` for the saved
Suicune preparation. Test saves and screenshots remain under ignored test-output.

The following guardian pass adds Lugia and Ho-Oh coverage; natural Mewtwo
capture, postgame battles, other full starting routes and hardware checks
remain outstanding. Earlier seven-legendary fixtures
are encounter-system tests and remain separate from these earned-party results.

## Recovering guardians and Timer Ball access

Natural champion-party coverage now includes Malta's level-65 Lugia and
Austria's level-65 Ho-Oh. Ho-Oh opens with the three purifications actually
earned during the campaign; no care or story gate is patched. Separate branches
start from the same earned champion/preparation save, so these captures are
not claimed as one continuously stocked six-legendary run.

The initial Lugia catch uses 51 Ultra Balls, seven heals and five move selections.
Lugia knocks out Raichu and restores its own HP with Recover; Lapras keeps the
attempt alive. A Ho-Oh pilot exhausts enemy PP and ends in a native knockout.
The uncaught flag stays clear, storage is unchanged, and the runner heals and
retries without restoring supplies or setting progress. Its retry catches Ho-Oh
with another 21 Ultra Balls. The capture helper can restore Raichu with a real
Revive and switch it back after the opponent's high-power attacks run out of PP.
An optional Shock Wave policy uses a conservative critical-hit damage bound;
it does not change damage, critical rates or enemy recovery.

These attempts exposed missing long-battle supplies. The shared League shop
now includes the existing FireRed Timer Ball for its native 1,000 price, bringing
stock to 23 items. The original Ball calculation is unchanged: Timer Balls grow
with the native battle turn counter and cap at the original multiplier. No RAM
state, new item type, encounter odds or guardian stats were added.

`--post --timer --guardian=lugia` buys 45 Ultra Balls, 45 Timer Balls, 15 Hyper
Potions and five Full Restores for 132,000 in earned money. The runner chooses
Timer Balls after ten battle turns, verifies consumption from the Ball pocket,
and compares both Ball stacks plus the full boxed record across cold Continue.
That observed Lugia run catches it with seven Ultra Balls and two Timer Balls;
Ho-Oh's run from the same saved preparation uses three Ultra and fourteen Timer
Balls with three heals. These are observed outcomes, not guaranteed counts.
Use `--post --timer --resume --guardian=ho_oh` for that preparation replay.
The cold-save checker now covers all six naturally captured guardians, verifies
their exact native level/experience, recorded Ball type, actor removal and stage.

`test_eclipse_timer_rules.py` uses explicit used-encounter, one-Timer-Ball and
escape fixtures to isolate Nuzlocke behavior. A blocked throw refunds the Timer
Ball; switching Nuzlocke OFF consumes it through the original catch handler.
This is a rule regression, separate from the natural capture balance checks.
The scrolling shop, stone prices, cancellation, shadow evolution refusal and
purified Raichu evolution checks remain in `test_eclipse_supplies.py`.

Build log: `build-eclipse-timer-balls.log`. EWRAM remains 261,084/262,144 bytes,
and IWRAM 29,824/32,768 bytes. The release alias matches the rebuilt ROM.
Natural Mewtwo capture and its six earned purifications are now verified. Postgame combat,
other full starting routes and hardware checks remain unfinished.

## Release-quality limits

The story and requested systems are implemented in a playable native campaign.
The geography uses compact districts, stylized landmarks and shared League
shelters rather than full-scale city reconstructions. Wild actors use defined
spawn points and do not roam. There are no following party sprites, dedicated gym interiors, snagging or
new Shadow-type moves. Custom villain sprites are now included.
One Normal-mode campaign has reached the ending with earned partners and
resources. Remaining earned circuit combat, other full starting routes,
and broad hardware/emulator checks remain before calling this a polished release.

Release: `Pokemon-Europe-Eclipse.gba`
SHA-256: `87854257a51e027ebf038ab97ef9f8de2b08a5a3db555d8e0a4f6cd3c33c43b0`

## Earned six-rescue Mewtwo route

`python3 scripts/test_eclipse_natural_mewtwo_unlock.py` cold-loads the earned
champion Timer Ball preparation. Native PC deposits free party slots for the
Zurich Eevee, wartime Paris Mareep and Berlin Dratini. Care raises the saved
purification count from three to six; all rescue bits and the six-member party
persist after cold Continue. No memory writes or battle fixtures are used.

`python3 scripts/test_eclipse_natural_legendaries.py --post --timer --resume --guardian=MEWTWO`
uses that checkpoint and native encounter gates, damage, PP and catch odds.
Mewtwo was caught with 39 Ultra Balls and 45 Timer Balls, 22 native healing
uses and three move selections. Raichu established paralysis; purified
Houndoom absorbed Psychic until its other attacks exhausted resources, and
Lapras finished the encounter. The exact boxed record and remaining Ball
quantities survived cold Continue. This expensive attempt warrants further
strategy/balance work; it does not establish a comfortable average catch cost.
The seven guardian saves are separate earned checkpoint branches, not one
continuous inventory route containing every legendary.

## Earned Scandinavia remnant hunt

`python3 scripts/test_eclipse_natural_nordic.py` continues the earned champion
party on Normal with Nuzlocke off. It buys 20 Hyper Potions, 10 Revives and
five Full Restores for 54,000 earned money, then follows Ada through Copenhagen,
Oslo and Stockholm. Native battles defeat Vex, Rime and Boreal without modified
levels, damage, opponent HP or victory fixtures. Each victory and the exact
healed party are cold-saved before continuing.

The successful route used 8/8/10 attack selections and 2/4/13 Hyper Potions
respectively; Boreal also required one Revive. No Full Restores were consumed.
Nidoqueen rose from level 60 to 62 and Raichu from 49 to 50. Raichu fainted
against the faster shadow Crobat; Nidoqueen handled the remainder with native
coverage and healing. Rime's Weezing is safer for Nidoqueen than the first
Lapras matchup, which failed to complete in the test harness. These results
verify one playable route, not comfortable balance for every party.

Ada's unique Shadow Ball TM, completion variable and exact inventory persist
after cold Continue, and another conversation does not duplicate the reward.
The native test helper now retries a missing party lookup on the next frame:
GetMonData can briefly leave boxed bytes decrypted at an emulator frame boundary.
The helper never changes encrypted Pokémon data.

## Earned Krakow restoration

`python3 scripts/test_eclipse_natural_krakow.py` continues the natural Nordic
completion. It purchases one Escape Rope, two Super Potions and a Water Stone
for 4,050 earned money, wins the Warsaw past operation with unmodified battles,
and chooses the garden through the native keeper dialogue. The saved timeline
choice opens Krakow restoration. Declining donations preserves materials;
accepting consumes the exact quantities and changes all three work areas.

The Lucky Egg is awarded once, and the level-30 Eevee adoption reaches native
PC storage because the party already contains six partners. Its exact boxed
record, restored garden tiles, adoption flag, reward and prior Nordic completion
survive cold Continue. The archive branch and capacity failures remain covered
by separate explicit quest fixtures, not this earned route.

## Champion training kit and earned circuit pilots

Stewart now awards HM03 Surf, TM24 Thunderbolt and TM35 Flamethrower after
circuit entry. Separate saved flags 0x8DE-0x8E0 track successful deliveries.
A held-over gift retries on another visit without repeating delivered gifts;
existing circuit saves can claim the kit. Surf already owned is recognized.
No additional runtime RAM is allocated.

`python3 scripts/test_eclipse_circuit_kit.py` uses explicit TM quantity fixtures
to verify declining entry, partial delivery, a full Thunderbolt stack, cold
pending state, successful retry and one-time rewards. Native Surf teaching
retains the HM for a second compatible partner; consumable TMs disappear.
Static campaign, geography, dialogue-width and encounter checks pass.

The earned Nordic/Krakow party lost to Ellis both before and after native kit
teaching. The upgraded attempt used one Hyper Potion and one Revive. Its
level-62 Nidoqueen, level-50 Raichu and several lower-level partners are not
yet adequate for the full level-64 opposing team; the pending circuit entry
and actual blackout were saved. These pilots do not establish a victory.

The second pilot branches from the earned six-purification Mewtwo capture.
Mareep is deposited and Mewtwo withdrawn through the native PC; no Pokémon or
supplies are transferred between saves. The route buys ten Hyper Potions and
five Revives for 19,500 earned money, then learns Surf on Lapras, Thunderbolt
on Mewtwo and Flamethrower on Houndoom through the TM Case.

Build: `build-eclipse-champion-kit.log`. EWRAM remains 261,084/262,144 bytes;
IWRAM remains 29,824/32,768 bytes. The release alias matches the rebuilt ROM.

The native Mewtwo route defeated Ellis and Marine with eight attack selections
each, using two and one Hyper Potions respectively. Both exact healed parties
and ordered victories survived cold Continue. The first Sabine pilot stalled
after prolonged sleep and Leech Seed; switching purified Houndoom into Exeggutor
won the retry in nine attack selections with one Hyper Potion and no status
items. Circuit tests use optional native status-item handling; later retries use
cheaper Full Heals for status and confusion.
The complete fixture regression still passes all 39 difficulty/team entries,
thirteen ordered wins, partial/cold saves, unique rewards and another-lap guards.

Further native circuit progression defeated Maarten (14 attack selections,
eight Hyper Potions and five Full Restores), Greta (five selections, no items)
and Irena (18 selections, four Hyper Potions). Their exact parties and circuit
cards survived cold Continue. Flavia's first attempt lost after burns and
confusion consumed 11 Hyper Potions and one Revive. The saved sixth victory
remained intact. Buying ten Full Heals for 6,000 earned money and using native
status/confusion treatment won the retry in eleven selections with four Hyper
Potions and three Full Heals. The current test policy restocks Hyper Potions
and Full Heals only when it has sufficient earned money.

Ines won in ten attack selections with four Hyper Potions and one Full Heal.
Thalia's first pilot lost after Jynx's Calm Mind and sleep. The automation now
scores visible Attack/Defense and special stat changes, burn, screens, accuracy
and evasion; it changes only its chosen native input. The retry won in twelve
selections with three Hyper Potions. Nikos won in eight selections with one
Hyper Potion, one Revive and one Full Heal. Each victory and exact party were
cold-saved. Retry counts are separate checkpoint branches and are not added
to the successful route's inventory consumption.

The earned route currently stops at Eleni with ten cold-saved circuit wins.
Her first pilot lost using ten Hyper Potions and one Revive. A retry switched
Nidoqueen into Absol, Houndoom and Umbreon, but also lost (seven Hyper Potions,
one Revive, five Full Heals). The pending match and main ending remain saved.
Further partner training is required before verifying Eleni, Leon, the rival
and the natural Master Ball reward. The fixture regression covers those rules
but does not replace earned combat. No circuit opponent stats were weakened.

## Weather and saved day/night cycle

The previous weather release added native animated rain and snow, regional weather,
48-minute days with dawn/dusk/night tint, and saved World Gear overrides.
Only outdoor European maps receive these effects. The clock reuses saved
playtime; menus/battles use their native palettes. Night tint is applied to the
hardware palette without modifying either source buffer, composing with sepia
and avoiding cumulative tint. Text BG palettes retain their contrast.
FireRed's dormant snow restart timer now advances, so snowfall continues.
RAM usage is unchanged: EWRAM 261,084 bytes; IWRAM 29,824 bytes.

On ROM `e400f0243f54a2f77e4b20c8d37fe2272199cbe2a7b391f18a54e14d608df971`:

- `scripts/test_eclipse_environment.py` passed native World Gear rain/snow/day/
  night selection, actual rain/snow sprite counts, snow callback respawning
  after 1,200 extra frames, hardware palette comparisons and stable frames.
  Native Save/cold Continue retains settings and location. Clock fixtures
  cover day/night/dawn/dusk and live time/weather boundary transitions.
  Native Norway travel verifies regional snow in both eras and historical
  tint composition; return to the champion shelter verifies indoor clear and
  untinted palettes despite forced settings. Restore Defaults resets controls.
  Only clock phases are memory fixtures; settings, travel, saving and reload
  use native inputs. The test allows the full native save prompt to finish.
- `scripts/test_eclipse_past_continue.py` passed historical map/player palette
  cold reload and modern return/cold palette restoration.
- `scripts/test_shadow_static.py` and `scripts/test_continent_static.py` passed
  campaign/map/trainer/encounter/dialogue validation.
- Rain/day, rain/night, snow/night, regional Norway snow, historical snow/night
  and indoor screenshots were inspected. Snow remains visible after repeated
  falls. Snow is visual; it does not apply hail damage in battles.

The older cosmetic suites' required European Tour checkpoint files are absent
from this clone, so those suites could not run here. Their row navigation was
updated for the expanded menu; the native environment check verifies scrolling
through both added options and the relocated Restore Defaults row. Real GBA
hardware timing and a full campaign replay remain outside this focused check.


## National roster, Dex moves and real-world local clock

The earlier 48-minute clock checks above describe the previous release. LOCAL
now reads the cartridge RTC; rain/snow regional timing still uses playtime.

Passed checks on the expanded build:
- `test_eclipse_roster_static.py`: all 1,025 species partitioned between common
  reserves, post-League guardian reserves and the seven original guardian events;
  639 imported table entries and asset sets; safe learnset and machine bounds.
- Battle asset validation: 1,278 indexed 64x64 front/back images, native colors.
- `test_eclipse_dex.py`: native SELECT tabs, LEFT/RIGHT boundaries, area/back,
  1,025-entry National list, Pecharunt entry/sprite/level moves, four-digit numbers.
  Complete seen/owned flags are explicit UI fixtures, not earned catches.
- `test_eclipse_reserve_visible.py`: naturally selected Pachirisu, its native
  icon-derived overworld sprite and matching wild battle.
- `test_eclipse_fairy.py`: native Sylveon typing and Dragon Rage immunity, with
  explicit move/encounter fixtures.
- `test_eclipse_local_time.py`: mGBA RTC fixtures converted with America/Chicago
  timezone through the actual cartridge GPIO reader: morning, previous-day night
  and dusk. The emulator bridge uses its fixed RTC source, not game-clock writes.
- `test_eclipse_environment.py`: native World Gear changes, rain/snow particles,
  stable daylight/night palettes, native cold Save/Continue, RTC phases, regional
  Norway snow, past-era composition, indoor clear and Restore Defaults.
- `test_eclipse_roster_runtime.py`: Turtwig, Scorbunny and Pecharunt native wild
  generation, capture, PC overflow and cold Continue with extended seen/caught
  flags. Explicit species and Master Ball fixtures isolate the data integration;
  the original earned six-member party remains unchanged.

This does not verify every species in battle, all modern evolution methods or
battle balance. Modern move/ability coverage is an adapted native subset, and
new species reuse an existing cry. The country reserves use shared rates and
regional levels; further habitat and individual encounter balancing remains.

Expanded roster release before custom villain artwork SHA-256: `63c7b535953831bb62b905acbf1c7567192cf524ebe4d3c594434f5c9e90ad02`.

## Custom villain uniforms and sprites — 2026-10-11

Eight original character designs now have 64x64 battle portraits and nine-frame
16x32 walking sheets: Eclipse grunt, Veil, Vex, Rime, Boreal, historical patrol,
research warden and laboratory director. All 43 affected battles have matching
map actors, including Germany's conditional laboratory encounter. Dedicated
trainer and object graphics IDs retain the original Rocket/scientist assets.
Eclipse and occupation labels replace the reused Rocket/scientist labels for
these opponents. All enemy parties, items, AI and original prize factors are
preserved. The new assets add no EWRAM or IWRAM globals.

Verified on the final ROM:

- `test_eclipse_villains_static.py`: eight transparent, palette-indexed portraits,
  72 nonempty walking frames, native 4bpp limits and every battle/map binding.
- `test_eclipse_villains.py`: actual native battle introduction for all eight
  designs; VRAM portraits and palettes match their compiled assets. Every
  compiled walking frame matches independently packed PNG pixel checksums,
  and each adjacent field actor is visible with its own correct palette.
- `test_eclipse_villains_environment.py`: Rime's field palette survives rain,
  animated night snow and a loaded visible partner. A native trainer victory
  returns to the same custom actor; normal Save and cold Continue preserve
  the actor, colors, weather settings and remnant progression.
- `test_eclipse_environment.py`: existing World Gear, RTC phase transitions,
  palette composition, weather particles, regional snow, historical tint,
  indoor clear weather and cold saved settings still pass.
- `test_shadow_static.py` and `test_continent_static.py`: campaign, map/NPC
  reachability, reward gates, dialogue widths and encounters still pass.

Rendering tests use explicit chapter/remnant/trainer-defeat fixtures and an
accelerated battle damage fixture. They verify artwork integration and native
callbacks rather than combat balance. Only test-created saves were used.
The walking-sheet build rule explicitly packs 2x4-tile frames, preventing
horizontal sheets from being treated as one row-major image.

Final agbcc build: EWRAM 261,196 / 262,144 bytes; IWRAM 29,824 / 32,768;
ROM content 17,275,272 bytes, padded to 32 MiB. Both `pokefirered.gba` and
`Pokemon-Europe-Eclipse.gba` contain the same verified release.
Previous villain-art release SHA-256: `87854257a51e027ebf038ab97ef9f8de2b08a5a3db555d8e0a4f6cd3c33c43b0`.

## Custom title and 2026 intro — October 11, 2026

`test_release_title.py` passes on the final ROM: fresh boot shows the current-year
credit canvas, then the custom skyline/rift title. Captures verify native pixels,
hovering Celebi and the blinking prompt. Start and A each enter New Game.
A separate cold boot loads the test-created Oslo checkpoint through Continue.
The original personal save files were never opened. Native title music and
shortcut handlers are retained; no additional EWRAM or save fields were added.

Final agbcc build: EWRAM 261,196 / 262,144 bytes; IWRAM 29,824 / 32,768;
ROM content 17,293,164 bytes, padded to 32 MiB. Both ROM aliases match.
Previous title release SHA-256: `c8eac326ee8b0331d80550cf23f8b309358acbb08e3eca713ad4499b48c2004b`.

## Earned final rematches and postgame journal — October 11, 2026

The existing Normal-mode, non-Nuzlocke earned party has now completed all
thirteen Champion circuit matches. The final opponents retain their original
levels, stats, held items, move PP and native AI. All preparation and combat use
native buttons: supplies are purchased with earned money, and battle experience
supplies level gains. Eleni required 31 attack selections, 12 Full Restores,
10 Full Heals and one Revive. Leon's actual midbattle emulator state was resumed
after fixing test-controller menu timing; his complete victory was cold-saved.
The rival required 17 attack selections, 13 Hyper Potions, three Full Restores,
one Full Heal and one Revive. Each final victory preserved the exact party on
cold Continue. Stewart then awarded exactly one Master Ball; repeated talk and
cold Continue preserved the reward flag, completed circuit and Ball quantity.

Test-created checkpoints: `natural-circuit-11-complete.sav`,
`natural-circuit-12-complete.sav`, `natural-circuit-13-complete.sav` and
`natural-circuit-complete.sav` in ignored `test-output/`. These are earned saves,
not forced-victory fixtures. The route includes naturally caught Mewtwo and
substantial healing supplies; it does not establish balance for every starter,
a non-legendary party, Hard mode or Nuzlocke.

The reusable earned controller now handles native Bag return timing, potion
fallback and affordable Full Restore purchases. `prepare_earned_circuit.py`
prepares the ten-match checkpoint through real shops and optional owned items.
`test_eclipse_natural_circuit.py --after=11 --full-restores` continues from the
earned Eleni checkpoint; `--after=12 --full-restores` runs the rival and reward.
Save helpers wait for native flash completion before exporting battery saves.

`test_eclipse_postgame_journal.py` passes on the final ROM: all 34 postgame
leads, thirteen match directions, care thresholds, pending rewards, active
circuit/restoration priority and all 136 native-width text lines. Every journal
view preserves the party, Bag, location, quest variables and reward flags.
These lead-selection cases explicitly fixture progress and do not claim battle
wins. Separate cold Continue of the naturally completed circuit verifies the
final ROM's compatibility with the earned Master Ball save. Campaign leads at
stages 0, 12 and 20 retain their original behavior and the seven milestone rows.
`test_release_title.py` also passes: 2026 intro, animated title, A/Start and cold
Continue. Campaign and continent static checks retain all maps, rewards,
dialogue widths and weighted encounter tables.

Final agbcc build: EWRAM 261,196 / 262,144 bytes; IWRAM 29,824 / 32,768;
ROM content 17,299,452 bytes, padded to 32 MiB. Both ROM aliases match.
Previous journal release SHA-256: `11eb4fa4b6f8df220087132422488b0aeabb5cf9a8e11f12d49054b566b535cb`.


## Friendship evolution and RTC conditions — 2026-10-11

The native Rare Candy handler verifies all nine added friendship evolutions,
Eevee's Espeon/Umbreon branches, opposite-time rejection, DAY/NIGHT overrides,
low friendship, Everstone and shadow-state prevention. Fixtures explicitly set
species, friendship, held item, cached level and one Rare Candy on an isolated
copy of the earned circuit save. These cases verify evolution mechanics, not
naturally earned friendship or captures. Every candy raises level 50 to 51.
The boundary cases cover 05:00, 06:00, 19:00 and 20:00. Evolved Silvally survives
native Save and cold Continue. Logs: test-eclipse-friendship.log and
 test-eclipse-friendship-boundaries.log. A final RTC refresh was added after
these cases; test-eclipse-friendship-final.log rechecks both overrides, shadow
prevention and deliberately stale menu-time fixtures for day Riolu/night Snom.

The parser regression rejects unsupported nested gender/item/move requirements
instead of dropping their conditions. It verifies nine friendship routes and
seven existing base-form aliases. Roster, campaign and continent static checks
pass; title boot and saved Continue pass. No RAM or saved-data fields were added.

Final ROM content: 17,299,532 bytes, padded to 32 MiB. EWRAM remains 261,196 /
262,144 bytes, IWRAM 29,824 / 32,768. Both ROM aliases match.
Previous friendship release SHA-256: `219bc65d5b509d28a81897fe2b30debd477c25de17c31f939d350be5f940c113`.


## Move-known evolution paths — 2026-10-11

`test_eclipse_move_evolution.py` passes the five new paths through native Rare
Candy use, required-move rejection, Everstone and shadow prevention. Tangela
learns Ancient Power and evolves on the same level-up at 24; Yanma does so at
33. Native Save / cold Continue retains evolved Yanmega and Ancient Power.
These are isolated species, level, moves, inventory and restriction fixtures;
they do not claim naturally raised or captured partners. The required move is
checked in the current moveset, rather than against historical learned moves.

`test-eclipse-move-fourth-slot.log` checks Clobbopus with Taunt in slot four.
`test-eclipse-move-friendship-regression.log` rechecks Riolu with deliberately
stale menu time, preserving the RTC friendship path. Parser assertions reject
unknown required moves and extra unsupported conditions. Existing evolution
projection, campaign static, boot/title and cold Continue checks pass.

The final rebuild matches the ROM used by the initial ten gameplay cases.
ROM content remains 17,299,532 bytes, padded to 32 MiB. EWRAM remains 261,196 /
262,144 bytes and IWRAM 29,824 / 32,768; no save layout changes.
Previous move-evolution release SHA-256: `71a4371084cb98045dd20e00a953f9440432b6dcf00107abda0b9c323f33d04b`.


## Gender-dependent evolution paths — 2026-10-11

`test_eclipse_gender_evolution.py` passes thirteen native Rare Candy cases:
female/male Combee at 21, female Combee below threshold, female/male Salandit
at 33, both Burmy branches at 20, Everstone and shadow prevention, both genders
of Espurr at 25 and both genders of Lechonk at 18. Personality fixtures properly
reorder and re-encrypt the mon substructures. Species, gender/personality,
level, restrictions and inventory are explicit test fixtures on an isolated
copy of the earned circuit battery; they do not claim natural captures or
training. Evolution preserves personality, while native level-up recalculates
the Pokémon's stats. Gen IX Oinkologne, its personality and extended seen/caught
flags survive native Save and cold Continue.

`test_eclipse_evolution_projection.py` also checks gender thresholds, female
base-form aliases, extra-condition rejection and contradictory duplicate gender
conditions. Fresh generation exactly matches the built evolution table: 214
supported and 139 omitted imported rules. The final ROM retains native
move-known Bonsly and stale-time RTC Riolu evolution coverage. Boot/title and
cold Continue pass. Espurr/Lechonk gender forms share the existing base-model
art/stats, and Wormadam uses its existing plant model; separate forms remain
listed in TODO-ECLIPSE.md.

ROM content remains 17,299,532 bytes, padded to 32 MiB. EWRAM remains 261,196 /
262,144 bytes and IWRAM 29,824 / 32,768; no new RAM globals or save fields.
Current release SHA-256: `6b6c8faba6238aefdd68ec0a587c0b0ef2f17d3a1cb058eb0e04a79e1123355f`.
