"""Accept a real study and follow each named route without injected progress."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_france_story import talk,npc
from test_country import wait_menu
from test_time import preserved
from test_trainers import defeated
from test_tour import item_count
from test_tour_journal import inspect
from key_item_test_helpers import reload

def decline_trainer(e):
 e.press('UP');e.press('A',180)
 for _ in range(12):
  if e.task_active('Task_YesNoMenu_HandleInput'):break
  e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'start-england',True);go(e,(10,14))
 assert e.var(0x40FB)==0 and not any(defeated(e,i) for i in [0,3,6])
 before=preserved(e)
 for choice in ['B','NO']:
  npc(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();assert preserved(e)==before
 npc(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',900)
 for page in range(6):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/england-accepted-{page}.png');e.press('A',900)
 e.finish_dialogue();assert e.var(0x40FB)==1 and item_count(e,184)==0
 e=reload(e,'england-accepted');before=preserved(e);talk(e);inspect(e,1,'england-accepted');assert preserved(e)==before
 print('PASS: native B/No decline preserves an unstarted study; Yes shows six accepted pages and saves the active study with the Oliver journal and no reward',flush=True)
 go(e,(15,1));e.walk('UP',2);e.frames(180);assert e.location()==(43,1,15,23),e.location()
 e.walk('UP',4);e.walk('RIGHT',2);assert e.location()==(43,1,17,19)
 before=preserved(e);decline_trainer(e);assert preserved(e)==before and not defeated(e,0) and not e.in_battle()
 e=reload(e,'england-accepted-Oliver');before=preserved(e);decline_trainer(e);assert preserved(e)==before
 print('PASS: north London route reaches Oliver east of the meadow path; optional B decline and cold Continue grant no win or reward',flush=True)
 e.walk('LEFT',2);e.walk('UP',20);e.frames(180);assert e.location()==(43,13,15,39),e.location()
 e.walk('UP',20);e.walk('RIGHT',2);assert e.location()==(43,13,17,19)
 before=preserved(e);decline_trainer(e);assert preserved(e)==before and not defeated(e,3) and not e.in_battle()
 e=reload(e,'england-accepted-Alice');before=preserved(e);decline_trainer(e);assert preserved(e)==before
 print('PASS: continuing north reaches Alice east of Oxford Trail path; optional decline and cold Continue retain both unearned trainer wins',flush=True)
 e.walk('LEFT',2);e.walk('UP',20);e.frames(180);assert e.location()==(43,12,15,23),e.location()
 go(e,(10,14));before=preserved(e);talk(e);assert preserved(e)==before and not defeated(e,6)
 e=reload(e,'england-accepted-rival');talk(e);inspect(e,1,'england-accepted-rival');assert preserved(e)==before and item_count(e,184)==0
 print('PASS: continuing north reaches the rival west of Oxford guide; missing Oliver gate repeats/cold Continues without battle, report or Bell',flush=True)
finally:e.close()
