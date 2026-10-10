"""Earned Oak/Celine reports, reward transitions and native Gym approaches."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel,item_count
from test_tour_journal import inspect
from test_time import preserved
from key_item_test_helpers import reload
from test_country import wait_menu
from test_chantilly_gym import approach

e=Emulator(ROOT/'pokefirered.gba')
try:
 for source,name,dest,stagevar,stage,reward,reportlead,gymdest,gymlead in [
  ('story-rival-won','Oak',0,0x40FB,1,184,4,3,5),
  ('celine-survey-gardens-forest-review','Celine',1,0x40FD,5,205,12,4,13)]:
  load_checkpoint(e,source,True);assert e.var(stagevar)==stage
  go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  e.walk('LEFT',6);assert e.location()==(43,dest*4,10,14)
  inspect(e,reportlead,'early-report-'+name)
  before=preserved(e),e.location();e=reload(e,'early-report-'+name)
  assert (preserved(e),e.location())==before;inspect(e,reportlead,'early-report-'+name+'-continued')
  print(f'PASS: {name} native return reaches west contact with required report lead and exact cold Continue',flush=True)
  count=item_count(e,reward);e.press('DOWN');e.press('A',900);e.finish_dialogue()
  assert e.var(stagevar)==stage+1 and item_count(e,reward)==count+1
  inspect(e,gymlead,'early-report-'+name+'-unlocked')
  before=preserved(e);e.press('DOWN');e.press('A',900);e.finish_dialogue();assert preserved(e)==before
  print(f'PASS: {name} normal report grants one reward, switches journal to next Gym and repeats read-only',flush=True)
  go(e,(16,14));travel(e,gymdest);go(e,(15,10));inspect(e,gymlead,'early-report-'+name+'-door')
  e.walk('UP',1);e.frames(180)
  if name=='Celine':
   assert e.location()==(43,25,8,18);approach(e);expected=(43,25,8,7)
  else:
   assert e.location()==(43,24,6,14);e.walk('UP',8);expected=(43,24,6,6)
  assert e.location()==expected;inspect(e,gymlead,'early-report-'+name+'-leader')
  before=preserved(e),e.location();e=reload(e,'early-report-'+name+'-leader')
  assert (preserved(e),e.location())==before
  print(f'PASS: {name} reward-earned route reaches next Gym leader and retains readiness on native cold Continue',flush=True)
  e.press('UP');e.press('A',900);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
  assert not e.in_battle() and (preserved(e),e.location())==before
  print(f'PASS: {name} unlocked Gym challenge decline preserves earned report, reward and badge state',flush=True)
finally:e.close()
