"""Bench plans reuse existing solid furniture and preserve old room state."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
raw=(R/'data/layouts/EuropeParisGardenRoom/map.bin').read_bytes();assert raw==(R/'data/geography/paris-workroom-v094.bin').read_bytes()
m=json.loads((R/'data/maps/EuropeParisGardenRoom/map.json').read_text());old=json.loads((R/'data/geography/paris-workroom-v094-events.json').read_text())
assert m['object_events']==old['object_events'] and m['coord_events']==old['coord_events']
assert m['warp_events']==old['warp_events']
print('PASS: exact workroom terrain, walking space, existing objects and exits retained')
t=struct.unpack('<130H',raw);events=m['bg_events'];assert len(events)==8
assert {(e['x'],e['y']) for e in events}=={(x,y) for x in (2,3,10,11) for y in (5,6)}
for e in events:
 assert t[e['y']*13+e['x']]&0xc00 and e['elevation']==0
 assert e['player_facing_dir']=='BG_EVENT_PLAYER_FACING_ANY'
 assert e['script']=='EuropeParisGardenRoom_'+('Plan' if e['x']<4 else 'Rota')
s=(R/'data/maps/EuropeParisGardenRoom/scripts.inc').read_text().split('EuropeParisGardenRoom_Plan::')[1].split('EuropeParisGardenRoom_End::')[0]
assert all(cmd not in s for cmd in ['setflag','setvar','giveitem','additem'])
print('PASS: all eight solid bench cells support reading; plans change no inventory or progression')
