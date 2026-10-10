"""One earned journey through every regional landmark room; native saves only."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk
from test_tour import travel
from test_time import preserved
from key_item_test_helpers import reload
from test_gym_ui import open_key_item
from test_navigation import wait_task
maps=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'mixed-map-pages',True);original=preserved(e)[1:],history(e)
 for tag,dest,point,name in [('radcliffe',3,(38,10),'EuropeRadcliffeVisitor'),('magdalen',3,(51,11),'EuropeMagdalenVisitor'),('chateau',4,(51,11),'EuropeChateauVisitor'),('stables',4,(38,19),'EuropeStablesVisitor'),('palace',5,(48,9),'EuropePalaceVisitor')]:
  go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  go(e,point);e.screenshot(ROOT/f'test-output/landmark-tour-{tag}-approach.png')
  for choice in ['NO','B']:
   before=preserved(e),history(e),e.location();talk(e,point,choice=choice);assert (preserved(e),history(e),e.location())==before
  talk(e,point,choice='YES');assert e.location()==(43,maps.index(name),5,7)
  for p in [(8,4),(3,4),(11,4)]:
   go(e,p);before=preserved(e),history(e);e.press('UP');e.press('A',900);assert e.read('sLockFieldControls',1);e.finish_dialogue();assert (preserved(e),history(e))==before
  assert (preserved(e)[1:],history(e))==original
  print(f'PASS: combined journey {tag} approach/No/B/entry and three conversations preserve completed activities',flush=True)
  go(e,(9,7));before=preserved(e),history(e),e.location();e=reload(e,'landmark-tour-'+tag);assert (preserved(e),history(e),e.location())==before
  open_key_item(e,361);wait_task(e,'Task_EuropeMap');assert e.read('sEuropeMapCurrent',1)==dest and e.read('sEuropeMapPast',1)==0;e.press('R',180);e.screenshot(ROOT/f'test-output/landmark-tour-{tag}-places.png')
  for _ in range(4):e.press('B',180)
  assert (preserved(e),history(e),e.location())==before and not e.read('sLockFieldControls',1)
  for x in [4,5]:
   go(e,(x,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,dest*4,*point)
   if x==4:talk(e,point,choice='YES');assert e.location()==(43,maps.index(name),5,7)
  assert (preserved(e)[1:],history(e))==original
  print(f'PASS: combined journey {tag} native interior cold Continue/Places/both south exits/re-entry retain location and progress',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'landmark-tour-complete');before=preserved(e),history(e);e.press('DOWN');e.press('A',900);e.finish_dialogue();assert (preserved(e),history(e))==before and (preserved(e)[1:],history(e))==original
 print('PASS: five-room tour returns to native saved Ada ending with all rewards and completed activities intact',flush=True)
except Exception:
 e.screenshot(ROOT/'test-output/landmark-tour-failure.png');raise
finally:e.close()
