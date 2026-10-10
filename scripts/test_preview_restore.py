"""Native default restoration resets cosmetics and preview; cancellation retains both."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved
from key_item_test_helpers import reload

def prefs(e):return tuple(e.var(v) for v in (0x40c3,0x40c4,0x40d2,0x40d3,0x40d4))
def view(e,bike,facing):
 assert e.read('sWorldPreviewBike',1)==bike and e.read('sWorldPreviewFacing',1)==facing
 i=e.read('sWorldPreviewSpriteId',1);assert i<64
 assert e.read(e.symbols['gSprites']+i*68+0x2a,1)==(0,2,1,3)[facing]
def close(e):
 for _ in range(4):e.press('B',180)
 assert not e.read('sLockFieldControls',1) and e.read('sWorldPreviewSpriteId',1)==64

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);before=preserved(e),e.location()
 open_key_item(e,363);wait_task(e,'Task_EuropeMap');e.frames(60)
 e.press('DOWN',60);e.press('LEFT',60)
 for _ in range(3):e.press('DOWN',60)
 e.press('RIGHT',60);settings=prefs(e);assert any(settings)
 e.press('SELECT',60);e.press('R',60);e.press('R',60);view(e,1,2)
 e.press('DOWN',60);e.press('A',60)
 for key in ['L','R','SELECT','LEFT','RIGHT']:e.press(key,60)
 assert prefs(e)==settings and e.read('sWorldPreviewBike',1)==1 and e.read('sWorldPreviewFacing',1)==2
 e.press('B',60);view(e,1,2);assert prefs(e)==settings
 e.screenshot(ROOT/'test-output/world-preview-restore-cancel.png')
 e.press('A',60);e.press('A',60);assert prefs(e)==(0,0,0,0,0);view(e,0,0)
 e.screenshot(ROOT/'test-output/world-preview-restore-confirmed.png');close(e)
 assert (preserved(e),e.location())==before
 e=reload(e,'world-preview-restore');assert prefs(e)==(0,0,0,0,0) and (preserved(e),e.location())==before
 open_key_item(e,363);wait_task(e,'Task_EuropeMap');e.frames(60);view(e,0,0);close(e)
 print('PASS: native cancellation retains custom settings/bicycle/facing; confirmation restores defaults/front walk, field state and cold Continue',flush=True)
finally:e.close()
