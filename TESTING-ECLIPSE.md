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
  rate-based visible encounters covering all 62 encounter-table species.
- Seven stationary legendary guardians: three before the League and four
  after the ending, native sprites/battles, story/care gates and saved catches.
- Native credits and ordinary Start-menu saving.

## Native checks

Static checks verify trainer IDs, all scripted references, dialogue widths,
map connectivity and every NPC/landmark approach. The final agbcc build links
successfully: 261,084 bytes EWRAM, 29,824 bytes IWRAM, about 15,091 KiB linked ROM,
padded to 16 MiB. RAM headroom is limited and must be checked on future additions.

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
These checks extend natural campaign coverage through the sixth badge;
Zurich onward and the postgame still need natural-level balancing coverage.

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

Checkpoints and screenshots are under ignored `test-output`. Native save files
can cold-load between builds; emulator state files must be regenerated whenever
the ROM changes. Preview capture: `scripts/preview_eclipse.py`.

## Release-quality limits

The story and requested systems are implemented in a playable native campaign.
The geography uses compact districts, stylized landmarks and shared League
shelters rather than full-scale city reconstructions. Wild actors use defined
spawn points and do not roam. There are no following party sprites, new villain
sprite sheets, dedicated gym interiors, snagging or new Shadow-type moves.
A full natural-level balancing playthrough and broad hardware/emulator testing
remain outstanding before calling this a polished final release.

Release: `Pokemon-Europe-Eclipse.gba`
SHA-256: `b763ab7e52a7e3bc775c812349de82089799b7f31f718e20383bc31a71a9ec82`
