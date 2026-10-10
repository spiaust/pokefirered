"""Append native stone parapet overlays without altering earlier Oranienburg art."""
from pathlib import Path
import json,struct
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[1]
def build():
 dest=r/'data/tilesets/secondary/europe_oranienburg';f=r/'data/geography/oranienburg-landmark-blocks.json';blocks=json.loads(f.read_text())
 count=max(v for name in ['palace'] for row in blocks[name] for v in row)+1-640
 meta=bytearray((dest/'metatiles.bin').read_bytes()[:count*16]);attrs=bytearray((dest/'metatile_attributes.bin').read_bytes()[:count*4])
 entries=struct.unpack('<%dH'%(len(meta)//2),meta);n=max(v&1023 for v in entries if v&1023>=640)-640+1
 tiles=Image.open(dest/'tiles.png');general=(r/'data/tilesets/primary/general/metatiles.bin').read_bytes();deck=struct.unpack_from('<4H',general,0x165*16)
 behavior=(r/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()[0x165*4:0x166*4];ids=[]
 for south in [False,True]:
  tile=Image.new('P',(16,16),0);draw=ImageDraw.Draw(tile);y=12 if south else 1
  draw.rectangle((0,y,15,y+2),fill=4);draw.line((0,y,15,y),fill=1)
  for x in [0,8]:
   draw.rectangle((x,10 if south else 0,x+1,15 if south else 5),fill=4);draw.point((x,10 if south else 0),fill=7)
  overlay=[]
  for dy,dx in [(0,0),(0,8),(8,0),(8,8)]:
   assert n<384;tiles.paste(tile.crop((dx,dy,dx+8,dy+8)),((n%16)*8,(n//16)*8));overlay.append(0x3000|640+n);n+=1
  ids.append(640+len(attrs)//4);meta+=struct.pack('<8H',*deck,*overlay);attrs+=behavior
 blocks['bridge_rails']=ids;tiles.save(dest/'tiles.png');(dest/'metatiles.bin').write_bytes(meta);(dest/'metatile_attributes.bin').write_bytes(attrs);f.write_text(json.dumps(blocks,indent=2)+'\n')
 print('Oranienburg bridge rails:',n,'secondary tiles')
if __name__=='__main__':build()
