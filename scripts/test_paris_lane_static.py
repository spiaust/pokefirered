"""Expanded Paris lane preserves old walking cells and hardware limits."""
from pathlib import Path
import json,struct
from paris_compatibility import assert_old_paris
R=Path(__file__).resolve().parents[1]
raw=(R/'data/layouts/EuropeParis/map.bin').read_bytes();assert_old_paris(raw,(R/'data/geography/paris-v089.bin').read_bytes())
t=struct.unpack('<2944H',raw);assert (64+15)*(46+14)<=0x2800
for bx in (44,54):
 for y in range(34,39):
  for x in range(bx,bx+5):assert t[y*64+x]&0xc00
 assert not t[39*64+bx+1]&0xc00
m=json.loads((R/'data/maps/EuropeParis/map.json').read_text());old=json.loads((R/'data/geography/paris-lane-v089-events.json').read_text())
assert m['object_events']==old['object_events'] and m['warp_events']==old['warp_events'] and m['coord_events']==old['coord_events']
assert all(e in m['bg_events'] for e in old['bg_events'])
assert len(m['bg_events'])==len(old['bg_events'])+4
from map_compatibility import assert_map_prefix
assert_map_prefix(json.loads((R/'data/maps/map_groups.json').read_text()),json.loads((R/'data/geography/paris-artist-v088-groups.json').read_text()))
print('PASS: old Paris walking cells, objects, entrances and IDs retained; only lane mouth opens the boundary')
print('PASS: two native home fronts have clear approaches; expanded grid fits the hardware buffer')
