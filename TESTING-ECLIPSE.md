# Eclipse verification â€” 2026-10-11

Separate clone: `S:/pokemon-europe-shadow`, branch `codex/europe-eclipse`.
The original project's tracked source and player saves were preserved.

## Delivered systems

- 21 chapters, eight badge battles, recurring counter-starter rival, Team
  Eclipse, WWII resistance missions, League council and champion ending.
- 42 campaign shelter/route maps plus 78 country era maps: 39 independently
  authored compact districts, landmarks, a country passport and station menu.
- 276 new trainer teams, repeatable practice, six shadow rescues, saved care,
  purification, evolution lock, damage modifiers and purple battle palettes.
- Bidirectional era travel, sepia historical colors, 39 saved local decisions,
  two present-day outcomes, an all-country epilogue and one-time reward.
- World Gear: Normal/Easy/Hard, independent optional Nuzlocke, and optional
  rate-based visible encounters covering all 62 encounter-table species.
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
SHA-256: `4853bd659ad9e30ac601fb174394f8f9448bca6630d91f4787bc292a514b8158`
