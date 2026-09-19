"""Preserve the full old terminal and prove the new coastal paths are connected."""
from pathlib import Path
import json,struct,sys
from collections import deque
R=Path(__file__).resolve().parents[1]
old=struct.unpack('<221H',(R/'data/layouts/Island_Harbor/map.bin').read_bytes())
layouts={v.get('id'):v for v in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
for city in sys.argv[1:] or ['Dover','Calais']:
 l=layouts[f'LAYOUT_EUROPE_{city.upper()}_PORT'];w,h=l['width'],l['height']
 blocks=struct.unpack('<%dH'%(w*h),(R/l['blockdata_filepath']).read_bytes())
 assert tuple(blocks[y*w+x] for y in range(13) for x in range(17))==old
 assert (w+15)*(h+14)<=0x2800
 base=R/f'data/tilesets/secondary/europe_{city.lower()}port'
 legacy=R/'data/tilesets/secondary/island_harbor'
 for f in ['metatiles.bin','metatile_attributes.bin']:
  assert (base/f).read_bytes().startswith((legacy/f).read_bytes())
 for p in (legacy/'palettes').glob('*.pal'):
  if p.name!='07.pal':assert (base/'palettes'/p.name).read_bytes()==p.read_bytes()
 attrs=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(base/'metatile_attributes.bin').read_bytes()
 assert max(t&1023 for t in blocks)<len(attrs)//4
 m=struct.unpack('<%dH'%((base/'metatiles.bin').stat().st_size//2),(base/'metatiles.bin').read_bytes())
 assert max(t&1023 for t in m)<1024 and max(t>>12 for t in m)<13
 def valid(x,y):
  if not (0<=x<w and 0<=y<h):return False
  b=blocks[y*w+x];return not b&0xc00 and b>>12!=1 and struct.unpack_from('<I',attrs,(b&1023)*4)[0]&511 not in (0x10,0x11,0x12,0x13,0x15,0x19,0x1a,0x1b)
 seen={(8,5)};q=deque(seen)
 while q:
  x,y=q.popleft()
  for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if p not in seen and valid(*p):seen.add(p);q.append(p)
 points=[(45,9),(48,13),(53,17),(35,23),(35,32)] if city=='Dover' else [(37,30),(45,16),(35,10),(51,7),(27,27)]
 assert all(p in seen for p in points),(city,[p for p in points if p not in seen])
 assert (8,2) in seen
 print(f'PASS: {city}: complete old terminal preserved, landmark paths connected, hardware limits respected')
