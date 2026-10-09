from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_country import party_species
from test_oxford_gym import count_pocket
e=Emulator(ROOT/'pokefirered.gba')
try:
 for name in ['gym-defeat-Oxford-retry-won','gym-defeat-Chantilly-retry-won','gym-defeat-Oranienburg-retry-won','walkthrough-germany-complete','walkthrough-france-complete','walkthrough-complete']:
  if not (ROOT/f'test-output/{name}.sav').exists():continue
  load_checkpoint(e,name,True)
  print(name,[party_species(e,index=i) for i in range(e.read('gPlayerPartyCount',1))], [count_pocket(e,t,0x464,58) for t in [327,291,322]],flush=True)
finally:e.close()
