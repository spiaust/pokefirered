from pathlib import Path
import struct,json,subprocess,sys
from collections import deque
r=Path(__file__).resolve().parents[1];b=r/'.local-tools/radcliffe-reading-before-v221'
for n in ['src/europe_map.c','data/maps/EuropeRadcliffeVisitor/map.json','data/layouts/layouts.json','data/maps/map_groups.json','data/event_scripts.s']:assert (r/n).read_bytes()==(b/n).read_bytes(),n
for name,version in [('EuropeChateauVisitor','v2.15'),('EuropePalaceVisitor','v2.16'),('EuropeStablesVisitor','v2.19'),('EuropeMagdalenVisitor','v2.20')]:
 for f in ['map.json','scripts.inc']:assert (r/'data/maps'/name/f).read_bytes()==(r/'artifacts/releases'/f'{version}-{name.replace("Europe", "").replace("Visitor", "").lower()}-map'/f).read_bytes(),name
s=(r/'data/maps/EuropeRadcliffeVisitor/scripts.inc').read_text();old=(b/'data/maps/EuropeRadcliffeVisitor/scripts.inc').read_text();assert s==old.replace('Take your time with the displays.','Browse the notes beside the shelves.')
a=struct.unpack('<130H',(r/'data/layouts/EuropeRadcliffeVisitor/map.bin').read_bytes());old=struct.unpack('<130H',(b/'data/layouts/EuropeRadcliffeVisitor/map.bin').read_bytes());m=json.loads((r/'data/maps/EuropeRadcliffeVisitor/map.json').read_text());objects={(v['x'],v['y']) for v in m['object_events']};blocked=lambda p: a[p[1]*13+p[0]]&0xc00 or p in objects
for p in [(8,4),(3,4),(11,4),(4,7),(5,7),*( (x,y) for y in range(10) for x in range(13) if not old[y*13+x]&0xc00 and (x,y) not in objects)]:
 seen={p};q=deque([p])
 while q:
  x,y=q.popleft()
  for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=n[0]<13 and 0<=n[1]<10 and n not in seen and not blocked(n):seen.add(n);q.append(n)
 assert {(4,7),(5,7)}<=seen,p
print('PASS: old IDs/events/other rooms preserved; every former floor position can reach both exits; guide and displays remain reachable')
files=['data/layouts/EuropeRadcliffeVisitor/map.bin','data/maps/EuropeRadcliffeVisitor/map.json','data/maps/EuropeRadcliffeVisitor/scripts.inc','data/layouts/layouts.json','data/maps/map_groups.json','data/event_scripts.s'];before={n:(r/n).read_bytes() for n in files};subprocess.run([sys.executable,str(r/'scripts/build-radcliffe-visitor.py')],check=True);assert all((r/n).read_bytes()==v for n,v in before.items());assert all(a[y*13+bx+dx]&1023==t for bx in (2,10) for y,row in enumerate([(0x2b,0x2c),(0x33,0x34),(0x3b,0x3c)]) for dx,t in enumerate(row));assert all(a[y*13+x]==0x3001 for y in (4,5) for x in (6,7))
print('PASS: native bookcase pairs and side tables reproduce byte-for-byte with a clear central aisle')
