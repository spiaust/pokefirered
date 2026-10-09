"""Observe a real vision and follow its report-return directions."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,forest,report,return_to_ada,visit_forest
from test_country import wait_menu
from test_time import preserved
from test_tour import item_count
from key_item_test_helpers import reload

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/celebi-return-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'gym-ada-forest',True);assert e.var(0x40EE)==1
 candy=item_count(e,68);forest(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180)
 for _ in range(80):
  if e.var(0x40EE)==2:break
  e.press('A',90)
 assert e.var(0x40EE)==2;pages(e,3,'first');assert item_count(e,68)==candy and not e.in_battle()
 before=preserved(e);forest(e);pages(e,4,'repeat');assert preserved(e)==before
 forest(e);e.finish_dialogue();assert preserved(e)==before
 e=reload(e,'celebi-return-ready');forest(e);e.finish_dialogue();assert preserved(e)==before
 print('PASS: genuine vision shows three first-return pages; four-page forest reminder repeats and cold Continues read-only with report ready and no reward',flush=True)
 return_to_ada(e);report(e);assert e.var(0x40EE)==3 and item_count(e,68)==candy+1
 before=preserved(e);report(e);assert preserved(e)==before
 e=reload(e,'celebi-return-claimed');report(e);assert preserved(e)==before
 print('PASS: actual northward forest walk and station train reach Ada east of Oxford guide; report grants one Candy and saved/repeated hand-ins duplicate nothing',flush=True)
 visit_forest(e);before=preserved(e)
 for choice in ['B','NO']:
  forest(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();assert preserved(e)==before and e.location()==(43,17,15,24) and not e.in_battle()
 e=reload(e,'celebi-return-completed-forest');forest(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
 assert preserved(e)==before and item_count(e,68)==candy+1
 print('PASS: normal completed-story forest revisit offers optional time travel; No/B and cold Continue retain the present location, one reward and completed report',flush=True)
finally:e.close()
