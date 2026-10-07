"""Genuine older station batteries, local board reads and cold Continue."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved

def read(e,city,label):
 go(e,(9,2));before=preserved(e);e.press('UP');assert e.location()[2:]==(9,2);e.press('A',900)
 for page in range(2):
  assert e.read('sLockFieldControls',1),(city,label,page)
  e.screenshot(ROOT/f'test-output/station-board-{city}-{label}-{page}.png')
  if page<1:e.press('A',900)
 e.finish_dialogue();assert not e.read('sLockFieldControls',1) and preserved(e)==before

for city,index in [('London',0),('Paris',4),('Berlin',8)]:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'station-board-'+city+'-v103',True);assert e.location()==(43,index+2,9,2);before=preserved(e)[1:]
  read(e,city,'old-save');read(e,city,'repeat')
  go(e,(4,7));e.walk('DOWN',2);e.frames(180);assert e.location()==(43,index,23,10)
  e.walk('UP',1);e.frames(180);assert e.location()==(43,index+2,4,8);e.walk('UP',1)
  read(e,city,'reentered');assert preserved(e)[1:]==before
  save(e,'station-board-'+city);saved=preserved(e)
  print('PASS: '+city+' v1.03 indoor battery reads local wall notice twice, exits/re-enters and preserves inventory/progress',flush=True)
 finally:e.close()
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'station-board-'+city,True);assert e.location()==(43,index+2,9,2) and preserved(e)==saved
  read(e,city,'reloaded');go(e,(4,7));e.walk('DOWN',2);e.frames(180);assert e.location()==(43,index,23,10)
  print('PASS: '+city+' local notice Save/cold Continue, repeat reading and station exit',flush=True)
 finally:e.close()
