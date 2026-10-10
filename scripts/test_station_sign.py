from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved
from key_item_test_helpers import reload
import struct

def grid(e,city):
 w=e.read('VMap');base=e.read(e.symbols['VMap']+8);width=72 if city=='Chantilly' else 64
 expected=struct.unpack('<%dH'%(width*24),(ROOT/f'data/layouts/Europe{city}/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(24) for x in range(width))==expected

e=Emulator(ROOT/'pokefirered.gba')
try:
 for city,dest in [('Oxford',3),('Chantilly',4),('Oranienburg',5)]:
  load_checkpoint(e,'mixed-map-pages',True);go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  grid(e,city);go(e,(22,12));before=preserved(e),e.location();e.press('UP');e.press('A',900)
  assert e.read('sLockFieldControls',1);e.screenshot(ROOT/f'test-output/station-sign-{city}.png');e.finish_dialogue();assert (preserved(e),e.location())==before
  e=reload(e,'station-sign-'+city);assert (preserved(e),e.location())==before;grid(e,city)
  e.press('UP');e.press('A',900);e.finish_dialogue();assert (preserved(e),e.location())==before
  go(e,(23,10));e.screenshot(ROOT/f'test-output/station-sign-{city}-field.png');e.walk('UP',1);e.frames(180);assert e.location()==(43,dest*4+2,4,8)
  saved=preserved(e),e.location();e=reload(e,'station-sign-'+city+'-inside');assert (preserved(e),e.location())==saved
  e.walk('DOWN',2);e.frames(180);assert e.location()==(43,dest*4,23,10)
  go(e,(16,14));travel(e,dest-3);assert e.location()[:2]==(43,(dest-3)*4)
  travel(e,dest);grid(e,city);assert preserved(e)[1:]==before[0][1:]
  go(e,(6,10));go(e,(15,10));go(e,(22,12));e=reload(e,'station-sign-'+city+'-complete');grid(e,city)
  assert preserved(e)[1:]==before[0][1:]
  print(f'PASS: {city} train sign read/repeat/cold Continue, station door/indoor save/exit and native capital rail round trip retain progress',flush=True)
finally:e.close()
