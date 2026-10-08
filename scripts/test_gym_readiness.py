"""Follow locked Gym directions before and after report-ready story stages."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from test_tour import travel,item_count
from test_country import wait_menu
from test_trainers import defeated
from test_germany_story import leave_gym
from key_item_test_helpers import reload
import test_oxford_gym as rock
import test_chantilly_gym as water
import test_oranienburg_gym as electric

def approach(e,index):
 go(e,(15,10));e.walk('UP',1);e.frames(180)
 if index==1:water.approach(e)
 else:e.walk('UP',8)

def locked(e,gym,city,index,label):
 before=preserved(e);gym.leader(e);e.frames(900)
 for page in range(5 if index==1 else 4):
  assert e.read('sLockFieldControls',1) and not e.in_battle()
  e.screenshot(ROOT/f'test-output/gym-ready-{city}-{label}-{page}.png')
  e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before
 assert not gym.badge(e) and not defeated(e,index+7) and not e.task_active('Task_YesNoMenu_HandleInput')

def capital(e,index):
 if index==1:leave_gym(e)
 else:e.walk('DOWN',10);e.frames(180)
 go(e,(16,14));travel(e,index);go(e,(10,14))

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,(city,gym,source,var,stage,reward) in enumerate([
  ('Oxford',rock,'story-report-ready',0x40FB,1,184),
  ('Chantilly',water,'france-report',0x40FD,5,205),
  ('Oranienburg',electric,'germany-report',0x40FF,2,208)]):
  load_checkpoint(e,'training-recovery-London-healed',True)
  e.walk('DOWN',5);e.frames(180);go(e,(16,14));travel(e,index+3);approach(e,index)
  locked(e,gym,city,index,'unstarted');e=reload(e,f'gym-ready-{city}-unstarted');locked(e,gym,city,index,'continued')
  baseline=preserved(e)[1:];capital(e,index)
  # The named contact is approachable. The first offer can be declined;
  # later country contacts correctly retain their prior-badge requirements.
  e.press('DOWN');e.press('A',180)
  if index==0:
   wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180)
  e.finish_dialogue();assert preserved(e)[1:]==baseline
  print(f'PASS: {city} unstarted Gym remains locked through Continue; exit and east-side station reach the named capital/contact without advancing story',flush=True)
  load_checkpoint(e,source,True);assert e.var(var)==stage
  go(e,(16,14));travel(e,index+3);approach(e,index)
  locked(e,gym,city,index,'report-ready');e=reload(e,f'gym-ready-{city}-report-ready');locked(e,gym,city,index,'report-continued')
  print(f'PASS: {city} report-ready Gym still requires actual hand-in; repeated directions and indoor cold Continue grant no battle, badge or TM',flush=True)
  capital(e,index);before=item_count(e,reward);e.press('DOWN');e.press('A',180);e.finish_dialogue()
  assert e.var(var)==stage+1 and item_count(e,reward)==before+1
  done=preserved(e);e.press('DOWN');e.press('A',180);e.finish_dialogue();assert preserved(e)==done
  go(e,(16,14));travel(e,index+3);approach(e,index)
  gym.leader(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
  assert not gym.badge(e) and not defeated(e,index+7)
  e=reload(e,f'gym-ready-{city}-unlocked');gym.leader(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
  assert e.var(var)==stage+1 and item_count(e,reward)==before+1 and not gym.badge(e)
  print(f'PASS: {city} named contact accepts earned report once; normal return and cold Continue unlock optional leader offer without awarding an unearned Gym badge',flush=True)
finally:e.close()
