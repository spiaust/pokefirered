"""Browse all modern page types through native controls and cold Continue."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved
from key_item_test_helpers import reload
from test_journal import journal_task
def pages(e,label):
 before=preserved(e),e.location()
 open_key_item(e,361);wait_task(e,'Task_EuropeMap');e.frames(60)
 while e.read('sEuropeMapSelection',1)!=0:e.press('LEFT',60)
 e.press('R',180);task=journal_task(e)
 for dest in range(8):
  assert e.read('sEuropeMapSelection',1)==dest and e.read(task+22,2)==1
  assert e.read('sEuropePlacesRooms',1)==0
  e.press('L',180);assert e.read('sEuropePlacesRooms',1)==int(dest<6)
  e.screenshot(ROOT/f'test-output/mixed-map-{label}-{dest}.png')
  e.press('RIGHT',90)
  assert e.read('sEuropeMapSelection',1)==(dest+1)%8 and e.read('sEuropePlacesRooms',1)==0
 # Room-to-Service backward wrap and route/journal resets.
 e.press('LEFT',90);e.press('LEFT',90);assert e.read('sEuropeMapSelection',1)==6
 e.press('LEFT',90);assert e.read('sEuropeMapSelection',1)==5
 e.press('L',90);assert e.read('sEuropePlacesRooms',1)==1
 e.press('A',180);assert e.read(task+22,2)==0 and e.read('sEuropePlacesRooms',1)==0
 e.press('R',180);e.press('L',90);assert e.read('sEuropePlacesRooms',1)==1
 e.press('SELECT',180);assert e.read('sEuropePlacesRooms',1)==0
 e.press('SELECT',180);assert e.read(task+22,2)==0
 for _ in range(4):e.press('B',180)
 assert not e.read('sLockFieldControls',1) and (preserved(e),e.location())==before
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'regional-services-complete',True);pages(e,'first')
 print('PASS: all eight modern stops select Rooms/Services/Places correctly; browsing and routes/story reset secondary pages without changing state',flush=True)
 before=preserved(e),e.location();e=reload(e,'mixed-map-pages');assert (preserved(e),e.location())==before
 pages(e,'continued')
 print('PASS: native cold Continue retains completed progress and mixed page controls with clean field return',flush=True)
finally:e.close()
