"""Historical bridge lanes and earned story/return paths through native controls."""
import json,struct
from collections import deque
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_time import preserved,cross,PAST
from test_le_havre import captain,clerk
from test_gym_ui import open_key_item
from test_navigation import wait_task
from key_item_test_helpers import reload
layouts={l.get('id'):l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
def go(e,target):
 group,index,x,y=e.location();groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());name=groups['gMapGroup_Europe'][index];m=json.loads((ROOT/f'data/maps/{name}/map.json').read_text());l=layouts[m['layout']];w,h=l['width'],l['height'];t=struct.unpack('<%dH'%(w*h),(ROOT/l['blockdata_filepath']).read_bytes());blocked={(v['x'],v['y']) for v in m['object_events']+m['warp_events']+m['coord_events']}
 primary='building' if l['primary_tileset']=='gTileset_Building' else 'general';secondary='europe_lehavrepast';attrs=(ROOT/f'data/tilesets/primary/{primary}/metatile_attributes.bin').read_bytes()+(ROOT/f'data/tilesets/secondary/{secondary}/metatile_attributes.bin').read_bytes()
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
 w=e.read('VMap');base=e.read(e.symbols['VMap']+8);expected=struct.unpack('<2560H',(ROOT/'data/layouts/EuropeLeHavrePast/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(40) for x in range(64))==expected

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'le-havre-complete',True);assert e.location()==(43,35,8,5) and e.var(0x40DB)==2;original=preserved(e)[1:],history(e);grid(e)
 for name,start,stop,top in [('roy',38,45,18),('south',40,44,29)]:
  for y in (top,top+1):
   go(e,(start,y));e.walk('RIGHT',stop-start);assert e.location()==(43,35,stop,y)
   e.walk('LEFT',stop-start);assert e.location()==(43,35,start,y)
  go(e,((start+stop)//2,top));e.screenshot(ROOT/f'test-output/havre-bridge-{name}.png');before=preserved(e),history(e),e.location();e=reload(e,'havre-bridge-'+name)
  assert (preserved(e),history(e),e.location())==before;grid(e);assert (preserved(e)[1:],history(e))==original
  print(f'PASS: Le Havre {name} crossing both lanes cross both directions; native midstream cold Continue retains exact grid/location/progress',flush=True)
 for x,y,d,label in [(34,28,'UP','church'),(56,29,'UP','house'),(45,13,'UP','commerce'),(46,22,'UP','roy')]:
  go(e,(x,y));e.press(d);before=preserved(e),history(e),e.location();e.press('A',900);assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/havre-bridge-sign-{label}.png');e.finish_dialogue();assert (preserved(e),history(e),e.location())==before
 open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapPast',1)==1 and e.read('sEuropeMapCurrent',1)==4
 e.screenshot(ROOT/'test-output/havre-bridge-map.png')
 for _ in range(4):e.press('B',180)
 assert not e.read('sLockFieldControls',1) and (preserved(e)[1:],history(e))==original
 print('PASS: four historical landmark signs and era map remain readable/read-only with clean field controls',flush=True)
 go(e,(8,5));captain(e,'YES');clerk(e);assert e.location()==(43,35,8,5);grid(e);assert (preserved(e)[1:],history(e))==original
 e=reload(e,'havre-bridges-return-ready');cross(e);assert e.location()==(43,17,15,24)
 assert (preserved(e)[1:],history(e))==original
 e=reload(e,'havre-bridges-complete');assert e.location()==(43,17,15,24) and (preserved(e)[1:],history(e))==original
 print('PASS: Rouen transport round trip and saved Celebi return retain all existing historical/story/party/item progress',flush=True)
except Exception:
 e.screenshot(ROOT/'test-output/havre-bridge-failure.png');raise
finally:e.close()
