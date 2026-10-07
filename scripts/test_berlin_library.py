"""Reading-room visits, records, cold saves and older indoor-save compatibility."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
inside=groups['gMapGroup_Europe'].index('EuropeBerlinLibrary')
def read(e,point,label,facing='UP'):
 go(e,point);e.press(facing);e.press('A',180)
 assert e.read('sLockFieldControls',1),label
 e.screenshot(ROOT/f'test-output/berlin-library-{label}.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'start-germany',True);before=preserved(e)[1:]
 for choice in ['NO','B']:
  talk(e,(51,32),choice=choice);assert e.location()==(43,8,51,32)
 talk(e,(51,32),choice='YES');assert e.location()==(43,inside,5,7)
 e.screenshot(ROOT/'test-output/berlin-library-interior.png')
 read(e,(6,3),'catalog',facing='DOWN');read(e,(8,4),'librarian');read(e,(3,4),'garden-book');read(e,(11,4),'history-book')
 assert not e.read('sLockFieldControls',1) and preserved(e)[1:]==before
 go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,8,51,32)
 talk(e,(51,32),choice='YES');go(e,(9,7));save(e,'berlin-library-save');saved=preserved(e)
 print('PASS: reading room No/B, entry, librarian, both books, exit and re-entry preserve progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'berlin-library-save',True)
 assert e.location()==(43,inside,9,7) and preserved(e)==saved
 read(e,(11,4),'history-book-reloaded');go(e,(4,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,8,51,32)
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180)
 assert e.location()[:2]==(43,9)
 print('PASS: reading-room Save/cold Continue, second exit tile and return to countryside',flush=True)
finally:e.close()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'berlin-library-v066',True)
 assert e.location()==(43,inside,9,7)
 before=preserved(e)
 read(e,(6,3),'catalog-old-save',facing='DOWN');read(e,(6,6),'catalog-south-old-save');read(e,(8,4),'librarian-old-save')
 assert preserved(e)==before
 go(e,(5,7));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,8,51,32)
 talk(e,(51,32),choice='YES');assert e.location()==(43,inside,5,7)
 print('PASS: v0.66 reading-room battery save retains its map, records, progress and exit',flush=True)
finally:e.close()
