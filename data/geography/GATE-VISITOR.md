# Gate visitor room (v0.77)

This fictional compact visitor room is reached through an A-button
invitation at the west pillar (19,36), approached from (19,37). It is a
supporting gameplay interior, not a reconstruction of a real Gate room.
The central passage at x20-21 is retained. No outdoor map tiles change.

Native windows and two side exhibit benches leave a clear central route.
The guide at (8,3) connects the garden paths west of the Gate with the
courtyard east of it. Displays at (3,3) and (11,3) encourage quiet
observation and shared care. These conversations are repeatable and
change no inventory, rewards or story flags.

Both southern exit triggers return to (19,37). EuropeGateVisitor appends
after EuropeLondonEyeGallery; all earlier map IDs and layout IDs retain
their ordering. The regional-map country switch includes this room as
Germany. Normal Save/Continue retains the room and player position.

Generate with scripts/build-gate-visitor.py, then
scripts/build-capital-maps.py Berlin. The native room uses the Building
and GenericBuilding1 tilesets. Verify with test_gate_static.py and
test_gate_visitor.py. berlin-v076.bin preserves the complete outdoor
terrain, and gate-v076-map-ids.json preserves every prior Europe map ID.
