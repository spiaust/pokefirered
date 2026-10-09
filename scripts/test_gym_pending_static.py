"""Verify exact pending-reward text scope and native font fit."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
for city in ['Oxford','Chantilly','Oranienburg']:
 b=(r/f'data/maps/Europe{city}Gym/scripts.inc').read_bytes();old=(r/f'data/geography/gym-pending-{city.lower()}-v137.inc').read_bytes()
 start=f'Europe{city}Gym_Text_Full::'.encode();end=f'Europe{city}Gym_Text_NotReady::'.encode()
 a=b.index(start);z=b.index(end,a);oa=old.index(start);oz=old.index(end,oa)
 assert b[:a]+old[oa:oz]+b[z:]==old
 extra=('\t.string "Check BAG\'s KEY ITEMS pocket.\\n"\r\n'
 '\t.string "A TM CASE holds your TM rewards.\\p"\r\n'
 '\t.string "If you already have this TM,\\n"\r\n'
 '\t.string "use or give one copy to make room.\\p"\r\n'
 '\t.string "Return here for your waiting TM.\\n"\r\n'
 '\t.string "No rematch needed. Your badge stays!$"\r\n').encode()
 assert b[a:z]==old[oa:oz].replace(b'.$"',b'.\\p"')+extra
 texts+=re.findall(rb'\.string "([^"]+)"',extra)
print('PASS: exact pending-TM text additions preserve all original Gym gates, battles, badges, reward commands and other messages')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in texts:
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: new TM Case, stack room-making and no-rematch instructions fit the native font and message window')
