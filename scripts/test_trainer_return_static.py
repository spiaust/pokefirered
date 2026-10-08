"""Extended trainer victory text adds reward-guide return directions only."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
extra=b'\t.string "Follow the clear path north to town.\\n"\r\n\t.string "The guide waits in the town square.\\p"\r\n\t.string "Both regional wins earn a RARE CANDY.\\n"\r\n\t.string "Free clinic: west side of the square.$"'
for city in ['Oxford','Chantilly','Oranienburg']:
 b=(r/f'data/maps/Europe{city}Trail/scripts.inc').read_bytes()
 old=f'\t.string "{city.upper()} guide for your reward.$"'.encode();new=old.replace(b'.$"',b'.\\p"')+b'\r\n'+extra
 assert b.count(new)==1 and b.replace(new,old)==(r/f'data/geography/trainer-return-{city.lower()}-v133.inc').read_bytes()
print('PASS: exact victory-text additions preserve previous messages, opponents, battle commands and reward eligibility')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in re.findall(rb'\.string "([^"]+)"',extra):
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: northward path, town-square guide, reward requirement and clinic lines fit the native font and window')
