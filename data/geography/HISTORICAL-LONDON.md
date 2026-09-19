# Historical London (v0.59)

From the historical London reception, walk EAST through the opening in the
trees. Follow the paths to Parliament Square, the Palace of Westminster,
the Thames and the two river crossings. Return west for Rose, the return
transport notice and Celebi. Story characters remain in their usual places.

## Recognizable layout

Whitehall approaches Parliament Square from the north. The Palace stands
on the west side of the Thames, south of Westminster Bridge. Lambeth Bridge
provides the southern crossing, with paths connecting the two riverbanks.
The palace and clock-tower artwork is reused from the present-day London
district; the historical map does not place the London Eye or Jubilee Gardens.
The two maps have independent layouts.

These are compressed exterior landmarks, not a full recreation of London.
The palace footprint, square, river bend and distances are simplified, and
the bridges currently use ordinary path tiles rather than unique structural
art. Westminster Abbey, County Hall, surrounding streets, building interiors
and finer period details remain future work. The original reception is a
fictional story hub retained for save compatibility.

## Period references

- [Westminster Bridge, 1862](https://historicengland.org.uk/listing/the-list/list-entry/1066172)
- [Lambeth Bridge, opened 1932](https://historicengland.org.uk/listing/the-list/list-entry/1393007?section=official-list-entry)
- [Parliament's wartime damage chronology](https://www.parliament.uk/about/living-heritage/building/palace/architecture/palacestructure/bomb-damage/)
- [Clock tower history](https://www.parliament.uk/about/living-heritage/building/palace/big-ben/building-clock-tower/how-the-clock-tower-has-changed-over-the-decades/)

The game episode has no precise date within 1940. This pass uses an intact
palace exterior, not a reconstruction of damage after the September/December
1940 raids or the May 1941 destruction of the Commons Chamber. Blackout
lighting, facade paint history and individual bomb sites are not simulated.

## Compatibility and verification

Historical London has an 80x40 layout, retaining the original 24x20 quest
area and its walkable terrain/elevations. The eastern forest opening connects
to the new district. Normal CONTINUE refreshes cached terrain; expanded-area
saves retain their position. All original story objects and services stay put.

The emulator walks the square, palace and both crossings; reads all four
signs; checks every loaded terrain cell; saves beside Parliament and cold-loads
that save; verifies the historical Town Map; and returns through Southampton
and Celebi. Existing London welcome/journal/rail-booking checks, archived-save
migration and prerequisite/transport regressions cover story compatibility.
Static checks cover bounds, terrain, dialogue width, deterministic generation
and explicit absence of London Eye metatiles in the historical map.

Generator: `scripts/build-london-past-map.py`. Existing source artwork:
`graphics/europe/landmarks/london-source.png`, compiled by
`scripts/build-london-assets.py`. No new image generation was needed.

This completes the first landmark passes for the currently playable historical
destinations. Next: fuller streets and building infill, more distinctive bridge
and waterfront details, then the remaining World Options/customization work.
