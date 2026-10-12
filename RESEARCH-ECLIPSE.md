# Repository research and provenance

Researched 2026-10-10 and updated 2026-10-11. Original campaign code and
writing sit on the existing FireRed decompilation. Imported Pokemon artwork
and metadata are attributed below.

- https://github.com/pret/pokefirered — same engine as this base; preserve upstream credits.
- https://github.com/Maruno17/pokemon-essentials — RPG Maker XP/Ruby engine;
  release notes confirm Shadow Pokemon support. CC BY-NC-SA 4.0 license:
  https://github.com/Maruno17/pokemon-essentials/blob/master/LICENSE .
  Reference for heart recovery and purification concepts; not drop-in GBA code.
- https://github.com/VisibleOverworldWildEncounters/Visible-Overworld-Wild-Encounters-V20
  — Essentials overworld encounter plugin; requires follower sprites. Reference
  for rate-based visible encounters; no license-cleared sprite set imported.
- https://github.com/rh-hideout/pokeemerald-expansion — Emerald GBA hack base,
  not FireRed; requires engine migration or individual verified ports. Repository
  asks for RHH attribution when reused. Used for the additional National Dex species, sprites and source learnset metadata; see the pinned import below.

Present implementation uses native overworld sprites and an original shadow
status mechanism in the existing unused ribbon nibble. It does not include Essentials code or the expansion battle engine.

The expedition keeps native weighted encounter tables, with original field
spawn code and icon-derived sprite adaptations. Native landmark art is original
and compiled into FireRed tilesets. Later-generation artwork is imported from the credited RHH source below.
Additional primary references:

- https://github.com/pret/pokefirered/blob/master/src/data/wild_encounters.json
- https://www.dhm.de/en/museum/about-us/documentation-centre-german-occupation-of-europe-in-the-second-world-war/resistance/

The DHM resistance material supports the historical framing of diverse civilian
and German resistance; the game's time anchors and shadow experiments are fiction.


## Expanded roster and local clock

The 639 species from National Dex 387 through 1025 use species metadata and
front/back/icon/footprint/palette artwork from rh-hideout/pokeemerald-expansion,
pinned at `7b4344c7ee867c98c8fb9d6026791df4f8eaecf7`. The complete upstream
artist and contributor attribution is retained in `data/RHH-ROSTER-CREDITS.md`.
`data/eclipse-roster.json` records each source asset and the move/ability
projection. `scripts/import_eclipse_roster.py` regenerates the import from its
pinned upstream source. Base species are included, rather than every alternate
form. Existing Gen III species and their moves remain unchanged.

FireRed's native move and ability engine remains in use. Unsupported modern
moves are omitted and unsupported abilities use NONE. Five supported modern
attacks and Fairy type have been added with native effects; damage still uses
Gen III's type-based physical/special rules. Later species reuse the Unown cry.
Compatible native TM/HM lists use the union of upstream SV, SwSh, BDSP and USUM
machine learnsets. Only native evolution methods and native items are imported.
These are deliberate engine adaptations, not a complete modern battle port.

The read-only cartridge RTC protocol follows pret/pokeemerald's `src/siirtc.c`:
https://github.com/pret/pokeemerald/blob/master/src/siirtc.c . The game reads the
RTC without resetting it. Compatible emulators supply their host local time;
DAY and NIGHT remain manual World Gear overrides. If an RTC is unavailable,
automatic lighting holds at daylight until the player chooses an override.

## Original villain artwork — 2026-10-11

Eight new character sheets were created with the built-in `image_gen.imagegen`
tool: Eclipse grunt, Veil, Vex, Rime, Boreal, historical patrol, research warden
and laboratory director. Their charcoal/violet/crescent identity and separate
period uniforms are original campaign designs. No other fan game's villain
art was copied. `graphics/eclipse_villains/prompts.json` retains every final
prompt; `source/` retains the generated sheets. `scripts/pack_eclipse_villains.py`
performs only deterministic cropping, nearest-neighbor scaling, palette indexing
and packing into native 64x64 battle and nine-frame 16x32 walking assets.

