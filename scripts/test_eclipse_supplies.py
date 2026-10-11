"""Buy evolution supplies with earned money and evolve a purified rescue."""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import talk, go, monfield
from test_country import wait_menu
from test_shops import confirm_purchase
from test_trainers import money
from test_oxford_gym import count_pocket
from test_gym_ui import start_action
from test_navigation import wait_task
from tm_teaching_test_helpers import field
from test_landmark_cases import save


def count(e,item): return count_pocket(e,item,0x310,42)


def use_stone(e,item=96,party_index=2):
 start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
 for _ in range(6):
  if e.read(bag+6,2)==0:break
  e.press('LEFT',60)
 slots=e.read('gSaveBlock1Ptr')+0x310
 index=next(i for i in range(42) if e.read(slots+i*4,2)==item)
 for _ in range(80):
  cur=e.read(bag+8,2)+e.read(bag+14,2)
  if cur==index:break
  e.press('DOWN' if cur<index else 'UP',30)
 assert cur==index
 e.press('A',90);e.press('A',180);wait_task(e,'Task_HandleChooseMonInput')
 for _ in range(10):
  cur=e.read(e.symbols['gPartyMenu']+9,1)
  if cur==party_index:break
  e.press('RIGHT' if cur==0 else 'DOWN',60)
 assert cur==party_index
 e.press('A',900)


def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-third-badge',True);assert e.read('gPlayerPartyCount',1)==2
  talk(e,(2,7));assert e.location()[:2]==(44,4)
  talk(e,(8,4));assert e.read('gPlayerPartyCount',1)==3
  assert monfield(e,2,0,0)&0xffff==25 and monfield(e,2,3,8)&(1<<27)
  stage=e.var(0x408C)
  go(e,(8,7));e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
  stock=e.symbols['Shadow_ShopItems'];items=[]
  while e.read(stock+2*len(items),2):items.append(e.read(stock+2*len(items),2))
  assert len(items)==21 and set(range(93,99)).issubset(items),items
  shop=e.symbols['sShopData']
  for item in (96,94):
   index=items.index(item)
   for _ in range(60):
    cur=e.read(shop+12,2)+e.read(shop+14,2)
    if cur==index:break
    e.press('DOWN' if cur<index else 'UP',30)
   assert cur==index
   before=money(e),count(e,item);assert before[0]>=2100
   confirm_purchase(e);e.press('B',90);wait_menu(e,'Task_BuyMenu')
   assert (money(e),count(e,item))==before
   confirm_purchase(e);e.press('A',180);wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
   assert money(e)==before[0]-2100 and count(e,item)==before[1]+1
   e.press('A',90);wait_menu(e,'Task_BuyMenu')
  e.screenshot(ROOT/'test-output/eclipse-evolution-shop.png')
  e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
  print('PASS: scrolling shop, cancel, Thunder/Moon Stones at 2100 each using earned money.',flush=True)
  use_stone(e)
  for _ in range(8):e.press('A',90)
  field(e)
  assert count(e,96)==1 and monfield(e,2,0,0)&0xffff==25 and monfield(e,2,3,8)&(1<<27)
  print('PASS: shadow partner refuses stone evolution without consuming the stone.',flush=True)
  for _ in range(13):talk(e,(4,4))
  assert not monfield(e,2,3,8)&(1<<27) and e.var(0x408F)==1
  use_stone(e)
  for _ in range(100):
   if monfield(e,2,0,0)&0xffff==26 and count(e,96)==0:break
   e.press('A',90)
  field(e)
  assert monfield(e,2,0,0)&0xffff==26 and count(e,96)==0 and e.var(0x408C)==stage
  save(e,'natural-raichu');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-raichu',True)
  assert monfield(e,2,0,0)&0xffff==26 and not monfield(e,2,3,8)&(1<<27)
  assert count(e,96)==0 and count(e,94)==1 and e.var(0x408C)==stage and e.var(0x408F)==1
  e.screenshot(ROOT/'test-output/eclipse-purified-raichu.png')
  print('PASS: purified rescue evolves to Raichu, consumes one stone, and survives cold Continue.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
