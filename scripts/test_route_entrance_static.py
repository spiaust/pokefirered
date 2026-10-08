"""Route entrance signs add optional-training help with exact source scope."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
for city,trainer in [('London','OLIVER'),('Paris','CAMILLE'),('Berlin','FELIX')]:
 b=(r/f'data/maps/Europe{city}/scripts.inc').read_bytes()
 extra=(f'\t.string "Look for {trainer} on the north route.\\n"\r\n'+'\t.string "Battles are optional. You can say No.\\p"\r\n\t.string "Free clinic: west side of the square.\\n"\r\n\t.string "Supplies: shop inside the station.\\p"\r\n').encode()
 assert b.count(extra)==1 and b.replace(extra,b'')==(r/f'data/geography/route-entrance-{city.lower()}-v131.inc').read_bytes()
 texts+=re.findall(rb'\.string "([^"]+)"',extra)
print('PASS: exact optional-training sign additions preserve all prior destinations, visitor-room text, scripts and reward commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in texts:
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: trainer, optional-battle, clinic and supply directions fit the native font and message window')
