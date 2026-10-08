"""Follow earned local victories to optional extended matches and rewards."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from test_tour import item_count,guide
from test_trainers import defeated,money
from test_country import wait_menu,party_species
from test_challenges import fight_with_supplies
from key_item_test_helpers import reload

def advice(e,city,label):
 before=preserved(e);e.press('UP');e.press('A',900)
 for page in range(4):
  assert e.read('sLockFieldControls',1) and not e.in_battle()
  e.screenshot(ROOT/f'test-output/trainer-onward-{city}-{label}-{page}.png');e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,(city,town,team) in enumerate([('London','Oxford',(16,179)),('Paris','Chantilly',(10,43)),('Berlin','Oranienburg',(161,163))]):
  load_checkpoint(e,f'training-intro-{city}-won',True)
  assert defeated(e,index) and not defeated(e,index+3) and e.var(0x40F8+index)==0
  advice(e,city,'first');advice(e,city,'repeat');e=reload(e,f'trainer-onward-{city}-advice');advice(e,city,'continued')
  print(f'PASS: {city} earned-victory advice names onward trail, opponent and regional reward; repeat and cold Continue grant no duplicate prize',flush=True)
  e.walk('LEFT',2);e.walk('UP',20);e.frames(180);assert e.location()==(43,index*4+13,15,39)
  e.walk('UP',20);e.walk('RIGHT',2);assert e.location()==(43,index*4+13,17,19)
  before=preserved(e);e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
  assert preserved(e)==before and not defeated(e,index+3)
  e.walk('LEFT',2);e.walk('UP',20);e.frames(180);assert e.location()==(43,index*4+12,15,23)
  go(e,(16,14));count=item_count(e,68);guide(e);assert item_count(e,68)==count and e.var(0x40F8+index)==0
  go(e,(6,10));e.walk('UP',1);e.frames(180);e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
  p=e.symbols['gPlayerParty'];assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
  e=reload(e,f'trainer-onward-{town}-prepared');e.walk('DOWN',5);e.frames(180)
  go(e,(15,23));e.walk('DOWN',1);e.frames(180);e.walk('DOWN',19);e.walk('RIGHT',2)
  print(f'PASS: {city} north path reaches named optional opponent and {town}; B decline and free clinic/Continue retain unbeaten match and pending reward',flush=True)
  e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180)
  for _ in range(30):
   if e.in_battle():break
   e.press('A',90)
  assert e.in_battle();e.frames(300)
  assert e.read('gTrainerBattleOpponent_A',2)==746+index and tuple(party_species(e,'gEnemyParty',i) for i in range(2))==team
  funds=money(e);fight_with_supplies(e);assert defeated(e,index+3) and money(e)>funds
  before=preserved(e);e.press('UP');e.press('A',180);e.finish_dialogue();assert preserved(e)==before
  e.walk('LEFT',2);e.walk('UP',20);e.frames(180);go(e,(16,14));count=item_count(e,68);guide(e)
  assert e.var(0x40F8+index)==1 and item_count(e,68)==count+1
  won=preserved(e);guide(e);assert preserved(e)==won
  e=reload(e,f'trainer-onward-{town}-reward');guide(e);assert preserved(e)==won
  print(f'PASS: {town} correct accepted battle wins normally; guide gives exactly one Rare Candy after both victories, retained through repeat and cold Continue',flush=True)
finally:e.close()
