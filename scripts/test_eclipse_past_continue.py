"""Keep country map and player colors correct across cold saves in both eras."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk
from test_continent_runtime import world
from test_landmark_cases import save
from test_eclipse_natural_past import palette

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-paris1940-complete',True);assert e.var(0x408C)==13
  world(e,1);assert e.location()[:2]==(45,2)
  modern=palette(e);talk(e,(18,31),'YES');assert e.location()[:2]==(45,3)
  past=palette(e);assert past[0]!=modern[0] and past[1]!=modern[1]
  save(e,'natural-country-past-continue')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-country-past-continue',True)
  assert e.location()[:2]==(45,3) and e.var(0x408C)==13 and palette(e)==past
  talk(e,(18,31),'YES');assert e.location()[:2]==(45,2) and palette(e)==modern
  save(e,'natural-country-modern-continue')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-country-modern-continue',True)
  assert e.location()[:2]==(45,2) and e.var(0x408C)==13 and palette(e)==modern
  print('PASS: historical country tiles/player tint survives cold Continue; modern return and cold colors remain correct.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
