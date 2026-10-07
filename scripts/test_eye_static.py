"""London Eye entrance and gallery regenerate without changing outdoor terrain."""
from pathlib import Path
import struct,json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[1]
raw=(R/'data/layouts/EuropeLondon/map.bin').read_bytes()
from london_compatibility import assert_old_london
l=next(l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if l.get('id')=='LAYOUT_EUROPE_LONDON')
assert_old_london(raw,(R/'data/geography/london-v069.bin').read_bytes(),l['width'])
t=struct.unpack('<%dH'%(len(raw)//2),raw);w=l['width']
assert not t[29*w+29]&0xc00 and t[28*w+29]&0xc00
m=json.loads((R/'data/maps/EuropeLondon/map.json').read_text())
assert sum(e['script']=='EuropeLondonEyeGallery_Enter' and (e['x'],e['y'])==(29,28) for e in m['bg_events'])==1
g=json.loads((R/'data/maps/map_groups.json').read_text())['gMapGroup_Europe']
assert g.index('EuropeLondonEyeGallery')>g.index('EuropeEiffelVisitor')
print('PASS: Eye entrance approach is open; old London walkable terrain and earlier map IDs retained')
paths=[R/'data/maps/map_groups.json',R/'data/layouts/layouts.json',R/'data/maps/EuropeLondon/map.json',R/'data/maps/EuropeLondon/scripts.inc',R/'data/layouts/EuropeLondon/map.bin']
paths+=list((R/'data/maps/EuropeLondonEyeGallery').glob('*'))+list((R/'data/layouts/EuropeLondonEyeGallery').glob('*'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
for script in ['build-eye-gallery.py','build-london-map.py']:subprocess.run([sys.executable,str(R/'scripts'/script)],check=True,stdout=subprocess.DEVNULL)
assert all(sha(p)==h for p,h in before.items())
print('PASS: Eye gallery and London regenerate identically with Westminster entrance retained')
