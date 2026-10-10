from pathlib import Path
import struct,json
r=Path.cwd();p=r/'data/layouts/EuropeSouthamptonPast/map.bin';a=list(struct.unpack('<2560H',p.read_bytes()));blocks=json.loads((r/'data/geography/southamptonpast-landmark-blocks.json').read_text())
cells=[(x,y,t) for x,t in zip((48,50),blocks['bridge_rails']) for y in range(35,39)]
for x,y,t in cells:
 i=y*64+x;assert a[i]&1023 in (0x165,t);a[i]=(a[i]&0xfc00)|t
p.write_bytes(struct.pack('<2560H',*a))
