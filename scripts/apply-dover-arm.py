from pathlib import Path
import struct,json
r=Path.cwd();p=r/'data/layouts/EuropeDoverPort/map.bin';a=list(struct.unpack('<2240H',p.read_bytes()));blocks=json.loads((r/'data/geography/doverport-landmark-blocks.json').read_text())
for y,t in zip((31,33),blocks['arm_rails']):
 for x in range(27,39):
  i=y*56+x;assert a[i]&1023 in (0x165,t);a[i]=(a[i]&0xfc00)|t
p.write_bytes(struct.pack('<2240H',*a))
