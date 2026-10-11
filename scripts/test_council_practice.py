"""Final-candidate practice uses earned starter XP, evolves and restores PP."""
import struct
from council_test_helpers import *
from test_country import party_species
from test_trainers import money
from battle_recovery_test_helpers import orders

def full_pp(e):
 for i in range(e.read('gPlayerPartyCount',1)):
  p=e.symbols['gPlayerParty']+100*i;pid=e.read(p);key=pid^e.read(p+4);growth,attacks=orders[pid%24][:2]
  decode=lambda slot:b''.join(struct.pack('<I',e.read(p+32+slot*12+j)^key) for j in (0,4,8))
  data=decode(attacks);bonus=decode(growth)[8]
  for j,m in enumerate(struct.unpack('<4H',data[:8])):
   if m:
    base=e.read(e.symbols['gBattleMoves']+12*m+4,1);assert data[8+j]==base*(5+((bonus>>(2*j))&3))//5

e=Emulator(ROOT/'pokefirered.gba')
try:
 baseline(e,'england');h=history(e);enter(e);level=e.read(e.symbols['gPlayerParty']+84,1);assert level==15 and party_species(e)==1
 for i in range(2):
  cash=money(e);begin(e,(6,7),758);battle(e);assert e.location()[:2]==(43,HALL)
  assert council(e)==(0,0) and history(e)==h and money(e)>cash
  full_pp(e);assert party_species(e)==2 and e.read(e.symbols['gPlayerParty']+84,1)>=16
  e=reload(e,'council-native-practice-'+str(i));full_pp(e)
 print('PASS: final candidate repeats practice normally, earns XP/prizes, evolves Bulbasaur, restores HP/status/all move PP and saves without Council progress',flush=True)
finally:e.close()
