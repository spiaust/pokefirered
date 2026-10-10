from pathlib import Path
import struct,json
r=Path.cwd();p=r/'data/layouts/EuropeLondonPast/map.bin';a=list(struct.unpack('<3200H',p.read_bytes()));blocks=json.loads((r/'data/geography/london-landmark-blocks.json').read_text())
for name,x,y in [('westminster',52,15),('lambeth',54,32)]:
 for dy,t in enumerate(blocks['past_bridges'][name]):
  for dx in range(6):
   i=(y+dy)*80+x+dx;assert a[i]&1023 in (0x165,t);a[i]=(a[i]&0xfc00)|t
p.write_bytes(struct.pack('<3200H',*a))
