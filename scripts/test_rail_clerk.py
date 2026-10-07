"""Old-battery clerk menus, preview cancellation and saved transfer decisions."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,STORY
from test_landmark_cases import go
from test_country import wait_menu
from test_time import preserved
from rail_test_helpers import BOOKING,choose_destination,board,route,finish_saved_journey
VARS=(STORY,0x40ef,0x40f0,*range(0x40f2,0x4100))
def without_booking(value):
 value=list(value);vars=list(value[2]);vars[VARS.index(BOOKING)]=0;value[2]=tuple(vars);return tuple(value)
def done(e,origin,before):
 e.finish_dialogue();assert e.location()==(43,origin*4+2,7,7) and preserved(e)==before and not e.read('sLockFieldControls',1) and e.var(BOOKING)==0

for origin,checkpoint in enumerate(['start-england','start-france','start-germany','oxford-arrival','chantilly-arrival','oranienburg-arrival']):
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,checkpoint,True);assert e.var(BOOKING)==0
  go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1);go(e,(7,7));before=preserved(e)
  e.press('UP');e.press('A',900);assert e.read('sLockFieldControls',1);e.screenshot(ROOT/f'test-output/rail-clerk-welcome-{origin}-0.png')
  e.press('A',900);assert e.read('sLockFieldControls',1);e.screenshot(ROOT/f'test-output/rail-clerk-welcome-{origin}-1.png')
  wait_menu(e,'Task_MultichoiceMenu_HandleInput');menu=ROOT/f'test-output/rail-clerk-menu-{origin}.state';e.state(menu)
  e.press('B',180);done(e,origin,before)
  e.state(menu,True)
  for _ in range(6):e.press('DOWN')
  e.press('A',180);done(e,origin,before)
  e.state(menu,True)
  for _ in range(origin):e.press('DOWN')
  e.press('A',900);e.screenshot(ROOT/f'test-output/rail-clerk-already-{origin}.png');done(e,origin,before)
  destination=5 if origin!=5 else 3
  for decline in ['B','NO']:
   e.state(menu,True);choose_destination(e,destination)
   assert e.read('gSpecialVar_0x8005',2)==destination and e.read('gSpecialVar_0x8006',2)==route(origin,destination)[0]
   assert e.read('gStringVar3',1)==0xa1+len(route(origin,destination))
   e.screenshot(ROOT/f'test-output/rail-clerk-preview-{origin}-{decline}.png')
   if decline=='B':e.press('B',180)
   else:e.press('DOWN');e.press('A',180)
   done(e,origin,before)
  print('PASS: station '+str(origin)+' old battery B/Exit/same-station and No/B preview preserve party, money, inventory, progress and location',flush=True)
 finally:e.close()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'rail-clerk-transfer-v104',True);assert e.location()==(43,2,4,7) and e.var(BOOKING)==6
 go(e,(7,7));before=preserved(e);e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput')
 state=ROOT/'test-output/rail-clerk-resume.state';e.state(state)
 for decision in ['B','NO','YES']:
  e.state(state,True);e.press('B',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.screenshot(ROOT/f'test-output/rail-clerk-cancel-{decision}.png')
  if decision=='B':e.press('B',180)
  else:
   if decision=='NO':e.press('DOWN')
   e.press('A',180)
  e.finish_dialogue();assert e.location()==(43,2,7,7) and not e.read('sLockFieldControls',1)
  assert e.var(BOOKING)==(0 if decision=='YES' else 6)
  assert without_booking(preserved(e))==without_booking(before)
 print('PASS: genuine v1.04 saved transfer retains booking on No/B and clears it only on confirmed cancellation',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'rail-clerk-transfer-v104',True);before=without_booking(preserved(e))[1:]
 finish_saved_journey(e);assert e.location()==(43,22,4,7) and e.var(BOOKING)==0
 assert without_booking(preserved(e))[1:]==before
 e.screenshot(ROOT/'test-output/rail-clerk-completed.png');e.walk('DOWN',2);e.frames(180);assert e.location()==(43,20,23,10)
 print('PASS: v1.04 London transfer continues via Paris/Berlin to Oranienburg, clears booking and retains progress/home country',flush=True)
finally:e.close()
