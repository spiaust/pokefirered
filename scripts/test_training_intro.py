"""Read trainer help, decline, cold Continue, accept and finish a normal battle."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk
from test_country import wait_menu,party_species
from test_time import preserved
from test_trainers import defeated,money
from test_challenges import fight_with_supplies
from key_item_test_helpers import reload

def prompt(e,city):
 e.press('UP');e.press('A',900);e.press('A',900)
 e.screenshot(ROOT/f'test-output/training-intro-{city}.png')
 wait_menu(e,'Task_YesNoMenu_HandleInput')

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,city,team in [(0,'London',(16,179)),(1,'Paris',(10,43)),(2,'Berlin',(161,163))]:
  load_checkpoint(e,'clinic-directions-'+city,True)
  e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
  e.walk('DOWN',5);e.frames(180)
  go(e,(15,14));e.walk('UP',15);e.walk('UP',4);e.walk('RIGHT',2)
  assert e.location()==(43,index*4+1,17,19) and not defeated(e,index)
  before=preserved(e)
  for choice in ['NO','B']:
   prompt(e,city)
   if choice=='NO':e.press('DOWN');e.press('A',180)
   else:e.press('B',180)
   e.finish_dialogue()
   assert not e.in_battle() and not defeated(e,index) and preserved(e)==before
   assert not e.read('sLockFieldControls',1)
  print('PASS: '+city+' new help page and No/B preserve exact party, money, items and progress without battle',flush=True)
  e=reload(e,'training-intro-'+city+'-ready')
  assert not defeated(e,index) and preserved(e)==before
  prompt(e,city);e.press('A',180)
  for _ in range(30):
   if e.in_battle():break
   e.press('A',90)
  assert e.in_battle();e.frames(300)
  assert e.read('gTrainerBattleOpponent_A',2)==743+index
  assert tuple(party_species(e,'gEnemyParty',i) for i in range(2))==team
  e.screenshot(ROOT/f'test-output/training-battle-{city}.png')
  print('PASS: '+city+' cold Continue retains undecided trainer; Yes starts the correct two-partner battle',flush=True)
  funds=money(e);fight_with_supplies(e)
  assert defeated(e,index) and money(e)>funds and e.location()==(43,index*4+1,17,19)
  funds=money(e);state=preserved(e)
  e.press('UP');e.press('A',180);e.finish_dialogue()
  assert not e.in_battle() and money(e)==funds and preserved(e)==state
  e=reload(e,'training-intro-'+city+'-won');assert defeated(e,index) and money(e)==funds
  e.screenshot(ROOT/f'test-output/training-victory-{city}.png')
  print('PASS: '+city+' normal victory awards prize once; repeat talk and cold Continue retain completion',flush=True)
finally:e.close()
