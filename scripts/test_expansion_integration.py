"""Combine new appearance, live archive notes and Lapras saves; reset cosmetics only."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_landmark_cases import go
from test_ride import ride,dismount,SURF
from test_time import preserved
from key_item_test_helpers import reload
from walking_test_helpers import assert_walk_preserved
PREFS=(0x40d4,0x40d3,0x40d2,0x40c3,0x40c4,0x40c5,0x40c6,0x40c7)
def quest(e):return tuple(e.var(v) for v in range(0x40c8,0x40cd))
def close(e):
 for _ in range(4):e.press('B',180)
 assert not e.read('sLockFieldControls',1)
def rgb(r,g,b):return r|(g<<5)|(b<<10)
def check_palette(e):
 expected={2:rgb(13,8,6),3:rgb(8,4,3),8:rgb(12,7,2),11:rgb(31,26,8),12:rgb(24,15,3),13:rgb(11,22,29),14:rgb(8,13,24)}
 for slot,color in expected.items():assert e.read(e.symbols['gPlttBufferUnfaded']+2*(256+slot),2)==color,(slot,color)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'archive-4-5-oxford',True);notes=quest(e);assert notes==(1,1,0,0,1)
 go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 go(e,(19,12));e.press('UP');e.press('A',900)
 for _ in range(12):
  if e.task_active('Task_EuropeMap'):break
  e.press('A',900)
 wait_task(e,'Task_EuropeMap');e.press('B',180);e.press('B',90);e.finish_dialogue();assert quest(e)==notes
 before=preserved(e);open_key_item(e,363);wait_task(e,'Task_EuropeMap')
 for _ in range(6):e.press('DOWN',60)
 e.press('LEFT',60);e.press('DOWN',60);e.press('RIGHT',60)
 for _ in range(3):e.press('UP',60)
 e.press('LEFT',60)
 for _ in range(3):e.press('UP',60)
 e.press('LEFT',60);close(e)
 assert (e.var(0x40d3),e.var(0x40c4),e.var(0x40c6),e.var(0x40c7))==(2,4,4,1)
 check_palette(e);assert quest(e)==notes and preserved(e)==before
 go(e,(26,16));before=preserved(e);ride(e)
 assert e.read('gPlayerAvatar',1)&SURF and quest(e)==notes and preserved(e)==before
 check_palette(e);e.screenshot(ROOT/'test-output/expansion-integration-custom-lapras.png')
 e=reload(e,'expansion-integration-water');assert quest(e)==notes and e.read('gPlayerAvatar',1)&SURF;check_palette(e)
 dismount(e);before=preserved(e);open_key_item(e,363);wait_task(e,'Task_EuropeMap');e.press('UP',60)
 e.press('A',60);e.press('B',60);assert e.var(0x40c6)==4 and quest(e)==notes
 e.press('A',60);e.press('A',60);close(e)
 assert all(e.var(v)==0 for v in PREFS) and quest(e)==notes and preserved(e)==before
 e=reload(e,'expansion-integration-defaults');assert all(e.var(v)==0 for v in PREFS) and quest(e)==notes and preserved(e)==before
 print('PASS: Leaf/deep skin/gold outfit/blue accent work together on Lapras; native water Continue and cosmetic reset preserve active archive notes, main ending and player state',flush=True)
finally:e.close()
