"""Earned-party League progression using native controls and cold saves."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from natural_team_test_helpers import lead
from natural_preparation_test_helpers import teach,give
from natural_supplies_test_helpers import buy
from test_navigation import wait_task
from test_eclipse_natural_past import palette
import sys

def party_record(e):
 return tuple((monfield(e,i,0,0),monfield(e,i,0,4),monfield(e,i,3,8),
               tuple(monfield(e,i,1,j)&65535 for j in (0,2,4,6)),
               e.read(e.symbols['gPlayerParty']+100*i+84,1),
               e.read(e.symbols['gPlayerParty']+100*i+86,2))
              for i in range(e.read('gPlayerPartyCount',1)))

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  start=int(next((x.split('=')[1] for x in sys.argv if x.startswith('--stage=')),16))
  load_checkpoint(e,f'natural-league-{start-1}-complete' if start>16 else 'natural-prepared-league' if '--resume' in sys.argv else 'natural-league-training' if '--train' in sys.argv else 'natural-geneva-complete',True)
  assert e.var(0x408C)==start and e.var(0x4090)==0 and e.var(0x4091)==0
  if '--resume' not in sys.argv and start==16:
   if '--train' not in sys.argv:
    teach(e,26,322,351,0);give(e,26,182)
    save(e,'natural-league-training')
   for practice in range(80):
    index=next(i for i in range(6) if monfield(e,i,0,0)&65535==26)
    level=e.read(e.symbols['gPlayerParty']+100*index+84,1)
    if level>=45:break
    talk(e,(2,4));talk(e,(10,7));result,turns=natural.natural_trainer_battle(e,(7,7))
    assert result==1
    talk(e,(15,20))
    level=e.read(e.symbols['gPlayerParty']+100*index+84,1)
    print('League shared training:',practice+1,'Raichu level',level,flush=True)
    if practice%5==4:save(e,'natural-league-training')
   assert level>=45
   talk(e,(2,4));talk(e,(6,7),'YES');talk(e,(10,16),'YES')
   assert e.location()[:2]==(44,32) and e.var(0x408C)==16
   buy(e,((21,10,1200),(24,3,1500)));talk(e,(2,4));save(e,'natural-prepared-league')
  for i in range(6):
   p=e.symbols['gPlayerParty']+100*i
   print('Earned partner:',monfield(e,i,0,0)&65535,e.read(p+84,1),'moves',[monfield(e,i,1,j)&65535 for j in (0,2,4,6)],flush=True)
  for stage in range(start,21):
   if e.location()[:2]!=(44,stage*2):talk(e,(10,4))
   assert e.location()[:2]==(44,stage*2)
   talk(e,(2,4))
   opener={16:26,17:31,18:229,19:131,20:26}[stage]
   index=next(i for i in range(6) if monfield(e,i,0,0)&65535==opener)
   if index:lead(e,index)
   before_palette=palette(e);battle_start(e,(6,4))
   result,turns=natural.natural_battle(e,healing_item=21,healing_limit=count_pocket(e,21,0x310,42),matchups={87:26,131:26,91:26,124:229,62:26,94:229,200:229,97:229,65:229,148:131,230:131,130:26,149:131,18:26,135:31,59:31,214:31},fallback_species=31,finish_low_enemy=True,trace=True,finish=stage!=20)
   print('League stage:',stage,'result',result,'attack selections',turns,flush=True)
   assert result==1
   if stage==20:
    for _ in range(50):
     if e.task_active('Task_EuropeMap'):break
     e.press('A',90)
    wait_task(e,'Task_EuropeMap')
    for page in range(3):
     e.screenshot(ROOT/f'test-output/eclipse-natural-ending-{page}.png')
     if page<2:e.press('A',90)
    e.press('B',240);e.finish_dialogue()
    n=0x82c;assert e.read(e.read('gSaveBlock1Ptr')+0xee0+n//8,1)&(1<<(n%8))
   assert e.var(0x408C)==stage+1
   talk(e,(2,4));name=f'natural-league-{stage}-complete';save(e,name)
   saved_party=party_record(e)
   e.screenshot(ROOT/f'test-output/eclipse-natural-league-{stage}.png')
   e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,name,True)
   assert e.var(0x408C)==stage+1 and e.read('gPlayerPartyCount',1)==6 and palette(e)==before_palette and party_record(e)==saved_party
   print('PASS: League chapter and earned party survive cold Continue:',stage,flush=True)
 finally:e.close()
if __name__=='__main__':main()
