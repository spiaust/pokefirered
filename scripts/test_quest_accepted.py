"""Follow accepted survey/courier directions without injected progress."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_country import wait_menu
from test_landmark_cases import go
from test_tour import travel,item_count
from test_france_story import talk,npc,gardens,forest
from test_time import preserved
from test_tour_journal import inspect
from key_item_test_helpers import reload

def accepted(e,country,var,pages):
 npc(e);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60);e.press('A',180);e.frames(900)
 for page in range(pages):
  assert e.read('sLockFieldControls',1)
  e.screenshot(ROOT/f'test-output/quest-accepted-{country}-{page}.png');e.press('A',900)
 e.finish_dialogue();assert e.var(var)==1
 before=preserved(e);talk(e);assert preserved(e)==before

def town(e,dest):
 go(e,(16,14))
 if e.location()[1]!=dest*4:travel(e,dest)

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'gym-onward-Oxford-contact',True);assert e.var(0x40FD)==0
 accepted(e,'France',0x40FD,5);e=reload(e,'quest-accepted-France');inspect(e,8,'accepted-France')
 print('PASS: normal French survey acceptance shows five pages, repeats safely and cold Continues with journal pointing to both habitats',flush=True)
 for order in [('gardens','forest'),('forest','gardens')]:
  load_checkpoint(e,'quest-accepted-France',True)
  first,second=order;label='-'.join(order)
  town(e,1 if first=='gardens' else 4);(gardens if first=='gardens' else forest)(e)
  stage=2 if first=='gardens' else 3;assert e.var(0x40FD)==stage
  e=reload(e,f'quest-survey-{label}-first');inspect(e,9 if first=='gardens' else 10,f'accepted-{label}-first')
  for dest in [1,4]:
   town(e,dest);go(e,(10,14));before=preserved(e);talk(e);assert preserved(e)==before
  assert e.var(0x40FD)==stage and item_count(e,205)==0
  print(f'PASS: survey {label}: normal north/south paths reach the first west-side study marker; repeat/cold Continue record only that site and both contacts withhold review/reward',flush=True)
  town(e,1 if second=='gardens' else 4);(gardens if second=='gardens' else forest)(e);assert e.var(0x40FD)==4
  town(e,1);go(e,(10,14));talk(e);assert e.var(0x40FD)==4 and item_count(e,205)==0
  town(e,4);go(e,(10,14));talk(e);assert e.var(0x40FD)==5
  before=preserved(e);talk(e);assert preserved(e)==before
  town(e,1);go(e,(10,14));talk(e);assert e.var(0x40FD)==6 and item_count(e,205)==1
  before=preserved(e);talk(e);assert preserved(e)==before
  e=reload(e,f'quest-survey-{label}-complete');inspect(e,13,f'accepted-{label}-complete');assert preserved(e)==before
  print(f'PASS: survey {label}: second observation, actual Remy review and Celine hand-in award one Miracle Seed; repeats/cold Continue preserve completion and journal names Chantilly Gym',flush=True)
 load_checkpoint(e,'gym-onward-Chantilly-contact',True);assert e.var(0x40FF)==0
 accepted(e,'Germany',0x40FF,4);e=reload(e,'quest-accepted-Germany');inspect(e,16,'accepted-Germany')
 print('PASS: normal German delivery acceptance shows four pages, repeats safely and cold Continues with parcel tracked outside the Bag and journal naming Karl',flush=True)
 town(e,5);go(e,(10,14));talk(e);assert e.var(0x40FF)==2 and item_count(e,208)==0
 before=preserved(e);talk(e);assert preserved(e)==before
 e=reload(e,'quest-courier-delivered');inspect(e,17,'accepted-Germany-delivered');assert preserved(e)==before
 print('PASS: normal east-station train reaches Karl west of Oranienburg guide; actual delivery records report once and cold Continue keeps journal on returning to Lena',flush=True)
 go(e,(15,23));e.walk('DOWN',1);assert e.location()==(43,21,15,0)
 e.walk('DOWN',40);assert e.location()==(43,9,15,0)
 e.walk('DOWN',24);assert e.location()==(43,8,15,0)
 go(e,(10,14));talk(e);assert e.var(0x40FF)==3 and item_count(e,208)==1
 before=preserved(e);talk(e);assert preserved(e)==before
 e=reload(e,'quest-courier-complete');inspect(e,18,'accepted-Germany-complete');assert preserved(e)==before
 print('PASS: normal Havel Trail/German Woodland southward walk returns Karl report to Lena for one Magnet; repeats/cold Continue preserve completion and journal names Oranienburg Gym',flush=True)
finally:
 e.screenshot(ROOT/'test-output/quest-accepted-final.png');e.close()
