"""Historical Westminster district east of the original London reception."""
from pathlib import Path
import json,struct
import sys
city='London'
R=Path(__file__).resolve().parents[1];W,H=80,40;ow=24
old=struct.unpack('<480H',(R/'data/geography/london-past-v058.bin').read_bytes())
a=[[0x3010]*W for _ in range(H)]
def rect(x,y,w,h,t):
 for yy in range(y,y+h):
  for xx in range(x,x+w):a[yy][xx]=t
for y in range(20):a[y][:ow]=old[y*ow:(y+1)*ow]
rect(ow-2,16,W-ow,4,0x3165)
# Whitehall approaches Parliament Square from the north, west of the river.
rect(35,3,3,14,0x3165);rect(28,14,23,3,0x3165)
rect(30,17,7,5,0x3004);rect(28,22,23,3,0x3165)
rect(39,17,12,14,0x3165);rect(27,28,25,3,0x3165)
rect(49,3,3,34,0x3165);rect(59,3,3,34,0x3165)
rect(61,11,14,3,0x3165);rect(72,11,3,26,0x3165)
rect(60,34,15,3,0x3165)
water=set()
for y in range(2,38):
 left=52 if y<26 else 53 if y<31 else 54
 for x in range(left,left+6):water.add((x,y))
bridges=[(49,15,13,2),(49,32,14,2)]
places=[('palace',41,19)]
signs=[('Palace',48,25,['PALACE OF WESTMINSTER','The clock tower beside the THAMES.']),('Square',37,18,['PARLIAMENT SQUARE','WHITEHALL leads north from here.']),('Westminster',60,14,['WESTMINSTER BRIDGE','Cross the THAMES by Parliament.']),('Lambeth',62,34,['LAMBETH BRIDGE','The southern river crossing.'])]
for x,y in water:
 l=(x-1,y) in water;r=(x+1,y) in water;u=(x,y-1) in water;d=(x,y+1) in water
 t=0x12b
 if not u:t=0x123 if l and r else 0x122 if not l else 0x124
 elif not d:t=0x131 if l and r else 0x130 if not l else 0x132
 elif not l:t=0x12a
 elif not r:t=0x12c
 a[y][x]=0x1000|t
for x,y,w,h in bridges:rect(x,y,w,h,0x3165)
blocks=json.loads((R/'data/geography/london-landmark-blocks.json').read_text())
for label,x,y in places:
 for dy,row in enumerate(blocks[label]):
  for dx,t in enumerate(row):a[y+dy][x+dx]=0x400|t
for _,x,y,_ in signs:a[y][x]=0x402
# Complete tree crowns at every exposed forest edge, including the old opening.
for y in range(H):
 for x in range(W):
  if (x>=ow or y>=20) and (x<2 or x>=W-2 or y<2 or y>=H-2):a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
original=[row[:] for row in a];forestids={0xe,0xf,*range(0x14,0x20),*range(0x24,0x28)}
def forest(x,y):return x<0 or y<0 or x>=W or y>=H or original[y][x]&1023 in forestids
for y in range(H):
 for x in range(W):
  if original[y][x]&1023 not in forestids:continue
  right=bool(x%2);t=(0x14 if y%2 else 0x1c)+right
  if not forest(x,y-1):t=0xf if right else 0xe
  elif not forest(x,y+1):t=0x25 if right else 0x24
  if not right and not forest(x-1,y) and t in (0x14,0x1c,0x24):t+=2
  if right and not forest(x+1,y) and t in (0x15,0x1d,0x25):t+=2
  a[y][x]=(original[y][x]&~1023)|t
from europe_trees import finish_trees
finish_trees(a)
(R/f'data/layouts/Europe{city}Past/map.bin').write_bytes(struct.pack('<%dH'%(W*H),*(v for row in a for v in row)))
p=R/'data/layouts/layouts.json';j=json.loads(p.read_text())
for l in j['layouts']:
 if l.get('id')==f'LAYOUT_EUROPE_{city.upper()}_PAST':l.update(width=W,height=H,secondary_tileset=f'gTileset_Europe{city}')
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/f'data/maps/Europe{city}Past/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith(f'Europe{city}Past_Realism')]
for suffix,x,y,lines in signs:j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=f'Europe{city}Past_Realism'+suffix))
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/f'data/maps/Europe{city}Past/scripts.inc';s=p.read_text().split(f'\nEurope{city}Past_Realism')[0]
for suffix,x,y,lines in signs:
 label=f'Europe{city}Past_Realism'+suffix;s+=f'\n{label}::\n\tmsgbox {label}Text, MSGBOX_SIGN\n\tend\n\n{label}Text::\n'
 for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\n')+'"\n'
p.write_text(s)
print(city,'historical district generated; original quest hub retained')
