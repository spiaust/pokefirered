"""Guestbook reuses a solid table without changing older room saves."""
from pathlib import Path
import json,struct,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
raw=(R/'data/layouts/EuropeBerlinHome/map.bin').read_bytes();assert raw==(R/'data/geography/berlin-home-v095.bin').read_bytes()
m=json.loads((R/'data/maps/EuropeBerlinHome/map.json').read_text());old=json.loads((R/'data/geography/berlin-home-v095-events.json').read_text())
assert m['object_events']==old['object_events'] and m['coord_events']==old['coord_events'] and m['warp_events']==old['warp_events']
assert json.loads((R/'data/maps/map_groups.json').read_text())==json.loads((R/'data/geography/berlin-home-v095-groups.json').read_text())
t=struct.unpack('<130H',raw);assert len(m['bg_events'])==4
assert {(e['x'],e['y']) for e in m['bg_events']}=={(x,y) for x in (6,7) for y in (4,5)}
for e in m['bg_events']:assert t[e['y']*13+e['x']]&0xc00 and e['elevation']==0 and e['player_facing_dir']=='BG_EVENT_PLAYER_FACING_ANY'
print('PASS: guestbook uses four existing solid table cells; exact room, objects, exits and map IDs retained')
paths=[R/'data/layouts/EuropeBerlinHome/map.bin',R/'data/maps/EuropeBerlinHome/map.json',R/'data/maps/EuropeBerlinHome/scripts.inc',R/'data/maps/EuropeBerlin/map.json',R/'data/layouts/layouts.json',R/'data/maps/map_groups.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-berlin-home.py')],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
s=(R/'data/maps/EuropeBerlinHome/scripts.inc').read_text().split('EuropeBerlinHome_Guestbook::')[1].split('EuropeBerlinHome_End::')[0]
assert all(cmd not in s for cmd in ['setflag','setvar','giveitem','additem'])
print('PASS: guestbook generation is stable; reading changes no inventory or progression')
