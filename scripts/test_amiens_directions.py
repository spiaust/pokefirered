"""Native Amiens arrival and meeting-note return, without injected progress."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_amiens import STORY,AMIENS,board,leave,nora,notice
from test_time import preserved
from key_item_test_helpers import reload
from test_garden import choose

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/amiens-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'garden-directions-amiens-offer',True);assert e.var(STORY)==0
 for choice in ['B','NO']:board(e,choice);assert e.var(STORY)==0
 e.walk('RIGHT',3);e.walk('UP',3);before=preserved(e);e.press('UP');e.press('A',180)
 from test_country import wait_menu
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180)
 pages(e,3,'arrival');assert e.location()==AMIENS and e.var(STORY)==1 and preserved(e)==before
 e=reload(e,'amiens-directions-arrived');notice(e);assert e.var(STORY)==1
 for choice in ['B','NO']:leave(e,choice);assert e.var(STORY)==1
 print('PASS: native optional boarding and three arrival pages locate Nora; saved arrival and early board preserve the welcome gate',flush=True)
 nora(e);assert e.var(STORY)==2;e=reload(e,'amiens-directions-briefed');nora(e);assert e.var(STORY)==2
 e.walk('RIGHT',7);e.walk('UP',10);before=preserved(e);e.press('UP');e.press('A',180)
 pages(e,6,'meeting');assert e.var(STORY)==3 and preserved(e)==before
 e.walk('DOWN',10);e.walk('LEFT',7);e=reload(e,'amiens-directions-noted');notice(e);assert e.var(STORY)==3
 print('PASS: actual Nora welcome unlocks meeting notice; six pages include return directions, and cold Continue retains copied notes',flush=True)
 nora(e);assert e.var(STORY)==4;e=reload(e,'amiens-directions-confirmed');nora(e);assert e.var(STORY)==4
 for choice in ['B','NO']:leave(e,choice);assert e.var(STORY)==4
 leave(e);board(e);assert e.var(STORY)==4;e=reload(e,'amiens-directions-returned');assert e.location()==AMIENS and e.var(STORY)==4
 print('PASS: native return to Nora confirms meeting instructions; optional return choices, actual round trip and cold Continue preserve completion',flush=True)
finally:e.close()
