"""Earn the first badge with native Totodile stats, EXP, moves and button inputs."""
from emulator import Emulator,ROOT
import test_shadow_runtime, test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from test_eclipse_natural import natural_battle,natural_go
from test_landmark_cases import save
from test_celebi import load_checkpoint

test_shadow_runtime.go=natural_go
test_continent_runtime.go=natural_go
e=Emulator(ROOT/'pokefirered.gba')
try:
 e.state(ROOT/'test-output/start-england-2.state',True);talk(e,(10,16));assert e.var(0x4090)==0
 assert monfield(e,0,0,0)&0xffff==158,'expected Totodile'
 battle_start(e,(6,4));result,turns=natural_battle(e);assert result==1 and e.var(0x408C)==1
 talk(e,(2,4))
 # Practice through normal trainer interactions and heal between sessions.
 for practice in range(12):
  if e.read(e.symbols['gPlayerParty']+84,1)>=13:break
  talk(e,(10,7));battle_start(e,(11,11));outcome,n=natural_battle(e)
  assert outcome==1,('practice',practice,outcome)
  talk(e,(15,20));talk(e,(2,4))
  print('Natural route practice:',practice+1,'level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
 talk(e,(10,4));talk(e,(2,4));battle_start(e,(6,4));result,turns=natural_battle(e)
 print('Natural first gym:',result,turns,'turns; level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
 assert result==1 and e.var(0x408C)==2
 f=e.read('gSaveBlock1Ptr')+0xee0;assert e.read(f+0x820//8,1)&(1<<(0x820%8))
 save(e,'natural-first-badge');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-first-badge',True)
 assert e.var(0x408C)==2;e.screenshot(ROOT/'test-output/eclipse-natural-first-badge.png')
 print('PASS: Normal rival and Rock gym won without battle/stat/EXP edits; first badge and stage survive cold Continue.',flush=True)
finally:e.close()
