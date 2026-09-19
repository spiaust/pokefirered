"""Append coastal art while retaining every original harbor tile and palette."""
from pathlib import Path
from PIL import Image
import runpy,sys
R=Path(__file__).resolve().parents[1]
build=runpy.run_path(str(R/'scripts/build-capital-assets.py'))['build']
for city in sys.argv[1:] or ['Dover','Calais']:
 source=city.lower()+'-source.png';w,h=Image.open(R/'graphics/europe/landmarks'/source).size
 # Atlas separators are recorded explicitly; visible assets need not be centered.
 split=800 if city=='Dover' else 1100
 specs=([('castle',(0,0,split,h),(96,80)),('cliffs',(split,0,w,h),(128,48))]
        if city=='Dover' else [('hall',(0,0,split,h),(96,80)),('lighthouse',(split,0,w,h),(48,80))])
 build(city+'Port',specs,source,mask_palette=True,base_name='island_harbor',base_tiles=165)