### Nested evolution requirements

The pinned RHH source now expresses many evolutions using EVOLUTION / CONDITIONS
rather than separate friendship method names. scripts/eclipse_evolutions.py
reads balanced braces and projects only supported condition combinations into
the native FireRed table. The nine added friendship routes use this engine's
220-point threshold. Day is 06:00–19:59 local RTC; World Gear overrides apply.
Base-form aliases remain consistent with the existing roster projection.
The generated audit records 203 supported rules and 150 omitted rules across
639 imported species. Omitted rules include unavailable items, special methods,
additional conditions and unavailable regional/form targets. This pass does
not implement those methods or replace original species' cross-generation trees.
Source: https://github.com/rh-hideout/pokeemerald-expansion/tree/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7

### Move-known evolution support

EVO_LEVEL_MOVE checks the current four moves at normal level-up. The pinned
RHH IF_KNOWS_MOVE rules now project for Bonsly/Mimic, Steenee/Stomp and
Clobbopus/Taunt. Unknown moves and additional conditions remain omitted.
The imported audit now contains 206 supported and 147 omitted rules.
Tangela/Tangrowth and Yanma/Yanmega additionally use the same Ancient Power
rule from the pinned gen_1_families.h and gen_2_families.h sources. Ancient
Power at levels 24/33 comes from the pinned Gen IX learnsets; their other
existing level-up moves remain intact. These two original-species branches
are in the original evolution table, outside the 639-row import audit.
Mime Jr.'s regional rule, Poipole/Dragon Pulse, Dipplin/Dragon Cheer and
Piloswine's reminder-dependent route remain future work.

### Gender-based evolution support

The pinned RHH IF_GENDER rules now map to native EVO_LEVEL_MALE / FEMALE
methods while retaining their level thresholds. Combee, Salandit and Burmy
use their actual gender-specific targets. Espurr and Lechonk retain both
branches using the existing base-species representation: female Meowstic and
Oinkologne targets deliberately map to the same base model as their male
counterparts. Separate form graphics, stats and abilities are not supplied
by this pass. Burmy's Wormadam target uses the existing plant-coat model.
The import audit now lists 214 supported rules and 139 omitted rules. Gender
plus unsupported extra conditions and contradictory duplicate conditions
remain omitted. Native gender reads the preserved personality and species
ratio; no saved fields or RAM globals are added.

### Campaign move-reminder access

The original FireRed ChooseMonForMoveRelearner / TeachMoveRelearnerMove menus
now have free campaign entry points at 100 maps. Their existing earlier-level
selection, deduplication, move replacement and egg checks are retained. Piloswine
receives the level-1 Ancient Power lesson and move-known Mamoswine branch from
the already pinned RHH Gen IX learnset / Gen II family source. This original
species branch is outside the 639-row imported evolution audit. No new global
RAM or save fields are introduced. Reminder lessons deliberately have no
mushroom or money charge so all country starts can recover evolution moves.

### Modern evolution stones

Four unused item slots (52–55) now hold Shiny, Dusk, Dawn and Ice Stones.
Existing item constants/IDs, pocket sizes and save fields remain fixed; the
old unused ITEM_034–037 aliases remain defined. Native evolution-item handling,
item consumption and shop purchases are used, with the shared stone effect
flag. Colored Sun/Moon/Thunder/Water Stone icons are reused respectively.
Each costs 2,100, matching the original shop stones.

The pinned RHH family data supplies four original-species Shiny/Dusk branches,
gender-conditioned Dawn Stone routes for Kirlia/Snorunt, and modern Leaf/Ice
Eevee alternatives. Six imported stone rules now project as well. The import
audit contains 220 supported and 133 omitted rules, excluding manual original
species branches. EVO_ITEM_MALE/FEMALE retain gender during party-menu checks
and actual use. EVOS_PER_MON increases from five to seven in ROM tables to
retain every existing Eevee branch while adding Leafeon and Glaceon; all native
consumers use the same constant. Aegislash retains the existing shield-form
representation; this pass does not add battle form switching or new abilities.

