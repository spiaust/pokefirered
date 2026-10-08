"""Natural Gym losses and retries from existing story-earned batteries."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_trainers import defeated,money
from test_time import preserved
from test_country import wait_menu
from key_item_test_helpers import reload
from battle_recovery_test_helpers import moves_pp,begin,lose
import test_oxford_gym as rock
import test_chantilly_gym as water
import test_oranienburg_gym as electric

def heal(e,index):
 go(e,(6,10));e.walk('UP',1);e.frames(180)
 e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
 assert e.location()==(43,15+index*4,7,4)
 e.walk('DOWN',5);e.frames(180)

def approach(e,index):
 go(e,(15,10));e.walk('UP',1);e.frames(180)
 if index==1:water.approach(e)
 else:e.walk('UP',8)
 assert e.location()==(43,24+index,*((8,7) if index==1 else (6,6)))

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,(city,source,gym) in enumerate([
  ('Oxford','story-complete',rock),
  ('Chantilly','water-gym-entrance',water),
  ('Oranienburg','electric-gym-entrance',electric)]):
  load_checkpoint(e,source,True)
  if index==0:go(e,(16,14));travel(e,3)
  else:e.walk('DOWN',2);e.frames(180)
  heal(e,index);approach(e,index)
  assert not gym.badge(e) and not defeated(e,index+7) and e.var(gym.TM_REWARD)==0
  initial=preserved(e);tm=gym.tm_count(e);moves,pp=moves_pp(e)
  assert moves[1] in (43,45)
  level=e.read(e.symbols['gPlayerParty']+84,1)
  badges=initial[4][0].bit_count();assert badges==index
  begin(e);assert e.read('gTrainerBattleOpponent_A',2)==750+index
  turns=lose(e)
  assert e.location()[:2]==(43,15+index*4),e.location()
  loss=min(initial[1],level*4*[2,4,6][badges])
  assert money(e)==initial[1]-loss
  assert preserved(e)[2:]==initial[2:] and moves_pp(e)==(moves,pp)
  p=e.symbols['gPlayerParty'];assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
  assert not gym.badge(e) and not defeated(e,index+7) and gym.tm_count(e)==tm
  e.screenshot(ROOT/f'test-output/gym-defeat-{city}-clinic.png')
  print(f'PASS: {city} natural loss after {turns} status moves: local clinic, full HP/PP, exact {loss} money loss, no unearned badge/TM/victory',flush=True)
  e=reload(e,f'gym-defeat-{city}-recovered')
  x,y=e.location()[2:]
  if x!=7:e.walk('RIGHT' if x<7 else 'LEFT',abs(x-7))
  if y!=4:e.walk('UP' if y>4 else 'DOWN',abs(y-4))
  e.walk('DOWN',5);e.frames(180);approach(e,index)
  gym.leader(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);before=preserved(e)
  e.press('B',180);e.finish_dialogue();assert preserved(e)==before
  print(f'PASS: {city} recovered cold Continue returns to unbeaten leader; B declines retry without changing progress',flush=True)
  funds=money(e);begin(e);gym.gym_fight(e)
  assert gym.badge(e) and defeated(e,index+7) and e.var(gym.TM_REWARD)==1 and gym.tm_count(e)==tm+1
  assert money(e)>funds
  won=preserved(e);gym.complete_talk(e);assert preserved(e)==won
  e=reload(e,f'gym-defeat-{city}-retry-won');gym.complete_talk(e);assert preserved(e)==won
  print(f'PASS: {city} normal retry victory earns badge and one TM; repeat talk and cold Continue retain one-time rewards',flush=True)
finally:e.close()
