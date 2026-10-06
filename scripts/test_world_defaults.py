"""Confirmed cosmetic reset, cancellation, field return and saved defaults."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item,start_action
from test_navigation import wait_task
from test_time import preserved
def prefs(e):return tuple(e.var(v) for v in (0x40d4,0x40d3,0x40d2,0x40c3,0x40c4))
def who(e):
 p=e.read('gSaveBlock2Ptr');return bytes(e.read(p+i,1) for i in range(14))
def close(e):
 e.press('B',180);e.press('B',180);e.press('B',90);assert not e.read('sLockFieldControls',1)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-flowers-save',True)
 assert prefs(e)==(1,2,1,1,0)
 before=preserved(e);identity=who(e);loc=e.location()
 open_key_item(e,363);wait_task(e,'Task_EuropeMap');e.press('UP',60);e.press('UP',60);e.press('RIGHT',60);e.press('DOWN',60)
 e.press('LEFT',60);e.press('RIGHT',60);assert prefs(e)==(1,2,1,1,1)
 for cancel in ('B','START'):
  e.press('A',60);e.press(cancel,60)
  assert e.task_active('Task_EuropeMap') and prefs(e)==(1,2,1,1,1)
 e.press('A',60);e.screenshot(ROOT/'test-output/world-defaults-confirm.png')
 assert prefs(e)==(1,2,1,1,1)
 e.press('A',60);assert prefs(e)==(0,0,0,0,0)
 e.screenshot(ROOT/'test-output/world-defaults-menu.png');close(e)
 assert e.location()==loc and preserved(e)==before and who(e)==identity
 assert e.read(e.symbols['gPlayerAvatar']+7,1)==e.read(e.read('gSaveBlock2Ptr')+8,1)
 start_action(e,4)
 for _ in range(5):e.press('A',150)
 e.battery(ROOT/'test-output/world-defaults-save.sav');saved=preserved(e)
 print('PASS: sixth-row wrap, Left/Right ignored, B/START cancellation and confirmed cosmetic-only reset',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-defaults-save',True)
 assert prefs(e)==(0,0,0,0,0) and e.location()==loc and who(e)==identity and preserved(e)==saved
 assert e.read(e.symbols['gPlayerAvatar']+7,1)==e.read(e.read('gSaveBlock2Ptr')+8,1)
 e.screenshot(ROOT/'test-output/world-defaults-reloaded.png')
 print('PASS: normal Save/cold Continue retains restored defaults, original avatar and unchanged identity/progress',flush=True)
finally:e.close()
