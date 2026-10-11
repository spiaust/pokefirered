"""Native postgame hunt with explicit victory and bag-capacity fixtures.

This verifies quest/team rules and persistence; it does not assert combat balance.
"""
import json,re
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import talk,go,monfield,setstage
from test_continent_runtime import world,var,battle_start
from test_landmark_cases import save
from test_eclipse_natural import first_symbol
from test_oxford_gym import count_pocket
D=json.loads((ROOT/'data/eclipse-postgame.json').read_text())['nordic_hunt']


def target(tag,label):
 m=json.loads((ROOT/f'data/maps/Continent{tag}/map.json').read_text())
 o=next(o for o in m['object_events'] if o['script']=='EclipseNordic_'+label)
 return o['x'],o['y']+1


def flag(e):return bool(e.read(e.read('gSaveBlock1Ptr')+0xee0+0x8d5//8,1)&(1<<(0x8d5%8)))


def win(e):
 action=first_symbol('HandleInputChooseAction');move=first_symbol('HandleInputChooseMove')
 for _ in range(1500):
  if not e.in_battle():break
  if e.read('gBattlerControllerFuncs')&~1 in (action,move):
   b=e.symbols['gBattleMons']
   for off in (4,6,10):e.write(b+off,30000,2)
   e.write(b+40,30000,2);e.write(b+44,30000,2);e.write(b+88+40,1,2)
   e.write(b+12,82,2);e.write(b+36,40,1);e.press('UP',2);e.press('LEFT',2)
  e.press('B' if e.read(e.read('gBattlescriptCurrInstr'),1)==0x5a else 'A',30)
 assert not e.in_battle() and e.read('gBattleOutcome',1)==1
 e.finish_dialogue();e.frames(240)


def main():
 moves={a:int(b) for a,b in re.findall(r'#define (MOVE_\w+)\s+(\d+)',(ROOT/'include/constants/moves.h').read_text())}
 items={a:int(b) for a,b in re.findall(r'#define (ITEM_\w+)\s+(\d+)',(ROOT/'include/constants/items.h').read_text())}
 source=(ROOT/'src/data/trainer_parties.h').read_text()
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-finished',True);e.write('sWildEncountersDisabled',1,1)
  world(e,15);ada=target('Copenhagen','Ada');setstage(e,20);talk(e,ada);assert e.var(0x40bd)==0
  setstage(e,21);talk(e,ada,'NO');assert e.var(0x40bd)==0
  world(e,16);talk(e,target('Oslo','Rime'));assert not e.in_battle() and e.var(0x40bd)==0
  world(e,15);talk(e,ada,'YES');assert e.var(0x40bd)==1
  for i,row in enumerate(D['trainers']):
   tag=D['route'][i];world(e,[15,16,17][i]);pos=target(tag,row['name'].title())
   talk(e,pos,'NO');assert e.var(0x40bd)==i+1 and not e.in_battle()
   state=ROOT/f"test-output/nordic-pre-{row['id']}.state";e.state(state)
   party=re.search(r'EclipseRemnantParty'+str(row['id'])+r'\[\] = \{(.*?)\n\};',source,re.S)[1]
   expected=[([moves[x] for x in re.findall(r'MOVE_\w+',m)],items[item]) for item,m in re.findall(r'\.heldItem = (ITEM_\w+), \.moves = \{([^}]+)\}',party)]
   for mode,delta in [(1,-4),(2,5),(0,0)]:
    e.state(state,True);var(e,0x4090,mode);battle_start(e,pos)
    for j,(want,item) in enumerate(expected):
     assert e.read(e.symbols['gEnemyParty']+100*j+84,1)==row['level']+delta
     actual=[monfield(e,j,1,k,'gEnemyParty')&0xffff for k in (0,2,4,6)]
     assert actual==want,(row['name'],mode,j,actual,want)
     assert monfield(e,j,0,2,'gEnemyParty')&0xffff==item and monfield(e,j,3,8,'gEnemyParty')&(1<<27)
    e.screenshot(ROOT/f"test-output/eclipse-nordic-{row['name'].lower()}.png")
    win(e);assert e.var(0x40bd)==i+2 and e.var(0x408c)==21
   talk(e,pos);assert not e.in_battle() and e.var(0x40bd)==i+2
   print('PASS:',row['name'],'all difficulty levels, curated moves/items, shadow teams and native victory gate.',flush=True)
  world(e,15);state=ROOT/'test-output/nordic-reward-ready.state';e.state(state)
  pocket=e.read('gSaveBlock1Ptr')+0x464;slot=next(i for i in range(58) if e.read(pocket+4*i,2) in (0,318));key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
  e.write(pocket+4*slot,318,2);e.write(pocket+4*slot+2,999^key,2)
  talk(e,ada);assert not flag(e) and e.var(0x40bd)==4 and count_pocket(e,318,0x464,58)==999
  e.state(state,True);before=count_pocket(e,318,0x464,58);talk(e,ada)
  assert flag(e) and e.var(0x40bd)==5 and count_pocket(e,318,0x464,58)==before+1
  talk(e,ada);assert count_pocket(e,318,0x464,58)==before+1
  save(e,'eclipse-nordic-complete');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'eclipse-nordic-complete',True)
  assert flag(e) and e.var(0x40bd)==5 and e.var(0x408c)==21 and count_pocket(e,318,0x464,58)==before+1
  talk(e,ada);assert count_pocket(e,318,0x464,58)==before+1
  print('PASS: pre-League/start/order/decline gates, bag-full retry, unique Shadow Ball reward and cold persistence.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
