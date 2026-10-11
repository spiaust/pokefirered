"""Independent first Council victory from each country's native stage-zero preparation."""
import sys
from council_test_helpers import *
from test_trainers import money
country=sys.argv[1]
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'council-'+country+'-prepared',True);h=history(e)
 assert council(e)==(0,0)
 nurse(e);stock(e);cash=money(e);begin(e,(2,4),753);battle(e)
 assert e.location()[:2]==(43,HALL) and council(e)==(1,0) and history(e)==h and money(e)>cash
 e=reload(e,'council-'+country+'-first-match-verified');assert council(e)==(1,0) and history(e)==h
 print('PASS: '+country+' native first Council victory and cold Save/Continue on final candidate',flush=True)
finally:e.close()
