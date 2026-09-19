"""Compile generated London landmark art to the GBA's indexed 4bpp format.
Keeps original Pallet metatile IDs stable; adds 56 London landmark blocks.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import struct,shutil,json
R=Path(__file__).resolve().parents[1]
def build():
 src=Image.open(R/'graphics/europe/landmarks/london-source.png').convert('RGBA')
 # Two atlas regions, cropped to their alpha bounds before hardware conversion.
 sprites=[]
 for box,size in [((0,0,1254,710),(128,80)),((0,710,650,1254),(64,64))]:
  s=src.crop(box);s=s.crop(s.getbbox());sprites.append(s.resize(size,Image.Resampling.LANCZOS))
 rgb=Image.new('RGB',(128,144),(0,0,0));rgb.paste(sprites[0].convert('RGB'),(0,0));rgb.paste(sprites[1].convert('RGB'),(0,80))
 colors=rgb.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
 palette=[0,0,0]+colors+[0]*(768-48)
 pal=Image.new('P',(1,1));pal.putpalette(colors+[0]*(768-45))
 base=R/'data/tilesets/secondary/pallet_town';dest=R/'data/tilesets/secondary/europe_london';dest.mkdir(exist_ok=True)
 shutil.copytree(base/'palettes',dest/'palettes',dirs_exist_ok=True)
 (dest/'palettes/07.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,palette[i:i+3])) for i in range(0,48,3))+'\n')
 tiles=Image.new('P',(128,192));tiles.putpalette(palette)
 original=Image.open(base/'tiles.png')
 for n in range(76):tiles.paste(original.crop(((n%16)*8,(n//16)*8,(n%16)*8+8,(n//16)*8+8)),((n%16)*8,(n//16)*8))
 meta=bytearray((base/'metatiles.bin').read_bytes());attrs=bytearray((base/'metatile_attributes.bin').read_bytes())
 general=(R/'data/tilesets/primary/general/metatiles.bin').read_bytes()
 under=struct.unpack_from('<4H',general,0x165*16)
 n=76;ids=[]
 for s in sprites:
  q=s.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE)
  idx=Image.new('P',s.size);idx.putpalette(palette);idx.putdata([0 if a<128 else c+1 for c,a in zip(q.getdata(),s.getchannel('A').getdata())])
  blocks=[]
  for my in range(s.height//16):
   row=[]
   for mx in range(s.width//16):
    entries=[]
    for dy,dx in [(0,0),(0,8),(8,0),(8,8)]:
     tile=idx.crop((mx*16+dx,my*16+dy,mx*16+dx+8,my*16+dy+8))
     tiles.paste(tile,((n%16)*8,(n//16)*8));entries.append(0x7000+640+n);n+=1
    row.append(640+len(attrs)//4);meta+=struct.pack('<8H',*under,*entries);attrs+=struct.pack('<I',0)
   blocks.append(row)
  ids.append(blocks)
 # Small native-palette rail overlays distinguish the two modern bridges.
 # Keep all existing landmark IDs and palettes unchanged.
 bridges={};deck=struct.unpack_from('<4H',general,0x16e*16)
 for name,colors in [('westminster',(3,15,1)),('lambeth',(11,10,9))]:
  bridges[name]=[]
  for south in (False,True):
   tile=Image.new('P',(16,16),0);draw=ImageDraw.Draw(tile)
   y=12 if south else 1
   draw.rectangle((0,y,15,y+2),fill=colors[0]);draw.line((0,y,15,y),fill=colors[1])
   for x in (0,8):
    draw.rectangle((x,10 if south else 0,x+1,15 if south else 5),fill=colors[0])
    draw.point((x,10 if south else 0),fill=colors[2])
   entries=[]
   for dy,dx in [(0,0),(0,8),(8,0),(8,8)]:
    tiles.paste(tile.crop((dx,dy,dx+8,dy+8)),((n%16)*8,(n//16)*8));entries.append(640+n);n+=1
   bridges[name].append(640+len(attrs)//4);meta+=struct.pack('<8H',*deck,*entries);attrs+=struct.pack('<I',0)
 assert n<=384,n
 tiles.save(dest/'tiles.png');(dest/'metatiles.bin').write_bytes(meta);(dest/'metatile_attributes.bin').write_bytes(attrs)
 (R/'data/geography/london-landmark-blocks.json').write_text(json.dumps(dict(palace=ids[0],eye=ids[1],bridges=bridges),indent=2)+'\n')
 print('London assets:',n,'tiles;',len(attrs)//4,'secondary metatiles')
if __name__=='__main__':build()
