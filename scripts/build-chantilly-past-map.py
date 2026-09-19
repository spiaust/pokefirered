"""A compressed historical estate east of the unchanged story refuge."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1];W,H=56,32
old=struct.unpack('<224H',(R/'data/geography/chantilly-past-v053.bin').read_bytes())
a=[[0x3010]*W for _ in range(H)]
def rect(x,y,w,h,t):
 for yy in range(y,y+h):
  for xx in range(x,x+w):a[yy][xx]=t
for y in range(14):a[y][:16]=old[y*16:(y+1)*16]
rect(14,10,8,2,0x3165);rect(18,11,3,15,0x3165)
rect(20,12,34,3,0x3165);rect(19,16,10,6,0x3165)
rect(27,18,24,2,0x3165)
water={(x,y) for y in range(4,13) for x in range(31,41)}
for y in range(5,12):
 for x in range(32,40):water.remove((x,y));a[y][x]=0x3165
water.update((x,y) for x in range(43,52) for y in range(3,5))
rect(42,5,2,14,0x3165);rect(51,5,2,14,0x3165)
rect(43,6,8,2,0x3004);rect(43,10,8,2,0x3004)
rect(46,5,2,14,0x3165)
# Grande Pelouse lies south of the Great Stables; quiet paths, no modern exhibits.
rect(19,23,19,2,0x3165);rect(19,28,19,2,0x3165)
rect(19,24,2,4,0x3165);rect(36,24,2,4,0x3165)
rect(27,20,2,4,0x3165)
for x,y in water:
 l=(x-1,y) in water;r=(x+1,y) in water;u=(x,y-1) in water;d=(x,y+1) in water
 t=0x12b
 if not u:t=0x123 if l and r else 0x122 if not l else 0x124
 elif not d:t=0x131 if l and r else 0x130 if not l else 0x132
 elif not l:t=0x12a
 elif not r:t=0x12c
 a[y][x]=0x1000|t
rect(34,11,2,5,0x3165)
blocks=json.loads((R/'data/geography/chantilly-landmark-blocks.json').read_text())
for label,x,y in [('chateau',33,6),('stables',19,16)]:
 for dy,row in enumerate(blocks[label]):
  for dx,t in enumerate(row):a[y+dy][x+dx]=0x400|t
signs=[('Chateau',37,14,['CHATEAU DE CHANTILLY - 1940','The moat surrounds the chateau.']),('Stables',25,19,['GRANDES ECURIES','The Great Stables face the lawns.']),('Pelouse',34,26,['GRANDE PELOUSE','Return west to the refuge.'])]
for _,x,y,_ in signs:a[y][x]=0x402
# Complete tree crowns at every exposed forest edge, including the old opening.
for y in range(H):
 for x in range(W):
  if (x>=16 or y>=14) and (x<2 or x>=W-2 or y<2 or y>=H-2):a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
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
(R/'data/layouts/EuropeChantillyPast/map.bin').write_bytes(struct.pack('<%dH'%(W*H),*(v for row in a for v in row)))
p=R/'data/layouts/layouts.json';j=json.loads(p.read_text())
for l in j['layouts']:
 if l.get('id')=='LAYOUT_EUROPE_CHANTILLY_PAST':l.update(width=W,height=H,secondary_tileset='gTileset_EuropeChantilly')
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeChantillyPast/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith('EuropeChantillyPast_Realism')]
for suffix,x,y,lines in signs:j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeChantillyPast_Realism'+suffix))
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeChantillyPast/scripts.inc';s=p.read_text().split('\nEuropeChantillyPast_Realism')[0]
for suffix,x,y,lines in signs:
 label='EuropeChantillyPast_Realism'+suffix;s+=f'\n{label}::\n\tmsgbox {label}Text, MSGBOX_SIGN\n\tend\n\n{label}Text::\n'
 for i,line in enumerate(lines):s+='\t.string "'+line+('$' if i==len(lines)-1 else '\\n')+'"\n'
p.write_text(s)
print('Historical Chantilly estate generated; story refuge and arrival coordinates retained')
