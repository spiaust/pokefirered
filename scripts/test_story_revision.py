"""Local readiness permits travel; optional reports remain available after ending."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,return_to_ada,researcher
from test_southampton import clerk as ferry,SOUTH
from test_london_past import clerk as onward,LONDON,rose
from test_time import cross
from test_garden import choose
from test_landmark_cases import talk
from test_journal import inspect

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'dock-check-complete',True)
 assert e.var(0x40D9)==0
 ferry(e);assert e.location()==SOUTH and e.var(0x40D9)==0
 inspect(e,51,32767,'optional-port-report-arrival')
 print('PASS: ferry uses local dock clearance without Oxford report; journal follows arrival',flush=True)
 load_checkpoint(e,'luggage-complete',True)
 assert e.var(0x40D6)==0
 onward(e);assert e.location()==LONDON and e.var(0x40D6)==0
 rose(e);assert e.var(0x40D5)==2
 inspect(e,58,786431,'optional-south-report-ending')
 print('PASS: London accepts local luggage clearance without Oxford report; journal reaches ending',flush=True)
 cross(e);return_to_ada(e)
 # Exercise a journey that deferred both optional accounts until the ending.
 base=e.read('gSaveBlock1Ptr')
 e.write(base+0x1000+(0x40D9-0x4000)*2,0,2)
 for var in (0x40D9,0x40D6):
  researcher(e);choose(e,'NO');assert e.var(var)==0
  researcher(e);choose(e,'YES');assert e.var(var)==1
 researcher(e);e.screenshot(ROOT/'test-output/story-ada-conclusion.png');e.finish_dialogue()
 assert not e.read('sLockFieldControls',1) and e.var(0x40D5)==2
 print('PASS: Ada ending remains repeatable; deferred port and reception reports can still be filed',flush=True)
 load_checkpoint(e,'case-notredame-complete',True)
 base=e.read('gSaveBlock1Ptr')
 for var in (0x40C1,0x40C2):e.write(base+0x1000+(var-0x4000)*2,6,2)
 talk(e,(12,14),'DOWN')
 assert [e.var(v) for v in (0x40C0,0x40C1,0x40C2)]==[6,6,6]
 assert not e.read('sLockFieldControls',1)
 print('PASS: completed three-case ledger provides synthesis without resetting progress',flush=True)
finally:e.close()
