"""Apply rail artwork to twelve existing walkable bridge deck cells."""
from pathlib import Path
import struct,json
r=Path(__file__).resolve().parents[1];f=r/'data/layouts/EuropeOranienburg/map.bin';a=list(struct.unpack('<1536H',f.read_bytes()))
ids=json.loads((r/'data/geography/oranienburg-landmark-blocks.json').read_text())['bridge_rails']
for x,y in [(55,12),(55,19)]:
 for dy,t in enumerate(ids):
  for dx in range(3):
   i=(y+dy)*64+x+dx;a[i]=(a[i]&0xfc00)|t
f.write_bytes(struct.pack('<1536H',*a))
