from council_test_helpers import *
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'council-france-stage-4',True);nurse(e);begin(e,(10,4),757);battle(e,trace=True,limit=500)
 print('END',e.location(),council(e),flush=True)
finally:e.close()
