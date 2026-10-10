# Next London architecture pass: western neighborhood home

The next visual improvement targets the fictional western home in the modern
London residential lane. Its existing red roof and plain native wall can gain
a more distinct residential facade while the eastern reading room keeps its
slate-blue roof. This is supporting neighborhood scenery, not a replica of a
named London building. Existing landmark art and historical London are separate.

## Exact scope

- Western home footprint: x44–48, y28–32 on the 64×44 London walking map.
- Keep its roof silhouette and the entrance at (45,32), approached from (45,33).
- First change only wall artwork at y31–32; retain the native doorway artwork.
- Preserve the front lane at y33–34, the south circuit at y40–41, all plants,
  signs, objects, scripts, events, warps, map IDs and layout dimensions.
- Keep the eastern reading room at x54–58 unchanged, including its roof palette.

The asset should distinguish the home through wall materials, window surrounds
and a restrained entrance detail. Avoid decorative objects on public paving.
Use the established GBA 16×16 metatile format and existing palette capacity.
Append tiles/metatiles instead of changing shared native entries or palettes.

## Source and generator requirements

The current London generator starts with immutable v0.50 hub terrain, adds the
landmark district and neighborhood, then applies the eastern roof mapping.
Extend that pipeline with a separately named western-wall mapping after the
roof pass. Retain every prior mapping and tile ID. Record the previous asset
files, block mappings, complete outdoor grid and map events before generating.

Inspect the final 1:1 in-game facade before packaging. Verify that windows,
wall edges and the doorway read together with the red roof and neighboring
slate-blue roof. The first pass should not enlarge either building.

## Acceptance checks

1. Outside the named wall cells, the complete London grid is byte-identical.
2. Changed cells retain collision/elevation bits and metatile attributes.
3. All earlier tile/metatile entries, palettes, map events and IDs remain exact.
4. Regeneration is deterministic and stays within secondary tileset capacity.
5. A genuine earlier outdoor battery loads at the same position and can reach
   the invitation, front lane and southern circuit through ordinary controls.
6. No/B invitation cancellation, indoor readings, both exit tiles, re-entry and
   native save/cold Continue preserve party, money, inventory and all progress.
7. Existing Westminster case, bridges, Eye gallery and historical London remain
   usable; old capital map caches refresh through the existing Continue path.
8. Preserve all four original player saves and archive the previous release.

Implemented in v1.72: nine western wall cells now use warm terracotta native
artwork variants with blue windows. The red roof and doorway are retained.
Fifteen focused checks and a separate player-save validation are archived.
