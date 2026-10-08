"""Normal Bag controls on clearly identified synthetic capacity batteries.

This test performs no memory writes. Source inventories were arranged by
test_regional_reward_capacity.py; battle wins were earned normally.
"""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_navigation import wait_task
from test_tour import guide,item_count
from test_time import preserved
from test_trainers import defeated
from key_item_test_helpers import reload

def choose_toss(e):
 e.press('A',90);wait_task(e,'Task_FieldItemContextMenuHandleInput')
 e.press('DOWN');e.press('DOWN');e.press('A',180)
 if e.task_active('Task_SelectQuantityToToss'):e.press('A',180)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,city in enumerate(['Oxford','Chantilly','Oranienburg']):
  for mode in ['full','capped']:
   load_checkpoint(e,f'reward-capacity-{city}-{mode}-pending',True)
   assert e.var(0x40F8+index)==0 and defeated(e,index) and defeated(e,index+3)
   original=preserved(e);candy=item_count(e,68)
   start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput')
   bag=e.symbols['gBagMenuState']
   for _ in range(3):
    if e.read(bag+6,2)==0:break
    e.press('LEFT',90)
   assert e.read(bag+6,2)==0
   for _ in range(45):
    current=e.read(bag+8,2)+e.read(bag+14,2)
    if current==0:break
    e.press('UP')
   assert current==0
   target=e.read(e.read('gSaveBlock1Ptr')+0x310,2);qty=item_count(e,target)
   choose_toss(e);e.screenshot(ROOT/f'test-output/reward-bag-{city}-{mode}-confirm.png')
   e.press('B',180);wait_task(e,'Task_BagMenu_HandleInput');assert preserved(e)==original
   choose_toss(e);e.press('A',180)
   wait_task(e,'Task_WaitAB_RedrawAndReturnToBag');e.press('A',180)
   wait_task(e,'Task_BagMenu_HandleInput')
   assert item_count(e,target)==qty-1
   e.press('B',180);e.press('B',90);assert not e.read('sLockFieldControls',1)
   room=preserved(e);assert room[:3]==original[:3] and room[4:]==original[4:]
   assert e.var(0x40F8+index)==0
   e=reload(e,f'reward-bag-{city}-{mode}-room')
   count=item_count(e,68);guide(e)
   assert item_count(e,68)==count+1 and e.var(0x40F8+index)==1
   after=preserved(e);guide(e);assert preserved(e)==after
   e=reload(e,f'reward-bag-{city}-{mode}-claimed');guide(e);assert preserved(e)==after
   print(f'PASS: {city} {mode}: Bag Toss cancellation preserves inventory; confirming one item makes room; Save/Continue and one-time reward succeed without memory writes',flush=True)
finally:e.close()
