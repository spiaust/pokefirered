"""Apply western wall art to the current map without regenerating its events."""
from pathlib import Path
import json,struct
r=Path(__file__).resolve().parents[1]
f=r/'data/layouts/EuropeBerlin/map.bin';a=list(struct.unpack('<2816H',f.read_bytes()))
mapping=json.loads((r/'data/geography/berlin-facade-blocks.json').read_text())['western_wall']
for y in range(30,32):
 for x in range(42,47):
  i=y*64+x;t=a[i];replacement=mapping.get(str(t&1023))
  if replacement is not None:a[i]=(t&0xfc00)|replacement
f.write_bytes(struct.pack('<2816H',*a))
