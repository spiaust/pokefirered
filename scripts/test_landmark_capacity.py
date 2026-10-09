"""Native recovery from explicitly prepared pocket boundary fixtures; no writes."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import talk
from test_gym_ui import start_action
from test_navigation import wait_task
from test_time import preserved
from key_item_test_helpers import reload
from landmark_capacity_test_helpers import CASES

def count(e,item):return sum(q for i,q in preserved(e)[3] if i==item)
def toss(e,pocket,amount):
 e.press('A',90);wait_task(e,'Task_FieldItemContextMenuHandleInput')
 for _ in range(2 if pocket==0 else 1):e.press('DOWN')
 e.press('A',180)
 if e.task_active('Task_SelectQuantityToToss'):
  for _ in range(amount-1):e.press('UP')
  e.press('A',180)
 else:assert amount==1

e=Emulator(ROOT/'pokefirered.gba')
try:
 for label,tag,var,reward,qty,pocket,mode in CASES:
  name='landmark-capacity-'+label;load_checkpoint(e,name+'-fixture',True);assert e.var(var)==5
  before=preserved(e);e.press('UP');e.press('A',180);e.frames(900)
  for i in range(4):
   assert e.read('sLockFieldControls',1);e.screenshot(ROOT/f'test-output/{name}-help-{i}.png');e.press('A',900)
  e.finish_dialogue();talk(e,(8,15));assert preserved(e)==before and e.var(var)==5
  e=reload(e,name+'-pending');talk(e,(8,15));assert preserved(e)==before
  print('PASS: '+label+' four pocket-help pages, repeated curator and cold Continue preserve resolved case and pending reward',flush=True)
  start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
  for _ in range(5):
   current=e.read(bag+6,2)
   if current==pocket:break
   e.press('RIGHT' if current<pocket else 'LEFT',90)
  assert e.read(bag+6,2)==pocket
  cursor,scroll=(8,14) if pocket==0 else (12,18)
  for _ in range(45):
   current=e.read(bag+cursor,2)+e.read(bag+scroll,2)
   if current==0:break
   e.press('UP')
  assert current==0
  offset=0x310 if pocket==0 else 0x430;target=e.read(e.read('gSaveBlock1Ptr')+offset,2);n=count(e,target);amount=qty if mode=='capped' else 1
  toss(e,pocket,amount);e.press('B',180);wait_task(e,'Task_BagMenu_HandleInput');assert preserved(e)==before
  toss(e,pocket,amount);e.press('A',180);wait_task(e,'Task_WaitAB_RedrawAndReturnToBag');e.press('A',180);wait_task(e,'Task_BagMenu_HandleInput')
  assert count(e,target)==n-amount;e.press('B',180);e.press('B',90);room=preserved(e)
  assert room[:3]==before[:3] and room[4:]==before[4:] and e.var(var)==5
  e=reload(e,name+'-room');assert preserved(e)==room
  print('PASS: '+label+' native Toss B cancels unchanged; confirmation removes exactly '+str(amount)+' and saved room keeps reward pending',flush=True)
  n=count(e,reward);talk(e,(8,15));assert e.var(var)==6 and count(e,reward)==n+qty
  claimed=preserved(e);talk(e,(8,15));assert preserved(e)==claimed
  e=reload(e,name+'-claimed');talk(e,(8,15));assert preserved(e)==claimed
  print('PASS: '+label+' normal curator return grants exactly '+str(qty)+' earned item(s); repeated talk and cold Continue cannot duplicate reward',flush=True)
finally:e.close()
