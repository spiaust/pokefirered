"""Read saved partial-quest reminders at actual contacts without progression."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel,item_count
from test_france_story import talk,npc
from test_time import preserved
from test_tour_journal import inspect
from key_item_test_helpers import reload

e=Emulator(ROOT/'pokefirered.gba')
try:
 for first,stage,lead in [('gardens',2,9),('forest',3,10)]:
  source='quest-survey-'+('gardens-forest' if first=='gardens' else 'forest-gardens')+'-first'
  for dest,contact in [(1,'Celine'),(4,'Remy')]:
   load_checkpoint(e,source,True);go(e,(16,14))
   if e.location()[1]!=dest*4:travel(e,dest)
   go(e,(10,14));before=preserved(e)
   npc(e);e.frames(900)
   for page in range(3):
    assert e.read('sLockFieldControls',1)
    e.screenshot(ROOT/f'test-output/quest-reminder-{first}-{contact}-{page}.png');e.press('A',900)
   e.finish_dialogue();talk(e);assert preserved(e)==before
   e=reload(e,f'quest-reminder-{first}-{contact}');talk(e);inspect(e,lead,f'reminder-{first}-{contact}')
   assert preserved(e)==before and e.var(0x40FD)==stage and item_count(e,205)==0
   print(f'PASS: {first}-first {contact} reminder names the remaining observation; repeats/cold Continue and journal keep the single-site stage and grant no premature review or Miracle Seed',flush=True)
 for source,label,stage,lead,pages in [('quest-accepted-Germany','parcel',1,16,3),('quest-courier-delivered','report',2,17,2)]:
  load_checkpoint(e,source,True);assert e.location()[2:]==(10,14)
  before=preserved(e);npc(e);e.frames(900)
  for page in range(pages):
   assert e.read('sLockFieldControls',1)
   e.screenshot(ROOT/f'test-output/quest-reminder-{label}-{page}.png');e.press('A',900)
  e.finish_dialogue();talk(e);assert preserved(e)==before
  e=reload(e,f'quest-reminder-{label}');talk(e);inspect(e,lead,f'reminder-{label}')
  assert preserved(e)==before and e.var(0x40FF)==stage and item_count(e,208)==0
  print(f'PASS: German {label} reminder gives the correct destination and walking/train routes; repeats/cold Continue and journal preserve cargo/report stage without premature Magnet',flush=True)
finally:e.close()
