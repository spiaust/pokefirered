"""Earn champion circuit victories with native battles and saved progression."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from test_eclipse_circuit import shelter,D,check_team
from test_eclipse_natural_league import party_record
from test_eclipse_legendaries import flag
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from natural_team_test_helpers import lead
from natural_supplies_test_helpers import buy
from test_trainers import money
from natural_preparation_test_helpers import teach
from test_eclipse_natural_mewtwo_unlock import deposit
from natural_capture_test_helpers import boxed_records
from test_navigation import wait_task
from test_country import wait_menu
import sys


def withdraw_mewtwo(e):
 records=boxed_records(e,150);assert len(records)==1
 storage=e.read('gPokemonStoragePtr')+4
 slot=next(i for i in range(30) if e.read(storage+80*i)==records[0][0] and e.read(storage+80*i+4)==records[0][1])
 natural.natural_go(e,(3,6));e.press('UP');e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.press('A',180)
 wait_task(e,'Task_PCMainMenu');e.frames(90);e.press('A',240)
 wait_task(e,'Task_PokeStorageMain');e.frames(120)
 for _ in range(slot%6):e.press('RIGHT',30)
 for _ in range(slot//6):e.press('DOWN',30)
 assert e.read('sCursorPosition',1)==slot
 e.press('A',120);e.press('A',240);e.frames(180)
 for _ in range(16):
  if e.task_active('Task_PCMainMenu'):break
  e.press('B',120);e.press('A',120)
 wait_task(e,'Task_PCMainMenu');e.press('B',180);e.finish_dialogue();e.frames(180)
 assert e.read('gPlayerPartyCount',1)==6 and any(monfield(e,i,0,0)&65535==150 for i in range(6))
 assert not boxed_records(e,150)
 print('PASS: earned Mewtwo withdrawn through native PC.',flush=True)

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  after=int(next((x.split('=')[1] for x in sys.argv if x.startswith('--after=')),0))
  stop=int(next((x.split('=')[1] for x in sys.argv if x.startswith('--stop=')),13))
  kit='--kit' in sys.argv;legend='--legend' in sys.argv;ready='--ready' in sys.argv
  checkpoint=next((x.split('=',1)[1] for x in sys.argv if x.startswith('--checkpoint=')),None)
  restored='--full-restores' in sys.argv
  load_checkpoint(e,checkpoint if checkpoint else f'natural-circuit-{after}-complete' if after else 'natural-circuit-kit-trained' if ready else 'natural-circuit-prepared' if kit else 'natural-caught-mewtwo' if legend else 'natural-krakow-complete',True)
  assert e.var(0x408C)==21 and e.var(0x4090)==0 and e.var(0x4091)==0
  if not after and not kit and not ready:
   if not legend:talk(e,(15,29),'YES')
   talk(e,(43,31),'YES');talk(e,(10,16),'YES')
   if legend:
    deposit(e,179);withdraw_mewtwo(e)
   buy(e,((21,10,1200),(24,5,1500)) if legend else ((21,35,1200),(24,10,1500),(19,5,3000)))
   talk(e,(5,6),'NO');assert e.var(0x40BF)==0
   talk(e,(5,6),'YES');assert e.var(0x40BF)==1
   save(e,'natural-circuit-prepared')
  if not after and not ready:
   if kit:talk(e,(5,6))
   assert all(flag(e,n) for n in (0x8DE,0x8DF,0x8E0))
   before=tuple(count_pocket(e,n,0x464,58) for n in (341,312,323))
   assert before==(1,1,1)
   talk(e,(5,6));assert tuple(count_pocket(e,n,0x464,58) for n in (341,312,323))==before
   teach(e,131,341,57,0,reusable=True)
   has_mewtwo=any(monfield(e,j,0,0)&65535==150 for j in range(6))
   if not has_mewtwo:teach(e,159,341,57,2,reusable=True)
   teach(e,150 if has_mewtwo else 26,312,85,2 if has_mewtwo else 0)
   teach(e,229,323,53,1)
   save(e,'natural-circuit-kit-trained')
  for i,row in enumerate(D['trainers'][:stop]):
   if i<after:continue
   shelter(e,row['map']);talk(e,(2,4))
   if count_pocket(e,21,0x310,42)<10 and money(e)>=12000:buy(e,((21,10,1200),))
   if count_pocket(e,23,0x310,42)<5 and money(e)>=6000:buy(e,((23,10,600),))
   if restored and count_pocket(e,19,0x310,42)<6 and money(e)>=3000:buy(e,((19,min(6,money(e)//3000),3000),))
   has_mewtwo=any(monfield(e,j,0,0)&65535==150 for j in range(6))
   opener=150 if has_mewtwo else 26 if i==1 else 131 if i==0 else 31
   index=next(j for j in range(6) if monfield(e,j,0,0)&65535==opener)
   if index:lead(e,index)
   talk(e,(6,4),'NO');assert e.var(0x40BF)==i+1 and not e.in_battle()
   supplies=tuple(count_pocket(e,item,0x310,42) for item in (21,24,19,23))
   battle_start(e,(6,4));check_team(e,row,0)
   result,turns=natural.natural_battle(e,limit=7000,status_item=23,healing_item=(19,21) if restored else 21,healing_limit=sum(count_pocket(e,n,0x310,42) for n in ((19,21) if restored else (21,))),revive_species=31 if restored and i==10 else 150 if has_mewtwo else 31,matchups={94:150,376:31,229:31,197:31,103:229,297:150,3:150,76:150,139:150,141:150,142:150,248:150,62:150,131:150,121:150,230:150,350:150} if has_mewtwo else {76:131,139:26,141:31,142:26,248:31,62:26,131:26,121:26,230:31,350:26},fallback_species=150 if has_mewtwo else 31,finish_low_enemy=not restored,trace=True)
   spent=tuple(before-count_pocket(e,item,0x310,42) for item,before in zip((21,24,19,23),supplies))
   print('Natural circuit:',row['name'],result,turns,'attack selections; Hyper/Revive/FullRestore/FullHeal',spent,flush=True)
   if result!=1:
    save(e,f'natural-circuit-{i+1}-loss');assert e.var(0x40BF)==i+1
    raise AssertionError(('earned circuit needs preparation',row['name'],result))
   assert e.var(0x40BF)==i+2 and e.var(0x408C)==21
   talk(e,(2,4));name=f'natural-circuit-{i+1}-complete';save(e,name);record=party_record(e)
   e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,name,True)
   assert e.var(0x40BF)==i+2 and party_record(e)==record
   print('PASS: earned circuit victory and exact party survive cold Continue.',flush=True)
  if stop==13:
   before=count_pocket(e,1,0x430,13);talk(e,(5,6))
   assert flag(e,0x8DD) and e.var(0x40BF)==15 and count_pocket(e,1,0x430,13)==before+1
   talk(e,(5,6),'NO');assert count_pocket(e,1,0x430,13)==before+1 and e.var(0x40BF)==15
   save(e,'natural-circuit-complete')
   e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-circuit-complete',True)
   assert flag(e,0x8DD) and e.var(0x40BF)==15 and count_pocket(e,1,0x430,13)==before+1
   print('PASS: earned thirteen-match circuit and unique Master Ball persist after cold Continue.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
