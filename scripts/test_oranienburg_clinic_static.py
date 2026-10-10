from pathlib import Path
import struct,json,hashlib,subprocess,sys
from PIL import Image
r=Path(__file__).resolve().parents[1];b=r/'.local-tools/oranienburg-clinic-before-v197';prefix='data/tilesets/secondary/europe_oranienburg/'
old=struct.unpack('<1536H',(b/'data/layouts/EuropeOranienburg/map.bin').read_bytes());new=struct.unpack('<1536H',(r/'data/layouts/EuropeOranienburg/map.bin').read_bytes());blocks=json.loads((r/'data/geography/oranienburg-landmark-blocks.json').read_text())
attrs=(r/(prefix+'metatile_attributes.bin')).read_bytes()
changed={y*64+x for y in (8,9) for x in range(5,10) if not (x==6 and y==9)}
for i,(a,c) in enumerate(zip(old,new)):
 if i in changed:assert c==(a&0xfc00)|blocks['clinic_wall'][str(a&1023)]
 else:assert a==c
 assert a&0xfc00==c&0xfc00
 if i in changed:assert attrs[((a&1023)-640)*4:((a&1023)-640+1)*4]==attrs[((c&1023)-640)*4:((c&1023)-640+1)*4]
for name in ['data/maps/EuropeOranienburg/map.json','data/maps/EuropeOranienburg/scripts.inc','data/maps/map_groups.json','data/layouts/layouts.json']:assert (r/name).read_bytes()==(b/name).read_bytes()
for name in ['metatiles.bin','metatile_attributes.bin']:
 a=(b/(prefix+name)).read_bytes();assert (r/(prefix+name)).read_bytes()[:len(a)]==a
meta=(b/(prefix+'metatiles.bin')).read_bytes();n=max(v&1023 for v in struct.unpack('<%dH'%(len(meta)//2),meta) if v&1023>=640)-640+1
a=Image.open(b/(prefix+'tiles.png'));c=Image.open(r/(prefix+'tiles.png'))
for tile in range(n):
 box=(tile%16*8,tile//16*8,tile%16*8+8,tile//16*8+8);assert a.crop(box).tobytes()==c.crop(box).tobytes()
for f in (b/(prefix+'palettes')).glob('*.pal'):assert f.read_bytes()==(r/(prefix+'palettes')/f.name).read_bytes()
prior=json.loads((b/'data/geography/oranienburg-landmark-blocks.json').read_text())
assert all(blocks[k]==v for k,v in prior.items()) and n+len(blocks['clinic_wall_tiles'])<=384
print('PASS: only nine clinic wall cells change; prior artwork, palettes, collision, door, events and IDs remain exact')
files=[r/(prefix+x) for x in ['tiles.png','metatiles.bin','metatile_attributes.bin']]+[r/'data/geography/oranienburg-landmark-blocks.json',r/'data/layouts/EuropeOranienburg/map.bin']
before=[hashlib.sha256(f.read_bytes()).hexdigest() for f in files]
subprocess.run([sys.executable,str(r/'scripts/oranienburg_clinic_wall.py')],check=True);subprocess.run([sys.executable,str(r/'scripts/apply-oranienburg-clinic-wall.py')],check=True)
assert before==[hashlib.sha256(f.read_bytes()).hexdigest() for f in files]
print('PASS: appended wall artwork and map application regenerate identically within GBA limits')
