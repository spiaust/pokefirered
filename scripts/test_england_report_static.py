"""Exact rival report-return text scope and native font fit."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_story.inc').read_bytes();old=(r/'data/geography/england-report-v142.inc').read_bytes()
a=b.index(b'EuropeStory_Text_Return::');z=b.index(b'EuropeStory_Text_Reward::',a);oa=old.index(b'EuropeStory_Text_Return::');oz=old.index(b'EuropeStory_Text_Reward::',oa)
extra=('\t.string "Station: east side of town square.\\n"\r\n'
 '\t.string "Take a train to LONDON.\\p"\r\n'
 '\t.string "OAK\'s aide: west of the town guide.\\n"\r\n'
 '\t.string "Bring him the field study report.$"\r\n').encode()
assert b[:a]+old[oa:oz]+b[z:]==old and b[a:z]==old[oa:oz].replace(b'.$"',b'.\\p"')+extra and b[a:z].count(b'$"')==1
print('PASS: exact rival return-text addition preserves all original England gates, trainer flags, report hand-in, badge readiness and one-time Soothe Bell')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in re.findall(rb'\.string "([^"]+)"',extra):
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: new station, London train and Oak aide instructions fit the native font and message window')
