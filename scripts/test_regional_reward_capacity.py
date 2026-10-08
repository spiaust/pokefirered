"""Isolated inventory-capacity fixtures; trainer wins come from real battles.

Only the 42-slot items pocket is edited to arrange capacity boundaries.
No story flags, trainer flags, party, money or user batteries are edited.
Making room is another explicit fixture edit, not claimed as Bag UI coverage.
"""
import json,re
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import guide,item_count
from test_trainers import defeated
from test_time import preserved
from key_item_test_helpers import reload

ids={m[1]:int(m[2]) for m in re.finditer(r'^#define\s+(ITEM_\w+)\s+(\d+)\s*$',(ROOT/'include/constants/items.h').read_text(),re.M)}
items=json.loads((ROOT/'src/data/items.json').read_text())['items']
fill=[ids[x['itemId']] for x in items if x['pocket']=='POCKET_ITEMS' and x['english']!='????????' and x['itemId'] in ids and ids[x['itemId']] not in (0,68)][:42]
assert len(fill)==42 and len(set(fill))==42

def fixture(e,mode):
 p=e.read('gSaveBlock1Ptr')+0x310
 key=e.read(e.read('gSaveBlock2Ptr')+0xF20,2)
 slots=[(v,1) for v in fill]
 if mode=='capped':slots=[(68,999)]+[(0,0)]*41
 if mode=='stack':slots[0]=(68,998)
 for i,(item,qty) in enumerate(slots):
  e.write(p+i*4,item,2);e.write(p+i*4+2,qty^key,2)

def make_room(e,mode):
 p=e.read('gSaveBlock1Ptr')+0x310
 key=e.read(e.read('gSaveBlock2Ptr')+0xF20,2)
 if mode=='capped':e.write(p+2,998^key,2)
 else:e.write(p,0,2);e.write(p+2,key,2)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,city in enumerate(['Oxford','Chantilly','Oranienburg']):
  for mode in ['full','capped','stack']:
   load_checkpoint(e,'long-trail-'+city+'-won',True)
   assert defeated(e,index) and defeated(e,index+3) and e.var(0x40F8+index)==0
   e.walk('LEFT',2);e.walk('UP',20);e.frames(180);go(e,(16,14))
   fixture(e,mode);before=preserved(e);count=item_count(e,68)
   if mode!='stack':
    guide(e);assert preserved(e)==before and e.var(0x40F8+index)==0
    e=reload(e,f'reward-capacity-{city}-{mode}-pending')
    guide(e);assert preserved(e)==before and e.var(0x40F8+index)==0
    # Show the final pending-reward page for native text inspection.
    e.press('DOWN');e.press('A',900)
    for _ in range(4):e.press('A',900)
    e.screenshot(ROOT/f'test-output/reward-capacity-{city}-{mode}-pending.png')
    e.finish_dialogue();assert preserved(e)==before
    make_room(e,mode);count=item_count(e,68)
   guide(e)
   assert item_count(e,68)==count+1 and e.var(0x40F8+index)==1
   after=preserved(e);guide(e);assert preserved(e)==after
   e=reload(e,f'reward-capacity-{city}-{mode}-claimed')
   guide(e);assert preserved(e)==after
   assert defeated(e,index) and defeated(e,index+3)
   print(f'PASS: {city} {mode} inventory fixture: capacity handling, one reward, repeat and cold Continue preserve earned wins',flush=True)
finally:e.close()
