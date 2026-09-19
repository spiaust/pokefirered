"""Save-position safety and hardware limits for the expanded capital maps."""
import json,struct
from pathlib import Path
R=Path(__file__).resolve().parents[1]
layouts={l.get('id'):l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
primary=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()
legacy_attrs=primary+(R/'data/tilesets/secondary/pallet_town/metatile_attributes.bin').read_bytes()
def water(block,attrs):return struct.unpack_from('<I',attrs,(block&1023)*4)[0]&511 in (0x10,0x11,0x12,0x13,0x15,0x19,0x1a,0x1b)
for city in ('London','Paris','Berlin'):
 layout=layouts[f'LAYOUT_EUROPE_{city.upper()}'];w,h=layout['width'],layout['height'];new=struct.unpack('<%dH'%(w*h),(R/layout['blockdata_filepath']).read_bytes());old=struct.unpack('<768H',(R/f'data/geography/{city.lower()}-v050.bin').read_bytes());base=R/f'data/tilesets/secondary/europe_{city.lower()}';attrs=primary+(base/'metatile_attributes.bin').read_bytes()
 for i,b in enumerate(old):
  n=new[(i//32)*w+i%32]
  if not b&0xc00:
   assert not n&0xc00,(city,i,'old traversable position obstructed')
   assert water(b,legacy_attrs)==water(n,attrs),(city,i,'old land/water changed')
   assert b>>12==n>>12,(city,i,'old elevation changed')
 meta=struct.unpack('<%dH'%((base/'metatiles.bin').stat().st_size//2),(base/'metatiles.bin').read_bytes())
 assert max(t&1023 for t in meta)<1024 and max(t>>12 for t in meta)<13
 assert max(t&1023 for t in new)<len(attrs)//4
 print(f'PASS: {city}: all old traversable coordinates keep land/water and elevation; tileset fits hardware limits')
