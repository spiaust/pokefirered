from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];t=(r/'src/europe_tour_journal.c').read_text();old=(r/'.local-tools/tour-before-v185.c').read_text()
changes=[('north of LONDON.', 'North of LONDON; east of the main path.'), ('south of OXFORD.', 'South of OXFORD; east of the main path.')]
for a,b in changes:old=old.replace(a,b,1)
assert t==old
print('PASS: only two trainer direction lines change; all lead selection, milestones and other text remain exact')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontSmallLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for a,b in changes:assert len(b)+1<=44 and sum(widths[chars[c]] for c in b)<=216
print('PASS: all two changed direction lines fit native journal font/window and array')
