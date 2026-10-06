"""Courtyard companion interaction and save continuity through native input."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved

def greet(e):
 go(e,(54,37));e.press('UP');e.press('A',180)
 assert e.read('sLockFieldControls',1)
 e.screenshot(ROOT/'test-output/berlin-companion-dialogue.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'berlin-realism-save',True);before=preserved(e)
 go(e,(54,37));e.walk('UP',1);assert e.location()==(43,8,54,37)
 for _ in range(3):greet(e);assert preserved(e)==before
 for p in [(48,33),(43,32),(51,32),(58,32),(60,40),(48,40)]:go(e,p)
 go(e,(54,37));save(e,'berlin-companion-save');saved=preserved(e)
 e.screenshot(ROOT/'test-output/berlin-companion-courtyard.png')
 print('PASS: old courtyard save, companion collision and three greetings preserve party/inventory/progress and visitor lanes',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'berlin-companion-save',True)
 assert e.location()==(43,8,54,37) and preserved(e)==saved
 greet(e);assert preserved(e)==saved
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,9)
 print('PASS: courtyard companion Save/cold Continue, repeat greeting and countryside return',flush=True)
finally:e.close()
