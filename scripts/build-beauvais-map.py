"""A compressed Beauvais cathedral district east of the original reception garden."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1];W,H=64,36
old=struct.unpack('<480H',(R/'data/geography/beauvais-garden-v054.bin').read_bytes())
a=[[0x3010]*W for _ in range(H)]
def rect(x,y,w,h,t):
 for yy in range(y,y+h):
  for xx in range(x,x+w):a[yy][xx]=t
for y in range(20):a[y][:24]=old[y*24:(y+1)*24]
rect(22,16,40,4,0x3165)
rect(30,8,10,8,0x3165);rect(40,3,12,11,0x3165)
rect(38,12,4,8,0x3165);rect(50,12,3,12,0x3165)
rect(26,22,35,2,0x3165);rect(26,30,35,3,0x3165)
rect(30,19,3,12,0x3165);rect(54,19,3,12,0x3165)
water={(x,y) for y in range(25,28) for x in range(24,62)}
for x,y in water:
 l=(x-1,y) in water;r=(x+1,y) in water;u=(x,y-1) in water;d=(x,y+1) in water
 t=0x12b
 if not u:t=0x123 if l and r else 0x122 if not l else 0x124
 elif not d:t=0x131 if l and r else 0x130 if not l else 0x132
 elif not l:t=0x12a
 elif not r:t=0x12c
 a[y][x]=0x1000|t
rect(30,24,3,6,0x3165);rect(54,24,3,6,0x3165)
blocks=json.loads((R/'data/geography/beauvais-landmark-blocks.json').read_text())
for label,x,y in [('cathedral',43,5),('palace',32,10)]:
 for dy,row in enumerate(blocks[label]):
  for dx,t in enumerate(row):a[y+dy][x+dx]=0x400|t
signs=[('Cathedral',49,12,['SAINT-PIERRE - BEAUVAIS','The Gothic choir and transept.']),('Palace',38,14,['EPISCOPAL PALACE GATE','Two towers beside the cathedral.']),('River',46,23,['THERAIN RIVERSIDE','Cross the bridges to the south bank.'])]
for _,x,y,_ in signs:a[y][x]=0x402
# Complete tree crowns at every exposed forest edge, including the old opening.
for y in range(H):
 for x in range(W):
  if (x>=24 or y>=20) and (x<2 or x>=W-2 or y<2 or y>=H-2):a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
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
(R/'data/layouts/EuropeBeauvaisGarden/map.bin').write_bytes(struct.pack('<%dH'%(W*H),*(v for row in a for v in row)))
p=R/'data/layouts/layouts.json';j=json.loads(p.read_text())
for l in j['layouts']:
 if l.get('id')=='LAYOUT_EUROPE_BEAUVAIS_GARDEN':l.update(width=W,height=H,secondary_tileset='gTileset_EuropeBeauvais')
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeBeauvaisGarden/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith('EuropeBeauvaisGarden_Realism')]
for suffix,x,y,lines in signs:j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeBeauvaisGarden_Realism'+suffix))
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeBeauvaisGarden/scripts.inc';s=p.read_text().split('\nEuropeBeauvaisGarden_Realism')[0]
for suffix,x,y,lines in signs:
 label='EuropeBeauvaisGarden_Realism'+suffix;s+=f'\n{label}::\n\tmsgbox {label}Text, MSGBOX_SIGN\n\tend\n\n{label}Text::\n'
 for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\n')+'"\n'
p.write_text(s)
print('Historical Beauvais district generated; garden quests retained')
