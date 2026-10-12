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


### Species-specific Gen IV–IX cries

Audio comes from the same credited [RHH Pokémon Emerald expansion](https://github.com/rh-hideout/pokeemerald-expansion/tree/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/sound/direct_sound_samples/cries)
commit `7b4344c7ee867c98c8fb9d6026791df4f8eaecf7` as the imported roster.
`import_eclipse_cries.py` resolves each species' source cryId to its actual
sample label, including base-form and multiword aliases; it does not guess
filenames from display names. `data/eclipse-cries.json` records all 639 IDs,
source paths, SHA-256 hashes, sample rates and PCM frame counts. Samples retain
source WAV bytes and are converted by the existing native wav2agb DPCM rules.
Finizen and Palafin retain their shared source cry (638 unique WAV paths).
Credit and original Pokémon sound ownership remain with their source holders.

Separate normal/reverse tone tables dispatch bounded modern IDs in
PlayCryInternal, before the original SpeciesToCryId mapping. Both directions
share one ROM sample. The new allocated read-only `eclipse_cry_data` section
follows fixed graphics in both linker layouts, avoiding a .rodata overlap and
adding no global RAM or save fields. Long normal cries derive a minimum length
from their sample frame count/rate; shortened/reversed animation modes retain
the native settings. Original cry tables and samples retain their mapping.


### Overworld-weather evolution

The pinned Sliggoo source has two level-50 Goodra conditions: WEATHER_RAIN and
WEATHER_FOG. Conservative projection accepts only these known, single weather
conditions with levels 1–100; extra conditions and unsupported weather remain
omitted. Native methods EVO_LEVEL_RAIN/EVO_LEVEL_FOG read GetSav1Weather, the map weather
already selected by World Gear or the regional environment. Rain, thunderstorm
and downpour count as rain; horizontal/diagonal fog count as fog. Battle-weather
flags are excluded, and existing Everstone/shadow handling applies before the
new checks. World Gear rain makes the route obtainable without an added item;
no fog override or new fog map is introduced in this milestone.

The generated audit now has 240 supported and 113 omitted rules. Species,
items, move IDs, save offsets and global RAM are unchanged. London researcher
text covers the new route within native dialogue width limits.


### Modern armor, alloy and tea evolution items

Five existing unconditional item rules from the pinned roster source now
project: both Charcadet armor branches, Duraludon/Metal Alloy, Sinistea/Cracked
Pot and Poltchageist/Unremarkable Teacup. Existing base-form aliases resolve
Polteageist Phony and Sinistcha Unremarkable. Authenticity variants remain
outside the current base-species model. The audit is 245 supported and 108
omitted rules; no nested conditions are removed to unlock these routes.

Unused item slots 92 and 99–102 gain native party-menu evolution items, prices
of 2,100, descriptions and stable aliases. Short bag names AUSPIC.ARMOR,
MALIC.ARMOR and PLAIN TEACUP fit the native name limit. Shared native evolution
item handling consumes one only on success, honors Everstone/shadow guards and
preserves held items. Shops append the items without changing earlier stock.
Icons reuse Metal Coat, Fire Stone, Moon Stone, Berry Juice and Moomoo Milk
artwork; custom modern item artwork remains future visual work. No species,
move, save offsets or global RAM are added. Optional researcher dialogue now
explains the routes.


### Explicit Europe region adaptations

The pinned source gates standard Dewott, Dartrix, Goomy, Bergmite and Rufflet
level routes, plus Petilil's Sun Stone, with IF_NOT_REGION/REGION_HISUI.
Mime Jr.'s standard Mr. Mime route requires both Mimic and not REGION_GALAR.
This campaign deliberately treats Europe as outside those fictional source
regions. `project(..., campaign_region='EUROPE')` accepts only those exact known
negative-region patterns, keeping minimum levels, Sun Stone and Mimic intact.
Default callers still reject these conditions. Unknown regions, positive-region
requirements, additional conditions and invalid levels remain omitted. The
Hisuian/Galarian variants are neither redirected nor silently merged.

Both the full roster importer and standalone evolution generator pass the
explicit campaign context, so regeneration retains these seven routes. The
audit now has 252 supported and 101 omitted rules. Existing native level,
item and move-known methods handle them; there are no new engine methods,
species/move/item IDs, save offsets or global RAM changes. Optional researcher
tips provide all levels and requirements.


### Paired-trade evolution and solo adaptation

Pinned species rules require Karrablast traded for Shelmet and vice versa.
The [pinned native source's IF_TRADE_PARTNER_SPECIES check](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/pokemon.c)
also checks that the counterpart's held effect does not prevent evolution.
The projection accepts only a known single counterpart condition on level-zero
trade rules; extra/unavailable conditions stay audited. The new EVO_TRADE_PARTNER
parameter holds the counterpart species. The audit is 254 supported, 99 omitted.

For actual trades, all three FireRed trade-scene evolution callers pass the
sent Pokémon's species after TradeMons swaps it into the enemy party. Sending
an Egg or Everstone cannot satisfy the paired requirement; the received
Pokémon's existing Everstone/shadow guard also applies. Other trade methods
ignore this mode-specific argument and retain their original behavior.

Link Cable deliberately adapts the rule to a current-party hatched counterpart,
excluding Eggs, PC-only partners and Everstone holders. Fainted counterparts
count. Only the selected Pokémon evolves; the buddy is unchanged. Native
successful item-use consumes one cable, preserving unrelated held items.

Two appended native NPC trade profiles share Evelyn's London actor (fourteen
objects, within sixteen). They use level-matched partners, neutral IVs, no
held reward and repeatable optional offers. The script uses native party
selection, requested-species/Egg rejection and trade scenes. Existing trade
indices, sprite/local IDs, save fields and global RAM remain unchanged.
Actual emulator-to-emulator or hardware link sessions remain unverified.


### Four additional modern special attacks

Metadata comes from the [pinned RHH move definitions](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/data/moves_info.h):
Dazzling Gleam 80 power/10 PP/both foes; Energy Ball 90/10 with a 10% Special
Defense drop; Dark Pulse 80/15 with 20% flinch; Draining Kiss 50/10/contact and
75% absorption. All have 100 accuracy and ordinary priority. They occupy move
IDs 365–368; MOVES_COUNT is 369, below the packed learnset's 9-bit move limit.
Fairy, Grass and Dark use native special damage, matching these four attacks.
Dazzling Gleam retains native Gen III spread-damage scaling rather than adding
a new damage-system migration. Later-generation ability/flag interactions
outside the current engine remain unimplemented.

Dazzling Gleam uses native both-target hit handling; Energy Ball and Dark Pulse
reuse native stat-drop/flinch effects. Draining Kiss uses the native absorption
script with a move-specific 3/4 calculation from actual HP dealt. Legacy drain
moves keep 1/2. Minimum-one healing, HP caps, overkill and Liquid Ooze continue
through the native script. Swift, Magical Leaf, Shadow Ball and Sweet Kiss
animations provide compatible native visual assets. Names/descriptions and
animation table/sentinel indices are extended without shifting earlier moves.

Refreshing cached Gen IX learnsets adds 73 lessons across 66 imported species,
without removing earlier lessons. All 639 compiled lists match metadata; the
largest is 23 moves, within the free reminder's 24-move limit. The full roster
importer already projects supported move constants, keeping regeneration stable.
No new save fields, items/species IDs or global RAM are required.


### Technician and regular ability restoration

The [pinned RHH damage source](https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/battle_util.c)
uses the effective-power threshold 60 and a 1.5 modifier for Technician.
This native port adds ability ID 78 (ABILITIES_COUNT 79), name and a single-line
skills-page description. CalculateBaseDamage applies integer 3/2 power scaling
for positive effective power up to 60, before native field reductions. Dynamic
callers supply their power override, so Low Kick uses calculated weight power.
Each hit recalculates from the original power, preventing cumulative multi-hit
boosts. Physical and special paths both share this code. Same-battler
confusion/disobedience self-damage is excluded from the move-only boost.

The existing source-ability metadata restores Ambipom, Minccino, Cinccino and
Marshadow. Six classic regular second slots are restored from pinned Gen I/II
family files: Meowth, Persian, Scyther, Scizor, Smeargle and Hitmontop. The
refresh script resolves Meowth's macro and the source's modern ability branches,
fetches missing pinned family cache files, validates both regular slots and
preserves all other species fields. The full importer already projects supported
ability constants for modern species; it leaves the classic table intact.
Hidden-only Technician and a general hidden-ability system remain omitted.

No stored ability flag, save layout, species/move/item IDs or global RAM change.
Old ability IDs remain stable. Existing saved slot flags continue selecting their
regular position; restored slots now provide the intended ability. Newly generated
partners use the native regular-slot selection and battle loading.

### Skill Link regular ability restoration

The pinned RHH family data supplies Shellder/Cloyster's modern second slot:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/data/pokemon/species_info/gen_1_families.h
The previously imported Gen VII metadata supplies the Pikipek family slots.
Behavior reference: https://bulbapedia.bulbagarden.net/wiki/Skill_Link
Native FireRed's random-hit counter now selects five for Skill Link. Fixed
counters are unchanged; Triple Kick bypasses later accuracy rolls after its
first successful strike. This is a small native implementation, not an import
of the expansion battle engine. No hidden abilities or new RAM are introduced.

### Feebas and Prism Scale

Pinned upstream Gen III family data includes Beauty 170 and trade while holding
Prism Scale, plus a direct-use convenience rule:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/data/pokemon/species_info/gen_3_families.h
The native classic evolution table preserves Beauty and adds the held trade
rule. The existing solo Link Cable adaptation makes that route available without
a second console. The projection parser treats Prism Scale as a held trade item
and rejects the direct-use shortcut. Item 105 was unused; no save structure or
existing item IDs move. Dragon Scale supplies an existing native icon.
Held-item consumption now distinguishes item-triggered evolution from level-up
evolution, so reaching Beauty 170 while holding Prism Scale does not lose it.
Hardware link trading remains unverified.

### Iron Fist and Drain Punch

Pinned RHH `src/battle_util.c` applies a 1.2 modifier to punching moves for
Iron Fist. `src/data/moves_info.h` supplies the punching classification:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/data/moves_info.h
The native implementation marks the twelve already supported punching moves
and Drain Punch using unused move flag bit 6, then modifies effective base
power before field/type reductions. No RAM or move struct size changes.
Ability slots use the pinned family data and cached imported metadata.

Drain Punch reuses native ABSORB with its normal half-drain, leaving the
Draining Kiss three-quarter exception intact. Five imported level lessons
come from the cached Gen IX learnsets. Hitmonchan's upstream evolution lesson
at level 0 is mapped to level 1 for native free recall, preserving its other
classic lessons. Native Mega Punch animation supplies the battle visual.

### Adaptability regular abilities

Pinned RHH battle damage calculation uses 2.0 rather than 1.5 for a matching
type when Adaptability is active:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/battle_util.c
The cached Gen I family source supplies Eevee's Run Away/Adaptability slots;
existing imported metadata supplies Porygon-Z, Basculin and Basculegion.
This native implementation shares the same-type modifier between Cmd_typecalc
and TypeCalc. Struggle returns before that modifier; native fixed-damage
scripts preserve their own damage assignment. No new RAM or save fields.
Hidden-only slots and the upstream Terastallization system are not imported.

### Reckless and Head Charge

Pinned RHH battle calculation applies a 1.2 modifier to recoil/crash attacks:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/battle_util.c
Native FireRed has a separate EFFECT_DOUBLE_EDGE, included explicitly. Its
Struggle shares EFFECT_RECOIL, so Struggle is excluded explicitly. Existing
Gen III recoil and missed-kick crash scripts remain intact.
Pinned moves_info.h supplies Head Charge power 120, Normal type, accuracy 100,
15 PP, contact and 25-percent recoil. Cached Gen IX lessons supply Bouffalant
level 40. The native recoil effect and Take Down animation implement it.
Regular slots come from cached family/metadata sources. No hidden abilities,
new RAM or save fields are introduced.

### Super Luck regular slots

Pinned RHH battle calculation adds one critical stage for Super Luck:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/battle_util.c
Cached Gen II/III family data supply Murkrow/Absol's regular slots; existing
imported metadata supply Honchkrow and the Pidove family. Ability refresh now
reads pinned Gen I–III families and remains reproducible on a fresh checkout.
Native critcalc adds the ability stage before the existing cap and armor guards.
The legacy odds table and critical damage multiplier stay intact; this does
not introduce the modern guaranteed-critical stage or hidden abilities.
No new RAM or save fields are needed.

### Tinted Lens regular slots

Pinned RHH damage calculation applies a 2.0 modifier for resisted attacks:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/battle_util.c
Cached Gen I/III families supply Venonat, Venomoth and Illumise's second regular
slots; imported metadata supply Yanmega. The native shared helper runs after
both defending types and Wonder Guard in Cmd_typecalc and TypeCalc. It preserves
effectiveness labels and rejects no-effect, neutral and fixed-damage cases.
Native battler damage estimates use the same helper; broader AI switching
heuristics are not rewritten. No new RAM/save fields or hidden abilities.

### Solid Rock and Filter

Pinned RHH damage calculation reduces super-effective hits with these abilities:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/battle_util.c
Cached Gen I/III families supply Mr. Mime/Camerupt's second regular slots;
imported metadata supply Mime Jr., Rhyperior, Tirtouga and Carracosta.
The native helper applies 3/4 damage after combined typing in Cmd_typecalc,
TypeCalc and AI_TypeCalc, preserves effectiveness flags, and excludes zero/
negative damage, Struggle, fixed power-zero moves and no-effect cases.
No new RAM/save fields or hidden abilities. Mold Breaker-style bypass and
alternate-form abilities remain outside the current engine support.

### Sniper critical damage

Pinned RHH battle calculation applies a 1.5 modifier when Sniper scores a crit:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/battle_util.c
Cached Gen I/II family data supply the Horsea and Remoraid families' regular
slots; imported metadata supply Skorupi/Drapion and Binacle/Barbaracle.
A shared native helper applies the existing critical multiplier and then the
Sniper modifier in Cmd_damagecalc and AI_CalcDmg. Keeping gCritMultiplier at
its native value preserves stat-stage bypass and critical message behavior.
Native critical odds/damage rules otherwise stay intact. No new RAM/save
fields, hidden abilities or alternate-form data.

### Big Pecks stat protection

Imported regular slots come from the pinned RHH species family data:
https://github.com/rh-hideout/pokeemerald-expansion/tree/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/data/pokemon/species_info
Nine regular slots become supported with ability ID 88. Native ChangeStatBuffs
uses the existing specific-stat protection script and records the ability;
the stat-animation eligibility check also excludes protected Defense drops.
Both checks allow self-inflicted changes, and certain native stat costs bypass
protection. No extra RAM, save fields, hidden slots or modern Crunch conversion.

### Snow Cloak battle weather

Pinned RHH accuracy calculation applies an 80% modifier in icy weather:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/battle_util.c
The native engine supports Hail, so Snow Cloak uses its weather flag and existing
WEATHER_HAS_EFFECT guard alongside Sand Veil. Cmd_weatherdamage skips hail
residual damage for Snow Cloak regardless of typing. Gen II pinned family data
restore Swinub/Piloswine's second slots; imported metadata restore eight modern
species (nine regular slots because Glaceon has two). No added RAM/save fields,
hidden abilities, alternate forms, or conversion of visual snowfall to Hail.

### Ice Body hail recovery

Pinned RHH end-turn logic supplies Ice Body's hail healing and submerged guards:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/battle_util.c
Five Gen III family regular slots and six imported slots become supported.
The native ability handler shares Rain Dish's generic ability-name recovery
script and 1/16 healing calculation, keeping the active ability ID for text
and recording. Its hail branch excludes underground/underwater battlers.
Cmd_weatherdamage excludes Ice Body from hail damage regardless of typing.
Native Rain Dish retains its original submerged behavior. No additional RAM,
save fields, hidden abilities, modern snow rules or Heal Block support.

### Slush Rush turn order

Regular slots are projected from pinned RHH Gen V and IX family data:
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/data/pokemon/species_info/gen_5_families.h
https://github.com/rh-hideout/pokeemerald-expansion/blob/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/data/pokemon/species_info/gen_9_families.h
The native GetWhoStrikesFirst weather multiplier now includes Slush Rush for
both battler arguments, using the existing active-weather suppression guard.
It preserves subsequent native Speed-stage, item, badge, paralysis and move
priority calculations. No additional RAM, save fields, hidden slots, alternate
forms or modern snow conversion. Alolan Sandshrew/Sandslash are not projected
onto the existing base forms; hidden-only users remain unsupported.

### Sand Rush turn order and residual protection

The six supported regular users are projected from pinned RHH family data:
https://github.com/rh-hideout/pokeemerald-expansion/tree/7b4344c7ee867c98c8fb9d6026791df4f8eaecf7/src/data/pokemon/species_info
The native GetWhoStrikesFirst weather multiplier includes Sand Rush for both
battler arguments and retains its existing active-weather suppression guard
and subsequent native Speed-stage, item, badge, paralysis and priority rules.
Cmd_weatherdamage excludes Sand Rush from sandstorm damage, independent of
typing. Permanent and temporary sandstorm flags both activate the speed bonus.
Hidden-only Sandshrew/Sandslash slots and alternate Lycanroc forms remain
outside this projection. No extra RAM/save fields or new weather flags.
