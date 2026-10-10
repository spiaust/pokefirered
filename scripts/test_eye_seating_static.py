from pathlib import Path
import struct,json,subprocess,sys
from collections import deque
r=Path(__file__).resolve().parents[1];b=r/'.local-tools/eye-seating-before-v226'
for n in ['src/europe_map.c','data/maps/EuropeLondonEyeGallery/map.json','data/layouts/layouts.json','data/maps/map_groups.json','data/event_scripts.s']:assert (r/n).read_bytes()==(b/n).read_bytes(),n
s=(r/'data/maps/EuropeLondonEyeGallery/scripts.inc').read_text();old=(b/'data/maps/EuropeLondonEyeGallery/scripts.inc').read_text();assert s==old
a=struct.unpack('<130H',(r/'data/layouts/EuropeLondonEyeGallery/map.bin').read_bytes());old=struct.unpack('<130H',(b/'data/layouts/EuropeLondonEyeGallery/map.bin').read_bytes());m=json.loads((r/'data/maps/EuropeLondonEyeGallery/map.json').read_text());objects={(v['x'],v['y']) for v in m['object_events']};blocked=lambda p: a[p[1]*13+p[0]]&0xc00 or p in objects
for p in [(6,4),(2,4),(10,4),(4,7),(5,7),*( (x,y) for y in range(10) for x in range(13) if not old[y*13+x]&0xc00 and (x,y) not in objects)]:
 seen={p};q=deque([p])
 while q:
  x,y=q.popleft()
  for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=n[0]<13 and 0<=n[1]<10 and n not in seen and not blocked(n):seen.add(n);q.append(n)
 assert {(4,7),(5,7)}<=seen,p
changed={(5+y)*13+bx+dx:t for bx in (2,10) for y,row in enumerate([(0x44c,0x44d),(0x454,0x455)]) for dx,t in enumerate(row)}
assert all(v==changed.get(i,old[i]) for i,v in enumerate(a))
print('PASS: old IDs/events preserved; every former floor position can reach both exits; guide and displays remain reachable')
files=['data/layouts/EuropeLondonEyeGallery/map.bin','data/maps/EuropeLondonEyeGallery/map.json','data/maps/EuropeLondonEyeGallery/scripts.inc','data/layouts/layouts.json','data/maps/map_groups.json','data/event_scripts.s'];before={n:(r/n).read_bytes() for n in files};subprocess.run([sys.executable,str(r/'scripts/build-eye-gallery.py')],check=True);assert all((r/n).read_bytes()==v for n,v in before.items());assert all(a[(5+y)*13+bx+dx]==t for bx in (2,10) for y,row in enumerate([(0x44c,0x44d),(0x454,0x455)]) for dx,t in enumerate(row))
print('PASS: native side benches reproduce byte-for-byte; existing windows and all other map cells remain exact')
