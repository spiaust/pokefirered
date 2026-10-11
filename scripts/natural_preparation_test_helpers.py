"""Native TM learning and held-item support for earned-party preparation."""
from test_shadow_runtime import monfield
from tm_teaching_test_helpers import select,field
from test_eclipse_natural_zurich import advance
from test_navigation import wait_task
from test_gym_ui import start_action
from test_oxford_gym import count_pocket

def choose(e,index):
 for _ in range(12):
  cur=e.read(e.symbols['gPartyMenu']+9,1)
  if cur==index:break
  e.press('LEFT' if index==0 else 'RIGHT' if cur==0 else 'DOWN' if cur<index else 'UP',60)
 assert cur==index

def teach(e,species,tm,move,slot,reusable=False):
 index=next(i for i in range(e.read('gPlayerPartyCount',1)) if monfield(e,i,0,0)&65535==species)
 old=[monfield(e,index,1,j)&65535 for j in (0,2,4,6)]
 assert count_pocket(e,tm,0x464,58)
 select(e,tm);choose(e,index);e.press('A',900)
 advance(e,'Task_HandleReplaceMoveYesNoInput');e.press('A',180)
 advance(e,'Task_InputHandler_SelectOrForgetMove')
 for _ in range(8):
  cur=e.read('sMoveSelectionCursorPos',1)
  if cur==slot:break
  e.press('DOWN' if cur<slot else 'UP',60)
 assert cur==slot;e.press('A',900)
 for _ in range(15):
  if not count_pocket(e,tm,0x464,58):break
  e.press('A',180)
 e.press('A',180);field(e);old[slot]=move
 assert [monfield(e,index,1,j)&65535 for j in (0,2,4,6)]==old
 assert count_pocket(e,tm,0x464,58)==(1 if reusable else 0)
 print('Earned TM learned:',species,tm,move,flush=True)

def give(e,species,item):
 assert count_pocket(e,item,0x310,42)
 start_action(e,2);wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
 for _ in range(5):
  if e.read(bag+6,2)==0:break
  e.press('LEFT',90)
 base=e.read('gSaveBlock1Ptr')+0x310;target=next(i for i in range(42) if e.read(base+4*i,2)==item)
 for _ in range(60):
  cur=e.read(bag+8,2)+e.read(bag+14,2)
  if cur==target:break
  e.press('DOWN' if cur<target else 'UP',30)
 assert cur==target;e.press('A',90);e.press('DOWN',60);e.press('A',180)
 wait_task(e,'Task_HandleChooseMonInput')
 index=next(i for i in range(e.read('gPlayerPartyCount',1)) if monfield(e,i,0,0)&65535==species)
 choose(e,index);e.press('A',180)
 for _ in range(6):e.press('A',90)
 field(e);assert monfield(e,index,0,0)>>16==item and not count_pocket(e,item,0x310,42)
 print('Native held item given:',species,item,flush=True)
