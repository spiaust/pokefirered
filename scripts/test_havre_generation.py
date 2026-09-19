"""The historical harbor reproduces exactly from its recorded source inputs."""
from pathlib import Path
import hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
paths=[R/'data/layouts/layouts.json',R/'data/layouts/EuropeLeHavrePast/map.bin',R/'data/maps/EuropeLeHavrePast/map.json',R/'data/maps/EuropeLeHavrePast/scripts.inc',R/'data/geography/lehavrepast-landmark-blocks.json']
paths += [p for p in (R/'data/tilesets/secondary/europe_lehavrepast').rglob('*') if p.suffix in ('.png','.pal','.bin')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
for script in ['build-havre-assets.py','build-havre-map.py']:subprocess.run([sys.executable,str(R/'scripts'/script)],check=True)
assert all(sha(p)==v for p,v in before.items())
print('PASS: Le Havre art, map, signs and metadata regenerate byte-for-byte')
