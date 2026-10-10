from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from test_tour import travel
from key_item_test_helpers import reload
import struct
def grid(e):
 w=e.read('VMap');base=e.read(e.symbols['VMap']+8);expected=struct.unpack('<1536H',(ROOT/'data/layouts/EuropeOranienburg/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(24) for x in range(64))==expected
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'oranienburg-station-complete',True);original=preserved(e)[1:];go(e,(16,14));travel(e,5);grid(e)
 go(e,(6,10));e.screenshot(ROOT/'test-output/oranienburg-clinic-front.png');before=preserved(e),e.location();e=reload(e,'oranienburg-clinic-front');assert (preserved(e),e.location())==before;grid(e)
 e.walk('UP',1);e.frames(180);assert e.location()==(43,23,6,8)
 before=preserved(e),e.location();e=reload(e,'oranienburg-clinic-inside');assert (preserved(e),e.location())==before
 e.walk('UP',4);e.walk('RIGHT',1);assert e.location()[2:]==(7,4)
 funds=preserved(e)[1];bag=preserved(e)[3];e.press('UP');e.press('A',900);e.finish_dialogue()
 count=e.read('gPlayerPartyCount',1)
 for i in range(count):
  p=e.symbols['gPlayerParty']+i*100
  assert e.read(p+80)==0 and e.read(p+86,2)==e.read(p+88,2)
 before=preserved(e);e.press('UP');e.press('A',900);e.finish_dialogue();assert preserved(e)==before
 assert preserved(e)[1]==funds and preserved(e)[3]==bag
 e.walk('DOWN',5);e.frames(180);assert e.location()==(43,20,6,10);grid(e)
 assert preserved(e)[1:]==original
 print('PASS: prior save refreshes clinic walls; exterior/interior cold Continue, free repeated care and exit preserve inventory/money/progress',flush=True)
 for point in [(15,10),(23,10),(48,10),(48,9),(37,8),(59,17)]:go(e,point)
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'oranienburg-clinic-complete');e.press('DOWN');e.press('A',900);e.finish_dialogue();assert preserved(e)[1:]==original
 print('PASS: Gym/station/landmark paths and native saved Ada ending remain available without extra rewards',flush=True)
finally:e.close()
