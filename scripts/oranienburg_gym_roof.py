"""Append gold native roof variants after Oranienburg's existing bridge artwork."""
from pathlib import Path
import json,struct
from PIL import Image
r=Path(__file__).resolve().parents[1]
def build():
 dest=r/'data/tilesets/secondary/europe_oranienburg';f=r/'data/geography/oranienburg-landmark-blocks.json';blocks=json.loads(f.read_text())
 count=max(blocks['bridge_rails'])+1-640
 meta=bytearray((dest/'metatiles.bin').read_bytes()[:count*16]);attrs=bytearray((dest/'metatile_attributes.bin').read_bytes()[:count*4])
 entries=struct.unpack('<%dH'%(len(meta)//2),meta);n=max(v&1023 for v in entries if v&1023>=640)-640+1
 tiles=Image.open(dest/'tiles.png');primary=Image.open(r/'data/tilesets/primary/general/tiles.png')
 source=[tuple(map(int,line.split())) for line in (dest/'palettes/09.pal').read_text().splitlines()[3:]]
 target=[tuple(map(int,line.split())) for line in (dest/'palettes/09.pal').read_text().splitlines()[3:]]
 remap=[0]+[min(range(1,16),key=lambda j:sum((source[i][c]-target[j][c])**2 for c in range(3))) for i in range(1,16)];remap[2:8]=[11,12,13,14,7,7]
 ids={};copies={}
 # The lab-shaped Gym roof occupies these two rows; leave walls/door alone.
 for old in [0x2b0,0x2b1,0x2b3,0x2b4,0x2b8,0x2b9,0x2bb,0x2bc]:
  values=list(struct.unpack_from('<8H',meta,(old-640)*16))
  for i,v in enumerate(values):
   if v>>12!=9:continue
   tileid=v&1023;assert tileid>=640
   if tileid not in copies:
    index=tileid-640;image=tiles.crop((index%16*8,index//16*8,index%16*8+8,index//16*8+8));image.putdata([remap[c] for c in image.getdata()])
    assert n<384;tiles.paste(image,(n%16*8,n//16*8));copies[tileid]=640+n;n+=1
   values[i]=0x9000|(v&0xc00)|copies[tileid]
  ids[str(old)]=640+len(attrs)//4;meta+=struct.pack('<8H',*values);attrs+=attrs[(old-640)*4:(old-640+1)*4]
 assert len(attrs)//4<=384
 blocks.update(gym_roof=ids,gym_roof_tiles=copies,gym_roof_remap=remap)
 tiles.save(dest/'tiles.png');(dest/'metatiles.bin').write_bytes(meta);(dest/'metatile_attributes.bin').write_bytes(attrs);f.write_text(json.dumps(blocks,indent=2)+'\n')
 print('Oranienburg Gym roof:',n,'secondary tiles')
if __name__=='__main__':build()
