"""Synthetic inventory limits before normal Gym wins; no progress injections."""
import json,re
from collections import Counter
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_trainers import defeated,money
from test_time import preserved
from test_navigation import wait_task
from test_gym_ui import open_key_item,start_action
from key_item_test_helpers import reload
from battle_recovery_test_helpers import begin
import test_oxford_gym as rock
import test_chantilly_gym as water
import test_oranienburg_gym as electric

ids={m[1]:int(m[2]) for m in re.finditer(r'^#define\s+(ITEM_\w+)\s+(\d+)\s*$',(ROOT/'include/constants/items.h').read_text(),re.M)}
items=json.loads((ROOT/'src/data/items.json').read_text())['items']
keys=[ids[x['itemId']] for x in items if x['pocket']=='POCKET_KEY_ITEMS' and x['english']!='????????' and x['itemId'] in ids and ids[x['itemId']]!=364][:30]
assert len(keys)==30 and len(set(keys))==30

def slot(e,offset,item,qty):
 p=e.read('gSaveBlock1Ptr')+offset;k=e.read(e.read('gSaveBlock2Ptr')+0xF20,2)
 e.write(p,item,2);e.write(p+2,qty^k,2)

def fixture(e,mode,tm):
 if mode=='key':
  for i,item in enumerate(keys):slot(e,0x3B8+4*i,item,1)
 else:
  slot(e,0x464,tm,999)
  for i in range(1,58):slot(e,0x464+4*i,0,0)
  p=e.read('gSaveBlock1Ptr')+0x3B8
  if not any(e.read(p+4*i,2)==364 for i in range(30)):
   empty=next(i for i in range(30) if e.read(p+4*i,2)==0)
   slot(e,0x3B8+4*empty,364,1)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,(city,gym,tm) in enumerate([('Oxford',rock,327),('Chantilly',water,291),('Oranienburg',electric,322)]):
  for mode in ['tm','key']:
   load_checkpoint(e,f'gym-defeat-{city}-recovered',True)
   x,y=e.location()[2:]
   if x!=7:e.walk('RIGHT' if x<7 else 'LEFT',abs(x-7))
   if y!=4:e.walk('UP' if y>4 else 'DOWN',abs(y-4))
   e.walk('DOWN',5);e.frames(180);go(e,(15,10));e.walk('UP',1);e.frames(180)
   if index==1:water.approach(e)
   else:e.walk('UP',8)
   fixture(e,mode,tm);count=gym.tm_count(e);funds=money(e)
   assert not gym.badge(e) and not defeated(e,index+7) and e.var(gym.TM_REWARD)==0
   begin(e);gym.gym_fight(e)
   assert gym.badge(e) and defeated(e,index+7) and money(e)>funds
   assert gym.tm_count(e)==count and e.var(gym.TM_REWARD)==0
   pending=preserved(e);gym.complete_talk(e);assert preserved(e)==pending
   e=reload(e,f'gym-capacity-{city}-{mode}-pending');gym.complete_talk(e);assert preserved(e)==pending
   gym.leader(e);e.frames(900);e.screenshot(ROOT/f'test-output/gym-capacity-{city}-{mode}-pending.png');e.finish_dialogue()
   # Explicit inventory fixture edit; not a claim of native room-making UI.
   if mode=='tm':slot(e,0x464,tm,998)
   else:slot(e,0x3B8,0,0)
   expected=999 if mode=='tm' else count+1
   gym.complete_talk(e)
   assert gym.tm_count(e)==expected and e.var(gym.TM_REWARD)==1 and gym.badge(e)
   assert gym.count_pocket(e,364,0x3B8,30)==1
   claimed=preserved(e);gym.complete_talk(e);assert preserved(e)==claimed
   e=reload(e,f'gym-capacity-{city}-{mode}-claimed');gym.complete_talk(e);assert preserved(e)==claimed
   print(f'PASS: {city} {mode} fixture: real victory retains badge and pending TM through Continue; room permits one claim and no duplicate',flush=True)
   start_action(e,3);wait_task(e,'Task_TrainerCard');e.frames(180)
   card=e.read('sTrainerCardDataPtr');assert [e.read(card+17+i,1) for i in range(8)]==[1]*(index+1)+[0]*(7-index)
   e.screenshot(ROOT/f'test-output/gym-capacity-{city}-{mode}-card.png')
   e.press('B',180);e.press('B',90)
   open_key_item(e,364);e.frames(180)
   assert e.read('sTMCaseDynamicResources')!=0 and gym.tm_count(e)==expected
   e.screenshot(ROOT/f'test-output/gym-capacity-{city}-{mode}-case.png')
   e.press('B',180);e.press('B',180);e.press('B',90)
   closed=preserved(e)
   assert not e.read('sLockFieldControls',1)
   assert closed[:3]==claimed[:3] and closed[4:]==claimed[4:]
   # The TM Case normally sorts multiple TMs; quantities and progress matter.
   assert Counter(x for x in closed[3] if x[0])==Counter(x for x in claimed[3] if x[0])
   print(f'PASS: {city} {mode}: Trainer Card shows only earned badges; claimed TM Case opens and closes without changing rewards/progress',flush=True)
finally:e.close()
