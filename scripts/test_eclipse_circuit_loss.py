"""Native loss/retry with explicit one-partner, HP and harmless-move fixtures."""
from test_eclipse_circuit import *
from test_eclipse_natural import first_symbol


def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-finished',True);e.write('sWildEncountersDisabled',1,1);var(e,0x40bf,1)
  shelter(e,'ShadowLondon')
  if not flag(e,0x8c6):talk(e,(6,4),'NO')
  e.write('gPlayerPartyCount',1,1);e.write(e.symbols['gPlayerParty']+86,1,2)
  battle_start(e,(6,4));action=first_symbol('HandleInputChooseAction');move=first_symbol('HandleInputChooseMove')
  for _ in range(800):
   if not e.in_battle():break
   if e.read('gBattlerControllerFuncs')&~1 in (action,move):
    b=e.symbols['gBattleMons'];e.write(b+40,1,2);e.write(b+4,1,2);e.write(b+10,1,2);e.write(b+12,MOVES['MOVE_SPLASH'],2);e.write(b+36,40,1);e.press('UP',2);e.press('LEFT',2)
   e.press('A',30)
  assert not e.in_battle() and e.read('gBattleOutcome',1)==2
  e.finish_dialogue();e.frames(480);assert e.var(0x40bf)==1 and e.var(0x408c)==21
  print('Native blackout location:',e.location(),flush=True)
  if e.location()[:2]==(43,3):
   go(e,(7,7))
   for _ in range(4):
    if e.location()[:2]!=(43,3):break
    e.walk('DOWN',1);e.frames(240)
   assert e.location()[:2]==(43,0),e.location()
  if e.location()[:2]==(43,0):talk(e,(10,16),'YES');assert e.location()[:2]==(44,40)
  shelter(e,'ShadowLondon');battle_start(e,(6,4));win(e);assert e.var(0x40bf)==2 and e.var(0x408c)==21
  print('PASS: native blackout preserves pending circuit match and main ending; real retry victory advances once.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
