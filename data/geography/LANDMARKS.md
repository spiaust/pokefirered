# Landmark districts (v0.51)

This release adds explorable landmark districts to the three starting cities.
Walk south from the original central square; London's original bridge now
continues into Westminster. The clinic, station, quest characters, map boards,
rail order and old arrival coordinates remain in place.

| City | New scenery and layout |
| --- | --- |
| London | Palace of Westminster with clock tower, London Eye across the Thames, Whitehall approach, Parliament Square, Westminster Bridge, South Bank paths and Jubilee Gardens |
| Paris | Eiffel Tower on the left bank, Champ de Mars paths, Seine quays and crossings, Notre-Dame on an island representing Ile de la Cite |
| Berlin | Reichstag north of Brandenburg Gate, Spree crossings, an open central gate passage, Tiergarten paths to the west and Unter den Linden approach to the east |

These are compressed landmark districts that retain the prototype service
hubs. Additional neighborhood buildings, more natural river bends, bridge
art, street furniture and architectural variety remain future refinements.
Oxford, Chantilly and Oranienburg received their first pass in
[v0.52](REGIONAL-LANDMARKS.md). Ports received their first pass in [v0.53](COASTAL-LANDMARKS.md).
Historical London now has a separate [v0.59 Westminster district](HISTORICAL-LONDON.md). Chantilly has a separate
[v0.54 historical estate](HISTORICAL-CHANTILLY.md) using period-appropriate exteriors.

The new landmarks are always visible. WORLD OPTIONS still controls the
regional-map shading/colors and avatar presets; it does not yet toggle
walking-map decoration.

## References

- Westminster/clock tower: https://www.parliament.uk/about/living-heritage/building/palace/architecture/palacestructure/towers-of-parliament/
- London Eye and opposite bank: https://www.londoneye.com/plan-your-visit/before-you-visit/directions/
- London districts: https://www.visitlondon.com/things-to-do/london-areas/westminster
- Eiffel Tower/Champ de Mars: https://www.toureiffel.paris/en/access-map
- Seine and Ile de la Cite: https://www.paris.fr/webdocs/rives-de-seine-3d
- Berlin government district: https://www.visitberlin.de/de/regierungsviertel/karte
- Berlin landmarks/streets: https://www.visitberlin.de/system/files/document/2023-04-04_BWC-Guide_2023_Komplett_SOWG_RZ_web_0.pdf

## Asset pipeline

Original generated atlases and the prompts used with the built-in image tool
are in `graphics/europe/landmarks/`. The compilers crop the atlas regions,
reduce them to GBA dimensions, quantize a shared 15-color palette per city,
and pack the indexed pixels into 4bpp tiles. Palette 7 is unused by the
original Pallet Town metatiles and is reserved for these city landmarks.
Original metatile IDs are preserved; new landmark IDs are appended.

Regenerate with `scripts/build-london-assets.py`, `scripts/build-london-map.py`,
`scripts/build-capital-assets.py`, and `scripts/build-capital-maps.py`.
The v0.50 hub blocks in `data/geography/*-v050.bin` are immutable generation
inputs, not emulator states or player saves.

## Save compatibility

The three expanded maps discard their cached tile views when loading.
The engine's saved-map empty check now respects the array bound; the former
out-of-bounds check could incorrectly restore zero tiles after clearing a
cache. The change was reproduced against v0.50 with a surfing battery save
and verified by comparing every loaded capital tile with the authored map.
No player save is edited by packaging or testing. Use normal CONTINUE with a
battery save, not a save state from another ROM build.
