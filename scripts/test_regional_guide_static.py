"""Remaining-trainer branches preserve all original gates and rewards."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
for city,local,extended in [('Oxford','OLIVER','ALICE'),('Chantilly','CAMILLE','LUCIE'),('Oranienburg','FELIX','OTTO')]:
 b=(r/f'data/maps/Europe{city}/scripts.inc').read_bytes();marker=f'\r\nEuropeChallenge_{city}_NeedExtended::'.encode()
 assert b.count(marker)==1;body,extra=b.split(marker)
 branches=(f'\tgoto_if_defeated TRAINER_EUROPE_{local}, EuropeChallenge_{city}_NeedExtended\r\n'+f'\tgoto_if_defeated TRAINER_EUROPE_{extended}, EuropeChallenge_{city}_NeedLocal\r\n').encode()
 assert body.count(branches)==1 and body.replace(branches,b'')==(r/f'data/geography/regional-guide-{city.lower()}-v134.inc').read_bytes()
 assert body.index(f'goto_if_eq VAR_0x8005, 2, EuropeChallenge_{city}_Reward'.encode())<body.index(branches)
 for kind,trainer in [('Extended',extended),('Local',local)]:
  label=f'EuropeChallenge_{city}_Need{kind}'
  assert f'\tmsgbox {label}Text\r\n\trelease\r\n\tend'.encode() in extra
  assert f'Next: {trainer} in '.encode() in extra
 assert not any(cmd in extra for cmd in [b'\tsetvar',b'\tgiveitem',b'\tsetflag',b'\ttrainerbattle'])
 texts+=re.findall(rb'\.string "([^"]+)"',extra)
print('PASS: remaining-trainer branches come after original two-win reward gate; original scripts restore exactly and new dialogues cannot grant items or progress')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in texts:
 for line in re.split(r'\\[npl]|\$',text.decode().replace('{STR_VAR_1}','1')):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: all six remaining-opponent messages and directions fit the native font and message window')
