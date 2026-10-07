"""Station entry/exit, local directions, repeat reads and cold Continue."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved

def read(e,city,label):
 go(e,(22,13));e.walk('UP',1);assert e.location()[2:]==(22,12);before=preserved(e);e.press('A',900)
 for page in range(3):
  assert e.read('sLockFieldControls',1),(city,label,page)
  e.screenshot(ROOT/f'test-output/capital-station-{city}-{label}-{page}.png')
  if page<2:e.press('A',900)
 e.finish_dialogue();assert not e.read('sLockFieldControls',1) and preserved(e)==before

for city,country,index,doors in [('London','england',0,[(45,33),(55,33)]),('Paris','france',4,[(45,39),(55,39)]),('Berlin','germany',8,[(43,32),(51,32),(58,32)])]:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'start-'+country,True);before=preserved(e)[1:]
  go(e,(23,10));e.walk('UP',1);e.frames(180);assert e.location()==(43,index+2,4,8),e.location();e.walk('UP',1);assert e.location()==(43,index+2,4,7)
  e.walk('DOWN',2);e.frames(180);assert e.location()==(43,index,23,10),e.location()
  read(e,city,'old-save');read(e,city,'repeat')
  for p in doors:go(e,p)
  assert preserved(e)[1:]==before
  go(e,(22,12));save(e,'capital-station-'+city.lower());saved=preserved(e)
  print('PASS: '+city+' old battery station entry/exit, all sign pages twice, neighborhood approaches and unchanged inventory/progress',flush=True)
 finally:e.close()
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'capital-station-'+city.lower(),True);assert e.location()==(43,index,22,12) and preserved(e)==saved
  read(e,city,'reloaded');go(e,(23,10));e.walk('UP',1);e.frames(180);assert e.location()==(43,index+2,4,8),e.location();e.walk('UP',1);assert e.location()==(43,index+2,4,7)
  go(e,(5,7));e.walk('DOWN',1);assert e.location()==(43,index+2,5,8);e.walk('LEFT',1);e.walk('DOWN',1);e.frames(180);assert e.location()==(43,index,23,10),e.location()
  print('PASS: '+city+' station-sign Save/cold Continue, rereading and side approach to the marked station exit',flush=True)
 finally:e.close()
