"""Fresh candidate-ending saves from all three countries unlock the Council."""
from council_test_helpers import *
from test_country import party_species
manifest=json.loads((ROOT/'.local-tools/council-validation/manifest.json').read_text())
for country in ('england','france','germany'):
 assert any(x['suite']==country+'-fresh' and x['exit_code']==0 for x in manifest)
 assert any(x['suite']==country+'-accounts' and x['exit_code']==0 for x in manifest)
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'release-'+country+'-all-accounts',True);h=history(e)
  assert e.var(0x40cc)==1 and e.var(0x40d5)==2 and council(e)==(0,0)
  assert e.var(0x40f0)==('england','france','germany').index(country)+1
  enter(e);assert council(e)==(0,0) and history(e)==h
  e=reload(e,'council-fresh-'+country+'-access');assert council(e)==(0,0) and history(e)==h
  print('PASS: fresh '+country+' candidate journey reaches Council reception/Hall and native Save/Continue with its main ending intact',flush=True)
 finally:e.close()
