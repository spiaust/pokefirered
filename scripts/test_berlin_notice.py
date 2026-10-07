"""Courtyard notice pages, old outdoor battery, cold Continue and visitor routes."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved

def read(e,label):
 go(e,(56,35));e.press('UP');before=preserved(e);e.press('A',900)
 for page in range(4):
  assert e.read('sLockFieldControls',1),(label,page)
  e.screenshot(ROOT/f'test-output/berlin-notice-{label}-{page}.png')
  if page<3:e.press('A',900)
 e.finish_dialogue();assert not e.read('sLockFieldControls',1) and preserved(e)==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'berlin-court-v098',True);assert e.location()==(43,8,54,37);before=preserved(e)[1:]
 read(e,'old-save');read(e,'repeat')
 for p in [(43,32),(51,32),(58,32),(60,40),(48,40),(56,35)]:go(e,p)
 assert preserved(e)[1:]==before
 save(e,'berlin-notice-save');saved=preserved(e)
 print('PASS: v0.98 courtyard battery reads all notice pages twice and retains visitor routes, inventory and progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'berlin-notice-save',True);assert e.location()==(43,8,56,35) and preserved(e)==saved
 read(e,'reloaded')
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,9)
 print('PASS: courtyard notice Save/cold Continue, repeated reading and countryside return',flush=True)
finally:e.close()
