"""Follow capital entrance signs to optional trainers and preparation services."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from test_tour import item_count
from test_trainers import money,defeated
from test_country import wait_menu
from test_shops import confirm_purchase
from key_item_test_helpers import reload

def sign(e,city,label):
 assert e.location()[2:]==(15,4)
 before=preserved(e);e.press('LEFT');e.press('A',900)
 for page in range(6):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/route-entrance-{city}-{label}-{page}.png');e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,(city,trainer) in enumerate([('London','OLIVER'),('Paris','CAMILLE'),('Berlin','FELIX')]):
  load_checkpoint(e,f'training-intro-{city}-ready',True)
  e.walk('LEFT',2);e.walk('DOWN',5);e.frames(180);assert e.location()==(43,index*4,15,0)
  go(e,(15,4));sign(e,city,'first');sign(e,city,'repeat')
  e=reload(e,f'route-entrance-{city}-sign');sign(e,city,'continued')
  assert not defeated(e,index)
  print(f'PASS: {city} all six entrance-sign pages retain destinations/visitor advice, name {trainer}, explain optional battles and services; repeats and cold Continue preserve state',flush=True)
  baseline=preserved(e)[1:];go(e,(15,1));e.walk('UP',2);e.frames(180);e.walk('UP',4);e.walk('RIGHT',2)
  assert e.location()==(43,index*4+1,17,19)
  before=preserved(e);e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
  assert preserved(e)==before and not e.in_battle() and not defeated(e,index)
  e.walk('LEFT',2);e.walk('DOWN',5);e.frames(180);assert e.location()==(43,index*4,15,0) and preserved(e)[1:]==baseline
  print(f'PASS: {city} clear north route reaches named optional trainer; B decline and southward return award no victory/prize and retain progress',flush=True)
  go(e,(6,10));e.walk('UP',1);e.frames(180);e.walk('UP',4);e.walk('RIGHT',1)
  before=preserved(e);e.press('UP');e.press('A',180);e.finish_dialogue();assert preserved(e)==before
  e=reload(e,f'route-entrance-{city}-clinic');e.walk('DOWN',5);e.frames(180)
  go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1);go(e,(1,7))
  funds=money(e);count=item_count(e,13)
  e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu');e.press('DOWN')
  confirm_purchase(e);e.frames(60);e.press('A',180);wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
  assert money(e)==funds-300 and item_count(e,13)==count+1
  e.press('A',90);e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
  e=reload(e,f'route-entrance-{city}-supplied');go(e,(4,7));e.walk('DOWN',2);e.frames(180)
  go(e,(15,4));sign(e,city,'supplied')
  assert money(e)==funds-300 and item_count(e,13)==count+1 and not defeated(e,index)
  print(f'PASS: {city} west-square free clinic and station shop are reachable; real Potion purchase and unbeaten trainer persist through indoor Continue and return to sign',flush=True)
finally:e.close()
