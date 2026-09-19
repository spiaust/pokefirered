# Historical station and Beauvais districts (v0.55)

At the Chantilly station post, walk EAST from Celebi to the station forecourt
and trackside paths. The original notice still handles train boarding, and
the original dispatcher and refuge guide remain at their usual positions.

In Beauvais, accept Elise's existing garden visit when unlocked, then walk
EAST from the garden into the cathedral district. Explore Saint-Pierre's
choir and transept, the twin-towered episcopal palace gate, the river paths
and two crossings. Return west to the garden guide or Celebi. Reception stays
in its existing interior, and Luc's Pidgey quest stays in the original garden.

## Historical interpretation

Beauvais's recognizable cathedral silhouette consists of the tall choir and
transept, without an invented long nave or twin western towers. The palace's
fortified entrance has two round towers. These are simplified original sprites
based on the surviving historic structures. The river and street relationships
are compressed, not a measured historical street plan.

- [Saint-Pierre's choir and transept](https://www.visitbeauvais.fr/fiche/cathedrale-saint-pierre-de-beauvais/)
- [Cathedral and episcopal quarter](https://800anscathedrale.beauvais.fr/en/la-cathedrale-saint-pierre/la-cathedrale-saint-pierre-la-cathedrale-et-son-quartier-episcopal/)
- [Palace history and fortified towers](https://mudo.oise.fr/decouvrir/lhistoire-du-palais/)
- [Cathedral history, including 1940 damage](https://cathedrale-beauvais.fr/historique-de-la-cathedrale-de-beauvais/)
- [Chantilly's station-to-estate heritage route](https://www.ville-chantilly.fr/decouvrir-chantilly/chantilly-ville-dart-et-dhistoire/)

Beauvais suffered major damage in June 1940. This game map does not establish
a precise day or reproduce the extent of damage street by street. It should
not be read as an intact post-bombardment reconstruction. The station building
is a period-inspired regional station interpretation, not an exact recreation
of Chantilly-Gouvieux's facade. The refugee tasks and Pokemon are fictional.
Landmarks are exterior scenery; the rail strip is a walkable scenic crossing,
not a moving-train system. Finer streets, damage chronology and measured
station architecture remain future work.

## Save compatibility and implementation

The station post previously shared the refuge layout. v0.54 expanded that
shared layout, unintentionally giving both locations estate scenery. v0.55
assigns the post its own 56x32 layout and migrates old saved layout IDs on
Continue. All on-foot coordinates reachable in v0.54 remain traversable at
the same elevation. This includes saves made in its expanded eastern area.
The refuge retains its estate. A regression asserts these historical maps
have distinct layouts to prevent scenery changes spreading to another map.

Beauvais Garden expands from 24x20 to 64x36; its original quest area and
arrival coordinates are preserved. Old terrain caches are cleared for both
updated maps. Original object scripts control character and Pidgey visibility.

Generators: `build-history-assets.py`, `build-chantilly-post-map.py` and
`build-beauvais-map.py`. Immutable inputs are `chantilly-post-v054.bin` and
`beauvais-garden-v054.bin`. Original generated atlases and complete built-in
image-tool prompts are in
[`HISTORY-PROMPTS.md`](../../graphics/europe/landmarks/HISTORY-PROMPTS.md).

## Verification

Each map was built and tested before the next. A battery was created through
normal walking and Save in the actual v0.54 ROM's expanded post, then migrated
and checked tile by tile. New mGBA tests walk the station and Beauvais landmarks,
read signs, save/cold Continue, check era-map return and use the original exits.
Story regression covers the station notice, evacuation, Pidgey reunion,
onward Amiens travel, the refuge and pending rail bookings. Static checks cover
old walking coordinates, separate layouts, hardware bounds, all 38 European
maps, dialogue widths and deterministic generation.

Use normal Save and CONTINUE when updating. Packaging leaves player batteries
untouched and retains the previous ROM. Amiens and Rouen are next on the
historical map roadmap.
