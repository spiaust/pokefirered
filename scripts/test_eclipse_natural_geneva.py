"""Purify the earned Lapras rescue and defeat Veil with native matchup switches."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from natural_supplies_test_helpers import buy
from natural_team_test_helpers import lead
from test_eclipse_natural_past import palette
import sys

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  resume='--resume' in sys.argv or '--train' in sys.argv
  load_checkpoint(e,'natural-prepared-geneva' if resume else 'natural-geneva-ready',True)
  assert e.var(0x408C)==15 and e.var(0x4090)==0 and e.var(0x4091)==0
  if not resume:
   assert e.read('gPlayerPartyCount',1)==5 and not e.var(0x408E)&16
   talk(e,(2,7));assert e.location()[:2]==(44,28)
   talk(e,(2,7));assert e.location()[:2]==(44,26)
   purified=e.var(0x408F);talk(e,(8,4))
   assert e.read('gPlayerPartyCount',1)==6 and monfield(e,5,0,0)&65535==131 and monfield(e,5,3,8)&(1<<27)
   for _ in range(13):talk(e,(4,4))
   assert e.var(0x408F)==purified+1 and not monfield(e,5,3,8)&(1<<27)
   assert 58 in [monfield(e,5,1,j)&65535 for j in (0,2,4,6)]
   talk(e,(10,4));talk(e,(10,4));assert e.location()[:2]==(44,30)
   buy(e,((21,5,1200),(24,1,1500)));talk(e,(2,4));save(e,'natural-prepared-geneva')
  if not resume or '--train' in sys.argv:
   index=next(i for i in range(6) if monfield(e,i,0,0)&65535==229)
   if index:lead(e,index)
   for mapnum in (28,26,24,22,20,18,16,14):
    talk(e,(2,7));assert e.location()[:2]==(44,mapnum)
   for practice in range(50):
    if e.read(e.symbols['gPlayerParty']+84,1)>=40:break
    talk(e,(2,4));talk(e,(10,7));result,turns=natural.natural_trainer_battle(e,(7,7))
    assert result==1
    talk(e,(15,20))
    print('Geneva Dark-partner training:',practice+1,'level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
   assert e.read(e.symbols['gPlayerParty']+84,1)>=40
   talk(e,(2,4));talk(e,(6,7),'YES');talk(e,(10,16),'YES')
   assert e.location()[:2]==(44,30) and e.var(0x408C)==15
   index=next(i for i in range(6) if monfield(e,i,0,0)&65535==31)
   if index:lead(e,index)
   save(e,'natural-prepared-geneva')
  before_palette=palette(e);battle_start(e,(6,4))
  result,turns=natural.natural_battle(e,healing_item=21,healing_limit=count_pocket(e,21,0x310,42),matchups={82:31,248:31,229:31,94:229,149:131},fallback_species=31,finish_low_enemy=True,trace=True)
  print('Geneva final Veil battle:',result,turns,'attack selections',flush=True)
  assert result==1 and e.var(0x408C)==16
  talk(e,(2,4));save(e,'natural-geneva-complete');e.screenshot(ROOT/'test-output/eclipse-natural-geneva.png')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-geneva-complete',True)
  assert e.var(0x408C)==16 and e.read('gPlayerPartyCount',1)==6 and palette(e)==before_palette
  assert e.var(0x408E)&16 and e.var(0x408F)==3
  assert any(monfield(e,i,0,0)&65535==131 and not monfield(e,i,3,8)&(1<<27) for i in range(6))
  print('PASS: native Lapras rescue and purification, final Veil victory and cold Continue.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
