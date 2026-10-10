from pathlib import Path
import struct,json
r=Path.cwd();p=r/'data/layouts/EuropeCalaisPort/map.bin';a=list(struct.unpack('<2240H',p.read_bytes()));b=json.loads((r/'data/geography/calaisport-landmark-blocks.json').read_text())
for x,t in zip((50,52),b['pier_rails']):
 for y in range(5,11):
  i=y*56+x;assert a[i]&1023 in (0x165,t);a[i]=(a[i]&0xfc00)|t
p.write_bytes(struct.pack('<2240H',*a))
