# Paris garden and promenade pass (v0.61)

The compressed Eiffel Tower / Champ de Mars district now has paved loops
around its flower beds, western and eastern garden approaches, and a
clearer left-bank promenade leading toward Notre-Dame's island bridge.
The Eiffel and Seine signs describe these routes.

The tower remains west of the island landmark, with the gardens south of
the river. This is a condensed gameplay arrangement, not a street-by-street
reconstruction. The paths are inspired by the relationships shown on the
[Eiffel Tower's official access map](https://www.toureiffel.paris/en/access-map).
No additional real street names are assigned to the compressed paths.

Every v0.60 map cell retains its collision, elevation and land/water type.
The river, bridges, landmark footprints, services and Notre-Dame entrance
stay in place. The map refresh on normal Continue displays the new paving
without relocating the player. The v0.60 terrain snapshot is retained as
an automated compatibility fixture.

Regenerate with `scripts/build-capital-maps.py Paris`. Verify with
`scripts/test_paris_promenade.py`, `scripts/test_capital_realism.py Paris`
and `scripts/test_landmark_cases.py NotreDame`.

Next town-detail work: more distinctive waterfront/bridge treatment in
London, followed by street and building infill that respects saved positions.
