"""Only three report-back lead lines change; progression selection stays exact."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
old=(R/'data/geography/tour-journal-v112.c').read_bytes()
new=(R/'src/europe_tour_journal.c').read_bytes()
pairs=[('Tell him about your rival match.','Collect his reward to battle ELLIS.'),('Give her the reviewed survey.','Collect her reward to battle MARINE.'),('Tell her the parts reached KARL.','Collect her reward to battle CONRAD.')]
for before,after in pairs:
 assert old.count(before.encode())==1
 old=old.replace(before.encode(),after.encode())
 assert len(after)<44
assert old==new
font=(R/'src/text.c').read_text();body=re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S).group(1)
widths=list(map(int,re.findall(r'\b\d+\b',body)))
chars={m.group(1):int(m.group(2),16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(encoding='utf-8'),re.M)}
for _,line in pairs:assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: exactly three lead lines change; Bag reminders, lead selection, milestones and reward logic remain exact; text fits')
