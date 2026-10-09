"""Native reunion report to Ada and onward bulletin unlock."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,return_to_ada,visit_forest,researcher
from test_amiens_account import archive,ACCOUNT
from test_amiens import reach_post,board
from test_amiens_news import porter
from test_reunion import relocated
from test_time import cross,preserved
from key_item_test_helpers import reload
from test_country import wait_menu

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/account-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'reunion-directions-complete-mira',True);assert e.var(ACCOUNT)==0 and e.var(0x40E0)==6
 porter(e);assert e.var(0x40DE)==0
 e.walk('RIGHT',3);e.walk('UP',7);before=preserved(e);e.press('UP');e.press('A',180)
 pages(e,6,'home');assert preserved(e)==before;e.walk('DOWN',7);e.walk('LEFT',3)
 e=reload(e,'account-directions-reunion');cross(e);return_to_ada(e)
 for choice in ['B','NO']:archive(e,choice);assert e.var(ACCOUNT)==0
 e=reload(e,'account-directions-offer');archive(e,'B');assert e.var(ACCOUNT)==0
 print('PASS: six reunion pages explain Celebi, Chantilly station and Ada; real return journey, optional archive No/B and cold Continue retain unarchived story',flush=True)
 before=preserved(e);researcher(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180)
 pages(e,6,'archived');assert e.var(ACCOUNT)==1 and preserved(e)==before
 e=reload(e,'account-directions-archived');archive(e);assert e.var(ACCOUNT)==1
 print('PASS: native Ada acceptance records reunion; six record/reminder pages point back to Amiens porter, with exact party/items/money and persistent repeated archive',flush=True)
 visit_forest(e);reach_post(e);board(e);relocated(e)
 for choice in ['B','NO']:porter(e,choice);assert e.var(0x40DE)==0
 porter(e);assert e.var(0x40DE)==1
 e=reload(e,'account-directions-news-active');porter(e);assert e.var(ACCOUNT)==1 and e.var(0x40DE)==1 and e.var(0x40E0)==6
 print('PASS: real return to Amiens preserves reunited Meowth; porter bulletin unlocks only after archive, supports No/B and retains actual acceptance after cold Continue',flush=True)
finally:e.close()
