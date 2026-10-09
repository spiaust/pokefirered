"""Exact rival preparation text scope and native font widths."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_story.inc').read_bytes();old=(r/'data/geography/england-rival-prep-v145.inc').read_bytes()
insert=b'\t.string "Need to heal? Choose NO for now.\\n"\r\n\t.string "The clinic is west of the square.\\p"\r\n'
extra=b'\t.string "Clinic: west side of town square.\\n"\r\n\t.string "Talk to the nurse to heal for free.\\p"\r\n\t.string "Return here when your team is ready.\\n"\r\n\t.string "Our battle will wait for you.$"\r\n'
a=b.index(b'EuropeStory_Text_BattleDecline::');z=b.index(b'EuropeStory_Text_BattleIntro::',a);oa=old.index(b'EuropeStory_Text_BattleDecline::');oz=old.index(b'EuropeStory_Text_BattleIntro::',oa)
assert b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
rest=b[:a]+old[oa:oz]+b[z:];assert rest.count(insert)==1 and rest.replace(insert,b'')==old
print('PASS: exact offer/decline text additions preserve native optional Yes/No battle, trainer team, wins, report and reward logic')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in re.findall(rb'\.string "([^"]+)"',insert+extra):
 for line in re.split(r'\\[npl]|\$',s.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: pre-battle clinic and free-healing instructions fit the native font and message window')
