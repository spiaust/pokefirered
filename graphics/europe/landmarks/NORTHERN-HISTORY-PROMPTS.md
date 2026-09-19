# Amiens and Rouen source artwork

Generated with the built-in image tool and imagegen skill. Final atlases:
[amiens-source.png](amiens-source.png) and [rouen-source.png](rouen-source.png).
`scripts/build-northern-history-assets.py` performs deterministic alpha cropping,
palette reduction and GBA tile conversion. These are simplified original sprites.

## Amiens prompt

Transparent RGBA pixel-art sprite atlas for Pokemon FireRed historical Amiens. Two separate objects in left/right halves with ample transparent gap. LEFT: Notre-Dame d'Amiens cathedral, tall cream limestone Gothic west facade with three deep portals, large central rose window and TWO UNEQUAL square western towers with flat ornate tops; long grey slate roof and slender crossing fleche visible behind, raised three-quarter overworld view, recognizable Amiens silhouette, full building, target96x96 pixels. RIGHT: small row of three modest old Saint-Leu canal houses, narrow timber-framed and pale plaster facades, steep grey/red roofs, no shops signs or people, target96x48 pixels. Crisp chunky limited-palette game sprites, no modern elements, no text, no ground, no water, no shadows outside objects, no surrounding scene. Genuinely transparent background, roofs and bases fully inside each half.
# Rouen generation prompt

Transparent RGBA pixel-art sprite atlas for Pokemon FireRed historical Rouen around 1940, two isolated landmarks with a wide transparent gap. LEFT: Notre-Dame Cathedral of Rouen, ornate pale limestone Gothic western facade, deeply carved portals, two distinct asymmetrical western towers including the elaborate Butter Tower, steep grey nave roofs and extremely tall slender dark cast-iron crossing spire behind. Recognizably Rouen, raised three-quarter overworld view, all spires and base fully visible, target96x96 pixels. RIGHT: Gros-Horloge of Rouen, Renaissance stone clock pavilion spanning a single arched street passage, prominent round blue clock dial with golden sun and golden numerals, ornate red/gold decorations, slate-roofed belfry adjoining its left side, target64x80 pixels. Each full landmark entirely within its own half. Chunky crisp pixel-art shapes with a shared limited 15-color palette, no photo texture, no modern signage or cars, no people, no ground or cast shadows outside buildings, no text labels, no scenery. Genuinely transparent alpha.
