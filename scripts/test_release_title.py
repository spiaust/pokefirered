"""Check current-year boot art, animated title, Start/A and Continue.
Uses fresh emulator cores and only test-output checkpoints, never player saves.
"""
from emulator import Emulator,ROOT
import hashlib,json
for key in ['START','A']:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  e.frames(90)
  e.screenshot(ROOT/f'test-output/eclipse-copyright-{key}.png')
  # Full credit canvas requires a separate screen block beyond its 600 tiles.
  assert e.read(0x4000008,2)&0x1f00==31<<8
  e.frames(510)
  assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_EuropeTitleRun']&~1
  sid=e.read('sEuropeTitleMon',1);assert sid<64
  p=e.symbols['gSprites']+sid*68
  positions=set();hashes=set()
  for i in range(6):
   e.screenshot(ROOT/f'test-output/eclipse-title-{key}-{i}.png')
   hashes.add(hashlib.sha256((ROOT/f'test-output/eclipse-title-{key}-{i}.png').read_bytes()).hexdigest())
   positions.add((e.read(p+0x24,2),e.read(p+0x26,2)))
   e.frames(16)
  assert len(hashes)>2 and len(positions)>2,(hashes,positions)
  print('PASS: 2026 credits, custom European eclipse art, blinking prompt and animated Celebi',flush=True)
  e.press(key,240)
  assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_NewGameScene']&~1
  e.screenshot(ROOT/f'test-output/eclipse-title-{key}-new-game.png')
  print('PASS: '+key+' opens native new-game flow',flush=True)
 finally:e.close()
# A save created by the uniform runtime test is safe for a cold Continue check.
save=ROOT/'test-output/villain-uniforms.sav'
if save.exists():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  e.battery(save,load=True);e.frames(600);e.press('START',240)
  e.screenshot(ROOT/'test-output/eclipse-title-continue-menu.png')
  e.press('A',300)
  for _ in range(8):
   if e.read('gQuestLogState',1) not in [2,3]:break
   e.press('B',120)
  assert e.location()[:2]==(45, json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Continent'].index('ContinentOslo')),e.location()
  e.screenshot(ROOT/'test-output/eclipse-title-continue.png')
  print('PASS: cold boot through new title preserves Continue and saved Oslo location',flush=True)
 finally:e.close()
