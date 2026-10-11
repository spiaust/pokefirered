"""Native battle automation: normal inputs, original stats/HP/PP and native AI.

Starter checkpoints come from test_country's actual New Game button sequences.
This records outcomes; it does not require a lone starter to beat every opponent.
"""
from emulator import Emulator,ROOT
from test_shadow_runtime import talk,go
from test_continent_runtime import battle_start
import json,sys

def first_symbol(name):
 return next(int(t.split()[0],16)&~1 for t in (ROOT/'pokefirered.sym').read_text().splitlines() if t.split()[-1:]==[name])
def move_score(e,slot):
 b=e.symbols['gBattleMons'];move=e.read(b+12+2*slot,2);pp=e.read(b+36+slot,1)
 if not move or not pp:return -1
 if move==e.read(e.symbols['gDisableStructs']+4,2):return -1
 m=e.symbols['gBattleMoves']+12*move;power=e.read(m+1,1);kind=e.read(m+2,1);accuracy=e.read(m+3,1)
 if not power:return 0
 damage=power*(accuracy or 100)/100
 attack=e.read(b+(2 if kind<=8 else 8),2);defense=e.read(b+88+(4 if kind<=8 else 10),2)
 damage*=attack/max(1,defense)
 if kind in (e.read(b+33,1),e.read(b+34,1)):damage*=1.5
 targets=set([e.read(b+88+33,1),e.read(b+88+34,1)])
 table=e.symbols['gTypeEffectiveness']
 for i in range(140):
  a,d,f=(e.read(table+3*i+j,1) for j in range(3))
  if a==255:break
  if a==kind and d in targets:damage*=f/10
 return damage

