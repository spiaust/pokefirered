# Eclipse villain artwork

Generated with the built-in `image_gen.imagegen` tool on 2026-10-11.
Final generation prompts and source paths: `prompts.json`.
All generated source sheets are retained in `source/`; `preview.png` shows
native-size output enlarged with nearest-neighbor sampling.

| Character | Design |
| --- | --- |
| Grunt / infiltrator | Charcoal utility uniform, violet panels, crescent badge |
| Veil | Silver hair, high collar, flowing charcoal/violet coat |
| Vex | Violet bob, technician jacket, crescent badge |
| Rime | Blue hair, goggles, cold-weather scout coat |
| Boreal | Auburn hair, fur collar, expedition coat and violet scarf |
| Historical patrol | Grey-green period tunic and cap |
| Research warden | Grey lab coat, glasses, document pouch |
| Laboratory director | Olive officer coat, cap and gloves |

Run `python scripts/pack_eclipse_villains.py` with Pillow installed to reproduce
native PNG and JASC palette assets. The usual ROM build converts those into
4bpp/LZ and GBA palettes. The explicit walking-sheet conversion rule uses
2x4-tile metatiles, keeping each horizontal-strip frame contiguous.
`overworld/frame_checksums.json` records all 72 native tile-frame checksums
computed directly from the indexed PNG pixels. Battle portraits are 64x64 with index-zero
transparency and at most fifteen visible colors. Overworld sheets contain nine
16x32 frames in the engine's standard S/N/W idle and walking order; east uses
native mirroring. All walking designs share one fifteen-color palette. Vex's
last side-facing generated frame is mirrored during packing to keep its west
walking animation consistent.

`bindings.json` records 43 trainer IDs and their corresponding map actors.
Original FireRed Rocket and scientist assets are retained. Dedicated graphics
IDs keep the new art specific to Eclipse campaign encounters. A dynamically
allocated field palette keeps the uniforms independent of ordinary NPCs,
visible reserve Pokemon and weather. Historical tint and night lighting still
compose with the character palette. No save structure or RAM globals were added.
