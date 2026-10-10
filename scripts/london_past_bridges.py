"""Reuse modern rail artwork over unchanged historical London paving."""
from pathlib import Path
import json,struct
r=Path(__file__).resolve().parents[1]
def build():
 d=r/'data/tilesets/secondary/europe_london';f=r/'data/geography/london-landmark-blocks.json';blocks=json.loads(f.read_text());count=max(blocks['western_wall'].values())+1-640
 meta=bytearray((d/'metatiles.bin').read_bytes()[:count*16]);attrs=bytearray((d/'metatile_attributes.bin').read_bytes()[:count*4]);primary=r/'data/tilesets/primary/general'
 deck=struct.unpack_from('<4H',(primary/'metatiles.bin').read_bytes(),0x165*16);behavior=(primary/'metatile_attributes.bin').read_bytes()[0x165*4:0x166*4];ids={}
 for name,source in blocks['bridges'].items():
  ids[name]=[]
  for old in source:
   overlay=struct.unpack_from('<4H',meta,(old-640)*16+8);ids[name].append(640+len(attrs)//4);meta+=struct.pack('<8H',*deck,*overlay);attrs+=behavior
 blocks['past_bridges']=ids;(d/'metatiles.bin').write_bytes(meta);(d/'metatile_attributes.bin').write_bytes(attrs);f.write_text(json.dumps(blocks,indent=2)+'\n')
 print('London past bridges: four metatiles; existing rail tiles and palettes retained')
if __name__=='__main__':build()
