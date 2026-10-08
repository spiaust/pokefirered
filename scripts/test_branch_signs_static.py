"""Only the three existing station entrance text blocks may change."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1]
b=json.loads((R/'data/geography/branch-signs-v110.json').read_text())
for path,old in b.items():
 if path=='unchanged':continue
 current=(R/path).read_text()
 if path.endswith('scripts.inc'):
  city=path.split('/Europe')[1].split('/')[0]
  pattern=re.escape(f'Europe{city}_Text_Station::')+r'\n(?:[ \t]*\.string[^\n]*\n)+'
  before=re.search(pattern,old).group();after=re.search(pattern,current).group()
  assert before.replace('$',r'\p').strip() in after
  assert 'GYM: north of the town square.' in after
  assert {'Oxford':'ADA','Chantilly':'REMY','Oranienburg':'KARL'}[city]+' waits' in after
  assert re.sub(pattern,'STATION_TEXT\n',old)==re.sub(pattern,'STATION_TEXT\n',current),path
 else:assert current==old,path
for path,digest in b['unchanged'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,path
print('PASS: only three station text blocks change; original ticket guidance, maps, terrain, events, IDs and rail scripts retained')
