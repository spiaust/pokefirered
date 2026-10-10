"""Append native stone parapet overlays without altering earlier Amiens art."""
from pathlib import Path
import json,struct
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[1]
def build():
 dest=r/'data/tilesets/secondary/europe_amiens';f=r/'data/geography/amiens-landmark-blocks.json';blocks=json.loads(f.read_text())
 count=max(v for name in ['cathedral','houses'] for row in blocks[name] for v in row)+1-640
 meta=bytearray((dest/'metatiles.bin').read_bytes()[:count*16]);attrs=bytearray((dest/'metatile_attributes.bin').read_bytes()[:count*4])
 entries=struct.unpack('<%dH'%(len(meta)//2),meta);n=max(v&1023 for v in entries if v&1023>=640)-640+1
 tiles=Image.open(dest/'tiles.png');general=(r/'data/tilesets/primary/general/metatiles.bin').read_bytes();deck=struct.unpack_from('<4H',general,0x165*16)
 behavior=(r/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()[0x165*4:0x166*4];ids=[]
 for direction in range(4):
  east=bool(direction%2)
  tile=Image.new('P',(16,16),0);draw=ImageDraw.Draw(tile);x=12 if east else 1
  draw.rectangle((x,0,x+2,15),fill=4);draw.line((x,0,x,15),fill=1)
  for y in [0,8]:
   draw.rectangle((10 if east else 0,y,15 if east else 5,y+1),fill=4)
   draw.point((10 if east else 0,y),fill=7)
  if direction>=2:tile=tile.transpose(Image.Transpose.TRANSPOSE)
  overlay=[]
  for dy,dx in [(0,0),(0,8),(8,0),(8,8)]:
   assert n<384;tiles.paste(tile.crop((dx,dy,dx+8,dy+8)),((n%16)*8,(n//16)*8));overlay.append(0x3000|640+n);n+=1
  ids.append(640+len(attrs)//4);meta+=struct.pack('<8H',*deck,*overlay);attrs+=behavior
 blocks['bridge_rails']=ids;tiles.save(dest/'tiles.png');(dest/'metatiles.bin').write_bytes(meta);(dest/'metatile_attributes.bin').write_bytes(attrs);f.write_text(json.dumps(blocks,indent=2)+'\n')
 print('Amiens bridge rails:',n,'secondary tiles')
if __name__=='__main__':build()
