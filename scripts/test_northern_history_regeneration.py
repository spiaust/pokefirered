"""Deterministic Amiens/Rouen asset and map generation."""
from pathlib import Path
import hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1];paths=[R/'data/layouts/layouts.json']
for city in ['Amiens','Rouen']:
 paths += [p for p in (R/f'data/tilesets/secondary/europe_{city.lower()}').rglob('*') if p.suffix in ('.png','.pal','.bin')]
 paths += [R/f'data/geography/{city.lower()}-landmark-blocks.json',R/f'data/layouts/Europe{city}Past/map.bin',R/f'data/maps/Europe{city}Past/map.json',R/f'data/maps/Europe{city}Past/scripts.inc']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
import shutil
backup=R/'.local-tools/northern-history-regeneration-v207';backup.mkdir(exist_ok=True)
for p in paths:
 d=backup/p.relative_to(R);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
try:
 subprocess.run([sys.executable,str(R/'scripts/build-northern-history-assets.py')],check=True)
 for city in ['Amiens','Rouen']:subprocess.run([sys.executable,str(R/'scripts/build-northern-history-map.py'),city],check=True)
 changed=[str(p.relative_to(R)) for p,v in before.items() if sha(p)!=v]
 for n in changed:print('Changed:',n,'newline-only:',(R/n).read_bytes().replace(b'\r\n',b'\n')==(backup/n).read_bytes().replace(b'\r\n',b'\n'),flush=True)
 assert not changed,changed
 print('PASS: Amiens/Rouen tiles, palettes, blocks, signs and metadata regenerate byte-for-byte')
except BaseException:
 for p in paths:shutil.copy2(backup/p.relative_to(R),p)
 raise
