"""Follow Gym guide directions to free care and real Potion purchases."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel,item_count
from test_time import preserved
from test_trainers import money
from test_country import wait_menu
from test_shops import confirm_purchase
from key_item_test_helpers import reload

def enter(e,index):
 go(e,(15,10));e.walk('UP',1);e.frames(180)
 e.walk('UP',1);e.walk('LEFT' if index==1 else 'RIGHT',1)
 assert e.location()==(43,24+index,*((7,17) if index==1 else (7,13)))

def advice(e,index,city,label):
 before=preserved(e);e.press('UP');e.press('A',900)
 for page in range(5 if index==1 else 6):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/gym-guide-{city}-{label}-{page}.png')
  e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before and not e.in_battle()

def exit_gym(e,index):
 e.walk('RIGHT' if index==1 else 'LEFT',1);e.walk('DOWN',3);e.frames(180)
 assert e.location()==(43,12+4*index,15,10)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,city in enumerate(['Oxford','Chantilly','Oranienburg']):
  load_checkpoint(e,'training-recovery-London-healed',True)
  e.walk('DOWN',5);e.frames(180);go(e,(16,14));travel(e,index+3);enter(e,index)
  advice(e,index,city,'first');advice(e,index,city,'repeat')
  e=reload(e,f'gym-guide-{city}-advice');advice(e,index,city,'continued')
  print(f'PASS: {city} complete type/story advice and new clinic/shop directions repeat and cold Continue without changing party/items/progress',flush=True)
  exit_gym(e,index);go(e,(6,10));e.walk('UP',1);e.frames(180)
  e.walk('UP',4);e.walk('RIGHT',1);before=preserved(e);e.press('UP');e.press('A',180);e.finish_dialogue()
  assert preserved(e)==before
  p=e.symbols['gPlayerParty'];assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
  e=reload(e,f'gym-guide-{city}-clinic');e.walk('DOWN',5);e.frames(180)
  print(f'PASS: {city} west-square clinic offers free care and indoor Continue; prepared team and progress stay intact',flush=True)
  go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1);go(e,(1,7))
  before=preserved(e);count=item_count(e,13);funds=money(e)
  e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
  e.press('DOWN');confirm_purchase(e);e.frames(60);e.press('B',180);wait_menu(e,'Task_BuyMenu');assert preserved(e)==before
  confirm_purchase(e);e.frames(60);e.press('A',180);wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
  assert item_count(e,13)==count+1 and money(e)==funds-300
  e.screenshot(ROOT/f'test-output/gym-guide-{city}-bought.png')
  e.press('A',90);e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
  after=preserved(e);assert after[0]==before[0] and after[2]==before[2] and after[4:]==before[4:]
  e=reload(e,f'gym-guide-{city}-supplied');go(e,(4,7));e.walk('DOWN',2);e.frames(180);enter(e,index)
  advice(e,index,city,'supplied');assert item_count(e,13)==count+1 and money(e)==funds-300
  print(f'PASS: {city} east-side station shop cancels safely and sells one Potion for exactly 300; purchase survives indoor Continue and return to guide',flush=True)
finally:e.close()
