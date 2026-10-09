"""Native Southampton crossing, welcome and optional luggage introduction."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_southampton import STORY,SOUTH,clerk,host
from test_le_havre import PORT
from test_luggage import worker,bag
from test_time import preserved
from key_item_test_helpers import reload
from test_country import wait_menu

def pages(e,count,label,finish=True):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/south-directions-{label}-{i}.png');e.press('A',900)
 if finish:e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'dock-directions-active',True);clerk(e);assert e.location()==PORT and e.var(STORY)==0
 e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'dock-directions-rested',True)
 for choice in ['B','NO']:clerk(e,choice);assert e.var(STORY)==0
 e=reload(e,'south-directions-ready');clerk(e,'B');assert e.var(STORY)==0
 print('PASS: unconfirmed dock instructions block crossing; actual confirmed save supports crossing No/B and cold Continue without starting Southampton journey',flush=True)
 e.walk('UP',2);e.walk('LEFT',2);before=preserved(e);e.press('LEFT');e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);pages(e,3,'arrival')
 assert e.location()==SOUTH and e.var(STORY)==1 and preserved(e)==before
 e=reload(e,'south-directions-arrived');worker(e);bag(e,False);assert e.var(STORY)==1 and e.var(0x40D7)==0
 print('PASS: three crossing pages locate reception host; saved arrival, early worker and absent luggage preserve host welcome prerequisite',flush=True)
 before=preserved(e);e.press('DOWN');e.press('A',180);pages(e,4,'welcome',False)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
 assert e.location()==SOUTH and e.var(STORY)==2 and preserved(e)==before
 e=reload(e,'south-directions-welcomed')
 for choice in ['B','NO']:worker(e,choice);host(e,choice);assert e.var(0x40D7)==0
 host(e,'YES');clerk(e);assert e.location()==SOUTH and e.var(STORY)==2
 e=reload(e,'south-directions-returned');worker(e,'B');assert e.var(0x40D7)==0
 print('PASS: four host welcome pages locate luggage worker; saved welcome, optional search/return No/B and actual Le Havre round trip preserve unstarted luggage task',flush=True)
finally:e.close()
