"""Native paved routes to Oliver/Alice without accepting their battles."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_country import wait_menu
from test_time import preserved
from test_trainers import defeated
from key_item_test_helpers import reload
e=Emulator(ROOT/'pokefirered.gba')
try:
 for name,index in [('Oliver',0),('Alice',3)]:
  load_checkpoint(e,'early-contact-england-accepted',True);original=preserved(e)[1:]
  if index:
   go(e,(16,14));travel(e,3);go(e,(15,14));e.walk('DOWN',10);e.frames(180);e.walk('DOWN',19)
  else:go(e,(15,14));e.walk('UP',15);e.frames(180);e.walk('UP',4)
  e.walk('RIGHT',2);assert e.location()==(43,13 if index else 1,17,19)
  assert preserved(e)[1:]==original and not defeated(e,index)
  print(f'PASS: {name} paved route reaches east-of-path approach17,19 without battle or quest changes',flush=True)
  before=preserved(e),e.location()
  for choice in ['NO','B']:
   e.press('UP');e.press('A',900);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
   if choice=='NO':e.press('DOWN');e.press('A',180)
   else:e.press('B',180)
   e.finish_dialogue();assert (preserved(e),e.location())==before and not e.in_battle()
  e=reload(e,'english-trail-directions-'+name);assert (preserved(e),e.location())==before and not defeated(e,index)
  print(f'PASS: {name} UP/A reaches correct optional offer; No/B and cold Continue retain unbeaten state',flush=True)
finally:e.close()
