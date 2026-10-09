"""Follow real reviewed reports to capital hand-ins and return safely."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go
from test_tour import travel,item_count
from test_france_story import forest,talk,npc
from test_time import preserved
from test_tour_journal import inspect
from key_item_test_helpers import reload

def town(e,dest):
 go(e,(16,14))
 if e.location()[1]!=dest*4:travel(e,dest)

e=Emulator(ROOT/'pokefirered.gba')
try:
 for country,var,stage,reward,dest,branch,lead in [('France',0x40FD,5,205,1,4,12),('Germany',0x40FF,2,208,2,5,17)]:
  if country=='France':
   load_checkpoint(e,'quest-survey-gardens-forest-first',True);assert e.var(var)==2
   town(e,4);forest(e);assert e.var(var)==4
   go(e,(10,14));talk(e);assert e.var(var)==5
  else:load_checkpoint(e,'quest-courier-delivered',True)
  assert e.var(var)==stage and item_count(e,reward)==0
  before=preserved(e);npc(e);e.frames(900)
  for page in range(3):
   assert e.read('sLockFieldControls',1)
   e.screenshot(ROOT/f'test-output/quest-report-{country}-{page}.png');e.press('A',900)
  e.finish_dialogue();talk(e);assert preserved(e)==before
  e=reload(e,f'quest-report-{country}-ready');talk(e);inspect(e,lead,f'report-{country}-ready');assert preserved(e)==before
  print(f'PASS: {country} earned report reminder shows three pages, repeats and cold Continues read-only with correct journal and no premature item reward',flush=True)
  town(e,dest);go(e,(10,14));talk(e)
  assert e.var(var)==stage+1 and item_count(e,reward)==1
  claimed=preserved(e);talk(e);assert preserved(e)==claimed
  e=reload(e,f'quest-report-{country}-claimed');talk(e);inspect(e,lead+1,f'report-{country}-claimed');assert preserved(e)==claimed
  print(f'PASS: {country} east-station train reaches the named capital contact; actual report hand-in grants one reward and repeats/cold Continue duplicate nothing',flush=True)
  baseline=preserved(e)[1:];town(e,branch);go(e,(10,14));before=preserved(e);talk(e);assert preserved(e)==before
  e=reload(e,f'quest-report-{country}-returned');talk(e);assert preserved(e)==before and preserved(e)[1:]==baseline
  e.screenshot(ROOT/f'test-output/quest-report-{country}-returned.png')
  assert e.var(var)==stage+1 and item_count(e,reward)==1
  print(f'PASS: {country} normal return to the original report contact and another cold Continue retain completion and one reward; completed reminder remains read-only',flush=True)
finally:e.close()
