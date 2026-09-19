"""Author a compressed Westminster/South Bank district below London's hub.
The v0.50 hub's walkable tiles and event coordinates remain compatible.
"""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
W,H=40,44
old=struct.unpack('<768H',(R/'data/geography/london-v050.bin').read_bytes())
a=[[0x3010 for x in range(W)] for y in range(H)]
for y in range(22):a[y][:32]=old[y*32:(y+1)*32]
def rect(x,y,w,h,t):
 for yy in range(y,y+h):
  for xx in range(x,x+w):a[yy][xx]=t
# City streets: preserve every collision/event tile in the old hub.
for y in range(2,18):
 for x in range(2,30):
  if a[y][x]==0x3296:
   a[y][x]=0x3165 if (14<=x<=17 or 12<=y<=14) else 0x3010
# North/south Whitehall approach, Parliament Square, riverside paths.
rect(14,22,4,8,0x3165);rect(5,27,15,3,0x3165)
rect(5,35,15,3,0x3165);rect(18,22,2,12,0x3165)
rect(24,22,2,11,0x3165);rect(26,31,2,10,0x3165)
rect(24,29,12,2,0x3165);rect(24,23,12,2,0x3165)
rect(34,23,2,18,0x3165);rect(16,39,20,2,0x3165)
# River follows the Westminster bend. Top joins the existing river section.
water=set()
for y in range(22,42):
 left=20 if y<33 else 21 if y<36 else 22
 for x in range(left,left+4):water.add((x,y))
for x,y in water:
 l=(x-1,y) in water;r=(x+1,y) in water;u=(x,y-1) in water or y==22;d=(x,y+1) in water or y==41
 tile=0x12b
 if not u:tile=0x123 if l and r else 0x122 if not l else 0x124
 elif not d:tile=0x131 if l and r else 0x130 if not l else 0x132
 elif not l:tile=0x12a
 elif not r:tile=0x12c
 a[y][x]=0x1000|tile
# Westminster Bridge and southern crossing, with continuous walking approaches.
rect(18,28,8,2,0x3165);rect(19,38,9,2,0x3165)
# Distinct gardens either side: Parliament lawn, Jubilee Gardens behind wheel.
rect(6,24,6,2,0x3004);rect(28,32,5,3,0x3004)
rect(7,38,6,2,0x3004)
# Garden loop and continuous east-bank approach beside the Eye.
rect(27,31,7,1,0x3165);rect(33,31,1,7,0x3165)
rect(29,35,5,1,0x3165);rect(28,36,6,2,0x3165)
blocks=json.loads((R/'data/geography/london-landmark-blocks.json').read_text())
# Apply rails only over the existing bridge footprints, retaining clearance.
for name,x,y,w in [('westminster',20,28,4),('lambeth',22,38,4)]:
 for dy,t in enumerate(blocks['bridges'][name]):rect(x,y+dy,w,1,0x3000|t)
for label,x,y in [('palace',10,30),('eye',27,25)]:
 for dy,row in enumerate(blocks[label]):
  for dx,t in enumerate(row):a[y+dy][x+dx]=0x400|t
# Signs beside each landmark, all reachable from public paths.
for x,y in [(14,26),(18,30),(26,27),(28,35)]:a[y][x]=0x402
# Complete forest boundary; finish exposed caps/edges to avoid cut trees.
for y in range(H):
 for x in range(W):
  if x<2 or x>=W-2 or y>=H-2 or (y<2 and x>=32):a[y][x]=0x400|((0x14 if y%2 else 0x1c)+x%2)
original=[r[:] for r in a];forestids={0x14,0x15,0x1c,0x1d}
def forest(x,y):return x<0 or y<0 or x>=W or y>=H or original[y][x]&0x3ff in forestids
for y in range(H):
 for x in range(W):
  t=original[y][x]&0x3ff
  if t not in forestids:continue
  right=t in (0x15,0x1d)
  if t in (0x1c,0x1d) and not forest(x,y-1):t=0xf if right else 0xe
  elif t in (0x14,0x15) and not forest(x,y+1):t=0x25 if right else 0x24
  if t in (0x14,0x1c,0x24) and not forest(x-1,y):t+=2
  if t in (0x15,0x1d,0x25) and not forest(x+1,y):t+=2
  a[y][x]=(original[y][x]&~0x3ff)|t
from europe_trees import finish_trees
finish_trees(a)
(R/'data/layouts/EuropeLondon/map.bin').write_bytes(struct.pack('<%dH'%(W*H),*(v for row in a for v in row)))
p=R/'data/layouts/layouts.json';j=json.loads(p.read_text())
for l in j['layouts']:
 if l.get('id')=='LAYOUT_EUROPE_LONDON':l.update(width=W,height=H,secondary_tileset='gTileset_EuropeLondon')
p.write_text(json.dumps(j,indent=2)+'\n')
p=R/'data/maps/EuropeLondon/map.json';j=json.loads(p.read_text());j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith('EuropeLondon_Realism')]
for suffix,x,y in [('Whitehall',14,26),('Parliament',18,30),('Eye',26,27),('Gardens',28,35)]:
 j['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='EuropeLondon_Realism'+suffix))
p.write_text(json.dumps(j,indent=2)+'\n')
print('London:',W,'x',H,'with Westminster landmarks and two new crossings')
