"""Native-tile roof variants: terracotta home, green library, slate workroom."""
from pathlib import Path
from PIL import Image
import json,struct
R=Path(__file__).resolve().parents[1]
def build():
 dest=R/'data/tilesets/secondary/europe_berlin'
 landmarks=json.loads((R/'data/geography/berlin-landmark-blocks.json').read_text())
 count=max(v for rows in landmarks.values() for row in rows for v in row)+1-640
 meta=bytearray((dest/'metatiles.bin').read_bytes()[:count*16])
 attrs=bytearray((dest/'metatile_attributes.bin').read_bytes()[:count*4])
 original=(R/'data/tilesets/secondary/pallet_town/metatiles.bin').read_bytes()
 original_attrs=(R/'data/tilesets/secondary/pallet_town/metatile_attributes.bin').read_bytes()
 home=struct.unpack('<480H',(R/'data/layouts/PalletTown/map.bin').read_bytes())
 roof=[[home[(3+y)*24+5+x]&1023 for x in range(5)] for y in range(3)]
 palette=(R/'data/tilesets/primary/general/palettes/02.pal').read_text().splitlines()
 # Palette 12 is unused by the existing Berlin map. Keep neutral colors;
 # replace only its terracotta ramp with a muted copper-green ramp.
 palette[3+8:3+15]=['96 131 106','131 164 139','180 213 172','106 172 123','82 148 106','57 123 90','32 90 65']
 (dest/'palettes/12.pal').write_text('\n'.join(palette)+'\n')
 tiles=Image.open(dest/'tiles.png');general=Image.open(R/'data/tilesets/primary/general/tiles.png')
 entries=struct.unpack('<%dH'%(len(meta)//2),meta)
 n=max((v&1023)-640 for v in entries if v&1023>=640)+1
 tile_ids={};variants={'home':roof}
 for label in ('library','workroom'):
  ids={};rows=[]
  for row in roof:
   out=[]
   for t in row:
    if t not in ids:
     values=list(struct.unpack_from('<8H',original,(t-640)*16))
     for i,v in enumerate(values):
      if v>>12!=2:continue
      if label=='library':values[i]=(v&0xfff)|0xc000
      else:
       source=v&1023
       if source not in tile_ids:
        tile=general.crop(((source%16)*8,(source//16)*8,(source%16)*8+8,(source//16)*8+8))
        tile.putdata([{8:4,9:3,10:2,11:4,12:5,13:6,14:7}.get(c,c) for c in tile.getdata()])
        assert n<384
        tiles.paste(tile,((n%16)*8,(n//16)*8));tile_ids[source]=640+n;n+=1
       values[i]=(v&0xfc00)|tile_ids[source]
     ids[t]=640+len(attrs)//4
     meta+=struct.pack('<8H',*values)
     attrs+=original_attrs[(t-640)*4:(t-640+1)*4]
    out.append(ids[t])
   rows.append(out)
  variants[label]=rows
 assert len(attrs)//4<=384
 tiles.save(dest/'tiles.png');(dest/'metatiles.bin').write_bytes(meta);(dest/'metatile_attributes.bin').write_bytes(attrs)
 (R/'data/geography/berlin-facade-blocks.json').write_text(json.dumps(variants,indent=2)+'\n')
 print('Berlin roof variants generated:',n,'secondary tiles')
if __name__=='__main__':build()
