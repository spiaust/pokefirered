"""Read both trail signs and walk their north/south service routes."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import item_count
from test_time import preserved
from test_trainers import money
from test_country import wait_menu
from test_shops import confirm_purchase
from key_item_test_helpers import reload

def read(e,city,label):
 before=preserved(e);e.press('LEFT');e.press('A',900)
 for page in range(4):
  assert e.read('sLockFieldControls',1) and not e.in_battle()
  e.screenshot(ROOT/f'test-output/trail-sign-{city}-{label}-{page}.png');e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before

def clinic(e,mapindex):
 go(e,(6,10));e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,mapindex)
 e.walk('UP',4);e.walk('RIGHT',1);before=preserved(e)
 e.press('UP');e.press('A',180);e.finish_dialogue();assert preserved(e)==before
 e.walk('DOWN',5);e.frames(180)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,(city,capital) in enumerate([('Oxford','London'),('Chantilly','Paris'),('Oranienburg','Berlin')]):
  load_checkpoint(e,f'training-recovery-{capital}-healed',True)
  e.walk('DOWN',5);e.frames(180);baseline=preserved(e)[1:]
  go(e,(15,1));e.walk('UP',2);e.frames(180);assert e.location()==(43,index*4+1,15,23)
  e.walk('UP',24);e.frames(180);assert e.location()==(43,index*4+13,15,39),e.location()
  e.walk('UP',3);e.walk('LEFT',1);assert e.location()==(43,index*4+13,14,36)
  read(e,city,'south');read(e,city,'south-repeat')
  e.walk('RIGHT',1);e.walk('UP',33);e.walk('LEFT',1);assert e.location()==(43,index*4+13,14,3)
  read(e,city,'north');read(e,city,'north-repeat')
  e=reload(e,f'trail-sign-{city}-north');read(e,city,'continued');assert preserved(e)[1:]==baseline
  print(f'PASS: {city} both trail-end signs show all four pages, repeat and cold Continue without changing items, money, badges or progress',flush=True)
  e.walk('RIGHT',1);e.walk('UP',4);e.frames(180);assert e.location()==(43,index*4+12,15,23)
  clinic(e,index*4+15)
  go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1);go(e,(1,7))
  funds=money(e);count=item_count(e,13)
  e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu');e.press('DOWN')
  confirm_purchase(e);e.frames(60);e.press('A',180);wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
  assert money(e)==funds-300 and item_count(e,13)==count+1
  e.press('A',90);e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
  e=reload(e,f'trail-sign-{city}-supplied');go(e,(4,7));e.walk('DOWN',2);e.frames(180)
  print(f'PASS: {city} north route reaches named town, free west-square clinic and station shop; real Potion purchase survives indoor Continue',flush=True)
  before=preserved(e)[1:];go(e,(15,23));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,index*4+13,15,0)
  e.walk('DOWN',40);e.frames(180);assert e.location()==(43,index*4+1,15,0),e.location()
  e.walk('DOWN',24);e.frames(180);assert e.location()==(43,index*4,15,0),e.location()
  clinic(e,index*4+3);assert preserved(e)[1:]==before
  e=reload(e,f'trail-sign-{city}-capital');assert e.location()[:2]==(43,index*4)
  print(f'PASS: {city} clear south path crosses the named countryside to {capital}, reaches its free clinic and cold Continues with supplies/progress retained',flush=True)
finally:e.close()
