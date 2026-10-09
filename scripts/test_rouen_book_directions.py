"""Native route-book request, far-bank collection and return to Leon."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_rouen import leon,leave,board
from test_rouen_book import STORY,book,visible
from test_time import preserved
from key_item_test_helpers import reload
from test_country import wait_menu
from test_rouen_care import rest

def pages(e,count,label):
 e.frames(900)
 for i in range(count):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/book-directions-{label}-{i}.png');e.press('A',900)
 e.finish_dialogue()

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'rouen-directions-book-offer',True);assert e.var(STORY)==0
 book(e,False)
 for choice in ['B','NO']:leon(e,choice);assert e.var(STORY)==0
 e.walk('UP',1);e.walk('LEFT',4);e.walk('UP',6);before=preserved(e);e.press('UP');e.press('A',180)
 wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);pages(e,4,'search')
 assert e.var(STORY)==1 and preserved(e)==before
 e.walk('DOWN',6);e.walk('RIGHT',4);e.walk('DOWN',1)
 e=reload(e,'book-directions-active');leon(e);assert e.var(STORY)==1
 print('PASS: book absent before request; optional search No/B, actual acceptance and four route pages retain active request after cold Continue',flush=True)
 leave(e);board(e);e.walk('RIGHT',15);e.walk('UP',6);e.walk('RIGHT',8);e.walk('UP',4)
 assert e.location()==(43,34,33,6) and visible(e);before=preserved(e);e.press('LEFT');e.press('A',180)
 pages(e,3,'found');assert e.var(STORY)==2 and not visible(e) and preserved(e)==before
 e.walk('DOWN',4);e.walk('LEFT',21);e.walk('DOWN',6);e.walk('LEFT',2)
 e=reload(e,'book-directions-found');book(e,False);assert e.var(STORY)==2
 print('PASS: actual paved crossing and far-bank pickup show three return pages; exact inventory is preserved, and saved carrying state removes the book object',flush=True)
 leon(e);assert e.var(STORY)==3
 e=reload(e,'book-directions-returned');book(e,False)
 for choice in ['B','NO']:leon(e,choice);assert e.var(STORY)==3
 leave(e);board(e);e=reload(e,'book-directions-revisited');book(e,False);leon(e,'B');assert e.var(STORY)==3
 rest(e);e=reload(e,'book-directions-rested');rest(e)
 print('PASS: native Leon hand-in unlocks free care; rest No/B and actual Yes, Amiens round trip and cold Continue preserve completion and removed book',flush=True)
finally:e.close()
