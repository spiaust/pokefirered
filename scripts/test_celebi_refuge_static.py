"""Exact Ada Bag-help text scope and native font fit."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_celebi.inc').read_bytes();old=(r/'data/geography/celebi-refuge-v149.inc').read_bytes()
a=b.index(b'EuropeCelebi_Text_Complete::');z=b.index(b'EuropeCelebi_Text_Full::',a);oa=old.index(b'EuropeCelebi_Text_Complete::');oz=old.index(b'EuropeCelebi_Text_Full::',oa)
extra=b'\t.string "Return to CELEBI in the forest.\\n"\r\n\t.string "Say Yes to visit the refuge.\\p"\r\n\t.string "To come home, speak to CELEBI.\\n"\r\n\t.string "It waits beside the arrival point.$"\r\n'
assert b[:a]+old[oa:oz]+b[z:]==old and b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
print('PASS: exact Ada onward-refuge text addition preserves all Celebi vision, consent, report, reward and time-travel commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in re.findall(rb'\.string "([^"]+)"',extra):
 for line in re.split(r'\\[npl]|\$',s.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Ada forest-departure and return-home instructions fit native font and message window')
