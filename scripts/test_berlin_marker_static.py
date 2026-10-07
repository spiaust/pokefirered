"""The visible route marker changes exactly one tile without moving events."""
from pathlib import Path
import json,struct
from berlin_compatibility import before_route_marker
R=Path(__file__).resolve().parents[1];raw=(R/'data/layouts/EuropeBerlin/map.bin').read_bytes()
assert before_route_marker(raw)==(R/'data/geography/berlin-marker-v101.bin').read_bytes()
a=struct.unpack('<2816H',raw)
assert a[4*64+14]==0x402
for y in range(2,8):
 for x in (15,16,17):assert a[y*64+x]==0x3165
m=json.loads((R/'data/maps/EuropeBerlin/map.json').read_text());old=json.loads((R/'data/geography/berlin-court-v098-events.json').read_text());assert m==old
print('PASS: only Berlin (14,4) becomes a native sign; exact events, objects, exits and adjacent pavement retained')
groups=json.loads((R/'data/maps/map_groups.json').read_text());assert groups==json.loads((R/'data/geography/berlin-court-v098-groups.json').read_text())
s=(R/'src/overworld.c').read_text();assert 'gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_EUROPE_BERLIN)' in s
print('PASS: map IDs retained and Berlin old-save terrain refresh remains enabled')
