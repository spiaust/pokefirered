"""Earn guardian captures using native controls and purchased Ultra/Timer Balls."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import world,battle_start
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from natural_team_test_helpers import lead
from natural_supplies_test_helpers import buy
from natural_capture_test_helpers import capture,boxed,boxed_records
from test_eclipse_legendaries import D,flag,SPECIES
from test_trainers import money
import sys

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  post='--post' in sys.argv;timer='--timer' in sys.argv
  preparation='natural-prepared-timer-legendaries' if timer else 'natural-prepared-post-legendaries' if post else 'natural-prepared-legendaries'
  guardian=next((x.split('=')[1].upper() for x in sys.argv if x.startswith('--guardian=')),None)
  assert not guardian or post and guardian in {r['species'] for r in D[3:]}
  expected_stage=21 if post else 16
  after=next((x.split('=')[1] for x in sys.argv if x.startswith('--after=')),None)
  load_checkpoint(e,'natural-caught-'+after if after else preparation if '--resume' in sys.argv else 'natural-league-20-complete' if post else 'natural-prepared-league',True)
  assert e.var(0x408C)==expected_stage and e.var(0x4090)==0 and e.var(0x4091)==0
  print('Earned legendary budget:',money(e),flush=True)
  if '--resume' not in sys.argv and not after:
   orders=((2,45,1200),(10,45,1000),(21,15,1200),(19,5,3000)) if timer else ((2,90,1200),(21,15,1200),(19,5,3000))
   buy(e,orders);save(e,preparation)
  for row in ([r for r in D if r['species']==guardian] if guardian else D[3:4] if post else D[:3]):
   if flag(e,int(row['flag'],16)):continue
   world(e,row['country_index']);talk(e,(12,31))
   index=next(i for i in range(6) if monfield(e,i,0,0)&65535==26)
   if index:lead(e,index)
   assert e.var(0x408F)>=row['min_purified']
   species=SPECIES[row['species']];before=boxed(e).count(species)
   assert not flag(e,int(row['flag'],16))
   for attempt in range(3):
    battle_start(e,(34,13));assert e.read(e.symbols['gBattleMons']+88,2)==species
    assert e.read(e.symbols['gEnemyParty']+84,1)==row['level']
    before_balls=sum(count_pocket(e,item,0x430,13) for item in (2,10))
    result,balls,heals,attacks=capture(e,fallback_species={'LUGIA':131,'HO_OH':229}.get(row['species'],31),strong_move=row['species'] in ('LUGIA','HO_OH'))
    assert sum(count_pocket(e,item,0x430,13) for item in (2,10))==before_balls-balls
    if result==7:break
    assert not flag(e,int(row['flag'],16)) and boxed(e).count(species)==before
    print('Native legendary KO leaves encounter available for retry:',row['species'],flush=True)
    talk(e,(12,31))
   assert result==7
   assert flag(e,int(row['flag'],16)) and boxed(e).count(species)==before+1
   name='natural-caught-'+row['species'].lower();save(e,name)
   caught_records=boxed_records(e,species);saved_balls=tuple(count_pocket(e,item,0x430,13) for item in (2,10))
   print('PASS: natural',row['species'],'capture:',balls,'purchased Balls',heals,'heals',attacks,'move selections',flush=True)
   e.screenshot(ROOT/f'test-output/{name}.png');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,name,True)
   assert e.var(0x408C)==expected_stage and flag(e,int(row['flag'],16)) and boxed(e).count(species)==before+1 and e.read('gPlayerPartyCount',1)==6
   assert boxed_records(e,species)==caught_records and tuple(count_pocket(e,item,0x430,13) for item in (2,10))==saved_balls
   print('PASS: caught legendary persists in native PC after cold Continue.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
