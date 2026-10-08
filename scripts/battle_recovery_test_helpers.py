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
