"""Historical station and Beauvais generation must be byte-for-byte repeatable."""
from pathlib import Path
import hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1];paths=[R/'data/layouts/layouts.json']
for asset,name in [('chantillypost','ChantillyPastPost'),('beauvais','BeauvaisGarden')]:
 base=R/f'data/tilesets/secondary/europe_{asset}'
 paths += [p for p in base.rglob('*') if p.suffix in ('.png','.pal','.bin')]
 paths += [R/f'data/geography/{asset}-landmark-blocks.json',R/f'data/layouts/Europe{name}/map.bin',R/f'data/layouts/Europe{name}/border.bin',R/f'data/maps/Europe{name}/map.json',R/f'data/maps/Europe{name}/scripts.inc']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
for script in ['build-history-assets.py','build-chantilly-post-map.py','build-beauvais-map.py']:
 subprocess.run([sys.executable,str(R/'scripts'/script)],check=True)
assert all(sha(p)==v for p,v in before.items()),[str(p) for p,v in before.items() if sha(p)!=v]
print('PASS: historical station and Beauvais tiles, palettes, layouts, signs and metadata regenerate identically')
