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
 load_checkpoint(e,'chantilly-bridge-complete',True);before=preserved(e)[1:]
 go(e,(16,14));travel(e,4);grid(e)
 go(e,(15,10));e.screenshot(ROOT/'test-output/chantilly-roof-front.png');saved=preserved(e),e.location();e=reload(e,'chantilly-roof-front');assert (preserved(e),e.location())==saved;grid(e)
 e.walk('UP',1);e.frames(180);assert e.location()==(43,25,8,18)
 e.walk('DOWN',2);e.frames(180);assert e.location()==(43,16,15,10);grid(e)
 assert preserved(e)[1:]==before
 print('PASS: earlier earned save refreshes blue roof; native front save/cold Continue and Gym door round trip preserve progress',flush=True)
 for point in [(6,10),(23,10),(51,11),(55,9),(38,19),(63,8),(65,14)]:go(e,point)
 e=reload(e,'chantilly-roof-district');grid(e);assert preserved(e)[1:]==before
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'chantilly-roof-complete')
 e.press('DOWN');e.press('A',900);e.finish_dialogue();assert preserved(e)[1:]==before
 print('PASS: clinic/station/estate/moat paths and saved Ada ending repeat retain completed quests and rewards',flush=True)
finally:e.close()
