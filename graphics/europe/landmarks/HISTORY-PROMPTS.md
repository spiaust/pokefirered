# Historical station and Beauvais artwork

## beauvais-source.png

Use case: historical-scene. Production transparent RGBA sprite atlas for a Pokemon FireRed overworld set in Beauvais, France, around 1940. TWO isolated assets, one fully inside each half. LEFT HALF: unmistakable Cathedral Saint-Pierre of Beauvais seen from a raised south-east three-quarter view: an exceptionally TALL Gothic choir with rounded polygonal apse, dense tall flying buttresses, enormous pointed clerestory windows, grey steep roof and broad south transept with rose window. It is an UNFINISHED cathedral consisting of CHOIR AND TRANSEPT: NO long western nave, NO twin west towers, NO central spire (the spire collapsed centuries earlier). Pale cream limestone, bold readable buttress silhouette, destination 96x96 pixels. RIGHT HALF: medieval Beauvais episcopal palace gatehouse, two stout ROUND stone towers with tall dark conical slate roofs flanking a central arched gateway, short stone wall/roof wing, destination 96x64 pixels. Historic exteriors without modern restoration scaffolding or museum branding. Crisp chunky limited-palette pixel art, top-down three-quarter GBA building sprites. Entire buildings and roofs visible with generous transparent margin and a wide gap between halves. No people, no ground, no shadows outside objects, no scenery, no labels, no text. Genuinely transparent alpha background.

Generated with the built-in image tool and imagegen skill. Final source
atlases are [chantillypost-source.png](chantillypost-source.png) and
[beauvais-source.png](beauvais-source.png), beside this file. `scripts/build-history-assets.py` crops them
and performs deterministic palette/tile conversion for the game.

The station is a period-inspired regional station interpretation, not a
measured reconstruction of Chantilly-Gouvieux's facade.

## chantillypost-source.png

Use case: historical-scene. A production sprite atlas with two isolated assets on genuinely transparent RGBA for a Pokemon FireRed overworld set in France in 1940. LEFT TWO THIRDS: modest Chantilly-Gouvieux-inspired northern French railway passenger station, long low cream limestone facade, red-brown brick accents, central two-storey pavilion with steep dark slate hipped roof, single-storey wings, tall evenly spaced arched windows and simple central entrance, small round clock on central facade. Top-down three-quarter game view, exterior only. Destination 96x64 pixels. It should be a restrained historic regional station, no modern glass extension, no electrical catenary, no contemporary logos, no text. RIGHT THIRD: separate simple horizontal railway track tile strip, two parallel steel rails left-to-right, repeating brown wooden sleepers on grey gravel ballast, viewed from above, rectangular full square strip for repeatable 32x32 pixel conversion. Large transparent gap separates building and track. Entire building with roofs and base visible, hard chunky pixel art, limited 15-color palette shared between sprites, no shadows outside objects, no people, no background, no labels.
