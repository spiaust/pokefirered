"""Collect optional stamps after the genuine completed story and cases."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_tour import travel,item_count,STAMPS,REWARDED,EXP_SHARE
from test_time import preserved
from test_tour_journal import inspect

def history(e):return tuple(e.var(v) for v in [*range(0x40D5,0x40F2),0x40FB,0x40FD,0x40FF,0x40C0,0x40C1,0x40C2])
def town(e,dest):go(e,(16,14));travel(e,dest)
def guide(e,label):
 assert e.location()[2:]==(16,14)
 e.press('DOWN');e.press('A',900)
 for page in range(40):
  if not e.read('sLockFieldControls',1):break
  e.screenshot(ROOT/f'test-output/walkthrough-stamps-{label}-{page}.png')
  e.press('A',900)
 assert not e.read('sLockFieldControls',1)
def ada(e):
 go(e,(18,14));before=preserved(e);e.press('DOWN');e.press('A',900)
 e.screenshot(ROOT/'test-output/walkthrough-stamps-ada.png')
 for _ in range(160):
  if not e.read('sLockFieldControls',1):break
  e.press('A',90)
 assert preserved(e)==before and not e.read('sLockFieldControls',1)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'walkthrough-optional-complete',True)
 original=history(e);assert all(e.var(v)==0 for v in STAMPS) and e.var(REWARDED)==0 and item_count(e,EXP_SHARE)==0
 seen=set()
 for dest,city in [(2,'Berlin'),(0,'London'),(1,'Paris')]:
  town(e,dest);guide(e,city);seen.add(dest)
  assert [e.var(v) for v in STAMPS]==[int(i in seen) for i in range(3)]
  assert e.var(REWARDED)==int(len(seen)==3) and item_count(e,EXP_SHARE)==int(len(seen)==3)
  assert history(e)==original
  before=preserved(e);guide(e,city+'-repeat');assert preserved(e)==before
  save(e,'walkthrough-stamps-'+city);saved=preserved(e)
  print('PASS: '+city+' guide grants only its stamp, third visit grants exactly one Exp. Share, repeated guide safe',flush=True)
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'walkthrough-stamps-'+city,True)
  assert preserved(e)==saved and e.location()==(43,dest*4,16,14) and history(e)==original
  print('PASS: '+city+' stamp save cold Continues with exact party, inventory and completed story/cases',flush=True)
 inspect(e,24,'walkthrough-tour-complete')
 print('PASS: journal shows completed tour with all seven stamp/reward/badge milestones; reading is read-only',flush=True)
 for dest,city in [(1,'Paris'),(0,'London'),(2,'Berlin')]:
  if e.location()[1]!=dest*4:town(e,dest)
  before=preserved(e);guide(e,city+'-completed');assert preserved(e)==before and item_count(e,EXP_SHARE)==1
 assert history(e)==original
 print('PASS: revisiting all three completed guides grants no duplicate rewards and retains main ending/cases',flush=True)
 town(e,3);ada(e);save(e,'walkthrough-stamps-complete');saved=preserved(e)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'walkthrough-stamps-complete',True)
 assert preserved(e)==saved and history(e)==original and e.var(REWARDED)==1 and item_count(e,EXP_SHARE)==1
 assert all(e.var(v)==1 for v in STAMPS)
 ada(e)
 print('PASS: final cold Continue retains all stamps, one Exp. Share, completed cases and repeatable Ada ending',flush=True)
finally:e.close()
