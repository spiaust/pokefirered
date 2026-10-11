"""Finish the Nordic remnant hunt using earned partners and native battles."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import world,battle_start
from test_eclipse_nordic import target,flag,D
from test_eclipse_natural_league import party_record
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from natural_team_test_helpers import lead
from natural_supplies_test_helpers import buy
import sys

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  resume=int(next((x.split('=')[1] for x in sys.argv if x.startswith('--after=')),0))
  load_checkpoint(e,f'natural-nordic-{resume}-complete' if resume else 'natural-league-20-complete',True)
  assert e.var(0x408C)==21 and e.var(0x4090)==0 and e.var(0x4091)==0
  if not resume:
   buy(e,((21,20,1200),(24,10,1500),(19,5,3000)))
   world(e,15);talk(e,target('Copenhagen','Ada'),'NO');assert e.var(0x40BD)==0
   talk(e,target('Copenhagen','Ada'),'YES');assert e.var(0x40BD)==1
  for i,row in enumerate(D['trainers']):
   if i<resume:continue
   world(e,15+i);talk(e,(12,31))
   index=next(j for j in range(6) if monfield(e,j,0,0)&65535==31)
   if index:lead(e,index)
   pos=target(D['route'][i],row['name'].title())
   talk(e,pos,'NO');assert e.var(0x40BD)==i+1 and not e.in_battle()
   supplies=tuple(count_pocket(e,item,0x310,42) for item in (21,24,19))
   battle_start(e,pos)
   result,turns=natural.natural_battle(e,healing_item=21,healing_limit=count_pocket(e,21,0x310,42),revive_species=31,matchups={169:26,101:31,89:31,82:31,229:31,110:31,197:31,248:31},fallback_species=31,trace=True)
   spent=tuple(before-count_pocket(e,item,0x310,42) for item,before in zip((21,24,19),supplies))
   print('Native Hyper Potion/Revive/Full Restore costs:',spent,flush=True)
   print('Natural Nordic battle:',row['name'],result,turns,'attack selections',flush=True)
   assert result==1 and e.var(0x40BD)==i+2 and e.var(0x408C)==21
   talk(e,(12,31));name=f'natural-nordic-{i+1}-complete';save(e,name);record=party_record(e)
   e.screenshot(ROOT/f'test-output/{name}.png')
   e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,name,True)
   assert e.var(0x40BD)==i+2 and party_record(e)==record
   print('PASS: earned Nordic victory and exact party persist after cold Continue.',flush=True)
  world(e,15);before=count_pocket(e,318,0x464,58);talk(e,target('Copenhagen','Ada'))
  assert e.var(0x40BD)==5 and flag(e) and count_pocket(e,318,0x464,58)==before+1
  talk(e,target('Copenhagen','Ada'));assert count_pocket(e,318,0x464,58)==before+1
  save(e,'natural-nordic-complete');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-nordic-complete',True)
  assert e.var(0x40BD)==5 and flag(e) and count_pocket(e,318,0x464,58)==before+1
  print('PASS: earned remnant hunt and unique Shadow Ball reward survive cold Continue.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
