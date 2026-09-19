# Regional landmark source atlases

Generated with the built-in image tool and imagegen skill. Final source files are stored beside this document. scripts/build-regional-assets.py performs deterministic palette and GBA tile conversion. Transparent RGB pixels are excluded from palette selection. Original generation prompts follow.

## oxford-source.png

A production sprite atlas with TWO completely isolated Oxford landmark building sprites side-by-side on a truly transparent RGBA background. Left half: Radcliffe Camera, recognizably circular Palladian Oxford library, honey limestone, two tiers with arched windows, columned drum, large grey lead dome and small lantern. Right half: Magdalen College Great Tower, tall square honey-stone Perpendicular Gothic bell tower with four slender corner pinnacles, crenellated top, long arched belfry windows; small college wing attached at its foot. Classic Pokemon FireRed top-down 3/4 overworld building pixel art. Radcliffe will become64x64 pixels, Magdalen48x80 pixels. Hard chunky pixel edges, 15-color palette, large readable silhouettes, no photo texture, no antialiasing. Transparent holes and ample transparent padding between and around sprites. No ground, no cast shadows, no scenery, no labels, no text, no border. Both structures fully visible, no cropped roofs or feet. This is production building art for a playable GBA town.

## chantilly-source.png

Production transparent RGBA sprite atlas: TWO isolated Chateau de Chantilly estate buildings side-by-side, with a wide transparent gap. LEFT: recognizable Chateau de Chantilly, pale warm French limestone Renaissance chateau, ornate grey-blue steep slate roofs, round corner towers with pointed conical roofs, tall chimneys and complex central roof pavilion; front/top-down three-quarter game building view. RIGHT: Chantilly Grandes Ecuries (Great Stables), long low symmetrical classical sandstone facade and wings, prominent central dark slate dome over a grand arched entrance, small sculptural group at dome top. Each entire building within its half, large transparent margin. Classic Pokemon FireRed GBA pixel-art overworld style, crisp chunky pixels, 15-color palette, silhouettes readable when left sprite is96x80 pixels and right sprite96x48. No fine noisy texture, no antialiasing. NO background, no water, no ground, no cast shadows, no scenery, no text/labels. Genuinely transparent alpha channel.

## oranienburg-source.png

Create ONE isolated production game building sprite of Schloss Oranienburg, the recognizable Brandenburg baroque palace: long white/cream symmetrical facade, central slightly projecting entrance pavilion with pediment, rows of dark windows, warm terracotta hipped roofs, two forward side wings making an open forecourt. Low broad horizontal palace, no fantasy spires or castle towers. Slight elevated front/top-down 3/4 view matching Pokemon FireRed overworld building sprites. Crisp hard chunky pixel art, restricted15 colors, readable silhouette reduced to128x64 pixels. Whole building visible with generous padding on a genuinely transparent RGBA background. NO ground, no gardens, no water, no shadows outside the building, no scenery, no people, no text, no labels, no painted checkerboard. Production GBA landmark sprite.

## Oxford corrective edit

Remove the entire dark/gradient background, glow and all external shadows from this Oxford sprite atlas. Return a true transparent RGBA PNG, with transparent empty space around and between BOTH buildings, never a painted checkerboard. Preserve both pixel-art building designs and all their visible architecture. Keep the Radcliffe Camera fully in the LEFT HALF and Magdalen Tower fully in the RIGHT HALF, with a large transparent central gap. Both entire buildings including roofs and bases must remain fully visible. No ground or scenery.

