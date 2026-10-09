"""Follow genuine completed-country reminders to optional unlocked Gyms."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_france_story import talk,npc
from test_country import wait_menu
from test_time import preserved
from test_tour_journal import inspect
from key_item_test_helpers import reload
import test_chantilly_gym as water
import test_oranienburg_gym as electric

e=Emulator(ROOT/'pokefirered.gba')
try:
 for country,contact,source,gym,dest,lead,pages in [
  ('France','Celine','quest-report-France-claimed',water,4,13,3),
  ('France','Remy','quest-report-France-returned',water,4,13,1),
  ('Germany','Lena','quest-report-Germany-claimed',electric,5,18,3),
  ('Germany','Karl','quest-report-Germany-returned',electric,5,18,2)]:
  load_checkpoint(e,source,True);assert not gym.badge(e) and e.var(gym.TM_REWARD)==0
  before=preserved(e);npc(e);e.frames(900)
  for page in range(pages):
   assert e.read('sLockFieldControls',1)
   e.screenshot(ROOT/f'test-output/quest-gym-{contact}-{page}.png');e.press('A',900)
  e.finish_dialogue();talk(e);assert preserved(e)==before
  e=reload(e,f'quest-gym-{contact}-reminder');talk(e);inspect(e,lead,f'quest-gym-{contact}')
  assert preserved(e)==before
  print(f'PASS: {contact} completed-country reminder repeats/cold Continues read-only with the correct next Gym journal and no unearned badge or TM',flush=True)
  baseline=preserved(e)[1:];go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  go(e,(15,10));e.walk('UP',1);e.frames(180)
  if dest==4:water.approach(e)
  else:e.walk('UP',8)
  arrived=preserved(e);gym.leader(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
  assert preserved(e)==arrived and not gym.badge(e) and not e.in_battle()
  e=reload(e,f'quest-gym-{contact}-leader');gym.leader(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('DOWN');e.press('A',180);e.finish_dialogue()
  assert preserved(e)==arrived and preserved(e)[1:]==baseline and not gym.badge(e) and e.var(gym.TM_REWARD)==0
  e.screenshot(ROOT/f'test-output/quest-gym-{contact}-declined.png')
  print(f'PASS: {contact} normal station/town route reaches the unlocked Gym; native B and No declines across cold Continue preserve earned quest rewards and grant no battle, badge or TM',flush=True)
finally:e.close()
