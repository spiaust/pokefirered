"""Normally deliver the care parcel and unlock repeatable free rest."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,visit_forest
from test_time import preserved,cross
from test_evac import RECEPTION,return_service,board_train,host
from test_relief import RELIEF,to_reception,host_choice,host_prompt,rest,assert_healed
from test_country import wait_menu
from test_departure import dispatcher
from key_item_test_helpers import reload

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/relief-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'message-directions-claimed',True);assert e.var(RELIEF)==0 and e.var(0x40E4)==4
 visit_forest(e);to_reception(e);before=preserved(e)
 for choice in ['B','NO']:host_choice(e,choice);assert e.var(RELIEF)==0 and preserved(e)==before
 host_prompt(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);pages(e,3,'accepted');e.walk('DOWN',2)
 assert e.var(RELIEF)==1;e=reload(e,'relief-directions-active');host(e);assert e.var(RELIEF)==1
 print('PASS: normal return to Beauvais unlocks optional relief offer; No/B preserve unaccepted task, Yes shows three route pages, and repeats/cold Continue retain the request',flush=True)
 return_service(e);before=preserved(e);e.walk('RIGHT',3);e.walk('UP',3);e.press('UP');e.press('A',180)
 for _ in range(50):
  if e.var(RELIEF)==2:break
  e.press('A',90)
 assert e.var(RELIEF)==2;pages(e,2,'parcel');e.walk('DOWN',3);e.walk('LEFT',3);assert preserved(e)==before
 e=reload(e,'relief-directions-parcel');dispatcher(e);assert e.var(RELIEF)==2 and preserved(e)==before
 print('PASS: native south return service reaches the named dispatcher; actual parcel collection shows two boarding/host pages and survives repeats/cold Continue without Bag or money changes',flush=True)
 board_train(e);host(e);assert e.var(RELIEF)==3
 before=preserved(e)
 for choice in ['B','NO']:host_choice(e,choice);assert preserved(e)==before and e.var(RELIEF)==3
 e=reload(e,'relief-directions-unlocked');rest(e);assert_healed(e)
 healed=preserved(e);rest(e);assert preserved(e)==healed
 e=reload(e,'relief-directions-rested');assert_healed(e);assert preserved(e)==healed
 print('PASS: real boarding and host delivery unlock care corner; optional rest declines, native free full HP/PP care, repeats and cold Continue retain completed relief without duplicate rewards',flush=True)
finally:e.close()
