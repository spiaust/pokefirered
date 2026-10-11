"""Earn Amsterdam's badge using a naturally caught and stone-evolved partner."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import world,battle_start
from natural_team_test_helpers import capture,lead
from test_eclipse_supplies import use_stone,count
from test_oxford_gym import count_pocket
from tm_teaching_test_helpers import field
from test_landmark_cases import save
import sys
battle=natural.natural_battle


def encounter(e):
 if not e.read('gBattleTypeFlags')&8:
  if e.read('gPlayerPartyCount',1)==3 and monfield(e,0,0,0,'gEnemyParty')&0xffff==29:return capture(e)
  action=natural.first_symbol('HandleInputChooseAction')
  for _ in range(400):
   if not e.in_battle():break
   if e.task_active('Task_HandleChooseMonInput'):
    target=next(i for i in range(e.read('gPlayerPartyCount',1)) if e.read(e.symbols['gPlayerParty']+100*i+86,2))
    for _ in range(10):
     cur=e.read(e.symbols['gPartyMenu']+9,1)
     if cur==target:break
     e.press('LEFT' if target==0 else 'RIGHT' if cur==0 else 'DOWN' if cur<target else 'UP',60)
    e.press('A',180);e.press('A',180);continue
   if e.read('gBattlerControllerFuncs')&~1==action:
    e.press('UP',2);e.press('LEFT',2);e.press('DOWN',2);e.press('RIGHT',2);e.press('A',90)
   else:e.press('A',30)
  if e.in_battle() or e.read('gBattleOutcome',1) not in (4,5):
   e.screenshot(ROOT/'test-output/amsterdam-escape.png');e.state(ROOT/'test-output/amsterdam-escape.state')
  assert not e.in_battle() and e.read('gBattleOutcome',1) in (4,5),(e.in_battle(),e.read('gBattleOutcome',1),monfield(e,0,0,0,'gEnemyParty')&0xffff)
  e.finish_dialogue();e.frames(180);return e.read('gBattleOutcome',1),0
 return battle(e)


def main():
 natural.natural_battle=encounter
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  resume='--resume' in sys.argv;caught='--caught' in sys.argv
  load_checkpoint(e,'natural-trained-amsterdam' if resume else 'natural-caught-nidoran' if caught else 'natural-raichu',True)
  assert e.var(0x408C)==4 and e.var(0x4090)==0
  if not resume and not caught:
   talk(e,(2,4));world(e,3)
   for _ in range(400):
    if e.read('gPlayerPartyCount',1)==4:break
    natural.natural_go(e,(5,21));natural.natural_go(e,(6,21))
   assert e.read('gPlayerPartyCount',1)==4,'no Nidoran encountered'
   assert monfield(e,3,0,0)&0xffff==29
   save(e,'natural-caught-nidoran')
  if not resume:
   lead(e,3);assert monfield(e,0,0,0)&0xffff==29
   talk(e,(43,31),'YES');talk(e,(10,16),'YES');assert e.location()[:2]==(44,8)
   talk(e,(2,7));assert e.location()[:2]==(44,6)
   for practice in range(30):
    if monfield(e,0,0,0)&0xffff==30:break
    talk(e,(2,4));talk(e,(10,7));battle_start(e,(7,7));result,turns=battle(e)
    assert result==1,('Nidoran practice',practice,result)
    talk(e,(15,20));print('Nidoran practice:',practice+1,'level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
   assert monfield(e,0,0,0)&0xffff==30
   assert count(e,94)==1;use_stone(e,94,0)
   for _ in range(100):
    if monfield(e,0,0,0)&0xffff==31 and count(e,94)==0:break
    e.press('A',90)
   for _ in range(12):e.press('A',180)
   e.screenshot(ROOT/'test-output/amsterdam-stone.png')
   field(e);assert monfield(e,0,0,0)&0xffff==31 and count(e,94)==0
   print('PASS: naturally caught Nidoran levels into Nidorina and purchased Moon Stone evolves Nidoqueen.',flush=True)
   for practice in range(30):
    if e.read(e.symbols['gPlayerParty']+84,1)>=25:break
    talk(e,(2,4));talk(e,(10,7));battle_start(e,(7,7));result,turns=battle(e)
    assert result==1,('Nidoqueen practice',practice,result)
    talk(e,(15,20));print('Nidoqueen practice:',practice+1,'level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
   assert e.read(e.symbols['gPlayerParty']+84,1)>=25
   talk(e,(2,4));talk(e,(10,4));talk(e,(2,4));save(e,'natural-trained-amsterdam')
  battle_start(e,(6,4));result,turns=battle(e)
  print('Natural Amsterdam gym:',result,turns,'selections; level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
  assert result==1 and e.var(0x408C)==5
  assert e.read(e.read('gSaveBlock1Ptr')+0xee0+0x823//8,1)&(1<<(0x823%8))
  assert count_pocket(e,322,0x464,58)==1
  e.screenshot(ROOT/'test-output/eclipse-natural-amsterdam.png');save(e,'natural-fourth-badge')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-fourth-badge',True)
  assert e.var(0x408C)==5 and monfield(e,0,0,0)&0xffff==31 and e.read('gPlayerPartyCount',1)==4
  assert e.read(e.read('gSaveBlock1Ptr')+0xee0+0x823//8,1)&(1<<(0x823%8))
  assert count_pocket(e,322,0x464,58)==1
  print('PASS: fourth badge won at normal levels/stats/AI; four-partner team and badge survive cold Continue.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
