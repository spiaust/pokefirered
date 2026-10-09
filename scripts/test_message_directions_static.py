"""Exact refuge reminder additions and native font widths."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];b=(r/'data/scripts/europe_message.inc').read_bytes();old=(r/'data/geography/message-directions-message-v153.inc').read_bytes();texts=[]
changes={'Directions': ('Decline', ['Return guide: west of the dispatcher.\\n', "Keeper: north of CELEBI's arrival.$"]), 'KeeperDone': ('Reply', ['Station-post guide: southeast corner.\\n', 'Read the board to reach BEAUVAIS.\\p', 'ELISE: east of reception entrance.\\n', 'Speak to her to deliver my reply.$']), 'Report': ('EliseDone', ['CELEBI by the entrance leads home.\\n', 'Then take a train to OXFORD.\\p', 'ADA waits east of the town guide.\\n', 'Tell her about both messages.$'])}
for name,(end,lines) in reversed(list(changes.items())):
 a=b.index(f'EuropeMessage_Text_{name}::'.encode());z=b.index(f'EuropeMessage_Text_{end}::'.encode(),a);oa=old.index(f'EuropeMessage_Text_{name}::'.encode());oz=old.index(f'EuropeMessage_Text_{end}::'.encode(),oa)
 extra=''.join(f'\t.string "{s}"\r\n' for s in lines).encode();assert b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
 b=b[:a]+old[oa:oz]+b[z:];texts+=lines
assert b==old
for name,oldline,newline in [('time',b'Please speak to him about EEVEE.',b'Please speak to her about EEVEE.'),('departure',b'Tell him the confirmed station news.',b'Tell her the confirmed station news.')]:
 previous=(r/f'data/geography/message-directions-{name}-v153.inc').read_bytes();current=(r/f'data/scripts/europe_{name}.inc').read_bytes();assert previous.count(oldline)==1 and current==previous.replace(oldline,newline)

print('PASS: exact message-direction additions and two keeper pronouns preserve all task, reward and travel commands')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in texts:
 for line in re.split(r'\\[npl]|\$',s):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Message delivery, reply and Ada account directions fit native font and message window')
