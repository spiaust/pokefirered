"""Calais pier rails preserve terminal, walkability, prior art and events."""
from pathlib import Path
from PIL import Image
import json,struct
from calais_pier import build
r=Path(__file__).resolve().parents[1];b=r/'.local-tools/calais-pier-before-v203';prefix='data/tilesets/secondary/europe_calaisport/'
old=struct.unpack('<2240H',(b/'data/layouts/EuropeCalaisPort/map.bin').read_bytes());new=struct.unpack('<2240H',(r/'data/layouts/EuropeCalaisPort/map.bin').read_bytes());blocks=json.loads((r/'data/geography/calaisport-landmark-blocks.json').read_text());changed=set()
attrs=(r/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(r/(prefix+'metatile_attributes.bin')).read_bytes()
for x,t in zip((50,52),blocks['pier_rails']):
 for y in range(5,11):
  i=y*56+x;assert new[i]==(old[i]&0xfc00)|t;changed.add(i)
for i,(a,c) in enumerate(zip(old,new)):
 assert a&0xfc00==c&0xfc00
 assert attrs[(a&1023)*4:(a&1023)*4+4]==attrs[(c&1023)*4:(c&1023)*4+4]
 if i not in changed:assert a==c
assert len(changed)==12
for name in ['data/maps/EuropeCalaisPort/map.json','data/maps/EuropeCalaisPort/scripts.inc','data/maps/map_groups.json','data/layouts/layouts.json','data/layouts/EuropeDoverPort/map.bin']:assert (r/name).read_bytes()==(b/name).read_bytes()
for f in (b/(prefix+'palettes')).glob('*.pal'):assert f.read_bytes()==(r/(prefix+'palettes')/f.name).read_bytes()
print('PASS: exactly twelve pier-edge cells change; all collision/elevation/behavior, terminal, three lanes, events, palettes and Dover remain intact')
for name in ['metatiles.bin','metatile_attributes.bin']:
 a=(b/(prefix+name)).read_bytes();assert (r/(prefix+name)).read_bytes()[:len(a)]==a
meta=(b/(prefix+'metatiles.bin')).read_bytes();n=max(v&1023 for v in struct.unpack('<%dH'%(len(meta)//2),meta) if v&1023>=640)-640+1
a=Image.open(b/(prefix+'tiles.png'));c=Image.open(r/(prefix+'tiles.png'))
for tile in range(n):
 box=(tile%16*8,tile//16*8,tile%16*8+8,tile//16*8+8);assert a.crop(box).tobytes()==c.crop(box).tobytes()
prior=json.loads((b/'data/geography/calaisport-landmark-blocks.json').read_text())
for k,v in prior.items():assert blocks[k]==v
assert n+8<=384
paths=[r/(prefix+name) for name in ['metatiles.bin','metatile_attributes.bin','tiles.png']]+[r/'data/geography/calaisport-landmark-blocks.json']
before=[p.read_bytes() for p in paths];build();assert [p.read_bytes() for p in paths]==before
print('PASS: pier rails append eight tiles/two metatiles within hardware limits; prior art/mappings remain exact and generation is deterministic')
