"""Deterministic Southampton asset and map generation."""
from pathlib import Path
import hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1];paths=[R/'data/layouts/layouts.json']
for city in ['Southampton']:
 paths += [p for p in (R/f'data/tilesets/secondary/europe_southamptonpast').rglob('*') if p.suffix in ('.png','.pal','.bin')]
 paths += [R/f'data/geography/southamptonpast-landmark-blocks.json',R/f'data/layouts/Europe{city}Past/map.bin',R/f'data/maps/Europe{city}Past/map.json',R/f'data/maps/Europe{city}Past/scripts.inc']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
import shutil
backup=R/'.local-tools/southampton-regeneration-v210';backup.mkdir(exist_ok=True)
for p in paths:
 d=backup/p.relative_to(R);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
try:
 subprocess.run([sys.executable,str(R/'scripts/build-southampton-assets.py')],check=True)
 for city in ['Southampton']:subprocess.run([sys.executable,str(R/'scripts/build-southampton-map.py')],check=True)
 changed=[str(p.relative_to(R)) for p,v in before.items() if sha(p)!=v]
 for n in changed:print('Changed:',n,'newline-only:',(R/n).read_bytes().replace(b'\r\n',b'\n')==(backup/n).read_bytes().replace(b'\r\n',b'\n'),flush=True)
 assert not changed,changed
 print('PASS: Southampton tiles, palettes, blocks, signs and metadata regenerate byte-for-byte')
except BaseException:
 for p in paths:shutil.copy2(backup/p.relative_to(R),p)
 raise
