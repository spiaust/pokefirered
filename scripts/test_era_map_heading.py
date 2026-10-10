"""Era map navigation and cold Continue on earned historical batteries."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved
from test_journal import journal_task
from key_item_test_helpers import reload
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())
def state(e):return preserved(e),tuple(e.var(v) for v in range(0x40C0,0x4100)),e.location()
def page(e,label,anchor):
 before=state(e);open_key_item(e,361);wait_task(e,'Task_EuropeMap');task=journal_task(e)
 assert e.read('sEuropeMapPast',1)==1 and e.read('sEuropeMapCurrent',1)==anchor
 e.screenshot(ROOT/f'test-output/era-map-{label}.png')
 e.press('RIGHT',90);assert e.read('sEuropeMapSelection',1)==(anchor+1)%8
 e.press('LEFT',90);assert e.read('sEuropeMapSelection',1)==anchor
 e.press('R',180);assert e.read(task+22,2)==1
 e.press('L',180);assert e.read('sEuropePlacesRooms',1)==1
 e.press('A',180);assert e.read(task+22,2)==0
 e.press('SELECT',180);e.press('SELECT',180)
 for _ in range(4):e.press('B',180)
 assert not e.read('sLockFieldControls',1) and state(e)==before
e=Emulator(ROOT/'pokefirered.gba')
try:
 for label,source,mapname,anchor in [
  ('chantilly','time-arrival','EuropeChantillyPast',4),
  ('post','departure-confirmed','EuropeChantillyPastPost',4),
  ('beauvais','beauvais-directions-arrived','EuropeBeauvaisPast',4),
  ('garden','garden-found','EuropeBeauvaisGarden',4),
  ('amiens','compat-v207-amiens-news-complete','EuropeAmiensPast',4),
  ('rouen','rouen-arrival','EuropeRouenPast',4),
  ('le-havre','le-havre-arrival','EuropeLeHavrePast',4),
  ('southampton','southampton-arrival','EuropeSouthamptonPast',0),
  ('london','london-directions-arrived','EuropeLondonPast',0)]:
  load_checkpoint(e,source,True);assert e.location()[0]==43 and groups['gMapGroup_Europe'][e.location()[1]]==mapname,(source,e.location())
  page(e,label,anchor);before=state(e);e=reload(e,'era-map-'+label);assert state(e)==before;page(e,label+'-continued',anchor)
  print(f'PASS: {label} historical map/Places/secondary/story controls retain exact state and cold Continue',flush=True)
finally:e.close()
