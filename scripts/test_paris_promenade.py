"""Preserve every v0.60 Paris save position and deterministic promenade generation."""
from pathlib import Path
import json,struct,subprocess,sys,hashlib
R=Path(__file__).resolve().parents[1]
p=R/'data/layouts/EuropeParis/map.bin'
old=struct.unpack('<1840H',(R/'data/geography/paris-v060.bin').read_bytes())
new=struct.unpack('<1840H',p.read_bytes())
attrs=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(R/'data/tilesets/secondary/europe_paris/metatile_attributes.bin').read_bytes()
water=lambda t:struct.unpack_from('<I',attrs,(t&1023)*4)[0]&511 in (0x10,0x11,0x12,0x13,0x15,0x19,0x1a,0x1b)
for i,(a,b) in enumerate(zip(old,new)):
 assert (a&0xfc00)==(b&0xfc00),(i,'collision/elevation')
 assert water(a)==water(b),(i,'land/water')
for x,y in [(4,32),(4,36),(4,42),(13,42),(13,36),(17,32),(21,38),(26,38),(33,38)]:
 assert new[y*40+x]==0x3165,(x,y,'missing pavement')
print('PASS: every v0.60 Paris collision, elevation and land/water cell retained; promenade paths paved')
paths=[p,R/'data/maps/EuropeParis/map.json',R/'data/maps/EuropeParis/scripts.inc',R/'data/layouts/layouts.json',R/'data/layouts/EuropeBerlin/map.bin']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-capital-maps.py'),'Paris'],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
m=json.loads((R/'data/maps/EuropeParis/map.json').read_text())
assert any(e['script']=='EuropeCase_NotreDame_Enter' and (e['x'],e['y'])==(28,34) for e in m['bg_events'])
print('PASS: Paris regeneration is identical, preserves Notre-Dame entrance and leaves Berlin unchanged')
