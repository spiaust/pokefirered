"""Old historical save positions, deterministic generation and map limits."""
from pathlib import Path
import hashlib,json,struct,subprocess,sys
R=Path(__file__).resolve().parents[1]
l=next(v for v in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if v.get('id')=='LAYOUT_EUROPE_CHANTILLY_PAST')
w,h=l['width'],l['height'];new=struct.unpack('<%dH'%(w*h),(R/l['blockdata_filepath']).read_bytes())
old=struct.unpack('<224H',(R/'data/geography/chantilly-past-v053.bin').read_bytes())
primary=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()
legacy=primary+(R/'data/tilesets/secondary/pallet_town/metatile_attributes.bin').read_bytes()
attrs=primary+(R/'data/tilesets/secondary/europe_chantilly/metatile_attributes.bin').read_bytes()
for i,b in enumerate(old):
 n=new[(i//16)*w+i%16]
 if not b&0xc00:
  assert not n&0xc00 and b>>12==n>>12,(i,b,n)
  assert struct.unpack_from('<I',legacy,(b&1023)*4)[0]&511==struct.unpack_from('<I',attrs,(n&1023)*4)[0]&511
assert (w+15)*(h+14)<=0x2800 and max(t&1023 for t in new)<len(attrs)//4
print('PASS: historical Chantilly old traversable coordinates retain behavior/elevation; map fits hardware')
paths=[R/'data/layouts/layouts.json',R/l['blockdata_filepath'],R/'data/maps/EuropeChantillyPast/map.json',R/'data/maps/EuropeChantillyPast/scripts.inc']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-chantilly-past-map.py')],check=True)
assert all(sha(p)==v for p,v in before.items())
print('PASS: historical Chantilly blocks, signs and layout regenerate byte-for-byte')
