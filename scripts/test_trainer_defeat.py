"""Lose through normal battle commands, recover, then earn a retry victory."""
import re,struct
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_country import wait_menu,party_species
from test_trainers import defeated,money
from test_landmark_cases import go
from test_challenges import fight_with_supplies
from test_time import preserved
from key_item_test_helpers import reload

orders={int(m[1]):tuple(map(int,m.groups()[1:])) for m in re.finditer(r'SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)',(ROOT/'src/pokemon.c').read_text())}
def moves_pp(e):
 p=e.symbols['gPlayerParty'];personality=e.read(p);key=personality^e.read(p+4)
 slot=orders[personality%24][1]
 data=b''.join(struct.pack('<I',e.read(p+32+slot*12+j)^key) for j in (0,4,8))
 return struct.unpack('<4H',data[:8]),tuple(data[8:])
def begin(e):
 e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A',180)
 for _ in range(30):
  if e.in_battle():break
  e.press('A',90)
 assert e.in_battle();e.frames(300)
def lose(e):
 action=next(int(line.split()[0],16) for line in (ROOT/'pokefirered.sym').read_text().splitlines() if line.split()[-1:]==['HandleInputChooseAction'])
 move=e.symbols['HandleInputChooseMove'];commands=0
 for _ in range(2500):
  if not e.in_battle():break
  fn=e.read('gBattlerControllerFuncs')&~1
  if fn==action:
   e.press('UP');e.press('LEFT');e.press('A',30)
  elif fn==move:
   e.press('LEFT');e.press('RIGHT')
   assert e.read('gMoveSelectionCursor',1)==1
   e.press('A',30);commands+=1
  else:e.press('A',30)
 assert not e.in_battle() and e.read('gBattleOutcome',1)==2,(commands,e.read('gBattleOutcome',1))
 e.frames(300);e.finish_dialogue();e.frames(180)
 return commands

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,city in enumerate(['London','Paris','Berlin']):
  load_checkpoint(e,'training-intro-'+city+'-ready',True)
  assert e.location()==(43,index*4+1,17,19) and not defeated(e,index)
  initial=preserved(e);species=party_species(e);moves,fullpp=moves_pp(e)
  assert moves[1] in (43,45),(city,moves)
  level=e.read(e.symbols['gPlayerParty']+84,1)
  begin(e);turns=lose(e)
  assert e.location()[:2]==(43,index*4+3) and not defeated(e,index),e.location()
  assert money(e)==initial[1]-min(initial[1],level*8),(city,money(e),initial[1])
  assert preserved(e)[2:]==initial[2:] and party_species(e)==species
  p=e.symbols['gPlayerParty'];assert e.read(p+86,2)==e.read(p+88,2) and e.read(p+80)==0
  assert moves_pp(e)==(moves,fullpp)
  e.screenshot(ROOT/f'test-output/trainer-defeat-{city}-clinic.png')
  print('PASS: '+city+' natural loss after '+str(turns)+' status-move turns returns to local clinic, restores HP/PP and charges exact loss without victory/prize/items gained',flush=True)
  e=reload(e,'trainer-defeat-'+city+'-recovered');assert not defeated(e,index)
  x,y=e.location()[2:]
  if x!=7:e.walk('RIGHT' if x<7 else 'LEFT',abs(x-7))
  if y!=4:e.walk('UP' if y>4 else 'DOWN',abs(y-4))
  assert e.location()==(43,index*4+3,7,4),e.location()
  e.press('UP');e.press('A',180);e.finish_dialogue()
  e.walk('DOWN',5);e.frames(180)
  go(e,(15,14));e.walk('UP',15);e.walk('UP',4);e.walk('RIGHT',2)
  assert e.location()==(43,index*4+1,17,19)
  e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput')
  before=preserved(e);e.press('B',180);e.finish_dialogue();assert preserved(e)==before and not defeated(e,index)
  print('PASS: '+city+' recovered cold Continue reaches still-unbeaten trainer; B safely declines the retry',flush=True)
  funds=money(e);begin(e);fight_with_supplies(e)
  assert defeated(e,index) and money(e)>funds and e.location()==(43,index*4+1,17,19)
  before=preserved(e);e.press('UP');e.press('A',180);e.finish_dialogue();assert preserved(e)==before
  e=reload(e,'trainer-defeat-'+city+'-retry-won');assert defeated(e,index) and preserved(e)==before
  print('PASS: '+city+' normal retry victory earns one prize; repeat talk and cold Continue retain earned completion',flush=True)
finally:e.close()
