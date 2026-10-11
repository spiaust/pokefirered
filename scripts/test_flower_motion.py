"""Native flower motion preference, independent visibility, reset and cold save."""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item, start_action
from test_navigation import wait_task
from test_time import preserved

VAR = 0x40c5

def tiles(e, start, length):
 return bytes(e.read(0x06000000 + start + i, 1) for i in range(length))

def grid(e):
 p=e.read(e.symbols['VMap']+8);w=e.read('VMap');h=e.read(e.symbols['VMap']+4)
 return tuple(e.read(p+2*i,2) for i in range(w*h))

def options(e, row):
 open_key_item(e,363);wait_task(e,'Task_EuropeMap')
 for _ in range(row): e.press('DOWN',60)

def close(e):
 for wait in (180,180,90): e.press('B',wait)
 assert not e.read('sLockFieldControls',1)

def flower_frames(e):
 result=[]
 for _ in range(10):
  e.frames(16);result.append(tiles(e,508*32,128))
 return result

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True)
 assert e.var(VAR)==0 and e.var(0x40c3)==0
 before=preserved(e);loc=e.location();terrain=grid(e)
 assert len(set(flower_frames(e)))>1
 options(e,5);e.press('RIGHT',60);assert e.var(VAR)==1
 e.screenshot(ROOT/'test-output/flower-motion-menu.png');close(e)
 assert len(set(flower_frames(e)))==1
 water=tiles(e,416*32,1536);e.frames(32)
 assert water!=tiles(e,416*32,1536)
 assert grid(e)==terrain and preserved(e)==before and e.location()==loc
 e.screenshot(ROOT/'test-output/flower-motion-still.png')
 options(e,3);e.press('RIGHT',60);close(e)
 assert e.var(VAR)==1 and e.var(0x40c3)==1 and grid(e)==terrain
 options(e,3);e.press('LEFT',60);close(e)
 assert e.var(VAR)==1 and e.var(0x40c3)==0
 start_action(e,4)
 for _ in range(5):e.press('A',150)
 e.battery(ROOT/'test-output/flower-motion-save.sav');saved=preserved(e)
 print('PASS: flowers freeze, water continues, visibility independent, terrain and progress unchanged',flush=True)
finally:e.close()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'flower-motion-save',True)
 assert e.var(VAR)==1 and preserved(e)==saved and e.location()==loc
 assert len(set(flower_frames(e)))==1
 options(e,5);e.press('LEFT',60);close(e)
 assert e.var(VAR)==0 and len(set(flower_frames(e)))>1
 options(e,5);e.press('A',60);close(e);assert e.var(VAR)==1
 options(e,8);e.press('A',60);e.press('B',60);assert e.var(VAR)==1
 e.press('A',60);e.press('A',60);close(e)
 assert e.var(VAR)==0 and len(set(flower_frames(e)))>1
 assert grid(e)==terrain and preserved(e)==saved and e.location()==loc
 e.screenshot(ROOT/'test-output/flower-motion-reset.png')
 print('PASS: native save/cold Continue, Left/A toggle and cancelled/confirmed defaults restore motion',flush=True)
finally:e.close()
