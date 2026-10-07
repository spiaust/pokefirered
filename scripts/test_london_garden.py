"""London garden visitor and companion interaction and save continuity through native input."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved

def greet(e):
 go(e,(31,35));before=preserved(e);e.press('UP');e.press('A',180)
 assert e.read('sLockFieldControls',1)
 e.screenshot(ROOT/'test-output/london-garden-companion-dialogue.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1) and preserved(e)==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);before=preserved(e)[1:]
 go(e,(31,35));e.walk('UP',1);assert e.location()==(43,0,31,35)
 for _ in range(3):
  go(e,(30,35));party_before=preserved(e);e.press('UP');e.press('A',180);assert e.read('sLockFieldControls',1)
  e.frames(120)
  e.screenshot(ROOT/'test-output/london-garden-visitor.png')
  e.finish_dialogue();assert not e.read('sLockFieldControls',1)
  assert preserved(e)==party_before
  greet(e);assert preserved(e)[1:]==before
 for p in [(27,31),(33,31),(33,36),(29,36),(27,37),(29,29),(20,28),(22,38)]:go(e,p)
 go(e,(31,35));save(e,'london-garden-companion-save');saved=preserved(e)
 e.screenshot(ROOT/'test-output/london-garden-companion-courtyard.png')
 print('PASS: old London garden save, companion collision and three greetings preserve party/inventory/progress and garden/bridge routes',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'london-garden-companion-save',True)
 assert e.location()==(43,0,31,35) and preserved(e)==saved
 greet(e);assert preserved(e)==saved
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,1)
 print('PASS: London companion Save/cold Continue, repeat greeting and countryside return',flush=True)
finally:e.close()
