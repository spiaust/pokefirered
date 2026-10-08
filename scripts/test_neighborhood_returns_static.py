"""Neighborhood sign direction changes leave native logic exact."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
font=(r/'src/text.c').read_text()
widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)}
for city,label,gen,added in [
    ('London','Homes','build-london-map.py',2),
    ('Paris','Homes','build-capital-maps.py',0),
    ('Berlin','Court','build-capital-maps.py',2),
]:
    old=(r/'data/geography'/('neighborhood-'+city.lower()+'-v118.inc')).read_bytes()
    new=(r/'data/maps'/('Europe'+city)/'scripts.inc').read_bytes()
    pattern=rb'(Europe'+city.encode()+b'_Realism'+label.encode()+rb'Text::\s*)(.*?)(?=\r?\nEurope|\Z)'
    a=re.search(pattern,old,re.S);b=re.search(pattern,new,re.S)
    assert a and b
    oldlines=re.findall(rb'\.string "(.*?)"',a[2]);lines=re.findall(rb'\.string "(.*?)"',b[2])
    assert len(lines)==len(oldlines)+added
    if added:
        assert oldlines[:-1]==lines[:len(oldlines)-1]
        assert oldlines[-1][:-1]+b'\\p'==lines[len(oldlines)-1]
    else:
        assert oldlines[:-1]==lines[:-1]
        assert lines[-1]==b'Return west for EIFFEL and bridges.$'
    assert old[:a.start(2)]+old[a.end(2):]==new[:b.start(2)]+new[b.end(2):]
    generator=(r/'scripts'/gen).read_bytes()
    for line in lines:
        text=re.split(rb'\\[np]|\$',line)[0]
        assert b"'"+text+b"'" in generator
        assert sum(widths[chars[c]] for c in text.decode())<=216,text
print('PASS: only three neighborhood signs change; original room listings, commands and generator text preserved')
print('PASS: all neighborhood sign pages fit the actual native font and text window')
