from pathlib import Path
import json,struct
r=Path(__file__).resolve().parents[1];f=r/'data/layouts/EuropeChantilly/map.bin';a=list(struct.unpack('<1728H',f.read_bytes()))
ids=json.loads((r/'data/geography/chantilly-landmark-blocks.json').read_text())['station_roof']
for y in (6,7):
 for x in range(20,27):
  i=y*72+x;t=a[i];replacement=ids.get(str(t&1023))
  if replacement is not None:a[i]=(t&0xfc00)|replacement
f.write_bytes(struct.pack('<1728H',*a))
