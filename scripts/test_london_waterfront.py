"""Check London bridge overlays, old-save terrain and deterministic assets."""
from pathlib import Path
import json,struct,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
p=R/'data/layouts/EuropeLondon/map.bin';old=struct.unpack('<1760H',(R/'data/geography/london-v061.bin').read_bytes());new=struct.unpack('<1760H',p.read_bytes())
attrs=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(R/'data/tilesets/secondary/europe_london/metatile_attributes.bin').read_bytes()
water=lambda t:struct.unpack_from('<I',attrs,(t&1023)*4)[0]&511 in (0x10,0x11,0x12,0x13,0x15,0x19,0x1a,0x1b)
for i,(a,b) in enumerate(zip(old,new)):
 assert a&0xfc00==b&0xfc00,(i,'collision/elevation')
 assert water(a)==water(b),(i,'land/water')
bridges=json.loads((R/'data/geography/london-landmark-blocks.json').read_text())['bridges']
for name,x,y in [('westminster',20,28),('lambeth',22,38)]:
 for dy,t in enumerate(bridges[name]):
  for dx in range(4):assert new[(y+dy)*40+x+dx]==0x3000|t
print('PASS: all v0.61 London collision/elevation and water retained; both bridge overlays remain walkable')
base=R/'data/tilesets/secondary/europe_london'
paths=[p,R/'data/layouts/EuropeLondonPast/map.bin',R/'data/maps/EuropeLondon/map.json',R/'data/geography/london-landmark-blocks.json',base/'tiles.png',base/'metatiles.bin',base/'metatile_attributes.bin']+list((base/'palettes').glob('*.pal'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
for script in ['build-london-assets.py','build-london-map.py']:subprocess.run([sys.executable,str(R/'scripts'/script)],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==v for p,v in before.items())
assert any(e['script']=='EuropeCase_Westminster_Enter' for e in json.loads((R/'data/maps/EuropeLondon/map.json').read_text())['bg_events'])
print('PASS: bridge assets and London regenerate identically; historical layout and Westminster entrance retained')
