"""Old-footprint safety and stable London residential-lane generation."""
from pathlib import Path
import json,struct,hashlib,subprocess,sys
from london_compatibility import assert_old_london
R=Path(__file__).resolve().parents[1]
p=R/'data/layouts/EuropeLondon/map.bin';raw=p.read_bytes()
assert_old_london(raw,(R/'data/geography/london-v082.bin').read_bytes(),64)
t=struct.unpack('<2816H',raw)
assert (64+15)*(44+14)<=0x2800
for bx in (44,54):
 for y in range(28,33):
  for x in range(bx,bx+5):assert t[y*64+x]&0xc00
 assert not t[33*64+bx+1]&0xc00
m=json.loads((R/'data/maps/EuropeLondon/map.json').read_text())
assert len(m['object_events'])==6
for script in ('EuropeCase_Westminster_Enter','EuropeLondonEyeGallery_Enter'):
 assert sum(e['script']==script for e in m['bg_events'])==1
print('PASS: old London walkable positions, collision and entrances retained; lane mouth opens, homes solid and map fits hardware')
paths=[p,R/'data/maps/EuropeLondon/map.json',R/'data/maps/EuropeLondon/scripts.inc',R/'data/layouts/layouts.json',R/'data/maps/map_groups.json',R/'data/layouts/EuropeParis/map.bin']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-london-map.py')],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
print('PASS: London lane regeneration is identical and retains map IDs, events and Paris terrain')
