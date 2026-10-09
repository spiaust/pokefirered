from pathlib import Path
import re
r=Path(__file__).resolve().parents[1];texts=[]
changes=[('data/scripts/europe_dock_check.inc', 'dock-account-v167.inc', 'EuropeDockCheck_Text_', 'Unlocked', 'Rest', ['CELEBI waits beside the captain.\\n', 'Ask to return to your own time.\\p', 'Go north to CHANTILLY station.\\n', 'Take the OXFORD train to ADA.\\p', 'ADA waits east of the OXFORD guide.\\n', 'Tell her about the port reception.$']), ('data/scripts/europe_port_account.inc', 'port-account-v167.inc', 'EuropePortAccount_Text_', 'Archived', 'Later', ['In the forest, speak to CELEBI.\\n', 'Choose LE HAVRE to revisit the port.$'])]
for path,backup,prefix,name,end,lines in changes:
 b=(r/path).read_bytes();old=(r/'data/geography'/backup).read_bytes();a=b.index((prefix+name+'::').encode());z=b.index((prefix+end+'::').encode(),a);oa=old.index((prefix+name+'::').encode());oz=old.index((prefix+end+'::').encode(),oa)
 extra=''.join(f'\t.string "{s}"\r\n' for s in lines).encode();assert b[a:z]==old[oa:oz].replace(b'$"',b'\\p"')+extra and b[a:z].count(b'$"')==1
 assert b[:a]+old[oa:oz]+b[z:]==old;texts+=lines
print('PASS: exact dock completion/port account reminder additions preserve task commands, rewards and travel gates')
font=(r/'src/text.c').read_text();widths=list(map(int,re.findall(r'\b\d+\b',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',font,re.S)[1])))
chars={m[1]:int(m[2],16) for m in re.finditer(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(r/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
for s in texts:
 for line in re.split(r'\\[npl]|\$',s):assert sum(widths[chars[c]] for c in line)<=216,line
print('PASS: Ada return and Celebi direct port directions fit native font and message window')
