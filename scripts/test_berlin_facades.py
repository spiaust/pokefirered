"""Roof-only changes retain every collision, behavior, door and old palette."""
from pathlib import Path
import struct,json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
old=struct.unpack('<2816H',(R/'data/geography/berlin-v067.bin').read_bytes())
new=struct.unpack('<2816H',(R/'data/layouts/EuropeBerlin/map.bin').read_bytes())
attrs=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()+(R/'data/tilesets/secondary/europe_berlin/metatile_attributes.bin').read_bytes()
meta=(R/'data/tilesets/primary/general/metatiles.bin').read_bytes()+(R/'data/tilesets/secondary/europe_berlin/metatiles.bin').read_bytes()
changed=set()
for i,(a,b) in enumerate(zip(old,new)):
 if i==4*64+14:assert a==0x3165 and b==0x402;continue
 assert a&0xfc00==b&0xfc00
 assert attrs[(a&1023)*4:(a&1023)*4+4]==attrs[(b&1023)*4:(b&1023)*4+4]
 if a!=b:
  x,y=i%64,i//64;assert 27<=y<=29 and (50<=x<=54 or 57<=x<=61)
  changed.add((x,y))
assert len(changed)==30
used={v>>12 for t in set(old) for v in struct.unpack_from('<8H',meta,(t&1023)*16)}
assert 12 not in used
for x in (43,51,58):assert old[31*64+x]==new[31*64+x]
print('PASS: two roofs and the documented northern sign change; all other terrain behavior, collision, elevations and doors retained')
paths=[R/'data/tilesets/secondary/europe_berlin'/p for p in ['tiles.png','metatiles.bin','metatile_attributes.bin','palettes/12.pal']]+[R/'data/geography/berlin-facade-blocks.json',R/'data/layouts/EuropeBerlin/map.bin']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
for script,args in [('berlin_facades.py',[]),('build-capital-maps.py',['Berlin'])]:subprocess.run([sys.executable,str(R/'scripts'/script),*args],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==h for p,h in before.items())
assert len((R/'data/tilesets/secondary/europe_berlin/metatile_attributes.bin').read_bytes())//4<=384
print('PASS: roof assets and map regenerate identically within GBA tileset limits')
