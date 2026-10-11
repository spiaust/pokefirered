"""Inventory-only capacity fixture; notes/party/story were earned natively.
Only the 42 item slots are arranged to make a full bag. Space is then freed
with actual Bag Toss controls. No original player battery is opened/written.
"""
import json,re
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,researcher
from test_landmark_cases import go
from test_tour import travel,item_count
from test_time import preserved
from test_gym_ui import start_action
from test_navigation import wait_task
from key_item_test_helpers import reload
ids={m[1]:int(m[2]) for m in re.finditer(r'^#define\s+(ITEM_\w+)\s+(\d+)\s*$',(ROOT/'include/constants/items.h').read_text(),re.M)}
items=json.loads((ROOT/'src/data/items.json').read_text())['items']
fill=[ids[x['itemId']] for x in items if x['pocket']=='POCKET_ITEMS' and x['english']!='????????' and x['itemId'] in ids and ids[x['itemId']] not in (0,69)][:42]
assert len(fill)==len(set(fill))==42

def toss(e):
 e.press('A',90);wait_task(e,'Task_FieldItemContextMenuHandleInput')
 e.press('DOWN');e.press('DOWN');e.press('A',180)
 if e.task_active('Task_SelectQuantityToToss'):e.press('A',180)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'archive-4-5-town-5',True);assert tuple(e.var(v) for v in range(0x40c8,0x40cc))==(1,1,1,1)
 go(e,(5,7));e.walk('DOWN',1);e.frames(180);go(e,(16,14));travel(e,3);go(e,(18,14))
 base=e.read('gSaveBlock1Ptr')+0x310;key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
 for i,item in enumerate(fill):e.write(base+i*4,item,2);e.write(base+i*4+2,1^key,2)
 before=preserved(e);researcher(e);e.finish_dialogue()
 assert e.var(0x40c8)==1 and item_count(e,69)==0 and preserved(e)==before
 e.screenshot(ROOT/'test-output/archive-capacity-full.png')
 e=reload(e,'archive-capacity-pending');assert e.var(0x40c8)==1 and preserved(e)==before
 print('PASS: full 42-slot inventory fixture prevents chapter completion/reward while retaining all natively earned notes and cold Continue',flush=True)
 start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');state=e.symbols['gBagMenuState']
 for _ in range(5):
  if e.read(state+6,2)==0:break
  e.press('LEFT',90)
 assert e.read(state+6,2)==0
 for _ in range(45):
  current=e.read(state+8,2)+e.read(state+14,2)
  if current==0:break
  e.press('UP')
 assert current==0
 toss(e);e.press('B',180);wait_task(e,'Task_BagMenu_HandleInput');assert preserved(e)==before
 toss(e);e.press('A',180);wait_task(e,'Task_WaitAB_RedrawAndReturnToBag');e.press('A',180);wait_task(e,'Task_BagMenu_HandleInput')
 e.press('B',180);e.press('B',90);assert not e.read('sLockFieldControls',1)
 assert preserved(e)[:3]==before[:3] and preserved(e)[4:]==before[4:]
 e=reload(e,'archive-capacity-room');researcher(e);e.finish_dialogue();assert e.var(0x40c8)==2 and item_count(e,69)==1
 after=preserved(e);researcher(e);e.finish_dialogue();assert preserved(e)==after
 e=reload(e,'archive-capacity-complete');assert e.var(0x40c8)==2 and item_count(e,69)==1
 print('PASS: native Bag Toss cancellation/confirmation, saved space, one PP UP and completed cold Continue recover the pending chapter',flush=True)
finally:e.close()
