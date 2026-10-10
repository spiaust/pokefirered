from pathlib import Path
import json,struct
from PIL import Image
from chantilly_station_wall import build
r=Path(__file__).resolve().parents[1];b=r/'.local-tools/chantilly-station-before-v213';prefix='data/tilesets/secondary/europe_chantilly/';ids=json.loads((r/'data/geography/chantilly-landmark-blocks.json').read_text())['station_wall']
old=struct.unpack('<1728H',(b/'data/layouts/EuropeChantilly/map.bin').read_bytes());new=struct.unpack('<1728H',(r/'data/layouts/EuropeChantilly/map.bin').read_bytes());cells=set()
for y in (8,9):
 for x in range(20,27):
  i=y*72+x;t=ids.get(str(old[i]&1023))
  if t is not None:assert new[i]==(old[i]&0xfc00)|t;cells.add(i)
assert len(cells)==13 and old[9*72+23]==new[9*72+23]
for i,(a,c) in enumerate(zip(old,new)):
 assert a&0xfc00==c&0xfc00
 if i not in cells:assert a==c
for f in b.rglob('*'):
 if not f.is_file() or str(f.relative_to(b)).replace('\\','/') in ['data/layouts/EuropeChantilly/map.bin','data/geography/chantilly-landmark-blocks.json',prefix+'metatiles.bin',prefix+'metatile_attributes.bin',prefix+'tiles.png']:continue
 assert f.read_bytes()==(r/f.relative_to(b)).read_bytes(),f
print('PASS: exactly thirteen station wall cells change; door/roof/sign/collision/events/palettes and other regional towns remain intact')
for name in ['metatiles.bin','metatile_attributes.bin']:
 a=(b/(prefix+name)).read_bytes();assert (r/(prefix+name)).read_bytes()[:len(a)]==a
m=(r/(prefix+'metatiles.bin')).read_bytes();a=(r/(prefix+'metatile_attributes.bin')).read_bytes()
blocks=json.loads((r/'data/geography/chantilly-landmark-blocks.json').read_text());copies=blocks['station_wall_tiles'];remap=blocks['station_wall_remap']
for old,t in ids.items():
 old=int(old);v=struct.unpack_from('<8H',m,(old-640)*16);assert struct.unpack_from('<8H',m,(t-640)*16)==tuple(0x3000|(x&0xc00)|copies[str(x&1023)] if x>>12==9 else x for x in v)
 assert a[(old-640)*4:(old-639)*4]==a[(t-640)*4:(t-639)*4]
assert len(a)//4<=384
beforetiles=Image.open(b/(prefix+'tiles.png'));aftertiles=Image.open(r/(prefix+'tiles.png'));prior=(b/(prefix+'metatiles.bin')).read_bytes();count=max(v&1023 for v in struct.unpack('<%dH'%(len(prior)//2),prior) if v&1023>=640)-640+1
box=lambda n:(n%16*8,n//16*8,n%16*8+8,n//16*8+8)
for n in range(count):assert beforetiles.crop(box(n)).tobytes()==aftertiles.crop(box(n)).tobytes()
for source,t in copies.items():assert list(aftertiles.crop(box(t-640)).getdata())==[remap[c] for c in beforetiles.crop(box(int(source)-640)).getdata()]
assert count+len(copies)<=384
paths=[r/(prefix+n) for n in ['metatiles.bin','metatile_attributes.bin','tiles.png']]+[r/'data/geography/chantilly-landmark-blocks.json'];before=[p.read_bytes() for p in paths];build();assert before==[p.read_bytes() for p in paths]
print('PASS: thirteen metatiles preserve behavior; original tiles remain exact, appended warm wall colors fit hardware limits and regenerate deterministically')
