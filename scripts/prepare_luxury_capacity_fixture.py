"""Explicit capped Luxury Ball fixture; genuine message account untouched."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint,return_to_ada,report
from test_time import cross,preserved
from test_landmark_cases import save
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'message-directions-account',True);assert e.var(0x40E4)==3
 cross(e);return_to_ada(e);before=preserved(e)
 p=e.read('gSaveBlock1Ptr')+0x430;k=e.read(e.read('gSaveBlock2Ptr')+0xF20,2)
 for i in range(13):
  item,qty=(11,999) if i==0 else (0,0)
  e.write(p+4*i,item,2);e.write(p+4*i+2,qty^k,2)
 after=preserved(e);assert after[:3]==before[:3] and after[4:]==before[4:] and after[3][:72]==before[3][:72] and after[3][85:]==before[3][85:]
 report(e);assert preserved(e)==after and e.var(0x40E4)==3
 save(e,'quest-capacity-Luxury-capped-fixture')
 print('FIXTURE: only 13 Poke Balls slots arranged as Luxury Ball 999; genuine account, all other pockets, party, money and badges unchanged',flush=True)
finally:e.close()
