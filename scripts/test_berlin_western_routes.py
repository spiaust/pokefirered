"""Berlin visitor rooms and completed Reichstag retain earned progress."""
import json
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk
from test_time import preserved
from test_tour import travel
from key_item_test_helpers import reload
maps=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'paris-western-complete',True);original=preserved(e)[1:],history(e)
 go(e,(16,14));travel(e,2)
 for label,point,name in [('library',(51,32),'EuropeBerlinLibrary'),('garden',(58,32),'EuropeBerlinGardenRoom'),('Gate',(19,37),'EuropeGateVisitor')]:
  go(e,point);e.screenshot(ROOT/f'test-output/berlin-western-{label}-outside.png')
  for choice in ['NO','B']:
   before=preserved(e),history(e);talk(e,point,choice=choice);assert (preserved(e),history(e))==before
  talk(e,point,choice='YES');assert e.location()==(43,maps.index(name),5,7)
  e=reload(e,'berlin-western-'+label)
  go(e,(5,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,8,*point)
  assert (preserved(e)[1:],history(e))==original
 print('PASS: unchanged Berlin library, garden room and Gate visitor support cancellation, indoor cold Continue and native exit while retaining all completion state',flush=True)
 talk(e,(21,33),choice='YES');assert e.location()[:2]==(43,40)
 before=preserved(e),history(e);talk(e,(8,15));assert (preserved(e),history(e))==before
 e=reload(e,'berlin-western-notredame');go(e,(10,15));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,8,21,33) and (preserved(e)[1:],history(e))==original
 go(e,(16,14));travel(e,3);go(e,(18,14));e=reload(e,'berlin-western-routes-complete')
 before=preserved(e),history(e);e.press('DOWN');e.press('A',900);e.finish_dialogue()
 assert (preserved(e),history(e))==before and (preserved(e)[1:],history(e))==original
 print('PASS: completed Reichstag repeat grants no duplicate reward; indoor Continue, saved rail return and Ada ending preserve cumulative journey',flush=True)
finally:e.close()
