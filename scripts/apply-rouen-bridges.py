from pathlib import Path
import struct,json
r=Path.cwd();p=r/'data/layouts/EuropeRouenPast/map.bin';a=list(struct.unpack('<2880H',p.read_bytes()));blocks=json.loads((r/'data/geography/rouen-landmark-blocks.json').read_text())
for left in (43,71):
 for x,t in zip((left,left+2),blocks['bridge_rails']):
  for y in range(25,28):
   i=y*80+x;assert a[i]&1023 in (0x165,t);a[i]=(a[i]&0xfc00)|t
p.write_bytes(struct.pack('<2880H',*a))
