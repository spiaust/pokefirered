"""Native Rouen departure gate, arrival and optional route-book introduction."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_amiens_news import porter
from test_amiens import notice
from test_rouen import STORY,ROUEN,board,leave,leon
from test_time import preserved
from key_item_test_helpers import reload
from test_country import wait_menu

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/rouen-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'news-directions-checked',True);porter(e);assert e.var(STORY)==0 and e.var(0x40DE)==3
 e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'news-directions-returned',True)
 assert e.var(STORY)==0 and e.var(0x40DE)==4
 notice(e);assert e.var(STORY)==0
 for choice in ['B','NO']:board(e,choice);assert e.var(STORY)==0
 e=reload(e,'rouen-directions-ready');board(e,'B');assert e.var(STORY)==0
 print('PASS: checked but undelivered bulletin cannot board Rouen; delivered departure notice, optional No/B and cold Continue preserve unstarted journey',flush=True)
 e.walk('RIGHT',8);e.walk('UP',3);before=preserved(e);e.press('UP');e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);pages(e,3,'arrival')
 assert e.location()==ROUEN and e.var(STORY)==1 and preserved(e)==before
 e=reload(e,'rouen-directions-arrived')
 for choice in ['B','NO']:leave(e,choice);assert e.var(STORY)==1
 leave(e);board(e);assert e.var(STORY)==1
 print('PASS: three native journey pages locate Leon; saved arrival and optional return choices retain unregistered arrival across actual Amiens round trip',flush=True)
 e.walk('UP',1);e.walk('LEFT',4);e.walk('UP',6);before=preserved(e);e.press('UP');e.press('A',180)
 pages(e,6,'welcome');assert preserved(e)==before and e.var(STORY)==2 and e.var(0x40DC)==0
 e.walk('DOWN',6);e.walk('RIGHT',4);e.walk('DOWN',1)
 e=reload(e,'rouen-directions-welcomed')
 for choice in ['B','NO']:leon(e,choice);assert e.var(0x40DC)==0
 e=reload(e,'rouen-directions-book-offer');leon(e,'B');assert e.var(STORY)==2 and e.var(0x40DC)==0
 print('PASS: six native Leon welcome pages register arrival and introduce missing route book; saved repeat No/B preserve optional search without forcing acceptance',flush=True)
finally:e.close()
