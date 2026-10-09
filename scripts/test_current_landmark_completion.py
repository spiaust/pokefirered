"""All three optional cases on one genuine post-ending player journey."""
from collections import Counter
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,researcher
from test_landmark_cases import DATA,go,talk
from test_tour import travel
from test_time import preserved
from key_item_test_helpers import reload
from test_journal import inspect
from test_journal_pages import inspect_pages

def count(e,item):return sum(q for i,q in preserved(e)[3] if i==item)
def bag_counts(e):return Counter({i:count(e,i) for i,q in preserved(e)[3] if i and q})
def pages(e,n,label):
 e.frames(900)
 for i in range(n):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/current-landmarks-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'current-ending-revisited',True)
 assert e.var(0x40D5)==2 and all(e.var(v)==0 for v in [0x40C0,0x40C1,0x40C2])
 historical=tuple(e.var(v) for v in range(0x40D5,0x4100))
 for row,reward,qty in zip(DATA,[213,68,3],[1,1,3]):
  tag,city,country,index,inside,door,var,selection=row;name='current-landmarks-'+tag.lower()
  go(e,(16,14));travel(e,selection);go(e,door)
  for choice in ['B','NO']:talk(e,door,choice=choice);assert e.var(var)==0 and e.location()[1]==index
  talk(e,door,choice='YES');assert e.location()==(43,inside,10,15)
  talk(e,(10,5));assert e.var(var)==0
  for choice in ['B','NO']:talk(e,(8,15),choice=choice);assert e.var(var)==0
  talk(e,(8,15),choice='YES');assert e.var(var)==1
  e=reload(e,name+'-active')
  for first,second,stage,label in [((4,6),(15,8),2,'forward'),((15,8),(4,6),3,'reverse')]:
   if label=='reverse':
    e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,name+'-active',True)
   talk(e,first);talk(e,first);assert e.var(var)==stage
   talk(e,(10,5));assert e.var(var)==stage
   e=reload(e,name+'-'+label+'-one');talk(e,second);assert e.var(var)==4
   e=reload(e,name+'-'+label+'-both')
  print('PASS: '+tag+' native entry/request No/B, both clue orders, repeated clues, early-attendant gates and cold Continue retain normally earned evidence',flush=True)
  for choice in ['B','NO']:talk(e,(10,5),choice=choice);assert e.var(var)==4
  talk(e,(10,5),choice='YES');assert e.var(var)==5;e=reload(e,name+'-resolved')
  go(e,(8,15));before=preserved(e);items=bag_counts(e);n=count(e,reward)
  talk(e,(8,15));assert e.var(var)==6 and count(e,reward)==n+qty
  expected=items.copy();expected[reward]+=qty;assert bag_counts(e)==expected
  assert preserved(e)[:3]==before[:3] and preserved(e)[4:]==before[4:]
  e=reload(e,name+'-complete')
  for point,direction in [((8,15),'UP'),((12,14),'DOWN')]:
   go(e,point);before=preserved(e);talk(e,point,direction);assert preserved(e)==before
  assert tuple(e.var(v) for v in range(0x40D5,0x4100))==historical
  go(e,(10,15));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,index,*door)
  talk(e,door,choice='YES');assert e.var(var)==6;go(e,(10,15));e.walk('DOWN',1);e.frames(180)
  print('PASS: '+tag+' native peaceful resolution and saved reward grant exactly '+str(qty)+' item(s); repeated curator/ledger, exit and re-entry preserve case and completed historical journey',flush=True)
 assert all(e.var(v)==6 for v in [0x40C0,0x40C1,0x40C2])
 talk(e,door,choice='YES');go(e,(8,15));before=preserved(e);e.press('UP');e.press('A',180);pages(e,6,'synthesis');assert preserved(e)==before
 talk(e,(12,14),'DOWN');go(e,(10,15));e.walk('DOWN',1);e.frames(180)
 go(e,(16,14));travel(e,3);go(e,(18,14));before=preserved(e);researcher(e);pages(e,9,'ada');assert preserved(e)==before
 inspect(e,58,1048575,'current-landmarks');inspect_pages(e,1048575,'current-landmarks')
 e=reload(e,'current-landmarks-all-complete');before=preserved(e);researcher(e);e.finish_dialogue();assert preserved(e)==before
 assert all(e.var(v)==6 for v in [0x40C0,0x40C1,0x40C2]) and tuple(e.var(v) for v in range(0x40D5,0x4100))==historical
 print('PASS: all three cases unlock shared synthesis at curator/ledger/Ada; final twenty-milestone journal and cold Continue preserve all cases, one-time rewards and historical ending',flush=True)
finally:e.close()
