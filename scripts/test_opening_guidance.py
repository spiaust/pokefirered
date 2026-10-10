"""Use map board and opening Tour lead from three untouched country batteries."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from test_tour import travel,item_count
from test_tour_journal import inspect
from key_item_test_helpers import reload
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
e=Emulator(ROOT/'pokefirered.gba')
try:
 for dest,country in enumerate(['england','france','germany']):
  load_checkpoint(e,'start-'+country+'-0',True)
  assert e.location()==(43,dest*4,15,14) and e.var(0x40F0)==dest+1
  original=history(e);go(e,(19,12));before=preserved(e)[:2]
  e.press('UP');e.press('A',900)
  for _ in range(20):
   if e.task_active('Task_EuropeMap'):break
   e.press('A',180)
  assert e.task_active('Task_EuropeMap')
  e.press('B',180);e.frames(180);e.finish_dialogue()
  bag=e.read('gSaveBlock1Ptr')+0x3B8
  assert sum(e.read(bag+i*4,2)==361 for i in range(30))==1
  assert history(e)==original and preserved(e)[:2]==before
  inspect(e,0,'opening-'+country)
  print(f'PASS: {country} starting city board supplies Town Map and Europe Tour names Oak without advancing story',flush=True)
  before=preserved(e),history(e),e.location();e=reload(e,'opening-guidance-'+country)
  assert (preserved(e),history(e),e.location())==before
  inspect(e,0,'opening-'+country+'-continued')
  print(f'PASS: {country} native cold Continue retains opening lead, board position and complete starting state',flush=True)
  go(e,(16,14))
  if dest:travel(e,0)
  go(e,(10,14));assert e.location()==(43,0,10,14) and history(e)==original
  e.screenshot(ROOT/f'test-output/opening-guidance-{country}-aide.png')
  print(f'PASS: {country} native route reaches London aide approach without changing initial story progress',flush=True)
finally:e.close()
