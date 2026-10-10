from pathlib import Path
import struct,json
r=Path.cwd();p=r/'data/layouts/EuropeAmiensPast/map.bin';a=list(struct.unpack('<2304H',p.read_bytes()));blocks=json.loads((r/'data/geography/amiens-landmark-blocks.json').read_text())
cells=[(x,y,t) for left in (30,53) for x,t in zip((left,left+2),blocks['bridge_rails'][:2]) for y in range(10,13)]
cells += [(x,y,t) for y,t in zip((6,7),blocks['bridge_rails'][2:]) for x in range(39,42)]
for x,y,t in cells:
 i=y*64+x;assert a[i]&1023 in (0x165,t);a[i]=(a[i]&0xfc00)|t
p.write_bytes(struct.pack('<2304H',*a))
