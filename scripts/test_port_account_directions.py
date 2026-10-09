"""Native dock confirmation, Oxford report and unlocked Celebi destinations."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,return_to_ada,visit_forest,researcher
from test_port_account import ACCOUNT,archive
from test_port_return import destination
from test_dock_care import rest
from test_time import cross,preserved,cancel_checks
from key_item_test_helpers import reload
from test_country import wait_menu

def pages(e,count,label,finish=True):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/port-account-directions-{label}-{i}.png');e.press('A',900)
 if finish:e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'dock-directions-noted',True);assert e.var(ACCOUNT)==0 and e.var(0x40DA)==2 and e.var(0x40D7)==0
 before=preserved(e);e.press('DOWN');e.press('A',180);pages(e,8,'return',False)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
 assert e.var(0x40DA)==3 and preserved(e)==before
 e=reload(e,'port-account-directions-confirmed');cross(e);return_to_ada(e)
 for choice in ['B','NO']:archive(e,choice);assert e.var(ACCOUNT)==0
 e=reload(e,'port-account-directions-offer');archive(e,'B');assert e.var(ACCOUNT)==0
 print('PASS: real captain confirmation shows eight confirmation/care/return pages; actual Oxford journey and archive No/B retain unrecorded port account after cold Continue',flush=True)
 before=preserved(e);researcher(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);pages(e,7,'archived')
 assert e.var(ACCOUNT)==1 and preserved(e)==before
 e=reload(e,'port-account-directions-archived');archive(e);assert e.var(ACCOUNT)==1 and e.var(0x40D7)==0
 print('PASS: native Ada report records Le Havre; seven record/reminder pages explain forest Celebi and LE HAVRE choice, and saved repeat preserves exact party/items/money',flush=True)
 visit_forest(e);cancel_checks(e)
 for choice in ['B',2]:destination(e,choice)
 destination(e,0);cross(e);destination(e,1);rest(e)
 e=reload(e,'port-account-directions-revisited');rest(e);cross(e);destination(e,1)
 e=reload(e,'port-account-directions-returned');assert e.var(ACCOUNT)==1 and e.var(0x40DA)==3 and e.var(0x40D7)==0
 print('PASS: native unlocked menu supports initial No/B, menu B/Exit, refuge and direct Le Havre; free care, repeated direct travel and cold Continue preserve progress',flush=True)
finally:e.close()
