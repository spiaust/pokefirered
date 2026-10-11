"""Native legendary gates/catches with explicit progress, Ball and field fixtures.

This tests encounter rules and persistence, not natural-level combat balance.
"""
import json,re
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import talk,monfield,setstage
from test_continent_runtime import world,var,battle_start
from test_navigation import wait_task
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from test_eclipse_natural import first_symbol,natural_battle
D=json.loads((ROOT/'data/eclipse-legendaries.json').read_text())['encounters']
SPECIES={'ARTICUNO':144,'ZAPDOS':145,'MOLTRES':146,'SUICUNE':245,'LUGIA':249,'HO_OH':250,'MEWTWO':150}


def flag(e,n):return bool(e.read(e.read('gSaveBlock1Ptr')+0xee0+n//8,1)&(1<<(n%8)))


def open_ball(e):
 action=first_symbol('HandleInputChooseAction')
 for _ in range(150):
  if e.read('gBattlerControllerFuncs')&~1==action:break
  e.press('A',30)
 assert e.read('gBattlerControllerFuncs')&~1==action
 e.press('UP',2);e.press('LEFT',2);e.press('RIGHT',2);e.press('A',180);wait_task(e,'Task_BagMenu_HandleInput')
 bag=e.symbols['gBagMenuState']
 for _ in range(6):
  pocket=e.read(bag+6,2)
  if pocket==2:break
  e.press('RIGHT' if pocket<2 else 'LEFT',60)
 for _ in range(20):e.press('UP',10)
 e.press('A',90);e.press('A',180)


def capture(e):
 before=count_pocket(e,1,0x430,13);open_ball(e)
 for _ in range(160):
  if not e.in_battle():break
  if e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_NamingScreen']&~1:e.press('START',30);e.press('A',120)
  else:e.press('B',60);e.press('A',60)
 assert not e.in_battle() and e.read('gBattleOutcome',1)==7
 e.finish_dialogue();e.frames(240)
 assert count_pocket(e,1,0x430,13)==before-1


def flee(e):
 # Escape-speed/survival fixture isolates the retry callback from combat balance.
 b=e.symbols['gBattleMons']
 for off in (4,6,10):e.write(b+off,30000,2)
 e.write(b+40,30000,2);e.write(b+44,30000,2)
 action=first_symbol('HandleInputChooseAction')
 for _ in range(250):
  if not e.in_battle():break
  if e.read('gBattlerControllerFuncs')&~1==action:
   e.press('UP',2);e.press('LEFT',2);e.press('DOWN',2);e.press('RIGHT',2);e.press('A',90)
  else:e.press('A',30)
 assert not e.in_battle() and e.read('gBattleOutcome',1) in (4,5)
 e.finish_dialogue();e.frames(240)


def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-finished',True)
  e.write('sWildEncountersDisabled',1,1);var(e,0x4091,0)
  p=e.read('gSaveBlock1Ptr')+0x430;key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
  e.write(p,1,2);e.write(p+2,10^key,2) # Explicit Master Ball fixture, not earned inventory.
  for row in D:
   world(e,row['country_index']);target=row['x'],row['y']+1;f=int(row['flag'],16)
   setstage(e,row['min_stage']-1);talk(e,target);assert not e.in_battle() and not flag(e,f)
   setstage(e,row['min_stage'])
   if row['min_purified']:
    var(e,0x408f,row['min_purified']-1);talk(e,target);assert not e.in_battle() and not flag(e,f)
   var(e,0x408f,6);talk(e,target,'NO');assert not e.in_battle() and not flag(e,f)
   battle_start(e,target);assert monfield(e,0,0,0,'gEnemyParty')&0xffff==SPECIES[row['species']]
   assert e.read(e.symbols['gEnemyParty']+84,1)==row['level']
   e.screenshot(ROOT/f"test-output/eclipse-legendary-{row['species'].lower()}.png")
   if row['species']=='ARTICUNO':
    flee(e);assert not flag(e,f)
    battle_start(e,target)
    e.write(e.symbols['gBattleMons']+88+40,1,2) # Explicit KO fixture.
    e.write(e.symbols['gBattleMons']+2,30000,2);e.write(e.symbols['gBattleMons']+8,30000,2)
    result,_=natural_battle(e);assert result==1 and not flag(e,f)
    battle_start(e,target)
   capture(e);assert flag(e,f)
   print('PASS:',row['species'],'story/care gates, decline, native catch, exact level and saved removal.',flush=True)
  setstage(e,21);save(e,'eclipse-seven-legendaries');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'eclipse-seven-legendaries',True)
  assert all(flag(e,int(row['flag'],16)) for row in D)
  assert count_pocket(e,1,0x430,13)==3 and e.read('gPlayerPartyCount',1)==6
  rows={int(a):tuple(map(int,b)) for a,*b in re.findall(r'SUBSTRUCT_CASE\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)',(ROOT/'src/pokemon.c').read_text())}
  boxed=set();storage=e.read('gPokemonStoragePtr')+4
  for i in range(14*30):
   p=storage+80*i;person=e.read(p);key=person^e.read(p+4)
   boxed.add((e.read(p+32+12*rows[person%24][0])^key)&0xffff)
  assert {250,150}.issubset(boxed),'full-party legendary catches did not persist in PC'
  assert {144,145,146,245,249}.issubset({monfield(e,i,0,0)&0xffff for i in range(6)})
  # Re-enter each refuge to prove the native saved hide flags prevent duplicates.
  e.write('sWildEncountersDisabled',1,1)
  for row in D:
   world(e,row['country_index']);m=json.loads((ROOT/f"data/maps/{row['map']}/map.json").read_text());lid=next(i+1 for i,o in enumerate(m['object_events']) if o['script']=='EclipseLegendary_'+row['species'])
   assert not any(e.read(e.symbols['gObjectEvents']+36*i,1)&1 and e.read(e.symbols['gObjectEvents']+36*i+8,1)==lid for i in range(16))
  print('PASS: flee/KO retry; all seven catch flags and Ball consumption survive cold Continue; no duplicate actors; overflow catches persist in PC.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
