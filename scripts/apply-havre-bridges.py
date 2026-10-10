from pathlib import Path
import struct,json
r=Path.cwd();p=r/'data/layouts/EuropeLeHavrePast/map.bin';a=list(struct.unpack('<2560H',p.read_bytes()));blocks=json.loads((r/'data/geography/lehavrepast-landmark-blocks.json').read_text())
cells=[(x,y,t) for start,stop,top in [(39,45,18),(41,44,29)] for y,t in zip((top,top+1),blocks['bridge_rails']) for x in range(start,stop)]
for x,y,t in cells:
 i=y*64+x;assert a[i]&1023 in (0x165,t);a[i]=(a[i]&0xfc00)|t
p.write_bytes(struct.pack('<2560H',*a))
