"""Enter the past naturally, verify reversible palettes, and defeat its patrol."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk
from test_continent_runtime import battle_start
from test_landmark_cases import save
from test_oxford_gym import count_pocket

def palette(e):
 p=e.symbols['gPlttBufferUnfaded']
 player=next(e.symbols['gObjectEvents']+36*i for i in range(16) if e.read(e.symbols['gObjectEvents']+36*i,1)&1 and e.read(e.symbols['gObjectEvents']+36*i+2,1)&1)
 sprite=e.symbols['gSprites']+68*e.read(player+4,1)
 slot=e.read(sprite+4,2)>>12
 tiles=tuple(e.read(p+2*i,2) for i in range(13*16))
 actor=tuple(e.read(p+512+32*slot+2*i,2) for i in range(16))
 return tiles,actor

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-lisbon-complete',True)
  assert e.var(0x408C)==12 and e.var(0x4090)==0 and e.location()[:2]==(44,22)
  modern=palette(e)
  talk(e,(10,4),'NO');assert e.location()[:2]==(44,22)
  talk(e,(10,4),'YES');assert e.location()[:2]==(44,24) and palette(e)!=modern
  past=palette(e);talk(e,(2,7),'NO');assert e.location()[:2]==(44,24)
  talk(e,(2,7),'YES');assert e.location()[:2]==(44,22) and palette(e)==modern and e.var(0x408C)==12
  talk(e,(10,4),'YES');assert e.location()[:2]==(44,24) and palette(e)==past
  print('PASS: earned wartime gate, travel declines, past palette and modern restoration.',flush=True)
  talk(e,(2,4));battle_start(e,(6,4))
  result,turns=natural.natural_battle(e,healing_item=21,healing_limit=count_pocket(e,21,0x310,42))
  print('Paris 1940 native patrol:',result,turns,'selections',flush=True)
  assert result==1 and e.var(0x408C)==13
  talk(e,(2,4));save(e,'natural-paris1940-complete');e.screenshot(ROOT/'test-output/eclipse-natural-paris1940.png')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-paris1940-complete',True)
  assert e.var(0x408C)==13 and e.location()[:2]==(44,24) and palette(e)==past
  print('PASS: naturally unlocked Paris 1940 patrol, sepia palette and cold Continue.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
