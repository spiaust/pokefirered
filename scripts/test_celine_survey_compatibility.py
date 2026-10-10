"""Native unlocked survey, both site orders and earned reward after text update."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_country import wait_menu
from test_tour import travel,item_count
from test_france_story import gardens,forest,to_paris_from_gym,SURVEY,SEED
from test_time import preserved
from key_item_test_helpers import reload
def talk(e):
 go(e,(10,14));e.press('DOWN');e.press('A',900);e.finish_dialogue()
def offer(e,choice):
 e.press('DOWN');e.press('A',900);wait_menu(e,'Task_YesNoMenu_HandleInput');e.frames(60)
 if choice=='NO':e.press('DOWN')
 e.press('B' if choice=='B' else 'A',900);e.finish_dialogue()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'gym-complete',True);to_paris_from_gym(e);go(e,(10,14))
 assert e.var(SURVEY)==0
 before=preserved(e)
 for choice in ['NO','B']:offer(e,choice);assert preserved(e)==before
 e=reload(e,'celine-survey-offer');assert preserved(e)==before
 print('PASS: earned first badge unlocks Celine offer; No/B and native cold Continue retain unstarted survey',flush=True)
 offer(e,'YES');assert e.var(SURVEY)==1
 e=reload(e,'celine-survey-active');talk(e);assert e.var(SURVEY)==1
 print('PASS: normal acceptance and saved active directions retain unlocked survey without early reward',flush=True)
 for order in [('gardens','forest'),('forest','gardens')]:
  load_checkpoint(e,'celine-survey-active',True);label='-'.join(order)
  initial=item_count(e,SEED)
  for i,site in enumerate(order):
   dest=1 if site=='gardens' else 4;go(e,(16,14))
   if e.location()[1]!=dest*4:travel(e,dest)
   (gardens if site=='gardens' else forest)(e)
   assert e.var(SURVEY)==(4 if i else 2 if site=='gardens' else 3)
   if i==0:
    stage=e.var(SURVEY);go(e,(16,14))
    if dest!=4:travel(e,4)
    talk(e);go(e,(16,14));travel(e,1);talk(e)
    assert e.var(SURVEY)==stage and item_count(e,SEED)==initial
    e=reload(e,'celine-survey-'+label+'-first');assert e.var(SURVEY)==stage
    print(f'PASS: {label} first marker repeats safely; Remy/Celine retain missing-site gate and saved progress',flush=True)
  go(e,(16,14))
  if e.location()[1]!=4:travel(e,1)
  talk(e);assert e.var(SURVEY)==4 and item_count(e,SEED)==initial
  go(e,(16,14));travel(e,4);talk(e);assert e.var(SURVEY)==5
  talk(e);assert e.var(SURVEY)==5
  e=reload(e,'celine-survey-'+label+'-review');assert e.var(SURVEY)==5
  print(f'PASS: {label} both notes require Remy review; repeat and cold Continue retain reviewed report',flush=True)
  go(e,(16,14));travel(e,1);talk(e);assert e.var(SURVEY)==6 and item_count(e,SEED)==initial+1
  before=preserved(e);talk(e);assert preserved(e)==before
  e=reload(e,'celine-survey-'+label+'-reward');assert preserved(e)==before
  talk(e);assert preserved(e)==before
  print(f'PASS: {label} native Celine report grants exactly one Miracle Seed; repeat/cold Continue preserve completion',flush=True)
 load_checkpoint(e,'current-navigation-complete',True);go(e,(16,14));travel(e,1);go(e,(10,14))
 before=preserved(e);talk(e);e=reload(e,'celine-survey-completed-journey');talk(e);assert preserved(e)==before and e.var(SURVEY)==6
 print('PASS: completed historical journey Celine repeat/save retains all rewards and finished survey',flush=True)
finally:e.close()
