"""Eiffel visits, exhibits, both exits and indoor Save/cold Continue."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
inside=groups['gMapGroup_Europe'].index('EuropeEiffelVisitor')
def read(e,point,label):
 go(e,point);e.press('UP');e.press('A',180)
 assert e.read('sLockFieldControls',1),label
 e.screenshot(ROOT/f'test-output/eiffel-visitor-{label}.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'start-france',True);before=preserved(e)[1:]
 for choice in ['NO','B']:
  talk(e,(9,37),choice=choice);assert e.location()==(43,4,9,37)
 talk(e,(9,37),choice='YES');assert e.location()==(43,inside,5,7)
 e.screenshot(ROOT/'test-output/eiffel-visitor-interior.png')
 read(e,(8,4),'guide');read(e,(3,4),'garden-exhibit');read(e,(11,4),'river-exhibit')
 assert not e.read('sLockFieldControls',1) and preserved(e)[1:]==before
 go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,4,9,37)
 talk(e,(9,37),choice='YES');go(e,(9,7));save(e,'eiffel-visitor-save');saved=preserved(e)
 print('PASS: Eiffel No/B, entry, guide, both exhibits, exit and re-entry preserve progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'eiffel-visitor-save',True)
 assert e.location()==(43,inside,9,7) and preserved(e)==saved
 read(e,(11,4),'river-exhibit-reloaded');go(e,(4,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,4,9,37)
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180)
 assert e.location()[:2]==(43,5)
 print('PASS: Eiffel visitor Save/cold Continue, second exit tile and return to countryside',flush=True)
finally:e.close()
