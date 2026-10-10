"""Walk every Dover harbor arm lane, native saves, signs and transport on earned battery."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from key_item_test_helpers import reload
from test_coast import crossing,leave_port
from test_tour import travel
import struct

def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def grid(e):
 w=e.read('VMap');base=e.read(e.symbols['VMap']+8);expected=struct.unpack('<2240H',(ROOT/'data/layouts/EuropeDoverPort/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(40) for x in range(56))==expected

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'coast-sightseeing-Dover',True);assert e.location()[:2]==(43,27);original=preserved(e)[1:],history(e);grid(e)
 for y in (31,32,33):
  go(e,(27,y));e.walk('RIGHT',11);assert e.location()==(43,27,38,y)
  e.screenshot(ROOT/f'test-output/dover-arm-row-{y}.png')
  e.walk('LEFT',11);assert e.location()==(43,27,27,y)
 go(e,(38,32));before=preserved(e),history(e),e.location();e=reload(e,'dover-arm-tip');assert (preserved(e),history(e),e.location())==before;grid(e)
 e.walk('LEFT',11);assert e.location()==(43,27,27,32) and (preserved(e)[1:],history(e))==original
 print('PASS: earlier coastal battery refreshes exact harbor arm grid; all three lanes walk both directions and tip cold Continue retains progress',flush=True)
 for x,y,d,label in [(44,13,'UP','Castle'),(52,18,'RIGHT','Cliffs'),(29,23,'UP','Seafront')]:
  go(e,(x,y));e.press(d);before=preserved(e),history(e),e.location();e.press('A',900);assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/dover-arm-sign-{label}.png');e.finish_dialogue();assert (preserved(e),history(e),e.location())==before
 go(e,(35,23));before=preserved(e),history(e),e.location();e=reload(e,'dover-arm-district');assert (preserved(e),history(e),e.location())==before;grid(e)
 print('PASS: castle, cliffs and seafront signs remain reachable/read-only; district cold Continue preserves exact state',flush=True)
 go(e,(8,5));crossing(e);assert e.location()==(43,28,8,5);crossing(e);assert e.location()==(43,27,8,5);grid(e);leave_port(e)
 assert e.location()==(43,0,23,10) and (preserved(e)[1:],history(e))==original
 print('PASS: normal Channel ferry round trip and Dover north coach exit return to London without changing completed activities',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'dover-arm-complete');before=preserved(e),history(e);e.press('DOWN');e.press('A',900);e.finish_dialogue()
 assert (preserved(e),history(e))==before and (preserved(e)[1:],history(e))==original
 print('PASS: native saved Oxford return and repeated Ada ending retain all completed story, case and stamp progress',flush=True)
except Exception:
 e.screenshot(ROOT/'test-output/dover-arm-failure.png');raise
finally:e.close()
