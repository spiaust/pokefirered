"""Apply western wall art to the current map without regenerating its events."""
from pathlib import Path
import json,struct
r=Path(__file__).resolve().parents[1]
f=r/'data/layouts/EuropeParis/map.bin';a=list(struct.unpack('<2944H',f.read_bytes()))
mapping=json.loads((r/'data/geography/paris-landmark-blocks.json').read_text())['western_wall']
for y in range(37,39):
 for x in range(44,49):
  i=y*64+x;t=a[i];replacement=mapping.get(str(t&1023))
  if replacement is not None:a[i]=(t&0xfc00)|replacement
f.write_bytes(struct.pack('<2944H',*a))
