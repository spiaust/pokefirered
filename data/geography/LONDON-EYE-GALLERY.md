# London Eye visitor gallery (v0.70)

A fictional compressed gallery uses native windows and two exhibit boards.
This is a visitor room, not a working wheel ride or a reconstruction of an
actual capsule. The attendant introduces South Bank walks; garden and
bridge displays help visitors recognize the outdoor paths and crossings.
Conversations give no rewards and do not change story flags or inventory.

Face (29,28) from (29,29) and press A to enter. Both front exits return to
(29,29). The gallery map is appended after the Eiffel room. London outdoor
tiles are byte-identical to the retained london-v069.bin fixture. Existing
Westminster access and historical London remain unchanged.

Regenerate with scripts/build-eye-gallery.py, then scripts/build-london-map.py.
Verify using scripts/test_eye_static.py, scripts/test_eye_gallery.py,
scripts/test_london_realism.py and the Westminster landmark-case test.
