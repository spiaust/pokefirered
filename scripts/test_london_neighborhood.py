"""Walk the residential lane from an older London save and cold-load there."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved
import struct
raw=struct.unpack('<2816H',(ROOT/'data/layouts/EuropeLondon/map.bin').read_bytes())
def checkmap(e):
 w=e.read('VMap');base=e.read(e.symbols['VMap']+8)
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(44) for x in range(64))==raw

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);checkmap(e);before=preserved(e)[1:]
 for p in [(39,36),(45,33),(55,33),(60,33),(60,40),(50,40),(40,40),(50,34)]:go(e,p)
 e.screenshot(ROOT/'test-output/london-neighborhood-homes.png')
 for x in (45,55):
  go(e,(x,33));e.walk('UP',1);assert e.location()==(43,0,x,33)
 for x in (43,55):
  go(e,(x,36));snapshot=preserved(e);e.press('UP');e.press('A',180)
  e.frames(120);e.screenshot(ROOT/f'test-output/london-neighborhood-sign-{x}.png')
  e.finish_dialogue();assert not e.read('sLockFieldControls',1) and preserved(e)==snapshot
 assert preserved(e)[1:]==before
 go(e,(60,40));save(e,'london-neighborhood-save');saved=preserved(e)
 print('PASS: old London battery refresh, new home approaches, solid doors, complete lane loop and signs preserve progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'london-neighborhood-save',True);checkmap(e)
 assert e.location()==(43,0,60,40) and preserved(e)==saved
 go(e,(29,29));go(e,(20,28));go(e,(22,38));go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180)
 assert e.location()[:2]==(43,1)
 print('PASS: expanded-lane Save/cold Continue retains position and progress; return to Eye, both bridges and countryside',flush=True)
finally:e.close()
