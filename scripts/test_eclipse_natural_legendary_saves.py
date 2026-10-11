"""Cold-verify earned legendary captures against native data and saved actor flags."""
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from natural_capture_test_helpers import boxed_records
from test_eclipse_legendaries import D,flag,SPECIES
from test_oxford_gym import count_pocket
import json

def main():
 for row in D:
  name='natural-caught-'+row['species'].lower();e=Emulator(ROOT/'pokefirered.gba')
  try:
   load_checkpoint(e,name,True);species=SPECIES[row['species']]
   records=boxed_records(e,species);assert len(records)==1
   # All seven legendaries use the native Slow experience curve.
   assert records[0][2][0][1]==row['level']**3*5//4
   assert (records[0][2][3][0]>>27)&15 in (2,10),'unexpected catch Ball in boxed data'
   assert flag(e,int(row['flag'],16)) and e.read('gPlayerPartyCount',1)==6
   assert e.var(0x408C)==(21 if row['min_stage']==21 else 16)
   assert e.var(0x4090)==0 and e.var(0x4091)==0
   m=json.loads((ROOT/f"data/maps/{row['map']}/map.json").read_text())
   lid=next(i+1 for i,o in enumerate(m['object_events']) if o['script']=='EclipseLegendary_'+row['species'])
   assert not any(e.read(e.symbols['gObjectEvents']+36*i,1)&1 and e.read(e.symbols['gObjectEvents']+36*i+8,1)==lid for i in range(16))
   assert count_pocket(e,1,0x430,13)==0,'natural captures used an unearned Master Ball'
   print('PASS: cold earned',row['species'],'exact level/experience, PC data, completed stage and absent actor.',flush=True)
  finally:e.close()
if __name__=='__main__':main()
