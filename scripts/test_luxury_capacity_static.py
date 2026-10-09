"""Exact Ada Bag-help text scope and native font fit."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_message.inc').read_bytes();old=(r/'data/geography/luxury-capacity-v154.inc').read_bytes()
a=b.index(b'EuropeMessage_Text_Full::');z=len(b);oa=old.index(b'EuropeMessage_Text_Full::');oz=len(old)
extra=b'\t.string "BAG: open the POKE BALLS pocket.\\n"\r\n\t.string "Give or toss one unneeded ball.\\p"\r\n\t.string "If LUXURY BALLS are at the limit,\\n"\r\n\t.string "make room in that stack and return.$"\r\n'
assert b[:a]+old[oa:oz]+b[z:]==old and b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
print('PASS: exact pending Luxury Ball text addition preserves message, account, reward and travel commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in re.findall(rb'\.string "([^"]+)"',extra):
 for line in re.split(r'\\[npl]|\$',s.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Poke Balls pocket and capped Luxury Ball instructions fit native font and message window')
