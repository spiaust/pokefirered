# Historical Le Havre (v0.57)

From the original terminal, walk north to the dockworker, pass behind him
along the widened boardwalk, then follow the quay EAST into the new district.
The existing captain, Celebi, dockworker, notice and Southampton clerk remain
in their original positions. Return west for the story and ferry services.

## Recognizable geography

The compressed district places the long Bassin du Commerce to the north,
Bassin du Roy between the two old quarters, Notre-Dame church to the west,
and the Maison de l'Armateur in Saint-Francois to the east. Quay paths follow
the basins, with crossings between the quarters and a channel to the harbor
south of Bassin du Roy. A short eastern water connection suggests the route
toward the wider harbor; it does not recreate every intermediate basin.

Notre-Dame's broad facade and single flat-topped bell tower distinguish it
from the Gothic cathedrals in Amiens and Rouen. Its in-game sign calls it a
church: it did not become a cathedral until 1974. The Maison de l'Armateur
sprite represents its tall classical facade and roof lantern. Both are
simplified original exterior sprites, without accessible interiors.

## Period sources and limits

- [Notre-Dame's architecture and cathedral status](https://www.lehavreseine-patrimoine.fr/patrimoines/patrimoine-funeraire-et-religieux/cathedrale-notre-dame)
- [Maison de l'Armateur architecture and history](https://www.musees-mah-lehavre.fr/musees/maison-armateur/description-maison-de-larmateur)
- [Saint-Francois east of Bassin du Roy](https://www.lehavreseine-patrimoine.fr/patrimoines/le-havre-patrimoine-mondial/quartier-saint-francois)
- [Bassin du Commerce, municipal archives](https://archives.lehavre.fr/blog/72/le-bassin-du-commerce)
- [City archive's 1932 plan catalogue](https://archives.lehavre.fr/document-archives/plans/plan-de-la-ville-et-du-port-du-havre-apres-lannexion-de-graville-vers-1932)

The map uses pre-reconstruction landmarks appropriate to the historical
episode. Modern Perret architecture and the modern Saint-Joseph tower are
not used. Street distances, waterfront outlines and bridge positions are
compressed for play; this is not a measured 1940 street map or a reconstruction
of damage on a specific day. The archive plan is a historical reference
catalogue, not a claim that its full image was traced. The original terminal
is a fictional transport hub retained for story/save compatibility.

## Save compatibility and checks

Le Havre has its own 64x40 layout and secondary tileset. All original walkable
positions retain their terrain. Two formerly blocked dock-edge tiles form
the bypass behind the worker; other original terminal cells are unchanged.
The northern terminal exit remains blocked. Southampton keeps its own map.
Normal CONTINUE refreshes cached terrain, and saves in the new district reload
at the saved position. The player's save file is not used during testing.

The emulator walks the quays and crossings, reads all four landmark signs,
checks the complete loaded terrain, saves and cold-loads in the new district,
checks the historical Town Map and returns via Rouen and Celebi. Existing
dock quests, healing, direct port return and Southampton travel are also
tested, along with archived dockworker/ferry-clerk save migrations.
Static checks verify original harbor art, map limits, sign widths, map links
and deterministic generation.

Source artwork and built-in image-tool prompt:
[LE-HAVRE-PROMPT.md](../../graphics/europe/landmarks/LE-HAVRE-PROMPT.md).
Generators: `scripts/build-havre-assets.py`, `scripts/build-havre-map.py`.
Next geographic passes: historical Southampton and London.
