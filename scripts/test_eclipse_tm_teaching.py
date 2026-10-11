"""Teach a truly earned Eclipse TM through native menus and cold-save it."""
from emulator import Emulator,ROOT
from test_shadow_runtime import talk
from test_celebi import load_checkpoint
from test_oxford_gym import count_pocket
from battle_recovery_test_helpers import moves_pp
from tm_teaching_test_helpers import select,field
from test_landmark_cases import save

def advance(e,task):
 for _ in range(40):
  if e.task_active(task):e.frames(60);return
  e.press('A',90)
 raise AssertionError(task)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'natural-second-badge',True);talk(e,(6,4));assert count_pocket(e,291,0x464,58)==1
 stage=e.var(0x408C);old,pp=moves_pp(e)
 select(e,291);e.press('B',180);field(e);assert count_pocket(e,291,0x464,58)==1 and moves_pp(e)==(old,pp)
 select(e,291);e.press('A',900);advance(e,'Task_HandleReplaceMoveYesNoInput');e.press('A',180)
 advance(e,'Task_InputHandler_SelectOrForgetMove')
 for _ in range(5):
  if e.read('sMoveSelectionCursorPos',1)==0:break
  e.press('DOWN',60)
 assert e.read('sMoveSelectionCursorPos',1)==0;e.press('A',900)
 for _ in range(15):
  if count_pocket(e,291,0x464,58)==0:break
  e.press('A',180)
 e.press('A',180);field(e);new,newpp=moves_pp(e)
 assert new==(352,)+old[1:] and newpp[1:]==pp[1:]
 assert newpp[0]==e.read(e.symbols['gBattleMoves']+12*352+4,1) and count_pocket(e,291,0x464,58)==0 and e.var(0x408C)==stage
 save(e,'natural-water-pulse');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-water-pulse',True)
 assert moves_pp(e)==(new,newpp) and count_pocket(e,291,0x464,58)==0 and e.var(0x408C)==stage
 talk(e,(6,4));assert count_pocket(e,291,0x464,58)==0
 e.screenshot(ROOT/'test-output/eclipse-water-pulse-learned.png')
 print('PASS: earned Water Pulse teaches normally, consumes one TM, survives cold Continue and cannot be reclaimed.',flush=True)
finally:e.close()
