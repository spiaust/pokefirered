"""Exact accepted-message additions preserve country quest logic."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
for country,end,lines in [
 ('France','FirstBadge',['FRENCH GARDENS: leave PARIS north.\\n','Study marker: west of the main path.\\p','CHANTILLY FOREST: south of town.\\n','Its study marker is west of the path.$']),
 ('Germany','Directions',['Station: east side of BERLIN square.\\n','Take a train to ORANIENBURG.\\p','Or walk north through the two routes.\\n','KARL waits west of the town guide.$'])]:
 b=(r/f'data/scripts/europe_{country.lower()}_story.inc').read_bytes();old=(r/f'data/geography/quest-accepted-{country.lower()}-v139.inc').read_bytes()
 start=f'Europe{country}_Text_Accepted::'.encode();stop=f'Europe{country}_Text_{end}::'.encode();a=b.index(start);z=b.index(stop,a);oa=old.index(start);oz=old.index(stop,oa)
 assert b[:a]+old[oa:oz]+b[z:]==old
 extra=''.join(f'\t.string "{line}"\r\n' for line in lines).encode()
 assert b[a:z]==old[oa:oz].replace(b'.$"',b'.\\p"')+extra
 texts+=re.findall(rb'\.string "([^"]+)"',extra)
print('PASS: exact accepted-quest text additions preserve all original country scripts, gates, stages, markers, cargo and rewards')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in texts:
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: new survey-marker and courier travel directions fit the native font and message window')
