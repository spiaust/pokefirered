"""Enter landmarks with buttons; investigate, save, resolve and collect once."""
import json,struct,sys
from collections import deque
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_garden import choose
from test_time import preserved
from test_gym_ui import start_action,open_key_item
from test_navigation import wait_task
from test_country import wait_menu,party_species
DATA=[('NotreDame','Paris','france',4,38,(28,35),0x40c0,1),('Westminster','London','england',0,39,(14,35),0x40c1,0),('Reichstag','Berlin','germany',8,40,(21,33),0x40c2,2)]
layouts={l.get('id'):l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
def go(e,target):
 group,index,x,y=e.location();groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());name=groups['gMapGroup_Europe'][index];m=json.loads((ROOT/f'data/maps/{name}/map.json').read_text());l=layouts[m['layout']];w,h=l['width'],l['height'];t=struct.unpack('<%dH'%(w*h),(ROOT/l['blockdata_filepath']).read_bytes());blocked={(v['x'],v['y']) for v in m['object_events']+m['warp_events']+m['coord_events']}
 primary='building' if l['primary_tileset']=='gTileset_Building' else 'general';secondary='pokemon_tower' if primary=='building' else 'europe_'+name[6:].lower();attrs=(ROOT/f'data/tilesets/primary/{primary}/metatile_attributes.bin').read_bytes()+(ROOT/f'data/tilesets/secondary/{secondary}/metatile_attributes.bin').read_bytes()
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
def talk(e,point,d='UP',choice=None):
 go(e,point);e.press(d);e.press('A',180)
 if choice is not None:choose(e,choice)
 else:e.finish_dialogue()
def save(e,name):
 start_action(e,4)
 for _ in range(5):e.press('A',150)
 e.battery(ROOT/f'test-output/{name}.sav')
 e.press('B',180);e.press('B',180);e.frames(90)
def run(row):
 tag,city,country,index,inside,door,var,selection=row;name='case-'+tag.lower();e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'start-'+country,True);assert e.var(var)==0
  before=preserved(e)[1:];go(e,door)
  for choice in ['NO','B']:
   talk(e,door,choice=choice);assert e.location()==(43,index,*door) and e.var(var)==0
  talk(e,door,choice='YES');assert e.location()==(43,inside,10,15)
  e.screenshot(ROOT/f'test-output/{name}-interior.png')
  talk(e,(10,5));assert e.var(var)==0
  talk(e,(8,15),choice='NO');assert e.var(var)==0
  talk(e,(8,15),choice='YES');assert e.var(var)==1
  talk(e,(15,8));assert e.var(var)==3
  talk(e,(15,8));assert e.var(var)==3
  talk(e,(4,6));assert e.var(var)==4
  assert preserved(e)[1:]==before
  save(e,name+'-clues');saved=preserved(e)
 finally:e.close()
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,name+'-clues',True);assert e.var(var)==4 and preserved(e)==saved
  open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapCurrent',1)==selection and not e.read('sEuropeMapPast',1)
  e.press('B',180);e.press('B',180);e.press('B',90)
  talk(e,(10,5),choice='NO');assert e.var(var)==4
  talk(e,(10,5),choice='YES');assert e.var(var)==5
  save(e,name+'-resolved')
  talk(e,(8,15));assert e.var(var)==6
  before=preserved(e);talk(e,(8,15));assert preserved(e)==before
  talk(e,(12,14),'DOWN');assert preserved(e)==before
  save(e,name+'-complete');e.screenshot(ROOT/f'test-output/{name}-complete.png')
  go(e,(10,15));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,index,*door),e.location()
  talk(e,door,choice='YES');assert e.var(var)==6 and e.location()==(43,inside,10,15)
  print(f'PASS: {tag} door No/B, clues in reverse order, peaceful resolution, one-time reward, ledger and exit/re-entry',flush=True)
 finally:e.close()
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,name+'-complete',True);assert e.var(var)==6 and e.location()[:2]==(43,inside)
  print(f'PASS: {tag} cold saves retain clues/completion, inventory and correct present-day map anchor',flush=True)
 finally:e.close()
if __name__=='__main__':
 for row in DATA:
  if not sys.argv[1:] or row[0] in sys.argv[1:]:run(row)
