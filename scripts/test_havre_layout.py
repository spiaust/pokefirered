"""Verify the Le Havre terminal and original harbor art survive expansion."""
from pathlib import Path
import json,struct
from PIL import Image
R=Path(__file__).resolve().parents[1]
layouts={v.get('id'):v for v in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
l=layouts['LAYOUT_EUROPE_LE_HAVRE_PAST'];w,h=l['width'],l['height'];assert (w,h)==(64,40)
tiles=struct.unpack('<%dH'%(w*h),(R/l['blockdata_filepath']).read_bytes())
old=struct.unpack('<221H',(R/'data/geography/le-havre-v056.bin').read_bytes())
for y in range(13):
 for x in range(17):
  if (x,y) in ((10,4),(11,4)):
   assert old[y*17+x]&0xc00 and tiles[y*w+x]==0x3282
  else:assert tiles[y*w+x]==old[y*17+x]
assert sum(json.loads(p.read_text())['layout']==l['id'] for p in (R/'data/maps').glob('Europe*/map.json'))==1
assert (w+15)*(h+14)<=0x2800
base=R/'data/tilesets/secondary/island_harbor';new=R/'data/tilesets/secondary/europe_lehavrepast'
for name in ['metatiles.bin','metatile_attributes.bin']:assert (new/name).read_bytes().startswith((base/name).read_bytes())
assert max(t&1023 for t in tiles)<640+len((new/'metatile_attributes.bin').read_bytes())//4
before=Image.open(base/'tiles.png');after=Image.open(new/'tiles.png')
for n in range(165):
 box=((n%16)*8,(n//16)*8,(n%16)*8+8,(n//16)*8+8)
 assert before.crop(box).tobytes()==after.crop(box).tobytes()
# Original metatiles must not reference the palette reserved for new landmarks.
assert all((v>>12)!=7 for v in struct.unpack('<%dH'%(len((base/'metatiles.bin').read_bytes())//2),(base/'metatiles.bin').read_bytes()))
for p in (base/'palettes').glob('*.pal'):
 if p.name!='07.pal':assert p.read_bytes()==(new/'palettes'/p.name).read_bytes()
print('PASS: Le Havre original save positions, tiles and palettes preserved; two-cell dockworker bypass; layout fits hardware')
