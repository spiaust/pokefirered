"""Native dock notice request, reading, captain confirmation and free care."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_dock_check import STORY,worker,notice
from test_le_havre import captain,clerk,PORT
from test_dock_care import rest
from test_time import preserved
from key_item_test_helpers import reload
from test_country import wait_menu

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/dock-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'havre-directions-returned',True);assert e.var(STORY)==0 and e.var(0x40DB)==2
 notice(e);assert e.var(STORY)==0
 for choice in ['B','NO']:worker(e,choice);assert e.var(STORY)==0
 e.walk('UP',2);e.walk('RIGHT',1);before=preserved(e);e.press('RIGHT');e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);pages(e,2,'active')
 assert e.var(STORY)==1 and preserved(e)==before;e.walk('LEFT',1);e.walk('DOWN',2)
 e=reload(e,'dock-directions-active');worker(e);captain(e,'B');assert e.var(STORY)==1
 print('PASS: early notice and optional dock No/B preserve unstarted task; actual request/two direction pages/cold Continue retain active task and early captain gate',flush=True)
 e.walk('UP',2);before=preserved(e);e.press('UP');e.press('A',180);pages(e,6,'notice')
 assert e.var(STORY)==2 and preserved(e)==before;e.walk('DOWN',2)
 e=reload(e,'dock-directions-noted');notice(e);worker(e);assert e.var(STORY)==2
 print('PASS: six native posted-notice and ready pages locate captain; actual read, repeated notice/worker and cold Continue retain unconfirmed instructions',flush=True)
 captain(e,'B');assert e.var(STORY)==3 and e.location()==PORT
 e=reload(e,'dock-directions-confirmed')
 for choice in ['B','NO']:rest(e,choice);captain(e,choice);assert e.var(STORY)==3
 rest(e);captain(e,'YES');clerk(e);assert e.location()==PORT and e.var(STORY)==3
 e=reload(e,'dock-directions-rested');rest(e);assert e.var(STORY)==3
 print('PASS: native captain confirmation unlocks free care; rest/return No/B, actual care, Rouen round trip and cold Continue retain completion',flush=True)
finally:e.close()
