"""Live menu preview colors, avatar swaps, confirmation and field cleanup."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved
def preview(e):
 i=e.read('sWorldPreviewSpriteId',1);assert i<64
 return i
def close(e):
 e.press('B',180);e.press('B',180);e.press('B',90)
 assert e.read('sWorldPreviewSpriteId',1)==64 and not e.read('sLockFieldControls',1)
def outfit(e,color):
 expected={1:(5|(7<<5)|(13<<10),11|(22<<5)|(29<<10),8|(13<<5)|(24<<10)),2:(4|(11<<5)|(6<<10),14|(26<<5)|(16<<10),7|(18<<5)|(10<<10))}[color]
 actual=tuple(e.read(e.symbols['gPlttBufferUnfaded']+2*(256+i),2) for i in (8,11,12))
 assert actual==expected,(actual,expected,e.var(0x40c4),e.read('gReservedSpritePaletteCount',1),hex(e.read(e.symbols['gSprites']+preview(e)*68+4,2)))
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);before=preserved(e);loc=e.location()
 open_key_item(e,363);wait_task(e,'Task_EuropeMap');preview(e)
 e.press('DOWN',60);e.press('LEFT',60);assert e.var(0x40d3)==1;preview(e)
 for _ in range(3):e.press('DOWN',60)
 e.press('RIGHT',60);outfit(e,1);preview(e)
 e.screenshot(ROOT/'test-output/world-preview-blue-red.png')
 e.press('RIGHT',60);outfit(e,2);preview(e)
 for _ in range(3):e.press('UP',60)
 e.press('RIGHT',60);assert e.var(0x40d3)==2;preview(e);outfit(e,2)
 e.screenshot(ROOT/'test-output/world-preview-green-leaf.png')
 prefs=tuple(e.var(v) for v in (0x40d2,0x40d3,0x40d4,0x40c3,0x40c4))
 e.press('SELECT',60);assert e.read('sWorldPreviewBike',1)==1;preview(e);outfit(e,2)
 assert tuple(e.var(v) for v in (0x40d2,0x40d3,0x40d4,0x40c3,0x40c4))==prefs
 e.screenshot(ROOT/'test-output/world-preview-bike-leaf.png')
 for _ in range(12):
  e.press('RIGHT',60);preview(e);outfit(e,2)
 assert e.var(0x40d3)==2
 assert e.read('sWorldPreviewBike',1)==1
 e.press('SELECT',60);assert e.read('sWorldPreviewBike',1)==0;outfit(e,2)
 e.press('UP',60);e.press('UP',60);e.press('A',60)
 e.screenshot(ROOT/'test-output/world-preview-confirm.png')
 e.press('B',60);preview(e);outfit(e,2)
 e.press('A',60);e.press('A',60);preview(e);assert e.var(0x40c4)==0 and e.var(0x40d3)==0
 e.screenshot(ROOT/'test-output/world-preview-defaults.png');close(e)
 assert preserved(e)==before and e.location()==loc
 open_key_item(e,363);wait_task(e,'Task_EuropeMap');assert e.read('sWorldPreviewBike',1)==0;close(e)
 open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sWorldPreviewSpriteId',1)==64
 e.screenshot(ROOT/'test-output/world-preview-regional-map.png');close(e)
 print('PASS: walking/cycling toggle, live Red/Leaf outfit preview, restore confirmation/cancel, default preview and clean map/field return',flush=True)
finally:e.close()
