"""Teach genuinely earned Gym TMs through native menus; no memory writes."""
from collections import Counter
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved
from test_oxford_gym import count_pocket
from battle_recovery_test_helpers import moves_pp
from key_item_test_helpers import reload

def state(e):
 p=preserved(e)
 return p[:3]+(Counter(x for x in p[3] if x[0]),)+p[4:]

def select(e,tm):
 open_key_item(e,364);e.frames(180)
 base=e.read('gSaveBlock1Ptr')+0x464
 target=next(i for i in range(58) if e.read(base+4*i,2)==tm)
 # Native TM list cursor is stored in its active ListMenu task. Moving to
 # the top avoids relying on a previously saved or freshly sorted position.
 for _ in range(60):e.press('UP',10)
 for _ in range(target):e.press('DOWN',60)
 e.press('A',180);e.press('A',180)
 wait_task(e,'Task_HandleChooseMonInput');e.frames(60)

def field(e):
 for _ in range(8):e.press('B',180)
 e.screenshot(ROOT/'test-output/gym-tm-field-debug.png')
 assert not e.read('sLockFieldControls',1)
 assert not e.task_active('Task_HandleChooseMonInput')

def advance(e,task):
 for _ in range(40):
  if e.task_active(task):
   e.frames(60);return
  e.press('A',90)
 raise AssertionError(task)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for city,tm in [('Oxford',327),('Chantilly',291),('Oranienburg',322)]:
  load_checkpoint(e,f'gym-defeat-{city}-retry-won',True)
  before=state(e);assert count_pocket(e,tm,0x464,58)==1
  select(e,tm);e.press('A',900)
  e.screenshot(ROOT/'test-output/gym-tm-replacement-debug.png')
  e.screenshot(ROOT/f'test-output/gym-tm-{city}-incompatible.png')
  e.press('A',180);field(e);assert state(e)==before
  e=reload(e,f'gym-tm-{city}-incompatible');assert state(e)==before
  print(f'PASS: {city} incompatible Bulbasaur attempt keeps the earned TM, moves, party and journey unchanged through cold Continue',flush=True)
 for name,tm,move in [('Rock-Tomb',327,317),('Water-Pulse',291,352)]:
  load_checkpoint(e,'walkthrough-germany-complete',True)
  before=state(e);oldmoves,oldpp=moves_pp(e)
  assert count_pocket(e,tm,0x464,58)==1 and move not in oldmoves and all(oldmoves)
  select(e,tm);e.press('B',180);field(e);assert state(e)==before
  select(e,tm);e.press('A',900)
  advance(e,'Task_HandleReplaceMoveYesNoInput');e.press('B',180)
  advance(e,'Task_HandleStopLearningMoveYesNoInput');e.press('A',900)
  e.press('A',180);field(e);assert state(e)==before
  print(f'PASS: {name} party selection and four-move replacement cancellation preserve earned TM and exact state',flush=True)
  select(e,tm);e.press('A',900)
  advance(e,'Task_HandleReplaceMoveYesNoInput');e.press('A',180)
  advance(e,'Task_InputHandler_SelectOrForgetMove');e.frames(180)
  for _ in range(5):e.press('UP',60)
  # Move selection wraps; explicitly select slot zero using its native cursor.
  for _ in range(5):
   if e.read('sMoveSelectionCursorPos',1)==0:break
   e.press('DOWN',60)
  assert e.read('sMoveSelectionCursorPos',1)==0
  e.screenshot(ROOT/f'test-output/gym-tm-{name}-replace.png');e.press('A',900)
  for _ in range(15):
   if count_pocket(e,tm,0x464,58)==0:break
   e.press('A',180)
  assert count_pocket(e,tm,0x464,58)==0
  e.screenshot(ROOT/f'test-output/gym-tm-{name}-learned.png');e.press('A',180);field(e)
  newmoves,newpp=moves_pp(e)
  assert newmoves==(move,)+oldmoves[1:] and newpp[1:]==oldpp[1:]
  assert newpp[0]==e.read(e.symbols['gBattleMoves']+12*move+4,1)
  after=state(e);assert after[1:3]==before[1:3] and after[4:]==before[4:]
  bag=before[3].copy();bag[(tm,1)]-=1
  assert +bag==after[3]
  print(f'PASS: {name} normal teaching replaces only selected Marshtomp move, gives full native PP and consumes exactly one TM without changing money/story/badges',flush=True)
  e=reload(e,f'gym-tm-{name}-learned')
  assert moves_pp(e)==(newmoves,newpp) and state(e)==after and count_pocket(e,tm,0x464,58)==0
  print(f'PASS: {name} learned move, PP and consumed TM persist through normal Save and cold Continue',flush=True)
finally:
 e.screenshot(ROOT/'test-output/gym-tm-final-debug.png')
 e.close()
