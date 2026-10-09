"""Native Bag recovery on explicitly generated country inventory fixtures.

This runtime test performs no memory writes; only the separate fixture
generator arranges the Items capacity boundary.
"""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_celebi import report as talk, researcher as npc
from test_gym_ui import start_action
from test_navigation import wait_task
from test_tour import item_count
from test_time import preserved
from key_item_test_helpers import reload
CASES=[('Ada','celebi-return-ready',0x40EE,2,68,3)]

def toss(e):
 e.press('A',90);wait_task(e,'Task_FieldItemContextMenuHandleInput')
 e.press('DOWN');e.press('DOWN');e.press('A',180)
 if e.task_active('Task_SelectQuantityToToss'):e.press('A',180)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for country,source,var,stage,reward,dest in CASES:
  for mode in ['full','capped']:
   load_checkpoint(e,f'quest-capacity-{country}-{mode}-fixture',True);assert e.var(var)==stage
   before=preserved(e);npc(e);e.frames(900)
   for page in range(4):
    assert e.read('sLockFieldControls',1)
    e.screenshot(ROOT/f'test-output/quest-capacity-{country}-{mode}-{page}.png');e.press('A',900)
   e.finish_dialogue();talk(e);assert preserved(e)==before
   e=reload(e,f'quest-capacity-{country}-{mode}-pending');talk(e);assert preserved(e)==before
   print(f'PASS: {country} {mode} pending reward shows all four Bag-help pages; repeats/cold Continue preserve the earned report and unclaimed item',flush=True)
   start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
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
   toss(e);e.screenshot(ROOT/f'test-output/quest-capacity-{country}-{mode}-toss.png')
   e.press('B',180);wait_task(e,'Task_BagMenu_HandleInput');assert preserved(e)==before
   toss(e);e.press('A',180);wait_task(e,'Task_WaitAB_RedrawAndReturnToBag');e.press('A',180);wait_task(e,'Task_BagMenu_HandleInput')
   assert item_count(e,target)==qty-1
   e.press('B',180);e.press('B',90);room=preserved(e)
   assert room[:3]==before[:3] and room[4:]==before[4:] and e.var(var)==stage
   e=reload(e,f'quest-capacity-{country}-{mode}-room');assert preserved(e)==room
   print(f'PASS: {country} {mode} native Toss cancellation preserves inventory; confirming removes exactly one item and saved room leaves the report pending',flush=True)
   count=item_count(e,reward);talk(e);assert item_count(e,reward)==count+1 and e.var(var)==stage+1
   claimed=preserved(e);talk(e);assert preserved(e)==claimed
   e=reload(e,f'quest-capacity-{country}-{mode}-claimed');talk(e);assert preserved(e)==claimed
   print(f'PASS: {country} {mode} normal return grants exactly one earned item and completes the report; repeats/cold Continue cannot duplicate the reward',flush=True)
finally:e.close()
