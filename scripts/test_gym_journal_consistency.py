"""Check journal priorities against earned Gym rewards and real next steps."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_tour_journal import inspect
from test_landmark_cases import go
from test_time import preserved
from test_tour import travel,guide
from test_country import wait_menu
from test_germany_story import leave_gym
from key_item_test_helpers import reload
import test_oxford_gym as rock
import test_chantilly_gym as water
import test_oranienburg_gym as electric

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,(city,gym,lead) in enumerate([('Oxford',rock,7),('Chantilly',water,15),('Oranienburg',electric,20)]):
  for mode,expected in [('claimed',lead),('pending',lead-1)]:
   source=f'gym-onward-{city}-returned' if mode=='claimed' else f'gym-pending-{city}-tm'
   load_checkpoint(e,source,True)
   assert gym.badge(e) and e.var(gym.TM_REWARD)==int(mode=='claimed')
   inspect(e,expected,f'gym-consistency-{city}-{mode}')
   print(f'PASS: {city} {mode} journal selects saved lead {expected}, shows only earned stamps/badges and switches topics read-only',flush=True)
   e=reload(e,f'gym-journal-{city}-{mode}')
   inspect(e,expected,f'gym-consistency-{city}-{mode}-continued')
   print(f'PASS: {city} {mode} journal priority and earned checklist persist through normal Save/cold Continue without reward or story changes',flush=True)
  load_checkpoint(e,f'gym-onward-{city}-returned',True)
  if index==1:leave_gym(e)
  else:e.walk('DOWN',10);e.frames(180)
  go(e,(16,14));travel(e,index+1 if index<2 else 0)
  if index<2:
   go(e,(10,14));before=preserved(e)
   e.press('DOWN');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);e.finish_dialogue()
   var=0x40FD if index==0 else 0x40FF
   assert e.var(var)==1
   inspect(e,lead+1,f'gym-consistency-{city}-accepted')
   accepted=preserved(e);e=reload(e,f'gym-journal-{city}-accepted')
   inspect(e,lead+1,f'gym-consistency-{city}-accepted-continued');assert preserved(e)==accepted
   assert accepted[0:2]==before[0:2] and accepted[3:]==before[3:]
   print(f'PASS: {city} normal next-contact acceptance updates the journal to the actual new task; accepted task and read-only journal survive cold Continue',flush=True)
  else:
   assert e.var(0x40F2)==0
   guide(e);assert e.var(0x40F2)==1
   inspect(e,21,'gym-consistency-Oranienburg-London-stamp')
   stamp=preserved(e);guide(e);assert preserved(e)==stamp
   e=reload(e,'gym-journal-Oranienburg-London-stamp')
   inspect(e,21,'gym-consistency-Oranienburg-stamp-continued');assert preserved(e)==stamp
   print('PASS: after Oranienburg, normal London guide talk records its optional stamp once; the journal advances to the missing Paris stamp and remains correct after cold Continue',flush=True)
finally:e.close()
