"""Timer Ball Nuzlocke rejection/refund with explicit encounter/escape fixtures.
This isolates the shared Ball rule; it is not a natural combat-balancing run.
"""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_shadow_runtime import setstage
from test_continent_runtime import world,var,battle_start
from test_eclipse_legendaries import D,flag,open_ball,flee
from test_oxford_gym import count_pocket
import test_eclipse_natural as natural

def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-finished',True)
  e.write('sWildEncountersDisabled',1,1);row=D[0];world(e,row['country_index']);setstage(e,row['min_stage'])
  var(e,0x4091,1);area=21+row['country_index'];bank=0x4095+area//16
  var(e,bank,e.var(bank)|(1<<(area%16))) # Explicit already-used encounter allowance.
  p=e.read('gSaveBlock1Ptr')+0x430;key=e.read(e.read('gSaveBlock2Ptr')+0xf20,2)
  e.write(p,10,2);e.write(p+2,1^key,2) # Explicit one-Timer-Ball fixture.
  target=row['x'],row['y']+1;f=int(row['flag'],16);before=e.read('gPlayerPartyCount',1)
  battle_start(e,target);assert e.var(0x4094)==1;open_ball(e)
  for _ in range(100):
   ptr=e.read('gBattlescriptCurrInstr')
   if e.symbols['BattleScript_NuzlockeBallBlock']<=ptr<e.symbols['BattleScript_NuzlockeBallBlock']+20:break
   e.frames(10)
  assert e.symbols['BattleScript_NuzlockeBallBlock']<=ptr<e.symbols['BattleScript_NuzlockeBallBlock']+20
  assert count_pocket(e,10,0x430,13)==1 and e.read('gPlayerPartyCount',1)==before and not flag(e,f)
  flee(e);var(e,0x4091,0);battle_start(e,target);assert e.var(0x4094)==0
  open_ball(e)
  for _ in range(200):
   if not e.in_battle() or e.read('gBattlerControllerFuncs')&~1==natural.first_symbol('HandleInputChooseAction'):break
   if e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_NamingScreen']&~1:e.press('START',30);e.press('A',120)
   else:e.press('A',30)
  assert count_pocket(e,10,0x430,13)==0
  assert e.read(e.symbols['gBattleResults']+0x36+8,1)==1
  if e.in_battle():flee(e)
  print('PASS: Timer Ball is refused and refunded for an exhausted Nuzlocke allowance; OFF consumes it through the native catch handler.',flush=True)
 finally:e.close()
if __name__=='__main__':main()
