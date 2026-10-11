"""Final Ada conclusion from the genuine current London journey, no fixtures."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,return_to_ada,visit_forest,researcher
from test_time import preserved,cross
from test_journal import inspect
from test_journal_pages import inspect_pages
from test_port_return import destination
from test_southampton_care import rest
from test_london_past import clerk,rose
from key_item_test_helpers import reload

def progress(e):return tuple(e.var(v) for v in range(0x40C0,0x4100) if v != 0x40CC)

def conclusion(e,label):
 before=preserved(e),progress(e);researcher(e);e.frames(900)
 for i in range(5):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/current-ending-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue();assert not e.read('sLockFieldControls',1);assert e.var(0x40CC)==1
 assert (preserved(e),progress(e))==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'london-directions-report-ready',True)
 assert e.var(0x40D5)==2 and e.var(0x40D6)==1 and e.var(0x40D9)==1
 cross(e);return_to_ada(e);conclusion(e,'first')
 e=reload(e,'current-ending-reported');conclusion(e,'saved')
 print('PASS: genuine completed London journey returns through Celebi/Chantilly/Oxford to five Ada ending pages; cold Continue and repeat preserve party, items, money and all regional/historical variables',flush=True)
 inspect(e,58,1048575,'current-ending');inspect_pages(e,1048575,'current-ending')
 e=reload(e,'current-ending-journal');inspect(e,58,1048575)
 print('PASS: final journal lead and all twenty historical milestones remain read-only; page wrapping, topic controls and cold Continue retain complete records',flush=True)
 visit_forest(e);destination(e,2);rest(e);clerk(e);rose(e)
 assert e.var(0x40D5)==2;cross(e);return_to_ada(e);conclusion(e,'revisited')
 e=reload(e,'current-ending-revisited');conclusion(e,'final')
 print('PASS: completed journey remains playable through direct Southampton return, native free care and historical London revisit; actual return to Ada and cold Continue repeat ending without resetting progress',flush=True)
finally:e.close()
