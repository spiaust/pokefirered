"""London Eye gallery visits, displays, exits and indoor Save/cold Continue."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
inside=groups['gMapGroup_Europe'].index('EuropeLondonEyeGallery')
def read(e,point,label):
 go(e,point);e.press('UP');e.press('A',180)
 assert e.read('sLockFieldControls',1),label
 e.screenshot(ROOT/f'test-output/eye-gallery-{label}.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'start-england',True);before=preserved(e)[1:]
 for choice in ['NO','B']:
  talk(e,(29,29),choice=choice);assert e.location()==(43,0,29,29)
 talk(e,(29,29),choice='YES');assert e.location()==(43,inside,5,7)
 e.screenshot(ROOT/'test-output/eye-gallery-interior.png')
 read(e,(6,4),'attendant');read(e,(2,4),'garden-panel');read(e,(10,4),'bridge-panel')
 assert not e.read('sLockFieldControls',1) and preserved(e)[1:]==before
 go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,0,29,29)
 talk(e,(29,29),choice='YES');go(e,(9,7));save(e,'eye-gallery-save');saved=preserved(e)
 print('PASS: London Eye No/B, entry, attendant, both displays, exit and re-entry preserve progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'eye-gallery-save',True)
 assert e.location()==(43,inside,9,7) and preserved(e)==saved
 read(e,(10,4),'bridge-panel-reloaded');go(e,(4,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,0,29,29)
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180)
 assert e.location()[:2]==(43,1)
 print('PASS: London Eye gallery Save/cold Continue, second exit tile and return to countryside',flush=True)
finally:e.close()
