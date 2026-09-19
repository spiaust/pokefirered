# Coastal landmark districts (v0.53)

Take the existing coach from London's station to Dover or from Paris's station
to Calais (the third badge is required). From the ferry arrival position,
walk UP twice, then EAST along the quay to explore. The existing north exit
still returns to the city and the sailor still offers the Channel crossing.

| Port | New district |
| --- | --- |
| Dover | Square Norman Great Tower, chalk cliff face meeting the sea, clifftop path, seafront promenade and a harbor arm |
| Calais | Red-brick town hall and belfry, white lighthouse in the maritime quarter, northern seafront promenade, pier and garden paths |

These are compressed landmark districts, not complete street replicas.
Dover's castle is inland of the waterfront and west of the cliff section;
Calais's hall lies south of its lighthouse and northern seafront. The retained
ferry terminal occupies a separate compressed corner, so its placement and
orientation do not reproduce the real passenger terminals. Neighborhoods,
beaches, natural shoreline curves and detailed harbor infrastructure remain
future refinements. Buildings are exterior scenery, without enterable rooms.
WORLD OPTIONS does not yet toggle walking-map decorations.

## Official geographic references

- [Dover Castle and its Great Tower](https://www.english-heritage.org.uk/visit/places/dover-castle/history-and-stories/history-dover/)
- [National Trust White Cliffs](https://www.nationaltrust.org.uk/visit/kent/the-white-cliffs-of-dover)
- [Harbor-to-cliffs route map](https://static.nationaltrust.org.uk/trails/visit/kent/the-white-cliffs-of-dover/dover-cruise-terminal-to-white-cliffs-visitor-centre-trail-walking.pdf)
- [Calais town hall and belfry](https://www.calaisxxl.com/en/offers/have-to-do/Calais-Town-Hall-and-Belfry/)
- [Calais lighthouse](https://www.calaisxxl.com/en/offers/have-to-do/the-calais-lighthouse/)
- [Calais seafront and maritime quarter](https://www.calaisxxl.com/en/inspirations/visiter-calais-incontournables/)

The official sources inform the landmark choices and relationships. Artwork
is original generated pixel art. Sources and complete built-in image-tool
prompts are recorded in
[`PORT-PROMPTS.md`](../../graphics/europe/landmarks/PORT-PROMPTS.md).

## Implementation and compatibility

`scripts/build-port-assets.py` retains the original Island Harbor's 165 tiles,
metatiles and used palettes, then appends landmark art using unused palette 7.
It uses the shared compiler with explicit base tileset parameters; defaults
for the previous six towns remain unchanged. Dover uses 381 of the available
384 secondary tiles; Calais uses 345. Atlas separators and alpha-threshold
crops are explicit and deterministic.

`scripts/build-port-maps.py` creates individual 56x40 layouts and preserves
every tile of the original 17x13 terminal. Original map IDs, captain/boat
coordinates, arrival positions, coach exits and transport scripts are kept.
Existing port batteries are migrated from the shared Island Harbor layout
to the appropriate individual layout and their old cached tiles are cleared.
No other Island Harbor maps use the new artwork or layout.

Use normal Save and CONTINUE when updating. Emulator states from a different
ROM build are unsupported. Packaging leaves player battery files untouched.

## Verification

Each port is built and tested individually before the combined release.
Headless mGBA walks the landmarks through real input, reads signs, checks all
loaded tiles, saves in the district, cold-loads that save, opens/closes the
regional map, crosses the Channel twice and exits by coach. Separate transport
checks cover badge gating, No/B choices, coach entry and an old saved train
booking resumed through Paris to Berlin. Earlier capital, regional and
historical travel tests cover shared map-loading behavior. Static checks
validate all 38 European maps, terminal preservation, palette/tile limits,
path connectivity, sign widths and byte-for-byte regeneration.

Historical town redesigns and finer modern neighborhood detail remain next.
