"""Legendary Nuzlocke enforcement with explicit stage/Ball/escape fixtures."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import setstage
from test_continent_runtime import world,var,battle_start
from test_eclipse_legendaries import D,flag,open_ball,capture,flee
from test_oxford_gym import count_pocket


def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-finished',True);e.write('sWildEncountersDisabled',1,1)
  row=D[0];world(e,row['country_index']);setstage(e,row['min_stage'])
  var(e,0x4091,1);area=21+row['country_index'];bank=0x4095+area//16
  var(e,bank,e.var(bank)&~(1<<(area%16)))
  p=e.read('gSaveBlock1Ptr')+0x430;key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
  e.write(p,1,2);e.write(p+2,1^key,2)
  target=row['x'],row['y']+1;f=int(row['flag'],16)
  battle_start(e,target);assert e.var(0x4094)==0;flee(e);assert not flag(e,f)
  battle_start(e,target);assert e.var(0x4094)==1
  before=e.read('gPlayerPartyCount',1);open_ball(e)
  for _ in range(100):
   ptr=e.read('gBattlescriptCurrInstr')
   if e.symbols['BattleScript_NuzlockeBallBlock']<=ptr<e.symbols['BattleScript_NuzlockeBallBlock']+20:break
   e.frames(10)
  assert e.symbols['BattleScript_NuzlockeBallBlock']<=ptr<e.symbols['BattleScript_NuzlockeBallBlock']+20
  assert count_pocket(e,1,0x430,13)==1 and e.read('gPlayerPartyCount',1)==before and not flag(e,f)
  e.screenshot(ROOT/'test-output/eclipse-legendary-nuzlocke.png');flee(e)
  var(e,0x4091,0);battle_start(e,target);assert e.var(0x4094)==0;capture(e);assert flag(e,f)
  print('PASS: legendary first encounter allowed; retry refuses/refunds Master Ball in Nuzlocke; OFF allows native catch.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
