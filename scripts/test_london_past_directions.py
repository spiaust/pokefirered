"""Native historical London boarding, Rose arrival and saved return directions."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_london_past import STORY,LONDON,clerk,leave,rose
from test_time import preserved
from key_item_test_helpers import reload
from test_country import wait_menu

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/london-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'south-directions-returned',True);clerk(e);assert e.var(STORY)==0 and e.var(0x40D7)==0
 e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'south-account-directions-returned',True)
 for choice in ['B','NO']:clerk(e,choice);assert e.var(STORY)==0
 e=reload(e,'london-directions-ready');clerk(e,'B');assert e.var(STORY)==0
 print('PASS: missing luggage clearance blocks London; actual completed luggage save supports boarding No/B and cold Continue without forced departure',flush=True)
 e.walk('UP',1);e.walk('RIGHT',1);before=preserved(e);e.press('RIGHT');e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);pages(e,3,'arrival')
 assert e.location()==LONDON and e.var(STORY)==1 and preserved(e)==before
 e=reload(e,'london-directions-arrived')
 for choice in ['B','NO']:leave(e,choice);assert e.var(STORY)==1
 leave(e);clerk(e);assert e.location()==LONDON and e.var(STORY)==1
 print('PASS: three native journey pages locate Rose; saved arrival, return No/B and actual Southampton round trip retain unregistered London arrival',flush=True)
 rose(e);assert e.var(STORY)==2;e=reload(e,'london-directions-welcomed')
 e.walk('UP',1);e.walk('LEFT',4);e.walk('UP',6);before=preserved(e);e.press('UP');e.press('A',180);pages(e,6,'report')
 assert e.var(STORY)==2 and preserved(e)==before;e.walk('DOWN',6);e.walk('RIGHT',4);e.walk('DOWN',1)
 e=reload(e,'london-directions-report-ready');rose(e)
 print('PASS: actual Rose welcome records London; six completed-reminder pages explain Celebi/Chantilly/Oxford/Ada, and saved repeated talks preserve exact stationary party/items/money',flush=True)
finally:e.close()
