"""Verify England accepted-study text scope and native line widths."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_story.inc').read_bytes();old=(r/'data/geography/england-accepted-v143.inc').read_bytes()
a=b.index(b'EuropeStory_Text_Accepted::');z=b.index(b'EuropeStory_Text_Progress::',a);oa=old.index(b'EuropeStory_Text_Accepted::');oz=old.index(b'EuropeStory_Text_Progress::',oa)
lines=['Leave LONDON north for the meadow.\\n','OLIVER stands east of the main path.\\p','Head north again for OXFORD TRAIL.\\n','ALICE stands east of its main path.\\p','Continue north to OXFORD square.\\n','Your rival waits west of the guide.$']
extra=''.join(f'\t.string "{s}"\r\n' for s in lines).encode()
assert b[:a]+old[oa:oz]+b[z:]==old and b[a:z]==old[oa:oz].replace(b'.$"',b'.\\p"')+extra and b[a:z].count(b'$"')==1
print('PASS: exact accepted-study text addition preserves all original scripts, trainer gates, report and one-time reward logic')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in lines:
 for line in re.split(r'\\[npl]|\$',s):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: London, Oliver, Alice and Oxford rival directions fit the native font and message window')
