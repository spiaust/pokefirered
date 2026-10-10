"""Native earned delivery report and Conrad readiness journal approaches."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel,item_count
from test_tour_journal import inspect
from test_time import preserved
from key_item_test_helpers import reload
from test_germany_story import STORY,MAGNET
from test_country import wait_menu

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'lena-delivery-delivered',True)
 assert e.var(STORY)==2
 go(e,(16,14));travel(e,2);e.walk('LEFT',6)
 assert e.location()==(43,8,10,14)
 inspect(e,17,'german-report-Lena')
 before=preserved(e),e.location();e=reload(e,'german-report-Lena')
 assert (preserved(e),e.location())==before
 inspect(e,17,'german-report-Lena-continued')
 print('PASS: native return to Lena shows pending report lead and exact cold Continue at west contact',flush=True)
 count=item_count(e,MAGNET);e.press('DOWN');e.press('A',900);e.finish_dialogue()
 assert e.var(STORY)==3 and item_count(e,MAGNET)==count+1
 inspect(e,18,'german-report-unlocked')
 before=preserved(e);e.press('DOWN');e.press('A',900);e.finish_dialogue();assert preserved(e)==before
 print('PASS: Lena grants one Magnet and immediately changes journal to Conrad Gym challenge; repeat is read-only',flush=True)
 go(e,(16,14));travel(e,5);go(e,(15,10));inspect(e,18,'german-report-Conrad-door')
 e.walk('UP',1);e.frames(180);assert e.location()==(43,26,6,14)
 e.walk('UP',8);assert e.location()==(43,26,6,6)
 inspect(e,18,'german-report-Conrad');before=preserved(e),e.location()
 e=reload(e,'german-report-Conrad');assert (preserved(e),e.location())==before
 print('PASS: reward-earned route reaches Conrad through north door and retains challenge lead on native cold Continue',flush=True)
 e.press('UP');e.press('A',900);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
 assert not e.in_battle() and (preserved(e),e.location())==before
 print('PASS: Conrad challenge can be declined without changing earned delivery, reward or badge state',flush=True)
finally:e.close()
