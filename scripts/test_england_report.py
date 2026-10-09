"""Follow genuinely earned England reports by train and on foot."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel,item_count
from test_france_story import talk,npc
from test_time import preserved
from test_tour_journal import inspect
from key_item_test_helpers import reload
from test_country import wait_menu
import test_oxford_gym as gym

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'story-report-ready',True);go(e,(16,14));travel(e,3);go(e,(10,14))
 assert e.var(0x40FB)==1 and item_count(e,184)==0
 before=preserved(e);npc(e);e.frames(900)
 for page in range(4):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/england-report-return-{page}.png');e.press('A',900)
 e.finish_dialogue();talk(e);assert preserved(e)==before
 e=reload(e,'england-report-ready');talk(e);inspect(e,4,'england-report-ready');assert preserved(e)==before
 print('PASS: earned England report shows four return pages, repeats and cold Continues read-only with the correct journal',flush=True)
 go(e,(15,10));e.walk('UP',1);e.frames(180);e.walk('UP',8)
 before=preserved(e);gym.complete_talk(e);assert preserved(e)==before and not gym.badge(e)
 e.walk('DOWN',10);e.frames(180);go(e,(16,14));travel(e,0);go(e,(10,14));talk(e)
 assert e.var(0x40FB)==2 and item_count(e,184)==1
 before=preserved(e);talk(e);e=reload(e,'england-report-claimed');talk(e);inspect(e,5,'england-report-claimed');assert preserved(e)==before
 print('PASS: Gym stays locked before the report; normal London train reaches Oak aide and claims one Bell across repeats and cold Continue',flush=True)
 go(e,(16,14));travel(e,3);go(e,(10,14));before=preserved(e);talk(e);assert preserved(e)==before
 go(e,(15,10));e.walk('UP',1);e.frames(180);e.walk('UP',8);before=preserved(e)
 gym.leader(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue();assert preserved(e)==before
 e=reload(e,'england-report-gym');gym.leader(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('DOWN');e.press('A',180);e.finish_dialogue()
 assert preserved(e)==before and not gym.badge(e) and e.var(gym.TM_REWARD)==0 and not e.in_battle()
 print('PASS: completed rival reminder leads to the unlocked Oxford Gym; B and No declines across cold Continue grant no badge or TM',flush=True)
 load_checkpoint(e,'england-report-ready',True);go(e,(15,23));e.walk('DOWN',1);e.frames(180)
 assert e.location()==(43,13,15,0),e.location()
 e.walk('DOWN',40);e.frames(180);assert e.location()==(43,1,15,0),e.location()
 e.walk('DOWN',24);e.frames(180);assert e.location()==(43,0,15,0),e.location()
 go(e,(10,14));talk(e);assert e.var(0x40FB)==2 and item_count(e,184)==1
 before=preserved(e);talk(e);e=reload(e,'england-report-walked');talk(e);inspect(e,5,'england-report-walked');assert preserved(e)==before
 print('PASS: normal southward walk through both routes also reaches Oak aide and claims one Bell without repeat or cold Continue duplicates',flush=True)
finally:e.close()

