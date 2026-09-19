"""Compile historical station and Beauvais exteriors into GBA tilesets."""
from pathlib import Path
from PIL import Image
import runpy,sys
R=Path(__file__).resolve().parents[1]
build=runpy.run_path(str(R/'scripts/build-capital-assets.py'))['build']
for city in sys.argv[1:] or ['ChantillyPost','Beauvais']:
 source=city.lower()+'-source.png';w,h=Image.open(R/'graphics/europe/landmarks'/source).size
 split=round(w*0.67) if city=='ChantillyPost' else 1050
 specs=([('station',(0,0,split,h),(96,64)),('track',(split,0,w,h),(32,32))]
        if city=='ChantillyPost' else [('cathedral',(0,0,split,h),(96,96)),('palace',(split,0,w,h),(96,64))])
 build(city,specs,source,mask_palette=True)
