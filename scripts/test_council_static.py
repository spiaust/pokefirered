from pathlib import Path
import json,re,struct,hashlib,subprocess,sys
from collections import deque
r=Path(__file__).resolve().parents[1]
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
bad=[]
for text in re.findall(r'\.string "([^"\n]+)"',(r/'data/scripts/europe_council.inc').read_text()):
 for line in re.split(r'\\[npl]|\$',text):
  w=sum(widths[chars[c]] for c in line)
  if w>216:bad.append((w,line))
assert not bad,bad
print('PASS: Council dialogue fits native font',flush=True)
layouts=json.loads((r/'data/layouts/layouts.json').read_text())['layouts']
for name,targets in [('EuropeCouncilHall',[(x,4) for x in (2,4,6,8,10)]+[(2,7),(4,7),(6,7),(10,7),(5,7)]),('EuropeLondonReadingRoom',[(5,4),(8,5),(3,4),(9,2),(4,7),(5,7)])]:
 m=json.loads((r/'data/maps'/name/'map.json').read_text());l=next(x for x in layouts if x.get('id')==m['layout']);w=l['width'];h=l['height'];a=struct.unpack('<'+str(w*h)+'H',(r/l['blockdata_filepath']).read_bytes());blocked={(o['x'],o['y']) for o in m['object_events']};seen={(5,7)};q=deque(seen)
 while q:
  x,y=q.popleft()
  for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
   xx,yy=p
   if p not in seen and 0<=xx<w and 0<=yy<h and p not in blocked and not a[yy*w+xx]&0xc00:seen.add(p);q.append(p)
 assert all(p in seen for p in targets),(name,targets,seen)
print('PASS: five opponents, nurse, steward, reception and original room displays are reachable',flush=True)
paths=[r/'data/layouts/layouts.json',r/'data/maps/map_groups.json',r/'data/maps/EuropeCouncilHall/map.json',r/'data/layouts/EuropeCouncilHall/map.bin',r/'data/layouts/EuropeCouncilHall/border.bin']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={p:sha(p) for p in paths};subprocess.run([sys.executable,str(r/'scripts/build-council-hall.py')],check=True);assert all(sha(p)==v for p,v in before.items())
old=json.loads((r/'artifacts/releases/v3.2-evidence/map_groups.json').read_text()) if (r/'artifacts/releases/v3.2-evidence/map_groups.json').exists() else None
if old:assert json.loads((r/'data/maps/map_groups.json').read_text())['gMapGroup_Europe'][:-1]==old['gMapGroup_Europe']
print('PASS: Hall generator is byte-idempotent and appends its map',flush=True)
