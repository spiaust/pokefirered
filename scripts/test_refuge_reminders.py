"""Read refuge stage reminders, save each task and deliver normally."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_time import preserved,PAST,ARRIVAL,keeper,child,cross,PRESENT
from key_item_test_helpers import reload

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/refuge-reminder-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'celebi-refuge-arrived',True);assert e.location()==ARRIVAL and e.var(PAST)==1
 baseline=preserved(e);e.walk('UP',3);e.press('UP');e.press('A',180);pages(e,3,'welcome');assert preserved(e)==baseline and e.var(PAST)==1
 e=reload(e,'refuge-reminder-welcome');e.press('UP');e.press('A',180);e.finish_dialogue();assert preserved(e)==baseline and e.var(PAST)==1
 e.walk('DOWN',3);keeper(e);assert preserved(e)==baseline and e.var(PAST)==1
 print('PASS: three welcome pages identify Elise to the east; repeated keeper talks and cold Continue preserve unstarted blanket help and present-day state',flush=True)
 e.walk('RIGHT',3);e.walk('UP',3);e.press('UP');e.press('A',180)
 for _ in range(60):
  if e.var(PAST)==2:break
  e.press('A',90)
 assert e.var(PAST)==2;pages(e,2,'request');assert preserved(e)==baseline
 e=reload(e,'refuge-reminder-request');e.walk('DOWN',3);e.walk('LEFT',3);child(e);assert e.var(PAST)==2 and preserved(e)==baseline
 print('PASS: native Elise/Eevee request identifies keeper to the west; repeat request and cold Continue preserve stage 2 without blanket, Bag or reward changes',flush=True)
 e.walk('UP',3);e.press('UP');e.press('A',180)
 for _ in range(50):
  if e.var(PAST)==3:break
  e.press('A',90)
 assert e.var(PAST)==3;pages(e,2,'carry');assert preserved(e)==baseline
 e.walk('DOWN',3);e=reload(e,'refuge-reminder-carry');keeper(e);assert e.var(PAST)==3 and preserved(e)==baseline
 child(e);assert e.var(PAST)==4 and preserved(e)==baseline
 child(e);keeper(e);assert e.var(PAST)==4 and preserved(e)[1:]==baseline[1:]
 completed=preserved(e)
 e=reload(e,'refuge-reminder-complete');assert e.var(PAST)==4 and preserved(e)==completed
 cross(e);assert e.location()==PRESENT and e.var(PAST)==4 and preserved(e)==completed
 print('PASS: keeper gives carried blanket and eastward delivery directions; native delivery, repeats, cold Continue and Celebi return retain completed help with no inventory or reward duplication',flush=True)
finally:e.close()
