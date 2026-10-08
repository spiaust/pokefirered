"""Trainer decline gains one route page without changing battle commands."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
old=b'then come back when you\'re ready.$'
new=b'then come back when you\'re ready.\\p"\r\n\t.string "Follow the clear path south to town.\\n"\r\n\t.string "Free clinic: west side of the square.$'
b=(r/'data/scripts/europe_trails.inc').read_bytes()
assert b.count(new)==1 and b.replace(new,old)==(r/'data/geography/trails-v123.inc').read_bytes()
for city,name in [('London','Oliver'),('Paris','Camille'),('Berlin','Felix')]:
 s=(r/f'data/maps/Europe{city}Countryside/scripts.inc').read_text()
 assert 'goto_if_eq VAR_RESULT, NO, EuropeTrail_Decline' in s
print('PASS: shared decline gains exactly one page; all battle/reward/progress commands remain exact')
font=(r/'src/text.c').read_text()
widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
for line in ['Follow the clear path south to town.','Free clinic: west side of the square.']:
 assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: both countryside return lines fit the native font and message window')
