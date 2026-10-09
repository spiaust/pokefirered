"""Pending Gym instructions and native TM giving on explicit capacity fixtures."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_time import preserved
from test_gym_ui import open_key_item
from test_navigation import wait_task
from battle_recovery_test_helpers import orders,moves_pp
from key_item_test_helpers import reload
from tm_teaching_test_helpers import field
import test_oxford_gym as rock
import test_chantilly_gym as water
import test_oranienburg_gym as electric

def held(e):
 p=e.symbols['gPlayerParty'];personality=e.read(p);key=personality^e.read(p+4)
 return ((e.read(p+32+12*orders[personality%24][0])^key)>>16)&65535

def give(e):
 open_key_item(e,364);e.frames(180)
 for _ in range(60):e.press('UP',10)
 e.press('A',180);e.press('DOWN',60);e.press('A',180)
 wait_task(e,'Task_HandleChooseMonInput');e.frames(60)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for city,gym,tm in [('Oxford',rock,327),('Chantilly',water,291),('Oranienburg',electric,322)]:
  for mode in ['tm','key']:
   load_checkpoint(e,f'gym-capacity-{city}-{mode}-pending',True)
   assert gym.badge(e) and e.var(gym.TM_REWARD)==0
   before=preserved(e);gym.leader(e);e.frames(900)
   for page in range(4):
    assert e.read('sLockFieldControls',1)
    e.screenshot(ROOT/f'test-output/gym-pending-{city}-{mode}-{page}.png');e.press('A',900)
   e.finish_dialogue();assert preserved(e)==before
   gym.complete_talk(e);assert preserved(e)==before
   e=reload(e,f'gym-pending-{city}-{mode}');gym.complete_talk(e);assert preserved(e)==before
   print(f'PASS: {city} {mode} pending reward shows four instruction pages; repeats and cold Continue preserve badge, reward eligibility and exact state',flush=True)
   if mode=='key':continue
   assert gym.tm_count(e)==999 and held(e)==0
   moves=moves_pp(e)
   give(e);e.press('B',180);field(e);assert preserved(e)==before
   give(e);e.press('A',900)
   for _ in range(20):
    if held(e)==tm:break
    e.press('A',90)
   assert held(e)==tm and gym.tm_count(e)==998
   e.screenshot(ROOT/f'test-output/gym-pending-{city}-give.png')
   e.press('A',180);field(e)
   room=preserved(e);assert room[1:3]==before[1:3] and room[4:]==before[4:] and moves_pp(e)==moves
   assert e.var(gym.TM_REWARD)==0 and gym.badge(e)
   e=reload(e,f'gym-pending-{city}-room');assert preserved(e)==room and held(e)==tm
   print(f'PASS: {city} native TM Case Give cancellation preserves state; confirming transfers one existing TM to Bulbasaur, frees stack space and survives cold Continue',flush=True)
   gym.complete_talk(e);assert gym.tm_count(e)==999 and e.var(gym.TM_REWARD)==1 and held(e)==tm and gym.badge(e)
   claimed=preserved(e);gym.complete_talk(e);assert preserved(e)==claimed
   e=reload(e,f'gym-pending-{city}-claimed');gym.complete_talk(e);assert preserved(e)==claimed
   print(f'PASS: {city} normal leader talk grants exactly one waiting TM without a rematch; held copy remains and repeats/cold Continue duplicate no reward',flush=True)
finally:
 e.screenshot(ROOT/'test-output/gym-pending-final.png');e.close()
