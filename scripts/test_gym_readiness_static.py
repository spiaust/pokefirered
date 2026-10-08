"""Readiness directions alter only three text blocks, with native font fit."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
for city,capital,contact in [('Oxford','LONDON',"OAK's aide"),('Chantilly','PARIS','CELINE'),('Oranienburg','BERLIN','LENA')]:
 p=r/f'data/maps/Europe{city}Gym/scripts.inc';b=p.read_bytes();old=(r/f'data/geography/gym-readiness-{city.lower()}-v128.inc').read_bytes()
 start=f'Europe{city}Gym_Text_NotReady::'.encode();end=f'Europe{city}Gym_Text_Decline::'.encode()
 a=b.index(start);z=b.index(end,a);oa=old.index(start);oz=old.index(end,oa)
 assert b[:a]+old[oa:oz]+b[z:]==old
 extra=''
 if city=='Chantilly':extra+='\t.string "REMY: west of CHANTILLY\'s guide.\\p"\r\n'
 extra+='\t.string "Exit the GYM; station east of square.\\n"\r\n'+f'\t.string "Take a train to {capital}.\\p"\r\n'+f'\t.string "Find {contact} west of the guide.$"\r\n'
 assert b[a:z]==old[oa:oz].replace(b'.$"',b'.\\p"')+extra.encode()
 texts+=re.findall(rb'\.string "([^"]+)"',extra.encode())
print('PASS: exact readiness-text additions preserve all original messages, gates, battles and reward commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in texts:
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: new station, train, reviewer and contact directions fit the native font and message window')
