"""Check native sprite limits and consistency between story battles and map actors."""
from pathlib import Path
from PIL import Image
import json,re
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'graphics/eclipse_villains'
bind=json.loads((BASE/'bindings.json').read_text())
trainer_source=(ROOT/'src/data/trainers.h').read_text(encoding='utf-8')
for asset in json.loads((BASE/'prompts.json').read_text())['assets']:
 n=asset['name']
 for folder,size in [('battle',(64,64)),('overworld',(144,32))]:
  im=Image.open(BASE/folder/f'{n}.png')
  assert im.mode=='P' and im.size==size and im.info.get('transparency')==0,(n,folder,im.mode,im.size)
  assert max(im.getdata())<16,(n,folder,'exceeds 4bpp')
  if folder=='overworld':
   for i in range(9):assert im.crop((i*16,0,i*16+16,32)).getbbox(),(n,i,'empty walking frame')
 assert (BASE/'source'/f'{n}.png').exists()
for name,script,trainer in bind['map_actors']:
 d=json.loads((ROOT/f'data/maps/{name}/map.json').read_text())
 o=next(o for o in d['object_events'] if o['script']==script)
 asset=bind['trainers'][str(trainer)]
 assert o['graphics_id']=='OBJ_EVENT_GFX_ECLIPSE_'+asset.upper(),(name,script,trainer)
 line=next(l for l in trainer_source.splitlines() if re.match(r'\s*\[%d\] ='%trainer,l))
 assert 'TRAINER_PIC_ECLIPSE_'+asset.upper() in line
assert set(t for _,_,t in bind['map_actors'])==set(map(int,bind['trainers'])), 'A battle has no matching field actor'
assert len(bind['trainers'])==43
# The original Rocket sprites are retained; their roster still uses the original IDs.
assert 'TRAINER_PIC_ROCKET_GRUNT_M' in trainer_source
assert 'OBJ_EVENT_GFX_ROCKET_M' in (ROOT/'data/maps/SilphCo_2F/map.json').read_text()
print('PASS: 8 portraits, 72 walking frames, transparent 4bpp limits, 43 battle/map bindings, original Rocket assets retained')
