"""The historical harbor reproduces exactly from its recorded source inputs."""
from pathlib import Path
import hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
paths=[R/'data/layouts/layouts.json',R/'data/layouts/EuropeSouthamptonPast/map.bin',R/'data/maps/EuropeSouthamptonPast/map.json',R/'data/maps/EuropeSouthamptonPast/scripts.inc',R/'data/geography/southamptonpast-landmark-blocks.json']
paths += [p for p in (R/'data/tilesets/secondary/europe_southamptonpast').rglob('*') if p.suffix in ('.png','.pal','.bin')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
for script in ['build-southampton-assets.py','build-southampton-map.py']:subprocess.run([sys.executable,str(R/'scripts'/script)],check=True)
assert all(sha(p)==v for p,v in before.items())
print('PASS: Southampton art, map, signs and metadata regenerate byte-for-byte')
