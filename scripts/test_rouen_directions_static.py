"""Exact refuge reminder additions and native font widths."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/maps/EuropeRouenPast/scripts.inc').read_bytes();old=(r/'data/geography/rouen-directions-v161.inc').read_bytes();texts=[]
changes={'Journey': ('Return', ['LEON waits northwest of south guide.\\n', 'Speak to him to record your arrival.$']), 'Welcomed': ('Notice', ['Speak to me again if you can help.\\n', 'Our route book is still missing.$'])}
for name,(end,lines) in reversed(list(changes.items())):
 a=b.index(f'EuropeRouen_Text_{name}::'.encode());z=b.index(f'EuropeRouen_Text_{end}::'.encode(),a);oa=old.index(f'EuropeRouen_Text_{name}::'.encode());oz=old.index(f'EuropeRouen_Text_{end}::'.encode(),oa)
 extra=''.join(f'\t.string "{s}"\r\n' for s in lines).encode();assert b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
 b=b[:a]+old[oa:oz]+b[z:];texts+=lines
assert b==old
print('PASS: exact Rouen arrival reminder additions preserve all task stages, arrival registration, travel and onward chapter commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in texts:
 for line in re.split(r'\\[npl]|\$',s):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Leon arrival and optional route book directions fit native font and message window')
