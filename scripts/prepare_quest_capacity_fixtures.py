"""Explicit isolated Items-pocket edits; earned reports are never injected."""
import json,re
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_tour import travel
from test_france_story import talk
from test_time import preserved
from quest_capacity_test_helpers import CASES

ids={m[1]:int(m[2]) for m in re.finditer(r'^#define\s+(ITEM_\w+)\s+(\d+)\s*$',(ROOT/'include/constants/items.h').read_text(),re.M)}
items=json.loads((ROOT/'src/data/items.json').read_text())['items']
e=Emulator(ROOT/'pokefirered.gba')
try:
 for country,source,var,stage,reward,dest in CASES:
  for mode in ['full','capped']:
   load_checkpoint(e,source,True);assert e.var(var)==stage
   go(e,(16,14))
   if e.location()[1]!=dest*4:travel(e,dest)
   go(e,(10,14));before=preserved(e)
   fill=[ids[x['itemId']] for x in items if x['pocket']=='POCKET_ITEMS' and x['english']!='????????' and x['itemId'] in ids and ids[x['itemId']] not in (0,reward)][:42]
   assert len(fill)==len(set(fill))==42 and fill[0]==13
   slots=[(x,1) for x in fill] if mode=='full' else [(reward,999)]+[(0,0)]*41
   p=e.read('gSaveBlock1Ptr')+0x310;k=e.read(e.read('gSaveBlock2Ptr')+0xF20,2)
   for i,(item,qty) in enumerate(slots):e.write(p+4*i,item,2);e.write(p+4*i+2,qty^k,2)
   after=preserved(e);assert after[:3]==before[:3] and after[4:]==before[4:]
   talk(e);assert preserved(e)==after and e.var(var)==stage
   save(e,f'quest-capacity-{country}-{mode}-fixture')
   print(f'FIXTURE: {country} {mode}: only 42 Items slots arranged; genuine report, party, money and badges unchanged',flush=True)
finally:e.close()
