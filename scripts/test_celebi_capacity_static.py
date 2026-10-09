"""Exact Ada Bag-help text scope and native font fit."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_celebi.inc').read_bytes();old=(r/'data/geography/celebi-capacity-v148.inc').read_bytes()
a=b.index(b'EuropeCelebi_Text_Full::');z=b.index(b'EuropeCelebi_Conclusion::',a);oa=old.index(b'EuropeCelebi_Text_Full::');oz=old.index(b'EuropeCelebi_Conclusion::',oa)
extra=b'\t.string "Open BAG, then the ITEMS pocket.\\n"\r\n\t.string "Use, give or toss an unneeded item.\\p"\r\n\t.string "Come back after making room.\\n"\r\n\t.string "Your vision report stays safe.$"\r\n'
assert b[:a]+old[oa:oz]+b[z:]==old and b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
print('PASS: exact Ada pending-reward text addition preserves all Celebi vision, consent, report, reward and time-travel commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in re.findall(rb'\.string "([^"]+)"',extra):
 for line in re.split(r'\\[npl]|\$',s.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Ada Items-pocket and safe-report instructions fit native font and message window')
