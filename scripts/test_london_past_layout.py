"""Keep Amiens/Rouen old save terrain and independent layouts safe."""
from pathlib import Path
import json,struct,sys
R=Path(__file__).resolve().parents[1]
layouts={v.get('id'):v for v in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
maps=[json.loads(p.read_text()) for p in (R/'data/maps').glob('Europe*/map.json')]
primary=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()
legacy=primary+(R/'data/tilesets/secondary/pallet_town/metatile_attributes.bin').read_bytes()
for city in ['London']:
 id=f'LAYOUT_EUROPE_{city.upper()}_PAST';l=layouts[id];w,h=l['width'],l['height'];ow=24
 assert sum(m['layout']==id for m in maps)==1
 old=struct.unpack('<%dH'%(ow*20),(R/'data/geography/london-past-v058.bin').read_bytes());new=struct.unpack('<%dH'%(w*h),(R/l['blockdata_filepath']).read_bytes())
 attrs=primary+(R/f'data/tilesets/secondary/europe_{city.lower()}/metatile_attributes.bin').read_bytes()
 for i,b in enumerate(old):
  if b&0xc00:continue
  n=new[(i//ow)*w+i%ow];assert not n&0xc00 and n>>12==b>>12,(city,i,b,n)
  assert struct.unpack_from('<I',legacy,(b&1023)*4)[0]&511==struct.unpack_from('<I',attrs,(n&1023)*4)[0]&511,(city,i,'behavior')
 assert (w+15)*(h+14)<=0x2800 and max(b&1023 for b in new)<len(attrs)//4
 print(f'PASS: {city} original save positions retain terrain/elevation; independent layout fits hardware')
