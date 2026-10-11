"""Buy ordinary shelter supplies with earned money through native shop menus."""
from test_country import wait_menu
from test_shops import confirm_purchase
from test_trainers import money
from test_oxford_gym import count_pocket
import test_eclipse_natural as natural

def buy(e,orders):
 natural.natural_go(e,(8,7));e.press('UP');e.press('A',180)
 wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
 stock=e.symbols['Shadow_ShopItems'];items=[]
 while e.read(stock+2*len(items),2):items.append(e.read(stock+2*len(items),2))
 shop=e.symbols['sShopData']
 for item,quantity,price in orders:
  index=items.index(item)
  for _ in range(60):
   cur=e.read(shop+12,2)+e.read(shop+14,2)
   if cur==index:break
   e.press('DOWN' if cur<index else 'UP',30)
  assert cur==index
  before=money(e),count_pocket(e,item,0x310,42);assert before[0]>=quantity*price
  confirm_purchase(e,quantity);e.press('A',180);wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
  assert money(e)==before[0]-quantity*price and count_pocket(e,item,0x310,42)==before[1]+quantity
  e.press('A',90);wait_menu(e,'Task_BuyMenu')
  print('Native supplies purchased:',item,quantity,'cost',quantity*price,flush=True)
 e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
