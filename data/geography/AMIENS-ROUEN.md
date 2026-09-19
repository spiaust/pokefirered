# Historical Amiens and Rouen (v0.56)

In AMIENS, walk EAST from the original story area into the new district.
Notre-Dame stands south of the Somme and Saint-Leu canal houses. Follow the
riverbanks and cross the two bridges or the small canal crossing. Return west
for the bulletin quest, train notice and Celebi.

In ROUEN, use the existing river crossing, then follow the eastern path from
the original district. The Gros-Horloge stands west of Notre-Dame Cathedral,
with the Seine and its quays to the south. The book-search area, Leon and
train notice stay in their original positions. Return west for story tasks.

## Geographic and historical interpretation

The districts compress real landmark relationships into walkable game maps.
Amiens has unequal western cathedral towers and a slender crossing fleche;
Rouen has asymmetrical towers and its tall iron spire. The Gros-Horloge has
a clock pavilion, street arch and adjoining belfry. These are simplified
original sprites, exterior scenery without building interiors.

- [Amiens cathedral visitor guide](https://www.cathedrale-amiens.fr/)
- [Amiens heritage exploration booklet](https://www.amiens.fr/content/download/31368/562634/file/Livret%2Bexplorateurs.pdf)
- [Saint-Leu in May 1940](https://www.amiens.fr/Dossier-autre/AMIENS-AU-FIL/Rue-Saint-Leu-Mai-1940-Amiens-sous-les-bombes)
- [Rouen cathedral](https://www.visiterouen.com/patrimoines/histoire/cathedrale-rouen-intime-flamboyante/)
- [Gros-Horloge](https://www.visiterouen.com/offres/le-gros-horloge-rouen-fr-3940868/)
- [Rouen city plan](https://www.visiterouen.com/app/uploads/rouen/2025/10/RT-PLAN-FRANCAIS.pdf)
- [Rouen during the Second World War](https://www.rouen.fr/fr/seconde-guerre-mondiale)
- [Rouen bridge destruction and reconstruction](https://www.rouen.fr/fr/exposition-reconstruction-rouen)

Amiens suffered bombing in May 1940; Rouen's bridges were destroyed and its
cathedral-to-Seine quarter burned in June 1940. The game's historical episode
does not establish a precise day. These intact landmark districts and playable
crossings use pre-destruction geography; they are not a reconstruction of
conditions after those attacks. Exact street plans, damage chronology and
bridge closures remain future work. The original quest areas are retained
alongside the new scenery for save compatibility.

## Implementation and verification

Amiens is 64x36 tiles; Rouen is 80x36. Each has a separate layout and tileset.
Normal CONTINUE clears stale cached terrain on these maps, preserving player
position and progression. All originally traversable tiles retain their
terrain behavior and elevation. Existing story objects and warps stay put.

The emulator tests walk both districts using button inputs, inspect signs,
check every loaded terrain cell, save in the new scenery, cold-load that save,
check the historical Town Map anchor, ride trains and return through Celebi.
Existing quest and older river/book migration tests cover the retained hubs.
Static checks cover map limits, collision reachability and dialogue width;
generation is checked byte-for-byte for reproducibility.

Artwork sources and exact prompts: [NORTHERN-HISTORY-PROMPTS.md](../../graphics/europe/landmarks/NORTHERN-HISTORY-PROMPTS.md).
Generators: `scripts/build-northern-history-assets.py` and
`scripts/build-northern-history-map.py`. Immutable v0.55 map inputs preserve
the original quest hubs. Next: historical Le Havre, Southampton and London.
