"""Walk the London district via real input, including old saves and cold saves."""
import json,struct
from collections import deque
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action,open_key_item
from test_time import preserved
from test_navigation import wait_task
layout=next(l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'] if l.get('id')=='LAYOUT_EUROPE_LONDON')
W,H=layout['width'],layout['height'];tiles=struct.unpack('<%dH'%(W*H),(ROOT/layout['blockdata_filepath']).read_bytes())
m=json.loads((ROOT/'data/maps/EuropeLondon/map.json').read_text());blocked={(e['x'],e['y']) for e in m['object_events']+m['warp_events']}
a=(ROOT/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(ROOT/'data/tilesets/secondary/europe_london/metatile_attributes.bin').read_bytes()
def valid(x,y):
 if not(0<=x<W and 0<=y<H) or (x,y) in blocked:return False
 t=tiles[y*W+x];return not t&0xc00 and struct.unpack_from('<I',a,(t&1023)*4)[0]&511 not in (0x10,0x11,0x12,0x13,0x15,0x19,0x1a,0x1b)
def assert_map(e):
 width=e.read('VMap');base=e.read(e.symbols['VMap']+8)
 actual=tuple(e.read(base+2*((y+7)*width+x+7),2) for y in range(H) for x in range(W))
 assert actual==tiles,[(i%W,i//W,hex(a),hex(b)) for i,(a,b) in enumerate(zip(actual,tiles)) if a!=b][:8]
def go(e,target):
 start=e.location()[2:];q=deque([start]);prev={start:None}
 while q and target not in prev:
  x,y=q.popleft()
  for dx,dy,d in [(-1,0,'LEFT'),(1,0,'RIGHT'),(0,-1,'UP'),(0,1,'DOWN')]:
   p=(x+dx,y+dy)
   if p not in prev and valid(*p):prev[p]=((x,y),d);q.append(p)
 assert target in prev,target
 path=[];p=target
 while prev[p]:p,d=prev[p];path.append(d)
 for d in reversed(path):e.walk(d,1)
 assert e.location()==(43,0,*target), (target,e.location())
def save(e,name):
 start_action(e,4)
 for _ in range(5):e.press('A',150)
 e.battery(ROOT/f'test-output/{name}.sav')

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);assert_map(e);before=preserved(e)
 assert e.location()==(43,0,19,12)
 for point,name in [((15,25),'whitehall'),((15,35),'parliament'),((25,29),'westminster-bridge'),((31,29),'london-eye'),((27,38),'south-bank')]:
  go(e,point);e.screenshot(ROOT/f'test-output/london-realism-{name}.png')
 for x,y,label in [(20,28,'green-north'),(20,29,'green-south'),(22,38,'red-north'),(22,39,'red-south')]:
  go(e,(x,y));e.walk('RIGHT',4);assert e.location()==(43,0,x+4,y)
  e.walk('LEFT',4);assert e.location()==(43,0,x,y)
  e.screenshot(ROOT/f'test-output/london-bridge-{label}.png')
 for p in [(27,31),(33,31),(33,36),(29,36),(27,37)]:go(e,p)
 e.screenshot(ROOT/'test-output/london-garden-loop.png')
 assert preserved(e)==before
 print('PASS: v0.50 battery continues; walking loop reaches Parliament, both banks, bridges and Eye without changing progress',flush=True)
 for point,d in [((14,27),'UP'),((19,30),'LEFT'),((25,27),'RIGHT'),((28,36),'UP')]:
  go(e,point);e.press(d);e.press('A',180);e.finish_dialogue();assert not e.read('sLockFieldControls',1)
 print('PASS: four landmark signs release controls and all approaches are reachable',flush=True)
 go(e,(31,30));before=preserved(e);save(e,'london-realism-eye')
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'london-realism-eye',True);assert_map(e);assert e.location()==(43,0,31,30);assert preserved(e)==before
 go(e,(15,25));open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapCurrent',1)==0
 e.press('B',180);e.press('B',180);e.press('B',90)
 go(e,(6,10));e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,3)
 e.walk('UP',1);e.walk('RIGHT',1);e.walk('DOWN',2);e.frames(180)
 assert e.location()[:2]==(43,0),e.location()
 go(e,(23,10));e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,2)
 print('PASS: district Save/cold Continue, map return, clinic and station entrances',flush=True)
finally:e.close()


