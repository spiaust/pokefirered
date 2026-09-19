"""Historical London generation is deterministic and excludes the modern wheel."""
from pathlib import Path
import hashlib,json,struct,subprocess,sys
R=Path(__file__).resolve().parents[1]
paths=[R/'data/layouts/layouts.json',R/'data/layouts/EuropeLondonPast/map.bin',R/'data/maps/EuropeLondonPast/map.json',R/'data/maps/EuropeLondonPast/scripts.inc']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths}
subprocess.run([sys.executable,str(R/'scripts/build-london-past-map.py')],check=True)
assert all(sha(p)==v for p,v in before.items())
b=(R/'data/layouts/EuropeLondonPast/map.bin').read_bytes();used={t&1023 for t in struct.unpack('<%dH'%(len(b)//2),b)}
blocks=json.loads((R/'data/geography/london-landmark-blocks.json').read_text())
assert not used.intersection(t for row in blocks['eye'] for t in row)
assert {t for row in blocks['palace'] for t in row}<=used
print('PASS: historical London regenerates byte-for-byte; palace is present and modern wheel is absent')
