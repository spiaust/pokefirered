"""Deterministic Le Havre asset and map generation."""
from pathlib import Path
import hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1];paths=[R/'data/layouts/layouts.json']
for city in ['LeHavre']:
 paths += [p for p in (R/f'data/tilesets/secondary/europe_lehavrepast').rglob('*') if p.suffix in ('.png','.pal','.bin')]
 paths += [R/f'data/geography/lehavrepast-landmark-blocks.json',R/f'data/layouts/Europe{city}Past/map.bin',R/f'data/maps/Europe{city}Past/map.json',R/f'data/maps/Europe{city}Past/scripts.inc']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
import shutil
backup=R/'.local-tools/havre-regeneration-v209';backup.mkdir(exist_ok=True)
for p in paths:
 d=backup/p.relative_to(R);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
try:
 subprocess.run([sys.executable,str(R/'scripts/build-havre-assets.py')],check=True)
 for city in ['LeHavre']:subprocess.run([sys.executable,str(R/'scripts/build-havre-map.py')],check=True)
 changed=[str(p.relative_to(R)) for p,v in before.items() if sha(p)!=v]
 for n in changed:print('Changed:',n,'newline-only:',(R/n).read_bytes().replace(b'\r\n',b'\n')==(backup/n).read_bytes().replace(b'\r\n',b'\n'),flush=True)
 assert not changed,changed
 print('PASS: Le Havre tiles, palettes, blocks, signs and metadata regenerate byte-for-byte')
except BaseException:
 for p in paths:shutil.copy2(backup/p.relative_to(R),p)
 raise
