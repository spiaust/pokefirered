"""Regional Places text fits the native map and changes only two entries."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
def entries(t):
 b=t.split('static const u8 sPlacesLines[][4][44] = {',1)[1].split('\n};',1)[0]
 return re.findall(r'\{(.*?)\}',b,re.S)
now=(r/'src/europe_map.c').read_text();old=(r/'.local-tools/europe-map-before-v179.c').read_text()
a,b=entries(now),entries(old);assert len(a)==len(b)==8
for i in range(8):assert (a[i]!=b[i])==(i in (6,7))
rest=now
for i in (6,7):rest=rest.replace(a[i],b[i],1)
assert rest==old
print('PASS: only Dover and Calais Places entries change; all navigation code and other pages are exact')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontSmallLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
for i,city in [(6,'Dover'),(7,'Calais')]:
 lines=re.findall(r'_\("([^"]+)"\)',a[i]);assert len(lines)==4
 assert all(len(t)+1<=44 and sum(widths[chars[c]] for c in t)<=216 for t in lines)
 print(f'PASS: {city} four landmark/direction lines fit native array and map text width')
