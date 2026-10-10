from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved
from key_item_test_helpers import reload
import struct
def grid(e):
 w=e.read('VMap');base=e.read(e.symbols['VMap']+8);expected=struct.unpack('<1728H',(ROOT/'data/layouts/EuropeChantilly/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(24) for x in range(72))==expected
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'chantilly-roof-complete',True);before=preserved(e)[1:];go(e,(16,14));travel(e,4);grid(e)
 go(e,(23,10));e.screenshot(ROOT/'test-output/chantilly-station-front.png');saved=preserved(e),e.location();e=reload(e,'chantilly-station-front');assert (preserved(e),e.location())==saved;grid(e)
 e.walk('UP',1);e.frames(180);assert e.location()[2:]==(4,8)
 saved=preserved(e),e.location();e=reload(e,'chantilly-station-inside');assert (preserved(e),e.location())==saved
 e.walk('DOWN',2);e.frames(180);assert e.location()==(43,16,23,10);grid(e)
 assert preserved(e)[1:]==before
 print('PASS: earlier save refreshes station roof; native door entry/exit and exterior/interior cold Continue retain progress',flush=True)
 go(e,(16,14));travel(e,1);assert e.location()[:2]==(43,4)
 travel(e,4);assert e.location()[:2]==(43,16);grid(e)
 for point in [(15,10),(6,10),(51,11),(55,9),(38,19),(63,8),(65,14)]:go(e,point)
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'chantilly-station-complete');e.press('DOWN');e.press('A',900);e.finish_dialogue();assert preserved(e)[1:]==before
 print('PASS: native Paris/Chantilly rail round trip, Gym/clinic/landmark paths and saved Ada ending preserve completed journey',flush=True)
finally:e.close()
