"""Sketch display stays on the old wall, preserving walking space and IDs."""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[1]
old=struct.unpack('<130H',(R/'data/geography/paris-home-v093.bin').read_bytes());new=struct.unpack('<130H',(R/'data/layouts/EuropeParisHome/map.bin').read_bytes())
for i,(a,b) in enumerate(zip(old,new)):
 assert a&0xfc00==b&0xfc00,(i,'collision/elevation')
 if a!=b:assert i in (9,10,22,23)
 if not a&0xc00:assert a==b
assert old!=new
from paris_compatibility import assert_paris_facade
assert_paris_facade((R/'data/layouts/EuropeParis/map.bin').read_bytes(),(R/'data/geography/paris-v092.bin').read_bytes())
print('PASS: display artwork changes only four solid wall cells; all walking tiles and outdoor terrain retained')
m=json.loads((R/'data/maps/EuropeParisHome/map.json').read_text());before=json.loads((R/'data/geography/paris-home-v093-events.json').read_text())
assert m['object_events']==before['object_events'] and m['coord_events']==before['coord_events']
assert len(m['bg_events'])==1 and (m['bg_events'][0]['x'],m['bg_events'][0]['y'])==(9,1)
s=(R/'data/maps/EuropeParisHome/scripts.inc').read_text().split('EuropeParisHome_Display::')[1].split('EuropeParisHome_End::')[0]
assert all(cmd not in s for cmd in ['setflag','setvar','giveitem','additem'])
print('PASS: existing objects and exits stay fixed; display reading changes no inventory or progression')
