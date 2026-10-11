"""Inventory-only capacity fixture after four genuine Council victories."""
import re
from council_test_helpers import *
from test_gym_ui import start_action
from test_navigation import wait_task
ids={m[1]:int(m[2]) for m in re.finditer(r'^#define\s+(ITEM_\w+)\s+(\d+)\s*$',(ROOT/'include/constants/items.h').read_text(),re.M)}
items=json.loads((ROOT/'src/data/items.json').read_text())['items'];fill=[ids[x['itemId']] for x in items if x['pocket']=='POCKET_ITEMS' and x['english']!='????????' and x['itemId'] in ids and ids[x['itemId']] not in (0,68)][:42]
assert len(fill)==len(set(fill))==42 and 13 in fill and 22 in fill

def toss(e):
 e.press('A',90);wait_task(e,'Task_FieldItemContextMenuHandleInput');e.press('DOWN');e.press('DOWN');e.press('A',180)
 if e.task_active('Task_SelectQuantityToToss'):e.press('A',180)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'council-england-stage-4',True);assert council(e)==(4,0);h=history(e);nurse(e)
 base=e.read('gSaveBlock1Ptr')+0x310;key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
 for i,item in enumerate(fill):e.write(base+i*4,item,2);e.write(base+i*4+2,(99 if item==22 else 1)^key,2)
 begin(e,(10,4),757);battle(e);assert e.location()[:2]==(43,HALL)
 assert council(e)==(5,1) and item_count(e,68)==0 and history(e)==h
 e.screenshot(ROOT/'test-output/council-capacity-pending.png');e=reload(e,'council-capacity-pending');assert council(e)==(5,1)
 before=preserved(e);npc(e,(10,7));e.finish_dialogue();assert council(e)==(5,1) and preserved(e)==before
 print('PASS: inventory-only full-bag fixture still earns and saves Champion title; steward preserves the pending prize without another battle',flush=True)
 start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');state=e.symbols['gBagMenuState']
 for _ in range(5):
  if e.read(state+6,2)==0:break
  e.press('LEFT',90)
 assert e.read(state+6,2)==0
 for _ in range(45):
  if e.read(state+8,2)+e.read(state+14,2)==0:break
  e.press('UP')
 toss(e);e.press('B',180);wait_task(e,'Task_BagMenu_HandleInput');assert preserved(e)==before
 toss(e);e.press('A',180);wait_task(e,'Task_WaitAB_RedrawAndReturnToBag');e.press('A',180);wait_task(e,'Task_BagMenu_HandleInput');e.press('B',180);e.press('B',90)
 e=reload(e,'council-capacity-room');npc(e,(10,7));e.finish_dialogue();assert council(e)==(5,2) and item_count(e,68)==1 and history(e)==h
 e=reload(e,'council-capacity-complete');before=preserved(e);npc(e,(10,4));e.finish_dialogue();assert preserved(e)==before and item_count(e,68)==1
 print('PASS: native Toss cancel/confirm, cold Continue, pending prize claim and no duplication preserve championship completion',flush=True)
finally:e.close()
