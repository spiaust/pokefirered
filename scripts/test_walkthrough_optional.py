"""Complete all optional cases on the genuine fresh Germany ending save."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import DATA,go,talk,save
from test_tour import travel
from test_oxford_gym import count_pocket
from test_time import preserved

def history(e):return tuple(e.var(v) for v in range(0x40D5,0x40F2))
def town(e,dest):go(e,(16,14));travel(e,dest)
def synthesis(e,point,facing,label):
 go(e,point);before=preserved(e);e.press(facing);e.press('A',900)
 for page in range(9):
  assert e.read('sLockFieldControls',1),(label,page)
  if page>=5:e.screenshot(ROOT/f'test-output/walkthrough-optional-{label}-{page-5}.png')
  if page<8:e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before and not e.read('sLockFieldControls',1)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'walkthrough-germany-all-accounts',True)
 assert e.var(0x40D5)==2 and e.var(0x40F0)==3
 original=history(e);assert all(e.var(v)==0 for v in range(0x40C0,0x40C3))
 for row,reward,quantity,offset,slots in zip(DATA,[213,68,3],[1,1,3],[0x310,0x310,0x430],[42,42,13]):
  tag,city,country,index,inside,door,var,selection=row
  town(e,selection);before=count_pocket(e,reward,offset,slots)
  talk(e,door,choice='YES');assert e.location()==(43,inside,10,15)
  talk(e,(8,15),choice='YES');assert e.var(var)==1
  talk(e,(15,8));assert e.var(var)==3
  talk(e,(4,6));assert e.var(var)==4
  talk(e,(10,5),choice='YES');assert e.var(var)==5
  talk(e,(8,15));assert e.var(var)==6
  assert count_pocket(e,reward,offset,slots)==before+quantity
  state=preserved(e);talk(e,(8,15));assert preserved(e)==state
  assert history(e)==original
  e.screenshot(ROOT/f'test-output/walkthrough-optional-{tag}-reward.png')
  save(e,'walkthrough-optional-'+tag);saved=preserved(e)
  print('PASS: '+tag+' documented curator/clues/attendant sequence, exact reward once and ending progress retained',flush=True)
  e.close();e=Emulator(ROOT/'pokefirered.gba')
  load_checkpoint(e,'walkthrough-optional-'+tag,True)
  assert preserved(e)==saved and e.var(var)==6 and history(e)==original
  go(e,(10,15));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,index,*door)
  talk(e,door,choice='YES');assert e.var(var)==6
  print('PASS: '+tag+' cold Continue retains exact state, exits and re-enters normally',flush=True)
  if tag!='Reichstag':
   go(e,(10,15));e.walk('DOWN',1);e.frames(180)
 assert all(e.var(v)==6 for v in range(0x40C0,0x40C3))
 synthesis(e,(12,14),'DOWN','ledger')
 print('PASS: completed three-case ledger displays all four synthesis pages without rewards or story changes',flush=True)
 go(e,(10,15));e.walk('DOWN',1);e.frames(180);town(e,3)
 synthesis(e,(18,14),'DOWN','ada')
 assert history(e)==original
 print('PASS: Ada displays ending conclusion then all four case synthesis pages with exact progress retained',flush=True)
 save(e,'walkthrough-optional-complete');saved=preserved(e)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'walkthrough-optional-complete',True)
 assert preserved(e)==saved and history(e)==original and all(e.var(v)==6 for v in range(0x40C0,0x40C3))
 synthesis(e,(18,14),'DOWN','continued-ada')
 print('PASS: final cold Continue retains all case rewards and main ending; Ada conclusion/synthesis repeat safely',flush=True)
finally:e.close()
