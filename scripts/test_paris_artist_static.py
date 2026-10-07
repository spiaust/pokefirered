"""The promenade sketcher appends without changing any outdoor tile or ID."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
raw=(R/'data/layouts/EuropeParis/map.bin').read_bytes();from paris_compatibility import assert_old_paris
assert_old_paris(raw,(R/'data/geography/paris-v077.bin').read_bytes())
t=struct.unpack('<2944H',raw);m=json.loads((R/'data/maps/EuropeParis/map.json').read_text());old=json.loads((R/'data/geography/paris-artist-v088-events.json').read_text())
assert m['object_events'][:-1]==old['object_events'] and all(e in m['bg_events'] for e in old['bg_events']) and m['coord_events']==old['coord_events']
a=m['object_events'][-1];assert (a['x'],a['y'])==(30,42) and a['script']=='EuropeParis_PromenadeArtist' and a['flag']=='0'
assert not t[42*64+30]&0xc00 and t[42*64+30]!=0x3165 and not t[43*64+30]&0xc00
from map_compatibility import assert_map_prefix
assert_map_prefix(json.loads((R/'data/maps/map_groups.json').read_text()),json.loads((R/'data/geography/paris-artist-v088-groups.json').read_text()))
print('PASS: sketcher stands off the paved promenade; old walking terrain, prior objects, entrances and map IDs retained')
s=(R/'data/maps/EuropeParis/scripts.inc').read_text().split('EuropeParis_PromenadeArtist::')[1]
assert all(cmd not in s for cmd in ['setflag','setvar','giveitem','additem'])
assert a['movement_type']=='MOVEMENT_TYPE_FACE_DOWN' and a['movement_range_x']==a['movement_range_y']==0
print('PASS: stationary sketcher dialogue has no inventory or progression rewards')
