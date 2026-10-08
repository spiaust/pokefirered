"""Readiness directions alter only three text blocks, with native font fit."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
extra=b'\t.string "Free clinic: west side of the square.\\p"\r\n\t.string "POTIONS: shop inside the station.\\n"\r\n\t.string "Station: east side of the square.$"\r\n'
for city in ['Oxford','Chantilly','Oranienburg']:
 b=(r/f'data/maps/Europe{city}Gym/scripts.inc').read_bytes();old=(r/f'data/geography/gym-guide-{city.lower()}-v129.inc').read_bytes()
 start=f'Europe{city}Gym_Text_Advice::'.encode();end=f'Europe{city}Gym_Text_Statue::'.encode()
 a=b.index(start);z=b.index(end,a);oa=old.index(start);oz=old.index(end,oa)
 assert b[:a]+old[oa:oz]+b[z:]==old
 assert b[a:z]==old[oa:oz].replace(b'.$"',b'.\\p"')+extra
texts=re.findall(rb'\.string "([^"]+)"',extra)
print('PASS: exact Gym-guide advice additions preserve all original messages, gates, battles and reward commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in texts:
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: new clinic and Potion-shop directions fit the native font and message window')
