"""Courtyard notice reuses the existing sign and keeps the full map exact."""
from berlin_compatibility import before_route_marker
from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
assert before_route_marker((R/'data/layouts/EuropeBerlin/map.bin').read_bytes())==(R/'data/geography/berlin-court-v098.bin').read_bytes()
for current,old in [('data/maps/EuropeBerlin/map.json','data/geography/berlin-court-v098-events.json'),('data/maps/map_groups.json','data/geography/berlin-court-v098-groups.json')]:assert json.loads((R/current).read_text())==json.loads((R/old).read_text())
m=json.loads((R/'data/maps/EuropeBerlin/map.json').read_text());events=[e for e in m['bg_events'] if e['script']=='EuropeBerlin_RealismCourt'];assert len(events)==1 and (events[0]['x'],events[0]['y'])==(56,34)
s=(R/'data/maps/EuropeBerlin/scripts.inc').read_text().split('EuropeBerlin_RealismCourt::')[1].split('EuropeBerlin_CourtGardener::')[0]
for line in ['West: home. Middle: reading room.','East: the garden workroom.','COURTYARD NOTES','Seed and watering notes: workroom.','Garden log: middle reading room.','Share a memory in the western home.']:assert line in s
assert all(cmd not in s for cmd in ['setflag','setvar','giveitem','additem'])
print('PASS: courtyard notice retains exact terrain, events, objects, exits and map IDs; reading grants no rewards')
paths=[R/p for p in ['data/layouts/EuropeBerlin/map.bin','data/maps/EuropeBerlin/map.json','data/maps/EuropeBerlin/scripts.inc','data/layouts/layouts.json','data/maps/map_groups.json','data/layouts/EuropeParis/map.bin']]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-capital-maps.py'),'Berlin'],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
print('PASS: courtyard notice regenerates identically and preserves the Paris map')
