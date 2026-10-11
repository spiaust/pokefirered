"""Read all three earned final batteries on the exact expansion build."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,researcher
from test_time import preserved
from test_oxford_gym import badge as badge1
from test_chantilly_gym import badge as badge2
from test_oranienburg_gym import badge as badge3
for n,country in enumerate(('england','france','germany'),1):
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'release-'+country+'-all-accounts',True)
  assert e.var(0x40f0)==n and e.var(0x40d5)==2 and e.var(0x40cc)==1
  assert badge1(e) and badge2(e) and badge3(e)
  assert tuple(e.var(v) for v in range(0x40c8,0x40cc))==(0,0,0,0)
  assert e.location()==(43,12,18,14)
  before=preserved(e);researcher(e);e.finish_dialogue();assert preserved(e)==before
  print('PASS: '+country+' fresh-game final native battery has three badges, Ada completion, unstarted optional archive and repeatable main ending',flush=True)
 finally:e.close()