### Sylveon and Baby-Doll Eyes

The same pinned RHH source provides Eevee's level-15 Baby-Doll Eyes and Sylveon's
friendship plus known-Fairy-move rule. See the cached gen_9 learnset and
[gen_1 family data](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/data/pokemon/species_info/gen_1_families.h).
This game retains the classic 220 friendship threshold. Its new native method
checks all four current move slots, rejects empty/invalid move IDs, and uses the
battle move's type. Sylveon's rule is the eighth and final Eevee slot, so it
wins over its day/night friendship branches. The conservative importer accepts
this exact pair of conditions and still rejects unknown types/extra conditions.
The imported 639-row audit remains 220 supported and 133 omitted rules; Eevee
is an original-species manual branch. The generator/importer now retain eight
slots. ROM-only table growth adds no global RAM or save fields.

Baby-Doll Eyes is native move 360, with Fairy typing, 100 accuracy, 30 PP,
priority +1 and the existing one-stage Attack-down status effect. It reuses
Charm's animation, has its own description and fits the 12-character native
move label limit. Existing move IDs and animations remain fixed. Only Eevee's
learnset is expanded in this pass; other modern learnsets remain projected.

### Held-item day/night evolutions

The pinned RHH [Gen II family source](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/data/pokemon/species_info/gen_2_families.h)
requires nighttime and held Razor items for base Sneasel and Gligar. Its cached
Happiny rule requires held Oval Stone and a non-night time. This pass implements
the classic level-up paths. Hisuian Sneasel and conditional direct item-use
alternatives remain outside the current base-species projection.

Unused item slots 56–58 now hold Oval Stone, Razor Claw and Razor Fang, with old
unused-slot aliases retained. Shops charge 2,100; Bag Give uses the native held
item flow. Razor Claw reuses Scope Lens's critical effect; Razor Fang reuses
King's Rock's 10% flinch effect. Existing Moon Stone, Quick Claw and Dragon Fang
icons are reused. The new methods query Eclipse_IsNight, including World Gear
overrides and a refreshed RTC. Neither method changes held items while checking
eligibility. The normal evolution scene consumes the matching held item only
when it commits the evolved species; cancellation leaves it intact. Ordinary
level/stone/friendship evolutions retain unrelated held items.

The conservative parser accepts exactly one known held item plus one supported
day/night condition at level zero, rejecting missing items, extra conditions and
unsupported times/level requirements. Happiny adds one generated rule: 221
supported, 132 omitted across 639 imported rows. Sneasel/Gligar remain manual
original-species branches. Generated files now use UTF-8/LF consistently on
Windows. Item/species/save IDs and global RAM allocations remain fixed.

### Link Cable for solo trade paths

Link Cable is a deliberate single-player adaptation, using unused item ID 59
and the native evolution-item effect/party flow. It costs 2,100 and reuses the
Up-Grade icon. Existing item/save IDs remain fixed and ITEM_03B stays an alias.
The eligibility query reuses existing EVO_TRADE/EVO_TRADE_ITEM table entries;
it accepts a held-item path only when the current held item matches. It never
mutates the held item during preview. The successful normal evolution commit
consumes matching trade items; plain trade evolutions preserve unrelated items.
The native item flow consumes one cable and uses the same National Dex,
Everstone and shadow restrictions. Existing link-trade handling is unchanged.

Eight plain paths (four original, four imported) and eight original held-item
paths are supported. King's Rock, Metal Coat, Dragon Scale, Up-Grade, Deep Sea
Tooth and Deep Sea Scale are now sold at their existing native prices. Additional
modern trade items, paired Karrablast/Shelmet conditions, forms and newer special
rules remain outside this pass. The 639-row imported evolution audit is still
221 supported/132 omitted because no new table rules are projected here.

