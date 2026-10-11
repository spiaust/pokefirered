"""Convert generated backdrop, existing logo and native font into GBA tiles.
Only deterministic resizing, compositing, text layout and palette conversion.
Run with Pillow; source artwork and prompt remain in graphics/eclipse_title.
"""
from pathlib import Path
import re,struct
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'graphics/eclipse_title'
COLORS=[(8,8,24),(8,8,24),(240,248,224),(248,200,72),
 (16,32,56),(40,96,96),(32,40,72),(16,64,64),
 (144,224,160),(40,64,152),(40,24,56),(248,232,56),
 (64,160,128),(88,64,112),(72,120,136),(152,112,48)]
def indexed(im,colors):
 pal=Image.new('P',(1,1));pal.putpalette(sum(map(list,colors),[])+list(colors[0])*(256-len(colors)))
 return im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE)
def savepal(path,colors):
 path.write_bytes(('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in colors)).encode('ascii'))
font=Image.open(ROOT/'graphics/fonts/latin_normal.png')
charmap={m[1]:int(m[2],16) for m in re.finditer(r"'([^']+)'\s*=\s*([0-9A-F]{2})",(ROOT/'charmap.txt').read_text(encoding='utf-8'))}
widths=list(map(int,re.findall(r'\d+',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{([^}]+)',(ROOT/'src/text.c').read_text(encoding='utf-8')).group(1))))
def text(im,label,y,scale=1,color=(240,248,224),shadow=(8,8,24),x=None):
 w=sum(widths[charmap[c]] for c in label)*scale
 if x is None:x=(240-w)//2
 for c in label:
  n=charmap[c];g=font.crop((n%16*16,n//16*16,n%16*16+16,n//16*16+16))
  mask=Image.new('L',g.size);mask.putdata([255 if v==1 else 0 for v in g.getdata()]);mask=mask.resize((16*scale,16*scale),Image.Resampling.NEAREST)
  if shadow:im.paste(shadow,(x+scale,y+scale),mask)
  im.paste(color,(x,y),mask);x+=widths[n]*scale
im=Image.open(BASE/'source/backdrop.png').convert('RGB').resize((240,160),Image.Resampling.BOX)
logo=Image.open(ROOT/'graphics/title_screen/firered/game_title_logo.png').crop((0,0,176,64))
mask=Image.new('L',logo.size);mask.putdata([0 if v==0 else 255 for v in logo.getdata()])
logo=logo.convert('RGB').resize((176,53),Image.Resampling.NEAREST);mask=mask.resize((176,53),Image.Resampling.NEAREST)
im.paste(logo,(32,0),mask)
text(im,'EUROPE',49,color=COLORS[8])
text(im,'ECLIPSE',62,2,color=COLORS[3])
art=indexed(im,COLORS);art.save(BASE/'artwork.png');savepal(BASE/'artwork.pal',COLORS)
art.convert('RGB').resize((720,480),Image.Resampling.NEAREST).save(BASE/'preview.png')
# Keep original company names and display the requested current year.
credits=Image.new('RGB',(240,160),(0,0,0))
for y,label in zip([43,59,75,91],['2026  Pokémon.','1995-2026 Nintendo.','1995-2026 Creatures Inc.','1995-2026 GAME FREAK inc.']):
 text(credits,label,y,color=(248,248,248),shadow=None,x=38)
 d=ImageDraw.Draw(credits);d.ellipse((27,y+3,34,y+10),outline=(248,248,248));d.line([(32,y+5),(29,y+5),(29,y+8),(32,y+8)],fill=(248,248,248))
text(credits,'EUROPE: ECLIPSE / 2026',120,color=(144,224,160),shadow=None)
credits=indexed(credits,[(0,0,0),(248,248,248),(144,224,160)]+[(0,0,0)]*13)
credits.save(BASE/'copyright.png');savepal(BASE/'copyright.pal',[(0,0,0),(248,248,248),(144,224,160)]+[(0,0,0)]*13)
# Screen block has 32 tiles per row, visible image has 30; 600 sequential tiles.
(BASE/'copyright.bin').write_bytes(b''.join(struct.pack('<H',y*30+x if x<30 and y<20 else 0) for y in range(32) for x in range(32)))
print('Packed 240x160 title and current-year copyright screen')
