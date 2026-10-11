"""Five genuine Council victories from each country's earned main-ending save."""
import sys,json
from council_test_helpers import *
from test_country import party_species
from test_trainers import money
country=sys.argv[sys.argv.index('--country')+1] if '--country' in sys.argv else 'england'
e=Emulator(ROOT/'pokefirered.gba')
try:
 if '--resume-prepared' in sys.argv:
  load_checkpoint(e,'council-'+country+'-prepared',True);h=history(e);exit_hall(e);npc(e,(5,4));answer(e);e.finish_dialogue()
 else:baseline(e,country);h=history(e);enter(e)
 assert history(e)==h
 go(e,(10,4));before=preserved(e);npc(e,(10,4));e.finish_dialogue();assert council(e)==(0,0) and preserved(e)==before
 go(e,(10,7));before=preserved(e);npc(e,(10,7));e.finish_dialogue();assert preserved(e)==before
 for p in [(2,4),(6,7)]:
  for refusal in ('NO','B'):
   go(e,p);before=preserved(e);npc(e,p);answer(e,refusal);e.finish_dialogue();assert preserved(e)==before and council(e)==(0,0)
 print('PASS: '+country+' entry, rules, out-of-order Champion, Council and practice No/B declines',flush=True)
 e.screenshot(ROOT/f'test-output/council-{country}-hall.png')
 if '--resume-prepared' not in sys.argv:e=practice(e)
 nurse(e);e=reload(e,'council-'+country+'-prepared')
 assert history(e)==h and council(e)==(0,0);print('PASS: '+country+' repeated native practice, experience, evolution, free healing and cold Continue',flush=True)
 stock(e);assert history(e)==h;print('PASS: '+country+' native shop cancellation, twelve Super Potions and exact 8400 cost',flush=True)
 candy=item_count(e,68)
 for i,x in enumerate((2,4,6,8,10)):
  nurse(e);beforemoney=money(e);begin(e,(x,4),753+i)
  expected=((17,164,162),(12,70,188),(81,100,66),(54,61,116),(133,17,2,25))[i]
  actual=tuple(party_species(e,'gEnemyParty',j) for j in range(len(expected)));assert actual==expected,(actual,expected)
  e.screenshot(ROOT/f'test-output/council-{country}-match-{i+1}.png');battle(e)
  assert e.location()[:2]==(43,HALL) and council(e)==(i+1,2 if i==4 else 0),(i,e.location(),council(e))
  assert money(e)>beforemoney and history(e)==h
  expectedcandy=candy+(1 if i==4 else 0);assert item_count(e,68)==expectedcandy
  e=reload(e,f'council-{country}-stage-{i+1}');assert council(e)==(i+1,2 if i==4 else 0)
  before=preserved(e);npc(e,(x,4));e.finish_dialogue();assert preserved(e)==before and not e.in_battle()
  if i==0:
   exit_hall(e);go(e,(5,7));e.walk('DOWN',1);e.frames(180);assert e.location()==(43,0,55,33)
   e=reload(e,'council-'+country+'-paused');assert council(e)==(1,0);enter(e);assert council(e)==(1,0)
  print('PASS: '+country+f' match {i+1}, expected team, earned victory/prize, saved stage and no repeat reward',flush=True)
 go(e,(10,7));before=preserved(e)
 for refusal in ('NO','B'):
  npc(e,(10,7));answer(e,refusal);e.finish_dialogue();assert preserved(e)==before and council(e)==(5,2)
 e=reload(e,'council-'+country+'-champion');assert council(e)==(5,2) and history(e)==h
 if country=='england':
  npc(e,(10,7));answer(e);e.finish_dialogue();assert council(e)==(0,2)
  nurse(e);begin(e,(2,4),753);battle(e);assert council(e)==(1,2) and item_count(e,68)==candy+1
  e=reload(e,'council-england-replay-stage-1');assert council(e)==(1,2)
  print('PASS: replay restarts native trainer flags while retaining the permanent Champion title and single prize',flush=True)
 print('PASS: '+country+' championship conclusion, replay No/B, complete Save/Continue and unchanged main/archive/preferences',flush=True)
 result={'country':country,'completed_five_matches':True,'main_and_archive_unchanged':True,'native_practice':True,'champion_saved':True,'one_completion_candy':True}
 (ROOT/f'test-output/council-{country}-results.json').write_text(json.dumps(result,indent=2)+'\n')
finally:e.close()
