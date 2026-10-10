from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
import json
for label in ['mixed-map-pages','tour-approach-Oxford']:
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,label,True);go(e,(15,10));e.screenshot(ROOT/f'test-output/services-palette-{label}.png')
  print(label,e.location(),[hex(e.read(e.symbols['gPlttBufferUnfaded']+2*(32+i),2)) for i in range(16)],flush=True)
 finally:e.close()
