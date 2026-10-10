"""Native paved habitat approaches, observation recording and saved journal leads."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved
from test_france_story import marker,SURVEY
from test_tour_journal import inspect
from key_item_test_helpers import reload
e=Emulator(ROOT/'pokefirered.gba')
try:
 for name,dest,index,y,stage,lead in [('Gardens',1,5,17,2,9),('Forest',4,17,21,3,10)]:
  load_checkpoint(e,'celine-survey-active',True);go(e,(16,14))
  if dest==4:travel(e,4)
  e.walk('LEFT',1)
  if dest==1:e.walk('UP',15);e.frames(180);e.walk('UP',6)
  else:e.walk('DOWN',10);e.frames(180);e.walk('DOWN',21)
  e.walk('LEFT',2);assert e.location()==(43,index,13,y) and e.var(SURVEY)==1
  inspect(e,8,'marker-journal-'+name+'-both');before=preserved(e);marker(e);assert e.var(SURVEY)==stage and preserved(e)[3]==before[3] and preserved(e)[1]==before[1]
  state=preserved(e);marker(e);assert preserved(e)==state
  inspect(e,lead,'marker-journal-'+name)
  print(f'PASS: {name} paved route reaches west-of-path marker; UP/A records once and journal names remaining habitat',flush=True)
  before=preserved(e),e.location();e=reload(e,'marker-journal-'+name)
  assert (preserved(e),e.location())==before;marker(e);inspect(e,lead,'marker-journal-'+name+'-continued')
  assert (preserved(e),e.location())==before
  print(f'PASS: {name} native cold Continue retains approach, recorded observation and read-only repeat/journal controls',flush=True)
finally:e.close()
