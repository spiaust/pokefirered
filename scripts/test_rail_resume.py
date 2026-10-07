"""Real saved-trip pages and explicit keep/board choices after cold Continue."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_time import preserved
from test_landmark_cases import go
from test_country import wait_menu
from rail_test_helpers import BOOKING,board

def prompt(e,label):
 go(e,(7,7));before=preserved(e);e.press('UP');e.press('A',900)
 for page in range(3):
  assert e.read('sLockFieldControls',1) and e.var(BOOKING)==6 and e.location()[2:]==(7,7)
  assert preserved(e)==before
  e.screenshot(ROOT/f'test-output/rail-resume-{label}-{page}.png')
  if page<2:e.press('A',900)
 wait_menu(e,'Task_YesNoMenu_HandleInput');return before

for checkpoint,station,next_stop in [('rail-clerk-transfer-v104',2,1),('rail-explore-paris',6,2)]:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,checkpoint,True)
  if station==6:
   go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1)
  assert e.location()[:2]==(43,station) and e.var(BOOKING)==6
  before=prompt(e,str(station));state=ROOT/f'test-output/rail-resume-{station}.state';e.state(state)
  for decline in ['NO','B']:
   e.state(state,True)
   if decline=='NO':e.press('DOWN');e.press('A',180)
   else:e.press('B',180)
   wait_menu(e,'Task_YesNoMenu_HandleInput');assert e.var(BOOKING)==6
   e.screenshot(ROOT/f'test-output/rail-resume-{station}-keep-{decline}.png')
   e.press('DOWN');e.press('A',180);e.finish_dialogue()
   assert preserved(e)==before and e.location()==(43,station,7,7) and not e.read('sLockFieldControls',1)
  e.state(state,True);board(e,next_stop,5)
  assert e.var(BOOKING)==6
  print('PASS: cold saved trip at station '+str(station)+' shows all resume pages, No/B opens cancellation, NO keeps exact state and YES boards the expected next train',flush=True)
 finally:e.close()
