from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk
from test_tour import travel
from test_time import preserved
from key_item_test_helpers import reload
from test_gym_ui import open_key_item
from test_navigation import wait_task
import json
maps=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def page(e,city,dest,tag):
 before=preserved(e),history(e),e.location();open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapCurrent',1)==dest;e.press('R',180);e.screenshot(ROOT/f'test-output/room-directions-{city}-{tag}.png')
 for _ in range(4):e.press('B',180)
 assert (preserved(e),history(e),e.location())==before and not e.read('sLockFieldControls',1)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'mixed-map-pages',True);original=preserved(e)[1:],history(e)
 for city,dest,point,name in [('Oxford',3,(38,10),'EuropeRadcliffeVisitor'),('Chantilly',4,(51,11),'EuropeChateauVisitor'),('Oranienburg',5,(48,9),'EuropePalaceVisitor')]:
  go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  page(e,city,dest,'outside');go(e,point);talk(e,point,choice='YES');assert e.location()==(43,maps.index(name),5,7)
  e=reload(e,'room-directions-'+city);page(e,city,dest,'inside-continued');go(e,(5,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,dest*4,*point) and (preserved(e)[1:],history(e))==original
  print(f'PASS: {city} map directions lead to native room entry, interior cold Continue/map and correct south exit without progress changes',flush=True)
finally:e.close()
