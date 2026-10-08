"""Old ROM inactive-contact batteries, repeated dialogue and Save/Continue."""
import sys
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_tour import travel
from test_time import preserved
CASES=[('Oxford',3,3),('Chantilly',4,2),('Oranienburg',5,3)]
def talk(e,city,pages,label):
 before=preserved(e);e.press('DOWN');e.press('A',900)
 for page in range(pages):
  assert e.read('sLockFieldControls',1) and not e.in_battle()
  e.screenshot(ROOT/f'test-output/quest-contact-{city}-{label}-{page}.png')
  if page<pages-1:e.press('A',900)
 e.finish_dialogue()
 assert not e.read('sLockFieldControls',1) and preserved(e)==before
 assert [e.var(v) for v in [0x40FB,0x40FD,0x40FF]]==[0,0,0]
for city,index,pages in CASES:
 prepare='--prepare' in sys.argv
 e=Emulator(ROOT/('artifacts/releases/Pokemon-European-Tour-v1.13.gba' if prepare else 'pokefirered.gba'))
 try:
  if prepare:
   load_checkpoint(e,'start-england',True);go(e,(16,14));travel(e,index);go(e,(10,14))
   save(e,'quest-contact-'+city+'-v113');print('Prepared genuine v1.13 inactive-contact battery: '+city,flush=True);continue
  load_checkpoint(e,'quest-contact-'+city+'-v113',True);assert e.location()==(43,index*4,10,14)
  talk(e,city,pages,'old-save');talk(e,city,pages,'repeat')
  save(e,'quest-contact-'+city);saved=preserved(e)
  print('PASS: '+city+' old battery repeats inactive-contact directions without quest acceptance, battles, rewards or progress changes',flush=True)
 finally:e.close()
 if not prepare:
  e=Emulator(ROOT/'pokefirered.gba')
  try:
   load_checkpoint(e,'quest-contact-'+city,True);assert preserved(e)==saved and e.location()==(43,index*4,10,14)
   talk(e,city,pages,'continued');go(e,(23,10));e.walk('UP',1);e.frames(180)
   assert e.location()==(43,index*4+2,4,8)
   print('PASS: '+city+' cold Continue retains exact state, repeats directions and enters station normally',flush=True)
  finally:e.close()
