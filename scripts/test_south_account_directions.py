"""Native two-port reporting order and direct Southampton return."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,return_to_ada,visit_forest,researcher
from test_south_account import ACCOUNT,archive
from test_port_account import archive as port_archive
from test_port_return import destination
from test_southampton_care import rest
from test_luggage import bag
from test_time import cross,preserved,cancel_checks
from key_item_test_helpers import reload
from test_country import wait_menu

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/south-account-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'luggage-directions-found',True);assert e.var(ACCOUNT)==0 and e.var(0x40D9)==0 and e.var(0x40D7)==2
 e.walk('UP',2);e.walk('RIGHT',1);before=preserved(e);e.press('RIGHT');e.press('A',180);pages(e,7,'return')
 assert e.var(0x40D7)==3 and preserved(e)==before;e.walk('LEFT',1);e.walk('DOWN',2)
 e=reload(e,'south-account-directions-complete');cross(e);return_to_ada(e)
 for choice in ['B','NO']:port_archive(e,choice);assert e.var(0x40D9)==0 and e.var(ACCOUNT)==0
 port_archive(e);assert e.var(0x40D9)==1 and e.var(ACCOUNT)==0
 for choice in ['B','NO']:archive(e,choice);assert e.var(ACCOUNT)==0
 e=reload(e,'south-account-directions-offer');archive(e,'B');assert e.var(ACCOUNT)==0
 print('PASS: actual luggage hand-in shows seven return/care/report pages; real Oxford trip records Le Havre first, then optional Southampton No/B and cold Continue preserve pending report',flush=True)
 before=preserved(e);researcher(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);pages(e,8,'archived')
 assert e.var(ACCOUNT)==1 and e.var(0x40D9)==1 and preserved(e)==before
 e=reload(e,'south-account-directions-archived');archive(e);assert e.var(ACCOUNT)==1
 print('PASS: native Ada Southampton acceptance shows eight record/reminder pages explaining direct destination; exact stationary party/items/money and both recorded accounts persist',flush=True)
 visit_forest(e);cancel_checks(e)
 for choice in ['B',3]:destination(e,choice)
 destination(e,0);cross(e);destination(e,1);cross(e);destination(e,2);bag(e,False);rest(e)
 e=reload(e,'south-account-directions-revisited');rest(e);cross(e);destination(e,2)
 e=reload(e,'south-account-directions-returned');assert e.var(ACCOUNT)==1 and e.var(0x40D9)==1 and e.var(0x40D7)==3
 print('PASS: native three-destination menu supports initial No/B and menu B/Exit, refuge, Le Havre and Southampton; free care, repeated direct travel and cold Continue preserve completed luggage',flush=True)
finally:e.close()
