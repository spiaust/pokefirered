"""Catch wild legendaries with earned supplies, native damage and catch odds."""
from emulator import Emulator,ROOT
import test_eclipse_natural as natural
from test_oxford_gym import count_pocket
from test_navigation import wait_task
from test_shadow_runtime import monfield
from battle_recovery_test_helpers import orders

def boxed_records(e,species):
 storage=e.read('gPokemonStoragePtr')+4;result=[]
 for i in range(14*30):
  p=storage+80*i;person=e.read(p);trainer=e.read(p+4);key=person^trainer
  blocks=tuple(tuple(e.read(p+32+12*orders[person%24][block]+j)^key for j in (0,4,8)) for block in range(4))
  if blocks[0][0]&65535==species:result.append((person,trainer,blocks))
 return tuple(result)

def boxed(e):
 storage=e.read('gPokemonStoragePtr')+4;result=[]
 for i in range(14*30):
  p=storage+80*i;person=e.read(p);key=person^e.read(p+4)
  species=(e.read(p+32+12*orders[person%24][0])^key)&65535
  if species:result.append(species)
 return result

def throw(e,item=2):
 before=count_pocket(e,item,0x430,13);assert before
 e.press('UP',2);e.press('LEFT',2);e.press('RIGHT',2);e.press('A',180)
 wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
 for _ in range(6):
  pocket=e.read(bag+6,2)
  if pocket==2:break
  e.press('RIGHT' if pocket<2 else 'LEFT',60)
 base=e.read('gSaveBlock1Ptr')+0x430
 target=next(i for i in range(13) if e.read(base+4*i,2)==item)
 for _ in range(30):
  cur=e.read(bag+12,2)+e.read(bag+18,2)
  if cur==target:break
  e.press('DOWN' if cur<target else 'UP',30)
 assert cur==target;e.press('A',90);e.press('A',180)
 assert count_pocket(e,item,0x430,13)==before-1

def move(e,number,fn):
 if fn==natural.first_symbol('HandleInputChooseAction'):
  e.press('UP',2);e.press('LEFT',2);e.press('A',30)
 slot=next(i for i in range(4) if e.read(e.symbols['gBattleMons']+12+2*i,2)==number and e.read(e.symbols['gBattleMons']+36+i,1))
 e.press('UP',2);e.press('LEFT',2)
 if slot&1:e.press('RIGHT',2)
 if slot&2:e.press('DOWN',2)
 e.press('A',30)

def quick_attack_max_damage(e):
 # Conservative critical-hit bound for neutral Quick Attack from Raichu.
 # Critical hits ignore negative Attack and positive Defense stages.
 b=e.symbols['gBattleMons'];atk=e.read(b+2,2);defense=e.read(b+88+4,2)
 attack_stage=max(6,e.read(b+25,1));defense_stage=min(6,e.read(b+88+26,1))
 atk=atk*(attack_stage-4)//2
 defense=defense*2//(8-defense_stage)
 level=e.read(b+42,1)
 return ((2*level//5+2)*40*atk//max(1,defense)//50)*2+6

def capture(e,limit=7000):
 action=natural.first_symbol('HandleInputChooseAction');movefn=natural.first_symbol('HandleInputChooseMove')
 b=e.symbols['gBattleMons'];balls=heals=attacks=0
 for _ in range(limit):
  if e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_NamingScreen']&~1:
   e.press('START',30);e.press('A',120);continue
  if not e.in_battle():break
  fn=e.read('gBattlerControllerFuncs')&~1
  if e.task_active('Task_HandleChooseMonInput'):
   living=[i for i in range(e.read('gPlayerPartyCount',1)) if e.read(e.symbols['gPlayerParty']+100*i+86,2)]
   assert living
   target=next((i for i in living if monfield(e,i,0,0)&65535==31),living[0])
   from natural_preparation_test_helpers import choose
   choose(e,target);e.press('A',180);e.press('A',180);e.frames(300);continue
  if fn in (action,movefn):
   hp,maxhp=e.read(b+40,2),e.read(b+44,2);status=e.read(b+76)
   enemyhp,enemymax,enemystatus=e.read(b+128,2),e.read(b+132,2),e.read(b+164)
   preparing=enemyhp*5>enemymax or not enemystatus
   if hp*2<maxhp or status&32 and preparing:
    item=19 if status and count_pocket(e,19,0x310,42) else 21
    if count_pocket(e,item,0x310,42) and (hp*2<maxhp or status&32 and preparing):
     if fn==movefn:e.press('B',30)
     natural.use_battle_heal(e,item);heals+=1;continue
   enemyhp,enemymax,status=e.read(b+128,2),e.read(b+132,2),e.read(b+164)
   species=e.read(b,2)
   if species==26 and not status and e.read(b+36+2,1):
    move(e,86,fn);attacks+=1;continue
   if species==26 and enemyhp*5>enemymax and enemyhp>quick_attack_max_damage(e) and e.read(b+36+3,1):
    move(e,98,fn);attacks+=1;continue
   if fn==movefn:e.press('B',30)
   print('Native capture throw:',balls+1,'enemy HP',enemyhp,enemymax,'status',status,'player',species,hp,flush=True)
   throw(e);balls+=1
  else:e.press('A',30)
 else:raise AssertionError('native capture stalled')
 outcome=e.read('gBattleOutcome',1);e.finish_dialogue();e.frames(240)
 assert outcome in (1,7),('natural capture failed',outcome,balls,heals,attacks)
 return outcome,balls,heals,attacks
