"""Native four-direction previews across avatars and poses without save edits."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved

def prefs(e):return tuple(e.var(v) for v in (0x40c3,0x40c4,0x40d2,0x40d3,0x40d4))
def facing(e,n):
 assert e.read('sWorldPreviewFacing',1)==n
 i=e.read('sWorldPreviewSpriteId',1);assert i<64
 assert e.read(e.symbols['gSprites']+i*68+0x2a,1)==(0,2,1,3)[n]
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);before=preserved(e);loc=e.location();help_r=e.read('gHelpSystemToggleWithRButtonDisabled',1)
 open_key_item(e,363);wait_task(e,'Task_EuropeMap');e.frames(60);facing(e,0)
 e.press('DOWN',60)
 for avatar in range(3):
  settings=prefs(e)
  for pose in range(2):
   for n in range(1,5):
    e.press('R',60);facing(e,n%4);assert prefs(e)==settings
    if avatar==0 and n in (1,2,3):e.screenshot(ROOT/f'test-output/world-preview-facing-{pose}-{n}.png')
   e.press('SELECT',60);facing(e,0)
  e.press('RIGHT',60)
 e.press('R',60);facing(e,1)
 e.press('UP',60);e.press('UP',60);e.press('A',60)
 e.press('R',60);assert e.read('sWorldPreviewFacing',1)==1
 e.press('B',60);facing(e,1)
 settings=prefs(e)
 e.press('B',180);e.press('B',180);e.press('B',90)
 assert preserved(e)==before and e.location()==loc and prefs(e)==settings
 assert e.read('gHelpSystemToggleWithRButtonDisabled',1)==help_r
 open_key_item(e,363);wait_task(e,'Task_EuropeMap');e.frames(60);facing(e,0)
 e.press('B',180);e.press('B',180);e.press('B',90)
 print('PASS: all avatar/pose facing animations, four-turn wrap, confirmation ignore/cancel, fresh front view and field Help/save continuity',flush=True)
finally:e.close()
