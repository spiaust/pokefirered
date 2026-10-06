"""Outfit palettes for both avatars, cycling, unchanged skin colors and cold saves."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item,start_action
from test_navigation import wait_task
from test_time import preserved
def who(e):
 p=e.read('gSaveBlock2Ptr');return bytes(e.read(p+i,1) for i in range(14))
def palette(e):return tuple(e.read(e.symbols['gPlttBufferUnfaded']+2*(256+i),2) for i in range(16))
def rgb(r,g,b):return r|(g<<5)|(b<<10)
def check(e,color,classic):
 p=palette(e);expected={1:(rgb(5,7,13),rgb(11,22,29),rgb(8,13,24)),2:(rgb(4,11,6),rgb(14,26,16),rgb(7,18,10))}[color]
 assert tuple(p[i] for i in (8,11,12))==expected,p
 assert all(p[i]==classic[i] for i in range(16) if i not in (8,11,12))
def options(e):open_key_item(e,363);wait_task(e,'Task_EuropeMap')
def close(e):
 e.press('B',180);e.press('B',180);e.press('B',90);assert not e.read('sLockFieldControls',1)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);assert e.var(0x40c4)==0
 loc=e.location();before=preserved(e);identity=who(e);classic=palette(e)
 options(e);e.press('DOWN',60);e.press('LEFT',60);assert e.var(0x40d3)==1
 for _ in range(3):e.press('DOWN',60)
 e.press('RIGHT',60);assert e.var(0x40c4)==1
 e.screenshot(ROOT/'test-output/world-outfit-menu.png');close(e);check(e,1,classic)
 assert e.read(e.symbols['gPlayerAvatar']+7,1)==0
 e.screenshot(ROOT/'test-output/world-outfit-blue-red.png')
 e.walk('LEFT',1);e.walk('RIGHT',1);check(e,1,classic)
 open_key_item(e,360);e.frames(120);assert e.read('gPlayerAvatar',1)&2;check(e,1,classic)
 e.screenshot(ROOT/'test-output/world-outfit-blue-bike.png')
 open_key_item(e,360);e.frames(120);assert not e.read('gPlayerAvatar',1)&2;check(e,1,classic)
 options(e);e.press('DOWN',60);e.press('RIGHT',60);assert e.var(0x40d3)==2
 for _ in range(3):e.press('DOWN',60)
 e.press('RIGHT',60);assert e.var(0x40c4)==2;close(e);check(e,2,classic)
 assert e.read(e.symbols['gPlayerAvatar']+7,1)==1
 e.screenshot(ROOT/'test-output/world-outfit-green-leaf.png')
 assert e.location()==loc and who(e)==identity and preserved(e)==before
 start_action(e,4)
 for _ in range(5):e.press('A',150)
 e.battery(ROOT/'test-output/world-outfit-save.sav');saved=preserved(e)
 print('PASS: Red blue and Leaf green outfits, unchanged non-clothing colors, cycling/dismount and trainer progress',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-outfit-save',True)
 assert e.var(0x40c4)==2 and e.var(0x40d3)==2 and preserved(e)==saved and who(e)==identity
 check(e,2,classic);e.screenshot(ROOT/'test-output/world-outfit-reloaded.png')
 options(e)
 for _ in range(4):e.press('DOWN',60)
 e.press('A',60);assert e.var(0x40c4)==0;close(e);assert palette(e)==classic
 assert preserved(e)==saved and e.location()==loc
 print('PASS: outfit cold Continue retains color and avatar; A wraps to the exact classic palette without changing progress',flush=True)
finally:e.close()
