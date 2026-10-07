"""London garden residents preserve terrain and old object ordering."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
raw=(R/'data/layouts/EuropeLondon/map.bin').read_bytes()
from london_compatibility import assert_old_london
w=next(l['width'] for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if l.get('id')=='LAYOUT_EUROPE_LONDON')
assert_old_london(raw,(R/'data/geography/london-v078.bin').read_bytes(),w)
t=struct.unpack('<%dH'%(len(raw)//2),raw)
m=json.loads((R/'data/maps/EuropeLondon/map.json').read_text())
assert m['object_events'][:4]==json.loads((R/'data/geography/london-v078-objects.json').read_text())
assert len(m['object_events'])==6
for o,point,gfx in zip(m['object_events'][4:],[(30,34),(31,34)],['OBJ_EVENT_GFX_LITTLE_GIRL','OBJ_EVENT_GFX_JIGGLYPUFF']):
 assert (o['x'],o['y'])==point and o['graphics_id']==gfx and not t[point[1]*w+point[0]]&0xc00
 assert o['movement_type']=='MOVEMENT_TYPE_FACE_DOWN' and o['flag']=='0'
assert {(30,34),(31,34)}.isdisjoint({(27,31),(33,31),(33,36),(29,36),(27,37),(29,29),(20,28),(22,38)})
print('PASS: old London walkable terrain and original object retained; stationary garden residents sit clear of garden/bridge routes')
