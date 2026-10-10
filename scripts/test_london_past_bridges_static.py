from pathlib import Path
import json,struct
from london_past_bridges import build
r=Path(__file__).resolve().parents[1];b=r/'.local-tools/london-past-bridges-before-v205';old=struct.unpack('<3200H',(b/'data/layouts/EuropeLondonPast/map.bin').read_bytes());new=struct.unpack('<3200H',(r/'data/layouts/EuropeLondonPast/map.bin').read_bytes());blocks=json.loads((r/'data/geography/london-landmark-blocks.json').read_text());changed=set()
d=r/'data/tilesets/secondary/europe_london';attrs=(r/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(d/'metatile_attributes.bin').read_bytes()
for name,x,y in [('westminster',52,15),('lambeth',54,32)]:
 for dy,t in enumerate(blocks['past_bridges'][name]):
  for dx in range(6):
   i=(y+dy)*80+x+dx;assert new[i]==(old[i]&0xfc00)|t;changed.add(i)
assert len(changed)==24
for i,(a,c) in enumerate(zip(old,new)):
 assert a&0xfc00==c&0xfc00 and attrs[(a&1023)*4:(a&1023)*4+4]==attrs[(c&1023)*4:(c&1023)*4+4]
 if i not in changed:assert a==c
for name in ['data/layouts/EuropeLondon/map.bin','data/maps/EuropeLondonPast/map.json','data/maps/EuropeLondonPast/scripts.inc','data/layouts/layouts.json']:assert (r/name).read_bytes()==(b/name).read_bytes()
print('PASS: exactly twenty-four historical bridge cells change; collision/terrain/hub/events and modern London remain intact')
for name in ['metatiles.bin','metatile_attributes.bin']:
 a=(b/f'data/tilesets/secondary/europe_london/{name}').read_bytes();assert (d/name).read_bytes()[:len(a)]==a
for name in ['tiles.png',*[str(p.relative_to(d)) for p in (d/'palettes').glob('*.pal')]]:assert (d/name).read_bytes()==(b/f'data/tilesets/secondary/europe_london/{name}').read_bytes()
prior=json.loads((b/'data/geography/london-landmark-blocks.json').read_text())
for k,v in prior.items():assert blocks[k]==v
paths=[d/'metatiles.bin',d/'metatile_attributes.bin',r/'data/geography/london-landmark-blocks.json'];before=[p.read_bytes() for p in paths];build();assert [p.read_bytes() for p in paths]==before
print('PASS: four historical metatiles append using identical existing tiles/palettes/mappings; helper generation is deterministic')
