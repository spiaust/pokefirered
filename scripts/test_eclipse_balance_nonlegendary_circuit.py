"""Run earned champion rematches without legendaries or shared checkpoint overwrites."""
import sys
from emulator import ROOT
import test_eclipse_natural_circuit as circuit
from test_shadow_runtime import monfield
original_save=circuit.save;original_load=circuit.load_checkpoint;original_shelter=circuit.shelter
prefix='balance-nonlegendary-'
def save(e,name):return original_save(e,prefix+name)
def load(e,name,legacy=False):
 if name.startswith('natural-circuit'):name=prefix+name
 original_load(e,name,legacy)
 species=[monfield(e,i,0,0)&65535 for i in range(e.read('gPlayerPartyCount',1))]
 assert len(species)==6 and all(s in (31,159,160,131,17,18,26,229) for s in species),species
 print('Earned non-legendary party',[(s,e.read(e.symbols['gPlayerParty']+100*i+84,1)) for i,s in enumerate(species)],flush=True)
def shelter(e,name):
 from tm_teaching_test_helpers import field
 field(e)
 try:original_shelter(e,name)
 except AssertionError:
  e.screenshot(ROOT/'test-output/balance-circuit-navigation.png');e.state(ROOT/'test-output/balance-circuit-navigation.state')
  print('Navigation callback',hex(e.read(e.symbols['gMain']+4)),'locked',e.read('sLockFieldControls',1),flush=True)
  raise
circuit.save=save;circuit.load_checkpoint=load;circuit.shelter=shelter
if not any(x.startswith('--checkpoint=') for x in sys.argv):sys.argv.append('--checkpoint=natural-krakow-complete')
circuit.main()
