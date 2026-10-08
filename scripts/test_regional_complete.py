"""Follow claimed regional rewards by train to both other guide towns."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_tour import guide,travel,item_count
from test_time import preserved
from key_item_test_helpers import reload

def complete(e,index,city,label):
 before=preserved(e);e.press('DOWN');e.press('A',900)
 for _ in range(3 if index==0 else 4):e.press('A',900)
 for page in range(4):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/regional-complete-{city}-{label}-{page}.png');e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before

e=Emulator(ROOT/'pokefirered.gba')
try:
 for index,city in enumerate(['Oxford','Chantilly','Oranienburg']):
  load_checkpoint(e,f'regional-guide-{city}-claimed',True)
  expected=tuple(int(i==index) for i in range(3));assert tuple(e.var(0x40F8+i) for i in range(3))==expected
  candy=item_count(e,68);complete(e,index,city,'first');guide(e)
  e=reload(e,f'regional-complete-{city}-start');complete(e,index,city,'continued')
  print(f'PASS: {city} claimed guide names other regional towns and east-side station; repeat and cold Continue preserve earned completion and Candy',flush=True)
  before=preserved(e)[1:]
  for destination in [i for i in range(3) if i!=index]:
   travel(e,destination+3);state=preserved(e);guide(e);assert preserved(e)==state
   e=reload(e,f'regional-complete-{city}-visit-{destination}')
   guide(e);assert preserved(e)==state
   assert tuple(e.var(0x40F8+i) for i in range(3))==expected and item_count(e,68)==candy and preserved(e)[1:]==before
  print(f'PASS: {city} normal east-station trains and required interchanges reach both other guide towns; visits and cold Continue award no unearned completion or Candy',flush=True)
  travel(e,index+3);complete(e,index,city,'returned');assert preserved(e)[1:]==before
  e=reload(e,f'regional-complete-{city}-returned');complete(e,index,city,'return-continued')
  assert tuple(e.var(0x40F8+i) for i in range(3))==expected and item_count(e,68)==candy
  print(f'PASS: {city} return train journey and another claimed-guide cold Continue retain rewards and progress without duplicates',flush=True)
finally:e.close()
