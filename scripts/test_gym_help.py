"""Follow each leader's optional battle and clinic help with normal controls."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_country import wait_menu,party_species
from test_time import preserved
from test_trainers import defeated,money
from key_item_test_helpers import reload
from test_germany_story import leave_gym
from battle_recovery_test_helpers import begin
import test_oxford_gym as rock
import test_chantilly_gym as water
import test_oranienburg_gym as electric

def leave_clinic(e):
 x,y=e.location()[2:]
 if x!=7:e.walk('RIGHT' if x<7 else 'LEFT',abs(x-7))
 if y!=4:e.walk('UP' if y>4 else 'DOWN',abs(y-4))
 e.walk('DOWN',5);e.frames(180)

def approach(e,index):
 go(e,(15,10));e.walk('UP',1);e.frames(180)
 if index==1:water.approach(e)
 else:e.walk('UP',8)

def prompt(e,gym,city):
 gym.leader(e);e.frames(900)
 e.screenshot(ROOT/f'test-output/gym-help-{city}-intro.png')
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,(city,gym,team) in enumerate([('Oxford',rock,(74,95)),('Chantilly',water,(54,116)),('Oranienburg',electric,(100,25))]):
  load_checkpoint(e,f'gym-defeat-{city}-recovered',True);leave_clinic(e);approach(e,index)
  assert not gym.badge(e) and not defeated(e,index+7) and e.var(gym.TM_REWARD)==0
  original=preserved(e)
  for choice in ['NO','B']:
   prompt(e,gym,city)
   if choice=='NO':e.press('DOWN');e.press('A',900)
   else:e.press('B',900)
   e.press('A',900);e.screenshot(ROOT/f'test-output/gym-help-{city}-{choice}-exit.png')
   e.press('A',900);e.screenshot(ROOT/f'test-output/gym-help-{city}-{choice}-clinic.png')
   e.finish_dialogue();assert not e.in_battle() and preserved(e)==original
  print(f'PASS: {city} optional battle help and No/B decline show exit/clinic directions without changing party, money, items, badges or progress',flush=True)
  if index==1:leave_gym(e)
  else:e.walk('DOWN',10);e.frames(180)
  assert e.location()[:2]==(43,12+index*4)
  go(e,(6,10));e.walk('UP',1);e.frames(180)
  e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
  p=e.symbols['gPlayerParty'];assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
  assert preserved(e)[1:]==original[1:]
  e=reload(e,f'gym-help-{city}-clinic');leave_clinic(e);approach(e,index)
  assert not gym.badge(e) and not defeated(e,index+7)
  print(f'PASS: {city} leader exit reaches the west-square free clinic; indoor cold Continue and return retain the unbeaten Gym',flush=True)
  funds=money(e);begin(e);assert e.read('gTrainerBattleOpponent_A',2)==750+index
  assert tuple(party_species(e,'gEnemyParty',i) for i in range(2))==team
  gym.gym_fight(e)
  assert gym.badge(e) and defeated(e,index+7) and e.var(gym.TM_REWARD)==1 and gym.tm_count(e)==1 and money(e)>funds
  won=preserved(e);gym.complete_talk(e);assert preserved(e)==won
  e=reload(e,f'gym-help-{city}-won');gym.complete_talk(e);assert preserved(e)==won
  print(f'PASS: {city} accepted battle uses correct leader/team; normal victory, badge, one TM and prize survive repeat talk and cold Continue',flush=True)
finally:e.close()