### Seven modern held trade items

The pinned RHH gen_1/gen_3 family sources provide Rhydon, Electabuzz, Magmar,
Porygon2 and Dusclops's held-item trade conditions. Cached imported Spritzee and
Swirlix bodies provide Sachet/Whipped Dream conditions. This pass implements
those classic trade conditions consistently with Link Cable, not the source's
optional direct-use item alternatives. The parser projects only exactly one
known IF_HOLD_ITEM condition at EVO_TRADE level zero into EVO_TRADE_ITEM; it
rejects unavailable items, paired-trade rules, extra conditions and nonzero
parameters. Direct use for these seven held-only items stays explicitly omitted.

Unused item slots 60, 61, 62, 72, 82, 87 and 88 now hold Electirizer, Magmarizer,
Protector, Dubious Disc, Reaper Cloth, Sachet and Whipped Dream. Existing IDs,
old unused-slot aliases, save fields and global RAM stay fixed. All seven items
are held-only with no added battle effect and cost 2,100. Icons reuse native
Magnet, Charcoal, Metal Coat, Up-Grade, Cleanse Tag and Leftovers art.

Five original-species rows are manual; Spritzee/Swirlix add two generated
trade rules. The 639-row audit now has 223 supported and 130 omitted rules.
Link Cable supports twenty-three paths. Native link-trade checks see the same
new table rows, although hardware link trading remains untested in this pass.

### Thunder Stone and required-move cross-generation paths

The pinned RHH family data supplies Thunder Stone alternatives for Magneton
and Nosepass, alongside magnetic-field rules. This pass uses the stone paths;
Charjabug's already projected Thunder Stone path remains unchanged. Five manual
original-species rows add Magnezone, Probopass, Lickilicky, Ambipom and Farigiraf.
Lickitung's source condition is known Rollout; Aipom's is known Double Hit;
Girafarig's is known Twin Beam. No new evolution method is needed.

The cached Gen IX level-up source provides Rollout at Lickitung level 6,
Double Hit at Aipom 32 and Girafarig 28, and Twin Beam at Girafarig 32. Those
lessons are inserted in order while preserving the original classic moves.
Native free reminders and Pokédex level-up lists use the resulting learnsets.
Imported evolved-species learnsets are not regenerated in this pass; evolved
partners retain newly learned moves, while broader learnset coverage is pending.
The imported audit remains 223 supported/130 omitted rules.

Moves 361/362 implement Double Hit/Twin Beam using EFFECT_DOUBLE_HIT: exactly
two strikes with one PP deduction. Double Hit is Normal, power 35 per strike,
accuracy 85, PP 10 and contact; Twin Beam is Psychic, power 40 per strike,
accuracy 100, PP 10 and non-contact. Both retain native Protect/Mirror Move and
eligible King's Rock flags. Animations reuse Double Slap and Psybeam respectively;
names/descriptions are native and original move IDs/animation positions stay
fixed. Gen III's Normal physical/Psychic special categories fit these moves.
No new global RAM, save fields, item IDs or graphics assets are introduced.

### Evolution apples, Dragon Pulse and imported lesson refresh

The pinned cached Gen VIII/IX species data supplies Applin's Tart/Sweet/Syrupy
Apple branches and Poipole's known-Dragon-Pulse requirement. Items 89–91 reuse
unused slots and retain their old aliases. Native item evolution handling,
shop purchases and consumption are used; each apple costs 2,100. Icons reuse
Aspear, Cheri and Sitrus Berry art respectively. Existing item/save IDs remain
fixed. Dragon Pulse is move 363: 85 power, Dragon type, 100 accuracy, 10 PP,
native single-hit effect and a reused Dragon Breath animation without paralysis.
Gen III's Dragon special category fits this move.

