"""Read-only battle automation: normal inputs, original stats/HP/PP and native AI.

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

def natural_battle(e,limit=1800):
 action=first_symbol('HandleInputChooseAction');move=first_symbol('HandleInputChooseMove');turns=0
 for _ in range(limit):
  if not e.in_battle():break
  fn=e.read('gBattlerControllerFuncs')&~1
  if fn==action:
   e.press('UP',2);e.press('LEFT',2);e.press('A',30)
  elif fn==move:
   slot=max(range(4),key=lambda x:move_score(e,x));e.press('UP',2);e.press('LEFT',2)
   if slot&1:e.press('RIGHT',2)
   if slot&2:e.press('DOWN',2)
   e.press('A',30);turns+=1
  else:
   # Decline optional switches and move replacement; allow ordinary evolutions.
   e.press('B' if e.read(e.read('gBattlescriptCurrInstr'),1)==0x5a else 'A',30)
 else:
  e.screenshot(ROOT/'test-output/natural-stalled.png');raise AssertionError('natural battle stalled')
 outcome=e.read('gBattleOutcome',1)
 e.finish_dialogue();e.frames(240)
 return outcome,turns

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
