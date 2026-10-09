"""Exact Ada Bag-help text scope and native font fit."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_departure.inc').read_bytes();old=(r/'data/geography/departure-beauvais-v152.inc').read_bytes()
a=b.index(b'EuropeDeparture_Text_RefugeDone::');z=b.index(b'EuropeDeparture_Text_ChildDone::',a);oa=old.index(b'EuropeDeparture_Text_RefugeDone::');oz=old.index(b'EuropeDeparture_Text_ChildDone::',oa)
extra=b'\t.string "Station-post guide: southeast corner.\\n"\r\n\t.string "Return there and read the board.\\p"\r\n\t.string "A train to BEAUVAIS is ready.\\n"\r\n\t.string "Speak to the host when you arrive.$"\r\n'
assert b[:a]+old[oa:oz]+b[z:]==old and b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
print('PASS: exact keeper completed-report addition preserves all news, boarding, reception and return-travel commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in re.findall(rb'\.string "([^"]+)"',extra):
 for line in re.split(r'\\[npl]|\$',s.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Station-post board and Beauvais reception instructions fit native font and message window')
