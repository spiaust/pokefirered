"""Catch a Flying partner and earn the third badge through native menus/training."""
from emulator import Emulator,ROOT
import test_eclipse_natural as natural
import test_shadow_runtime,test_continent_runtime
from test_shadow_runtime import talk,monfield
from test_continent_runtime import battle_start
from test_celebi import load_checkpoint
from test_gym_ui import start_action
from test_navigation import wait_task
from test_country import wait_menu
from test_landmark_cases import save
from test_oxford_gym import count_pocket
import sys
battle=natural.natural_battle

def capture(e):
 action=natural.first_symbol('HandleInputChooseAction');before=e.read('gPlayerPartyCount',1)
 for attempt in range(10):
  for _ in range(150):
   if e.read('gBattlerControllerFuncs')&~1==action:break
   e.press('A',30)
  assert count_pocket(e,4,0x430,13)>0,'no Balls remain'
  e.press('UP',2);e.press('LEFT',2);e.press('RIGHT',2);e.press('A',180)
  wait_task(e,'Task_BagMenu_HandleInput');bag=e.symbols['gBagMenuState']
  for _ in range(5):
   pocket=e.read(bag+6,2)
   if pocket==2:break
   e.press('RIGHT' if pocket<2 else 'LEFT',60)
  e.press('A',90);e.press('A',180)
  for _ in range(150):
   if e.read('gPlayerPartyCount',1)>before:
    for _ in range(30):
     if not e.in_battle():break
     if e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_NamingScreen']&~1:e.press('START',30);e.press('A',120)
     else:e.press('B',90);e.press('A',90)
    e.finish_dialogue();e.frames(180)
    assert not e.in_battle()
    print('PASS: Pidgey caught with native full HP, catch rate and',attempt+1,'Ball attempts.',flush=True)
    return 7,attempt+1
   if e.read('gBattlerControllerFuncs')&~1==action:break
   e.press('A',30)
 raise AssertionError('Pidgey capture failed')

def encounter(e):
 if not e.read('gBattleTypeFlags')&8 and e.read('gPlayerPartyCount',1)==1 and monfield(e,0,0,0,'gEnemyParty')&0xffff==16:return capture(e)
 if not e.read('gBattleTypeFlags')&8 and e.read('gPlayerPartyCount',1)==1:
  action=natural.first_symbol('HandleInputChooseAction')
  for _ in range(220):
   if not e.in_battle():break
   if e.read('gBattlerControllerFuncs')&~1==action:
    e.press('UP',2);e.press('LEFT',2);e.press('DOWN',2);e.press('RIGHT',2);e.press('A',90)
   else:e.press('A',30)
  assert not e.in_battle() and e.read('gBattleOutcome',1)==4
  e.finish_dialogue();e.frames(180);return 4,0
 return battle(e)

natural.natural_battle=encounter
test_shadow_runtime.go=natural.natural_go;test_continent_runtime.go=natural.natural_go

def lead(e,index):
 start_action(e,1);wait_task(e,'Task_HandleChooseMonInput')
 for _ in range(12):
  cur=e.read(e.symbols['gPartyMenu']+9,1)
  if cur==index:break
  e.press('DOWN' if cur<index else 'UP',30)
 assert cur==index
 e.press('A',60);wait_task(e,'Task_HandleSelectionMenuInput');e.frames(120);e.press('DOWN',60);e.press('A',120)
 wait_task(e,'Task_HandleChooseMonInput');e.frames(120)
 # Switch mode uses slotId2 as the destination; slotId remains the source.
 e.press('LEFT',60)
 assert e.read(e.symbols['gPartyMenu']+10,1)==0
 e.press('A',180);wait_task(e,'Task_HandleChooseMonInput')
 for _ in range(8):e.press('B',180)
 e.frames(180)
 assert not e.task_active('Task_HandleChooseMonInput') and not e.read('sLockFieldControls',1)
 assert monfield(e,0,0,0)&0xffff==16

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'natural-trained-brussels' if '--resume' in sys.argv else 'natural-caught-brussels' if '--caught' in sys.argv else 'natural-second-badge',True)
 assert e.var(0x408C)==3 and e.var(0x4090)==0
 if '--resume' not in sys.argv and '--caught' not in sys.argv:
  talk(e,(10,4));talk(e,(2,4));talk(e,(10,7))
  for _ in range(200):
   if e.read('gPlayerPartyCount',1)>1:break
   # Ordinary walking encounters; no spawn/rate or RNG modifications.
   natural.natural_go(e,(5,8));natural.natural_go(e,(6,8))
   e.walk('UP',1);e.frames(90)
   if e.in_battle():encounter(e)
   e.walk('DOWN',1);e.frames(90)
   if e.in_battle():encounter(e)
  assert e.read('gPlayerPartyCount',1)==2,'no Pidgey encountered'
  talk(e,(15,20));talk(e,(2,4));save(e,'natural-caught-brussels')
 if '--resume' not in sys.argv:
  lead(e,1)
  for practice in range(15):
   if e.read(e.symbols['gPlayerParty']+84,1)>=22:break
   talk(e,(10,7));battle_start(e,(7,7));result,turns=battle(e)
   assert result==1,('Grass route practice',practice,result)
   talk(e,(15,20));talk(e,(2,4))
   print('Natural Flying-partner practice:',practice+1,'level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
  save(e,'natural-trained-brussels')
 battle_start(e,(6,4));result,turns=battle(e)
 print('Natural Brussels gym:',result,turns,'turns; level',e.read(e.symbols['gPlayerParty']+84,1),flush=True)
 e.screenshot(ROOT/'test-output/eclipse-natural-brussels.png')
 assert result==1 and e.var(0x408C)==4
 save(e,'natural-third-badge');e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'natural-third-badge',True)
 assert e.var(0x408C)==4
 print('PASS: naturally caught/trained Flying partner earns third badge; native save survives cold Continue.',flush=True)
finally:e.close()
