"""Earned Gym-ready batteries use native reads, saves, door walks and declines."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from key_item_test_helpers import reload
from test_country import wait_menu
from test_tour_journal import inspect
from test_germany_story import leave_gym
from test_chantilly_gym import approach
import struct

def grid(e,city):
 width=72 if city=='Chantilly' else 64;w=e.read('VMap');base=e.read(e.symbols['VMap']+8)
 expected=struct.unpack('<%dH'%(width*24),(ROOT/f'data/layouts/Europe{city}/map.bin').read_bytes())
 assert tuple(e.read(base+2*((y+7)*w+x+7),2) for y in range(24) for x in range(width))==expected

e=Emulator(ROOT/'pokefirered.gba')
try:
 for city,town,gym,lead in [('Oxford',12,24,5),('Chantilly',16,25,13),('Oranienburg',20,26,18)]:
  load_checkpoint(e,'tour-approach-'+city,True);original=preserved(e)[1:];grid(e,city);go(e,(14,12))
  before=preserved(e),e.location();e.press('UP');e.press('A',900);assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/gym-sign-{city}.png');e.finish_dialogue();assert (preserved(e),e.location())==before
  e=reload(e,'gym-sign-'+city);assert (preserved(e),e.location())==before;grid(e,city)
  e.press('UP');e.press('A',900);e.finish_dialogue();assert (preserved(e),e.location())==before
  go(e,(15,10));e.screenshot(ROOT/f'test-output/gym-sign-{city}-field.png');e.walk('UP',1);e.frames(180)
  assert e.location()==(43,gym,8 if city=='Chantilly' else 6,18 if city=='Chantilly' else 14)
  inspect(e,lead,'gym-sign-'+city+'-entry');saved=preserved(e),e.location();e=reload(e,'gym-sign-'+city+'-inside');assert (preserved(e),e.location())==saved
  if city=='Chantilly':approach(e)
  else:e.walk('UP',8)
  before=preserved(e);e.press('UP');e.press('A',900);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('B',180);e.finish_dialogue()
  assert not e.in_battle() and preserved(e)==before
  if city=='Chantilly':leave_gym(e);e.walk('LEFT',1);e.walk('UP',4)
  else:e.walk('DOWN',10);e.frames(180)
  assert e.location()==(43,town,15,10) and preserved(e)[1:]==original;grid(e,city)
  e=reload(e,'gym-sign-'+city+'-returned');assert e.location()==(43,town,15,10) and preserved(e)[1:]==original
  print(f'PASS: {city} Gym sign read/repeat/cold Continue, entry/readiness/indoor save, leader decline and exit retain progress',flush=True)
finally:e.close()
