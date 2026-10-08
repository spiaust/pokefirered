"""Follow clinic signs from fresh country starts and retain service on Continue."""
from emulator import Emulator,ROOT
from test_country import start_new_game,wait_menu,party_species
from test_landmark_cases import go,talk
from test_time import preserved
from key_item_test_helpers import reload
from test_celebi import load_checkpoint

e=Emulator(ROOT/'pokefirered.gba')
try:
 start_new_game(e)
 for choice,city,species in [(0,'London',1),(1,'Paris',152),(2,'Berlin',277)]:
  e.state(ROOT/'test-output/country-menu.state',True)
  for _ in range(choice):e.press('DOWN')
  e.press('A',180);wait_menu(e,'Task_MultichoiceMenu_HandleInput')
  e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput')
  e.press('A',900);e.finish_dialogue()
  assert e.location()==(43,choice*4,15,14) and party_species(e)==species
  go(e,(5,12));e.press('UP');before=preserved(e)
  e.press('A',900);e.press('A',900)
  e.screenshot(ROOT/f'test-output/clinic-directions-{city}.png')
  e.finish_dialogue();assert preserved(e)==before
  talk(e,(5,12));assert preserved(e)==before
  print('PASS: '+city+' fresh clinic sign displays directions and repeats without changing party/items/progress',flush=True)
  go(e,(6,10));e.walk('UP',1);e.frames(180)
  assert e.location()[:2]==(43,choice*4+3)
  e=reload(e,'clinic-directions-'+city)
  e.walk('UP',4);e.walk('RIGHT',1);e.press('UP');e.press('A',180);e.finish_dialogue()
  for i in range(e.read('gPlayerPartyCount',1)):
   p=e.symbols['gPlayerParty']+100*i
   assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
  e.walk('DOWN',5);e.frames(180)
  assert e.location()==(43,choice*4,6,10) and preserved(e)[1:]==before[1:]
  assert e.var(0x40F0)==choice+1 and party_species(e)==species
  print('PASS: '+city+' directions reach nurse; indoor cold Continue, free care and exit retain starter/items/progress',flush=True)
 load_checkpoint(e,'landmark-guide-v120',True)
 go(e,(5,12));e.press('UP');before=preserved(e)
 e.press('A',900);e.press('A',900);e.finish_dialogue()
 assert preserved(e)==before
 print('PASS: older completed-game battery retains exact state while reading new clinic instructions',flush=True)
finally:e.close()
