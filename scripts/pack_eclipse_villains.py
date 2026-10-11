"""Pack generated character sheets into native GBA assets (Pillow required).
Artwork is in source/; this only crops, scales, indexes and packs it.
"""
from pathlib import Path
import hashlib,json
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
NAMES=['grunt','veil','boreal','patrol','vex','rime','warden','director']
BASE=ROOT/'graphics/eclipse_villains'
FIELD_COLORS=[(16,16,24),(40,40,48),(64,64,72),(144,144,152),(216,208,200),
 (240,184,144),(176,112,80),(56,32,80),(96,64,128),(144,104,168),
 (80,88,64),(104,64,48),(152,80,48),(144,168,208),(96,120,160)]
def fit(im,size,limits):
 a=im.getchannel('A').point(lambda x:255 if x>=128 else 0)
 box=a.getbbox();assert box,'empty source cell'
 im=im.crop(box);im.putalpha(a.crop(box))
 im.thumbnail(limits,Image.Resampling.NEAREST)
 out=Image.new('RGBA',size);out.alpha_composite(im,((size[0]-im.width)//2,size[1]-im.height-1))
 return out
def indexed(im,colors):
 p=Image.new('P',(1,1));p.putpalette(sum((list(c) for c in colors),[])+list(colors[-1])*(256-len(colors)))
 q=im.convert('RGB').quantize(palette=p,dither=Image.Dither.NONE)
 out=Image.new('P',im.size);out.putpalette([255,0,255]+sum((list(c) for c in colors),[])+[0]*720)
 out.putdata([v+1 if a>=128 else 0 for v,a in zip(q.getdata(),im.getchannel('A').getdata())])
 out.info['transparency']=0
 return out
def pal(path,colors):
 text='JASC-PAL\r\n0100\r\n16\r\n255 0 255\r\n'+''.join('%d %d %d\r\n'%c for c in colors)
 path.write_bytes(text.encode('ascii'))
for folder in ['battle','overworld']: (BASE/folder).mkdir(exist_ok=True)
pal(BASE/'overworld/shared.pal',FIELD_COLORS)
preview=Image.new('RGB',(8*160,220),(224,232,224));draw=ImageDraw.Draw(preview)
frame_checksums={}
for n,name in enumerate(NAMES):
 im=Image.open(BASE/'source'/f'{name}.png').convert('RGBA');w,h=im.size;mid=w//2
 battle=fit(im.crop((0,0,mid,h)),(64,64),(58,60))
 pixels=[rgb[:3] for rgb in battle.getdata() if rgb[3]>=128]
 opaque=Image.new('RGB',(len(pixels),1));opaque.putdata(pixels)
 q=opaque.quantize(colors=15,dither=Image.Dither.NONE)
 colors=[tuple(q.getpalette()[i*3:i*3+3]) for i in range(15)]
 native=indexed(battle,colors);native.save(BASE/'battle'/f'{name}.png');pal(BASE/'battle'/f'{name}.pal',colors)
 cells=[]
 for row in range(3):
  for col in range(3):
   cell=im.crop((mid+(w-mid)*col//3,h*row//3,mid+(w-mid)*(col+1)//3,h*(row+1)//3))
   if name=='vex' and row==2 and col==2:cell=ImageOps.mirror(cell)
   cells.append(fit(cell,(16,32),(14,28)))
 # Standard engine frame order: S idle,N idle,W idle,S steps,N steps,W steps.
 packed=Image.new('RGBA',(144,32))
 for i,j in enumerate([0,3,6,1,2,4,5,7,8]):packed.alpha_composite(cells[j],(16*i,0))
 packed_native=indexed(packed,FIELD_COLORS);packed_native.save(BASE/'overworld'/f'{name}.png')
 pixels=packed_native.load();frame_checksums[name]=[]
 for frame in range(9):
  raw=bytearray()
  for ty in range(4):
   for tx in range(2):
    for y in range(8):
     for x in range(0,8,2):
      px=frame*16+tx*8+x;py=ty*8+y
      raw.append(pixels[px,py]|(pixels[px+1,py]<<4))
  frame_checksums[name].append(hashlib.sha256(raw).hexdigest())
 preview.paste(native.convert('RGBA').resize((128,128),Image.Resampling.NEAREST),(n*160+16,22),native.convert('RGBA').resize((128,128),Image.Resampling.NEAREST))
 draw.text((n*160+16,4),name.upper(),fill=(24,24,32))
 for i in range(3):
  c=indexed(cells[i*3],FIELD_COLORS).convert('RGBA').resize((32,64),Image.Resampling.NEAREST)
  preview.paste(c,(n*160+24+i*36,154),c)
preview.save(BASE/'preview.png')
(BASE/'overworld/frame_checksums.json').write_text(json.dumps(frame_checksums,indent=2)+'\n',encoding='utf-8')
print('Packed eight 64x64 portraits and eight nine-frame 16x32 walking sheets.')
