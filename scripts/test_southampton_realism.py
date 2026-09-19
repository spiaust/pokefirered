"""Walk historical Southampton landmarks while preserving historical progression."""
import json,struct,sys
from collections import deque
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action,open_key_item
from test_navigation import wait_task
from test_time import preserved
DATA={'SouthamptonPast':(36,0,[(48,7,'bargate'),(36,25,'tudor'),(28,18,'walls'),(43,20,'high-street'),(49,37,'quay')],[(49,10,'UP'),(37,28,'UP'),(29,15,'LEFT'),(51,34,'UP')])}

def run(city):
 index,selection,points,signs=DATA[city]
 layout=next(l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'] if l.get('id')=='LAYOUT_EUROPE_SOUTHAMPTON_PAST')
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
  load_checkpoint(e,'southampton-arrival',True);checkmap(e);before=preserved(e)[1:];story=tuple(e.var(v) for v in range(0x40d5,0x40ef))
  for x,y,name in points:go(e,(x,y));e.screenshot(ROOT/f'test-output/{city.lower()}-realism-{name}.png')
  for x,y,d in signs:
   go(e,(x,y));e.press(d);e.press('A',180);e.screenshot(ROOT/f'test-output/{city.lower()}-realism-sign-{x}-{y}.png');e.finish_dialogue();assert not e.read('sLockFieldControls',1)
  assert preserved(e)[1:]==before and tuple(e.var(v) for v in range(0x40d5,0x40ef))==story
  print(f'PASS: {city} old battery terrain, landmark routes, crossings, signs and preserved progress',flush=True)
  x,y,_=points[0];go(e,(x,y));before=preserved(e)
  start_action(e,4)
  for _ in range(5):e.press('A',150)
  e.battery(ROOT/f'test-output/{city.lower()}-realism-save.sav')
 finally:e.close()
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,f'{city.lower()}-realism-save',True);checkmap(e);assert e.location()==(43,index,x,y) and preserved(e)==before
  open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapCurrent',1)==selection and e.read('sEuropeMapPast',1)==1
  e.press('B',180);e.press('B',180);e.press('B',90);assert not e.read('sLockFieldControls',1)
  go(e,(8,5));checkmap(e)
  from test_southampton import host,clerk
  host(e,'YES');clerk(e);checkmap(e)
  from test_time import cross
  cross(e);assert e.location()==(43,17,15,24)
  print(f'PASS: {city} district Save/cold Continue, era map, Le Havre ferry round trip and Celebi return',flush=True)
 finally:e.close()
if __name__=='__main__':
 for city in sys.argv[1:] or DATA:run(city)
