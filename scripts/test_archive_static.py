"""Archive dialogue width, researcher access and native room map bounds."""
import json,re,struct
from collections import deque
from pathlib import Path
r=Path(__file__).resolve().parents[1]
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
texts=re.findall(r'\.string "([^"\n]+)"',(r/'data/scripts/europe_archive.inc').read_text())
assert len(texts)>30
for text in texts:
 for line in re.split(r'\\[npl]|\$',text):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: every archive offer, direction, question and ending line fits the native dialogue font',flush=True)
layouts=json.loads((r/'data/layouts/layouts.json').read_text())['layouts']
for name in ('EuropeRadcliffeVisitor','EuropeChateauVisitor','EuropePalaceVisitor'):
 m=json.loads((r/'data/maps'/name/'map.json').read_text());layout=next(x for x in layouts if x.get('id')==m['layout']);w=layout['width'];h=layout['height']
 cells=struct.unpack('<'+str(w*h)+'H',(r/layout['blockdata_filepath']).read_bytes())
 blocked={(o['x'],o['y']) for o in m['object_events']}
 researcher=[o for o in m['object_events'] if o['script'].startswith('EuropeArchive_')]
 assert len(researcher)==1 and researcher[0]['x']==6 and researcher[0]['y']==3
 seen={(5,7)};queue=deque(seen)
 while queue:
  x,y=queue.popleft()
  for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
   xx,yy=p
   if p not in seen and 0<=xx<w and 0<=yy<h and p not in blocked and not cells[yy*w+xx]&0xc00:seen.add(p);queue.append(p)
 assert all(p in seen for p in ((6,4),(8,4),(3,4),(11,4),(4,7),(5,7))),name
print('PASS: all three researchers, original guide/displays and both exit approaches remain reachable',flush=True)
