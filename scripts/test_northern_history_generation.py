"""Deterministic Amiens/Rouen asset and map generation."""
from pathlib import Path
import hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1];paths=[R/'data/layouts/layouts.json']
for city in ['Amiens','Rouen']:
 paths += [p for p in (R/f'data/tilesets/secondary/europe_{city.lower()}').rglob('*') if p.suffix in ('.png','.pal','.bin')]
 paths += [R/f'data/geography/{city.lower()}-landmark-blocks.json',R/f'data/layouts/Europe{city}Past/map.bin',R/f'data/maps/Europe{city}Past/map.json',R/f'data/maps/Europe{city}Past/scripts.inc']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-northern-history-assets.py')],check=True)
for city in ['Amiens','Rouen']:subprocess.run([sys.executable,str(R/'scripts/build-northern-history-map.py'),city],check=True)
assert all(sha(p)==v for p,v in before.items())
print('PASS: Amiens/Rouen tiles, palettes, blocks, signs and metadata regenerate byte-for-byte')
