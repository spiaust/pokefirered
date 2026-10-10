"""Regenerate regional assets/maps; restore originals if any output differs."""
from pathlib import Path
import hashlib,subprocess,sys,json,shutil
version=sys.argv[1] if len(sys.argv)>1 else 'v203';assert version.startswith('v') and version[1:].isdigit();r=Path(__file__).resolve().parents[1];b=r/f'.local-tools/port-regeneration-{version}';b.mkdir(exist_ok=True)
files=[r/'data/layouts/layouts.json']
for city in ['DoverPort','CalaisPort']:
 files += [r/f'data/layouts/Europe{city}/map.bin',r/f'data/layouts/Europe{city}/border.bin',r/f'data/geography/{city.lower()}-landmark-blocks.json',r/f'data/maps/Europe{city}/map.json',r/f'data/maps/Europe{city}/scripts.inc']
 d=r/f'data/tilesets/secondary/europe_{city.lower()}'
 files += [d/n for n in ['tiles.png','metatiles.bin','metatile_attributes.bin']]+list((d/'palettes').glob('*.pal'))
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
before={str(f.relative_to(r)):sha(f) for f in files}
for f in files:
 dest=b/f.relative_to(r);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
try:
 subprocess.run([sys.executable,str(r/'scripts/build-port-assets.py')],check=True)
 subprocess.run([sys.executable,str(r/'scripts/build-port-maps.py')],check=True)
 changed=[n for n,h in before.items() if sha(r/n)!=h]
 for n in changed:
  old=(b/n).read_bytes();new=(r/n).read_bytes()
  print(n,'normalized equality:',old.replace(b'\r\n',b'\n')==new.replace(b'\r\n',b'\n'),flush=True)
  dest=r/f'.local-tools/port-regenerated-{version}'/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(new)
 (r/f'test-output/port-regeneration-{version}.json').write_text(json.dumps({'changed_files':changed,'original_hashes':before},indent=2)+'\n')
 assert not changed,changed
 print('PASS: full two-port asset/map pipeline reproduces pier/landmark assets, palettes, maps and events byte-for-byte',flush=True)
except BaseException:
 for f in files:shutil.copy2(b/f.relative_to(r),f)
 raise
