# Walking-map decoration (v0.71)

WORLD OPTIONS adds a fourth row, FLOWERS: ON/OFF. Save variable 0x40C3
stores 0 for flowers (default) and 1 for lawn. The choice uses normal
Save/Continue; no trainer identity, party, inventory or quest state is
modified. The original three menu rows retain their order and controls.
UP/DOWN now wraps across all four rows.

Only the camera's metatile renderer substitutes General flower metatile
0x004 with lawn 0x010. Rendering uses the lawn's layer arrangement. The
map grid, metatile getters, attributes, collision and elevation remain
unchanged. The substitution is restricted to the Europe map group and
TOWN/ROUTE map types, so indoor exhibits and other regions keep their art.
Menu return, scrolling and cold map load use the same renderer.

Verify with scripts/test_world_flowers.py, scripts/test_world_options.py
and scripts/test_world_options_movement.py. The flower test toggles the
fourth row through real input, checks the complete loaded map grid,
walks over the beds, cold-loads the saved choice and restores flowers.

## Restore Defaults (v0.72)

The fifth World Options row restores all four cosmetic preferences after
a separate confirmation. A enters the confirmation and A confirms; B or
START returns to the options menu without changes. Left/Right on the
restore row do nothing. The original four rows retain their order.
The reset writes only the four preference variables to zero. Original
avatar selection is applied through the existing return-to-field path.
Use normal Save/Continue to retain the choices. Test with
scripts/test_world_defaults.py alongside the existing options tests.

## Outfit colors (v0.73)

Save variable 0x40C4 stores CLASSIC (0), BLUE (1) or GREEN (2). The new
menu row follows FLOWERS; Restore Defaults moves to the final sixth row
and clears the outfit preference too. Older saves default to CLASSIC.

Player palette loading substitutes only entries 8, 11 and 12, with matching
reflection shades. Every other palette entry stays unchanged. Normal
player tags are limited to the reserved player palette slot; NPC colors
and maps outside Europe retain their native palettes. Existing walking,
cycling and other player sprite frames are reused. Battle portraits and
trainer-card art keep their native artwork; this is a field-avatar option.

Test with scripts/test_world_outfit.py and the existing World Options,
flower, movement and defaults tests. Outfit tests compare all sixteen
palette entries, both avatar choices, cycling/dismount and cold saves.

## Live preview and indoor location labels (v0.74)

The World Options screen displays a native walking sprite for the chosen
avatar and outfit. The menu owns its sprite template and palette slot;
repeated changes release the prior sprite safely. Reset confirmation hides
the preview, and cancel/confirm redraws it. Closing removes its resources
before field return. The regional map does not display the preview.

The regional map also recognizes the Eiffel visitor map as France and the
three Berlin courtyard room maps as Germany. Older indoor battery saves
retain their coordinates, progress and proper map labels. Verify with
scripts/test_world_preview.py and scripts/test_visitor_map_locations.py
alongside the existing World Options checks.

## Walking/cycling preview (v0.75)

SELECT toggles a menu-local pose using the native walking and bicycle
graphics IDs. Reopening starts at WALK. Outfit and avatar changes retain
the selected preview pose. Confirmation ignores SELECT, and field movement
and save variables are untouched by the toggle.
