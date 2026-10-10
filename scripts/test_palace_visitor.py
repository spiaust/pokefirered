import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk
from test_tour import travel
from test_time import preserved
from key_item_test_helpers import reload
from test_gym_ui import open_key_item
from test_navigation import wait_task
maps=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe'];inside=maps.index('EuropePalaceVisitor')
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'mixed-map-pages',True);original=preserved(e)[1:],history(e);go(e,(16,14));travel(e,5);go(e,(48,9));e.screenshot(ROOT/'test-output/palace-approach.png')
 for choice in ['NO','B']:
  before=preserved(e),history(e),e.location();talk(e,(48,9),choice=choice);assert (preserved(e),history(e),e.location())==before
 e=reload(e,'palace-outside');talk(e,(48,9),choice='YES');assert e.location()==(43,inside,5,7)
 for point in [(8,4),(3,4),(11,4)]:
  go(e,point);before=preserved(e),history(e);e.press('UP');e.press('A',900);assert e.read('sLockFieldControls',1);e.screenshot(ROOT/f'test-output/palace-display-{point[0]}.png');e.finish_dialogue();assert (preserved(e),history(e))==before
 assert (preserved(e)[1:],history(e))==original
 print('PASS: earned Oranienburg arrival, No/B declines, saved exterior, entry, guide and both displays preserve progress',flush=True)
 go(e,(9,7));before=preserved(e),history(e),e.location();e=reload(e,'palace-interior');assert (preserved(e),history(e),e.location())==before
 open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapCurrent',1)==5 and e.read('sEuropeMapPast',1)==0;e.press('R',180);e.screenshot(ROOT/'test-output/palace-map.png')
 for _ in range(4):e.press('B',180)
 assert not e.read('sLockFieldControls',1) and (preserved(e),history(e),e.location())==before
 print('PASS: interior native cold Continue and Oranienburg Town Map/Places retain exact location and progress',flush=True)
 for x in (4,5):
  go(e,(x,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,20,48,9)
  talk(e,(48,9),choice='YES');assert e.location()==(43,inside,5,7)
 go(e,(5,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,20,48,9) and (preserved(e)[1:],history(e))==original
 e=reload(e,'palace-returned');assert e.location()==(43,20,48,9) and (preserved(e)[1:],history(e))==original
 print('PASS: both south exit tiles, re-entry and native returned save reach the palace court without changing progress',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'palace-complete');before=preserved(e),history(e);e.press('DOWN');e.press('A',900);e.finish_dialogue();assert (preserved(e),history(e))==before and (preserved(e)[1:],history(e))==original
 print('PASS: native saved Oxford return and Ada ending retain completed activities and rewards',flush=True)
except Exception:
 e.screenshot(ROOT/'test-output/palace-failure.png');raise
finally:e.close()
