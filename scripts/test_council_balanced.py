"""Finish the Council with naturally caught/trained flying support."""
import sys,json
from council_test_helpers import *
from test_trainers import money
from test_country import party_species
country=sys.argv[sys.argv.index('--country')+1]
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'council-'+country+'-support-prepared',True);assert council(e)==(1,0) and e.read('gPlayerPartyCount',1)==2
 h=history(e);candy=item_count(e,68);assert party_species(e,index=1)==17
 for i,x in enumerate((4,6,8,10),1):
  nurse(e);cash=money(e);begin(e,(x,4),753+i)
  expected=((12,70,188),(81,100,66),(54,61,116),(133,17,2,25))[i-1]
  assert tuple(party_species(e,'gEnemyParty',j) for j in range(len(expected)))==expected
  e.screenshot(ROOT/f'test-output/council-{country}-balanced-match-{i+1}.png');battle(e)
  assert e.location()[:2]==(43,HALL) and council(e)==(i+1,2 if i==4 else 0),(i,e.location(),council(e))
  assert money(e)>cash and history(e)==h and item_count(e,68)==candy+(i==4)
  e=reload(e,'council-'+country+'-stage-'+str(i+1));assert council(e)==(i+1,2 if i==4 else 0)
  go(e,(x,4));before=preserved(e);npc(e,(x,4));e.finish_dialogue();assert preserved(e)==before
  print('PASS: '+country+f' balanced match {i+1}, native switching/healing, expected team, earned victory, saved stage and no repeated prize',flush=True)
 go(e,(10,7));before=preserved(e)
 for refusal in ('NO','B'):
  npc(e,(10,7));answer(e,refusal);e.finish_dialogue();assert preserved(e)==before and council(e)==(5,2)
 e=reload(e,'council-'+country+'-champion');assert council(e)==(5,2) and history(e)==h
 (ROOT/f'test-output/council-{country}-results.json').write_text(json.dumps({'country':country,'completed_five_matches':True,'native_support_capture_and_training':True,'main_and_archive_unchanged':True,'champion_saved':True,'one_completion_candy':True},indent=2)+'\n')
 print('PASS: '+country+' all five victories, permanent title, single prize, replay No/B and completed Save/Continue with main/archive progress intact',flush=True)
finally:e.close()
