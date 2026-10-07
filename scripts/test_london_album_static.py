"""Photo album occupies the existing table, preserving every walking tile."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
raw=(R/'data/layouts/EuropeLondonHome/map.bin').read_bytes()
assert raw==(R/'data/geography/london-home-v087.bin').read_bytes()
t=struct.unpack('<130H',raw);assert t[4*13+6]&0xc00 and not t[3*13+6]&0xc00
assert (R/'data/layouts/EuropeLondon/map.bin').read_bytes()==(R/'data/geography/london-v086.bin').read_bytes()
print('PASS: photo album uses existing solid table; exact indoor and outdoor layouts retained')
m=json.loads((R/'data/maps/EuropeLondonHome/map.json').read_text());old=json.loads((R/'data/geography/london-home-v087-events.json').read_text())
assert m['object_events'][:-1]==old['object_events']
assert m['coord_events']==old['coord_events'] and m['bg_events'][:-1]==old['bg_events']
b=m['bg_events'][-1];assert (b['x'],b['y'],b['elevation'])==(6,4,0) and b['script']=='EuropeLondonHome_Album'
a=m['object_events'][-1];assert (a['x'],a['y'])==(6,4) and a['script']=='EuropeLondonHome_Album' and a['flag']=='0'
from map_compatibility import assert_map_prefix
assert_map_prefix(json.loads((R/'data/maps/map_groups.json').read_text()),json.loads((R/'data/geography/london-home-v087-groups.json').read_text()))
s=(R/'data/maps/EuropeLondonHome/scripts.inc').read_text();album=s.split('EuropeLondonHome_Album::')[1].split('EuropeLondonHome_End::')[0]
assert all(cmd not in album for cmd in ['setflag','setvar','giveitem','additem'])
print('PASS: album appends without moving earlier objects, exits or map IDs and awards no progression')
