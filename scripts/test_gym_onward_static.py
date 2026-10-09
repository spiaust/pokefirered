"""Verify exact completed-Gym direction additions and native font fit."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
for city,destination,contact,task in [('Oxford','PARIS','CELINE','field task'),('Chantilly','BERLIN','LENA','delivery'),('Oranienburg','LONDON or OXFORD',None,None)]:
 b=(r/f'data/maps/Europe{city}Gym/scripts.inc').read_bytes();old=(r/f'data/geography/gym-onward-{city.lower()}-v138.inc').read_bytes()
 start=f'Europe{city}Gym_Text_Complete::'.encode();end=f'Europe{city}Gym_Text_Full::'.encode();a=b.index(start);z=b.index(end,a);oa=old.index(start);oz=old.index(end,oa)
 assert b[:a]+old[oa:oz]+b[z:]==old
 lines=['Exit GYM; station east of square.\\n',f'Take a train to {destination}.\\p']
 if contact:lines += [f'{contact}: west of the {destination} guide.\\n',f'She can explain your next {task}.$']
 else:lines += ['River landing: east of town square.\\n','Talk to the captain by the water.$']
 extra=''.join(f'\t.string "{line}"\r\n' for line in lines).encode()
 assert b[a:z]==old[oa:oz].replace(b'.$"',b'.\\p"').replace(b'!$"',b'!\\p"')+extra
 texts+=re.findall(rb'\.string "([^"]+)"',extra)
print('PASS: exact completed-Gym text additions preserve previous messages, scripts, battles, badges and one-time TM rewards')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in texts:
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: next-country contacts, east-station trains and river landing directions fit the native font and message window')
