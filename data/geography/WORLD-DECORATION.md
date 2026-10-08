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

## Travel-map Places guide (v0.80)

R opens a present-day Places page using the current stop selection. D-pad
browsing retains the page. B/START/R returns to the map; A returns with
route information and SELECT opens the journal. Journal navigation ignores
R. The page uses task-local data only and writes no saved preferences.
The map temporarily reserves R from native Help and restores the previous
reservation on exit; World Options retains its existing input behavior.

Use test_map_places.py for all eight stops, wrapped selection, R/B/START/A,
story return, Help restoration and unchanged save state from present and
historical battery saves. test_map_places_static.py measures all 35 text
lines and the map shortcut hint against the actual native font.

## Four-direction preview (v0.81)

R cycles native standing animations south, west, north and east. Direction
is menu-local and survives pose/avatar/outfit redraws. Reopening initializes
south. Restore confirmation ignores R, while cancellation restores the
chosen preview direction. World Options now reserves R from native Help
and restores the previous reservation on closing, as the travel map does.

Use test_world_preview_facing.py for every avatar and walking/cycling pose,
four-turn wrap, confirmation, reopening, unchanged save data and Help
restoration. Native sprite animation indices are verified, and side/back
screenshots are inspected. The font-fit test also covers both preview hints.

## Purple clothing ramp (v0.82)

Outfit value 3 adds Purple after the unchanged Classic/Blue/Green values.
Native player palette entries 8, 11 and 12 use RGB5 (10,4,14), (25,15,29)
and (18,8,23), with lighter corresponding reflection shades. Other entries
are copied unchanged. The menu uses a four-color cycle; no extra save
variable is allocated. Restore Defaults continues to set outfit value 0.

Use test_world_purple.py for Red/Leaf palettes, native non-clothing colors,
cycling/dismount, turned preview, Save/cold Continue and exact Classic
restoration. The original outfit test retains Blue/Green coverage and
checks Green-to-Purple-to-Classic cycling. Defaults now tests cancellation
and confirmation from Purple. Existing direction and Places checks run.

## v1.00 capital Rooms pages

In travel-map Places, L switches to a four-line Rooms page for London,
Paris and Berlin. It describes the east neighborhood approach and each
room's readable details. Existing Places landmark guidance is retained.
L returns to Places; changing stops resets the view. Noncapital stops
keep their usual Places page and have no Rooms shortcut. R/B/START/A and
SELECT retain their map/routes/story behavior. All guidance is explicitly
present-day, including when opened from a historical save.

The transient sEuropePlacesRooms flag resets on map initialization and
page exits; no saved variables or map IDs change. Native Help is suspended
while the map is open and its enabled/R-toggle states are restored on exit.
Physical L is handled before A to support L=A saves. test_map_rooms.py checks
retained batteries from all three capitals, controls and exact state on
exit. test_map_places_static.py checks 50 strings against native widths.

## v1.05 rail-clerk booking cues

The shared rail welcome explains previewing, B/Exit and booking only on
boarding. The same-station response explains how to choose another stop.
Routing, transfers, saved booking and cancellation commands are unchanged.
rail-clerk-v104.inc retains the complete prior script; rail_compatibility.py
normalizes only the two changed text blocks for older byte-hash checks.
The dedicated static test requires every other command/text block to match.

Native-input coverage uses retained arrival batteries at all six stations
and a genuine pre-change rail-clerk-transfer-v104 battery created in London
during an Oxford-to-Oranienburg trip. It checks menu cancellation, preview
No/B, saved-transfer keep/cancel and completion through Paris and Berlin.
Each stationary cancellation checks exact party, inventory and progress.

## v1.06 intermediate rail guidance

Only Europe_Train_Text_Board changes. It names the final destination, points
to local wall notices and explains retained bookings during exploration.
rail-transfer-v105.inc preserves the full prior source; before_transfer_cues
restores only that text for exact command compatibility checks. Runtime
coverage follows a genuine old transfer through a Paris garden visit, a
cold Save/Continue, Berlin and final Oranienburg arrival.

## v1.07 returning rail passengers

Only Europe_Train_Text_Resume changes. Three pages show the saved route,
retained booking during exploration, and the boarding/cancellation choice.
rail-resume-v106.inc preserves the previous source; before_resume_cues
restores only this dialogue for exact compatibility checks. Cold battery
tests cover London transfer and Paris exploration, keeping and boarding.

## v1.08 booked arrivals on foot

Only Europe_Train_Text_Completed changes. It names the reached destination,
confirms the cleared booking and invites a new trip. The v1.07 full source
is retained in rail-completion-v107.inc. Compatibility restoration replaces
exact dialogue byte blocks so mixed line endings remain intact. Genuine
v1.07 walking-arrival saves cover all three branch towns; runtime checks
verify completion, fresh menus, cold Continue and return journeys.

## v1.09 walking detours and route origin

One Resume dialogue line now explains the route begins at the current
station. rail-detour-v108.inc retains the previous complete script; exact
byte restoration proves every command remains unchanged. Old-ROM batteries
cover Oxford and Chantilly detours with Oranienburg booked, rejoining the
main line, cold Continue and final arrival.

## v1.10 branch-station wall notices

The shared station-boards.json generator now includes Oxford, Chantilly
and Oranienburg. Each adds one readable background event at (9,1) on
existing solid furniture, with two pages of Gym/contact/south-walk directions.
branch-station-v109.json retains complete old maps/scripts and map groups.
No room grid, staff, service or shared rail command changes. Runtime checks
use genuine v1.09 indoor batteries plus new cold Continue saves.

## v1.11 branch-town exterior station signs

Only the existing station entrance text blocks gain a second page naming
the Gym direction and local quest contact. Route signs already identify
the complete southbound walks. Baseline: branch-signs-v110.json.

## v1.12 exterior Gym guidance

The exterior signs add a regional quest hand-in page. Indoor statues remain
exact; the existing leader challenge gates are unchanged. Baseline:
gym-signs-v111.json.
