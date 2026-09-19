from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_ride import steps,dismount,SURF,party

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'ride-london',True)
 assert e.location()==(43,0,26,19) and e.read('gPlayerAvatar',1)&SURF,e.location()
 before=party(e);dismount(e);assert party(e)==before
 print('PASS: old surfing battery retains London landing and safe shore dismount',flush=True)
finally:e.close()
