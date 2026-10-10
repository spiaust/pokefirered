"""Find Remy/Karl from native arrival squares and retain earned quest leads."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_tour_journal import inspect
from test_time import preserved
from key_item_test_helpers import reload
e=Emulator(ROOT/'pokefirered.gba')
try:
 for source,city,dest,stagevar,stage,lead in [('celine-survey-gardens-forest-review','Chantilly',4,0x40FD,5,12),('lena-delivery-active','Oranienburg',5,0x40FF,1,16)]:
  load_checkpoint(e,source,True);go(e,(16,14))
  if e.location()[1]!=dest*4:travel(e,dest)
  original=preserved(e)[1:];e.walk('LEFT',6);assert e.location()==(43,dest*4,10,14)
  assert e.var(stagevar)==stage;inspect(e,lead,'branch-contact-'+city)
  print(f'PASS: {city} native arrival square LEFT six reaches west contact and correct earned journal lead',flush=True)
  before=preserved(e),e.location();e=reload(e,'branch-contact-'+city)
  assert (preserved(e),e.location())==before;inspect(e,lead,'branch-contact-'+city+'-continued')
  assert preserved(e)[1:]==original
  print(f'PASS: {city} contact approach cold Continue and read-only topic controls retain exact earned state',flush=True)
  before=preserved(e);e.press('DOWN');e.press('A',900);e.finish_dialogue()
  assert not e.read('sLockFieldControls',1)
  if city=='Chantilly':assert preserved(e)==before and e.var(stagevar)==5
  else:assert e.var(stagevar)==2 and preserved(e)[3]==before[3] and preserved(e)[1]==before[1]
  e=reload(e,'branch-contact-'+city+'-spoken')
  print(f'PASS: {city} DOWN/A speaks to intended contact; normal report/delivery branch saves without extra items',flush=True)
finally:e.close()
