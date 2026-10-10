"""Append a native-palette red-cross clinic sign without changing its behavior."""
from pathlib import Path
import json,struct,sys
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[1]
def build(city):
 dest=r/f'data/tilesets/secondary/europe_{city.lower()}';f=r/f'data/geography/{city.lower()}-landmark-blocks.json';blocks=json.loads(f.read_text())
 count=max(blocks['clinic_wall'].values())+1-640
 meta=bytearray((dest/'metatiles.bin').read_bytes()[:count*16]);attrs=bytearray((dest/'metatile_attributes.bin').read_bytes()[:count*4])
 entries=struct.unpack('<%dH'%(len(meta)//2),meta);n=max(v&1023 for v in entries if v&1023>=640)-640+1
 tiles=Image.open(dest/'tiles.png');icon=Image.new('P',(16,16),0);draw=ImageDraw.Draw(icon)
 draw.rectangle((1,0,14,11),fill=7);draw.rectangle((2,1,13,10),fill=1)
 draw.rectangle((6,2,9,9),fill=14);draw.rectangle((3,4,12,7),fill=14)
 draw.rectangle((7,12,8,15),fill=7)
 overlay=[]
 for dy,dx in [(0,0),(0,8),(8,0),(8,8)]:
  assert n<384;tiles.paste(icon.crop((dx,dy,dx+8,dy+8)),(n%16*8,n//16*8));overlay.append(0x2000|640+n);n+=1
 native=(r/'data/tilesets/primary/general/metatiles.bin').read_bytes();base=struct.unpack_from('<4H',native,2*16)
 behavior=(r/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()[8:12]
 blocks['clinic_sign']=640+len(attrs)//4;meta+=struct.pack('<8H',*base,*overlay);attrs+=behavior
 tiles.save(dest/'tiles.png');(dest/'metatiles.bin').write_bytes(meta);(dest/'metatile_attributes.bin').write_bytes(attrs);f.write_text(json.dumps(blocks,indent=2)+'\n')
 path=r/f'data/layouts/Europe{city}/map.bin';w=72 if city=='Chantilly' else 64;a=list(struct.unpack('<%dH'%(w*24),path.read_bytes()));i=11*w+5;a[i]=(a[i]&0xfc00)|blocks['clinic_sign'];path.write_bytes(struct.pack('<%dH'%len(a),*a))
 print(city,'clinic sign:',n,'secondary tiles')
if __name__=='__main__':
 for city in sys.argv[1:] or ['Oxford','Chantilly','Oranienburg']:build(city)
