"""Use genuinely taught Rock Tomb/Water Pulse and recover PP with native care."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_country import party_species
from test_landmark_cases import go
from test_tour import travel
from test_time import preserved
from test_trainers import money
from test_oxford_gym import count_pocket
from battle_recovery_test_helpers import moves_pp
from key_item_test_helpers import reload

def action(e):
 fn=next(int(line.split()[0],16) for line in (ROOT/'pokefirered.sym').read_text().splitlines() if line.split()[-1:]==['HandleInputChooseAction'])
 return e.read('gBattlerControllerFuncs')&~1==fn

def finish(e):
 for _ in range(200):
  if not e.in_battle():break
  if action(e):e.press('DOWN');e.press('RIGHT');e.press('A',90)
  else:e.press('B',60)
 assert not e.in_battle();e.frames(180);e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 for name,tm,move in [('Rock-Tomb',327,317),('Water-Pulse',291,352)]:
  load_checkpoint(e,f'gym-tm-{name}-learned',True)
  assert party_species(e)==284 and count_pocket(e,tm,0x464,58)==0
  history=tuple(e.var(v) for v in range(0x40C0,0x4100));before=preserved(e)[1:]
  go(e,(16,14));travel(e,0);go(e,(15,1));e.walk('UP',2)
  assert e.location()==(43,1,15,23)
  e.walk('UP',6);e.walk('LEFT',9);e.walk('UP',2)
  for _ in range(600):
   if e.in_battle():break
   e.walk('RIGHT' if e.location()[2]<=6 else 'LEFT',1)
  assert e.in_battle();e.frames(300)
  oldmoves,oldpp=moves_pp(e);assert oldmoves[0]==move
  mon=e.symbols['gBattleMons'];hp=e.read(mon+88+0x28,2);target=party_species(e,'gEnemyParty')
  for _ in range(400):
   if not e.in_battle():break
   if action(e):e.press('UP');e.press('LEFT');e.press('A',30)
   elif e.read('gBattlerControllerFuncs')&~1==e.symbols['HandleInputChooseMove']:
    e.press('UP');e.press('LEFT');e.press('A',30)
   else:e.press('A',30)
   if moves_pp(e)[1][0]<oldpp[0] and e.read(mon+88+0x28,2)<hp:break
  currentmoves,currentpp=moves_pp(e)
  assert currentmoves==oldmoves and currentpp[0]<oldpp[0] and currentpp[1:]==oldpp[1:]
  used=oldpp[0]-currentpp[0];assert e.read('gCurrentMove',2)==move and e.read(mon+88+0x28,2)<hp
  e.screenshot(ROOT/f'test-output/gym-tm-battle-{name}-used.png')
  if e.in_battle():finish(e)
  assert moves_pp(e)==(currentmoves,currentpp) and preserved(e)[1:]==before
  print(f'PASS: {name} taught Marshtomp move damages real wild species {target}, spends {used} PP and leaves other moves/PP, money, inventory and progress intact',flush=True)
  e=reload(e,f'gym-tm-battle-{name}-used')
  assert moves_pp(e)==(currentmoves,currentpp) and count_pocket(e,tm,0x464,58)==0
  assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
  print(f'PASS: {name} learned move, spent battle PP and consumed TM persist through normal Save/cold Continue',flush=True)
  x,y=e.location()[2:];e.walk('DOWN',17-y);e.walk('RIGHT',15-x);e.walk('DOWN',7)
  assert e.location()==(43,0,15,0)
  go(e,(6,10));e.walk('UP',1);e.frames(180);e.walk('UP',4);e.walk('RIGHT',1)
  cash=money(e);e.press('UP');e.press('A',180);e.finish_dialogue()
  learned,pp=moves_pp(e)
  assert learned==currentmoves and all(pp[i]==e.read(e.symbols['gBattleMoves']+12*m+4,1) for i,m in enumerate(learned))
  assert e.read(e.symbols['gPlayerParty']+86,2)==e.read(e.symbols['gPlayerParty']+88,2)
  assert money(e)==cash and preserved(e)[1:]==before
  e.screenshot(ROOT/f'test-output/gym-tm-battle-{name}-clinic.png')
  e=reload(e,f'gym-tm-battle-{name}-healed')
  assert moves_pp(e)==(learned,pp) and count_pocket(e,tm,0x464,58)==0
  print(f'PASS: {name} free London clinic restores all learned-move PP and HP without returning the TM or charging money; healed state survives cold Continue',flush=True)
finally:
 e.screenshot(ROOT/'test-output/gym-tm-battle-final.png');e.close()
