from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];t=(r/'src/europe_tour_journal.c').read_text();old=(r/'.local-tools/tour-before-v183.c').read_text()
changes=[('Both required trail matches are won.','Your rival waits west of the town guide.'),('Enter OXFORD GYM north of the square.','North of OXFORD square: walk in the door.'),('Enter the GYM north of CHANTILLY\'s square.','North of town square: walk in the door.'),('Enter the GYM north of the town square.','North of town square: walk in the door.')]
for a,b in changes:old=old.replace(a,b,1)
assert t==old
print('PASS: only four rival/Gym direction lines change; all lead selection, milestones and other text remain exact')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontSmallLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for a,b in changes:assert len(b)+1<=44 and sum(widths[chars[c]] for c in b)<=216
print('PASS: all four changed direction lines fit native journal font/window and array')
