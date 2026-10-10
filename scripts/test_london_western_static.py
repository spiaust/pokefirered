"""Exact footprint, append-only artwork and event compatibility for London."""
from pathlib import Path
import json,struct
from PIL import Image
r=Path(__file__).resolve().parents[1];b=r/'data/geography/london-facade-v171'
old=struct.unpack('<2816H',(b/'data/layouts/EuropeLondon/map.bin').read_bytes());new=struct.unpack('<2816H',(r/'data/layouts/EuropeLondon/map.bin').read_bytes())
blocks=json.loads((r/'data/geography/london-landmark-blocks.json').read_text());mapping=blocks['western_wall'];changed=[]
for i,(a,c) in enumerate(zip(old,new)):
 x,y=i%64,i//64;expected=a
 if 44<=x<49 and 31<=y<33 and str(a&1023) in mapping:expected=(a&0xfc00)|mapping[str(a&1023)]
 assert c==expected,(x,y,a,c)
 if a!=c:changed.append((x,y));assert a&0xfc00==c&0xfc00
assert len(changed)==9 and (45,32) not in changed
for name in ['data/maps/EuropeLondon/map.json','data/maps/EuropeLondon/scripts.inc','data/maps/map_groups.json','data/layouts/layouts.json']:
 assert (r/name).read_bytes()==(b/name).read_bytes(),name
print('PASS: exactly nine western wall cells change; doorway, all paths, events, scripts and map/layout IDs remain exact')
prefix='data/tilesets/secondary/europe_london/'
for name in ['metatiles.bin','metatile_attributes.bin']:
 a=(b/(prefix+name)).read_bytes();c=(r/(prefix+name)).read_bytes();assert c[:len(a)]==a
meta=(r/(prefix+'metatiles.bin')).read_bytes();attrs=(r/(prefix+'metatile_attributes.bin')).read_bytes()
for source,target in mapping.items():
 source=int(source);assert attrs[(source-640)*4:(source-639)*4]==attrs[(target-640)*4:(target-639)*4]
 a=struct.unpack_from('<8H',meta,(source-640)*16);c=struct.unpack_from('<8H',meta,(target-640)*16)
 assert c==tuple(0x8000|(v&0xc00)|blocks['wall_tiles'][str(v&1023)] if v>>12==3 else v for v in a)
prior=json.loads((b/'data/geography/london-landmark-blocks.json').read_text())
for key,value in prior.items():assert blocks[key]==value
oldtiles=Image.open(b/(prefix+'tiles.png'));tiles=Image.open(r/(prefix+'tiles.png'))
oldcount=max(prior['roof_tiles'].values())-640+1
for n in range(oldcount):
 box=((n%16)*8,(n//16)*8,(n%16)*8+8,(n//16)*8+8)
 assert oldtiles.crop(box).tobytes()==tiles.crop(box).tobytes(),n
for slot in range(16):
 assert (r/(prefix+f'palettes/{slot:02}.pal')).read_bytes()==(r/f'data/tilesets/secondary/pallet_town/palettes/{slot:02}.pal').read_bytes() or slot==7
assert max(blocks['wall_tiles'].values())-640<384 and blocks['wall_remap'][0]==0
print('PASS: native wall variants append within hardware capacity; earlier art, mappings, palettes, attributes, flips and transparency remain intact')
