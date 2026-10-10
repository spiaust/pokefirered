from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from key_item_test_helpers import reload
import struct
def grid(e):
 w=e.read('VMap');base=e.read(e.symbols['VMap']+8);expected=struct.unpack('<1536H',(ROOT/'data/layouts/EuropeOxford/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(24) for x in range(64))==expected
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'oxford-bridges-complete',True);grid(e);before=preserved(e)[1:]
 go(e,(15,10));e.screenshot(ROOT/'test-output/oxford-roof-front.png');saved=preserved(e),e.location();e=reload(e,'oxford-roof-front');assert (preserved(e),e.location())==saved;grid(e)
 e.walk('UP',1);e.frames(180);assert e.location()==(43,24,6,14)
 e.walk('DOWN',10);e.frames(180);assert e.location()==(43,12,15,10);grid(e)
 assert preserved(e)[1:]==before
 print('PASS: earlier earned save refreshes slate roof; native front save/cold Continue and Gym door round trip preserve progress',flush=True)
 for point in [(6,10),(23,10),(38,10),(54,10),(46,18)]:go(e,point)
 go(e,(18,14));e=reload(e,'oxford-roof-complete');grid(e);assert preserved(e)[1:]==before
 e.press('DOWN');e.press('A',900);e.finish_dialogue();assert preserved(e)[1:]==before
 print('PASS: clinic/station/landmark paths and saved Ada ending repeat retain completed quests and rewards',flush=True)
finally:e.close()
