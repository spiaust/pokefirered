"""Eastern host additions preserve native commands, original pages and font fit."""
from pathlib import Path
import re

r=Path(__file__).resolve().parents[1]
rows=[('EuropeLondonReadingRoom','build-london-reading-room.py','HostText'),
      ('EuropeParisGardenRoom','build-paris-garden-room.py','HostText'),
      ('EuropeBerlinGardenRoom','build-berlin-garden-room.py','GardenerText')]
font=(r/'src/text.c').read_text()
widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
for name,gen,label in rows:
    old=(r/'data/geography'/(name+'-v117.inc')).read_bytes()
    new=(r/'data/maps'/name/'scripts.inc').read_bytes()
    pattern=rb'('+name.encode()+b'_'+label.encode()+rb'::\s*)(.*?)(?=\r?\nEurope)'
    a=re.search(pattern,old,re.S);b=re.search(pattern,new,re.S)
    oldlines=re.findall(rb'\.string "(.*?)"',a[2]);newlines=re.findall(rb'\.string "(.*?)"',b[2])
    assert len(oldlines)==4 and len(newlines)==6 and oldlines[:3]==newlines[:3]
    assert oldlines[3][:-1]+b'\\p'==newlines[3]
    assert old[:a.start(2)]+old[a.end(2):]==new[:b.start(2)]+new[b.end(2):]
    generator=(r/'scripts'/gen).read_bytes()
    for line in newlines:
        if name=='EuropeBerlinGardenRoom':
            assert b"'"+re.split(rb'\\[np]|\$',line)[0]+b"'" in generator
        else:
            assert b'.string "'+line.replace(b'\\',b'\\\\')+b'"' in generator
        for text in re.split(rb'\\[np]|\$',line):
            assert sum(widths[chars[c]] for c in text.decode())<=216,text
print('PASS: only three eastern host final pages added; original pages, commands and generators preserved')
print('PASS: every eastern host dialogue line fits the actual native font and 216-pixel text window')