`scripts/refresh_eclipse_learnsets.py` reads the pinned cached Gen IX learnsets
and current supported move constants. It adds missing supported lessons while
retaining all prior projected lessons and their order at equal levels. It
normalizes evolution level zero to one, as the original importer does, and
rejects lists beyond the native reminder's 24-move capacity before writing.
Only learnsets/metadata are refreshed; stats, assets and machine compatibility
are unchanged. This adds 88 lessons across 80 imported species, including
Poipole's level-1 Dragon Pulse and Dipplin's level-32 Dragon Pulse. The maximum
learnset remains 22 moves. Running the refresh again adds zero lessons.

All three Applin item rules and Poipole's move-known rule now project, raising
the audit to 227 supported and 126 omitted imported evolution rules. Dipplin's
Dragon Cheer rule stays omitted: a faithful ally-targeted critical-stage
support effect and an obtainable lesson are still required. No new global RAM
or save fields are introduced.

### Dragon Cheer and native doubles training

The pinned RHH [battle command implementation](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/battle_script_commands.c)
checks for a live ally in doubles, rejects existing Cheer/Focus Energy, and
uses a one-stage Cheer volatile for non-Dragon allies or two-stage Focus
Energy for Dragon allies. Its pinned move metadata specifies 15 PP, Dragon
status, ally target, priority zero and substitute bypass. This implements the
Gen IX behavior; the newer Champions sound-move flag is outside this pass.

Move 364/effect 214 use an ally-selecting native script command, Helping Hand
animation and an ally-name message. STATUS3 bit 21 stores the one-stage boost;
existing Focus Energy stores two stages. Critical calculation adds one for the
new bit, retaining the Gen III rate table and other item/move modifiers.
Focus Energy, Dire Hit and the Focus Energy berry cannot stack over Cheer.
Normal switching clears the new volatile, and Baton Pass preserves it alongside
existing transferable statuses. No new global RAM is allocated.

The pinned Dipplin evolution requires known Dragon Cheer. Its upstream lesson
is TM-based, so this campaign deliberately adds a level-40 lesson to Dipplin
and Hydrapple. `scripts/eclipse_lessons.py` supplies the override to both the
full importer and cached refresh, so regeneration cannot remove it. One new
evolution rule brings the imported audit to 228 supported and 125 omitted.

A new optional modern-London NPC uses native doubles trainer 759, Lyra & Finn,
with level-40 Dragonair/Raichu and custom moves. It requires two fit partners
and clears only its own trainer flag for repeat matches. Existing NPC IDs are
preserved by appending the object. NUM_TRAINERS becomes 760; the existing
768-trainer flag capacity and save layout remain unchanged. Other countries,
wartime maps and main story gates are unchanged.

### Current-party partners and level/time requirements

Pinned source conditions require Remoraid in Mantyke's party and a Dark type
in Pancham's party at level 32. The upstream pokemon.c scans species without
an egg filter. This port deliberately requires hatched current-party partners;
fainted partners qualify, eggs/boxed partners do not. Both base type fields
are checked, with bounded species/party indexing and no battle-type changes.
The type method stores minimum level in the parameter's high byte and type in
the low byte; the species method supports the exact level-zero source rule.
Only the known Dark condition is currently projected; unknown types, extra
conditions and unsupported levels stay audited.

Two minimum-level/time methods use Eclipse_IsNight and its RTC refresh/World
Gear overrides. Exact single day/non-night or night conditions now project
Tyrunt, Amaura, Yungoos, Rockruff Midday, Fomantis, Greavard and both Cosmoem
branches. Levels are validated within 1–100. Conditional/alternate form rules
remain omitted. This adds ten rules across nine imported species: 238 supported,
115 omitted across 639 rows. No move/item IDs, save fields or global RAM change.

An optional modern-London researcher explains party/time requirements. Its
object is appended without changing existing local IDs; the map has thirteen
NPCs within the native sixteen-object limit. Dialogue is read-only and optional.
The rest of the campaign and chronology remains unchanged.
