"""Scope and font checks for first and repeated Celebi return directions."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_celebi.inc').read_bytes();old=(r/'data/geography/celebi-return-v147.inc').read_bytes()
extra=b'\t.string "Walk north to CHANTILLY square.\\n"\r\n\t.string "Station: east side of the square.\\p"\r\n\t.string "Take a train to OXFORD.\\n"\r\n\t.string "ADA waits east of the town guide.$"\r\n'
for name,end in [('Remember','Leave'),('Return','Quiet')]:
 a=b.index(f'EuropeCelebi_Text_{name}::'.encode());z=b.index(f'EuropeCelebi_Text_{end}::'.encode(),a);oa=old.index(f'EuropeCelebi_Text_{name}::'.encode());oz=old.index(f'EuropeCelebi_Text_{end}::'.encode(),oa)
 assert b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
 b=b[:a]+old[oa:oz]+b[z:]
assert b==old
print('PASS: exact first/repeated forest return text additions preserve all Celebi consent, sighting, report and one-time reward commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in re.findall(rb'\.string "([^"]+)"',extra):
 for line in re.split(r'\\[npl]|\$',s.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: northward Chantilly, station, Oxford train and Ada location instructions fit native font and message window')
