"""Old Paris battery, repeat sketcher greetings and normal Save/Continue."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved

def greet(e):
 go(e,(30,43));before=preserved(e);e.press('UP');e.press('A',180)
 assert e.read('sLockFieldControls',1)
 e.screenshot(ROOT/'test-output/paris-artist-dialogue.png')
 e.finish_dialogue();assert not e.read('sLockFieldControls',1) and preserved(e)==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'paris-realism-save',True);before=preserved(e)[1:]
 for _ in range(3):greet(e)
 go(e,(30,43));e.walk('UP',1);assert e.location()==(43,4,30,43)
 for p in [(33,38),(26,38),(13,42),(4,42)]:go(e,p)
 assert preserved(e)[1:]==before
 go(e,(30,43));e.screenshot(ROOT/'test-output/paris-artist-promenade.png');save(e,'paris-artist-save');saved=preserved(e)
 print('PASS: older Paris battery restores sketcher; repeated greetings and promenade routes preserve progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'paris-artist-save',True);assert e.location()==(43,4,30,43) and preserved(e)==saved
 greet(e);assert preserved(e)==saved
 go(e,(19,12));go(e,(15,0));e.walk('UP',1);e.frames(180);assert e.location()[:2]==(43,5)
 print('PASS: sketcher Save/cold Continue, repeat reading and countryside return',flush=True)
finally:e.close()
