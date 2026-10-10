"""Native regional Places controls, save restoration and final Ada return."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_journal import journal_task
from key_item_test_helpers import reload
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def page(e,city,dest,label):
 before=preserved(e),history(e),e.location()
 open_key_item(e,361);wait_task(e,'Task_EuropeMap');task=journal_task(e)
 assert e.read('sEuropeMapSelection',1)==dest and e.read('sEuropeMapPast',1)==0
 e.press('R',180);assert e.read(task+8+14,2)==1
 e.screenshot(ROOT/f'test-output/regional-services-{city}-{label}.png')
 e.press('L',180);assert e.read('sEuropePlacesRooms',1)==1
 e.screenshot(ROOT/f'test-output/regional-services-{city}-{label}-services.png')
 e.press('L',180);assert e.read('sEuropePlacesRooms',1)==0
 e.press('RIGHT',90);assert e.read('sEuropeMapSelection',1)==(dest+1)%8
 e.press('LEFT',90);assert e.read('sEuropeMapSelection',1)==dest
 e.press('A',180);assert e.read(task+8+14,2)==0
 e.press('R',180);assert e.read(task+8+14,2)==1
 e.press('R',180);assert e.read(task+8+14,2)==0
 e.press('B',180);e.press('B',180);e.press('B',180);e.press('B',180)
 assert not e.read('sLockFieldControls',1)
 assert (preserved(e),history(e),e.location())==before
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'oranienburg-bridges-complete',True);original=preserved(e)[1:],history(e)
 for city,dest in [('Oxford',3),('Chantilly',4),('Oranienburg',5)]:
  go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  page(e,city,dest,'places')
  print(f'PASS: {city} Places/Services toggle, stop browsing, A/R return and B exit retain exact state',flush=True)
  before=preserved(e),history(e),e.location();e=reload(e,'regional-services-'+city)
  assert (preserved(e),history(e),e.location())==before
  page(e,city,dest,'continued');assert (preserved(e)[1:],history(e))==original
  print(f'PASS: {city} cold Continue reopens service directions and retains completed journey',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'regional-services-complete')
 before=preserved(e),history(e);e.press('DOWN');e.press('A',900);e.finish_dialogue()
 assert (preserved(e),history(e))==before and (preserved(e)[1:],history(e))==original
 print('PASS: native return and saved Ada ending preserve all rewards and completed activities',flush=True)
finally:e.close()
