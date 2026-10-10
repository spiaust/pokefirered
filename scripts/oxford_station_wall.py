"""Append warm stone station walls using existing tiles and palettes."""
from pathlib import Path
import json,struct
from PIL import Image
r=Path(__file__).resolve().parents[1]
def build():
 d=r/'data/tilesets/secondary/europe_oxford';f=r/'data/geography/oxford-landmark-blocks.json';b=json.loads(f.read_text());n=b['gym_sign']+1-640
 m=bytearray((d/'metatiles.bin').read_bytes()[:n*16]);a=bytearray((d/'metatile_attributes.bin').read_bytes()[:n*4]);ids={}
 tiles=Image.open(d/'tiles.png');primary=Image.open(r/'data/tilesets/primary/general/tiles.png');copies={}
 count=max(v&1023 for v in struct.unpack('<%dH'%(len(m)//2),m) if v&1023>=640)-640+1
 remap=list(range(16));remap[2:5]=[8,8,9]
 for old in [0x2c0,0x2c1,0x2d0,0x2c2,0x2c3,0x2c4,0x2c5,0x2c8,0x2c9,0x2d8,0x2cb,0x2cc,0x2cd]:
  v=list(struct.unpack_from('<8H',m,(old-640)*16))
  for i,x in enumerate(v):
   if x>>12!=9:continue
   tile=x&1023
   if tile not in copies:
    source=tiles if tile>=640 else primary;index=tile-640 if tile>=640 else tile
    q=source.crop((index%16*8,index//16*8,index%16*8+8,index//16*8+8));q.putdata([remap[c] for c in q.getdata()]);assert count<384
    tiles.paste(q,(count%16*8,count//16*8));copies[tile]=640+count;count+=1
   v[i]=0x3000|(x&0xc00)|copies[tile]
  ids[str(old)]=640+len(a)//4;m+=struct.pack('<8H',*v);a+=a[(old-640)*4:(old-639)*4]
 b.update(station_wall=ids,station_wall_tiles=copies,station_wall_remap=remap);tiles.save(d/'tiles.png');(d/'metatiles.bin').write_bytes(m);(d/'metatile_attributes.bin').write_bytes(a);f.write_text(json.dumps(b,indent=2)+'\n')
 print('Oxford station stone walls:',count,'tiles')
if __name__=='__main__':build()
