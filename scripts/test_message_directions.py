"""Carry Elise's message, return a reply and report to Ada normally."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,return_to_ada,report
from test_message import MESSAGE,offer,to_keeper,to_elise,luxury_balls
from test_evac import RECEPTION,elise
from test_time import preserved,keeper,cross
from key_item_test_helpers import reload

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/message-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'beauvais-directions-checked-in',True);assert e.location()==RECEPTION and e.var(MESSAGE)==0
 before=preserved(e);balls=luxury_balls(e)
 for choice in ['B','NO']:
  offer(e)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();e.walk('LEFT',3);assert preserved(e)==before and e.var(MESSAGE)==0
 offer(e);e.press('A',180);pages(e,3,'delivery');e.walk('LEFT',3);assert e.var(MESSAGE)==1
 e=reload(e,'message-directions-active');elise(e);assert e.var(MESSAGE)==1 and luxury_balls(e)==balls
 print('PASS: optional Elise No/B preserves unaccepted message; real acceptance shows three delivery pages, repeats and cold Continues with no early reward',flush=True)
 to_keeper(e);e.walk('UP',3);e.press('UP');e.press('A',180)
 for _ in range(50):
  if e.var(MESSAGE)==2:break
  e.press('A',90)
 assert e.var(MESSAGE)==2;pages(e,4,'reply');e.walk('DOWN',3)
 e=reload(e,'message-directions-reply');keeper(e);assert e.var(MESSAGE)==2 and luxury_balls(e)==balls
 print('PASS: normal return service and guide deliver message to keeper; four reply-route pages, repeats and cold Continue preserve undelivered reply',flush=True)
 to_elise(e);e.walk('RIGHT',3);e.press('UP');e.press('A',180)
 for _ in range(80):
  if e.var(MESSAGE)==3:break
  e.press('A',90)
 assert e.var(MESSAGE)==3;pages(e,3,'account');e.walk('LEFT',3)
 e=reload(e,'message-directions-account');elise(e);assert e.var(MESSAGE)==3 and luxury_balls(e)==balls
 print('PASS: actual station-post boarding returns keeper reply to Elise; three Ada-return pages, repeated conversation and cold Continue retain the report without an early Ball',flush=True)
 cross(e);return_to_ada(e);report(e);assert e.var(MESSAGE)==4 and luxury_balls(e)==balls+1
 claimed=preserved(e);report(e);e=reload(e,'message-directions-claimed');report(e);assert preserved(e)==claimed
 print('PASS: native Celebi return and Oxford train reach Ada; account grants one Luxury Ball, with repeats/cold Continue preserving the claimed reward',flush=True)
finally:e.close()
