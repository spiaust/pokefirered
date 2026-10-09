"""Follow Ada onward to the refuge and return through native Celebi travel."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,report,researcher,visit_forest,return_to_ada
from test_time import preserved,cross,portal_prompt,keeper,child,PAST,ARRIVAL,PRESENT
from key_item_test_helpers import reload

def declines(e):
 before=preserved(e),e.var(PAST),e.location()
 for choice in ['B','NO']:
  portal_prompt(e)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();assert (preserved(e),e.var(PAST),e.location())==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'celebi-return-claimed',True);assert e.var(0x40EE)==3 and e.var(PAST)==0
 before=preserved(e);researcher(e);e.frames(900)
 for i in range(6):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/celebi-refuge-Ada-{i}.png');e.press('A',900)
 e.finish_dialogue();report(e);assert preserved(e)==before and e.var(PAST)==0
 e=reload(e,'celebi-refuge-Ada');report(e);assert preserved(e)==before
 print('PASS: completed vision report shows six Ada onward pages; repeats and cold Continue preserve reward and unstarted historical visit',flush=True)
 visit_forest(e);before=preserved(e);declines(e);e=reload(e,'celebi-refuge-departure');declines(e);assert preserved(e)==before and e.var(PAST)==0
 print('PASS: normal route reaches present forest Celebi; optional No/B departure and cold Continue preserve location, earned report and unstarted refuge',flush=True)
 cross(e);assert e.location()==ARRIVAL and e.var(PAST)==1
 before=preserved(e);declines(e);e=reload(e,'celebi-refuge-arrived');declines(e);assert preserved(e)==before and e.var(PAST)==1
 keeper(e);assert e.var(PAST)==1
 e.screenshot(ROOT/'test-output/celebi-refuge-arrived.png')
 print('PASS: native Yes reaches refuge and saves first visit; arrival Celebi offers optional return, No/B preserve state, and keeper cannot skip the child request',flush=True)
 child(e);assert e.var(PAST)==2;keeper(e);assert e.var(PAST)==3;child(e);assert e.var(PAST)==4
 before=preserved(e);e=reload(e,'celebi-refuge-helped');assert preserved(e)==before
 cross(e);assert e.location()==PRESENT and e.var(PAST)==4
 e=reload(e,'celebi-refuge-home');return_to_ada(e);before=preserved(e);report(e);assert preserved(e)==before and e.var(PAST)==4
 e=reload(e,'celebi-refuge-returned');report(e);assert preserved(e)==before
 print('PASS: native child/keeper help completes refuge; arrival Celebi returns home, and saved return to Ada preserves historical progress without another vision reward',flush=True)
finally:e.close()
