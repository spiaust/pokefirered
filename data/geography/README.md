See [HISTORICAL-LONDON.md](HISTORICAL-LONDON.md) for the v0.59 Westminster district.

See [HISTORICAL-SOUTHAMPTON.md](HISTORICAL-SOUTHAMPTON.md) for the v0.58 old town.

See [HISTORICAL-LE-HAVRE.md](HISTORICAL-LE-HAVRE.md) for the v0.57 harbor district.

See [AMIENS-ROUEN.md](AMIENS-ROUEN.md) for the v0.56 historical districts.

See [STATION-BEAUVAIS.md](STATION-BEAUVAIS.md) for the v0.55 historical districts.

See [HISTORICAL-CHANTILLY.md](HISTORICAL-CHANTILLY.md) for the v0.54 historical estate.

See [COASTAL-LANDMARKS.md](COASTAL-LANDMARKS.md) for the v0.53 Dover and Calais districts.

See [REGIONAL-LANDMARKS.md](REGIONAL-LANDMARKS.md) for the v0.52 Oxford,
Chantilly and Oranienburg districts, and [LANDMARKS.md](LANDMARKS.md) for the
London, Paris and Berlin districts.

# Geographic realism and World Options

## Current playable checkpoint

The regional travel map uses clipped public-domain Natural Earth 1:50m land
polygons. A single Mercator scale projects both the coast and approximate
WGS84 city centers. Stop names are in a list so nearby towns do not have to
be moved to fit labels. At GBA resolution several nearby cities share pixels;
selecting a stop highlights its position. This is a regional overview, not a
street map.

`cities.json` stores approximate city centers, not station/landmark addresses.
`northwest-europe-land.json` records the source archive URL and SHA256.
Regenerate the checked-in C data with `python3 scripts/build-geographic-map.py`.

Sources:
- https://naturalearthdata.com/about/terms-of-use/ (public-domain terms)
- https://naturalearth.s3.amazonaws.com/50m_physical/ne_50m_land.zip

## World Options

Interact with any existing town map board to receive WORLD OPTIONS once.
Open Bag > Key Items > WORLD OPTIONS. It can also be registered to SELECT.
Up/Down chooses a row; Left/Right or A changes it; B/START returns.

- Map detail: SIMPLE or SHADED. Currently affects the regional travel map
  coastline shading only; it does not add detail to the walking maps.
- Avatar: ORIGINAL, RED or LEAF. Changes the overworld avatar; ORIGINAL uses
  the gender selected when starting the save. Trainer identity is preserved.
  This is preset selection, not a clothing/hair/skin character editor.
- Map colors: NATURAL or HIGH CONTRAST, for the regional travel map.

Use the game's normal Save command to persist choices. Defaults are zero,
so older battery saves keep the original avatar and simple natural map.
The prototype reuses the otherwise unused Fame Checker key item (363).
Variables 0x40D2-0x40D4 hold preferences. No quest IDs or collision data change.

## Active town redesign brief

The user selected compressed, recognizable layouts with optional extra
visual detail. Further story chapters are deferred while this is the active
priority. The capital walking maps now include the landmark districts described in
LANDMARKS.md. Other towns remain early prototypes. A regional map and menu are the first foundation,
not completion of the town overhaul.

Next: refine the capital districts and redesign Oxford/Chantilly/Oranienburg, the coastal
ports, and the historical towns. Preserve map/event identifiers and validate
existing-save positions when routes or buildings move. Use local rivers,
road axes, landmark placement and architecture to distinguish each town.
Extra town decoration must not change collisions, doors or quest positions.
Historical 1940 maps require separate period references.

Initial reference maps:
- London: https://www.visitlondon.com/things-to-do/london-attractions-map
- Paris: https://www.paris.fr/webdocs/rives-de-seine-3d
- Berlin: https://www.visitberlin.de/en/top-sights/map
- Oxford: https://www.experienceoxfordshire.org/oxfordshire-visitor-guide/
- Chantilly: https://chateaudechantilly.fr/parc/
