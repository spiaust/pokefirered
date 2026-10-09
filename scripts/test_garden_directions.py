"""Find Pidgey, reunite with Luc, and follow normal onward travel."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_evac import return_service
from test_garden import STORY,GARDEN,enter,leave,luc,visible,home_bird
from test_amiens import board
from test_time import preserved
from key_item_test_helpers import reload

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/garden-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'relief-directions-rested',True);assert e.var(STORY)==0 and e.var(0x40E3)==3
 before=preserved(e)
 for choice in ['B','NO']:enter(e,choice);assert e.var(STORY)==0 and preserved(e)==before
 enter(e);assert e.location()==GARDEN
 for choice in ['B','NO']:luc(e,choice);assert e.var(STORY)==0
 luc(e);assert e.var(STORY)==1 and not visible(e,5)
 e=reload(e,'garden-directions-active');luc(e);assert e.var(STORY)==1
 print('PASS: optional garden and Luc No/B choices preserve unaccepted search; real acceptance and cold Continue retain active request and the wild Pidgey object',flush=True)
 e.walk('RIGHT',7);e.walk('UP',10);assert visible(e,4);e.press('UP');e.press('A',180)
 for _ in range(50):
  if e.var(STORY)==2:break
  e.press('A',90)
 assert e.var(STORY)==2;pages(e,2,'carry');assert not visible(e,4) and not visible(e,5)
 e.walk('DOWN',10);e.walk('LEFT',7);e=reload(e,'garden-directions-found');assert e.var(STORY)==2 and not visible(e,4) and not visible(e,5)
 print('PASS: actual northeast Pidgey interaction shows two Luc-return pages; saved carrying stage removes the tree bird without prematurely showing the reunited bird',flush=True)
 e.walk('UP',1);e.walk('LEFT',4);e.walk('UP',6);e.press('UP');e.press('A',180)
 for _ in range(50):
  if e.var(STORY)==3:break
  e.press('A',90)
 assert e.var(STORY)==3;pages(e,4,'onward');assert visible(e,5) and not visible(e,4)
 e.walk('DOWN',6);e.walk('RIGHT',4);e.walk('DOWN',1);home_bird(e)
 e=reload(e,'garden-directions-reunited');luc(e);home_bird(e);assert e.var(STORY)==3 and not visible(e,4)
 print('PASS: native return to Luc reunites Pidgey and shows four onward pages; repeat talks, bird interaction and cold Continue retain the correct reunited object',flush=True)
 leave(e);return_service(e);before=preserved(e)
 for choice in ['B','NO']:board(e,choice);assert e.var(0x40E1)==0 and preserved(e)[1:]==before[1:]
 e=reload(e,'garden-directions-amiens-offer');board(e,'B');assert e.var(STORY)==3 and e.var(0x40E1)==0
 print('PASS: south garden guide and reception return service reach the named dispatcher; optional Amiens No/B and cold Continue preserve reunion without forced onward travel',flush=True)
finally:e.close()
