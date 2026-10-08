"""One optional-battle help page changes text only in all three countries."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
addition=b'\t.string "You can say No and come back later.\\n"\r\n\t.string "The town clinic heals teams for free.\\p"\r\n'
for city in ['London','Paris','Berlin']:
 b=(r/f'data/maps/Europe{city}Countryside/scripts.inc').read_bytes()
 assert b.count(addition)==1 and b.replace(addition,b'')==(r/f'data/geography/training-{city.lower()}-v125.inc').read_bytes()
print('PASS: exactly one training introduction page added in each country; battle/decline/reward commands and other text remain exact')
font=(r/'src/text.c').read_text()
widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
for line in ['You can say No and come back later.','The town clinic heals teams for free.']:
 assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: both optional-battle introduction lines fit the native font and message window')
