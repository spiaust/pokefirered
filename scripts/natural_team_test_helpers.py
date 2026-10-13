"""Native capture and lead selection; no battle or party memory writes."""
from emulator import ROOT
import test_eclipse_natural as natural
from test_shadow_runtime import monfield
from test_oxford_gym import count_pocket
from test_navigation import wait_task
from test_gym_ui import start_action

def capture(e):
 action=natural.first_symbol('HandleInputChooseAction');before=e.read('gPlayerPartyCount',1)
 for attempt in range(10):
  for _ in range(150):
   if e.read('gBattlerControllerFuncs')&~1==action:break
   e.press('A',30)
  assert count_pocket(e,4,0x430,13)>0,'no Balls remain'
  e.press('UP',2);e.press('LEFT',2);e.press('RIGHT',2);e.press('A',180)
  wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
  for _ in range(5):
   pocket=e.read(bag+6,2)
   if pocket==2:break
   e.press('RIGHT' if pocket<2 else 'LEFT',60)
  e.press('A',90);e.press('A',180)
  for _ in range(150):
   if e.read('gPlayerPartyCount',1)>before:
    for _ in range(30):
     if not e.in_battle():break
     if e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_NamingScreen']&~1:e.press('START',30);e.press('A',120)
     else:e.press('B',90);e.press('A',90)
    e.finish_dialogue();e.frames(180)
    assert not e.in_battle()
    print('PASS: partner caught with native full HP, catch rate and',attempt+1,'Ball attempts.',flush=True)
    return 7,attempt+1
   if e.read('gBattlerControllerFuncs')&~1==action:break
   e.press('A',30)
 raise AssertionError('partner capture failed')

def lead(e,index):
 start_action(e,1);wait_task(e,'Task_HandleChooseMonInput')
 for _ in range(12):
  cur=e.read(e.symbols['gPartyMenu']+9,1)
  if cur==index:break
  e.press('RIGHT' if cur==0 else 'DOWN' if cur<index else 'UP',30)
 assert cur==index
 e.press('A',60);wait_task(e,'Task_HandleSelectionMenuInput');e.frames(120)
 # Field moves can appear before Switch, so inspect the native action list.
 menu=e.read('sPartyMenuInternal');count=e.read(menu+23,1)
 target=next(i for i in range(count) if e.read(menu+15+i,1)==1)
 for _ in range(8):
  cursor=e.read(e.symbols['sMenu']+2,1)
  if cursor==target:break
  e.press('DOWN' if cursor<target else 'UP',30)
 assert e.read(e.symbols['sMenu']+2,1)==target
 e.press('A',120)
 wait_task(e,'Task_HandleChooseMonInput');e.frames(120)
 # Switch mode uses slotId2 as the destination; slotId remains the source.
 e.press('LEFT',60)
 assert e.read(e.symbols['gPartyMenu']+10,1)==0
 e.press('A',180);wait_task(e,'Task_HandleChooseMonInput')
 for _ in range(8):e.press('B',180)
 e.frames(180)
 assert not e.task_active('Task_HandleChooseMonInput') and not e.read('sLockFieldControls',1)

