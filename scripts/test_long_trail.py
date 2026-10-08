"""Follow extended trainers' help, clinic paths, wins and regional rewards."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel,guide,item_count
from test_trainers import defeated,money
from test_country import wait_menu,party_species
from test_challenges import fight_with_supplies
from test_time import preserved
from key_item_test_helpers import reload

def to_trainer(e,index):
 go(e,(15,23));e.walk('DOWN',1);e.frames(180);e.walk('DOWN',19);e.walk('RIGHT',2)
 assert e.location()==(43,13+index*4,17,19),e.location()
def north(e,index):
 e.walk('LEFT',2);e.walk('UP',20);e.frames(180)
 assert e.location()==(43,12+index*4,15,23),e.location()
def nurse(e,index):
 go(e,(6,10));e.walk('UP',1);e.frames(180)
 assert e.location()[:2]==(43,15+index*4)
 e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
 p=e.symbols['gPlayerParty'];assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
def prompt(e,city):
 e.press('UP');e.press('A',900);e.press('A',900)
 e.screenshot(ROOT/f'test-output/long-trail-{city}-intro.png')
 wait_menu(e,'Task_YesNoMenu_HandleInput')

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,city,capital,team in [(0,'Oxford','London',(16,179)),(1,'Chantilly','Paris',(10,43)),(2,'Oranienburg','Berlin',(161,163))]:
  load_checkpoint(e,'training-recovery-'+capital+'-healed',True)
  assert defeated(e,index) and not defeated(e,index+3) and e.var(0x40F8+index)==0
  e.walk('DOWN',5);e.frames(180);go(e,(16,14));travel(e,index+3)
  before=item_count(e,68);guide(e);assert item_count(e,68)==before and e.var(0x40F8+index)==0
  to_trainer(e,index);original=preserved(e)
  for choice in ['NO','B']:
   prompt(e,city)
   if choice=='NO':e.press('DOWN');e.press('A',900)
   else:e.press('B',900)
   e.press('A',900);e.screenshot(ROOT/f'test-output/long-trail-{city}-{choice}-north.png')
   e.press('A',900);e.screenshot(ROOT/f'test-output/long-trail-{city}-{choice}-clinic.png')
   e.finish_dialogue()
   assert not e.in_battle() and not defeated(e,index+3) and preserved(e)==original
  print('PASS: '+city+' optional help and No/B show named northward clinic directions without changing party/items/progress',flush=True)
  north(e,index);nurse(e,index)
  e=reload(e,'long-trail-'+city+'-clinic')
  e.walk('DOWN',5);e.frames(180);to_trainer(e,index)
  assert preserved(e)[1:]==original[1:] and not defeated(e,index+3)
  print('PASS: '+city+' clear north path reaches the named free clinic; indoor cold Continue and return preserve the undecided challenge',flush=True)
  prompt(e,city);e.press('A',180)
  for _ in range(30):
   if e.in_battle():break
   e.press('A',90)
  assert e.in_battle();e.frames(300)
  assert e.read('gTrainerBattleOpponent_A',2)==746+index
  assert tuple(party_species(e,'gEnemyParty',i) for i in range(2))==team
  funds=money(e);fight_with_supplies(e)
  assert defeated(e,index+3) and money(e)>funds and e.location()==(43,13+index*4,17,19)
  state=preserved(e);e.press('UP');e.press('A',180);e.finish_dialogue();assert preserved(e)==state
  e=reload(e,'long-trail-'+city+'-won');assert defeated(e,index+3)
  print('PASS: '+city+' Yes starts correct battle; normal victory, prize-once repeat and cold Continue retain earned completion',flush=True)
  north(e,index);nurse(e,index);e.walk('DOWN',5);e.frames(180)
  go(e,(16,14));candy=item_count(e,68);guide(e)
  assert e.var(0x40F8+index)==1 and item_count(e,68)==candy+1
  state=preserved(e);guide(e);assert preserved(e)==state
  e=reload(e,'long-trail-'+city+'-reward');assert e.var(0x40F8+index)==1 and item_count(e,68)==candy+1
  guide(e);assert preserved(e)==state
  print('PASS: '+city+' guide awards exactly one regional Rare Candy after both wins; repeat and cold Continue cannot duplicate it',flush=True)
finally:e.close()
