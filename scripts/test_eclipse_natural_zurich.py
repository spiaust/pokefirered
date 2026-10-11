"""Prepare an earned Nidoqueen for Zurich through native TM and route menus."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from natural_team_test_helpers import lead
from tm_teaching_test_helpers import select,field
from test_landmark_cases import save
from test_oxford_gym import count_pocket
from battle_recovery_test_helpers import moves_pp
import sys

def advance(e,task):
 for _ in range(40):
  if e.task_active(task):e.frames(60);return
  e.press('A',90)
 raise AssertionError(task)

def main():
 test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'natural-trained-zurich' if '--resume' in sys.argv else 'natural-zurich-preparation' if '--training' in sys.argv else 'natural-sixth-badge',True)
  assert e.var(0x408C)==8 and e.var(0x4090)==0
  if '--resume' not in sys.argv and '--training' not in sys.argv:
   lead(e,3);assert monfield(e,0,0,0)&65535==31
   old,_=moves_pp(e);assert old[1]==24
   select(e,319);e.press('A',900);advance(e,'Task_HandleReplaceMoveYesNoInput');e.press('A',180)
   advance(e,'Task_InputHandler_SelectOrForgetMove')
   for _ in range(6):
    cur=e.read('sMoveSelectionCursorPos',1)
    if cur==1:break
    e.press('DOWN' if cur<1 else 'UP',60)
   assert e.read('sMoveSelectionCursorPos',1)==1
   e.press('A',900)
   for _ in range(15):
    if count_pocket(e,319,0x464,58)==0:break
    e.press('A',180)
   e.press('A',180);field(e)
   assert moves_pp(e)[0]==(old[0],280,old[2],old[3]) and count_pocket(e,319,0x464,58)==0
   talk(e,(10,4));assert e.location()[:2]==(44,16)
  if '--resume' not in sys.argv:
   assert e.location()[:2]==(44,16)
   for practice in range(25):
    if e.read(e.symbols['gPlayerParty']+84,1)>=37:break
    talk(e,(2,4));talk(e,(10,7));result,turns=natural.natural_trainer_battle(e,(22,7))
    print('Zurich preparation:',practice+1,'result',result,'level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
    assert result==1
    talk(e,(15,20));talk(e,(2,4));save(e,'natural-zurich-preparation')
   assert e.read(e.symbols['gPlayerParty']+84,1)>=37
   talk(e,(2,4));save(e,'natural-trained-zurich')
  battle_start(e,(6,4));result,turns=natural.natural_battle(e)
  print('Prepared Zurich:',result,turns,'selections',flush=True)
  assert result==1 and e.var(0x408C)==9
  talk(e,(2,4));save(e,'natural-zurich-complete')
  e.screenshot(ROOT/'test-output/eclipse-natural-zurich.png')
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-zurich-complete',True)
  assert e.var(0x408C)==9 and monfield(e,0,0,0)&65535==31 and moves_pp(e)[0][1]==280
  print('PASS: earned Brick Break, native training, Zurich victory and cold Continue.',flush=True)
 except Exception:
  print('Failure context:',e.location(),'battle',e.in_battle(),'stage',e.var(0x408C),'lock',e.read('sLockFieldControls',1),flush=True)
  e.screenshot(ROOT/'test-output/natural-zurich-failure.png')
  e.state(ROOT/'test-output/natural-zurich-failure.state')
  raise
 finally:e.close()
if __name__=='__main__':main()
