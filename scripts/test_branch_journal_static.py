from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];t=(r/'src/europe_tour_journal.c').read_text();old=(r/'.local-tools/tour-before-v184.c').read_text()
changes=[('Both habitat observations are saved.', 'REMY waits west of the town guide.'), ("You are carrying LENA's repair parcel.", 'KARL waits west of the town guide.'), ('It does not need a Bag slot.', 'Your parcel does not need a Bag slot.')]
for a,b in changes:old=old.replace(a,b,1)
assert t==old
print('PASS: only three branch-contact direction lines change; all lead selection, milestones and other text remain exact')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontSmallLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for a,b in changes:assert len(b)+1<=44 and sum(widths[chars[c]] for c in b)<=216
print('PASS: all three changed direction lines fit native journal font/window and array')
