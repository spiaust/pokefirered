"""Follow real notice verification and confirmed news back to the refuge."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_time import ARRIVAL,PAST,preserved,keeper
from test_departure import NEWS,POST,visit_post,notice,dispatcher,back_to_refuge,cancellations
from key_item_test_helpers import reload

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/departure-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'refuge-reminder-complete',True);assert e.location()==ARRIVAL and e.var(PAST)==4 and e.var(NEWS)==0
 visit_post(e);assert e.var(NEWS)==1;before=preserved(e);dispatcher(e);assert preserved(e)==before and e.var(NEWS)==1
 e.walk('RIGHT',6);e.walk('UP',5);e.press('UP');e.press('A',180)
 for _ in range(50):
  if e.var(NEWS)==2:break
  e.press('A',90)
 assert e.var(NEWS)==2;pages(e,2,'noted');assert preserved(e)==before
 e=reload(e,'departure-directions-noted');e.walk('DOWN',5);e.walk('LEFT',6);notice(e);assert e.var(NEWS)==2 and preserved(e)==before
 print('PASS: native guide reaches station post, dispatcher requires notice, and actual notice gives two direction pages; saved notes and repeat reading retain stage 2',flush=True)
 e.walk('RIGHT',3);e.walk('UP',3);e.press('UP');e.press('A',180)
 for _ in range(50):
  if e.var(NEWS)==3:break
  e.press('A',90)
 assert e.var(NEWS)==3;pages(e,3,'carry');assert preserved(e)==before
 e.walk('DOWN',3);e.walk('LEFT',3);e=reload(e,'departure-directions-confirmed');dispatcher(e);assert e.var(NEWS)==3 and preserved(e)==before
 cancellations(e,True);assert e.var(NEWS)==3 and e.location()==POST
 print('PASS: actual dispatcher verification gives three return-direction pages; repeat confirmation, cold Continue and optional return-guide No/B preserve confirmed news',flush=True)
 back_to_refuge(e);keeper(e);assert e.var(NEWS)==4 and e.var(PAST)==4 and preserved(e)[1:]==before[1:]
 completed=preserved(e);keeper(e);assert preserved(e)==completed
 e=reload(e,'departure-directions-reported');keeper(e);assert preserved(e)==completed and e.var(NEWS)==4
 print('PASS: normal return guide and north-of-arrival keeper route deliver the confirmed news; repeats/cold Continue retain completed report without rewards or progress duplication',flush=True)
finally:e.close()
