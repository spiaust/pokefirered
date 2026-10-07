"""Paris garden observer and companion interaction and save continuity through native input."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved

def greet(e):
 go(e,(7,41));before=preserved(e);e.press('UP');e.press('A',180)
 assert e.read('sLockFieldControls',1)
 e.screenshot(ROOT/'test-output/paris-garden-companion-dialogue.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1) and preserved(e)==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'paris-realism-save',True);before=preserved(e)[1:]
 go(e,(7,41));e.walk('UP',1);assert e.location()==(43,4,7,41)
 for _ in range(3):
  go(e,(6,41));party_before=preserved(e);e.press('UP');e.press('A',180);assert e.read('sLockFieldControls',1)
  e.frames(120)
  e.screenshot(ROOT/'test-output/paris-garden-observer.png')
  e.finish_dialogue();assert not e.read('sLockFieldControls',1)
  assert preserved(e)==party_before
  greet(e);assert preserved(e)[1:]==before
 for p in [(4,42),(13,42),(13,36),(9,37),(26,38),(33,38)]:go(e,p)
 go(e,(7,41));save(e,'paris-garden-companion-save');saved=preserved(e)
 e.screenshot(ROOT/'test-output/paris-garden-companion-courtyard.png')
 print('PASS: old Paris garden save, companion collision and three greetings preserve party/inventory/progress and promenade routes',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'paris-garden-companion-save',True)
 assert e.location()==(43,4,7,41) and preserved(e)==saved
 greet(e);assert preserved(e)==saved
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,5)
 print('PASS: Paris companion Save/cold Continue, repeat greeting and countryside return',flush=True)
finally:e.close()
