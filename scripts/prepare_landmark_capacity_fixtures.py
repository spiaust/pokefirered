"""Explicit isolated pocket edits; native resolved case stages are untouched."""
import json,re
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,talk,save
from test_time import preserved
from landmark_capacity_test_helpers import CASES
ids={m[1]:int(m[2]) for m in re.finditer(r'^#define\s+(ITEM_\w+)\s+(\d+)\s*$',(ROOT/'include/constants/items.h').read_text(),re.M)}
items=json.loads((ROOT/'src/data/items.json').read_text())['items']
e=Emulator(ROOT/'pokefirered.gba')
try:
 for label,tag,var,reward,qty,pocket,mode in CASES:
  load_checkpoint(e,'current-landmarks-'+tag+'-resolved',True);assert e.var(var)==5;go(e,(8,15));before=preserved(e)
  offset,slots=(0x310,42) if pocket==0 else (0x430,13)
  fill=[ids[x['itemId']] for x in items if x['pocket']=='POCKET_ITEMS' and x['english']!='????????' and x['itemId'] in ids and ids[x['itemId']] not in (0,reward)][:42]
  if mode=='full':assert len(fill)==len(set(fill))==42 and fill[0]==13
  arranged=[(x,1) for x in fill] if mode=='full' else [(reward,999)]+[(0,0)]*(slots-1)
  base=e.read('gSaveBlock1Ptr')+offset;k=e.read(e.read('gSaveBlock2Ptr')+0xF20,2)
  for i,(item,n) in enumerate(arranged):e.write(base+4*i,item,2);e.write(base+4*i+2,n^k,2)
  after=preserved(e);assert after[:3]==before[:3] and after[4:]==before[4:]
  start,end=(0,42) if pocket==0 else (72,85)
  assert after[3][:start]==before[3][:start] and after[3][end:]==before[3][end:]
  talk(e,(8,15));assert preserved(e)==after and e.var(var)==5
  save(e,'landmark-capacity-'+label+'-fixture')
  print('FIXTURE: '+label+': only specified inventory pocket arranged; native resolved case, party, other pockets, money and progression unchanged',flush=True)
finally:e.close()
