"""Read active-study reminders and walk to each named trainer normally."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_france_story import talk,npc
from test_country import wait_menu
from test_time import preserved
from test_trainers import defeated
from test_tour import travel,item_count
from test_tour_journal import inspect
from key_item_test_helpers import reload

def decline(e):
 e.press('UP');e.press('A',180)
 for _ in range(12):
  if e.task_active('Task_YesNoMenu_HandleInput'):break
  e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 for label,source,pages,lead in [('aide','england-accepted',5,1),('Oliver','england-accepted-rival',3,1),('Alice','training-intro-London-won',3,2)]:
  load_checkpoint(e,source,True)
  if label=='Alice':
   e.walk('LEFT',2);e.walk('DOWN',5);e.frames(180);go(e,(10,14))
   if e.var(0x40FB)==0:
    npc(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);e.finish_dialogue()
   go(e,(16,14));travel(e,3);go(e,(10,14))
  assert e.var(0x40FB)==1 and item_count(e,184)==0 and not defeated(e,6)
  assert defeated(e,0)==(label=='Alice') and not defeated(e,3)
  before=preserved(e);npc(e);e.frames(900)
  for page in range(pages):
   assert e.read('sLockFieldControls',1)
   e.screenshot(ROOT/f'test-output/england-reminder-{label}-{page}.png');e.press('A',900)
  e.finish_dialogue();talk(e);assert preserved(e)==before
  e=reload(e,f'england-reminder-{label}');talk(e);inspect(e,lead,f'england-reminder-{label}');assert preserved(e)==before
  print(f'PASS: {label} active-study reminder shows all {pages} pages and repeats/cold Continues read-only with correct journal and no report reward',flush=True)
  if label=='aide':
   go(e,(15,1));e.walk('UP',2);e.frames(180);e.walk('UP',4);e.walk('RIGHT',2)
   expected=(43,1,17,19);index=0
  else:
   go(e,(15,23));e.walk('DOWN',1);e.frames(180)
   if label=='Oliver':e.walk('DOWN',40);e.frames(180)
   e.walk('DOWN',19);e.walk('RIGHT',2)
   expected=(43,13 if label=='Alice' else 1,17,19);index=3 if label=='Alice' else 0
  assert e.location()==expected,e.location()
  before=preserved(e);decline(e);assert preserved(e)==before and not defeated(e,index) and not e.in_battle()
  e=reload(e,f'england-reminder-{label}-trainer');before=preserved(e);decline(e);assert preserved(e)==before and item_count(e,184)==0
  print(f'PASS: {label} reminder walking directions reach the required trainer; native B decline and cold Continue grant no trainer win or Bell',flush=True)
finally:e.close()
