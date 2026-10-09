"""Native Southampton luggage search, pickup, return and unlocked care."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_luggage import STORY,worker,bag,visible
from test_southampton import host,clerk,SOUTH
from test_southampton_care import rest
from test_time import preserved
from key_item_test_helpers import reload
from test_country import wait_menu

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/luggage-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'south-directions-returned',True);assert e.var(STORY)==0
 bag(e,False)
 for choice in ['B','NO']:worker(e,choice);assert e.var(STORY)==0
 e.walk('UP',2);e.walk('RIGHT',1);before=preserved(e);e.press('RIGHT');e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);pages(e,2,'active')
 assert e.var(STORY)==1 and preserved(e)==before;e.walk('LEFT',1);e.walk('DOWN',2)
 e=reload(e,'luggage-directions-active');worker(e);assert e.var(STORY)==1
 print('PASS: luggage absent before request; optional search No/B, actual acceptance/two direction pages and cold Continue retain active search',flush=True)
 host(e,'YES');clerk(e);e.walk('UP',2);e.walk('LEFT',2);assert visible(e)
 before=preserved(e);e.press('LEFT');e.press('A',180);pages(e,3,'found')
 assert e.var(STORY)==2 and not visible(e) and preserved(e)==before
 e.walk('RIGHT',2);e.walk('DOWN',2);e=reload(e,'luggage-directions-found');bag(e,False);assert e.var(STORY)==2
 print('PASS: actual west-quay pickup shows three worker-return pages with exact inventory; cold Continue retains carried luggage and removes quay object',flush=True)
 worker(e);assert e.var(STORY)==3;e=reload(e,'luggage-directions-returned');bag(e,False)
 for choice in ['B','NO']:rest(e,choice);host(e,choice);assert e.var(STORY)==3
 rest(e);host(e,'YES');clerk(e);assert e.location()==SOUTH and e.var(STORY)==3
 e=reload(e,'luggage-directions-rested');bag(e,False);rest(e);assert e.var(STORY)==3
 print('PASS: native worker hand-in unlocks free care; rest/return No/B, actual care, Le Havre round trip and cold Continue retain completion and absent luggage',flush=True)
finally:e.close()
