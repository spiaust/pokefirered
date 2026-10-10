"""Earned two-badge delivery, one-time Magnet and cold Continue on current ROM."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_country import wait_menu
from test_tour import travel,item_count
from test_germany_story import leave_gym,STORY,MAGNET
from test_time import preserved
from key_item_test_helpers import reload
def town(e,dest):
 go(e,(16,14))
 if e.location()[1]!=dest*4:travel(e,dest)
 go(e,(10,14))
def talk(e):e.press('DOWN');e.press('A',900);e.finish_dialogue()
def offer(e,choice):
 e.press('DOWN');e.press('A',900);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
 if choice=='NO':e.press('DOWN')
 e.press('B' if choice=='B' else 'A',900);e.finish_dialogue()
def cold(e,label):
 before=preserved(e),e.location();e=reload(e,'lena-delivery-'+label)
 assert (preserved(e),e.location())==before
 return e
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'water-gym-complete',True);leave_gym(e);town(e,5)
 assert e.var(STORY)==0
 before=preserved(e);talk(e);talk(e);assert preserved(e)==before
 print('PASS: Karl repeats cannot start an unaccepted delivery or grant Magnet',flush=True)
 town(e,2);before=preserved(e)
 for choice in ['NO','B']:offer(e,choice);assert preserved(e)==before
 e=cold(e,'offer');assert e.var(STORY)==0
 print('PASS: earned two badges unlock Lena offer; No/B and cold Continue retain unstarted quest',flush=True)
 offer(e,'YES');assert e.var(STORY)==1
 before=preserved(e);talk(e);assert preserved(e)==before;e=cold(e,'active')
 print('PASS: normal acceptance and repeated saved directions retain parcel outside Bag',flush=True)
 initial=item_count(e,MAGNET);town(e,5);talk(e);assert e.var(STORY)==2 and item_count(e,MAGNET)==initial
 before=preserved(e);talk(e);assert preserved(e)==before;e=cold(e,'delivered')
 print('PASS: native rail delivery to Karl advances report once; repeat/cold Continue retain pending reward',flush=True)
 town(e,2);talk(e);assert e.var(STORY)==3 and item_count(e,MAGNET)==initial+1
 before=preserved(e);talk(e);assert preserved(e)==before;e=cold(e,'reward');talk(e);assert preserved(e)==before
 print('PASS: normal Lena report grants exactly one Magnet; repeats and cold Continue retain completion',flush=True)
 town(e,5);before=preserved(e);talk(e);e=cold(e,'Karl-complete');talk(e);assert preserved(e)==before and e.var(STORY)==3
 print('PASS: completed Karl repeats and saved Oranienburg visit preserve Magnet and delivery',flush=True)
 load_checkpoint(e,'current-navigation-complete',True);town(e,2);before=preserved(e);talk(e);e=cold(e,'completed-journey');talk(e);assert preserved(e)==before and e.var(STORY)==3
 print('PASS: completed historical journey Lena repeats retain all rewards and finished delivery',flush=True)
finally:e.close()
