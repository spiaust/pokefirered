"""Read updated rival/Gym journal leads from earned native checkpoints."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_tour_journal import inspect
from test_landmark_cases import go
from test_time import preserved
from key_item_test_helpers import reload
from test_germany_story import leave_gym
e=Emulator(ROOT/'pokefirered.gba')
try:
 for source,label,lead,target in [('rival-prep-ready','rival',3,(10,14)),('gym-ready-Oxford-unlocked','Oxford',5,(15,10)),('gym-ready-Chantilly-unlocked','Chantilly',13,(15,10)),('gym-ready-Oranienburg-unlocked','Oranienburg',18,(15,10))]:
  load_checkpoint(e,source,True)
  if label!='rival':
   if label=='Chantilly':leave_gym(e)
   else:e.walk('DOWN',10);e.frames(180)
  go(e,target);before=preserved(e),e.location()
  inspect(e,lead,'tour-approach-'+label);assert (preserved(e),e.location())==before
  print(f'PASS: {label} earned approach shows correct updated read-only journal lead',flush=True)
  e=reload(e,'tour-approach-'+label);assert (preserved(e),e.location())==before
  inspect(e,lead,'tour-approach-'+label+'-continued');assert (preserved(e),e.location())==before
  print(f'PASS: {label} native cold Continue retains exact approach and updated lead controls',flush=True)
finally:e.close()
