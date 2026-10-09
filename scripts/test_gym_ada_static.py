"""Exact third-Gym Ada lead and native font validation."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/maps/EuropeOranienburgGym/scripts.inc').read_bytes();old=(r/'data/geography/gym-ada-v146.inc').read_bytes()
a=b.index(b'EuropeOranienburgGym_Text_Complete::');z=b.index(b'EuropeOranienburgGym_Text_Full::',a);oa=old.index(b'EuropeOranienburgGym_Text_Complete::');oz=old.index(b'EuropeOranienburgGym_Text_Full::',oa)
extra=b'\t.string "ADA studies old paths in OXFORD.\\n"\r\n\t.string "Find her east of the town guide.\\p"\r\n\t.string "She has a new lead from CHANTILLY.\\n"\r\n\t.string "Speak with her when you are ready.$"\r\n'
assert b[:a]+old[oa:oz]+b[z:]==old and b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
print('PASS: exact completed-third-Gym addition preserves commands, badges, one-time TM, river directions and all story gates')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in re.findall(rb'\.string "([^"]+)"',extra):
 for line in re.split(r'\\[npl]|\$',s.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Ada location and Chantilly story lead fit the native font and message window')
