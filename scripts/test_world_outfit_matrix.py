"""All five colors on Red/Leaf through preview, walking, bicycle and cold saves."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved
from key_item_test_helpers import reload
def palette(e):return tuple(e.read(e.symbols['gPlttBufferUnfaded']+2*(256+i),2) for i in range(16))
def rgb(r,g,b):return r|(g<<5)|(b<<10)
COLORS={1:(rgb(5,7,13),rgb(11,22,29),rgb(8,13,24)),2:(rgb(4,11,6),rgb(14,26,16),rgb(7,18,10)),3:(rgb(10,4,14),rgb(25,15,29),rgb(18,8,23)),4:(rgb(12,7,2),rgb(31,26,8),rgb(24,15,3))}
def identity(e):
 p=e.read('gSaveBlock2Ptr');return bytes(e.read(p+i,1) for i in range(14))
def options(e):open_key_item(e,363);wait_task(e,'Task_EuropeMap')
def close(e):
 for _ in range(4):e.press('B',180)
 assert not e.read('sLockFieldControls',1) and e.read('sWorldPreviewSpriteId',1)==64
def check(e,color,classic):
 p=palette(e)
 if color==0:assert p==classic
 else:
  assert tuple(p[i] for i in (8,11,12))==COLORS[color]
  assert all(p[i]==classic[i] for i in range(16) if i not in (8,11,12))
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);original=preserved(e)[1:],identity(e),e.location()
 for avatar,label in [(1,'red'),(2,'leaf')]:
  options(e);e.press('DOWN',60)
  while e.var(0x40D3)!=avatar:e.press('RIGHT',60)
  for _ in range(3):e.press('DOWN',60)
  while e.var(0x40C4)!=0:e.press('RIGHT',60)
  close(e);classic=palette(e)
  for color,name in enumerate(['classic','blue','green','purple','gold']):
   options(e)
   for _ in range(4):e.press('DOWN',60)
   while e.var(0x40C4)!=color:e.press('RIGHT',60)
   check(e,color,classic);prefs=e.var(0x40D3),e.var(0x40C4)
   e.press('L',60);e.press('R',60);e.press('SELECT',60);assert e.read('sWorldPreviewBike',1)==1;check(e,color,classic)
   assert (e.var(0x40D3),e.var(0x40C4))==prefs
   e.screenshot(ROOT/f'test-output/outfit-matrix-{label}-{name}-preview.png');close(e);check(e,color,classic)
   e.walk('LEFT',1);e.walk('RIGHT',1);check(e,color,classic)
   open_key_item(e,360);e.frames(120);assert e.read('gPlayerAvatar',1)&2;check(e,color,classic)
   e.screenshot(ROOT/f'test-output/outfit-matrix-{label}-{name}-bike.png')
   open_key_item(e,360);e.frames(120);assert not e.read('gPlayerAvatar',1)&2;check(e,color,classic)
   assert (preserved(e)[1:],identity(e),e.location())==original
   before=preserved(e);e=reload(e,f'outfit-matrix-{label}-{name}');assert preserved(e)==before and (e.var(0x40D3),e.var(0x40C4))==prefs
   assert (preserved(e)[1:],identity(e),e.location())==original;check(e,color,classic)
   print(f'PASS: {label} {name} preview/rotation/bicycle/field/cold Continue retains colors, other palette entries, identity and journey',flush=True)
finally:e.close()
