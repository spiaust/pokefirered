from emulator import Emulator,ROOT
import hashlib
for key in ['START','A']:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  e.frames(600);assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_EuropeTitleRun']&~1
  assert e.read('sEuropeTitleMon',1)<64
  hashes=set();frame=e.read('sEuropeTitleFrame',2)
  for i in range(6):
   p=ROOT/f'test-output/release-title-{key}-{i}.png';e.screenshot(p);hashes.add(hashlib.sha256(p.read_bytes()).hexdigest());e.frames(240)
  assert len(hashes)==6 and e.read('sEuropeTitleFrame',2)>frame+1300,(len(hashes),frame,e.read('sEuropeTitleFrame',2))
  print('PASS: '+key+' boot shows Celebi and six changing native town scenes with a running animation',flush=True)
  e.press(key,240);assert e.read(e.symbols['gMain']+4)&~1==e.symbols['CB2_NewGameScene']&~1
  e.screenshot(ROOT/f'test-output/release-title-{key}-new-game.png')
  print('PASS: '+key+' exits the animated title into the native new-game flow',flush=True)
 finally:e.close()
