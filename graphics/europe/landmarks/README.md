# Generated landmark source atlases

Created with the built-in image-generation tool using the imagegen skill.
These files are production source assets; GBA conversions live under
`data/tilesets/secondary/europe_*`. No generated asset is referenced outside
this workspace. Map geometry and paths are authored separately.

## london-source.png — generation prompt

Create a production pixel-art GAME ASSET atlas for a Game Boy Advance top-down town RPG. Transparent background, no text, no labels, no ground, no shadows outside objects. Canvas 1024x1024. Exactly TWO isolated sprites, aligned on a pixel grid, using hard chunky pixel edges and a restrained 15-color palette, NO antialiasing or painterly texture. Upper half (x0..1023 y0..511): one front/top-down three-quarter view recognizable Palace of Westminster with ornate warm sandstone Gothic facade, long horizontal building, dark slate roof, pointed Gothic windows, Victoria Tower at LEFT and tall Elizabeth clock tower/Big Ben at RIGHT with a clear cream circular clock face and dark pointed roof; silhouette wholly within upper half with ample transparent margins. Lower half (x0..511,y512..1023): one London Eye observation wheel, near frontal/top-down RPG view, white rim, radial spokes, dark capsule outlines and A-frame feet. Lower-right quarter EMPTY. The palace will be reduced to 128x64 pixels and the wheel to64x64, so use large readable features and no tiny noise. Match classic Pokemon FireRed overworld sprite perspective and pixel density. This atlas will be converted to a 16-color GBA tileset. Transparent negative space, no floor tiles, no surrounding scenery.

The returned atlas is 1254x1254. The compiler uses its measured alpha regions;
the final palace uses 128x80 pixels to retain the clock tower silhouette.

## capitals-source.png — initial generation prompt

Production game asset atlas, transparent canvas, four isolated architectural sprites in FOUR equal quadrants with ample transparent padding so none cross the quadrant boundaries. Exactly these 4 sprites: TOP LEFT Eiffel Tower, full silhouette with four splayed legs and open arch, dark bronze lattice, pointed tip, recognizably Paris; TOP RIGHT Notre-Dame de Paris cathedral, western facade with two square towers, rose window, Gothic arches, grey limestone roofs visible in slight top-down three-quarter perspective; BOTTOM LEFT Berlin Brandenburg Gate, full width six classical columns, five openings, horizontal sandstone entablature and recognizable small green quadriga sculpture on top; BOTTOM RIGHT Berlin Reichstag building, broad symmetrical sandstone facade, four corner towers, central transparent glass dome and columned entrance. NO text, no labels, no scenery, no ground plane, no shadows outside objects. Classic Pokemon FireRed GBA town building pixel art, hard pixel edges, compact chunky forms, light from upper left, restrained colors (15 colors per city), no antialiasing or noisy photo detail. The Eiffel Tower will be reduced to64x96 pixels, Notre Dame to96x64, Brandenburg Gate to96x48, Reichstag to96x64. All silhouettes must be readable at those tiny sizes. Each building completely contained in its quadrant. Transparent negative space and open arches. This is a single sprite atlas for the game, not concept art or a full scene.

## capitals-source.png — corrective edit prompt

Convert this exact four-building sprite atlas into a production TRANSPARENT PNG with a genuinely transparent alpha channel. Remove ALL dark gradient background, glow, ground, and exterior shadows; transparent open spaces between legs/columns. Keep the four recognizable building designs and pixel-art style. Re-layout on a SQUARE canvas in FOUR EQUAL QUADRANTS with plenty of transparent padding: Eiffel Tower top-left entirely above horizontal midpoint; Notre-Dame top-right entirely above midpoint; Brandenburg Gate bottom-left entirely below midpoint; Reichstag bottom-right entirely below midpoint. No sprite crossing any midpoint. Crisp hard pixel edges. No background color and no checkerboard painted into the image.

The final transparent atlas is 1254x1254. Its actual transparent gutters are
at x=600 and y=730; the compiler uses these measured regions instead of
assuming the requested equal quadrants were followed.
