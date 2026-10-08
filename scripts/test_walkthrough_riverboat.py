"""Both riverboat directions and mounted boarding after full completion."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_ferry import captain,sail
from test_country import wait_menu
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved

def decline(e):
 for choice in ['B','NO']:
  location=e.location();before=preserved(e);captain(e)
  wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();assert e.location()==location and preserved(e)==before
def reload(e,name,location):
 save(e,name);saved=preserved(e);e.close();e=Emulator(ROOT/'pokefirered.gba')
 load_checkpoint(e,name,True);assert preserved(e)==saved and e.location()==location
 return e

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'walkthrough-coast-complete',True);original=preserved(e)[1:]
 cases=tuple(e.var(v) for v in range(0x40C0,0x40C3))
 go(e,(24,16));before=preserved(e);sail(e,0);assert preserved(e)==before
 # Start the checked round trip in London, then return from Oxford.
 for origin,destination,selection in [(0,12,3),(12,0,0)]:
  assert e.location()==(43,origin,24,16);decline(e)
  before=preserved(e);sail(e,destination);assert preserved(e)==before
  e.screenshot(ROOT/f'test-output/walkthrough-riverboat-{origin}-to-{destination}.png')
  print('PASS: '+str(origin)+' to '+str(destination)+' captain No/B declines and free riverboat retain exact party/inventory/progress',flush=True)
  e=reload(e,'walkthrough-riverboat-'+str(destination),(43,destination,24,16))
  before=preserved(e);open_key_item(e,361);wait_task(e,'Task_EuropeMap')
  assert e.read('sEuropeMapCurrent',1)==selection and not e.read('sEuropeMapPast',1)
  e.screenshot(ROOT/f'test-output/walkthrough-riverboat-{destination}-map.png')
  e.press('B',180);e.press('B',180);e.press('B',90);assert preserved(e)==before
  e.walk('UP',1);e.walk('DOWN',1);assert e.location()==(43,destination,24,16)
  assert preserved(e)[1:]==original
  print('PASS: '+str(destination)+' landing cold Continues with exact state, correct city map and controllable movement',flush=True)
 open_key_item(e,360);e.frames(120);assert e.read('gPlayerAvatar',1)&2
 before=preserved(e);sail(e,12);assert preserved(e)==before
 sail(e,0);e.walk('UP',1);e.walk('DOWN',1)
 assert e.location()==(43,0,24,16) and preserved(e)[1:]==original
 print('PASS: Bicycle boarding permits free round-trip travel and controllable landing with rewards/progress intact',flush=True)
 sail(e,12);go(e,(18,14));e=reload(e,'walkthrough-riverboat-complete',(43,12,18,14))
 before=preserved(e);e.press('DOWN');e.press('A',900)
 e.screenshot(ROOT/'test-output/walkthrough-riverboat-ada.png')
 for _ in range(160):
  if not e.read('sLockFieldControls',1):break
  e.press('A',90)
 assert preserved(e)==before and preserved(e)[1:]==original and not e.read('sLockFieldControls',1)
 assert tuple(e.var(v) for v in range(0x40C0,0x40C3))==cases
 print('PASS: final cold Continue retains completed story/cases/stamps and repeatable Ada ending after riverboat trips',flush=True)
finally:e.close()
