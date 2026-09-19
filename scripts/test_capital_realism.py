"""Real-input tours of the Paris/Berlin landmark districts and old-save terrain."""
import json,struct,sys
from collections import deque
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_time import preserved

def run(city):
 index,country,points,signs=(4,'france',[(11,37,'eiffel'),(17,32,'seine'),(28,35,'notredame'),(27,38,'island-bridge'),(35,40,'south-bank')],[(6,38,'UP'),(24,36,'UP'),(18,27,'UP')]) if city=='Paris' else (8,'germany',[(21,33,'reichstag'),(21,37,'gate'),(31,26,'spree'),(33,38,'linden'),(9,33,'tiergarten')],[(26,31,'LEFT'),(26,36,'LEFT'),(14,34,'LEFT')])
 layout=next(l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'] if l.get('id')==f'LAYOUT_EUROPE_{city.upper()}')
 W,H=layout['width'],layout['height'];tiles=struct.unpack('<%dH'%(W*H),(ROOT/layout['blockdata_filepath']).read_bytes());m=json.loads((ROOT/f'data/maps/Europe{city}/map.json').read_text());blocked={(o['x'],o['y']) for o in m['object_events']+m['warp_events']}
 a=(ROOT/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(ROOT/f'data/tilesets/secondary/europe_{city.lower()}/metatile_attributes.bin').read_bytes()
 def valid(x,y):
  if not(0<=x<W and 0<=y<H) or (x,y) in blocked:return False
  t=tiles[y*W+x];return not t&0xc00 and struct.unpack_from('<I',a,(t&1023)*4)[0]&511 not in (0x10,0x11,0x12,0x13,0x15,0x19,0x1a,0x1b)
 def checkmap(e):
  width=e.read('VMap');base=e.read(e.symbols['VMap']+8)
  assert tuple(e.read(base+2*((y+7)*width+x+7),2) for y in range(H) for x in range(W))==tiles
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
  for d in reversed(path):e.walk(d,1)
  assert e.location()==(43,index,*target),(city,target,e.location())
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,f'start-{country}',True);checkmap(e);before=preserved(e)[1:]
  for x,y,name in points:go(e,(x,y));e.screenshot(ROOT/f'test-output/{city.lower()}-realism-{name}.png')
  if city=='Paris':
   for p in [(4,32),(4,36),(4,42),(13,42),(13,36),(17,32),(21,38),(26,38),(33,38)]:go(e,p)
   e.screenshot(ROOT/'test-output/paris-promenade-east.png')
   go(e,(9,40));e.screenshot(ROOT/'test-output/paris-garden-loop.png')
  if city=='Berlin':
   for p in [(4,32),(12,32),(12,36),(4,36),(4,32),(16,32)]:go(e,p)
   e.screenshot(ROOT/'test-output/berlin-garden-paths.png')
   go(e,(21,37));e.walk('UP',4);assert e.location()==(43,index,21,33)
  for x,y,d in signs:
   go(e,(x,y));e.press(d);e.press('A',180);e.screenshot(ROOT/f'test-output/{city.lower()}-realism-sign-{x}-{y}.png');e.finish_dialogue();assert not e.read('sLockFieldControls',1)
  assert preserved(e)[1:]==before
  print(f'PASS: {city} old battery terrain, landmark approaches, river crossings, signs and unchanged quest/inventory',flush=True)
  x,y,_=points[1];go(e,(x,y));before=preserved(e)
  start_action(e,4)
  for _ in range(5):e.press('A',150)
  e.battery(ROOT/f'test-output/{city.lower()}-realism-save.sav')
 finally:e.close()
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,f'{city.lower()}-realism-save',True);checkmap(e);assert e.location()==(43,index,x,y) and preserved(e)==before
  go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,index+1)
  print(f'PASS: {city} district Save/cold Continue and walk back through hub to countryside',flush=True)
 finally:e.close()
if __name__=='__main__':
 for city in sys.argv[1:] or ['Paris','Berlin']:run(city)
