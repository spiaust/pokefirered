"""Old finished save requires Ada acknowledgement, then normal Hall access."""
from council_test_helpers import *
from test_celebi import researcher
from walking_test_helpers import assert_walk_preserved
name='council-old-ending';shutil.copy2(ROOT/'artifacts/releases/v3.0-evidence/release-england-all-accounts.sav',ROOT/f'test-output/{name}.sav')
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,name,True);assert e.var(0x40cc)==0
 go(e,(16,14));travel(e,0);talk(e,(55,33),choice='YES');before=preserved(e);npc(e,(5,4));e.finish_dialogue()
 assert e.location()[:2]==(43,READING) and council(e)==(0,0) and preserved(e)==before
 assert not e.task_active('Task_YesNoMenu_HandleInput');e.screenshot(ROOT/'test-output/council-gated.png')
 go(e,(5,7));e.walk('DOWN',1);e.frames(180);go(e,(16,14));travel(e,3);go(e,(18,14));researcher(e);e.finish_dialogue();assert e.var(0x40cc)==1
 go(e,(16,14));travel(e,0);talk(e,(55,33),choice='YES')
 for refusal in ('NO','B'):
  before=preserved(e);npc(e,(5,4));answer(e,refusal);e.finish_dialogue();assert preserved(e)==before and e.location()[:2]==(43,READING)
 npc(e,(5,4));answer(e);e.finish_dialogue();assert e.location()[:2]==(43,HALL) and council(e)==(0,0)
 print('PASS: old finished native save, Ada acknowledgement gate, entry No/B, normal access and unchanged old main ending',flush=True)
finally:e.close()
