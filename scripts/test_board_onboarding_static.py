"""Board journal help appends text while retaining all item and map behavior."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];f=r/'data/scripts/europe_navigation.inc'
t=f.read_text();old=(r/'.local-tools/navigation-before-v180.inc').read_text()
extra='\n\t.string "UP/DOWN switches journal topics.\\n"\n\t.string "EUROPE TOUR lists badge tasks.\\p"\n\t.string "Start with OAK\'s aide in LONDON.\\n"\n\t.string "CELEBI JOURNEY tracks later visits.$"'
assert t.endswith(extra+'\n')
assert t.removesuffix(extra+'\n').replace('On the map, SELECT opens STORY.\\p','On the map, SELECT opens STORY.$')+'\n'==old
print('PASS: only board help text appends; original gifts, gates, map transition and script commands remain exact')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
chars["'"]=0xB4
for text in re.findall(r'\.string "([^"]+)"',t):
 for line in re.split(r'\\[npl]|\$',text):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: all board instruction lines fit the native dialogue font/window')
