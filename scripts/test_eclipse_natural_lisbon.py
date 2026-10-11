"""Use the earned Earthquake TM and ordinary training for Lisbon's handler."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from tm_teaching_test_helpers import select,field
from battle_recovery_test_helpers import moves_pp
from test_country import wait_menu
from test_shops import confirm_purchase
from test_trainers import money
import sys

def advance(e,task):
 for _ in range(40):
  if e.task_active(task):e.frames(60);return
  e.press('A',90)
 raise AssertionError(task)

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-trained-lisbon' if '--resume' in sys.argv else 'natural-eighth-badge',True)
  assert e.var(0x408C)==11 and e.var(0x4090)==0 and e.var(0x4091)==0
  if '--resume' not in sys.argv:
   assert monfield(e,0,0,0)&65535==31
   old,_=moves_pp(e);assert old[2]==40
   select(e,314);e.press('A',900);advance(e,'Task_HandleReplaceMoveYesNoInput');e.press('A',180)
   advance(e,'Task_InputHandler_SelectOrForgetMove')
   for _ in range(6):
    cur=e.read('sMoveSelectionCursorPos',1)
    if cur==2:break
    e.press('DOWN' if cur<2 else 'UP',60)
   assert e.read('sMoveSelectionCursorPos',1)==2
   e.press('A',900)
   for _ in range(15):
    if count_pocket(e,314,0x464,58)==0:break
    e.press('A',180)
   e.press('A',180);field(e)
   assert moves_pp(e)[0]==(old[0],old[1],89,old[3]) and count_pocket(e,314,0x464,58)==0
   talk(e,(2,7));assert e.location()[:2]==(44,18)
   for practice in range(25):
    if e.read(e.symbols['gPlayerParty']+84,1)>=45:break
    talk(e,(2,4));talk(e,(10,7));result,turns=natural.natural_trainer_battle(e,(7,7))
    print('Rome preparation:',practice+1,'result',result,'Nidoqueen level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
    assert result==1
    talk(e,(15,20));talk(e,(2,4));save(e,'natural-lisbon-preparation')
   assert e.read(e.symbols['gPlayerParty']+84,1)>=45
   talk(e,(10,4));talk(e,(10,4));assert e.location()[:2]==(44,22)
   talk(e,(2,4));save(e,'natural-trained-lisbon')
  # Use earned money and ordinary supplies rather than altering battle stats.
  natural.natural_go(e,(8,7));e.press('UP');e.press('A',180)
  wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
  stock=e.symbols['Shadow_ShopItems'];items=[]
  while e.read(stock+2*len(items),2):items.append(e.read(stock+2*len(items),2))
  index=items.index(21);shop=e.symbols['sShopData']
  for _ in range(60):
   cur=e.read(shop+12,2)+e.read(shop+14,2)
   if cur==index:break
   e.press('DOWN' if cur<index else 'UP',30)
  assert cur==index
  before=money(e),count_pocket(e,21,0x310,42);assert before[0]>=6000
  confirm_purchase(e,5);e.press('A',180);wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
  assert money(e)==before[0]-6000 and count_pocket(e,21,0x310,42)==before[1]+5
  e.press('A',90);wait_menu(e,'Task_BuyMenu')
  index=items.index(24)
  for _ in range(60):
   cur=e.read(shop+12,2)+e.read(shop+14,2)
   if cur==index:break
   e.press('DOWN' if cur<index else 'UP',30)
  assert cur==index
  revive_before=money(e),count_pocket(e,24,0x310,42)
  confirm_purchase(e);e.press('A',180);wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
  assert money(e)==revive_before[0]-1500 and count_pocket(e,24,0x310,42)==revive_before[1]+1
  e.press('A',90);wait_menu(e,'Task_BuyMenu');e.press('B',180)
  wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
  battle_start(e,(6,4));result,turns=natural.natural_battle(e,healing_item=21,healing_limit=5,revive_species=31)
  print('Prepared Lisbon:',result,turns,'selections',flush=True)
  assert result==1 and e.var(0x408C)==12
  talk(e,(2,4));save(e,'natural-lisbon-complete');e.screenshot(ROOT/'test-output/eclipse-natural-lisbon.png')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-lisbon-complete',True)
  assert e.var(0x408C)==12 and moves_pp(e)[0][2]==89 and count_pocket(e,314,0x464,58)==0
  print('PASS: earned Earthquake, native preparation, Lisbon victory and cold Continue.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
