# Eclipse title artwork

Original temporal-eclipse European skyline generated with the built-in
`image_gen.imagegen` tool; full prompt is in `prompts.json`. The source is
preserved in `source/backdrop.png`. The existing game logo and native font
supply crisp lettering. No new online asset was needed for this change.

`python scripts/pack_eclipse_title.py` (Pillow) deterministically resizes,
composites and indexes the artwork into a 16-color 240x160 background.
The game adds a hovering Celebi, tagline and blinking Start prompt.
`preview.png` shows only the packed background; emulator captures include
all runtime elements. Copyright artwork displays the requested 2026 dates
and retains the four original company credits, plus an Eclipse 2026 line.
The credit tilemap uses screen block 31 to avoid overlapping its 600 tiles.

Native title music, fade, Start/A, Continue, save-clear shortcut and Berry Fix
shortcut retain their existing callbacks. No save layout changes.
