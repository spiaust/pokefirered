"""Repeated native party swaps must release animation buffers and keep heap usage stable."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_navigation import wait_task
from test_shadow_runtime import monfield

def allocated(e):
 start=e.symbols['gHeap'];p=start;total=0
 for _ in range(1024):
  assert e.read(p+2,2)==0xa3a3,'invalid heap block'
  if e.read(p,2):total+=e.read(p+4)+16
  p=e.read(p+12)
  if p==start:return total
 raise AssertionError('heap chain did not terminate')

def swap(e):
 for _ in range(8):
  cur=e.read(e.symbols['gPartyMenu']+9,1)
  if cur==1:break
  e.press('RIGHT' if cur==0 else 'UP',60)
 assert cur==1;e.press('A',90);wait_task(e,'Task_HandleSelectionMenuInput');e.frames(120)
 e.press('DOWN',60);e.press('A',120);wait_task(e,'Task_HandleChooseMonInput');e.frames(120)
 e.press('LEFT',60);assert e.read(e.symbols['gPartyMenu']+10,1)==0
 e.press('A',180);e.frames(300);wait_task(e,'Task_HandleChooseMonInput')
 assert e.read('sSlot1TilemapBuffer')==0 and e.read('sSlot2TilemapBuffer')==0,'animation buffers retained'

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'natural-caught-brussels',True);assert e.read('gPlayerPartyCount',1)==2
 before=[monfield(e,i,0,0)&0xffff for i in range(2)]
 start_action(e,1);wait_task(e,'Task_HandleChooseMonInput');e.frames(120)
 swap(e);baseline=allocated(e)
 for i in range(19):
  swap(e);assert allocated(e)==baseline,(i,'heap grew',baseline,allocated(e))
 for _ in range(8):e.press('B',180)
 assert not e.read('sLockFieldControls',1)
 assert [monfield(e,i,0,0)&0xffff for i in range(2)]==before
 e.screenshot(ROOT/'test-output/eclipse-party-memory.png')
 print('PASS: 20 native party swaps retain neither animation buffer, keep allocated heap stable and preserve party order.',flush=True)
finally:e.close()
