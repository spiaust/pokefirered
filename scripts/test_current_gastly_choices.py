"""Native optional Gastly choices and ordinary escape; no injected items or party."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk
from test_country import party_species,wait_menu
from test_time import preserved
from key_item_test_helpers import reload
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'current-landmarks-notredame-complete',True);go(e,(10,5));before=preserved(e)
 for choice in ['B','NO']:talk(e,(10,5),choice=choice);assert not e.in_battle() and preserved(e)==before and e.var(0x40C0)==6
 e=reload(e,'current-gastly-ready');talk(e,(10,5),choice='B');assert preserved(e)==before
 print('PASS: completed Notre-Dame optional Gastly No/B and cold Continue preserve case, party, inventory and money without starting battle',flush=True)
 e.press('UP');e.press('A',180);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180)
 for _ in range(30):
  if e.in_battle():break
  e.frames(90)
 assert e.in_battle();e.frames(300)
 assert party_species(e,'gEnemyParty',0)==92 and e.read(e.symbols['gEnemyParty']+0x54,1)==12
 e.screenshot(ROOT/'test-output/current-gastly-battle.png')
 action=next(int(line.split()[0],16) for line in (ROOT/'pokefirered.sym').read_text().splitlines() if line.split()[-1:]==['HandleInputChooseAction'])
 for _ in range(600):
  if not e.in_battle():break
  if e.read('gBattlerControllerFuncs')&~1==action:
   e.press('DOWN');e.press('RIGHT');e.press('A',30)
  else:e.press('B',30)
 assert not e.in_battle() and e.read('gBattleOutcome',1)==4
 e.frames(180);e.finish_dialogue();assert e.var(0x40C0)==6 and preserved(e)[1:]==before[1:]
 e=reload(e,'current-gastly-escaped');talk(e,(10,5),choice='B');assert e.var(0x40C0)==6
 print('PASS: accepted native encounter creates level-12 Gastly; ordinary Run returns to resolved case, and saved repeat neither consumes items nor awards another reward',flush=True)
finally:e.close()
