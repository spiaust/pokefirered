"""Clinic directions are text-only and fit the native message window."""
from pathlib import Path
import re,ast
r=Path(__file__).resolve().parents[1]
old=b'Free care for traveling partners.$'
new=b'Free care for traveling partners.\\p"\n\t.string "Enter the door beside this sign.\\n"\n\t.string "Talk to the nurse to heal your team.$'
for city in ['London','Paris','Berlin']:
 b=(r/f'data/maps/Europe{city}/scripts.inc').read_bytes()
 assert b.count(new)==1 and b.replace(new,old)==(r/f'data/geography/clinic-{city.lower()}-v122.inc').read_bytes()
p=r/'scripts/create-europe-maps.py';b=p.read_bytes()
generator_new=new.replace(b'\\',b'\\\\').replace(b'\t',b'\\t').replace(b'\n',b'\r\n')
assert b.count(generator_new)==1 and b.replace(generator_new,old)==(r/'data/geography/clinic-generator-v122.py').read_bytes()
ast.parse(b.decode())
print('PASS: only one clinic sign page added in three capitals and generator; all commands and other text exact')
font=(r/'src/text.c').read_text()
widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
for line in ['Enter the door beside this sign.','Talk to the nurse to heal your team.']:
 assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: both clinic direction lines fit the native font and message window')
