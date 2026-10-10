"""Cross both walking rows and cold Continue on genuine completed Oranienburg save."""
import struct
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from test_journal import inspect
from test_tour import travel
from key_item_test_helpers import reload
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def grid(e):
 width=e.read('VMap');base=e.read(e.symbols['VMap']+8)
 expected=struct.unpack('<1536H',(ROOT/'data/layouts/EuropeOranienburg/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*width+x+7),2) for y in range(24) for x in range(64))==expected
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'chantilly-bridge-complete',True);original=preserved(e)[1:],history(e)
 go(e,(16,14));travel(e,5);grid(e)
 for label,start,end,y in [('Schlossplatz',53,61,12),('Park',53,61,19)]:
  for row in [y,y+1]:
   go(e,(start,row));e.walk('RIGHT',end-start);assert e.location()==(43,20,end,row)
   e.walk('LEFT',end-start);assert e.location()==(43,20,start,row)
  assert (preserved(e)[1:],history(e))==original
  e.screenshot(ROOT/f'test-output/oranienburg-bridges-{label}.png')
  print('PASS: '+label+' both bridge rows cross east/west with restored walking controls and all completed progress retained',flush=True)
  location=e.location();e=reload(e,'oranienburg-bridges-'+label);assert e.location()==location;grid(e)
  inspect(e,58,1048575);assert (preserved(e)[1:],history(e))==original
  print('PASS: '+label+' bridge cold Continue restores exact saved state, authored map tiles and read-only completed journal',flush=True)
 for point in [(48,10),(48,9),(37,8),(59,17),(15,10),(23,10),(6,10)]:go(e,point)
 go(e,(15,23));e.walk('DOWN',1);e.frames(180);assert e.location()[:2]==(43,21)
 e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,20);grid(e)
 assert (preserved(e)[1:],history(e))==original
 print('PASS: landmark paths, Gym/station/clinic approaches and southern trail round trip retain completed journey',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'oranienburg-bridges-complete');before=preserved(e),history(e)
 e.press('DOWN');e.press('A',900);e.finish_dialogue();assert (preserved(e),history(e))==before
 assert (preserved(e)[1:],history(e))==original
 print('PASS: saved native return to Ada repeats the ending without changing rewards, purchases or completed activities',flush=True)
finally:e.close()
