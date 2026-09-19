"""Compile Oxford/Chantilly/Oranienburg artwork with the shared GBA pipeline."""
from pathlib import Path
from PIL import Image
import runpy,sys
R=Path(__file__).resolve().parents[1]
build=runpy.run_path(str(R/'scripts/build-capital-assets.py'))['build']
for city in sys.argv[1:] or ['Oxford','Chantilly','Oranienburg']:
 source=city.lower()+'-source.png';w,h=Image.open(R/'graphics/europe/landmarks'/source).size
 specs={
  'Oxford':[('camera',(0,0,w//2,h),(64,64)),('magdalen',(w//2,0,w,h),(48,80))],
  'Chantilly':[('chateau',(0,0,w//2,h),(96,80)),('stables',(w//2,0,w,h),(96,48))],
  'Oranienburg':[('palace',(0,0,w,h),(128,64))],
 }[city]
 build(city,specs,source,mask_palette=True)
