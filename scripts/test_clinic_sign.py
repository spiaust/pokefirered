from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved
from key_item_test_helpers import reload
e=Emulator(ROOT/'pokefirered.gba')
try:
 for city,dest in [('Oxford',3),('Chantilly',4),('Oranienburg',5)]:
  load_checkpoint(e,'mixed-map-pages',True);go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  go(e,(5,12));before=preserved(e),e.location();e.press('UP');e.press('A',900)
  assert e.read('sLockFieldControls',1);e.screenshot(ROOT/f'test-output/clinic-sign-{city}.png');e.finish_dialogue();assert (preserved(e),e.location())==before
  e=reload(e,'clinic-sign-'+city);assert (preserved(e),e.location())==before
  e.press('UP');e.press('A',900);e.finish_dialogue();assert (preserved(e),e.location())==before
  go(e,(6,10));e.walk('UP',1);e.frames(180);assert e.location()==(43,dest*4+3,6,8)
  e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',900);e.finish_dialogue()
  e.walk('DOWN',5);e.frames(180);assert e.location()==(43,dest*4,6,10)
  e.screenshot(ROOT/f'test-output/clinic-sign-{city}-field.png')
  assert preserved(e)[1:]==before[0][1:]
  print(f'PASS: {city} red-cross sign reads once/repeatedly with exact native cold Continue; normal clinic care and exit retain progress',flush=True)
finally:e.close()
