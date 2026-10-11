# Repository research and provenance

Researched 2026-10-10. No outside code or artwork was copied in this campaign.
Original campaign code and writing sit on the existing FireRed decompilation.

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
  asks for RHH attribution when reused. Reviewed as a future mechanics source.

Present implementation uses native overworld sprites and an original shadow
status mechanism in the existing unused ribbon nibble. It does not include
Essentials code, the expansion engine, or downloaded fan-game sprite packs.

The expedition keeps native weighted encounter tables, with original field
spawn code and icon-derived sprite adaptations. Native landmark art is original
and compiled into FireRed tilesets. No external fan-game sprite pack was imported.
Additional primary references:

- https://github.com/pret/pokefirered/blob/master/src/data/wild_encounters.json
- https://www.dhm.de/en/museum/about-us/documentation-centre-german-occupation-of-europe-in-the-second-world-war/resistance/

The DHM resistance material supports the historical framing of diverse civilian
and German resistance; the game's time anchors and shadow experiments are fiction.
