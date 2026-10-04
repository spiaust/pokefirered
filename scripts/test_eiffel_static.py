"""Eiffel visitor entrance is reachable and regenerates without changing terrain."""
from pathlib import Path
import struct,json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
assert (R/'data/layouts/EuropeParis/map.bin').read_bytes()==(R/'data/geography/paris-v068.bin').read_bytes()
t=struct.unpack('<1840H',(R/'data/layouts/EuropeParis/map.bin').read_bytes())
assert not t[37*40+9]&0xc00 and t[36*40+9]&0xc00
m=json.loads((R/'data/maps/EuropeParis/map.json').read_text())
assert sum(e['script']=='EuropeEiffelVisitor_Enter' and (e['x'],e['y'])==(9,36) for e in m['bg_events'])==1
groups=json.loads((R/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
assert groups.index('EuropeEiffelVisitor')>groups.index('EuropeBerlinGardenRoom')
print('PASS: Eiffel entrance approach is open; every old Paris tile and indoor map ID retained')
paths=[R/'data/maps/map_groups.json',R/'data/layouts/layouts.json',R/'data/maps/EuropeParis/map.json',R/'data/maps/EuropeParis/scripts.inc',R/'data/layouts/EuropeParis/map.bin']
paths+=list((R/'data/maps/EuropeEiffelVisitor').glob('*'))+list((R/'data/layouts/EuropeEiffelVisitor').glob('*'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
for script,args in [('build-eiffel-visitor.py',[]),('build-capital-maps.py',['Paris'])]:subprocess.run([sys.executable,str(R/'scripts'/script),*args],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==h for p,h in before.items())
print('PASS: visitor room and Paris regenerate identically with both landmark entrances retained')
