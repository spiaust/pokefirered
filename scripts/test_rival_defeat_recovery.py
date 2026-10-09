"""Genuine rival defeat, clinic recovery, retry victory and report hand-in."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_france_story import npc,talk
from test_country import wait_menu
from test_trainers import defeated,money
from test_tour import travel,item_count
from test_time import preserved
from test_tour_journal import inspect
from battle_recovery_test_helpers import lose,moves_pp
from test_challenges import fight_with_supplies
from key_item_test_helpers import reload
from collections import Counter

def inventory_state(state):
 return state[:3]+(Counter((item,qty) for item,qty in state[3] if item),)+state[4:]

def offer(e):
 npc(e)
 for _ in range(12):
  if e.task_active('Task_YesNoMenu_HandleInput'):break
  e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)

def begin(e):
 offer(e);e.press('A',180)
 for _ in range(30):
  if e.in_battle():break
  e.press('A',90)
 assert e.in_battle();e.frames(300);assert e.read('gTrainerBattleOpponent_A',2)==749

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'rival-prep-returned',True)
 assert e.var(0x40FB)==1 and defeated(e,0) and defeated(e,3) and not defeated(e,6)
 before=preserved(e);funds=money(e);healed=moves_pp(e)
 begin(e);commands=lose(e)
 assert commands>0 and e.location()[:2]==(43,15),e.location()
 assert money(e)<funds and e.var(0x40FB)==1 and not defeated(e,6) and item_count(e,184)==0
 after=preserved(e);assert after[2:]==before[2:] and defeated(e,0) and defeated(e,3)
 assert moves_pp(e)==healed
 for i in range(e.read('gPlayerPartyCount',1)):
  p=e.symbols['gPlayerParty']+100*i;assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
 e.screenshot(ROOT/'test-output/rival-recovery-clinic.png')
 print('PASS: native non-damaging battle commands cause a real rival loss; Oxford clinic restores HP/status/PP, normal loss fee applies, and no win/report/reward is granted',flush=True)
 e=reload(e,'rival-recovery-healed');assert preserved(e)==after
 e.walk('DOWN',5);e.frames(180);go(e,(10,14));before=preserved(e)
 for choice in ['B','NO']:
  offer(e)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
  e.finish_dialogue();assert preserved(e)==before and not e.in_battle()
 inspect(e,3,'rival-recovery');assert preserved(e)==before
 e=reload(e,'rival-recovery-ready');assert preserved(e)==before
 print('PASS: real defeat survives cold Continue; walking back restores the optional offer, No/B and journal remain read-only, and retry readiness saves normally',flush=True)
 funds=money(e);begin(e);fight_with_supplies(e)
 assert defeated(e,6) and money(e)>funds and e.var(0x40FB)==1 and item_count(e,184)==0
 after=preserved(e);talk(e);assert preserved(e)==after
 e=reload(e,'rival-recovery-won');talk(e);inspect(e,4,'rival-recovery-won')
 assert inventory_state(preserved(e))==inventory_state(after)
 e.screenshot(ROOT/'test-output/rival-recovery-won.png')
 print('PASS: genuine retry victory pays once and unlocks the report; repeat rival talk, journal and cold Continue preserve completion without an early Bell',flush=True)
 go(e,(16,14));travel(e,0);go(e,(10,14));talk(e)
 assert e.var(0x40FB)==2 and item_count(e,184)==1
 after=preserved(e);talk(e);e=reload(e,'rival-recovery-claimed');talk(e);inspect(e,5,'rival-recovery-claimed');assert preserved(e)==after
 e.screenshot(ROOT/'test-output/rival-recovery-claimed.png')
 print('PASS: normally returning the retry victory report to Oak aide grants one Bell; repeats/cold Continue retain the reward and Oxford Gym journal without duplicates',flush=True)
finally:e.close()
