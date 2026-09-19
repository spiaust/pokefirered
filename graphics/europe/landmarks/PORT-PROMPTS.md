# Coastal landmark source artwork

## Calais prompt

Use case: stylized-concept. Transparent production sprite atlas for a Pokemon FireRed GBA overworld, two fully isolated landmarks side-by-side on actual transparent RGBA. LEFT HALF: Calais Hotel de Ville and its famous belfry, recognizable red-brick Flemish Renaissance town hall, pale stone trim, steep blue-grey roof, tall slender square clock belfry with ornate dark upper lantern and pointed spire, belfry attached to the right end of the long civic hall. Entire silhouette visible, top-down three-quarter game view, destination 96x80 pixels. RIGHT HALF: Calais lighthouse, tall slender WHITE OCTAGONAL masonry tower, black upper lantern base and black lantern roof, little simple pale base building, destination 48x80 pixels. Pixel art, crisp chunky edges, limited shared 15-color palette, simplified readable architecture. Both sprites entirely within their own halves with generous transparent gap and transparent padding. NO scenery, no ground, no cast shadow outside objects, no text, no labels, no cropped spires, no background.

Generated using the built-in image tool with the imagegen skill. Final atlases
are saved here as [dover-source.png](dover-source.png) and
[calais-source.png](calais-source.png). Technical palette
and tile conversion is performed by `scripts/build-port-assets.py`.

## Dover original prompt

Use case: stylized-concept. Production sprite atlas for a Pokemon FireRed GBA town, TWO isolated sprites on transparent RGBA. LEFT HALF: Dover Castle Great Tower, recognizable massive square pale grey Norman stone keep with four corner turrets, crenellations, narrow windows, short surrounding curtain wall; top-down three-quarter overworld view, whole structure visible, destination size 96x80 pixels. RIGHT HALF: long horizontal section of Dover white chalk cliffs, grassy green top, white vertical stratified face with sparse grey cracks, no sea or buildings, destination size 128x48 pixels. Completely separate assets with ample transparent space between, each in its own half. Crisp chunky pixel art with readable silhouettes and a small shared color palette. No scenery background, no shadows outside objects, no labels, no text, no cropped edges. Actual transparent alpha.

## Dover correction prompt

Correct ONLY the castle in the left half of this transparent sprite atlas. It must depict Dover Castle's actual Norman Great Tower: massive SQUARE/RECTANGULAR stone keep, four RECTANGULAR SQUARE corner turrets / projecting buttresses with flat crenellated tops, rectangular walls, narrow slit windows, NOT cylindrical towers. No round towers anywhere. Simplify the surrounding low curtain wall accordingly. Keep the same pixel-art game view, colors, scale, isolated full silhouette and actual transparent background. Keep the chalk cliff sprite in the right half completely unchanged. Keep the assets in separate left and right halves with ample gap.
