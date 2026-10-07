"""Paris garden residents preserve terrain and old object ordering."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
raw=(R/'data/layouts/EuropeParis/map.bin').read_bytes()
from paris_compatibility import assert_old_paris
assert_old_paris(raw,(R/'data/geography/paris-v077.bin').read_bytes())
t=struct.unpack('<2944H',raw)
m=json.loads((R/'data/maps/EuropeParis/map.json').read_text())
assert m['object_events'][:2]==json.loads((R/'data/geography/paris-v077-objects.json').read_text())
assert len(m['object_events'])==5
for o,point,gfx in zip(m['object_events'][2:4],[(6,40),(7,40)],['OBJ_EVENT_GFX_WOMAN_2','OBJ_EVENT_GFX_PSYDUCK']):
 assert (o['x'],o['y'])==point and o['graphics_id']==gfx and not t[point[1]*64+point[0]]&0xc00
 assert o['movement_type']=='MOVEMENT_TYPE_FACE_DOWN' and o['flag']=='0'
assert {(6,40),(7,40)}.isdisjoint({(4,42),(13,42),(13,36),(9,37),(26,38),(33,38)})
print('PASS: old Paris walking terrain and original objects retained; stationary garden residents sit clear of promenade routes')
