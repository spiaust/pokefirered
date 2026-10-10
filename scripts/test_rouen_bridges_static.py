"""RouenPast pier rails preserve terminal, walkability, prior art and events."""
from pathlib import Path
from PIL import Image
import json,struct
from rouen_bridges import build
r=Path(__file__).resolve().parents[1];b=r/'.local-tools/rouen-bridges-before-v206';prefix='data/tilesets/secondary/europe_rouen/'
old=struct.unpack('<2880H',(b/'data/layouts/EuropeRouenPast/map.bin').read_bytes());new=struct.unpack('<2880H',(r/'data/layouts/EuropeRouenPast/map.bin').read_bytes());blocks=json.loads((r/'data/geography/rouen-landmark-blocks.json').read_text());changed=set()
attrs=(r/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(r/(prefix+'metatile_attributes.bin')).read_bytes()
for left in (43,71):
 for x,t in zip((left,left+2),blocks['bridge_rails']):
  for y in range(25,28):
   i=y*80+x;assert new[i]==(old[i]&0xfc00)|t;changed.add(i)
for i,(a,c) in enumerate(zip(old,new)):
 assert a&0xfc00==c&0xfc00
 assert attrs[(a&1023)*4:(a&1023)*4+4]==attrs[(c&1023)*4:(c&1023)*4+4]
 if i not in changed:assert a==c
assert len(changed)==12
for name in ['data/maps/EuropeRouenPast/map.json','data/maps/EuropeRouenPast/scripts.inc','data/maps/map_groups.json','data/layouts/layouts.json','data/layouts/EuropeAmiensPast/map.bin']:assert (r/name).read_bytes()==(b/name).read_bytes()
for f in (b/(prefix+'palettes')).glob('*.pal'):assert f.read_bytes()==(r/(prefix+'palettes')/f.name).read_bytes()
print('PASS: exactly twelve bridge-edge cells change; all collision/elevation/behavior, original hub, three lanes, events, palettes and Amiens remain intact')
for name in ['metatiles.bin','metatile_attributes.bin']:
 a=(b/(prefix+name)).read_bytes();assert (r/(prefix+name)).read_bytes()[:len(a)]==a
meta=(b/(prefix+'metatiles.bin')).read_bytes();n=max(v&1023 for v in struct.unpack('<%dH'%(len(meta)//2),meta) if v&1023>=640)-640+1
a=Image.open(b/(prefix+'tiles.png'));c=Image.open(r/(prefix+'tiles.png'))
for tile in range(n):
 box=(tile%16*8,tile//16*8,tile%16*8+8,tile//16*8+8);assert a.crop(box).tobytes()==c.crop(box).tobytes()
prior=json.loads((b/'data/geography/rouen-landmark-blocks.json').read_text())
for k,v in prior.items():assert blocks[k]==v
assert n+8<=384
paths=[r/(prefix+name) for name in ['metatiles.bin','metatile_attributes.bin','tiles.png']]+[r/'data/geography/rouen-landmark-blocks.json']
before=[p.read_bytes() for p in paths];build();assert [p.read_bytes() for p in paths]==before
print('PASS: bridge rails append eight tiles/two metatiles within hardware limits; prior art/mappings remain exact and generation is deterministic')
