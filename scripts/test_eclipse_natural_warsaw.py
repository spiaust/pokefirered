"""Add a purified Dark partner and play Warsaw through native training and menus."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from natural_team_test_helpers import lead
from natural_supplies_test_helpers import buy
from test_eclipse_natural_past import palette
import sys

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  resume='--resume' in sys.argv;probe='--probe' in sys.argv
  load_checkpoint(e,'natural-trained-warsaw' if resume else 'natural-paris1940-complete',True)
  assert e.var(0x408C)==13 and e.var(0x4090)==0 and e.var(0x4091)==0
  if probe:
   talk(e,(10,4));talk(e,(2,4));battle_start(e,(6,4))
   result,turns=natural.natural_battle(e,healing_item=21,healing_limit=count_pocket(e,21,0x310,42))
   print('Warsaw baseline:',result,turns,'selections; stage',e.var(0x408C),flush=True)
   return
  if not resume:
   assert e.read('gPlayerPartyCount',1)==4 and not e.var(0x408E)&2
   for mapnum in (22,20,18,16,14,12):
    talk(e,(2,7));assert e.location()[:2]==(44,mapnum)
   purified=e.var(0x408F);talk(e,(8,4))
   assert e.read('gPlayerPartyCount',1)==5 and monfield(e,4,0,0)&65535==228 and monfield(e,4,3,8)&(1<<27)
   for _ in range(13):talk(e,(4,4))
   assert e.var(0x408F)==purified+1 and not monfield(e,4,3,8)&(1<<27)
   lead(e,4);talk(e,(10,4));assert e.location()[:2]==(44,14)
   for practice in range(15):
    if monfield(e,0,0,0)&65535==229:break
    talk(e,(2,4));talk(e,(10,7));result,turns=natural.natural_trainer_battle(e,(7,7))
    assert result==1
    talk(e,(15,20))
    print('Dark-partner Vienna preparation:',practice+1,'species',monfield(e,0,0,0)&65535,'level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
   assert monfield(e,0,0,0)&65535==229 and not monfield(e,0,3,8)&(1<<27)
   talk(e,(2,4));talk(e,(6,7),'YES');assert e.location()[:2]==(43,0)
   talk(e,(10,16),'YES');assert e.location()[:2]==(44,26) and e.var(0x408C)==13
   buy(e,((21,3,1200),(24,1,1500)));talk(e,(2,4));save(e,'natural-trained-warsaw')
  before_palette=palette(e);battle_start(e,(6,4))
  result,turns=natural.natural_battle(e,healing_item=21,healing_limit=count_pocket(e,21,0x310,42),revive_species=31,trace=True)
  print('Warsaw prepared battle:',result,turns,'selections',flush=True)
  assert result==1 and e.var(0x408C)==14
  talk(e,(2,4));save(e,'natural-warsaw1943-complete');e.screenshot(ROOT/'test-output/eclipse-natural-warsaw1943.png')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-warsaw1943-complete',True)
  assert e.var(0x408C)==14 and e.read('gPlayerPartyCount',1)==5 and palette(e)==before_palette
  assert e.var(0x408E)&2 and e.var(0x408F)==2
  assert any(monfield(e,i,0,0)&65535==229 and not monfield(e,i,3,8)&(1<<27) for i in range(5))
  print('PASS: native rescue, purification, Houndoom evolution, Warsaw victory and cold Continue.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
