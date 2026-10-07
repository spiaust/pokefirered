"""Old on-tile save escape, visible sign collision, repeated reads and cold Continue."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved

def marker(e):
 width=e.read('VMap');base=e.read(e.symbols['VMap']+8)
 assert e.read(base+2*((4+7)*width+14+7),2)==0x402

def read(e,label):
 go(e,(14,5));before=preserved(e);e.press('UP');assert e.location()==(43,8,14,5);e.press('A',900)
 for page in range(4):
  assert e.read('sLockFieldControls',1),(label,page)
  e.screenshot(ROOT/f'test-output/berlin-marker-{label}-{page}.png')
  if page<3:e.press('A',900)
 e.finish_dialogue();assert not e.read('sLockFieldControls',1) and preserved(e)==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'berlin-marker-v101',True);assert e.location()==(43,8,14,4);marker(e);before=preserved(e)[1:]
 e.screenshot(ROOT/'test-output/berlin-marker-legacy-on-tile.png')
 e.walk('DOWN',1);assert e.location()==(43,8,14,5)
 read(e,'old-save');read(e,'repeat')
 for p in [(15,5),(15,3),(14,3),(13,3),(13,5),(14,5)]:go(e,p)
 assert preserved(e)[1:]==before
 save(e,'berlin-marker-save');saved=preserved(e)
 print('PASS: v1.01 battery on the new sign retains position, steps off safely, reads twice and walks around it with progress retained',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'berlin-marker-save',True);assert e.location()==(43,8,14,5) and preserved(e)==saved;marker(e)
 read(e,'reloaded');go(e,(15,0));e.walk('UP',1);e.frames(180);assert e.location()==(43,9,15,23)
 e.walk('DOWN',1);e.frames(180);assert e.location()==(43,8,15,0);marker(e)
 print('PASS: visible northern marker Save/cold Continue, rereading and both countryside crossings',flush=True)
finally:e.close()
