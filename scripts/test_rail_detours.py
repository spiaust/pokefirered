"""Retained bookings recalculate after real walking detours to branch towns."""
import sys
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,STORY
from test_landmark_cases import go,save
from test_time import preserved
from test_country import wait_menu
from rail_test_helpers import BOOKING,speak_from_arrival,board,route
from test_oxford import walk_to_oxford
from test_chantilly import walk_to_chantilly
VARS=(STORY,0x40ef,0x40f0,*range(0x40f2,0x4100))
def without_booking(value):
 value=list(value);variables=list(value[2]);variables[VARS.index(BOOKING)]=0;value[2]=tuple(variables);return tuple(value)
CASES=[('oxford','rail-clerk-transfer-v104',0,3,walk_to_oxford),('chantilly','rail-explore-paris',1,4,walk_to_chantilly)]
if '--prepare' in sys.argv:
 for tag,checkpoint,capital,branch,walk in CASES:
  e=Emulator(ROOT/'artifacts/releases/Pokemon-European-Tour-v1.08.gba')
  try:
   load_checkpoint(e,checkpoint,True);assert e.var(BOOKING)==6;before=preserved(e)[1:]
   if capital==0:e.walk('DOWN',2);e.frames(180)
   go(e,(15,14));walk(e);assert e.var(BOOKING)==6 and preserved(e)[1:]==before
   go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1);go(e,(7,7))
   assert e.location()==(43,branch*4+2,7,7)
   save(e,'rail-detour-'+tag+'-v108')
   print('Prepared genuine v1.08 booked detour: '+tag,flush=True)
  finally:e.close()
else:
 for tag,checkpoint,capital,branch,walk in CASES:
  e=Emulator(ROOT/'pokefirered.gba')
  try:
   load_checkpoint(e,'rail-detour-'+tag+'-v108',True)
   assert e.var(BOOKING)==6 and e.location()==(43,branch*4+2,7,7)
   before=preserved(e);e.press('UP');e.press('A',900)
   for page in range(3):
    assert preserved(e)==before and e.read('sLockFieldControls',1)
    assert e.read('gSpecialVar_0x8006',2)==capital
    assert e.read('gStringVar3',1)==0xa1+len(route(branch,5))
    e.screenshot(ROOT/f'test-output/rail-detour-{tag}-{page}.png')
    if page<2:e.press('A',900)
   wait_menu(e,'Task_YesNoMenu_HandleInput');state=ROOT/f'test-output/rail-detour-{tag}.state';e.state(state)
   e.press('B',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('DOWN');e.press('A',180);e.finish_dialogue()
   assert preserved(e)==before and e.location()==(43,branch*4+2,7,7) and not e.read('sLockFieldControls',1)
   print('PASS: '+tag+' old walking detour recalculates next stop and remaining trains; keeping booking preserves exact state',flush=True)
   e.state(state,True);board(e,capital,5);assert e.var(BOOKING)==6
   go(e,(7,7));save(e,'rail-detour-'+tag+'-rejoined');saved=preserved(e)
  finally:e.close()
  e=Emulator(ROOT/'pokefirered.gba')
  try:
   load_checkpoint(e,'rail-detour-'+tag+'-rejoined',True);assert preserved(e)==saved and e.var(BOOKING)==6
   before=without_booking(preserved(e))[1:]
   e.press('UP');e.press('A',180)
   for index,next_stop in enumerate(route(capital,5)):
    if index:speak_from_arrival(e)
    board(e,next_stop,5)
   # Only the saved booking changes during onward rail travel.
   assert e.var(BOOKING)==0 and e.location()==(43,22,4,7)
   assert without_booking(preserved(e))[1:]==before
   e.screenshot(ROOT/f'test-output/rail-detour-{tag}-final.png')
   print('PASS: '+tag+' detour rejoins the main line, cold Continues and completes at Oranienburg without a stale booking',flush=True)
  finally:e.close()
