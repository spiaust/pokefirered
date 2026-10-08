"""Pending regional reward instructions change only shared dialogue."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
old=b'\t.string "Visit the other town guides, too!$"'
new=b'\t.string "Visit the other town guides, too!\\p"\r\n\t.string "Other guides: OXFORD, CHANTILLY,\\n"\r\n\t.string "and ORANIENBURG.\\p"\r\n\t.string "Station: east side of the square.\\n"\r\n\t.string "Book a train to your next guide town.$"'
b=(r/'data/scripts/europe_challenges.inc').read_bytes()
assert b.count(new)==1 and b.replace(new,old)==(r/'data/geography/regional-complete-help-v136.inc').read_bytes()
print('PASS: exact completed-reward text addition preserves all shared scripts, existing messages and reward commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in re.findall(rb'\.string "([^"]+)"',new):
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: guide-town and east-station onward instructions fit the native font and message window')
