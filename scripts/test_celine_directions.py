"""Early country quest contacts, native refusals/gates and cold Continue."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_country import wait_menu
from test_time import preserved
from key_item_test_helpers import reload
def history(e):return tuple(e.var(v) for v in range(0x40C0,0x4100))
def speak(e,country,choice=None):
 before=preserved(e),history(e),e.location();e.press('DOWN');e.press('A',900)
 if choice:
  wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
  if choice=='NO':e.press('DOWN');e.press('A',180)
  else:e.press('B',180)
 else:
  for page in range(4 if country=='france' else 2):
   e.screenshot(ROOT/f'test-output/celine-directions-{country}-page{page}.png');e.press('A',900)
 e.finish_dialogue();assert not e.in_battle() and not e.read('sLockFieldControls',1)
 assert (preserved(e),history(e),e.location())==before
e=Emulator(ROOT/'pokefirered.gba')
try:
 for dest,country in enumerate(['england','france','germany']):
  load_checkpoint(e,'start-'+country+'-0',True);go(e,(10,14))
  for choice in (['NO','B'] if dest==0 else [None,None]):speak(e,country,choice)
  print(f'PASS: {country} early contact approach and repeated refusal/badge gate retain exact starter, money, items and story',flush=True)
  before=preserved(e),history(e),e.location();e=reload(e,'celine-directions-'+country)
  assert (preserved(e),history(e),e.location())==before;speak(e,country,'NO' if dest==0 else None)
  print(f'PASS: {country} native cold Continue retains contact position and initial quest state',flush=True)
  if dest==0:
   e.press('DOWN');e.press('A',900);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',900);e.finish_dialogue()
   assert e.var(0x40FB)==1
   e=reload(e,'celine-directions-england-accepted');assert e.var(0x40FB)==1
   print('PASS: England normal Yes starts Oak study and native cold Continue retains acceptance',flush=True)
finally:e.close()
