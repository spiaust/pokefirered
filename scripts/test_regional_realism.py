"""Walk regional landmarks, old-save tiles, signs, map menu and south connections."""
import json,struct,sys
from collections import deque
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action,open_key_item
from test_navigation import wait_task
from test_time import preserved
DATA={
 'Oxford':(12,3,[(38,10,'camera'),(54,10,'magdalen'),(58,13,'cherwell'),(60,19,'bridge'),(46,19,'meadow')],[(41,11,'UP'),(54,11,'LEFT'),(46,19,'DOWN')]),
 'Chantilly':(16,4,[(51,11,'chateau'),(55,9,'chateau-side'),(38,19,'stables'),(63,8,'gardens'),(63,5,'canal'),(51,13,'moat')],[(53,15,'UP'),(42,19,'LEFT'),(65,14,'UP')]),
 'Oranienburg':(20,5,[(48,10,'palace'),(48,9,'palace-court'),(37,8,'park'),(56,13,'bridge'),(59,17,'havel'),(56,20,'south-bridge')],[(49,12,'UP'),(39,11,'UP'),(59,16,'LEFT')]),
}
def run(city):
 index,selection,points,signs=DATA[city]
 layout=next(l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'] if l.get('id')==f'LAYOUT_EUROPE_{city.upper()}')
 W,H=layout['width'],layout['height'];tiles=struct.unpack('<%dH'%(W*H),(ROOT/layout['blockdata_filepath']).read_bytes());m=json.loads((ROOT/f'data/maps/Europe{city}/map.json').read_text());blocked={(o['x'],o['y']) for o in m['object_events']+m['warp_events']}
 a=(ROOT/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(ROOT/f'data/tilesets/secondary/europe_{city.lower()}/metatile_attributes.bin').read_bytes()
 def valid(x,y):
  if not(0<=x<W and 0<=y<H) or (x,y) in blocked:return False
  t=tiles[y*W+x];return not t&0xc00 and t>>12!=1 and struct.unpack_from('<I',a,(t&1023)*4)[0]&511 not in (0x10,0x11,0x12,0x13,0x15,0x19,0x1a,0x1b)
 def checkmap(e):
  width=e.read('VMap');base=e.read(e.symbols['VMap']+8)
  assert tuple(e.read(base+2*((y+7)*width+x+7),2) for y in range(H) for x in range(W))==tiles,city
 def go(e,target):
  start=e.location()[2:];q=deque([start]);prev={start:None}
  while q and target not in prev:
   x,y=q.popleft()
   for dx,dy,d in [(-1,0,'LEFT'),(1,0,'RIGHT'),(0,-1,'UP'),(0,1,'DOWN')]:
    p=(x+dx,y+dy)
    if p not in prev and valid(*p):prev[p]=((x,y),d);q.append(p)
  assert target in prev,(city,target)
  path=[];p=target
  while prev[p]:p,d=prev[p];path.append(d)
  for d in reversed(path):
   previous=e.location()[2:];e.walk(d,1)
   dx,dy={'LEFT':(-1,0),'RIGHT':(1,0),'UP':(0,-1),'DOWN':(0,1)}[d]
   expected=(previous[0]+dx,previous[1]+dy)
   assert e.location()[2:]==expected,(city,'step',d,previous,expected,e.location())
  assert e.location()==(43,index,*target),(city,target,e.location())
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,city.lower()+'-arrival',True);checkmap(e);before=preserved(e)[1:]
  for x,y,name in points:go(e,(x,y));e.screenshot(ROOT/f'test-output/{city.lower()}-realism-{name}.png')
  for x,y,d in signs:
   go(e,(x,y));e.press(d);e.press('A',180);e.screenshot(ROOT/f'test-output/{city.lower()}-realism-sign-{x}-{y}.png');e.finish_dialogue();assert not e.read('sLockFieldControls',1)
  assert preserved(e)[1:]==before
  print(f'PASS: {city} old battery terrain, landmark routes, crossings, signs and preserved progress',flush=True)
  x,y,_=points[0];go(e,(x,y));before=preserved(e)
  start_action(e,4)
  for _ in range(5):e.press('A',150)
  e.battery(ROOT/f'test-output/{city.lower()}-realism-save.sav')
 finally:e.close()
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,f'{city.lower()}-realism-save',True);checkmap(e);assert e.location()==(43,index,x,y) and preserved(e)==before
  open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapCurrent',1)==selection
  e.press('B',180);e.press('B',180);e.press('B',90);assert not e.read('sLockFieldControls',1)
  go(e,(19,12));go(e,(15,10));go(e,(23,10));go(e,(6,10))
  go(e,(15,23));e.walk('DOWN',1);e.frames(180);assert e.location()[:2]==(43,index+1),e.location()
  e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,index),e.location()
  go(e,(30,13));checkmap(e);e.screenshot(ROOT/f'test-output/{city.lower()}-realism-town-approach.png')
  print(f'PASS: {city} district Save/cold Continue, map return, service approaches and south trail round trip',flush=True)
 finally:e.close()
if __name__=='__main__':
 for city in sys.argv[1:] or DATA:run(city)
