from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_tour_journal import inspect
from test_time import preserved
from key_item_test_helpers import reload
e=Emulator(ROOT/'pokefirered.gba')
try:
 for source,name,index,lead in [('england-accepted-Oliver','Oliver',1,1),('england-reminder-Alice-trainer','Alice',13,2)]:
  load_checkpoint(e,source,True);assert e.location()==(43,index,17,19)
  before=preserved(e),e.location();inspect(e,lead,'trail-journal-'+name);assert (preserved(e),e.location())==before
  print(f'PASS: {name} earned approach shows updated east-of-path lead with read-only journal controls',flush=True)
  e=reload(e,'trail-journal-'+name);assert (preserved(e),e.location())==before
  inspect(e,lead,'trail-journal-'+name+'-continued');assert (preserved(e),e.location())==before
  print(f'PASS: {name} native cold Continue retains exact trail approach, earned progress and updated lead',flush=True)
finally:e.close()
