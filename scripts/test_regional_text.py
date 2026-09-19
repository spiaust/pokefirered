"""Keep new regional sign lines within the game's 216-pixel dialogue window."""
import re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
font=(R/'src/text.c').read_text();body=re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S).group(1);widths=list(map(int,re.findall(r'\b\d+\b',body)))
chars={m.group(1):int(m.group(2),16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(encoding='utf-8'),re.M)}
chars["'"]=chars.get('’',0xb4)
for city in sys.argv[1:] or ['Oxford','Chantilly','Oranienburg']:
 text=(R/f'data/maps/Europe{city}/scripts.inc').read_text().split(f'Europe{city}_Realism',1)[1]
 biggest=0
 for line in re.findall(r'\.string "(.*?)"',text):
  for part in re.split(r'\\[npl]|\$',line):
   w=sum(widths[chars[c]] for c in part);biggest=max(biggest,w);assert w<=216,(city,w,part)
 print(f'PASS: {city} sign lines fit the dialogue window (maximum {biggest}px)')

