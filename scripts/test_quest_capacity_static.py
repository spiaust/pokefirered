"""Exact Bag-help additions preserve report and reward progression."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
extra=('\t.string "Open BAG, then the ITEMS pocket.\\n"\r\n'
 '\t.string "Use, give or toss an unneeded item.\\p"\r\n'
 '\t.string "Return here after making room.\\n"\r\n'
 '\t.string "Your report and reward stay safe!$"\r\n').encode()
for country,file,prefix,tag,end in [('England','europe_story.inc','EuropeStory','BagFull',None),('France','europe_france_story.inc','EuropeFrance','BagFull','Gardens'),('Germany','europe_germany_story.inc','EuropeGermany','Full','Delivered')]:
 b=(r/'data/scripts'/file).read_bytes();old=(r/f'data/geography/quest-capacity-{country.lower()}-v141.inc').read_bytes()
 start=f'{prefix}_Text_{tag}::'.encode();a=b.index(start);oa=old.index(start)
 z=b.index(f'{prefix}_Text_{end}::'.encode(),a) if end else len(b);oz=old.index(f'{prefix}_Text_{end}::'.encode(),oa) if end else len(old)
 assert b[:a]+old[oa:oz]+b[z:]==old and b[a:z]==old[oa:oz].replace(b'.$"',b'.\\p"').replace(b'!$"',b'!\\p"')+extra
 assert b[a:z].count(b'$"')==1
 texts+=re.findall(rb'\.string "([^"]+)"',extra)
print('PASS: exact country reward Bag-help text additions preserve original scripts, earned reports, capacity gates and one-time item rewards')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for text in texts:
 for line in re.split(r'\\[npl]|\$',text.decode()):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Items-pocket room-making and safe report/reward instructions fit the native font and message window')
