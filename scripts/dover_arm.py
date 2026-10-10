"""Append one mirrored rail tile for Dover's three-row harbor arm."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,struct
r=Path(__file__).resolve().parents[1]
def build():
 d=r/'data/tilesets/secondary/europe_doverport';f=r/'data/geography/doverport-landmark-blocks.json';blocks=json.loads(f.read_text())
 count=max(v for key in ['castle','cliffs'] for row in blocks[key] for v in row)+1-640
 meta=bytearray((d/'metatiles.bin').read_bytes()[:count*16]);attrs=bytearray((d/'metatile_attributes.bin').read_bytes()[:count*4]);entries=struct.unpack('<%dH'%(len(meta)//2),meta)
 n=max(v&1023 for v in entries if v&1023>=640)-640+1;assert n<384;tiles=Image.open(d/'tiles.png')
 assert not any(tiles.crop((0,0,8,8)).tobytes())
 rail=Image.new('P',(8,8),0);draw=ImageDraw.Draw(rail);draw.rectangle((0,1,7,3),fill=4);draw.line((0,1,7,1),fill=1);draw.rectangle((0,0,1,5),fill=4);draw.point((0,0),fill=7)
 tiles.paste(rail,(n%16*8,n//16*8));blank=0x3000|640;top=0x3000|640+n;bottom=top|0x800
 general=(r/'data/tilesets/primary/general/metatiles.bin').read_bytes();deck=struct.unpack_from('<4H',general,0x165*16)
 behavior=(r/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()[0x165*4:0x166*4];ids=[]
 for overlay in [(top,top,blank,blank),(blank,blank,bottom,bottom)]:
  ids.append(640+len(attrs)//4);meta+=struct.pack('<8H',*deck,*overlay);attrs+=behavior
 blocks['arm_rails']=ids;tiles.save(d/'tiles.png');(d/'metatiles.bin').write_bytes(meta);(d/'metatile_attributes.bin').write_bytes(attrs);f.write_text(json.dumps(blocks,indent=2)+'\n')
 print('Dover harbor arm rails:',n+1,'secondary tiles')
if __name__=='__main__':build()
