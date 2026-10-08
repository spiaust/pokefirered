"""Long-trail help/declines change only the intended text and decline target."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
help=b'\t.string "You can say No and come back later.\\n"\r\n\t.string "The town clinic heals teams for free.\\p"\r\n'
texts=[]
for city,trainer in [('Oxford','Alice'),('Chantilly','Lucie'),('Oranienburg','Otto')]:
 b=(r/f'data/maps/Europe{city}Trail/scripts.inc').read_bytes()
 marker=f'\r\nEuropeTrail_{trainer}_Decline::'.encode();assert b.count(marker)==1
 body,extra=b.split(marker)
 assert body.count(help)==1
 restored=body.replace(help,b'').replace(f'goto_if_eq VAR_RESULT, NO, EuropeTrail_{trainer}_Decline'.encode(),b'goto_if_eq VAR_RESULT, NO, EuropeTrail_Decline')
 assert restored==(r/f'data/geography/long-trail-{city.lower()}-v126.inc').read_bytes()
 assert b'\tmsgbox '+f'EuropeTrail_{trainer}_DeclineText'.encode()+b'\r\n\trelease\r\n\tend' in extra
 assert f'Next town: {city.upper()}.'.encode() in extra and b'path north.' in extra
 for line in re.findall(rb'\.string "([^"]+)"',help+extra):texts.extend(re.split(r'\\[npl]|\$',line.decode()))
print('PASS: three long-trail introductions and northward decline destinations preserve all battle/reward commands and previous text')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for line in texts:assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: all new introduction and named-town decline lines fit the native font and message window')
