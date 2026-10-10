"""Apply rail artwork to twelve existing walkable bridge deck cells."""
from pathlib import Path
import struct,json
r=Path(__file__).resolve().parents[1];f=r/'data/layouts/EuropeChantilly/map.bin';a=list(struct.unpack('<1728H',f.read_bytes()))
ids=json.loads((r/'data/geography/chantilly-landmark-blocks.json').read_text())['bridge_rails']
for dx,t in enumerate(ids):
 for y in range(11,16):
  i=y*72+50+dx;a[i]=(a[i]&0xfc00)|t
f.write_bytes(struct.pack('<1728H',*a))
