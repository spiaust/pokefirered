"""Reading-room furniture cannot block positions from prior indoor saves."""
from pathlib import Path
import struct,json
R=Path(__file__).resolve().parents[1]
old=struct.unpack('<130H',(R/'data/geography/london-reading-v086.bin').read_bytes())
new=struct.unpack('<130H',(R/'data/layouts/EuropeLondonReadingRoom/map.bin').read_bytes())
for i,(a,b) in enumerate(zip(old,new)):
 if not a&0xc00:
  assert a&0xf000==b&0xf000,(i,'elevation')
  assert not b&0xc00,(i,'new obstacle')
 if a!=b:assert (4<=i%13<10 and 3<=i//13<7) or (9<=i%13<11 and i//13<2),i
assert new!=old
for i in [7*13+5,7*13+9,8*13+4,8*13+5,2*13+9]:assert not new[i]&0xc00
print('PASS: reading furniture preserves elevation and every previously walkable saved position')
m=json.loads((R/'data/maps/EuropeLondonReadingRoom/map.json').read_text());before=json.loads((R/'data/geography/london-reading-v086-events.json').read_text())
assert m['object_events']==before['object_events'] and m['coord_events']==before['coord_events']
from map_compatibility import assert_map_prefix
assert_map_prefix(json.loads((R/'data/maps/map_groups.json').read_text()),json.loads((R/'data/geography/london-reading-v086-groups.json').read_text()))
assert len(m['bg_events'])==1 and (m['bg_events'][0]['x'],m['bg_events'][0]['y'])==(9,1)
assert (R/'data/layouts/EuropeLondon/map.bin').read_bytes()==(R/'data/geography/london-v086.bin').read_bytes()
print('PASS: existing objects, exits and map IDs retained; shared-book cabinet uses solid wall')
