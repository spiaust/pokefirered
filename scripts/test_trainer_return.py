"""Follow extended victories to the clinic and one-time regional reward."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_time import preserved
from test_tour import item_count,guide
from test_trainers import defeated
from key_item_test_helpers import reload

def advice(e,city,label):
 before=preserved(e);e.press('UP');e.press('A',900)
 for page in range(3):
  assert e.read('sLockFieldControls',1) and not e.in_battle()
  e.screenshot(ROOT/f'test-output/trainer-return-{city}-{label}-{page}.png');e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before

def north(e,index):
 e.walk('LEFT',2);e.walk('UP',20);e.frames(180)
 assert e.location()==(43,index*4+12,15,23)

def trainer(e,index):
 go(e,(15,23));e.walk('DOWN',1);e.frames(180);e.walk('DOWN',19);e.walk('RIGHT',2)
 assert e.location()==(43,index*4+13,17,19)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,city in enumerate(['Oxford','Chantilly','Oranienburg']):
  load_checkpoint(e,f'long-trail-{city}-won',True)
  assert defeated(e,index) and defeated(e,index+3) and e.var(0x40F8+index)==0
  advice(e,city,'first');advice(e,city,'repeat');e=reload(e,f'trainer-return-{city}-unclaimed');advice(e,city,'continued')
  print(f'PASS: {city} earned-victory return directions repeat and cold Continue without changing party/items, prize money or unclaimed reward',flush=True)
  before=preserved(e)[1:];north(e,index);go(e,(6,10));e.walk('UP',1);e.frames(180);e.walk('UP',4);e.walk('RIGHT',1)
  e.press('UP');e.press('A',180);e.finish_dialogue()
  p=e.symbols['gPlayerParty'];assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
  assert preserved(e)[1:]==before
  e=reload(e,f'trainer-return-{city}-clinic');e.walk('DOWN',5);e.frames(180);go(e,(16,14))
  count=item_count(e,68);guide(e);assert e.var(0x40F8+index)==1 and item_count(e,68)==count+1
  claimed=preserved(e);guide(e);assert preserved(e)==claimed
  e=reload(e,f'trainer-return-{city}-claimed');guide(e);assert preserved(e)==claimed
  print(f'PASS: {city} clear north path reaches west-square free clinic and square guide; earned two-win reward grants one Candy through repeats and cold Continue',flush=True)
  trainer(e,index);advice(e,city,'after-claim');e=reload(e,f'trainer-return-{city}-revisited');advice(e,city,'revisit-continued')
  assert defeated(e,index) and defeated(e,index+3) and e.var(0x40F8+index)==1 and item_count(e,68)==count+1
  north(e,index);go(e,(16,14));before=preserved(e);guide(e);assert preserved(e)==before
  print(f'PASS: {city} return to defeated trainer and another cold Continue cannot restart battle, repay prize or duplicate the claimed regional reward',flush=True)
finally:e.close()
