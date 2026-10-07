"""Northern arrival signs through native crossings, old batteries and cold Continue."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved

def read(e,city,label):
 go(e,(14,6));e.walk('UP',1);assert e.location()[2:]==(14,5);before=preserved(e);e.press('A',900)
 for page in range(4):
  assert e.read('sLockFieldControls',1),(city,label,page)
  e.screenshot(ROOT/f'test-output/capital-arrival-{city}-{label}-{page}.png')
  if page<3:e.press('A',900)
 e.finish_dialogue();assert not e.read('sLockFieldControls',1) and preserved(e)==before

for city,country,index in [('London','england',0),('Paris','france',4),('Berlin','germany',8)]:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'start-'+country,True);before=preserved(e)[1:]
  go(e,(15,0));e.walk('UP',1);e.frames(180);assert e.location()==(43,index+1,15,23)
  e.walk('DOWN',1);e.frames(180);assert e.location()==(43,index,15,0)
  read(e,city,'old-save');read(e,city,'repeat');assert preserved(e)[1:]==before
  save(e,'capital-arrival-'+city.lower());saved=preserved(e)
  print('PASS: '+city+' old battery northern crossing, arrival-sign pages, repeated reading and unchanged inventory/progress',flush=True)
 finally:e.close()
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'capital-arrival-'+city.lower(),True);assert e.location()==(43,index,14,5) and preserved(e)==saved
  read(e,city,'reloaded');go(e,(15,0));e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,index+1)
  print('PASS: '+city+' arrival-sign Save/cold Continue, rereading and countryside return',flush=True)
 finally:e.close()
