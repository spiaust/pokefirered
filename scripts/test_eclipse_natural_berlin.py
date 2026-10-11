"""Earn Berlin's fifth badge with the naturally caught Flying partner."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from natural_team_test_helpers import lead
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from battle_recovery_test_helpers import moves_pp
import sys
battle=natural.natural_battle


def trained_battle(e):return battle(e,learn_moves=(17,))


def main():
 natural.natural_battle=trained_battle
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  resume='--resume' in sys.argv
  load_checkpoint(e,'natural-trained-berlin' if resume else 'natural-fourth-badge',True)
  assert e.var(0x408C)==5 and e.var(0x4090)==0 and e.read('gPlayerPartyCount',1)==4
  if not resume:
   talk(e,(2,4))
   index=next(i for i in range(4) if monfield(e,i,0,0)&0xffff==17)
   if index:lead(e,index)
   talk(e,(2,7));assert e.location()[:2]==(44,6)
   for practice in range(25):
    if e.read(e.symbols['gPlayerParty']+84,1)>=27:break
    talk(e,(2,4));talk(e,(10,7));battle_start(e,(7,7));result,turns=trained_battle(e)
    assert result==1,('Grass preparation',practice,result)
    talk(e,(15,20))
    print('Flying-partner Grass preparation:',practice+1,'level',e.read(e.symbols['gPlayerParty']+84,1),'moves',moves_pp(e)[0],flush=True)
   assert 17 in moves_pp(e)[0]
   talk(e,(10,4));talk(e,(10,4));assert e.location()[:2]==(44,10)
   for practice in range(25):
    if e.read(e.symbols['gPlayerParty']+84,1)>=29:break
    talk(e,(2,4));talk(e,(10,7));battle_start(e,(7,7));result,turns=trained_battle(e)
    assert result==1,('Fighting practice',practice,result)
    talk(e,(15,20))
    print('Flying-partner Berlin practice:',practice+1,'level',e.read(e.symbols['gPlayerParty']+84,1),'moves',moves_pp(e)[0],flush=True)
   assert e.read(e.symbols['gPlayerParty']+84,1)>=29 and 17 in moves_pp(e)[0]
   talk(e,(2,4));save(e,'natural-trained-berlin')
  battle_start(e,(6,4));result,turns=trained_battle(e)
  print('Natural Berlin gym:',result,turns,'selections; level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
  assert result==1 and e.var(0x408C)==6
  assert e.read(e.read('gSaveBlock1Ptr')+0xee0+0x824//8,1)&(1<<(0x824%8))
  assert count_pocket(e,319,0x464,58)==1 and 17 in moves_pp(e)[0]
  e.screenshot(ROOT/'test-output/eclipse-natural-berlin.png');save(e,'natural-fifth-badge')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-fifth-badge',True)
  assert e.var(0x408C)==6 and monfield(e,0,0,0)&0xffff==17 and e.read('gPlayerPartyCount',1)==4
  assert count_pocket(e,319,0x464,58)==1 and 17 in moves_pp(e)[0]
  assert e.read(e.read('gSaveBlock1Ptr')+0xee0+0x824//8,1)&(1<<(0x824%8))
  print('PASS: natural fifth badge, Wing Attack learning, Brick Break reward and cold Continue.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
