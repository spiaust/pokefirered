"""Native rival declines, clinic round trip, and correct accepted battle."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_france_story import npc
from test_tour import travel,item_count
from test_country import wait_menu,party_species
from test_trainers import defeated
from test_time import preserved
from test_tour_journal import inspect
from key_item_test_helpers import reload

def offer(e,capture=False):
 npc(e);e.frames(900)
 for i in range(2):
  if capture:e.screenshot(ROOT/f'test-output/rival-prep-offer-{i}.png')
  e.press('A',900)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
 if capture:e.screenshot(ROOT/'test-output/rival-prep-offer-2.png')

def decline(e,choice,capture=False):
 offer(e,capture)
 if choice=='NO':e.press('DOWN');e.press('A',900)
 else:e.press('B',900)
 for i in range(3):
  assert e.read('sLockFieldControls',1)
  if capture:e.screenshot(ROOT/f'test-output/rival-prep-decline-{i}.png')
  e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'regional-guide-Oxford-claimed',True)
 assert defeated(e,0) and defeated(e,3) and not defeated(e,6)
 if e.var(0x40FB)==0:
  go(e,(16,14));travel(e,0);go(e,(10,14));npc(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);e.finish_dialogue()
  go(e,(16,14));travel(e,3)
 go(e,(10,14));assert e.var(0x40FB)==1 and item_count(e,184)==0
 before=preserved(e);decline(e,'NO',True);decline(e,'B');assert preserved(e)==before and not e.in_battle()
 e=reload(e,'rival-prep-ready');decline(e,'NO');inspect(e,3,'rival-prep-ready');assert preserved(e)==before
 print('PASS: genuinely earned trail wins unlock three-page rival offer; No/B show three clinic pages and cold Continue/journal retain the undecided match without rewards',flush=True)
 baseline=preserved(e)[1:];go(e,(6,10));e.walk('UP',1);e.frames(180);e.walk('UP',4);e.walk('RIGHT',1)
 assert e.location()==(43,15,7,4),e.location()
 e.press('UP');e.press('A',180);e.finish_dialogue()
 count=e.read('gPlayerPartyCount',1)
 for i in range(count):
  p=e.symbols['gPlayerParty']+i*100;assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
 assert preserved(e)[1:]==baseline
 e=reload(e,'rival-prep-healed');e.walk('DOWN',5);e.frames(180);go(e,(10,14));before=preserved(e);decline(e,'B');assert preserved(e)==before
 print('PASS: west-square clinic directions reach the nurse; native free healing, cold Continue and return preserve money, items and undecided rival progress',flush=True)
 e=reload(e,'rival-prep-returned');offer(e);e.press('A',180)
 for _ in range(30):
  if e.in_battle():break
  e.press('A',90)
 assert e.in_battle();e.frames(300)
 assert e.read('gTrainerBattleOpponent_A',2)==749 and tuple(party_species(e,'gEnemyParty',i) for i in range(2))==(16,133)
 assert not defeated(e,6) and e.var(0x40FB)==1 and item_count(e,184)==0
 e.screenshot(ROOT/'test-output/rival-prep-battle.png')
 print('PASS: normal return and Yes start the correct Pidgey/Eevee rival battle; entering battle grants no premature win, report or Bell',flush=True)
finally:e.close()
