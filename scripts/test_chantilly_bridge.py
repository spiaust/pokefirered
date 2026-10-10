"""Native moat crossing and saved travel on the genuine completed journey."""
import struct
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,visit_forest,return_to_ada
from test_landmark_cases import go
from test_time import preserved,cross
from test_tour import travel
from test_journal import inspect
from key_item_test_helpers import reload
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def grid(e):
 width=e.read('VMap');base=e.read(e.symbols['VMap']+8)
 expected=struct.unpack('<1728H',(ROOT/'data/layouts/EuropeChantilly/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*width+x+7),2) for y in range(24) for x in range(72))==expected
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'oxford-bridges-complete',True);original=preserved(e)[1:],history(e)
 go(e,(16,14));travel(e,4);grid(e)
 for x in [50,51]:
  go(e,(x,15));e.walk('UP',4);assert e.location()==(43,16,x,11)
  e.walk('DOWN',4);assert e.location()==(43,16,x,15)
 assert (preserved(e)[1:],history(e))==original
 go(e,(50,12));e.screenshot(ROOT/'test-output/chantilly-bridge-moat.png')
 print('PASS: both moat bridge columns cross north/south with clear château approach and completed progress intact',flush=True)
 location=e.location();e=reload(e,'chantilly-bridge-moat');assert e.location()==location;grid(e)
 inspect(e,58,1048575);assert (preserved(e)[1:],history(e))==original
 print('PASS: bridge cold Continue retains exact state/location, every authored map tile and complete read-only journal',flush=True)
 for point in [(51,11),(55,9),(38,19),(63,8),(63,5),(65,14),(15,10),(23,10),(6,10)]:go(e,point)
 go(e,(15,23));e.walk('DOWN',1);e.frames(180);assert e.location()[:2]==(43,17)
 e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,16);grid(e)
 assert (preserved(e)[1:],history(e))==original
 print('PASS: château/stables/garden/canal paths, Gym/station/clinic approaches and south trail remain usable without changing items or completed quests',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));visit_forest(e);cross(e);assert e.location()==(43,29,5,10)
 e=reload(e,'chantilly-bridge-historical');assert (preserved(e)[1:],history(e))==original
 cross(e);return_to_ada(e);assert (preserved(e)[1:],history(e))==original
 print('PASS: separately saved historical Chantilly revisit and native return preserve prior landmark artwork IDs and earned journey state',flush=True)
 e=reload(e,'chantilly-bridge-complete');before=preserved(e),history(e)
 e.press('DOWN');e.press('A',900);e.finish_dialogue();assert (preserved(e),history(e))==before
 assert (preserved(e)[1:],history(e))==original
 print('PASS: final saved Ada ending repeats with all rewards, purchases and completed activities retained',flush=True)
finally:e.close()
