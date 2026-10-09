"""Native Le Havre boarding, captain welcome and optional dockworker request."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_le_havre import STORY,PORT,clerk,captain
from test_rouen import ROUEN
from test_dock_check import worker,notice
from test_time import preserved
from key_item_test_helpers import reload
from test_country import wait_menu

def pages(e,count,label,finish=True):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/havre-directions-{label}-{i}.png');e.press('A',900)
 if finish:e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'book-directions-active',True);clerk(e);assert e.location()==ROUEN and e.var(STORY)==0
 e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'book-directions-rested',True)
 assert e.var(STORY)==0
 for choice in ['B','NO']:clerk(e,choice);assert e.var(STORY)==0
 e=reload(e,'havre-directions-ready');clerk(e,'B');assert e.var(STORY)==0
 print('PASS: unreturned route book blocks onward travel; actual completed-book save supports boarding No/B and cold Continue without starting journey',flush=True)
 e.walk('RIGHT',8);e.walk('UP',1);before=preserved(e);e.press('UP');e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);pages(e,3,'arrival')
 assert e.location()==PORT and e.var(STORY)==1 and preserved(e)==before
 e=reload(e,'havre-directions-arrived');worker(e);notice(e);assert e.var(STORY)==1 and e.var(0x40DA)==0
 print('PASS: three native journey pages locate captain; saved arrival and early worker/notice preserve captain welcome prerequisite',flush=True)
 before=preserved(e);e.press('DOWN');e.press('A',180);pages(e,4,'welcome',False)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
 assert e.location()==PORT and e.var(STORY)==2 and preserved(e)==before
 e=reload(e,'havre-directions-welcomed')
 for choice in ['B','NO']:worker(e,choice);captain(e,choice);assert e.var(0x40DA)==0
 captain(e,'YES');clerk(e);assert e.location()==PORT and e.var(STORY)==2
 e=reload(e,'havre-directions-returned');worker(e,'B');assert e.var(0x40DA)==0
 print('PASS: four captain welcome pages locate dockworker; saved welcome, optional dock request/return No/B and actual Rouen round trip retain unstarted dock task',flush=True)
finally:e.close()
