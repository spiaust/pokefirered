"""Travel-board shortcut help preserves all item/map/save commands."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
old=(r/'data/geography/navigation-v120.inc').read_bytes()
new=(r/'data/scripts/europe_navigation.inc').read_bytes()
prefix=b'EuropeNavigation_Text_Board::'
assert old.split(prefix)[0]==new.split(prefix)[0]
a=re.findall(rb'\.string "(.*?)"',old.split(prefix)[1])
b=re.findall(rb'\.string "(.*?)"',new.split(prefix)[1])
assert len(a)==3 and len(b)==7 and a[:2]==b[:2]
assert a[2][:-1]+b'\\p'==b[2]
assert b[3:]==[b'In BAG, choose KEY ITEMS and\\n',b'TOWN MAP, then REGISTER.\\p',b'SELECT opens your map in the field.\\n',b'On the map, SELECT opens STORY.$']
font=(r/'src/text.c').read_text()
widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
for line in b:
    for text in re.split(rb'\\[np]|\$',line):
        assert sum(widths[chars[c]] for c in text.decode())<=216,text
print('PASS: only two travel-board dialogue pages added; all existing pages, item grants, map calls and save behavior exact')
print('PASS: all travel-board instruction lines fit the native font and text window')
