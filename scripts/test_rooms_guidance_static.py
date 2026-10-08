"""The Rooms help change must leave all native map logic byte-identical."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
old = (root/'data/geography/rooms-map-v115.c').read_bytes()
new = (root/'src/europe_map.c').read_bytes()
line = b'Door: press A. Exit: south doorway.'
assert old.count(b'Face either door and press A.') == 2
assert old.count(b'Face any of the three doors; press A.') == 1
assert old.replace(b'Face either door and press A.', line).replace(
    b'Face any of the three doors; press A.', line) == new
assert new.count(line) == 3
print('PASS: only three capital Rooms text lines change; all map, input, preferences and saved-state logic exact')
