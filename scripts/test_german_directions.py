"""Old delivery-stage batteries and cold Continue direction reads."""
import sys
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import save,go
from test_time import preserved
CASES=[('active',8,1,3),('delivered',20,2,2)]
def read(e,stage,pages,label):
 before=preserved(e);e.press('DOWN');e.press('A',900)
 for page in range(pages):
  assert e.read('sLockFieldControls',1) and not e.in_battle()
  e.screenshot(ROOT/f'test-output/german-directions-{stage}-{label}-{page}.png')
  if page<pages-1:e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before and not e.read('sLockFieldControls',1)
for stage,index,value,pages in CASES:
 prepare='--prepare' in sys.argv
 e=Emulator(ROOT/('artifacts/releases/Pokemon-European-Tour-v1.14.gba' if prepare else 'pokefirered.gba'))
 try:
  load_checkpoint(e,'germany-'+stage if prepare else 'german-directions-'+stage+'-v114',True)
  assert e.location()==(43,index,10,14) and e.var(0x40FF)==value
  if prepare:
   save(e,'german-directions-'+stage+'-v114');print('Prepared genuine v1.14 '+stage+' delivery battery',flush=True);continue
  read(e,stage,pages,'old-save');read(e,stage,pages,'repeat')
  save(e,'german-directions-'+stage);saved=preserved(e)
  print('PASS: '+stage+' old delivery battery reads all direction pages twice with exact state and no rewards',flush=True)
 finally:e.close()
 if not prepare:
  e=Emulator(ROOT/'pokefirered.gba')
  try:
   load_checkpoint(e,'german-directions-'+stage,True);assert preserved(e)==saved and e.location()==(43,index,10,14)
   read(e,stage,pages,'continued');go(e,(23,10));e.walk('UP',1);e.frames(180)
   assert e.location()==(43,index+2,4,8) and e.var(0x40FF)==value
   print('PASS: '+stage+' cold Continue preserves exact state, repeats directions and enters station',flush=True)
  finally:e.close()
