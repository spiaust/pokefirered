"""Use native matchup switches to finish the Berlin 1944 resistance chapter."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from natural_team_test_helpers import lead
from test_eclipse_natural_past import palette

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-warsaw1943-complete',True)
  assert e.var(0x408C)==14 and e.var(0x4090)==0 and e.var(0x4091)==0
  index=next(i for i in range(5) if monfield(e,i,0,0)&65535==31)
  if index:lead(e,index)
  talk(e,(10,4));assert e.location()[:2]==(44,28)
  talk(e,(2,4));before_palette=palette(e);battle_start(e,(6,4))
  result,turns=natural.natural_battle(e,healing_item=21,healing_limit=count_pocket(e,21,0x310,42),revive_species=229,matchups={82:31,97:229,169:31,229:31},trace=True)
  print('Berlin 1944 prepared battle:',result,turns,'attack selections',flush=True)
  assert result==1 and e.var(0x408C)==15
  talk(e,(2,4));save(e,'natural-berlin1944-complete');e.screenshot(ROOT/'test-output/eclipse-natural-berlin1944.png')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-berlin1944-complete',True)
  assert e.var(0x408C)==15 and e.read('gPlayerPartyCount',1)==5 and palette(e)==before_palette
  past=palette(e);talk(e,(10,4),'NO');assert e.location()[:2]==(44,28)
  talk(e,(10,4),'YES');assert e.location()[:2]==(44,30) and palette(e)!=past and e.var(0x408C)==15
  save(e,'natural-geneva-ready');modern=palette(e)
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-geneva-ready',True)
  assert e.location()[:2]==(44,30) and e.var(0x408C)==15 and palette(e)==modern
  print('PASS: Berlin 1944 victory, native matchup switching, cold sepia save and modern Geneva return.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
