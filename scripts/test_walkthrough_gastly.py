"""Catch the optional Gastly with earned/purchased balls, without save edits."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_tour import travel
from test_country import wait_menu,party_species
from test_shops import confirm_purchase,balls
from test_trainers import money
from test_navigation import wait_task
from test_time import preserved
from test_oxford_gym import count_pocket

def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def town(e,dest):go(e,(16,14));travel(e,dest)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'walkthrough-lapras-complete',True);original=history(e)
 assert e.read('gPlayerPartyCount',1)==1 and count_pocket(e,3,0x430,13)==3
 town(e,1);go(e,(23,10));e.walk('UP',1);e.frames(180);e.walk('UP',1);go(e,(1,7))
 e.press('UP');e.press('A',180);wait_menu(e,'Task_ShopMenu');e.press('A',180);wait_menu(e,'Task_BuyMenu')
 before=money(e),balls(e);confirm_purchase(e,10);e.press('A',180);wait_menu(e,'Task_ReturnToItemListAfterItemPurchase')
 assert money(e)==before[0]-2000 and balls(e)==before[1]+10
 e.press('A',90);e.press('B',180);wait_menu(e,'Task_ShopMenu');e.press('B',180);e.finish_dialogue()
 go(e,(4,7));e.walk('DOWN',2);e.frames(180)
 print('PASS: buys ten Poke Balls through normal Paris shop with exact 2000 cost; three earned Great Balls retained',flush=True)
 talk(e,(28,35),choice='YES');assert e.location()==(43,38,10,15)
 for choice in ['NO','B']:
  before=preserved(e);talk(e,(10,5),choice=choice);assert preserved(e)==before and not e.in_battle() and history(e)==original
 print('PASS: optional Gastly No/B declines retain completed case, rewards and main ending',flush=True)
 save(e,'walkthrough-gastly-ready')
 go(e,(10,5));e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);e.frames(300)
 assert e.in_battle() and party_species(e,'gEnemyParty')==92 and e.read(e.symbols['gEnemyParty']+84,1)==12
 e.screenshot(ROOT/'test-output/walkthrough-gastly-battle.png')
 print('PASS: completed Notre Dame attendant starts a real level-12 Gastly encounter with case stage still rewarded',flush=True)
 action=next(int(line.split()[0],16) for line in (ROOT/'pokefirered.sym').read_text().splitlines() if line.split()[-1:]==['HandleInputChooseAction'])
 thrown=0;cash=money(e)
 for _ in range(1800):
  if e.read('gPlayerPartyCount',1)==2 and not e.in_battle():break
  if e.in_battle() and e.read('gBattlerControllerFuncs')&~1==action:
   e.press('UP');e.press('LEFT');e.press('RIGHT');e.press('A',180);wait_task(e,'Task_BagMenu_HandleInput')
   bag=e.symbols['gBagMenuState']
   for _ in range(5):
    if e.read(bag+6,2)==2:break
    e.press('RIGHT',90)
   assert e.read(bag+6,2)==2
   ball=3 if count_pocket(e,3,0x430,13) else 4
   assert count_pocket(e,ball,0x430,13)>0
   base=e.read('gSaveBlock1Ptr')+0x430
   target=next(i for i in range(13) if e.read(base+i*4,2)==ball)
   for _ in range(30):
    cursor=e.read(bag+12,2)+e.read(bag+18,2)
    if cursor==target:break
    e.press('DOWN' if cursor<target else 'UP')
   assert cursor==target
   e.press('A',90);e.press('A',180);thrown+=1
   print('Normal ball throw',thrown,'item',ball,flush=True)
  else:e.press('B',90)
 assert e.read('gPlayerPartyCount',1)==2 and not e.in_battle()
 e.frames(300);e.finish_dialogue()
 assert party_species(e,index=1)==92 and e.read(e.symbols['gPlayerParty']+184,1)==12
 assert history(e)==original and money(e)==cash
 e.screenshot(ROOT/'test-output/walkthrough-gastly-caught.png');save(e,'walkthrough-gastly-caught');saved=preserved(e)
 print('PASS: normal earned/purchased balls catch Gastly, add it to party and retain completed cases/story without edited items or catch rates',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'walkthrough-gastly-caught',True);assert preserved(e)==saved and history(e)==original and party_species(e,index=1)==92
 go(e,(10,15));e.walk('DOWN',1);e.frames(180);town(e,3);go(e,(18,14))
 before=preserved(e);e.press('DOWN');e.press('A',900)
 e.screenshot(ROOT/'test-output/walkthrough-gastly-ada.png')
 for _ in range(160):
  if not e.read('sLockFieldControls',1):break
  e.press('A',90)
 assert preserved(e)==before and history(e)==original and not e.read('sLockFieldControls',1)
 save(e,'walkthrough-gastly-complete')
 print('PASS: capture save cold Continues with exact party/inventory; return to Ada preserves optional cases and main conclusion',flush=True)
finally:e.close()
