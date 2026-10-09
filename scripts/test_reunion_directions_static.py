"""Exact refuge reminder additions and native font widths."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_reunion.inc').read_bytes();old=(r/'data/geography/reunion-directions-v158.inc').read_bytes();texts=[]
changes={'Reminder': ('Decline', ['MIRA waits east of NORA.\\n', 'The porter is southeast of MIRA.$']), 'Verified': ('Reunite', ['MIRA waits east of me.\\n', 'Tell her both reports are checked.$'])}
for name,(end,lines) in reversed(list(changes.items())):
 a=b.index(f'EuropeReunion_Text_{name}::'.encode());z=b.index(f'EuropeReunion_Text_{end}::'.encode(),a);oa=old.index(f'EuropeReunion_Text_{name}::'.encode());oz=old.index(f'EuropeReunion_Text_{end}::'.encode(),oa)
 extra=''.join(f'\t.string "{s}"\r\n' for s in lines).encode();assert b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
 b=b[:a]+old[oa:oz]+b[z:];texts+=lines
assert b==old
print('PASS: exact Meowth reunion reminder additions preserve all task stages, witness verification, travel and onward chapter commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in texts:
 for line in re.split(r'\\[npl]|\$',s):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Mira and porter reunion directions fit native font and message window')
