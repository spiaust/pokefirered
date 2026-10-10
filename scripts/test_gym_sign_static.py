from pathlib import Path
import json,struct
from PIL import Image
r=Path(__file__).resolve().parents[1];b=r/'.local-tools/gym-sign-before-v201'
for city in ['Oxford','Chantilly','Oranienburg']:
 prefix=f'data/tilesets/secondary/europe_{city.lower()}/';path=f'data/layouts/Europe{city}/map.bin';w=72 if city=='Chantilly' else 64
 old=struct.unpack('<%dH'%(w*24),(b/path).read_bytes());new=struct.unpack('<%dH'%(w*24),(r/path).read_bytes());blocks=json.loads((r/f'data/geography/{city.lower()}-landmark-blocks.json').read_text())
 assert [i for i,(a,c) in enumerate(zip(old,new)) if a!=c]==[11*w+14]
 assert new[11*w+14]==(old[11*w+14]&0xfc00)|blocks['gym_sign']
 attrs=(r/(prefix+'metatile_attributes.bin')).read_bytes();native=(r/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()[8:12]
 assert attrs[(blocks['gym_sign']-640)*4:(blocks['gym_sign']-639)*4]==native
 for name in ['metatiles.bin','metatile_attributes.bin']:
  a=(b/(prefix+name)).read_bytes();assert (r/(prefix+name)).read_bytes()[:len(a)]==a
 meta=(b/(prefix+'metatiles.bin')).read_bytes();n=max(v&1023 for v in struct.unpack('<%dH'%(len(meta)//2),meta) if v&1023>=640)-640+1
 a=Image.open(b/(prefix+'tiles.png'));c=Image.open(r/(prefix+'tiles.png'))
 for tile in range(n):
  box=(tile%16*8,tile//16*8,tile%16*8+8,tile//16*8+8);assert a.crop(box).tobytes()==c.crop(box).tobytes()
 for f in (b/(prefix+'palettes')).glob('*.pal'):assert f.read_bytes()==(r/(prefix+'palettes')/f.name).read_bytes()
 for name in ['map.json','scripts.inc']:assert (b/f'data/maps/Europe{city}/{name}').read_bytes()==(r/f'data/maps/Europe{city}/{name}').read_bytes()
 assert n+4<=384
 print(f'PASS: {city} one sign cell changes; collision/behavior/events/palettes and prior artwork remain exact')
