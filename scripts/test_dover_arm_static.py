"""Dover pier rails preserve terminal, walkability, prior art and events."""
from pathlib import Path
from PIL import Image
import json,struct
from dover_arm import build
r=Path(__file__).resolve().parents[1];b=r/'.local-tools/dover-arm-before-v204';prefix='data/tilesets/secondary/europe_doverport/'
old=struct.unpack('<2240H',(b/'data/layouts/EuropeDoverPort/map.bin').read_bytes());new=struct.unpack('<2240H',(r/'data/layouts/EuropeDoverPort/map.bin').read_bytes());blocks=json.loads((r/'data/geography/doverport-landmark-blocks.json').read_text());changed=set()
attrs=(r/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(r/(prefix+'metatile_attributes.bin')).read_bytes()
for y,t in zip((31,33),blocks['arm_rails']):
 for x in range(27,39):
  i=y*56+x;assert new[i]==(old[i]&0xfc00)|t;changed.add(i)
for i,(a,c) in enumerate(zip(old,new)):
 assert a&0xfc00==c&0xfc00
 assert attrs[(a&1023)*4:(a&1023)*4+4]==attrs[(c&1023)*4:(c&1023)*4+4]
 if i not in changed:assert a==c
assert len(changed)==24
for name in ['data/maps/EuropeDoverPort/map.json','data/maps/EuropeDoverPort/scripts.inc','data/maps/map_groups.json','data/layouts/layouts.json','data/layouts/EuropeCalaisPort/map.bin']:assert (r/name).read_bytes()==(b/name).read_bytes()
for f in (b/(prefix+'palettes')).glob('*.pal'):assert f.read_bytes()==(r/(prefix+'palettes')/f.name).read_bytes()
print('PASS: exactly twenty-four harbor-edge cells change; all collision/elevation/behavior, terminal, three lanes, events, palettes and Calais remain intact')
for name in ['metatiles.bin','metatile_attributes.bin']:
 a=(b/(prefix+name)).read_bytes();assert (r/(prefix+name)).read_bytes()[:len(a)]==a
meta=(b/(prefix+'metatiles.bin')).read_bytes();n=max(v&1023 for v in struct.unpack('<%dH'%(len(meta)//2),meta) if v&1023>=640)-640+1
a=Image.open(b/(prefix+'tiles.png'));c=Image.open(r/(prefix+'tiles.png'))
for tile in range(n):
 box=(tile%16*8,tile//16*8,tile%16*8+8,tile//16*8+8);assert a.crop(box).tobytes()==c.crop(box).tobytes()
prior=json.loads((b/'data/geography/doverport-landmark-blocks.json').read_text())
for k,v in prior.items():assert blocks[k]==v
assert n+1<=384
paths=[r/(prefix+name) for name in ['metatiles.bin','metatile_attributes.bin','tiles.png']]+[r/'data/geography/doverport-landmark-blocks.json']
before=[p.read_bytes() for p in paths];build();assert [p.read_bytes() for p in paths]==before
print('PASS: arm rails append one mirrored tile/two metatiles within hardware limits; prior art/mappings remain exact and generation is deterministic')
