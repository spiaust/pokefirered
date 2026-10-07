"""Intermediate guidance, local visit, cold-save exploration and resumed travel."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,STORY
from test_landmark_cases import go,save,talk
from test_time import preserved
from test_country import wait_menu
from rail_test_helpers import BOOKING,speak_from_arrival,board
VARS=(STORY,0x40ef,0x40f0,*range(0x40f2,0x4100))
def without_booking(value):
 value=list(value);vars=list(value[2]);vars[VARS.index(BOOKING)]=0;value[2]=tuple(vars);return tuple(value)

def guidance(e,next_stop,label):
 wait_menu(e,'Task_YesNoMenu_HandleInput');origin=e.location()[1]//4;e.press('A',900)
 assert bytes(e.read(e.symbols['gStringVar1']+i,1) for i in range(12))==bytes([0xbb+ord(c)-65 for c in 'ORANIENBURG']+[255])
 assert e.read('gSpecialVar_0x8006',2)==next_stop
 for page in range(3):
  assert e.read('sLockFieldControls',1) and e.location()==(43,origin*4+2,7,7) and e.var(BOOKING)==6
  e.screenshot(ROOT/f'test-output/rail-explore-{label}-{page}.png')
  if page<2:e.press('A',900)
 e.finish_dialogue();assert e.location()==(43,next_stop*4+2,4,7) and e.var(BOOKING)==6

def notice(e,label):
 go(e,(9,2));before=preserved(e);e.press('UP');e.press('A',900);assert e.read('sLockFieldControls',1)
 e.screenshot(ROOT/f'test-output/rail-explore-{label}-notice.png');e.finish_dialogue();assert preserved(e)==before and e.var(BOOKING)==6

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'rail-clerk-transfer-v104',True);assert e.location()==(43,2,4,7) and e.var(BOOKING)==6;before=without_booking(preserved(e))[1:]
 speak_from_arrival(e);guidance(e,1,'to-paris');notice(e,'paris')
 go(e,(4,7));e.walk('DOWN',2);e.frames(180);assert e.location()==(43,4,23,10)
 talk(e,(55,39),choice='YES');assert e.location()[:2]==(43,50)
 go(e,(2,4));e.press('DOWN');e.press('A',900);assert e.read('sLockFieldControls',1);e.screenshot(ROOT/'test-output/rail-explore-paris-garden.png');e.finish_dialogue();assert e.var(BOOKING)==6
 go(e,(4,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,4,55,39)
 assert without_booking(preserved(e))[1:]==before
 save(e,'rail-explore-paris');saved=preserved(e)
 print('PASS: old saved transfer shows all guidance pages, visits Paris wall notice/garden room and saves outside with booking and progress retained',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'rail-explore-paris',True);assert e.location()==(43,4,55,39) and preserved(e)==saved and e.var(BOOKING)==6
 before=without_booking(preserved(e))[1:]
 go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1);speak_from_arrival(e);guidance(e,2,'to-berlin');notice(e,'berlin')
 go(e,(4,7));speak_from_arrival(e);board(e,5,5);assert e.location()==(43,22,4,7) and e.var(BOOKING)==0
 assert without_booking(preserved(e))[1:]==before
 e.screenshot(ROOT/'test-output/rail-explore-final-arrival.png');e.walk('DOWN',2);e.frames(180);assert e.location()==(43,20,23,10)
 print('PASS: cold Continue after Paris exploration resumes via Berlin, reaches Oranienburg, clears booking and retains quest state/home country',flush=True)
finally:e.close()
