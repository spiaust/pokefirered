"""Regional map labels from existing visitor-room battery saves."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved
for checkpoint,country in [('berlin-home-v065',2),('berlin-library-v066',2),('berlin-garden-room-save',2),('eiffel-visitor-save',1)]:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,checkpoint,True);loc=e.location();before=preserved(e)
  open_key_item(e,361);wait_task(e,'Task_EuropeMap')
  assert e.read('sEuropeMapCurrent',1)==country,(checkpoint,e.read('sEuropeMapCurrent',1))
  assert e.read('sEuropeMapSelection',1)==country
  e.screenshot(ROOT/f'test-output/visitor-map-{checkpoint}.png')
  e.press('B',180);e.press('B',180);e.press('B',90)
  assert e.location()==loc and preserved(e)==before
  print('PASS: '+checkpoint+' shows the correct country and returns without changing saved progress',flush=True)
 finally:e.close()
