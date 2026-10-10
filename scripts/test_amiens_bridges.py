"""Historical bridge lanes and earned story/return paths through native controls."""
import json,struct
from collections import deque
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_time import preserved,cross,PAST
from test_rouen import leave,board
from test_gym_ui import open_key_item
from test_navigation import wait_task
from key_item_test_helpers import reload
layouts={l.get('id'):l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
def go(e,target):
 group,index,x,y=e.location();groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());name=groups['gMapGroup_Europe'][index];m=json.loads((ROOT/f'data/maps/{name}/map.json').read_text());l=layouts[m['layout']];w,h=l['width'],l['height'];t=struct.unpack('<%dH'%(w*h),(ROOT/l['blockdata_filepath']).read_bytes());blocked={(v['x'],v['y']) for v in m['object_events']+m['warp_events']+m['coord_events']}
 primary='building' if l['primary_tileset']=='gTileset_Building' else 'general';secondary='europe_amiens';attrs=(ROOT/f'data/tilesets/primary/{primary}/metatile_attributes.bin').read_bytes()+(ROOT/f'data/tilesets/secondary/{secondary}/metatile_attributes.bin').read_bytes()
 def valid(p):
  xx,yy=p
  if not(0<=xx<w and 0<=yy<h) or p in blocked:return False
  v=t[yy*w+xx];return not v&0xc00 and v>>12!=1 and struct.unpack_from('<I',attrs,(v&1023)*4)[0]&511 not in (0x10,0x11,0x12,0x13,0x15,0x19,0x1a,0x1b)
 q=deque([(x,y)]);prev={(x,y):None}
 for_p=[(-1,0,'LEFT'),(1,0,'RIGHT'),(0,-1,'UP'),(0,1,'DOWN')]
 while q and target not in prev:
  p=q.popleft()
  for dx,dy,d in for_p:
   n=(p[0]+dx,p[1]+dy)
   if n not in prev and valid(n):prev[n]=(p,d);q.append(n)
 assert target in prev,(name,target)
 path=[];p=target
 while prev[p]:p,d=prev[p];path.append(d)
 for d in reversed(path):
  before=e.location();e.walk(d,1)
  dx,dy={'LEFT':(-1,0),'RIGHT':(1,0),'UP':(0,-1),'DOWN':(0,1)}[d]
  assert e.location()==(group,index,before[2]+dx,before[3]+dy),(name,'step',d,before,e.location())
 assert e.location()==(group,index,*target),(name,target,e.location())
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def grid(e):
 w=e.read('VMap');base=e.read(e.symbols['VMap']+8);expected=struct.unpack('<2304H',(ROOT/'data/layouts/EuropeAmiensPast/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(36) for x in range(64))==expected

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'rouen-arrival',True);leave(e);assert e.location()==(43,33,10,16);original=preserved(e)[1:],history(e);grid(e)
 for name,left in [('west',30),('east',53)]:
  for x in (left,left+1,left+2):
   go(e,(x,9));e.walk('DOWN',5);assert e.location()==(43,33,x,14)
   e.walk('UP',5);assert e.location()==(43,33,x,9)
  go(e,(left+1,11));e.screenshot(ROOT/f'test-output/amiens-bridge-{name}.png');before=preserved(e),history(e),e.location();e=reload(e,'amiens-bridge-'+name)
  assert (preserved(e),history(e),e.location())==before;grid(e);assert (preserved(e)[1:],history(e))==original
  print(f'PASS: Amiens {name} bridge all three lanes cross both directions; native midstream cold Continue retains exact grid/location/progress',flush=True)
 for y in (6,7):
  go(e,(38,y));e.walk('RIGHT',4);assert e.location()==(43,33,42,y)
  e.walk('LEFT',4);assert e.location()==(43,33,38,y)
 go(e,(40,6));e.screenshot(ROOT/'test-output/amiens-bridge-canal.png');before=preserved(e),history(e),e.location();e=reload(e,'amiens-bridge-canal')
 assert (preserved(e),history(e),e.location())==before;grid(e);assert (preserved(e)[1:],history(e))==original
 print('PASS: canal bridge both lanes cross both directions and cold Continue retains grid/location/progress',flush=True)
 for x,y,d,label in [(50,24,'UP','cathedral'),(35,9,'UP','saint-leu'),(45,14,'UP','somme')]:
  go(e,(x,y));e.press(d);before=preserved(e),history(e),e.location();e.press('A',900);assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/amiens-bridge-sign-{label}.png');e.finish_dialogue();assert (preserved(e),history(e),e.location())==before
 open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapPast',1)==1 and e.read('sEuropeMapCurrent',1)==4
 e.screenshot(ROOT/'test-output/amiens-bridge-map.png')
 for _ in range(4):e.press('B',180)
 assert not e.read('sLockFieldControls',1) and (preserved(e)[1:],history(e))==original
 print('PASS: all three historical landmark signs and era map remain readable/read-only with clean field controls',flush=True)
 go(e,(10,16));board(e);leave(e);assert e.location()==(43,33,10,16);grid(e);assert (preserved(e)[1:],history(e))==original
 e=reload(e,'amiens-bridges-return-ready');cross(e);assert e.location()==(43,17,15,24)
 assert (preserved(e)[1:],history(e))==original
 e=reload(e,'amiens-bridges-complete');assert e.location()==(43,17,15,24) and (preserved(e)[1:],history(e))==original
 print('PASS: Rouen train round trip and saved Celebi return retain all existing historical/story/party/item progress',flush=True)
except Exception:
 e.screenshot(ROOT/'test-output/amiens-bridge-failure.png');raise
finally:e.close()
