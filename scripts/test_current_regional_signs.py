"""Read regional landmark signs and map guidance on an earned completed save."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved
from test_gym_ui import open_key_item
from test_navigation import wait_task
from key_item_test_helpers import reload

DATA=[('Oxford',3,[(41,11,'UP','Radcliffe'),(54,11,'LEFT','Magdalen'),(46,19,'DOWN','Meadow')]),('Chantilly',4,[(53,15,'UP','Chateau'),(42,19,'LEFT','Stables'),(65,14,'UP','Gardens')]),('Oranienburg',5,[(49,12,'UP','Palace'),(39,11,'UP','Park'),(59,16,'LEFT','Havel')])]
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'oranienburg-bridges-complete',True)
 original=preserved(e)[1:],history(e)
 for city,dest,signs in DATA:
  go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  for x,y,d,label in signs:
   go(e,(x,y));e.press(d);before=preserved(e),history(e),e.location()
   e.press('A',180);assert e.read('sLockFieldControls',1)
   e.screenshot(ROOT/f'test-output/current-regional-{city}-{label}.png')
   e.finish_dialogue();assert not e.read('sLockFieldControls',1)
   assert (preserved(e),history(e),e.location())==before
   print(f'PASS: {city} {label} sign reachable, readable and read-only',flush=True)
  before=preserved(e),history(e),e.location()
  open_key_item(e,361);wait_task(e,'Task_EuropeMap')
  assert (e.read('sEuropeMapCurrent',1),e.read('sEuropeMapSelection',1),e.read('sEuropeMapPast',1))==(dest,dest,0)
  e.screenshot(ROOT/f'test-output/current-regional-{city}-map.png')
  e.press('B',180);e.press('B',180);e.press('B',90)
  assert not e.read('sLockFieldControls',1)
  assert (preserved(e),history(e),e.location())==before
  print(f'PASS: {city} map guidance selects correct present-day town and restores walking without changes',flush=True)
  e=reload(e,'current-regional-'+city)
  assert (preserved(e),history(e),e.location())==before
  assert (preserved(e)[1:],history(e))==original
  print(f'PASS: {city} native cold Continue retains sign-path location and completed journey',flush=True)
finally:e.close()
