"""Gym help changes only the intended text, with native font limits."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
help=b'\t.string "You can say No and come back later.\\n"\r\n\t.string "The town clinic heals teams for free.\\p"\r\n'
old=b'\t.string "The clinic offers free healing.$"'
new=b'\t.string "The clinic offers free healing.\\p"\r\n\t.string "Follow the path back to the exit.\\p"\r\n\t.string "Free clinic: west side of the square.$"'
for city in ['Oxford','Chantilly','Oranienburg']:
 b=(r/f'data/maps/Europe{city}Gym/scripts.inc').read_bytes()
 assert b.count(help)==1 and b.count(new)==1
 assert b.replace(help,b'').replace(new,old)==(r/f'data/geography/gym-help-{city.lower()}-v127.inc').read_bytes()
print('PASS: all three Gym changes are exactly the preparation and decline text; gates, battles, badges, teams and reward commands are unchanged')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in re.findall(rb'\.string "([^"]+)"',help+new):
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: all new Gym help lines fit the native font and message window')
