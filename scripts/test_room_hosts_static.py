"""Host additions preserve commands and the original two dialogue pages."""
from pathlib import Path
import re

r=Path(__file__).resolve().parents[1]
for city in ['London','Paris','Berlin']:
    old=(r/'data/geography'/('host-'+city.lower()+'-v116.inc')).read_bytes()
    new=(r/'data/maps'/('Europe'+city+'Home')/'scripts.inc').read_bytes()
    pattern=rb'(Europe'+city.encode()+rb'Home_HostText::\s*)(.*?)(?=\r?\nEurope)'
    a=re.search(pattern,old,re.S); b=re.search(pattern,new,re.S)
    assert a and b
    oldlines=re.findall(rb'\.string "(.*?)"',a[2])
    newlines=re.findall(rb'\.string "(.*?)"',b[2])
    assert len(oldlines)==4 and len(newlines)==6
    assert oldlines[:3]==newlines[:3] and oldlines[3][:-1]+b'\\p'==newlines[3]
    assert old[:a.start(2)]+old[a.end(2):]==new[:b.start(2)]+new[b.end(2):]
    generator=(r/'scripts'/('build-'+city.lower()+'-home.py')).read_bytes()
    for line in newlines:
        assert b'.string "'+line.replace(b'\\',b'\\\\')+b'"' in generator
print('PASS: three host final pages added; original pages, all commands and generator text preserved')
