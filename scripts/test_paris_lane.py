"""Walk the residential lane from an older Paris save and cold-load there."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved
import struct
raw=struct.unpack('<2944H',(ROOT/'data/layouts/EuropeParis/map.bin').read_bytes())
def checkmap(e):
 w=e.read('VMap');base=e.read(e.symbols['VMap']+8)
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(46) for x in range(64))==raw

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'paris-realism-save',True);checkmap(e);before=preserved(e)[1:]
 for p in [(39,40),(45,39),(55,39),(60,39),(60,43),(50,43),(40,43),(50,40)]:go(e,p)
 e.screenshot(ROOT/'test-output/paris-lane-neighborhood-homes.png')
 for x in (45,55):
  go(e,(x,39));e.walk('UP',1);assert e.location()==(43,4,x,39)
 for x in (43,55):
  go(e,(x,42));snapshot=preserved(e);e.press('UP');e.press('A',180)
  e.frames(120);e.screenshot(ROOT/f'test-output/paris-lane-neighborhood-sign-{x}.png')
  e.finish_dialogue();assert not e.read('sLockFieldControls',1) and preserved(e)==snapshot
 assert preserved(e)[1:]==before
 go(e,(60,43));save(e,'paris-lane-neighborhood-save');saved=preserved(e)
 print('PASS: old Paris battery refresh, new home approaches, solid doors, complete lane loop and signs preserve progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'paris-lane-neighborhood-save',True);checkmap(e)
 assert e.location()==(43,4,60,43) and preserved(e)==saved
 go(e,(33,38));go(e,(26,38));go(e,(13,42));go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180)
 assert e.location()[:2]==(43,5)
 print('PASS: expanded-lane Save/cold Continue retains position and progress; return to gardens, river crossings and countryside',flush=True)
finally:e.close()
