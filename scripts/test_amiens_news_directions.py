"""Native Amiens bulletin reading, porter verification and Nora delivery."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_amiens_news import STORY,porter
from test_amiens import notice,leave,board
from test_reunion import talk,relocated
from test_time import preserved
from key_item_test_helpers import reload

def porter_pages(e,count,label):
 e.walk('RIGHT',8);e.walk('UP',3);before=preserved(e);e.press('UP');e.press('A',180);e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/news-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue();assert preserved(e)==before
 e.walk('DOWN',3);e.walk('LEFT',8)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'account-directions-news-active',True);assert e.var(STORY)==1 and e.var(0x40DF)==1
 porter_pages(e,2,'active');assert e.var(STORY)==1
 talk(e,'nora');assert e.var(STORY)==1
 e=reload(e,'news-directions-active');porter(e);assert e.var(STORY)==1
 print('PASS: two active bulletin pages locate northeast board and east-side porter; early Nora and cold Continue preserve unverified task',flush=True)
 notice(e);assert e.var(STORY)==2;notice(e);talk(e,'nora');assert e.var(STORY)==2
 e=reload(e,'news-directions-noted');assert e.var(STORY)==2
 porter_pages(e,4,'checked');assert e.var(STORY)==3
 e=reload(e,'news-directions-checked');porter(e);assert e.var(STORY)==3
 print('PASS: actual board reading retains porter-verification gate; four native verification/reminder pages locate Nora, and saved repeats retain checked news',flush=True)
 talk(e,'nora');assert e.var(STORY)==4 and e.var(0x40E0)==6 and e.var(0x40DF)==1
 e=reload(e,'news-directions-delivered');talk(e,'nora');relocated(e)
 for choice in ['B','NO']:leave(e,choice);assert e.var(STORY)==4
 leave(e);board(e);assert e.var(STORY)==4
 e=reload(e,'news-directions-returned');relocated(e);talk(e,'nora');assert e.var(STORY)==4
 print('PASS: native Nora delivery completes checked news; optional rest/return declines, actual station round trip and cold Continue retain completion and reunited Meowth',flush=True)
finally:e.close()
