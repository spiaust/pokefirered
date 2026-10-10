"""Compile the Paris/Berlin atlas into each city's independent GBA tileset."""
from pathlib import Path
from PIL import Image
import struct,shutil,json
R=Path(__file__).resolve().parents[1]
def build(city,specs,source="capitals-source.png",mask_palette=False,base_name="pallet_town",base_tiles=76):
 src=Image.open(R/'graphics/europe/landmarks'/source).convert('RGBA');w,h=src.size
 sprites=[]
 for label,region,size in specs:
  if len(region)==2:
   qx,qy=region;region=((0,600)[qx],(0,730)[qy],(600,w)[qx],(730,h)[qy])
  s=src.crop(region)
  bounds=s.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox() if mask_palette else s.getbbox()
  assert bounds, (city,label,'empty sprite')
  s=s.crop(bounds);sprites.append((label,s.resize(size,Image.Resampling.LANCZOS)))
 rgb=Image.new('RGB',(128,192),(0,0,0));y=0
 for _,s in sprites:
  mask=s.getchannel('A').point(lambda v:255 if v>=128 else 0) if mask_palette else None
  rgb.paste(s.convert('RGB'),(0,y),mask);y+=s.height
 colors=rgb.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45];palette=[0,0,0]+colors+[0]*(768-48)
 pal=Image.new('P',(1,1));pal.putpalette(colors+[0]*(768-45))
 base=R/f'data/tilesets/secondary/{base_name}';dest=R/f'data/tilesets/secondary/europe_{city.lower()}';dest.mkdir(exist_ok=True)
 shutil.copytree(base/'palettes',dest/'palettes',dirs_exist_ok=True)
 (dest/'palettes/07.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,palette[i:i+3])) for i in range(0,48,3))+'\n')
 tiles=Image.new('P',(128,192));tiles.putpalette(palette);original=Image.open(base/'tiles.png')
 for n in range(base_tiles):tiles.paste(original.crop(((n%16)*8,(n//16)*8,(n%16)*8+8,(n//16)*8+8)),((n%16)*8,(n//16)*8))
 meta=bytearray((base/'metatiles.bin').read_bytes());attrs=bytearray((base/'metatile_attributes.bin').read_bytes());general=(R/'data/tilesets/primary/general/metatiles.bin').read_bytes();under=struct.unpack_from('<4H',general,0x165*16)
 n=base_tiles;ids={}
 for label,s in sprites:
  q=s.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE);idx=Image.new('P',s.size);idx.putpalette(palette);idx.putdata([0 if a<128 else c+1 for c,a in zip(q.getdata(),s.getchannel('A').getdata())]);blocks=[]
  for my in range(s.height//16):
   row=[]
   for mx in range(s.width//16):
    entries=[]
    for dy,dx in [(0,0),(0,8),(8,0),(8,8)]:
     tiles.paste(idx.crop((mx*16+dx,my*16+dy,mx*16+dx+8,my*16+dy+8)),((n%16)*8,(n//16)*8));entries.append(0x7000+640+n);n+=1
    row.append(640+len(attrs)//4);meta+=struct.pack('<8H',*under,*entries);attrs+=struct.pack('<I',0)
   blocks.append(row)
  ids[label]=blocks
 if city=='Paris':
  # Copy native roof tiles into the existing blue-gray palette 8.
  # No shared palette is altered. Preserve transparent index zero.
  sourcepal=[tuple(map(int,line.split())) for line in (R/'data/tilesets/primary/general/palettes/02.pal').read_text().splitlines()[3:]]
  targetpal=[tuple(map(int,line.split())) for line in (base/'palettes/08.pal').read_text().splitlines()[3:]]
  for index,color in {11:(156,180,205),12:(115,148,180),13:(82,115,148),14:(49,74,106)}.items():sourcepal[index]=color
  remap=[0]+[min(range(1,16),key=lambda j:sum((sourcepal[i][c]-targetpal[j][c])**2 for c in range(3))) for i in range(1,16)]
  remap[11:15]=[3,4,6,7]  # Four ordered native blue-gray roof shades.
  primary=Image.open(R/'data/tilesets/primary/general/tiles.png')
  house={};tilecopies={}
  pallet=struct.unpack('<480H',(R/'data/layouts/PalletTown/map.bin').read_bytes())
  for old in sorted({pallet[y*24+x]&1023 for y in range(3,6) for x in range(5,10)}):
   entries=list(struct.unpack_from('<8H',meta,(old-640)*16))
   for i,v in enumerate(entries):
    if v>>12!=2:continue
    tileid=v&1023
    if tileid not in tilecopies:
     image=primary.crop(((tileid%16)*8,(tileid//16)*8,(tileid%16)*8+8,(tileid//16)*8+8))
     image.putdata([remap[c] for c in image.getdata()])
     tiles.paste(image,((n%16)*8,(n//16)*8));tilecopies[tileid]=640+n;n+=1
    entries[i]=0x8000|(v&0xc00)|tilecopies[tileid]
   house[str(old)]=640+len(attrs)//4
   meta+=struct.pack('<8H',*entries);attrs+=attrs[(old-640)*4:(old-640+1)*4]
  ids.update(garden_roof=house,roof_tiles=tilecopies,roof_remap=remap)
  western={};walltiles={};wallremap=[0,1,8,9,4,5,6,7,8,9,10,11,12,13,14,15]
  for old in (0x298,0x299,0x29a,0x29b,0x29c,0x2a0,0x2a1,0x2a2,0x2a4):
   entries=list(struct.unpack_from('<8H',meta,(old-640)*16))
   for i,v in enumerate(entries):
    if v>>12!=3:continue
    tileid=v&1023
    if tileid not in walltiles:
     image=primary.crop(((tileid%16)*8,(tileid//16)*8,(tileid%16)*8+8,(tileid//16)*8+8))
     image.putdata([wallremap[c] for c in image.getdata()])
     tiles.paste(image,((n%16)*8,(n//16)*8));walltiles[tileid]=640+n;n+=1
    entries[i]=0x3000|(v&0xc00)|walltiles[tileid]
   western[str(old)]=640+len(attrs)//4
   meta+=struct.pack('<8H',*entries);attrs+=attrs[(old-640)*4:(old-640+1)*4]
  ids.update(western_wall=western,wall_tiles=walltiles,wall_remap=wallremap)
 assert n<=384
 tiles.save(dest/'tiles.png');(dest/'metatiles.bin').write_bytes(meta);(dest/'metatile_attributes.bin').write_bytes(attrs)
 (R/f'data/geography/{city.lower()}-landmark-blocks.json').write_text(json.dumps(ids,indent=2)+'\n')
 print(city,n,'tiles;',len(attrs)//4,'secondary metatiles')
 if city=='Berlin':
  from berlin_facades import build as build_facades
  build_facades()
if __name__=='__main__':
 import sys
 cities=sys.argv[1:] or ['Paris','Berlin']
 if 'Paris' in cities:build('Paris',[('eiffel',(0,0),(64,96)),('notredame',(1,0),(96,64))])
 if 'Berlin' in cities:build('Berlin',[('gate',(0,1),(96,48)),('reichstag',(1,1),(96,64))])
