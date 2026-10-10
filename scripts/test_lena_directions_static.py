"""Board journal help appends text while retaining all item and map behavior."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];f=r/'data/scripts/europe_germany_story.inc'
t=f.read_text();old=(r/'.local-tools/germany-before-v182.inc').read_text()
extra='\n\t.string "Begin with OAK\'s aide in LONDON.\\n"\n\t.string "Finish his study and report to him.\\p"\n\t.string "After ELLIS, meet CELINE in PARIS.\\n"\n\t.string "Finish her survey and report to her.$"'
assert t.count(extra)==1
assert t.replace(extra,'').replace('in CHANTILLY after their studies.\\p','in CHANTILLY after their studies.$')==old
print('PASS: only Lena early badge help appends; all quest gates, rewards and scripts remain exact')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
chars["'"]=0xB4
for text in re.findall(r'\.string "([^"]+)"',t.split('EuropeGermany_Text_Badges::',1)[1].split('EuropeGermany_Text_Decline::',1)[0]):
 for line in re.split(r'\\[npl]|\$',text):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Lena early badge instruction lines fit the native dialogue font/window')
