"""Follow third-Gym directions to Ada and the genuine Celebi report."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,researcher,report,visit_forest,forest,accept_sighting,return_to_ada
from test_landmark_cases import go
from test_country import wait_menu
from test_time import preserved
from test_tour import travel,item_count
from key_item_test_helpers import reload
import test_oranienburg_gym as gym

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'gym-defeat-Oranienburg-retry-won',True)
 assert gym.badge(e) and e.var(gym.TM_REWARD)==1 and e.var(0x40EE)==0
 before=preserved(e);gym.leader(e);e.frames(900)
 for i in range(7):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/gym-ada-leader-{i}.png');e.press('A',900)
 e.finish_dialogue();gym.complete_talk(e);assert preserved(e)==before
 e=reload(e,'gym-ada-leader');gym.complete_talk(e);assert preserved(e)==before
 print('PASS: earned third Gym shows seven completed pages including Ada lead; repeat and cold Continue grant no duplicate TM or story progress',flush=True)
 e.walk('DOWN',10);e.frames(180);go(e,(16,14));travel(e,3);go(e,(18,14));before=preserved(e)
 for choice in ['B','NO']:
  researcher(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();assert preserved(e)==before
 e=reload(e,'gym-ada-offer');assert preserved(e)==before
 print('PASS: normal station train and east-of-guide directions reach Ada; earned Thunderbadge unlocks her optional offer and saved No/B declines change nothing',flush=True)
 candy=item_count(e,68);researcher(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);e.finish_dialogue()
 assert e.var(0x40EE)==1;before=preserved(e);report(e);assert preserved(e)==before
 e=reload(e,'gym-ada-active');visit_forest(e);before=preserved(e)
 for choice in ['B','NO']:
  forest(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();assert preserved(e)==before and not e.in_battle()
 e=reload(e,'gym-ada-forest');assert preserved(e)==before
 print('PASS: actual Ada acceptance and normal Chantilly train/forest walk reach Celebi; No/B sighting declines and cold Continue preserve active chapter without battle or reward',flush=True)
 accept_sighting(e);assert e.var(0x40EE)==2 and item_count(e,68)==candy
 before=preserved(e);forest(e);e.finish_dialogue();assert preserved(e)==before
 e=reload(e,'gym-ada-sighting');return_to_ada(e);report(e)
 assert e.var(0x40EE)==3 and item_count(e,68)==candy+1
 before=preserved(e);report(e);e=reload(e,'gym-ada-reported');report(e);assert preserved(e)==before
 e.screenshot(ROOT/'test-output/gym-ada-reported.png')
 print('PASS: genuine Celebi vision saves, normal return to Ada grants one report Candy, and repeats/cold Continue retain chapter completion without duplicates',flush=True)
finally:e.close()
