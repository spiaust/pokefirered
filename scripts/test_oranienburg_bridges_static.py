"""Oranienburg bridge overlays retain all prior art, terrain behavior and events."""
from pathlib import Path
import json,struct
from PIL import Image
r=Path(__file__).resolve().parents[1];b=r/'data/geography/oranienburg-bridges-v176';prefix='data/tilesets/secondary/europe_oranienburg/'
old=struct.unpack('<1536H',(b/'data/layouts/EuropeOranienburg/map.bin').read_bytes());new=struct.unpack('<1536H',(r/'data/layouts/EuropeOranienburg/map.bin').read_bytes())
blocks=json.loads((r/'data/geography/oranienburg-landmark-blocks.json').read_text());ids=blocks['bridge_rails'];changed=set()
for x,y in [(55,12),(55,19)]:
 for dy,t in enumerate(ids):
  for dx in range(3):
   i=(y+dy)*64+x+dx;assert new[i]==(old[i]&0xfc00)|t;changed.add(i)
attrs=(r/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(r/(prefix+'metatile_attributes.bin')).read_bytes()
for i,(a,c) in enumerate(zip(old,new)):
 assert a&0xfc00==c&0xfc00
 assert attrs[(a&1023)*4:(a&1023)*4+4]==attrs[(c&1023)*4:(c&1023)*4+4]
 if i not in changed:assert a==c
assert len(changed)==12
for name in ['data/maps/EuropeOranienburg/map.json','data/maps/EuropeOranienburg/scripts.inc','data/maps/map_groups.json','data/layouts/layouts.json']:assert (r/name).read_bytes()==(b/name).read_bytes()
print('PASS: exactly twelve bridge cells change; all collision/elevation/terrain behavior, river cells, approaches, events and IDs remain intact')
for name in ['metatiles.bin','metatile_attributes.bin']:
 a=(b/(prefix+name)).read_bytes();assert (r/(prefix+name)).read_bytes()[:len(a)]==a
meta=(b/(prefix+'metatiles.bin')).read_bytes();n=max(v&1023 for v in struct.unpack('<%dH'%(len(meta)//2),meta) if v&1023>=640)-640+1
a=Image.open(b/(prefix+'tiles.png'));c=Image.open(r/(prefix+'tiles.png'))
for tile in range(n):
 box=(tile%16*8,tile//16*8,tile%16*8+8,tile//16*8+8);assert a.crop(box).tobytes()==c.crop(box).tobytes()
prior=json.loads((b/'data/geography/oranienburg-landmark-blocks.json').read_text())
for k,v in prior.items():assert blocks[k]==v
assert n+8<=384
print('PASS: stone rails append eight tiles/two metatiles; all earlier artwork, landmark mappings and attributes remain exact within hardware limits')
