"""Decline each trail trainer with No/B and follow the new clinic route."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from test_country import wait_menu,party_species
from test_trainers import defeated
from key_item_test_helpers import reload

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,city,species in [(0,'London',1),(1,'Paris',152),(2,'Berlin',277)]:
  load_checkpoint(e,'clinic-directions-'+city,True)
  assert e.location()[:2]==(43,index*4+3) and not defeated(e,index),e.location()
  e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
  e.walk('DOWN',5);e.frames(180)
  assert e.location()[:2]==(43,index*4),e.location()
  go(e,(15,14));e.walk('UP',15);e.walk('UP',4);e.walk('RIGHT',2)
  assert e.location()==(43,index*4+1,17,19)
  for choice in ['NO','B']:
   e.press('UP');before=preserved(e)
   e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput')
   if choice=='NO':e.press('DOWN');e.press('A',900)
   else:e.press('B',900)
   e.press('A',900)
   e.screenshot(ROOT/f'test-output/trail-clinic-{city}-{choice}.png')
   e.finish_dialogue()
   assert not e.in_battle() and not defeated(e,index) and preserved(e)==before
   assert e.location()==(43,index*4+1,17,19) and not e.read('sLockFieldControls',1)
  print('PASS: '+city+' No/B show clinic route, unlock controls and retain exact party/items/money/progress without battle',flush=True)
  e.walk('LEFT',2);e.walk('DOWN',5);e.frames(180)
  assert e.location()==(43,index*4,15,0),e.location()
  go(e,(6,10));e.walk('UP',1);e.frames(180)
  assert e.location()[:2]==(43,index*4+3),e.location()
  e=reload(e,'trail-clinic-'+city)
  e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
  p=e.symbols['gPlayerParty'];assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
  e.walk('DOWN',5);e.frames(180)
  assert e.location()==(43,index*4,6,10) and preserved(e)[1:]==before[1:]
  assert not defeated(e,index) and party_species(e)==species and e.var(0x40F0)==index+1
  print('PASS: '+city+' clear south path reaches west clinic; indoor cold Continue, free nurse care and return preserve starter and progress',flush=True)
finally:e.close()
