"""A full second circuit retains the earned Champion title and single prize."""
from council_test_helpers import *
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'council-england-replay-stage-1',True);assert council(e)==(1,2);h=history(e);candy=item_count(e,68);stock(e)
 for i,x in enumerate((4,6,8,10),1):
  nurse(e);begin(e,(x,4),753+i);battle(e);assert e.location()[:2]==(43,HALL) and council(e)==(i+1,2)
  assert item_count(e,68)==candy and history(e)==h
  e=reload(e,'council-replay-stage-'+str(i+1));assert council(e)==(i+1,2)
 print('PASS: entire second five-match circuit, repeated Champion victory and native cold saves retain permanent title without another championship candy',flush=True)
finally:e.close()
