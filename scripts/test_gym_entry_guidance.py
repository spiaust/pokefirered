"""Walk Gym doors, native saves, leader declines and exits with earned readiness."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_tour_journal import inspect
from test_country import wait_menu
from test_time import preserved
from key_item_test_helpers import reload
from test_germany_story import leave_gym
from test_chantilly_gym import approach
e=Emulator(ROOT/'pokefirered.gba')
try:
 for city,town,gym,lead in [('Oxford',12,24,5),('Chantilly',16,25,13),('Oranienburg',20,26,18)]:
  load_checkpoint(e,'tour-approach-'+city,True);assert e.location()==(43,town,15,10)
  original=preserved(e)[1:];e.walk('UP',1);e.frames(180)
  assert e.location()==(43,gym,8 if city=='Chantilly' else 6,18 if city=='Chantilly' else 14)
  inspect(e,lead,'gym-entry-'+city)
  print(f'PASS: {city} north door walk enters correct Gym; journal lead and readiness remain intact',flush=True)
  before=preserved(e),e.location();e=reload(e,'gym-entry-'+city)
  assert (preserved(e),e.location())==before;inspect(e,lead,'gym-entry-'+city+'-continued')
  print(f'PASS: {city} native cold Continue retains exact indoor entry and read-only journal controls',flush=True)
  if city=='Chantilly':approach(e)
  else:e.walk('UP',8)
  before=preserved(e);e.press('UP');e.press('A',900);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
  assert not e.in_battle() and preserved(e)==before
  if city=='Chantilly':leave_gym(e);e.walk('LEFT',1);e.walk('UP',4)
  else:e.walk('DOWN',10);e.frames(180)
  assert e.location()==(43,town,15,10) and preserved(e)[1:]==original
  e=reload(e,'gym-entry-'+city+'-returned');assert e.location()==(43,town,15,10)
  print(f'PASS: {city} normal leader decline and south exit restore town approach without battle, badge or reward',flush=True)
finally:e.close()
