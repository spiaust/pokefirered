"""Catch a wild compatible partner, teach an earned TM and use it normally."""
import struct
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_country import party_species
from test_landmark_cases import go
from test_tour import travel
from test_gym_ui import start_action
from test_navigation import wait_task
from test_trainers import money
from test_oxford_gym import count_pocket
from battle_recovery_test_helpers import orders
from tm_teaching_test_helpers import select,field,state
from key_item_test_helpers import reload

def moves(e,index):
 p=e.symbols['gPlayerParty']+100*index;personality=e.read(p);key=personality^e.read(p+4)
 slot=orders[personality%24][1]
 data=b''.join(struct.pack('<I',e.read(p+32+slot*12+j)^key) for j in (0,4,8))
 return struct.unpack('<4H',data[:8]),tuple(data[8:])

def action(e):
 fn=next(int(line.split()[0],16) for line in (ROOT/'pokefirered.sym').read_text().splitlines() if line.split()[-1:]==['HandleInputChooseAction'])
 return e.read('gBattlerControllerFuncs')&~1==fn

def run(e):
 for _ in range(150):
  if not e.in_battle():break
  if action(e):
   e.press('DOWN');e.press('RIGHT');e.press('A',90)
  else:e.press('B',60)
 assert not e.in_battle();e.frames(180);e.finish_dialogue()

def encounter(e):
 for _ in range(600):
  if e.in_battle():break
  x=e.location()[2];e.walk('RIGHT' if x<=6 else 'LEFT',1)
 assert e.in_battle();e.frames(300)

def throw(e):
 e.press('UP');e.press('LEFT');e.press('RIGHT');e.press('A',180)
 wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
 for _ in range(5):
  if e.read(bag+6,2)==2:break
  e.press('RIGHT',90)
 ball=3 if count_pocket(e,3,0x430,13) else 4
 assert count_pocket(e,ball,0x430,13)>0
 base=e.read('gSaveBlock1Ptr')+0x430;target=next(i for i in range(13) if e.read(base+4*i,2)==ball)
 for _ in range(30):
  cursor=e.read(bag+12,2)+e.read(bag+18,2)
  if cursor==target:break
  e.press('DOWN' if cursor<target else 'UP')
 assert cursor==target
 e.press('A',90);e.press('A',180)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'walkthrough-germany-complete',True)
 assert e.read('gPlayerPartyCount',1)==1 and count_pocket(e,322,0x464,58)==1
 history=tuple(e.var(v) for v in range(0x40C0,0x4100));cash=money(e)
 go(e,(16,14));travel(e,0);go(e,(15,1));e.walk('UP',2);assert e.location()==(43,1,15,23)
 e.walk('UP',6);e.walk('LEFT',9);e.walk('UP',2)
 seen=[];throws=0
 for _ in range(50):
  encounter(e);species=party_species(e,'gEnemyParty');seen.append(species)
  if species!=179:run(e);continue
  e.screenshot(ROOT/'test-output/shock-wave-wild-Mareep.png')
  for _ in range(1600):
   if not e.in_battle() and e.read('gPlayerPartyCount',1)==2:break
   if e.in_battle() and action(e):throw(e);throws+=1
   else:e.press('B',60)
  assert e.read('gPlayerPartyCount',1)==2 and not e.in_battle();break
 assert e.read('gPlayerPartyCount',1)==2 and party_species(e,index=1)==179
 e.frames(180);e.finish_dialogue()
 assert money(e)==cash and tuple(e.var(v) for v in range(0x40C0,0x4100))==history
 print(f'PASS: normal London countryside walking finds and catches Mareep with {throws} earned balls after {len(seen)} encounters; no party/inventory/progress edits',flush=True)
 e=reload(e,'shock-wave-Mareep-caught');assert party_species(e,index=1)==179
 oldmoves,oldpp=moves(e,1);empty=oldmoves.index(0);before=state(e)
 select(e,322);e.press('RIGHT',60);assert e.read(e.symbols['gPartyMenu']+9,1)==1
 e.press('B',180);field(e);assert state(e)==before
 print('PASS: compatible Mareep selection can be canceled without consuming the earned Shock Wave TM or changing tested state',flush=True)
 select(e,322);e.press('RIGHT',60);assert e.read(e.symbols['gPartyMenu']+9,1)==1
 e.press('A',900)
 for _ in range(40):
  if count_pocket(e,322,0x464,58)==0:break
  e.press('A',90)
 assert count_pocket(e,322,0x464,58)==0
 e.press('A',180);field(e);newmoves,newpp=moves(e,1)
 expected=list(oldmoves);expected[empty]=351
 assert newmoves==tuple(expected) and newpp[empty]==20
 assert all(newpp[i]==oldpp[i] for i in range(4) if i!=empty)
 after=state(e);assert after[1:3]==before[1:3] and after[4:]==before[4:]
 bag=before[3].copy();bag[(322,1)]-=1;assert +bag==after[3]
 e.screenshot(ROOT/'test-output/shock-wave-taught.png')
 e=reload(e,'shock-wave-Mareep-taught');assert moves(e,1)==(newmoves,newpp) and state(e)==after
 print('PASS: normal empty-slot teaching gives Mareep Shock Wave with 20 PP, consumes one earned TM, preserves other moves/progress and survives cold Continue',flush=True)
 start_action(e,1);wait_task(e,'Task_HandleChooseMonInput');e.frames(60)
 e.press('RIGHT',60);e.press('A',180);e.press('DOWN',60);e.press('A',180)
 e.press('LEFT',60);e.press('A',180);e.press('B',180);e.press('B',180)
 assert party_species(e)==179 and party_species(e,index=1)==284
 encounter(e);mon=e.symbols['gBattleMons'];enemy_hp=e.read(mon+88+0x28,2)
 for _ in range(400):
  if not e.in_battle():break
  if action(e):e.press('UP');e.press('LEFT');e.press('A',30)
  elif e.read('gBattlerControllerFuncs')&~1==e.symbols['HandleInputChooseMove']:
   e.press('UP');e.press('LEFT')
   if empty&1:e.press('RIGHT')
   if empty&2:e.press('DOWN')
   e.press('A',30)
  else:e.press('A',30)
  if moves(e,0)[1][empty]==19 and e.read(mon+88+0x28,2)<enemy_hp:break
 assert moves(e,0)[0][empty]==351 and moves(e,0)[1][empty]==19
 assert e.read('gCurrentMove',2)==351 and e.read(mon+88+0x28,2)<enemy_hp
 e.screenshot(ROOT/'test-output/shock-wave-battle-used.png')
 if e.in_battle():run(e)
 e=reload(e,'shock-wave-Mareep-battle');assert moves(e,0)[1][empty]==19 and count_pocket(e,322,0x464,58)==0
 assert tuple(e.var(v) for v in range(0x40C0,0x4100))==history
 print('PASS: naturally caught Mareep uses taught Shock Wave in a real wild battle, damages its target and spends one PP; battle PP and consumed TM persist through cold Continue',flush=True)
finally:
 e.screenshot(ROOT/'test-output/shock-wave-final.png');e.close()
