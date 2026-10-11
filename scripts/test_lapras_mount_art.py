"""Dedicated mount frames survive native rental steering, water saves and exits."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel
from test_ride import ride,steps,dismount,SURF
from key_item_test_helpers import reload
from test_time import preserved
from build_lapras_mount import build

def mount(e):
 matches=[]
 for i in range(64):
  s=e.symbols['gSprites']+i*68
  if e.read(s+0x14)==e.symbols['gFieldEffectObjectTemplate_EuropeLaprasMount']:matches.append(s)
 assert len(matches)==1,matches
 assert e.read(matches[0]+0x0c)==e.symbols['sPicTable_EuropeLaprasMount']
 return matches[0]

asset=ROOT/'graphics/object_events/pics/misc/europe_lapras_mount.4bpp';before=asset.read_bytes();assert build()==before and len(before)==3072
print('PASS: six original native mount frames regenerate byte-exactly',flush=True)
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'current-riverboat-complete',True)
 for dest in (3,0):
  if e.location()[1]!=dest*4:go(e,(16,14));travel(e,dest)
  go(e,(26,16));before=preserved(e);ride(e);s=mount(e)
  assert preserved(e)==before
  steps(e,'LEFT',2);assert e.read(mount(e)+0x2a,1)==2
  e.screenshot(ROOT/f'test-output/lapras-mount-{dest}-west.png')
  steps(e,'RIGHT',2);assert e.read(mount(e)+0x2a,1)==3
  e.screenshot(ROOT/f'test-output/lapras-mount-{dest}-east.png')
  e=reload(e,f'lapras-mount-{dest}-water');assert e.read('gPlayerAvatar',1)&SURF;mount(e)
  dismount(e);assert not e.read('gPlayerAvatar',1)&SURF
  assert not any(e.read(e.symbols['gSprites']+i*68+0x14)==e.symbols['gFieldEffectObjectTemplate_EuropeLaprasMount'] and e.read(e.symbols['gSprites']+i*68+0x1c)&~1==e.symbols['UpdateSurfBlobFieldEffect']&~1 for i in range(64))
  e.screenshot(ROOT/f'test-output/lapras-mount-{dest}-dismount.png')
  print(f'PASS: town {dest} dedicated visible Lapras, left/right frames, native water Continue and clean dismount',flush=True)
finally:e.close()
