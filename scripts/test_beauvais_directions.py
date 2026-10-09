"""Follow completed report to actual Beauvais boarding and check-in."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_time import ARRIVAL,PAST,preserved,keeper,cross,PRESENT
from test_departure import NEWS,POST,visit_post,back_to_refuge
from test_evac import EVAC,RECEPTION,prompt,board_train,host,elise,return_service
from test_country import wait_menu
from key_item_test_helpers import reload

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'departure-directions-reported',True);assert e.location()==ARRIVAL and e.var(NEWS)==4 and e.var(EVAC)==0
 before=preserved(e);e.walk('UP',3);e.press('UP');e.press('A',900)
 for i in range(4):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/beauvais-directions-keeper-{i}.png');e.press('A',900)
 e.finish_dialogue();e.walk('DOWN',3);keeper(e);assert preserved(e)==before and e.var(EVAC)==0
 e=reload(e,'beauvais-directions-ready');keeper(e);assert preserved(e)==before
 print('PASS: completed news report gives four keeper pages including Beauvais boarding lead; repeats/cold Continue preserve unstarted journey and earned progress',flush=True)
 visit_post(e);before=preserved(e)
 for choice in ['B','NO']:
  prompt(e)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();assert preserved(e)==before and e.var(EVAC)==0
  e.walk('DOWN',5);e.walk('LEFT',6)
 e=reload(e,'beauvais-directions-board');assert e.location()==POST
 board_train(e);assert e.location()==RECEPTION and e.var(EVAC)==1 and e.var(NEWS)==4
 e=reload(e,'beauvais-directions-arrived');elise(e);assert e.var(EVAC)==1
 host(e);assert e.var(EVAC)==2;elise(e);assert e.var(0x40E4)==0
 e=reload(e,'beauvais-directions-checked-in');host(e);elise(e);assert e.var(EVAC)==2
 print('PASS: native guide and board route supports No/B before real train arrival; Elise requires host check-in, and saved check-in/repeats retain optional follow-up without forced acceptance',flush=True)
 before=preserved(e);return_service(e);assert e.location()==POST and e.var(EVAC)==2
 back_to_refuge(e);keeper(e);assert e.var(EVAC)==2 and e.var(NEWS)==4 and e.var(PAST)==4 and preserved(e)[1:]==before[1:]
 cross(e);assert e.location()==PRESENT
 e=reload(e,'beauvais-directions-home');assert e.var(EVAC)==2 and e.var(NEWS)==4
 print('PASS: native south-exit return service, refuge guide and Celebi return reach the present; cold Continue preserves check-in, news and refuge help without rewards or progress duplication',flush=True)
finally:e.close()
