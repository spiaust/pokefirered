"""Gate entrance, outdoor compatibility and stable visitor-room generation."""
from berlin_compatibility import before_route_marker
from pathlib import Path
import struct,json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
p=R/'data/layouts/EuropeBerlin/map.bin';raw=p.read_bytes()
assert before_route_marker(raw)==(R/'data/geography/berlin-v076.bin').read_bytes()
t=struct.unpack('<2816H',raw)
assert not t[37*64+19]&0xc00 and t[36*64+19]&0xc00
for y in (34,35,36):
 for x in (20,21):assert not t[y*64+x]&0xc00
m=json.loads((R/'data/maps/EuropeBerlin/map.json').read_text())
assert sum(e['script']=='EuropeGateVisitor_Enter' and (e['x'],e['y'])==(19,36) for e in m['bg_events'])==1
g=json.loads((R/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
old=json.loads((R/'data/geography/gate-v076-map-ids.json').read_text())
assert g[:len(old)]==old and g[len(old)]=='EuropeGateVisitor'
print('PASS: Gate side-pillar entrance, open central passage, old Berlin terrain apart from the documented northern marker and every prior map ID retained')
paths=[p,R/'data/maps/map_groups.json',R/'data/layouts/layouts.json',R/'data/maps/EuropeBerlin/map.json',R/'data/maps/EuropeBerlin/scripts.inc']
paths+=list((R/'data/maps/EuropeGateVisitor').glob('*'))+list((R/'data/layouts/EuropeGateVisitor').glob('*'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
for script,args in [('build-gate-visitor.py',[]),('build-capital-maps.py',['Berlin'])]:
 subprocess.run([sys.executable,str(R/'scripts'/script),*args],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
print('PASS: Gate visitor room and capital regenerate identically with existing entrances and residents retained')
