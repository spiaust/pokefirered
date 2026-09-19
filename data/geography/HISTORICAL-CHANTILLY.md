# Historical Chantilly estate (v0.54)

In Chantilly's 1940 refuge, walk EAST from Celebi along the opening in the
trees. The estate district contains the chateau and moat, Great Stables,
formal garden paths, a canal and the Grande Pelouse south of the stables.
Return west to the original refuge for Celebi, the keeper and station guide.
The station post now has its own station district in
[v0.55](STATION-BEAUVAIS.md).

## Period basis and limits

The Grand Chateau was rebuilt in 1875-1885, and the Great Stables date from
1719-1735. Their existing exterior sprites therefore represent structures
that already stood in 1940. This release reuses those building assets with
new historical signs and a separate layout. It does not add contemporary
tourist displays or performances.

- [Grand Chateau construction history](https://chateaudechantilly.fr/en/history/the-home-of-a-prince-and-collector/)
- [Great Stables construction history](https://chateaudechantilly.fr/en/great-stables/)
- [Estate history and garden layout](https://chateaudechantilly.fr/histoire/un-domaine-au-coeur-de-l-histoire/)
- [Chantilly's horse-racing landscape](https://www.france-galop.com/en/node/9059)

This is a compressed geographic interpretation, not a reconstruction of the
estate's exact condition or access restrictions on a particular day in 1940.
The refuge, Pokemon characters and associated tasks remain fictional game
scenes. Buildings are exterior scenery. The remaining historical towns,
detailed station architecture and street networks still need further work.

## Implementation

`scripts/build-chantilly-past-map.py` generates a 56x32 map from the immutable
16x14 refuge in `chantilly-past-v053.bin`. The original arrival point, characters,
quest signs and story scripts remain in place. Only the eastern forest opening
and exposed tree edges are adjusted in the original footprint; all previously
walkable coordinates retain their elevation and terrain behavior.

The map shares the existing Chantilly building tileset. The building source
art and prompts remain in `graphics/europe/landmarks/REGIONAL-PROMPTS.md`;
no new image generation is needed. Map loading clears obsolete cached terrain
for this refuge so old batteries see the expanded estate. Character visibility
and story state still come from the original transition scripts.

## Verification

The new mGBA test loads an old arrival battery, checks every runtime tile,
walks the landmarks and signs, saves inside the estate, cold-loads the save,
checks the historical map context, returns through Celebi and completes the
original blanket task. Existing time-travel, station-post and evacuation
regressions cover unfinished visits, quest ordering, character relocation,
No/B choices and real pending rail bookings. Static checks validate all 38
maps, sign widths, old save positions, buffer limits and deterministic generation.

Use normal in-game Save and CONTINUE after updating. Player battery files are
not modified by packaging. Save states from a different ROM are unsupported.
