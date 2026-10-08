"""Pending regional reward instructions change only shared dialogue."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
old=b'\t.string "Your RARE CANDY will be waiting!$"'
new=b'\t.string "Your RARE CANDY will be waiting!\\p"\r\n\t.string "Open BAG, then the ITEMS pocket.\\n"\r\n\t.string "Use, give or toss an unneeded item.\\p"\r\n\t.string "Return here after making room.\\n"\r\n\t.string "Your reward will still be waiting!$"'
b=(r/'data/scripts/europe_challenges.inc').read_bytes()
assert b.count(new)==1 and b.replace(new,old)==(r/'data/geography/regional-bag-help-v135.inc').read_bytes()
print('PASS: exact pending-reward text addition preserves all shared scripts, existing messages and reward commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in re.findall(rb'\.string "([^"]+)"',new):
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Items-pocket, room-making and return instructions fit the native font and message window')
