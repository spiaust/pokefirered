from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from key_item_test_helpers import reload
import json,struct
from collections import deque
from test_landmark_cases import talk
inside=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe'].index('EuropePalaceVisitor')
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def live_go(e,target):
 start=e.location()[2:];width=e.read('VMap');grid=e.read(e.symbols['VMap']+8);objects={(8,3),(3,3),(11,3)};exits={(4,8),(5,8)};prev={start:None};q=deque([start])
 while q:
  x,y=q.popleft()
  if (x,y)==target:break
  for dx,dy,d in [(-1,0,'LEFT'),(1,0,'RIGHT'),(0,-1,'UP'),(0,1,'DOWN')]:
   n=x+dx,y+dy
   if not(0<=n[0]<13 and 0<=n[1]<10) or n in prev or n in objects or n in exits:continue
   v=e.read(grid+2*((n[1]+7)*width+n[0]+7),2)
   if v&0xc00:continue
   prev[n]=((x,y),d);q.append(n)
 assert target in prev,(start,target)
 path=[];n=target
 while prev[n]:n,d=prev[n];path.append(d)
 for d in reversed(path):e.walk(d,1)
 assert e.location()[2:]==target
e=Emulator(ROOT/'pokefirered.gba')
try:
 for tag,point,direction in [('left',(2,5),'LEFT'),('right',(10,6),'DOWN')]:
  load_checkpoint(e,'palace-gallery-old-'+tag,True);assert e.location()==(43,inside,*point);before=preserved(e)[1:],history(e);e.screenshot(ROOT/f'test-output/palace-legacy-{tag}-continued.png');e.walk(direction,1)
  assert e.location()[2:]!=point
  live_go(e,(9,7));e=reload(e,'palace-legacy-'+tag);assert (preserved(e)[1:],history(e))==before
  live_go(e,(5,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,20,48,9) and (preserved(e)[1:],history(e))==before
  talk(e,(48,9),choice='YES');assert e.location()==(43,inside,5,7)
  width=e.read('VMap');grid=e.read(e.symbols['VMap']+8);expected=struct.unpack('<130H',(ROOT/'data/layouts/EuropePalaceVisitor/map.bin').read_bytes())
  assert tuple(e.read(grid+2*((y+7)*width+x+7),2) for y in range(10) for x in range(13))==expected
  e.screenshot(ROOT/f'test-output/palace-legacy-{tag}-reentered.png');go(e,(5,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,20,48,9) and (preserved(e)[1:],history(e))==before
  print(f'PASS: genuine v2.24 {tag}-table-position save cold Continues in its cached layout, saves/exits and re-enters the exact redesigned room with progress intact',flush=True)
finally:e.close()
