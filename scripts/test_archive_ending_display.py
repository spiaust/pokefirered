"""Capture every final chapter page and native Celebi portrait from earned notes."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,researcher
from test_landmark_cases import go
from test_tour import travel,item_count

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'archive-4-5-town-5',True);assert tuple(e.var(v) for v in range(0x40c8,0x40cc))==(1,1,1,1)
 go(e,(5,7));e.walk('DOWN',1);e.frames(180);go(e,(16,14));travel(e,3);go(e,(18,14))
 count=item_count(e,69);researcher(e);e.frames(900)
 for page in range(5):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/archive-ending-page-{page}.png');e.press('A',900)
 e.screenshot(ROOT/'test-output/archive-ending-celebi.png');e.finish_dialogue()
 assert e.var(0x40c8)==2 and item_count(e,69)==count+1
 print('PASS: five native conclusion pages, explicit Letters for Tomorrow completion, Celebi portrait and one PP UP',flush=True)
finally:e.close()
