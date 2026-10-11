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
