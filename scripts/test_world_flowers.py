"""World Options flower rendering, wrapping, cold saves and unchanged gameplay."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item,start_action
from test_navigation import wait_task
from test_landmark_cases import go
from test_time import preserved
VAR=0x40c3
def who(e):
 p=e.read('gSaveBlock2Ptr');return bytes(e.read(p+i,1) for i in range(14))
def grid(e):
 p=e.read(e.symbols['VMap']+8);w=e.read('VMap');h=e.read(e.symbols['VMap']+4)
 return tuple(e.read(p+2*i,2) for i in range(w*h))
def options(e):
 open_key_item(e,363);wait_task(e,'Task_EuropeMap');assert e.read('sWorldOptions',1)
def close(e):
 e.press('B',180);e.press('B',180);e.press('B',90);assert not e.read('sLockFieldControls',1)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);assert e.var(VAR)==0
 go(e,(8,24));loc=e.location();before=preserved(e);identity=who(e);tiles=grid(e)
 e.screenshot(ROOT/'test-output/world-flowers-on.png')
 options(e)
 for _ in range(6):e.press('UP',60) # Wrap past Restore Defaults, motion and outfit to flowers.
 e.press('RIGHT',60);assert e.var(VAR)==1
 e.screenshot(ROOT/'test-output/world-flowers-options.png');close(e)
 assert e.location()==loc and grid(e)==tiles and preserved(e)==before and who(e)==identity
 e.screenshot(ROOT/'test-output/world-flowers-off.png')
 go(e,(10,24));go(e,(8,24));assert grid(e)==tiles and preserved(e)[1:]==before[1:]
 start_action(e,4)
 for _ in range(5):e.press('A',150)
 e.battery(ROOT/'test-output/world-flowers-save.sav');saved=preserved(e)
 print('PASS: fourth-row wrap, flowers off, unchanged map grid/identity/progress and walking across the beds',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-flowers-save',True)
 assert e.var(VAR)==1 and e.location()==loc and preserved(e)==saved and who(e)==identity
 assert grid(e)==tiles
 e.screenshot(ROOT/'test-output/world-flowers-off-reloaded.png')
 options(e)
 for _ in range(3):e.press('DOWN',60)
 e.press('LEFT',60);assert e.var(VAR)==0
 e.press('A',60);assert e.var(VAR)==1
 e.press('RIGHT',60);assert e.var(VAR)==0
 close(e);assert grid(e)==tiles and e.location()==loc and preserved(e)==saved
 e.screenshot(ROOT/'test-output/world-flowers-restored.png')
 print('PASS: lawn preference cold-loads; Left/A/Right restore flowers without changing terrain or saved progress',flush=True)
finally:e.close()
