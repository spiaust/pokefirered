"""Trail signs add nearest-town services without changing gameplay."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
old=b'\t.string "Wild POKEMON live in the tall grass.$"'
for city in ['Oxford','Chantilly','Oranienburg']:
 b=(r/f'data/maps/Europe{city}Trail/scripts.inc').read_bytes()
 extra=('\t.string "Wild POKEMON live in the tall grass.\\p"\r\n\t.string "Need free healing? Head north.\\n"\r\n'+f'\t.string "Next town: {city.upper()}.\\p"\r\n'+'\t.string "Free clinic: west side of the square.\\n"\r\n\t.string "Supplies: shop in the town station.$"').encode()
 assert b.count(extra)==1 and b.replace(extra,old)==(r/f'data/geography/trail-sign-{city.lower()}-v130.inc').read_bytes()
 texts+=re.findall(rb'\.string "([^"]+)"',extra)
print('PASS: exact sign additions preserve all prior route directions, trainers, battles and reward commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in texts:
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: named-town, clinic and station-shop sign lines fit the native font and message window')
