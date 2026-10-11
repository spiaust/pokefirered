"""Native training path after the first badge; no stats or progress writes."""
from emulator import Emulator,ROOT
import sys
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk
from test_continent_runtime import battle_start
from test_eclipse_natural import natural_go,natural_battle
from test_celebi import load_checkpoint
from test_landmark_cases import save

test_shadow_runtime.go=natural_go
test_continent_runtime.go=natural_go
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'natural-trained-paris' if '--resume' in sys.argv else 'natural-first-badge',True)
 assert e.var(0x408C)==2 and e.var(0x4090)==0
 talk(e,(2,4))
 for practice in range(0 if '--resume' in sys.argv else 12):
  if e.read(e.symbols['gPlayerParty']+84,1)>=18:break
  talk(e,(10,7));battle_start(e,(11,11));result,turns=natural_battle(e)
  assert result==1,('London practice',practice,result)
  talk(e,(15,20));talk(e,(2,4))
  print('Natural London practice:',practice+1,'level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
 save(e,'natural-trained-paris')
 talk(e,(10,4));talk(e,(2,4));battle_start(e,(6,4));result,turns=natural_battle(e)
 print('Natural Paris gym:',result,turns,'turns; level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
 e.screenshot(ROOT/'test-output/eclipse-natural-paris.png')
 assert result==1 and e.var(0x408C)==3
 save(e,'natural-second-badge');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-second-badge',True)
 assert e.var(0x408C)==3
 print('PASS: second badge earned with native training and survives cold Continue.',flush=True)
finally:e.close()
