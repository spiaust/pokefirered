"""One starter-help page preserves gifts, choices and arrival commands."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
old=(r/'data/geography/starter-intro-v121.inc').read_bytes()
new=(r/'data/maps/PalletTown_PlayersHouse_2F/scripts.inc').read_bytes()
lines=[b'In KEY ITEMS, REGISTER the BICYCLE.\\n',b'SELECT lets you ride or walk outside.\\p']
addition=b''.join(b'\t.string "'+line+b'"\n' for line in lines)
assert new.count(addition)==1 and new.replace(addition,b'')==old
font=(r/'src/text.c').read_text()
widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
for line in lines:
    text=line[:-2].decode();assert sum(widths[chars[c]] for c in text)<=216,text
print('PASS: only one starter supplies help page added; all starter choices, gifts, welcome and arrival commands exact')
print('PASS: both Bicycle shortcut instruction lines fit the native font and text window')
