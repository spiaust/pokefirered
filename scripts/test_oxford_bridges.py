"""Cross both walking rows and cold Continue on genuine completed Oxford save."""
import struct
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from test_journal import inspect
from key_item_test_helpers import reload
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def grid(e):
 width=e.read('VMap');base=e.read(e.symbols['VMap']+8)
 expected=struct.unpack('<1536H',(ROOT/'data/layouts/EuropeOxford/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*width+x+7),2) for y in range(24) for x in range(64))==expected
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'current-navigation-complete',True);assert e.location()==(43,12,18,14);original=preserved(e)[1:],history(e);grid(e)
 for label,start,end,y in [('HighStreet',54,61,12),('Meadow',53,60,19)]:
  for row in [y,y+1]:
   go(e,(start,row));e.walk('RIGHT',end-start);assert e.location()==(43,12,end,row)
   e.walk('LEFT',end-start);assert e.location()==(43,12,start,row)
  assert (preserved(e)[1:],history(e))==original
  e.screenshot(ROOT/f'test-output/oxford-bridges-{label}.png')
  print('PASS: '+label+' both bridge rows cross east/west with restored walking controls and all completed progress retained',flush=True)
  location=e.location();e=reload(e,'oxford-bridges-'+label);assert e.location()==location;grid(e)
  inspect(e,58,1048575);assert (preserved(e)[1:],history(e))==original
  print('PASS: '+label+' bridge cold Continue restores exact saved state, authored map tiles and read-only completed journal',flush=True)
 for point in [(38,10),(54,10),(46,18),(15,10),(23,10),(6,10)]:go(e,point)
 go(e,(15,23));e.walk('DOWN',1);e.frames(180);assert e.location()[:2]==(43,13)
 e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,12);grid(e)
 assert (preserved(e)[1:],history(e))==original
 print('PASS: landmark paths, Gym/station/clinic approaches and southern trail round trip retain completed journey',flush=True)
 go(e,(18,14));e=reload(e,'oxford-bridges-complete');before=preserved(e),history(e)
 e.press('DOWN');e.press('A',900);e.finish_dialogue();assert (preserved(e),history(e))==before
 assert (preserved(e)[1:],history(e))==original
 print('PASS: saved native return to Ada repeats the ending without changing rewards, purchases or completed activities',flush=True)
finally:e.close()
