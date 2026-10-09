"""Follow completed Gym directions using genuinely earned reward batteries."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_country import wait_menu
from test_time import preserved
from test_germany_story import leave_gym
from test_ferry import captain,sail
from key_item_test_helpers import reload
import test_oxford_gym as rock
import test_chantilly_gym as water
import test_oranienburg_gym as electric

def completed(e,gym,city,label):
 before=preserved(e);gym.leader(e);e.frames(900);pages=0
 for page in range(12):
  if not e.read('sLockFieldControls',1):break
  e.screenshot(ROOT/f'test-output/gym-onward-{city}-{label}-{page}.png');e.press('A',900);pages+=1
 assert 5<=pages<=6,(city,pages)
 e.finish_dialogue();assert preserved(e)==before and not e.in_battle()

def contact(e):
 before=preserved(e);e.press('DOWN');e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180)
 e.finish_dialogue();assert preserved(e)==before

def approach(e,index):
 go(e,(15,10));e.walk('UP',1);e.frames(180)
 if index==1:water.approach(e)
 else:e.walk('UP',8)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,(city,gym) in enumerate([('Oxford',rock),('Chantilly',water),('Oranienburg',electric)]):
  load_checkpoint(e,f'gym-defeat-{city}-retry-won',True)
  assert gym.badge(e) and e.var(gym.TM_REWARD)==1 and gym.tm_count(e)==1
  completed(e,gym,city,'first');gym.complete_talk(e)
  e=reload(e,f'gym-onward-{city}-start');completed(e,gym,city,'continued')
  baseline=preserved(e)[1:]
  print(f'PASS: {city} completed leader advice repeats and cold Continues without duplicating the earned badge, TM or prize money',flush=True)
  if index==1:leave_gym(e)
  else:e.walk('DOWN',10);e.frames(180)
  go(e,(16,14))
  if index<2:
   travel(e,index+1);go(e,(10,14));contact(e)
   assert preserved(e)[1:]==baseline
   e=reload(e,f'gym-onward-{city}-contact');contact(e)
   assert preserved(e)[1:]==baseline
   e.screenshot(ROOT/f'test-output/gym-onward-{city}-contact.png')
   print(f'PASS: {city} exit and east station reach the named next-country contact; declining the next task and cold Continue grant no unearned story progress',flush=True)
  else:
   travel(e,3);go(e,(24,16));before=preserved(e)
   captain(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue();assert preserved(e)==before
   sail(e,0);assert preserved(e)==before
   e=reload(e,'gym-onward-Oranienburg-London-landing');assert preserved(e)==before
   e.screenshot(ROOT/'test-output/gym-onward-Oranienburg-landing.png')
   sail(e,12);assert preserved(e)==before
   e=reload(e,'gym-onward-Oranienburg-Oxford-landing');assert preserved(e)==before
   assert preserved(e)[1:]==baseline
   print('PASS: Oranienburg station directions reach Oxford river landing; captain B cancellation and free London/Oxford round trip with two cold Continues preserve earned progress',flush=True)
  go(e,(16,14));travel(e,index+3);approach(e,index)
  completed(e,gym,city,'returned');assert preserved(e)[1:]==baseline
  e=reload(e,f'gym-onward-{city}-returned');completed(e,gym,city,'return-continued')
  assert preserved(e)[1:]==baseline
  print(f'PASS: {city} normal return journey and another claimed-leader cold Continue retain all tested rewards/progress without duplicates',flush=True)
finally:
 e.screenshot(ROOT/'test-output/gym-onward-final.png');e.close()
