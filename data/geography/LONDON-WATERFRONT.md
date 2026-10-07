# London waterfront (v0.62)

The modern map now distinguishes Westminster Bridge with green rails and
the southern Lambeth crossing with red rails. Small overlays use the
existing native palette and retain the full two-row walking clearance.
The London Eye's garden loop connects back to the riverside paths. Existing
Parliament and garden signs explain these routes.

This remains a compressed district. The rail overlays suggest the bridges'
colour and structure; they do not reproduce their arches or full geometry.
Historical London's independent layout is unchanged. Its shared landmark
tiles retain their IDs and appearance.

References:

- [Historic England: Lambeth Bridge and its red scheme, contrasted with green Westminster Bridge](https://historicengland.org.uk/listing/the-list/list-entry/1393007?section=official-list-entry)
- [South Bank: Queen's Walk and riverside landmarks](https://southbank.london/see-and-do/queens-walk)
- [London Eye: location opposite Parliament](https://www.londoneye.com/plan-your-visit/before-you-visit/directions/)

All v0.61 map cells retain collision, elevation and land/water type. The
old terrain is stored in london-v061.bin for compatibility verification.
New rail tiles append to the London tileset without changing existing
metatile IDs or allocating a new palette. The interior generator updates
existing entrances in place so it does not reorder the town's events.

Regenerate with build-london-assets.py and build-london-map.py. Verify with
test_london_waterfront.py, test_london_realism.py, test_landmark_cases.py
Westminster, and test_london_past_realism.py in scripts/.

## Garden visitors (v0.79)

A stationary visitor at (30,34) and native JIGGLYPUFF at (31,34) rest beside
the South Bank flower beds. Speak from (30,35) or (31,35). The visitor
points toward the Eye gallery. The repeatable dialogue and normal cry
change no inventory or story state. The paved garden loop, bridge
crossings, gallery entrance and existing signs remain reachable.

Every v0.78 London tile is retained in london-v078.bin. The original four
objects retain their exact templates and order; the two visitors append
afterward. Older London saves restore only these two stationary templates
on Continue. All map and layout IDs are unchanged.

Regenerate with build-london-map.py. Verify with test_london_garden.py,
test_london_garden_static.py, the waterfront generation and London walking
checks, the Westminster case and the Eye gallery visits/cold saves.
