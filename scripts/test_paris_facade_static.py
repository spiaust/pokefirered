"""Native roof recoloring retains every prior tile attribute and ID."""
from pathlib import Path
import json,struct
from paris_compatibility import assert_paris_facade
R=Path(__file__).resolve().parents[1]
assert_paris_facade((R/'data/layouts/EuropeParis/map.bin').read_bytes(),(R/'data/geography/paris-v092.bin').read_bytes())
b=R/'data/tilesets/secondary/europe_paris';a=(b/'metatile_attributes.bin').read_bytes();m=(b/'metatiles.bin').read_bytes()
blocks=json.loads((R/'data/geography/paris-landmark-blocks.json').read_text());mapping=blocks['garden_roof']
for old,new in mapping.items():
 old=int(old);assert a[(old-640)*4:(old-639)*4]==a[(new-640)*4:(new-639)*4]
 source=struct.unpack_from('<8H',m,(old-640)*16);target=struct.unpack_from('<8H',m,(new-640)*16)
 assert target==tuple(0x8000|(v&0xc00)|blocks['roof_tiles'][str(v&1023)] if v>>12==2 else v for v in source)
print('PASS: only eastern roof art changes; all terrain, tile attributes and native artwork retained')
for slot in range(16):
 assert (b/'palettes'/f'{slot:02}.pal').read_bytes()==(R/'data/tilesets/secondary/pallet_town/palettes'/f'{slot:02}.pal').read_bytes() or slot==7
assert blocks['roof_remap'][0]==0
assert len(set(blocks['roof_remap'][11:15]))==4
print('PASS: shared palettes remain native; four roof shades remain distinct and transparency is retained')
