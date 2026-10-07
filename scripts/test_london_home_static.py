"""London home appends IDs and regenerates without changing outdoor terrain."""
from pathlib import Path
import json,hashlib,subprocess,sys,struct
R=Path(__file__).resolve().parents[1]
p=R/'data/layouts/EuropeLondon/map.bin';raw=p.read_bytes()
from london_compatibility import assert_london_facade
assert_london_facade(raw,(R/'data/geography/london-v083.bin').read_bytes())
t=struct.unpack('<2816H',raw);assert t[32*64+45]&0xc00 and not t[33*64+45]&0xc00
m=json.loads((R/'data/maps/EuropeLondon/map.json').read_text())
assert sum(e['script']=='EuropeLondonHome_Enter' and (e['x'],e['y'])==(45,32) for e in m['bg_events'])==1
old=json.loads((R/'data/geography/london-home-v083-map-ids.json').read_text())
g=json.loads((R/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
assert g[:len(old)]==old and g[len(old)]=='EuropeLondonHome'
print('PASS: London home entrance is reachable; exact outdoor terrain and every prior map ID retained')
paths=[p,R/'data/layouts/layouts.json',R/'data/maps/map_groups.json',R/'data/maps/EuropeLondon/map.json',R/'data/maps/EuropeLondon/scripts.inc']
paths+=list((R/'data/maps/EuropeLondonHome').glob('*'))+list((R/'data/layouts/EuropeLondonHome').glob('*'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
for script in ['build-london-home.py','build-london-map.py']:subprocess.run([sys.executable,str(R/'scripts'/script)],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
print('PASS: London home and outdoor lane regenerate identically with earlier entrances retained')
