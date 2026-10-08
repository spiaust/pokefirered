"""Post-victory local trainer directions change only intended text."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
old=b'\t.string "each country\'s countryside.$"'
for city,town,trail,trainer in [('London','OXFORD','OXFORD TRAIL','ALICE'),('Paris','CHANTILLY','CHANTILLY FOREST','LUCIE'),('Berlin','ORANIENBURG','HAVEL TRAIL','OTTO')]:
 b=(r/f'data/maps/Europe{city}Countryside/scripts.inc').read_bytes()
 extra=('\t.string "each country\'s countryside.\\p"\r\n'+f'\t.string "Head north to {trail}.\\n"\r\n'+f'\t.string "Meet {trainer} for an optional match.\\p"\r\n'+f'\t.string "{town} guide: one RARE CANDY.\\n"\r\n'+'\t.string "Win both matches to claim the reward.$"').encode()
 assert b.count(extra)==1 and b.replace(extra,old)==(r/f'data/geography/trainer-onward-{city.lower()}-v132.inc').read_bytes()
 texts+=re.findall(rb'\.string "([^"]+)"',extra)
print('PASS: exact post-victory text additions preserve all previous messages, battle commands, teams, gates and rewards')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in texts:
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: named trails, optional opponents, town guides and reward directions fit the native font and window')
