"""Nearby bridges, gallery and completed Westminster on the updated London."""
import json
from emulator import Emulator,ROOT
maps=json.loads((ROOT/"data/maps/map_groups.json").read_text())["gMapGroup_Europe"]
from test_celebi import load_checkpoint,visit_forest,return_to_ada
from test_landmark_cases import go,talk
from test_time import preserved,cross
from test_tour import travel
from test_port_return import destination
from test_london_past import clerk
from key_item_test_helpers import reload

def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'current-navigation-London',True);original=preserved(e)[1:],history(e)
 for start,end,y in [(18,25,28),(19,27,38)]:
  go(e,(start,y));e.walk('RIGHT',end-start);assert e.location()==(43,0,end,y)
  e.walk('LEFT',end-start);assert e.location()==(43,0,start,y)
 go(e,(55,33));e.screenshot(ROOT/'test-output/london-western-reading-outside.png')
 talk(e,(55,33),choice='YES');assert e.location()[:2]==(43,maps.index("EuropeLondonReadingRoom"))
 go(e,(5,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,0,55,33)
 talk(e,(29,29),choice='YES');assert e.location()[:2]==(43,maps.index("EuropeLondonEyeGallery"))
 go(e,(5,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,0,29,29)
 talk(e,(14,35),choice='YES');assert e.location()[:2]==(43,39)
 before=preserved(e),history(e);talk(e,(8,15));assert (preserved(e),history(e))==before
 go(e,(10,15));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,0,14,35)
 assert (preserved(e)[1:],history(e))==original
 print('PASS: both London bridges, unchanged reading room, Eye gallery and completed Westminster case remain usable without duplicate rewards or reset progress',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));visit_forest(e);destination(e,2);clerk(e)
 assert e.location()==(43,37,10,16)
 e.screenshot(ROOT/'test-output/london-western-historical.png');e=reload(e,'london-western-historical')
 assert (preserved(e)[1:],history(e))==original
 cross(e);return_to_ada(e);e=reload(e,'london-western-routes-complete')
 assert (preserved(e)[1:],history(e))==original
 print('PASS: historical London saved revisit and native return to Ada retain completed journey independently of modern facade artwork',flush=True)
finally:e.close()
