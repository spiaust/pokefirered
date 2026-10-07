"""Button-input home visits, cancellation, conversations and cold saves."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved
from test_gym_ui import open_key_item
from test_navigation import wait_task
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
inside=groups['gMapGroup_Europe'].index('EuropeLondonHome')
def read(e,point,label,facing='UP'):
 go(e,point);e.press(facing);e.press('A',180)
 assert e.read('sLockFieldControls',1),label
 e.screenshot(ROOT/f'test-output/london-home-{label}.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'london-home-v087',True)
 assert e.location()==(43,inside,9,7)
 old=preserved(e);read(e,(6,3),'album-old-save','DOWN')
 assert preserved(e)==old
 go(e,(4,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,0,45,33)
 print('PASS: v0.87 sitting-room battery reaches the album and exits with progress retained',flush=True)
finally:e.close()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);before=preserved(e)[1:]
 for choice in ['NO','B']:
  talk(e,(45,33),choice=choice);assert e.location()==(43,0,45,33)
 talk(e,(45,33),choice='YES');assert e.location()==(43,inside,5,7)
 e.screenshot(ROOT/'test-output/london-home-interior.png')
 read(e,(6,3),'album','DOWN');read(e,(8,5),'host');read(e,(3,4),'notebook')
 assert not e.read('sLockFieldControls',1) and preserved(e)[1:]==before
 go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,0,45,33)
 talk(e,(45,33),choice='YES');go(e,(9,7));save(e,'london-home-save');saved=preserved(e)
 print('PASS: home No/B, entry, host, notebook, exit and re-entry preserve progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'london-home-save',True)
 assert e.location()==(43,inside,9,7) and preserved(e)==saved
 open_key_item(e,361);wait_task(e,'Task_EuropeMap');e.frames(60);assert e.read('sEuropeMapCurrent',1)==0
 e.screenshot(ROOT/'test-output/london-home-map.png')
 e.press('B',180);e.press('B',180);e.press('B',90);assert preserved(e)==saved
 read(e,(3,4),'notebook-reloaded');go(e,(4,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,0,45,33)
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180)
 assert e.location()[:2]==(43,1)
 print('PASS: sitting-room Save/cold Continue, second exit tile and return to countryside',flush=True)
finally:e.close()
