"""Button-input garden workroom visits, conversations, exits and cold saves."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
inside=groups['gMapGroup_Europe'].index('EuropeBerlinGardenRoom')
def read(e,point,label,facing='UP'):
 go(e,point);e.press(facing);before_read=preserved(e);e.press('A',180)
 assert e.read('sLockFieldControls',1),label
 e.screenshot(ROOT/f'test-output/berlin-garden-room-{label}.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1)
 assert preserved(e)==before_read, (label,'reading changed party or progress')
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'start-germany',True);before=preserved(e)[1:]
 for choice in ['NO','B']:
  talk(e,(58,32),choice=choice);assert e.location()==(43,8,58,32)
 talk(e,(58,32),choice='YES');assert e.location()==(43,inside,5,7)
 e.screenshot(ROOT/'test-output/berlin-garden-room-interior.png')
 read(e,(2,4),'seed-notes','DOWN');read(e,(10,4),'watering-notes','DOWN');read(e,(8,4),'gardener');read(e,(3,4),'tools');read(e,(11,4),'planting-plan')
 assert not e.read('sLockFieldControls',1) and preserved(e)[1:]==before
 go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,8,58,32)
 talk(e,(58,32),choice='YES');go(e,(9,7));save(e,'berlin-garden-room-save');saved=preserved(e)
 print('PASS: garden room No/B, entry, gardener, tools and plan, exit and re-entry preserve progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'berlin-garden-room-save',True)
 assert e.location()==(43,inside,9,7) and preserved(e)==saved
 read(e,(11,4),'planting-plan-reloaded');go(e,(4,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,8,58,32)
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180)
 assert e.location()[:2]==(43,9)
 print('PASS: garden-room Save/cold Continue, second exit tile and return to countryside',flush=True)
finally:e.close()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'berlin-garden-room-v097',True)
 assert e.location()==(43,inside,9,7);before=preserved(e)[1:]
 for point,label,facing in [((2,4),'seed-old-save','DOWN'),((10,4),'watering-old-save','DOWN'),((2,7),'seed-south-old-save','UP'),((10,7),'watering-south-old-save','UP')]:read(e,point,label,facing)
 # Walking can trigger the native friendship step update; each read above
 # independently checks the complete party bytes and progress.
 assert preserved(e)[1:]==before
 go(e,(4,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,8,58,32)
 print('PASS: v0.97 indoor battery reads both bench notes from north/south and exits with progress retained',flush=True)
finally:e.close()
