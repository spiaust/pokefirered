from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk
from test_continent_runtime import battle_start
from test_landmark_cases import save

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-prague-complete',True)
  assert e.var(0x408C)==7 and e.var(0x4090)==0
  talk(e,(10,4));assert e.location()[:2]==(44,14)
  talk(e,(2,4));battle_start(e,(6,4))
  result,turns=natural.natural_battle(e)
  print('Natural Vienna gym:',result,turns,'selections; stage',e.var(0x408C),flush=True)
  if result==1:
   assert e.var(0x408C)==8
   talk(e,(2,4));save(e,'natural-sixth-badge')
   e.screenshot(ROOT/'test-output/eclipse-natural-vienna.png')
   e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-sixth-badge',True)
   assert e.var(0x408C)==8
   print('PASS: natural sixth badge and cold Continue.',flush=True)
  else:
   assert result==2 and e.var(0x408C)==7
   print('Training required before Vienna; Prague checkpoint preserved.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
