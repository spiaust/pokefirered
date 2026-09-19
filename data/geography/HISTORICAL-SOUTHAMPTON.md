# Historical Southampton (v0.58)

From reception, walk EAST past the London clerk along the new boardwalk,
then north around the two workers and east along the existing quay. The
original host, Celebi, luggage worker, luggage pickup and London clerk stay
in their usual positions. Return west for the existing story services.

## Landmark relationships

Bargate stands at the north end of the new district. High Street runs south
toward Town Quay and the waterfront. Tudor House lies west of High Street,
beside the old lanes, with three simplified medieval wall sections further
west. A short lane representing Blue Anchor Lane connects the wall-side walk
to the interior streets. Walk alongside the walls, then continue to the quay.

The gateway, timber-framed house and crenellated wall sections are original
pixel-art interpretations. They are exterior scenery; Bargate's arch is not
a walk-through tunnel and the walls cannot be climbed. Routes go around them.
The map preserves the main relative positions at a compressed scale rather
than copying every building, lane or waterfront contour.

## Period references and limits

- [City Council: Old Town, Bargate, High Street and western walls](https://www.southampton.gov.uk/moderngov/documents/s16090/CCAP-MRD%20-CCMP%20final%20130305.pdf)
- [City Council: monument history, including Bargate's 1930s changes](https://www.southampton.gov.uk/culture-leisure-tourism/history-and-preservation/monuments-and-landmarks/history-southampton-monuments/)
- [Tudor House history and its 1912 museum opening](https://tudorhouseandgarden.com/explore/history/)
- [Official Walk the Walls route](https://www.visitsouthampton.co.uk/walk-the-walls-trail/)

The landmarks predate the 1940 story. Gaps around Bargate are consistent with
the removal of adjoining wall sections before the war. The flower patch is
generic landscaping, not Tudor House's modern reconstructed garden, which
was designed in the 1980s. Modern shops, exhibition branding and contemporary
waterfront facilities are not represented. The dock remains a fictional
reception hub. This is a first landmark pass, not a measured street plan or
a day-specific reconstruction of wartime damage. Infill buildings, exact
wall profiles and street furniture remain future work.

## Compatibility and verification

Southampton has its own 64x40 layout and secondary tileset. All old walkable
terrain is unchanged. Three previously blocked edge cells become a boardwalk
around the luggage worker and London clerk; the original northern exit stays
blocked. No story character or pickup moves. Normal CONTINUE refreshes stale
cached terrain, and saves made beside the new landmarks reload in place.

Button-driven emulator checks cover the bypass, landmarks, lane and quay,
all four signs, every loaded terrain cell, cold-save reload, historical map,
Le Havre ferry round trip and Celebi return. Existing travel, luggage, care,
Oxford report and London travel tests cover story compatibility. Archived
v0.44/v0.48 saves verify immediate interactions beside the two workers.
Static checks cover original art/palettes, old terrain, map limits, dialogue
width and byte-for-byte reproducible generation. User saves are not used.

Source artwork and exact built-in image-tool prompt:
[SOUTHAMPTON-PROMPT.md](../../graphics/europe/landmarks/SOUTHAMPTON-PROMPT.md).
Generators: `scripts/build-southampton-assets.py` and
`scripts/build-southampton-map.py`. Next: historical London.