def use_battle_heal(e,item,target_species=0):
 """Spend a real healing item through the native battle Bag and party menu."""
 from test_navigation import wait_task
 from test_oxford_gym import count_pocket
 before=count_pocket(e,item,0x310,42)
 assert before>0
 e.press('UP',2);e.press('LEFT',2);e.press('RIGHT',2);e.press('A',180)
 wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
 for _ in range(6):
  if e.read(bag+6,2)==0:break
  e.press('LEFT',60)
 base=e.read('gSaveBlock1Ptr')+0x310
 index=next(i for i in range(42) if e.read(base+4*i,2)==item)
 for _ in range(80):
  cur=e.read(bag+8,2)+e.read(bag+14,2)
  if cur==index:break
  e.press('DOWN' if cur<index else 'UP',30)
 assert cur==index
 e.press('A',90);e.press('A',180);wait_task(e,'Task_HandleChooseMonInput')
 count=e.read('gPlayerPartyCount',1);current=e.read('gBattlerPartyIndexes',2)
 order=[(e.read(e.symbols['gBattlePartyCurrentOrder']+i//2,1)&15) if i&1 else (e.read(e.symbols['gBattlePartyCurrentOrder']+i//2,1)>>4) for i in range(count)]
 if target_species:
  from test_shadow_runtime import monfield
  # The Bag's party menu uses the current party array after battle switches.
  target=next(i for i in range(count) if monfield(e,i,0,0)&65535==target_species)
 else:target=order.index(current)
 for _ in range(12):
  cur=e.read(e.symbols['gPartyMenu']+9,1)
  if cur==target:break
  e.press('LEFT' if target==0 else 'RIGHT' if cur==0 else 'DOWN' if cur<target else 'UP',60)
 assert cur==target
 e.press('A',180)
 for _ in range(20):
  if not e.task_active('Task_HandleChooseMonInput'):break
  e.press('A',60)
 if count_pocket(e,item,0x310,42)!=before-1:
  print('Item menu context:',item,'target',target,'original',current,'order',order,'cursor',e.read(e.symbols['gPartyMenu']+9,1),flush=True)
  e.screenshot(ROOT/'test-output/natural-item-failure.png');e.state(ROOT/'test-output/natural-item-failure.state')
 assert count_pocket(e,item,0x310,42)==before-1
 print('Native battle healing item spent:',item,flush=True)


def natural_battle(e,limit=1800,learn_moves=(),healing_item=0,healing_limit=0,revive_species=0):
 action=first_symbol('HandleInputChooseAction');move=first_symbol('HandleInputChooseMove');turns=0;heals=0;revived=False
 for _ in range(limit):
  if not e.in_battle():break
  fn=e.read('gBattlerControllerFuncs')&~1
  if learn_moves and e.task_active('Task_InputHandler_SelectOrForgetMove'):
   # Normal move-forgetting UI: replace the first move, keeping useful coverage.
   for _ in range(6):
    if e.read('sMoveSelectionCursorPos',1)==0:break
    e.press('DOWN',60)
   assert e.read('sMoveSelectionCursorPos',1)==0
   e.press('A',900);continue
  if e.task_active('Task_HandleChooseMonInput'):
   count=e.read('gPlayerPartyCount',1);current=e.read('gBattlerPartyIndexes',2)
   order=[(e.read(e.symbols['gBattlePartyCurrentOrder']+i//2,1)&15) if i&1 else (e.read(e.symbols['gBattlePartyCurrentOrder']+i//2,1)>>4) for i in range(count)]
   active=next((i for i,x in enumerate(order) if x==current),0)
   living=[i for i in range(count) if e.read(e.symbols['gPlayerParty']+100*i+86,2)]
   if active in living:
    # Generic dialogue confirmation can accept an optional opponent switch.
    e.press('B',180);continue
   assert living,'no living partner available'
   target=living[0]
   for _ in range(8):
    cur=e.read(e.symbols['gPartyMenu']+9,1)
    if cur==target:break
    e.press('LEFT' if target==0 else 'RIGHT' if cur==0 else 'DOWN' if cur<target else 'UP',60)
   e.press('A',180);e.press('A',180);e.frames(300);continue
  if revive_species and not revived and fn in (action,move):
   from test_shadow_runtime import monfield
   from test_oxford_gym import count_pocket
   target=next(i for i in range(e.read('gPlayerPartyCount',1)) if monfield(e,i,0,0)&65535==revive_species)
   if e.read(e.symbols['gPlayerParty']+100*target+86,2)==0 and count_pocket(e,24,0x310,42):
    if fn==move:e.press('B',30)
    use_battle_heal(e,24,revive_species);revived=True;continue
  if fn==action:
   hp=e.read(e.symbols['gBattleMons']+40,2);maxhp=e.read(e.symbols['gBattleMons']+44,2)
   if healing_item and heals<healing_limit and 0<hp*3<maxhp*2:
    use_battle_heal(e,healing_item);heals+=1;continue
   e.press('UP',2);e.press('LEFT',2);e.press('A',30)
  elif fn==move:
   hp=e.read(e.symbols['gBattleMons']+40,2);maxhp=e.read(e.symbols['gBattleMons']+44,2)
   if healing_item and heals<healing_limit and 0<hp*3<maxhp*2:
    # Dialogue confirmation can advance directly into move selection.
    e.press('B',30);use_battle_heal(e,healing_item);heals+=1;continue
   slot=max(range(4),key=lambda x:move_score(e,x));e.press('UP',2);e.press('LEFT',2)
   if slot&1:e.press('RIGHT',2)
   if slot&2:e.press('DOWN',2)
   e.press('A',30);turns+=1
  else:
   # Learn only explicitly selected moves through the native prompt.
   learning=e.read(e.read('gBattlescriptCurrInstr'),1)==0x5a
   accept=e.read('gMoveToLearn',2) in learn_moves
   e.press('B' if learning and not accept else 'A',30)
 else:
  e.screenshot(ROOT/'test-output/natural-stalled.png');e.state(ROOT/'test-output/natural-stalled.state')
  instr=e.read('gBattlescriptCurrInstr');fn=e.read('gBattlerControllerFuncs')&~1
  nearby=[(k,hex(v)) for k,v in e.symbols.items() if abs((v&~1)-fn)<4]
  raise AssertionError(('natural battle stalled',hex(fn),nearby,hex(instr),e.read(instr,1),turns))
 outcome=e.read('gBattleOutcome',1)
 e.finish_dialogue();e.frames(240)
 return outcome,turns

def natural_trainer_battle(e,target):
 """Handle late grass transitions before talking to a route trainer."""
 for _ in range(8):
  try:
   battle_start(e,target)
   return natural_battle(e)
  except AssertionError:
   if not e.in_battle():raise
   trainer=bool(e.read('gBattleTypeFlags')&8)
   outcome,turns=natural_battle(e)
   if trainer:return outcome,turns
   assert outcome in (1,4,5,7),('approach encounter',outcome)
 raise AssertionError('too many encounters before trainer conversation')


def natural_go(e,target):
 """Walk normally and battle incidental encounters without field-state edits."""
 for _ in range(30):
  try:
   go(e,target);e.frames(90)
   if e.in_battle():
    result,turns=natural_battle(e);assert result in (1,4,5,7)
    continue
   return
  except AssertionError:
   # Grass encounters can interrupt movement before the battle flag is set.
   e.frames(180)
   if not e.in_battle():raise
   result,turns=natural_battle(e)
   assert result in (1,4,5,7),('route encounter',result)
 raise AssertionError('too many route encounters')

def main():
 results=[];e=Emulator(ROOT/'pokefirered.gba')
 assert e.read(e.symbols['gBattleMoves']+12*33+1,1)==35 and e.read(e.symbols['gBattleMoves']+12*10+1,1)==40,'move table stride'
 try:
  for country in ('england','france','germany'):
   city={'england':'London','france':'Paris','germany':'Berlin'}[country]
   m=json.loads((ROOT/f'data/maps/Europe{city}/map.json').read_text());o=next(o for o in m['object_events'] if o['script']=='Shadow_Entrance')
   for i in range(3):
    e.state(ROOT/f'test-output/start-{country}-{i}.state',True);talk(e,(o['x'],o['y']+1));battle_start(e,(6,4));outcome,turns=natural_battle(e)
    row={'country':country,'starter':i,'outcome':outcome,'turns':turns,'stage':e.var(0x408C),'level':e.read(e.symbols['gPlayerParty']+84,1)};results.append(row)
    if outcome==1:e.state(ROOT/f'test-output/natural-win-{country}-{i}.state')
    e.screenshot(ROOT/f'test-output/natural-{country}-{i}.png');print(row,flush=True)
  (ROOT/'test-output/natural-opening.json').write_text(json.dumps(results,indent=2)+'\n')
 finally:e.close()
if __name__=='__main__':main()
