from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_ride import dismount,party,SURF
from test_ferry import sail

e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'ride-oxford',True)
 assert e.location()==(43,12,26,19) and e.read('gPlayerAvatar',1)&SURF
 before=party(e);dismount(e);assert party(e)==before
 print('PASS: old Oxford surfing battery and shore dismount',flush=True)
finally:e.close()
e=Emulator(ROOT/'pokefirered.gba')
try:
 load_checkpoint(e,'ferry-oxford',True)
 sail(e,0);sail(e,12)
 print('PASS: old Oxford landing save, London riverboat round trip and preserved booking/party',flush=True)
finally:e.close()
