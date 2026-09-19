"""Discard stale tree tiles cached in route battery saves without moving players."""
import json,struct
from emulator import Emulator,ROOT
from test_celebi import load_checkpoint
from test_landmark_cases import go,save
from test_time import preserved
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
layouts={v.get('id'):v for v in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
cases=[('start-england',1,'UP'),('start-france',5,'UP'),('start-germany',9,'UP'),('oxford-arrival',13,'DOWN'),('chantilly-arrival',17,'DOWN'),('oranienburg-arrival',21,'DOWN')]
for fixture,index,direction in cases:
 e=Emulator(ROOT/'pokefirered.gba');name='tree-refresh-'+str(index)
 try:
  load_checkpoint(e,fixture,True);go(e,(15,0 if direction=='UP' else 23));e.walk(direction,1);e.frames(180)
  assert e.location()[:2]==(43,index),e.location()
  m=json.loads((ROOT/f'data/maps/{groups[index]}/map.json').read_text());l=layouts[m['layout']];w,h=l['width'],l['height'];tiles=struct.unpack('<%dH'%(w*h),(ROOT/l['blockdata_filepath']).read_bytes())
  width=e.read('VMap');base=e.read(e.symbols['VMap']+8)
  # Simulate the repeated canopy/trunk data stored by an older running ROM.
  for y in range(h):
   for x in range(w):
    t=tiles[y*w+x]
    if t&0xc00:e.write(base+2*((y+7)*width+x+7),(t&~1023)|0x14,2)
  location=e.location();before=preserved(e);save(e,name)
 finally:e.close()
 e=Emulator(ROOT/'pokefirered.gba')
 try:
  load_checkpoint(e,name,True);assert e.location()==location and preserved(e)==before
  width=e.read('VMap');base=e.read(e.symbols['VMap']+8)
  assert tuple(e.read(base+2*((y+7)*width+x+7),2) for y in range(h) for x in range(w))==tiles
  e.walk(direction,6);assert e.location()[:2]==(43,index) and not e.in_battle()
  e.screenshot(ROOT/f'test-output/{name}.png')
  print(f'PASS: {groups[index]} cold Continue replaces stale tree cache and preserves player/progress',flush=True)
 finally:e.close()
