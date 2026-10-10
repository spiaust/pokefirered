from pathlib import Path
import json,struct
r=Path(__file__).resolve().parents[1];f=r/'data/layouts/EuropeOxford/map.bin';a=list(struct.unpack('<1536H',f.read_bytes()))
ids=json.loads((r/'data/geography/oxford-landmark-blocks.json').read_text())['clinic_wall']
for y in (8,9):
 for x in range(5,10):
  i=y*64+x;t=a[i];replacement=ids.get(str(t&1023))
  if replacement is not None:a[i]=(t&0xfc00)|replacement
f.write_bytes(struct.pack('<1536H',*a))
