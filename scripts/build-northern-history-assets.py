"""Compile Amiens and Rouen historical landmark atlases."""
from pathlib import Path
from PIL import Image
import runpy,sys
R=Path(__file__).resolve().parents[1]
build=runpy.run_path(str(R/'scripts/build-capital-assets.py'))['build']
for city in sys.argv[1:] or ['Amiens','Rouen']:
 source=city.lower()+'-source.png';w,h=Image.open(R/'graphics/europe/landmarks'/source).size
 split=1100 if city=='Amiens' else 950
 specs=[('cathedral',(0,0,split,h),(96,96)),('houses' if city=='Amiens' else 'clock',(split,0,w,h),(96,48) if city=='Amiens' else (64,80))]
 build(city,specs,source,mask_palette=True)
