"""Repeat modern travel boards with genuine completed accounts and inventory."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved
from key_item_test_helpers import reload
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def board(e,dest):
 before=preserved(e),history(e),e.location()
 e.press('UP');e.press('A',900)
 for _ in range(25):
  if e.task_active('Task_EuropeMap'):break
  e.press('A',180)
 assert e.task_active('Task_EuropeMap')
 assert (e.read('sEuropeMapCurrent',1),e.read('sEuropeMapSelection',1),e.read('sEuropeMapPast',1))==(dest,dest,0)
 e.press('B',180);e.frames(180);e.finish_dialogue()
 assert not e.read('sLockFieldControls',1)
 assert (preserved(e),history(e),e.location())==before
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'completed-board-London',True);original=preserved(e)[1:],history(e)
 for dest,city in enumerate(['London','Paris','Berlin','Oxford','Chantilly','Oranienburg']):
  go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  go(e,(19,12));board(e,dest);board(e,dest)
  print(f'PASS: {city} repeated board opens correct map and retains exact inventory, party, money, story and position',flush=True)
  before=preserved(e),history(e),e.location();e=reload(e,'completed-board-'+city)
  assert (preserved(e),history(e),e.location())==before
  board(e,dest);assert (preserved(e)[1:],history(e))==original
  print(f'PASS: {city} native cold Continue retains completed board state and repeat gifts remain gated',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'completed-boards-complete')
 before=preserved(e),history(e);e.press('DOWN');e.press('A',900);e.finish_dialogue()
 assert (preserved(e),history(e))==before and (preserved(e)[1:],history(e))==original
 print('PASS: saved native Ada return retains all completed activities after six-town board review',flush=True)
finally:e.close()
