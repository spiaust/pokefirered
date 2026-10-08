"""Earn regional victories in reverse order and verify remaining-trainer help."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import guide,travel,item_count
from test_time import preserved
from test_trainers import defeated,money
from test_country import wait_menu
from test_challenges import fight_with_supplies
from key_item_test_helpers import reload

def advice(e,index,city,label,count):
 before=preserved(e);e.press('DOWN');e.press('A',900)
 for _ in range(3 if index==0 else 4):e.press('A',900)
 assert e.read('gSpecialVar_0x8005',2)==count
 for page in range(3 if count==0 else 4):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/regional-guide-{city}-{label}-{page}.png');e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before

def ready_town(e,index,city):
 load_checkpoint(e,f'training-intro-{city}-ready',True)
 e.walk('LEFT',2);e.walk('DOWN',5);e.frames(180);go(e,(16,14));travel(e,index+3)

def extended(e,index):
 go(e,(15,23));e.walk('DOWN',1);e.frames(180);e.walk('DOWN',19);e.walk('RIGHT',2)
 assert e.location()==(43,index*4+13,17,19)

def north(e,index):
 e.walk('LEFT',2);e.walk('UP',20);e.frames(180);go(e,(16,14))

def battle(e,index,offset):
 e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180)
 for _ in range(30):
  if e.in_battle():break
  e.press('A',90)
 assert e.in_battle();e.frames(300);assert e.read('gTrainerBattleOpponent_A',2)==743+index+offset
 funds=money(e);fight_with_supplies(e);assert defeated(e,index+offset) and money(e)>funds

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,(city,town) in enumerate([('London','Oxford'),('Paris','Chantilly'),('Berlin','Oranienburg')]):
  ready_town(e,index,city);assert not defeated(e,index) and not defeated(e,index+3)
  advice(e,index,town,'zero',0);guide(e);e=reload(e,f'regional-guide-{town}-zero');advice(e,index,town,'zero-continued',0)
  assert e.var(0x40F8+index)==0 and item_count(e,68)==0
  print(f'PASS: {town} zero-win guide retains original both-trainer directions, repeat and cold Continue without granting a reward',flush=True)
  extended(e,index);battle(e,index,3);assert not defeated(e,index)
  north(e,index);advice(e,index,town,'extended-first',1);guide(e)
  e=reload(e,f'regional-guide-{town}-extended-first');advice(e,index,town,'extended-continued',1)
  assert e.var(0x40F8+index)==0 and item_count(e,68)==0
  print(f'PASS: {town} real extended-first victory leaves local trainer unbeaten; guide names missing local opponent and southward route through repeat/Continue',flush=True)
  load_checkpoint(e,f'training-recovery-{city}-healed',True);e.walk('DOWN',5);e.frames(180);go(e,(16,14));travel(e,index+3)
  assert defeated(e,index) and not defeated(e,index+3)
  advice(e,index,town,'local-first',1);guide(e);e=reload(e,f'regional-guide-{town}-local-first');advice(e,index,town,'local-continued',1)
  assert e.var(0x40F8+index)==0 and item_count(e,68)==0
  print(f'PASS: {town} genuine local-first victory names missing extended opponent and nearby south trail; repeats/Continue preserve pending eligibility',flush=True)
  load_checkpoint(e,f'regional-guide-{town}-extended-first',True)
  go(e,(6,10));e.walk('UP',1);e.frames(180);e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue();e.walk('DOWN',5);e.frames(180)
  go(e,(15,23));e.walk('DOWN',1);e.frames(180);e.walk('DOWN',40);e.frames(180);e.walk('DOWN',19);e.walk('RIGHT',2)
  assert e.location()==(43,index*4+1,17,19);battle(e,index,0)
  e.walk('LEFT',2);e.walk('UP',20);e.frames(180);e.walk('UP',40);e.frames(180);go(e,(16,14))
  assert defeated(e,index) and defeated(e,index+3)
  count=item_count(e,68);guide(e);assert e.var(0x40F8+index)==1 and item_count(e,68)==count+1
  print(f'PASS: {town} following missing-local directions earns normal second victory and exactly one regional Candy in reverse battle order',flush=True)
  won=preserved(e);guide(e);assert preserved(e)==won;e=reload(e,f'regional-guide-{town}-claimed');guide(e);assert preserved(e)==won
  print(f'PASS: {town} claimed guide skips remaining-trainer branches and retains one reward across repeat and cold Continue',flush=True)
finally:e.close()
