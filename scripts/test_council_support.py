"""Prepare a balanced native party from the saved first Council victory."""
import sys
from council_support_test_helpers import *
country=sys.argv[sys.argv.index('--country')+1]
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'council-'+country+'-stage-1',True);assert council(e)==(1,0)
 if '--resume-training' in sys.argv:
  e.close();e=Emulator(ROOT/'pokefirered.gba');load_checkpoint(e,'council-'+country+'-support-training',True)
 else:
  e=capture_support(e);e=reload(e,'council-'+country+'-support-caught')
 e=train_support(e,country)
finally:e.close()
