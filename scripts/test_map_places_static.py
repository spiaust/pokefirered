"""Measure Places text against the actual native font and screen margins."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
font=(R/'src/text.c').read_text();body=re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S).group(1);widths=list(map(int,re.findall(r'\b\d+\b',body)))
chars={m.group(1):int(m.group(2),16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(encoding='utf-8'),re.M)}
s=(R/'src/europe_map.c').read_text();body=s.split('static const u8 sPlacesHeading',1)[1].split('static void DrawEuropePlaces',1)[0]
texts=re.findall(r'_\("([^"\n]*)"\)',body);assert len(texts)==50
for text in texts:assert sum(widths[chars[c]] for c in text)<=216,text
hint=re.search(r'sHelpHint\[\] = _\("([^"]+)"\)',s).group(1)
assert sum(widths[chars[c]] for c in hint)<=108,hint
for label,limit in [('sWorldOptionText6',216),('sPreviewTurn',42)]:
 text=re.search(label+r'\[\] = _\("([^"]+)"\)',s).group(1)
 assert sum(widths[chars[c]] for c in text)<=limit,text
print('PASS: all Places lines and map shortcut hint fit native font and screen margins')
