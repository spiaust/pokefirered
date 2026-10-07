"""Paris home appends after all prior maps and preserves the exact lane."""
from pathlib import Path
import json,hashlib,subprocess,sys,struct
from map_compatibility import assert_map_prefix
R=Path(__file__).resolve().parents[1]
raw=(R/'data/layouts/EuropeParis/map.bin').read_bytes();from paris_compatibility import assert_paris_facade
assert_paris_facade(raw,(R/'data/geography/paris-v090.bin').read_bytes())
old=json.loads((R/'data/geography/paris-workroom-v091-groups.json').read_text());new=json.loads((R/'data/maps/map_groups.json').read_text());assert_map_prefix(new,old)
assert new['gMapGroup_Europe']==old['gMapGroup_Europe']+['EuropeParisGardenRoom']
m=json.loads((R/'data/maps/EuropeParis/map.json').read_text());assert sum(e['script']=='EuropeParisGardenRoom_Enter' and (e['x'],e['y'])==(55,38) for e in m['bg_events'])==1
t=struct.unpack('<2944H',raw);assert t[38*64+55]&0xc00 and not t[39*64+55]&0xc00
print('PASS: Paris home appends all earlier map IDs; exact lane terrain and reachable entrance retained')
paths=[R/'data/maps/map_groups.json',R/'data/layouts/layouts.json',R/'data/maps/EuropeParis/map.json',R/'data/maps/EuropeParis/scripts.inc',R/'data/layouts/EuropeParis/map.bin']
paths+=list((R/'data/maps/EuropeParisGardenRoom').glob('*'))+list((R/'data/layouts/EuropeParisGardenRoom').glob('*'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
for script,args in [('build-paris-garden-room.py',[]),('build-capital-maps.py',['Paris'])]:subprocess.run([sys.executable,str(R/'scripts'/script),*args],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
print('PASS: Paris home and lane regenerate identically with previous entrances retained')
