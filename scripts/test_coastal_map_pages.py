"""Visit modern port scenery using native travel on an earned completed save."""
import json,struct
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_coast import coach,prompt,accept,crossing,leave_port
from test_time import preserved
from test_gym_ui import open_key_item
from test_navigation import wait_task
from key_item_test_helpers import reload
from test_journal import journal_task
DATA=[('Dover',0,27,[(45,9),(48,13),(53,17),(35,23),(35,32)],[(44,13,'UP','Castle'),(52,18,'RIGHT','Cliffs'),(29,23,'UP','Seafront')]),('Calais',1,28,[(37,30),(45,16),(35,10),(51,7),(27,27)],[(40,31,'UP','Hall'),(47,17,'UP','Lighthouse'),(30,12,'UP','Seafront')])]
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def grid(e,city):
 layouts=json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']
 l=next(v for v in layouts if v.get('id')==f'LAYOUT_EUROPE_{city.upper()}_PORT')
 w,h=l['width'],l['height'];expected=struct.unpack('<%dH'%(w*h),(ROOT/l['blockdata_filepath']).read_bytes())
 width=e.read('VMap');base=e.read(e.symbols['VMap']+8)
 assert tuple(e.read(base+2*((y+7)*width+x+7),2) for y in range(h) for x in range(w))==expected
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'regional-map-complete',True);original=preserved(e)[1:],history(e)
 for city,dest,port,points,signs in DATA:
  go(e,(16,14));travel(e,dest);coach(e);prompt(e);accept(e,port);grid(e,city)
  e.walk('UP',2);assert e.location()==(43,port,8,3)
  for point in points:go(e,point)
  assert (preserved(e)[1:],history(e))==original
  print(f'PASS: {city} native coach arrival, quay access and five landmark paths retain completed progress and authored map',flush=True)
  for x,y,d,label in signs:
   go(e,(x,y));e.press(d);before=preserved(e),history(e),e.location()
   e.press('A',900);assert e.read('sLockFieldControls',1)
   e.screenshot(ROOT/f'test-output/coastal-map-{city}-{label}.png')
   e.finish_dialogue();assert not e.read('sLockFieldControls',1)
   assert (preserved(e),history(e),e.location())==before
   print(f'PASS: {city} {label} sign reachable, readable and read-only',flush=True)
  go(e,points[0]);before=preserved(e),history(e),e.location()
  e=reload(e,'coastal-map-'+city);grid(e,city)
  assert (preserved(e),history(e),e.location())==before
  open_key_item(e,361);wait_task(e,'Task_EuropeMap')
  assert (e.read('sEuropeMapCurrent',1),e.read('sEuropeMapSelection',1),e.read('sEuropeMapPast',1))==(port-21,port-21,0)
  task=journal_task(e);e.press('R',180);assert e.read(task+22,2)==1
  e.screenshot(ROOT/f'test-output/coastal-map-{city}-places.png')
  e.press('RIGHT',90);assert e.read('sEuropeMapSelection',1)==(port-20)%8
  e.press('LEFT',90);assert e.read('sEuropeMapSelection',1)==port-21
  e.press('A',180);assert e.read(task+22,2)==0
  e.press('R',180);assert e.read(task+22,2)==1
  e.press('R',180);assert e.read(task+22,2)==0
  e.press('B',180);e.press('B',180);e.press('B',180);e.press('B',180)
  assert not e.read('sLockFieldControls',1)
  assert (preserved(e),history(e),e.location())==before
  print(f'PASS: {city} district cold Continue restores exact position/state/tiles and new Places guidance, browsing and A/R/B controls',flush=True)
  go(e,(8,5));crossing(e);crossing(e);grid(e,city);leave_port(e)
  assert e.location()==(43,dest*4,23,10) and (preserved(e)[1:],history(e))==original
  print(f'PASS: {city} native ferry round trip and north capital exit retain all completed activities',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'coastal-map-complete')
 before=preserved(e),history(e);e.press('DOWN');e.press('A',900);e.finish_dialogue()
 assert (preserved(e),history(e))==before and (preserved(e)[1:],history(e))==original
 print('PASS: saved native Ada return retains sightseeing journey and repeatable ending',flush=True)
except Exception:
 e.screenshot(ROOT/'test-output/coastal-map-failure.png')
 raise
finally:e.close()
