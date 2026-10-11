"""Independent skin/accent palettes, menu scrolling, preview, bike and native saves."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_gym_ui import open_key_item
from test_navigation import wait_task
from test_time import preserved
from key_item_test_helpers import reload
from walking_test_helpers import assert_walk_preserved

def rgb(r,g,b):return r|(g<<5)|(b<<10)
SKIN=[None,(rgb(31,26,22),rgb(25,18,15)),(rgb(28,20,13),rgb(22,13,9)),(rgb(21,13,8),rgb(14,8,5)),(rgb(13,8,6),rgb(8,4,3))]
ACCENT=[None,(rgb(11,22,29),rgb(8,13,24)),(rgb(14,26,16),rgb(7,18,10)),(rgb(25,15,29),rgb(18,8,23)),(rgb(31,26,8),rgb(24,15,3))]
def palette(e):return tuple(e.read(e.symbols['gPlttBufferUnfaded']+2*(256+i),2) for i in range(16))
def identity(e):
 p=e.read('gSaveBlock2Ptr');return bytes(e.read(p+i,1) for i in range(14))
def options(e,row):
 open_key_item(e,363);wait_task(e,'Task_EuropeMap')
 for _ in range(row):e.press('DOWN',60)
def close(e):
 for _ in range(4):e.press('B',180)
 assert not e.read('sLockFieldControls',1)
def set_value(e,var,value):
 for _ in range(5):
  if e.var(var)==value:return
  e.press('RIGHT',60)
 assert e.var(var)==value

def check(e,skin,accent,classic):
 expected=list(classic)
 if skin:expected[2],expected[3]=SKIN[skin]
 if accent:expected[13],expected[14]=ACCENT[accent]
 assert palette(e)==tuple(expected),(skin,accent,palette(e),expected)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'world-options-custom',True);who=identity(e);loc=e.location()
 for avatar in (1,2):
  options(e,1);set_value(e,0x40d3,avatar);close(e)
  options(e,6);set_value(e,0x40c6,0);e.press('DOWN',60);set_value(e,0x40c7,0);close(e)
  classic=palette(e);before=preserved(e)
  for skin in range(5):
   options(e,6);set_value(e,0x40c6,skin)
   e.press('DOWN',60)
   for accent in range(5):
    set_value(e,0x40c7,accent);check(e,skin,accent,classic)
   close(e)
  assert preserved(e)==before and identity(e)==who and e.location()==loc
  print(f'PASS: avatar {avatar} all 25 skin/accent pairs preserve clothing, hair, transparency and unrelated palette entries',flush=True)
  for skin in range(1,5):
   accent=5-skin
   options(e,6);set_value(e,0x40c6,skin);e.press('DOWN',60);set_value(e,0x40c7,accent)
   for key in ('L','R','R','R','SELECT'):e.press(key,60);check(e,skin,accent,classic)
   e.screenshot(ROOT/f'test-output/custom-avatar-{avatar}-skin-{skin}-preview.png');close(e)
   check(e,skin,accent,classic);before=preserved(e)
   e.walk('LEFT',1);e.walk('RIGHT',1);assert_walk_preserved(before,preserved(e));check(e,skin,accent,classic)
   open_key_item(e,360);e.frames(120);assert e.read('gPlayerAvatar',1)&2;check(e,skin,accent,classic)
   e.screenshot(ROOT/f'test-output/custom-avatar-{avatar}-skin-{skin}-bike.png')
   e=reload(e,f'custom-avatar-{avatar}-skin-{skin}')
   assert e.read('gPlayerAvatar',1)&2 and e.var(0x40c6)==skin and e.var(0x40c7)==accent
   check(e,skin,accent,classic);assert identity(e)==who and e.location()==loc
   open_key_item(e,360);e.frames(120);assert not e.read('gPlayerAvatar',1)&2;check(e,skin,accent,classic)
   print(f'PASS: avatar {avatar} skin {skin}/accent {accent} rotation, Walk/Bike preview, walking, mount/dismount and cold Continue',flush=True)
 options(e,8);e.press('A',60);e.press('B',60);assert e.var(0x40c6)==4 and e.var(0x40c7)==1
 e.press('A',60);e.press('A',60);close(e)
 assert e.var(0x40c6)==e.var(0x40c7)==0
 e=reload(e,'custom-defaults');assert e.var(0x40c6)==e.var(0x40c7)==0 and identity(e)==who and e.location()==loc
 print('PASS: scrolling Restore Defaults cancellation and confirmed native reset retain identity and journey',flush=True)
finally:e.close()
