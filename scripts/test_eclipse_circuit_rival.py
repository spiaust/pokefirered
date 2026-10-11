"""Native rematch ace for all nine starting species and all difficulties."""
from test_eclipse_circuit import *


def main():
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,'eclipse-finished',True);e.write('sWildEncountersDisabled',1,1)
  var(e,0x40bf,13);before=ROOT/'test-output/circuit-rival-ready.state';e.state(before)
  row=D['trainers'][-1]
  for starter in COUNTERS:
   for mode,delta in ((1,-4),(0,0),(2,5)):
    e.state(before,True);var(e,0x40f6,SPECIES['SPECIES_'+starter]);var(e,0x4090,mode)
    battle_start(e,(6,4));check_team(e,row,delta)
   print('PASS:',starter,'fully evolved counter-starter, curated ace moves, Lum Berry and three difficulty levels.',flush=True)
 finally:e.close()

if __name__=='__main__':main()
