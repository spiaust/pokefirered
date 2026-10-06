"""Button-input Gate visitor room visits, conversations, exits and cold saves."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved
from test_gym_ui import open_key_item
from test_navigation import wait_task
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
inside=groups['gMapGroup_Europe'].index('EuropeGateVisitor')
def read(e,point,label):
 go(e,point);e.press('UP');e.press('A',180)
 assert e.read('sLockFieldControls',1),label
 e.screenshot(ROOT/f'test-output/gate-visitor-{label}.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'start-germany',True);before=preserved(e)[1:]
 for choice in ['NO','B']:
  talk(e,(19,37),choice=choice);assert e.location()==(43,8,19,37)
 talk(e,(19,37),choice='YES');assert e.location()==(43,inside,5,7)
 e.screenshot(ROOT/'test-output/gate-visitor-interior.png')
 read(e,(8,4),'guide');read(e,(3,4),'garden-panel');read(e,(11,4),'court-panel')
 assert not e.read('sLockFieldControls',1) and preserved(e)[1:]==before
 go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,8,19,37)
 talk(e,(19,37),choice='YES');go(e,(9,7));save(e,'gate-visitor-save');saved=preserved(e)
 print('PASS: Gate room No/B, entry, guide and both displays, exit and re-entry preserve progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'gate-visitor-save',True)
 assert e.location()==(43,inside,9,7) and preserved(e)==saved
 open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapCurrent',1)==2
 e.screenshot(ROOT/'test-output/gate-visitor-regional-map.png')
 e.press('B',180);e.press('B',180);e.press('B',90)
 assert preserved(e)==saved
 read(e,(11,4),'court-panel-reloaded');go(e,(4,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,8,19,37)
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180)
 assert e.location()[:2]==(43,9)
 print('PASS: Gate-room Save/cold Continue, Germany map label, second exit tile and return to countryside',flush=True)
finally:e.close()
