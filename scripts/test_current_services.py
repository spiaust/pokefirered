"""Native station purchases and clinic care on the genuine completed journey."""
from collections import Counter
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_country import wait_menu
from test_shops import confirm_purchase
from test_time import preserved
from key_item_test_helpers import reload

def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def contents(e):return Counter({i:q for i,q in preserved(e)[3] if i})
def identity(e):
 return tuple((tuple(e.read(e.symbols['gPlayerParty']+100*i+j,1) for j in range(32)),e.read(e.symbols['gPlayerParty']+100*i+84,1)) for i in range(e.read('gPlayerPartyCount',1)))

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'current-interiors-complete',True);original=history(e)
 for dest,city in enumerate(['London','Paris','Berlin','Oxford','Chantilly','Oranienburg']):
  go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1);e.walk('LEFT',3)
  assert e.location()==(43,dest*4+2,1,7),e.location()
  e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
  before=preserved(e),history(e);confirm_purchase(e,2);e.press('B',90);wait_menu(e,'Task_BuyMenu')
  assert (preserved(e),history(e))==before
  expected=contents(e);cash=preserved(e)[1];assert cash>=700
  for quantity,item,cost in [(2,4,400),(1,13,300)]:
   confirm_purchase(e,quantity);e.press('A',180);wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
   expected[item]+=quantity;cash-=cost
   assert contents(e)==expected and preserved(e)[1]==cash and history(e)==original
   assert preserved(e)[0]==before[0][0]
   e.press('A',90)
   if item==4:e.press('DOWN')
  e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
  e.screenshot(ROOT/f'test-output/current-services-{city}-shop.png')
  print('PASS: '+city+' station purchase cancellation changes nothing; two Poke Balls and one Potion cost exactly 700 with no other item, party or progress changes',flush=True)
  e=reload(e,'current-services-'+city+'-shop');assert e.location()==(43,dest*4+2,1,7) and history(e)==original
  e.walk('RIGHT',3);e.walk('DOWN',2);e.frames(180);assert e.location()==(43,dest*4,23,10)
  print('PASS: '+city+' station cold Continue retains purchases and exact saved state; exit reaches the correct town',flush=True)
  go(e,(6,10));e.walk('UP',1);e.frames(180);assert e.location()==(43,dest*4+3,6,8)
  e=reload(e,'current-services-'+city+'-clinic');before=preserved(e)[1:],history(e),identity(e)
  e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
  for i in range(e.read('gPlayerPartyCount',1)):
   p=e.symbols['gPlayerParty']+100*i;assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
  assert (preserved(e)[1:],history(e),identity(e))==before
  e.screenshot(ROOT/f'test-output/current-services-{city}-clinic.png')
  e=reload(e,'current-services-'+city+'-healed');e.walk('DOWN',5);e.frames(180)
  assert e.location()==(43,dest*4,6,10) and history(e)==original
  print('PASS: '+city+' clinic indoor Continue, free full-HP/status care, saved recovery and exit preserve party identity, money, items and all completed progress',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'current-services-complete')
 before=preserved(e),history(e);e.press('DOWN');e.press('A',900);e.finish_dialogue()
 assert (preserved(e),history(e))==before and history(e)==original
 print('PASS: normal return to Ada and final cold Continue retain every purchase, completed activity and repeatable ending',flush=True)
finally:e.close()
