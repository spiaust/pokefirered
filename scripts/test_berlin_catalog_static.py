"""Catalog reuses a solid table without changing older room saves."""
from pathlib import Path
import json,struct,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
raw=(R/'data/layouts/EuropeBerlinLibrary/map.bin').read_bytes();assert raw==(R/'data/geography/berlin-library-v096.bin').read_bytes()
m=json.loads((R/'data/maps/EuropeBerlinLibrary/map.json').read_text());old=json.loads((R/'data/geography/berlin-library-v096-events.json').read_text())
assert m['object_events']==old['object_events'] and m['coord_events']==old['coord_events'] and m['warp_events']==old['warp_events']
assert json.loads((R/'data/maps/map_groups.json').read_text())==json.loads((R/'data/geography/berlin-library-v096-groups.json').read_text())
t=struct.unpack('<130H',raw);assert len(m['bg_events'])==4
assert all(e['script']=='EuropeBerlinLibrary_Catalog' for e in m['bg_events'])
assert all(e['script'].startswith('EuropeBerlinGardenRoom_') for e in json.loads((R/'data/maps/EuropeBerlinGardenRoom/map.json').read_text())['bg_events'])
assert {(e['x'],e['y']) for e in m['bg_events']}=={(x,y) for x in (6,7) for y in (4,5)}
for e in m['bg_events']:assert t[e['y']*13+e['x']]&0xc00 and e['elevation']==0 and e['player_facing_dir']=='BG_EVENT_PLAYER_FACING_ANY'
print('PASS: catalog uses four existing solid table cells; exact room, objects, exits and map IDs retained')
paths=[R/'data/layouts/EuropeBerlinLibrary/map.bin',R/'data/maps/EuropeBerlinLibrary/map.json',R/'data/maps/EuropeBerlinLibrary/scripts.inc',R/'data/maps/EuropeBerlin/map.json',R/'data/layouts/layouts.json',R/'data/maps/map_groups.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-berlin-library.py')],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
s=(R/'data/maps/EuropeBerlinLibrary/scripts.inc').read_text().split('EuropeBerlinLibrary_Catalog::')[1].split('EuropeBerlinLibrary_CatalogText::')[0]
assert all(cmd not in s for cmd in ['setflag','setvar','giveitem','additem'])
print('PASS: catalog generation is stable; reading changes no inventory or progression')
