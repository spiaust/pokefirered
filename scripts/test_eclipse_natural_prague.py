"""Continue the saved campaign through Prague with native battles and saves."""
from emulator import Emulator, ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime, test_continent_runtime
from test_shadow_runtime import talk
from test_continent_runtime import battle_start
from test_landmark_cases import save

def main():
 test_shadow_runtime.go=natural.natural_go
 test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-fifth-badge',True)
  assert e.var(0x408C)==6 and e.var(0x4090)==0
  talk(e,(2,4));talk(e,(10,4))
  assert e.location()[:2]==(44,12)
  talk(e,(2,4));battle_start(e,(6,4))
  result,turns=natural.natural_battle(e)
  print('Natural Prague mission:',result,turns,'selections',flush=True)
  assert result==1 and e.var(0x408C)==7
  talk(e,(2,4));save(e,'natural-prague-complete')
  e.screenshot(ROOT/'test-output/eclipse-natural-prague.png')
  e.close();e=Emulator(ROOT/'pokefirered.gba')
  load_checkpoint(e,'natural-prague-complete',True)
  assert e.var(0x408C)==7 and e.var(0x4090)==0
  print('PASS: Prague mission and cold Continue with naturally trained team.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
