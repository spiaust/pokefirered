"""Earn the eighth badge with the naturally trained seventh-badge party."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from test_continent_runtime import battle_start

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-seventh-badge',True)
  assert e.var(0x408C)==10 and e.var(0x4090)==0
  for stage,city,checkpoint in ((10,'Madrid','natural-eighth-badge'),):
   talk(e,(10,4));assert e.location()[:2]==(44,stage*2)
   talk(e,(2,4));battle_start(e,(6,4));result,turns=natural.natural_battle(e)
   print(city,'natural battle:',result,turns,'selections; stage',e.var(0x408C),flush=True)
   assert result==1 and e.var(0x408C)==stage+1
   assert count_pocket(e,314,0x464,58)==1
   for flag in range(0x820,0x828):
    assert e.read(e.read('gSaveBlock1Ptr')+0xee0+flag//8,1)&(1<<(flag%8))
   talk(e,(2,4));save(e,checkpoint);e.screenshot(ROOT/f'test-output/eclipse-natural-{city.lower()}.png')
   e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,checkpoint,True)
   assert e.var(0x408C)==stage+1 and e.var(0x4090)==0
   assert count_pocket(e,314,0x464,58)==1
   for flag in range(0x820,0x828):
    assert e.read(e.read('gSaveBlock1Ptr')+0xee0+flag//8,1)&(1<<(flag%8))
   print('PASS:',city,'victory and cold Continue.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
