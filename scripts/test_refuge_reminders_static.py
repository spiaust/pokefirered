"""Exact refuge reminder additions and native font widths."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_time.inc').read_bytes();old=(r/'data/geography/refuge-reminders-v150.inc').read_bytes();texts=[]
changes={'AskKeeper':('Welcome',['The keeper stands just west of me.\\n','Please speak to him about EEVEE.$']),'Welcome':('Blanket',['ELISE waits just east of me.\\n','Speak to her about her EEVEE.$']),'Carry':('Deliver',['I have given you EEVEE\'s blanket.\\n','Please bring it to ELISE, east of me.$'])}
for name,(end,lines) in reversed(list(changes.items())):
 a=b.index(f'EuropeTime_Text_{name}::'.encode());z=b.index(f'EuropeTime_Text_{end}::'.encode(),a);oa=old.index(f'EuropeTime_Text_{name}::'.encode());oz=old.index(f'EuropeTime_Text_{end}::'.encode(),oa)
 extra=''.join(f'\t.string "{s}"\r\n' for s in lines).encode();assert b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
 b=b[:a]+old[oa:oz]+b[z:];texts+=lines
assert b==old
print('PASS: exact three refuge reminder additions preserve all task stages, blanket handoff, travel and onward chapter commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in texts:
 for line in re.split(r'\\[npl]|\$',s):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Elise, keeper and carried-blanket directions fit native font and message window')
