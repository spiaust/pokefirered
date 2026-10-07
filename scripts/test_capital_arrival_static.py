"""Arrival guidance changes text only and regenerates identically."""
from pathlib import Path
import re,json,hashlib,subprocess,sys
from berlin_compatibility import before_route_marker
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,digest in json.loads((R/'data/geography/capital-arrival-v100.json').read_text()).items():
 raw=(R/path).read_bytes()
 if path=='data/layouts/EuropeBerlin/map.bin':raw=before_route_marker(raw)
 assert hashlib.sha256(raw).hexdigest()==digest,path
config=json.loads((R/'data/geography/capital-arrival-signs.json').read_text())
for city,entry in config.items():
 s=(R/f'data/maps/Europe{city}/scripts.inc').read_text();label=f'Europe{city}_Text_Route';body=re.search(re.escape(label)+r'::\n((?:[ \t]*\.string[^\n]*\n)+)',s).group(1)
 assert body.startswith(entry['base'].replace('$',chr(92)+'p')) and all(line in body for line in entry['notes'])
 m=json.loads((R/f'data/maps/Europe{city}/map.json').read_text());events=[e for e in m['bg_events'] if e['script']==f'Europe{city}_RouteSign'];assert len(events)==1 and (events[0]['x'],events[0]['y'])==(14,4)
print('PASS: arrival guidance retains exact capital/countryside maps, events, IDs, encounters and existing trail text')
paths=[R/f'data/maps/Europe{city}/scripts.inc' for city in config];before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-capital-arrival-signs.py')],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
print('PASS: all three capital arrival signs regenerate identically')
