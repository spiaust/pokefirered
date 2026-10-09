"""Read-only map/journal and registered shortcut on the completed journey."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,visit_forest,return_to_ada
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved,cross
from test_port_return import destination
from test_london_past import clerk
from test_journal import inspect,journal_task,registered
from test_journal_pages import inspect_pages
from test_tour_journal import inspect as tour
from test_gym_ui import open_key_item
from test_navigation import wait_task
from key_item_test_helpers import reload

def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def check(e,label,current,past):
 before=preserved(e),history(e),e.location()
 open_key_item(e,361);wait_task(e,'Task_EuropeMap')
 assert (e.read('sEuropeMapCurrent',1),e.read('sEuropeMapSelection',1),e.read('sEuropeMapPast',1))==(current,current,int(past))
 for _ in range(8):e.press('RIGHT',60)
 assert e.read('sEuropeMapSelection',1)==current
 for _ in range(8):e.press('LEFT',60)
 assert e.read('sEuropeMapSelection',1)==current
 e.screenshot(ROOT/f'test-output/current-navigation-{label}-map.png')
 e.press('B',180);e.press('B',180);e.press('B',90)
 inspect(e,58,1048575,'current-navigation-'+label)
 inspect_pages(e,1048575,'current-navigation-'+label);tour(e,24,'current-navigation-'+label)
 for key in ['B','START']:
  e.press('SELECT',180);wait_task(e,'Task_EuropeMap');task=journal_task(e)
  assert e.read(task+10,2)==0 and e.read('sEuropeMapCurrent',1)==current and e.read('sEuropeMapPast',1)==int(past)
  e.press('SELECT',60);e.press('A',60);assert e.read(task+10,2)==2
  e.press(key,180);assert not e.task_active('Task_EuropeMap') and not e.read('sLockFieldControls',1)
 assert (preserved(e),history(e),e.location())==before
 assert e.read(e.read('gSaveBlock1Ptr')+0x296,2)==361
 print('PASS: '+label+' correct map/current era, eight-stop wrap, complete historical/tour journal, topic/page controls and registered B/START exits are read-only',flush=True)
 return before

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'current-services-complete',True);original=preserved(e)[1:],history(e)
 if e.read(e.read('gSaveBlock1Ptr')+0x296,2)!=361:registered(e)
 for dest,label in enumerate(['London','Paris','Berlin','Oxford','Chantilly','Oranienburg']):
  go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  before=check(e,label,dest,False);e=reload(e,'current-navigation-'+label)
  assert (preserved(e),history(e),e.location())==before
  assert e.read(e.read('gSaveBlock1Ptr')+0x296,2)==361
  print('PASS: '+label+' cold Continue retains exact location, state and registered Town Map',flush=True)
 go(e,(16,14));travel(e,3);go(e,(18,14));visit_forest(e)
 for choice,label,current in [(0,'refuge',4),(1,'LeHavre',4),(2,'Southampton',0)]:
  destination(e,choice);before=check(e,label,current,True);e=reload(e,'current-navigation-'+label)
  assert (preserved(e),history(e),e.location())==before
  print('PASS: '+label+' historical cold Continue retains exact state and saved location',flush=True)
  if choice==2:
   clerk(e);before=check(e,'London1940',0,True);e=reload(e,'current-navigation-London1940')
   assert (preserved(e),history(e),e.location())==before
   print('PASS: London1940 cold Continue retains exact state and saved location',flush=True)
  cross(e)
 return_to_ada(e);e=reload(e,'current-navigation-complete')
 assert (preserved(e)[1:],history(e))==original
 before=preserved(e),history(e);e.press('DOWN');e.press('A',900);e.finish_dialogue()
 assert (preserved(e),history(e))==before
 print('PASS: normal historical return and final saved Ada ending retain all completed activities, purchases and registered map',flush=True)
finally:e.close()
